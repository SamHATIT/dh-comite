#!/usr/bin/env python3
"""Releve consolide des couts LLM et infrastructure — toutes sources.

POURQUOI (12/08) : Sam a releve, a juste titre, que mes estimations sous-estiment
systematiquement. Le 11/08 j'ai annonce ~4 USD pour les rondes du matin ; le reel
etait 21 USD. Facteur cinq.

La cause est structurelle : chaque source a son propre compteur, et j'en citais un
seul en croyant citer le tout. Ce script les additionne et — surtout — AFFICHE CE
QU'IL NE MESURE PAS. Un chiffre incomplet presente comme complet est pire qu'une
absence de chiffre.

Sources couvertes :
  1. Pipeline SDS/BUILD   table llm_interactions (base plateforme)
  2. Comite               fichiers JSON de dh-comite (modelUsage.costUSD)
  3. n8n                  comptage des executions appelant un modele
  4. GPU                  a saisir a la main, la plateforme ne l expose pas

Usage : couts-consolides.py [--jours 30]
"""
import json, glob, os, subprocess, sys
from datetime import datetime, timedelta, timezone

JOURS = int(sys.argv[sys.argv.index("--jours")+1]) if "--jours" in sys.argv else 30
DEPUIS = datetime.now(timezone.utc) - timedelta(days=JOURS)
PLAT = "postgresql://digital_humans:DH_SecurePass2025!@127.0.0.1:5432/digital_humans_db"

# Tarifs au 12/08/2026. La hausse Sonnet du 01/09 a ete ANNULEE le 10/08 :
# 2/10 est desormais le prix standard, pas un tarif d introduction.
TARIFS = {"opus": (5, 25), "sonnet": (2, 10), "haiku": (1, 5), "fable": (10, 50)}

def sql(q):
    r = subprocess.run(["psql", PLAT, "-tAF", "|", "-c", q], capture_output=True, text=True)
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]

def pipeline():
    q = f"""SELECT coalesce(agent_id,'?'), coalesce(model,'?'), count(*),
            coalesce(sum(tokens_input),0), coalesce(sum(tokens_output),0)
            FROM llm_interactions WHERE created_at > now() - interval '{JOURS} days'
            GROUP BY 1,2"""
    total, sans_entree, lignes = 0.0, 0, []
    for agent, modele, n, tin, tout in sql(q):
        pi, po = next((v for k, v in TARIFS.items() if k in modele.lower()), (2, 10))
        c = (int(tin)*pi + int(tout)*po) / 1e6
        if int(tin) == 0 and int(tout) > 0:
            sans_entree += int(n)
        total += c
        lignes.append((agent, int(n), c))
    return total, sorted(lignes, key=lambda x: -x[2]), sans_entree

def comite():
    total, n = 0.0, 0
    for f in glob.glob("/root/workspace/dh-comite/*/*.json"):
        if datetime.fromtimestamp(os.path.getmtime(f), timezone.utc) < DEPUIS:
            continue
        try: d = json.load(open(f))
        except Exception: continue
        if not isinstance(d, dict): continue
        c = sum((u or {}).get("costUSD", 0) or 0 for u in (d.get("modelUsage") or {}).values())
        if c: total, n = total + c, n + 1
    return total, n

def n8n_llm():
    import sqlite3
    try:
        c = sqlite3.connect("/root/.n8n/database.sqlite")
        q = f"""select count(*) from execution_entity e join workflow_entity w on w.id=e."workflowId"
                where e."startedAt" > datetime('now','-{JOURS} days')
                and (w.name like '%Gemini%' or w.name like '%Blog%')"""
        return c.execute(q).fetchone()[0]
    except Exception:
        return None

def main():
    p, lignes, sans_entree = pipeline()
    c, nc = comite()
    n8 = n8n_llm()

    # Mode machine, pour le cockpit. Les trous de mesure sont dans la charge utile,
    # pas en commentaire : une interface qui affiche 246 USD sans dire ce qui manque
    # reproduit exactement l erreur que ce script corrige.
    if "--json" in sys.argv:
        print(json.dumps({
            "periode_jours": JOURS,
            "mesure_usd": round(p + c, 2),
            "postes": [
                {"nom": "Comite (rondes et briefs)", "usd": round(c, 2), "executions": nc},
                {"nom": "Pipeline SDS/BUILD", "usd": round(p, 2),
                 "detail": [{"agent": a, "appels": n, "usd": round(cc, 2)} for a, n, cc in lignes]},
            ],
            "non_mesure": [
                {"poste": "Appels sans jetons d entree traces",
                 "detail": f"{sans_entree} appels, surtout Raj — cout inconnu, pas nul",
                 "chiffrable": False},
                {"poste": "Embeddings OpenAI du RAG",
                 "detail": "aucun compteur ; chaque recherche d Emma appelle text-embedding-3-large",
                 "chiffrable": False},
                {"poste": "Sessions Claude Code de developpement",
                 "detail": "hors de toute base — plus gros poste manquant",
                 "chiffrable": False},
                {"poste": "n8n / Google",
                 "detail": f"{n8} executions de workflows appelant un modele",
                 "chiffrable": False},
                {"poste": "GPU Packet.ai",
                 "detail": "0,66 USD/h, a relever sur le tableau de bord du fournisseur",
                 "chiffrable": False},
            ],
            "avertissement": ("Chiffre PARTIEL. Ecart constate avec la facture reelle le "
                              "11/08 : environ 185 USD/mois. Ne pas presenter comme un total."),
        }, ensure_ascii=False))
        return

    L = 62
    print("=" * L)
    print(f"RELEVE CONSOLIDE — {JOURS} derniers jours".center(L))
    print("=" * L)
    print(f"\n  Pipeline SDS/BUILD          {p:8.2f} USD")
    for a, n, cc in lignes[:6]:
        print(f"      {a:<22} {n:4} appels   {cc:6.2f}")
    print(f"\n  Comite (rondes + briefs)    {c:8.2f} USD   {nc} executions")
    print(f"\n  MESURE                      {p+c:8.2f} USD")
    print("\n" + "-" * L)
    print("CE QUI N EST PAS DANS CE CHIFFRE")
    print("-" * L)
    if sans_entree:
        print(f"  · {sans_entree} appels sans jetons d entree traces (Raj surtout).")
        print(f"    Leur cout d entree est INCONNU, pas nul.")
    print(f"  · Embeddings OpenAI du RAG : aucun compteur. Chaque recherche")
    print(f"    d Emma appelle text-embedding-3-large sans laisser de trace.")
    print(f"  · Sessions Claude Code de developpement : hors de toute base.")
    print(f"    C est le plus gros poste manquant.")
    if n8 is not None:
        print(f"  · n8n : {n8} executions de workflows appelant un modele sur")
        print(f"    la periode. Facture chez Google, non interrogeable ici.")
    print(f"  · GPU Packet.ai : 0,66 USD/h, a relever sur leur tableau de bord.")
    print("\n  Pour un chiffre complet, comparer a la facture reelle des")
    print("  fournisseurs. L ecart constate le 11/08 etait de ~185 USD/mois.")
    print("=" * L)

if __name__ == "__main__":
    main()
