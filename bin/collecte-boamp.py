#!/usr/bin/env python3
"""Collecte BOAMP -> table signaux_collecte (BRUTE, non qualifiee).

POURQUOI (12/08) : le workflow n8n existe mais n'a jamais tourne — il lui manque
une version publiee, et la CLI refuse de l'activer. Ce script fait le meme travail
sans n8n, et alimente la table de collecte creee le 11/08.

CE QU'IL N'EST PAS : un qualifieur. Il ecrit TOUT ce que le BOAMP renvoie, bruit
compris. C'est voulu. Le test du 11/08 a montre qu'un avis sur cinq seulement
concerne un CRM — les quatre autres (consommables de laboratoire, traiteur,
nettoyage) sont exactement les exemples NEGATIFS qui manquent au jeu de donnees.
Les 112 signaux existants vont de 6 a 9, sans aucun mauvais exemple.

RIEN NE PASSE EN signaux_publics SANS QUALIFICATION HUMAINE.

Usage : collecte-boamp.py [--jours 90] [--limite 100] [--dry]
"""
import json, sys, urllib.parse, urllib.request, subprocess, datetime, os

API = "https://www.boamp.fr/api/explore/v2.1/catalog/datasets/boamp/records"
DSN = "postgresql://digital_humans:DH_SecurePass2025!@127.0.0.1:5432/digital_humans_db"
TERMES = ['salesforce', 'Sales Cloud', 'Service Cloud', 'CRM', 'gestion relation client']

def arg(nom, defaut):
    return sys.argv[sys.argv.index(nom)+1] if nom in sys.argv else defaut

def recuperer(jours, limite):
    where = " OR ".join(f'search("{t}")' for t in TERMES)
    depuis = (datetime.date.today() - datetime.timedelta(days=int(jours))).isoformat()
    where = f'({where}) AND dateparution >= "{depuis}"'
    vus, sortie = set(), []
    for offset in range(0, int(limite), 100):
        q = urllib.parse.urlencode({"where": where, "limit": min(100, int(limite)-offset),
                                    "offset": offset, "order_by": "dateparution desc"})
        with urllib.request.urlopen(f"{API}?{q}", timeout=30) as r:
            res = json.load(r).get("results") or []
        if not res: break
        for x in res:
            ref = str(x.get("idweb") or x.get("id") or "")
            if not ref or ref in vus: continue
            vus.add(ref)
            sortie.append(x)
    return sortie

def esc(v):
    return "NULL" if v is None else "'" + str(v).replace("'", "''")[:2000] + "'"

def main():
    avis = recuperer(arg("--jours", 90), arg("--limite", 200))
    print(f"{len(avis)} avis recuperes")
    if "--dry" in sys.argv:
        for a in avis[:8]:
            print(" ", str(a.get('dateparution'))[:10], "|", str(a.get('nomacheteur'))[:34],
                  "|", str(a.get('objet'))[:58])
        return
    lignes = []
    for a in avis:
        lignes.append("(" + ",".join([
            esc("appel_offres"), esc("BOAMP"),
            esc(a.get("url_avis") or f"https://www.boamp.fr/avis/detail/{a.get('idweb')}"),
            esc(str(a.get("dateparution"))[:10]),
            esc(a.get("objet")), esc(a.get("nomacheteur") or "Acheteur non precise"),
            esc(a.get("datelimitereponse")), esc(a.get("idweb")),
            esc(json.dumps({k: a.get(k) for k in ("descripteur_libelle","type_marche","famille_libelle")}, ensure_ascii=False)),
        ]) + ")")
    sql = ("INSERT INTO signaux_collecte (signal_type,signal_source,signal_url,signal_date,"
           "signal_resume,entreprise,echeance,reference,brut) VALUES " + ",".join(lignes) +
           " ON CONFLICT (reference) DO NOTHING;")
    p = subprocess.run(["psql", DSN, "-v", "ON_ERROR_STOP=1", "-c", sql],
                       capture_output=True, text=True)
    print(p.stdout.strip() or p.stderr.strip()[:300])
    n = subprocess.run(["psql", DSN, "-tAc", "select count(*) from signaux_collecte"],
                       capture_output=True, text=True).stdout.strip()
    print(f"total en base : {n}")

if __name__ == "__main__":
    main()
