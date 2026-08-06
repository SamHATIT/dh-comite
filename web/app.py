"""Comité DH — API lecture seule pour le tableau de bord (V1.1, 14/07/2026)."""
import os, glob
import psycopg2, psycopg2.extras
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

DSN = os.environ["COMITE_DB_DSN"]
RO_DSN = os.environ.get("DEOS_RO_DSN", "")
BASE = "/workspace"
app = FastAPI(title="dh-comite-web", docs_url=None, redoc_url=None)

def q(dsn, sql, args=()):
    with psycopg2.connect(dsn) as c, c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, args)
        return cur.fetchall()

def ops():
    """Exploitation : activité clients (prod RO) + capacité serveur (host)."""
    out = {}
    try:
        a = q(RO_DSN, """SELECT
            count(*) FILTER (WHERE created_at > now()-interval '7 days')  AS exec_7j,
            count(*) FILTER (WHERE created_at > now()-interval '30 days') AS exec_30j,
            max(created_at) AS derniere,
            count(*) FILTER (WHERE completed_at IS NULL AND status NOT IN
              ('COMPLETED','FAILED','CANCELLED','WAITING_BR_VALIDATION')) AS en_cours
            FROM v_deos_executions""")[0]
        u = q(RO_DSN, """SELECT count(DISTINCT p.user_id) AS utilisateurs_30j
            FROM v_deos_projects p JOIN v_deos_executions e ON e.project_id = p.id
            WHERE e.created_at > now()-interval '30 days'""")[0]
        out["activite"] = {"executions_7j": a["exec_7j"], "executions_30j": a["exec_30j"],
                           "en_cours": a["en_cours"],
                           "derniere_execution": a["derniere"].isoformat() if a["derniere"] else None,
                           "utilisateurs_actifs_30j": u["utilisateurs_30j"]}
    except Exception as e:
        out["activite"] = {"erreur": f"prod injoignable: {type(e).__name__}"}
    try:
        with open("/proc/loadavg") as f: l1, l5, l15 = f.read().split()[:3]
        cores = os.cpu_count() or 1
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":")[0], int(line.split()[1])
                if k in ("MemTotal", "MemAvailable"): mem[k] = v
        st = os.statvfs("/workspace")
        disk_pct = round(100 * (1 - st.f_bavail / st.f_blocks), 1)
        out["serveur"] = {"charge": f"{l1} / {l5} / {l15} (sur {cores} vCPU)",
                          "charge_pct": round(float(l5) / cores * 100, 1),
                          "ram_dispo_gb": round(mem.get("MemAvailable", 0)/1048576, 1),
                          "ram_totale_gb": round(mem.get("MemTotal", 0)/1048576, 1),
                          "disque_utilise_pct": disk_pct}
    except Exception as e:
        out["serveur"] = {"erreur": type(e).__name__}
    return out

@app.get("/api/etat")
def etat():
    rows = q(DSN, "SELECT cle, valeur, maj_par, updated_at FROM deos_state")
    state = {r["cle"]: {"valeur": r["valeur"], "maj": r["updated_at"].isoformat(), "par": r["maj_par"]} for r in rows}
    decisions = q(DSN, """SELECT id, statut, origine, texte, recommandation, porte_sur,
                            (now()::date - date::date) AS age_j, date, updated_at
                     FROM decisions
                     WHERE statut NOT IN ('clos','refusee') OR updated_at > now()-interval '7 days'
                     ORDER BY (statut IN ('clos','refusee')), date DESC LIMIT 40""")
    briefs = sorted(glob.glob(f"{BASE}/briefs/brief-*.md") + glob.glob(f"{BASE}/briefs/comite-*.md"), reverse=True)[:14]
    brief_md = ""
    if briefs:
        with open(briefs[0], encoding="utf-8") as f: brief_md = f.read()
    page_suivi = ""
    try:
        with open(f"{BASE}/PageSuivi.md", encoding="utf-8") as f: page_suivi = f.read()
    except FileNotFoundError: pass
    return JSONResponse({
        "state": state,
        "decisions": [dict(d, date=d["date"].isoformat(), updated_at=d["updated_at"].isoformat()) for d in decisions],
        "brief_md": brief_md, "brief_fichier": os.path.basename(briefs[0]) if briefs else None,
        "briefs": [os.path.basename(b) for b in briefs],
        "page_suivi": page_suivi,
        "ops": ops(),
    })

@app.get("/api/brief/{nom}")
def brief(nom: str):
    nom = os.path.basename(nom)
    try:
        with open(f"{BASE}/briefs/{nom}", encoding="utf-8") as f:
            return JSONResponse({"nom": nom, "contenu": f.read()})
    except FileNotFoundError:
        return JSONResponse({"erreur": "brief introuvable"}, status_code=404)

@app.get("/api/dossiers")
def dossiers():
    """Liste les dossiers illustres disponibles."""
    fichiers = sorted(glob.glob(f"{BASE}/briefs/*.docx"), reverse=True)
    return JSONResponse({"dossiers": [os.path.basename(f) for f in fichiers[:30]]})

@app.get("/dossier/{nom}")
def dossier(nom: str):
    """Telecharge un dossier illustre (docx)."""
    from fastapi.responses import FileResponse
    nom = os.path.basename(nom)
    chemin = f"{BASE}/briefs/{nom}"
    if not nom.endswith(".docx") or not os.path.exists(chemin):
        return JSONResponse({"erreur": "dossier introuvable"}, status_code=404)
    return FileResponse(chemin, filename=nom,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# ── GOUVERNANCE — le curseur d'autonomie (CURSEUR-001, 06/08/2026)
# Page N1 au meme gabarit que les six directions : en-tete, 4 indicateurs
# maximum, puis le detail. Elle montre l'ECART entre ce qui est regle et ce
# qui s'est passe — c'est la difference entre un panneau de configuration et
# un instrument de pilotage.
@app.get("/api/gouvernance")
def api_gouvernance():
    import re, collections
    out = {"curseurs": [], "refus": [], "indicateurs": {}}

    # 1. Les reglages declares — via la fonction q() du fichier, pas subprocess.
    try:
        out["curseurs"] = [dict(r) for r in q(DSN, """
            SELECT direction, type_tache, niveau,
                   coalesce(justification,'')     AS justification,
                   coalesce(canal_impose,'')      AS canal_impose,
                   coalesce(evolution_prevue,'')  AS evolution_prevue,
                   coalesce(regle_code,'')        AS regle_code,
                   maj_par, maj_le
            FROM curseurs ORDER BY direction, type_tache""")]
        for c in out["curseurs"]:
            if c.get("maj_le"):
                c["maj_le"] = str(c["maj_le"])[:19]
    except Exception as e:
        out["erreur_curseurs"] = str(e)

    # 2. Le vecu — les refus reellement survenus. Sans cela, la page ne
    # montrerait qu'une intention.
    chemin = "/workspace/hooks.log"
    par_dir = collections.Counter()
    par_tache = collections.Counter()
    recents = []
    try:
        with open(chemin, encoding="utf-8", errors="ignore") as f:
            for l in f:
                if "CURSEUR-DENY" not in l and "DENY" not in l:
                    continue
                m = re.match(r"(\S+)\s+(CURSEUR-)?DENY\s+\[(\w+)\]\s+(.*)", l.strip())
                if not m:
                    continue
                horo, _, outil, reste = m.groups()
                mm = re.match(r"([\w-]+)/([\w_]+)\s+regle=(\d)\s+requis=(\d)\s+::\s+(.*)", reste)
                if mm:
                    d, t, regle, requis, cmd = mm.groups()
                    par_dir[d] += 1
                    par_tache[t] += 1
                    recents.append({"horodatage": horo, "direction": d, "type_tache": t,
                                    "regle": int(regle), "requis": int(requis),
                                    "commande": cmd[:110], "origine": "curseur"})
                else:
                    rr = reste.split(" :: ")
                    recents.append({"horodatage": horo, "direction": None,
                                    "type_tache": None, "regle_code": rr[0][:40],
                                    "commande": (rr[1][:110] if len(rr) > 1 else ""),
                                    "origine": "regle_figee"})
    except Exception as e:
        out["erreur_refus"] = str(e)

    out["refus"] = list(reversed(recents))[:40]

    # 3. Les quatre indicateurs de tete — pas un de plus, gabarit N1.
    total = len(out["curseurs"])
    autonomes = sum(1 for c in out["curseurs"] if c["niveau"] == 4)
    contraints = sum(1 for c in out["curseurs"] if c["niveau"] <= 2)
    out["indicateurs"] = {
        "reglages_total": total,
        "autonomes": autonomes,
        "contraints": contraints,
        "refus_total": len(recents),
        "refus_par_curseur": sum(1 for x in recents if x.get("origine") == "curseur"),
        "directions_avec_refus": len(par_dir),
        "tache_la_plus_bloquee": (par_tache.most_common(1)[0][0] if par_tache else None),
    }
    return out


@app.get("/api/pilotage")
def api_pilotage():
    """Poste de pilotage (N0). Agrege ce qui attend Sam maintenant, direction
    par direction. Principe du handoff : on concoit la cible et on AFFICHE LE
    MANQUE — jamais un zero a la place d'une donnee absente."""
    import datetime
    out = {"directions": [], "decisions": {}, "cash": {}, "maj": None}
    DIRS = [
        ("delivery",         "Delivery",        "rapport_delivery"),
        ("commercial",       "Commercial",      "rapport_commercial"),
        ("marketing",        "Marketing",       "rapport_marketing"),
        ("customer-success", "Customer Success","rapport_cs"),
        ("chief-of-staff",   "Chief of Staff",  "rapport_cos"),
        ("legal",            "Juridique",       "rapport_legal"),
    ]
    try:
        etat = {r["cle"]: r for r in q(DSN, "SELECT cle, valeur, updated_at AS maj FROM deos_state")}
    except Exception as e:
        return {"erreur": str(e)}

    aujourdhui = datetime.date.today()
    for cle, libelle, source in DIRS:
        e = etat.get(source)
        d = {"cle": cle, "libelle": libelle, "etat": "absent",
             "score": None, "statut": None, "alertes": [], "kpis": [],
             "fraicheur": None, "calcul": None, "manques": 0, "demandes": 0}
        if e and e.get("valeur"):
            v = e["valeur"] if isinstance(e["valeur"], dict) else {}
            maj = e.get("maj")
            age_h = None
            if maj:
                try:
                    age_h = (datetime.datetime.now(maj.tzinfo) - maj).total_seconds() / 3600
                except Exception:
                    pass
            # Un rapport de plus de 30 h est traite comme manquant : mieux vaut
            # afficher "pas de remontee" qu'un chiffre perime pris pour actuel.
            if age_h is not None and age_h > 30:
                d["etat"] = "perime"
                d["fraicheur"] = f"dernier rapport il y a {int(age_h)} h"
            else:
                d["etat"] = "ok"
                d["fraicheur"] = f"il y a {int(age_h)} h" if age_h is not None else None
                # domain_score porte la note ; calcul_score en est la
                # demonstration ecrite, qu'on garde pour l'infobulle.
                d["score"] = v.get("domain_score")
                if isinstance(d["score"], str) and d["score"].isdigit():
                    d["score"] = int(d["score"])
                cs = v.get("calcul_score")
                d["calcul"] = cs[:400] if isinstance(cs, str) else None
                d["manques"] = len(v.get("donnees_manquantes") or [])
                d["demandes"] = len(v.get("decisions_demandees") or [])
                d["statut"] = v.get("statut")
                al = v.get("alertes") or []
                d["alertes"] = [
                    (a.get("texte") if isinstance(a, dict) else str(a))[:180]
                    for a in al[:3]
                ]
                kp = v.get("kpis") or {}
                if isinstance(kp, dict):
                    d["kpis"] = [{"nom": k, "valeur": str(x)[:60]} for k, x in list(kp.items())[:4]]
        out["directions"].append(d)

    try:
        r = q(DSN, """SELECT statut, count(*) AS n,
                             min(date)::date AS plus_ancienne
                      FROM decisions GROUP BY statut""")
        par = {x["statut"]: x for x in r}
        out["decisions"] = {
            "attente_sam": par.get("attente_sam", {}).get("n", 0),
            "accordees_non_executees": (par.get("accordee", {}).get("n", 0)
                                        + par.get("en_execution", {}).get("n", 0)),
            "closes": par.get("clos", {}).get("n", 0),
            "plus_ancienne_en_attente": str(par.get("attente_sam", {}).get("plus_ancienne") or ""),
        }
        liste = q(DSN, """SELECT id, texte, date::date AS d,
                                 (CURRENT_DATE - date::date) AS age
                          FROM decisions WHERE statut='attente_sam'
                          ORDER BY date LIMIT 6""")
        out["decisions"]["liste"] = [
            {"id": x["id"], "texte": (x["texte"] or "")[:200], "age": x["age"]} for x in liste]
    except Exception as e:
        out["decisions"] = {"erreur": str(e)}

    c = etat.get("cash_suivi")
    if c and isinstance(c.get("valeur"), dict):
        v = c["valeur"]
        out["cash"] = {"solde": v.get("solde_declare"), "seuil": v.get("seuil_alerte_solde"),
                       "mrr": v.get("mrr_reel"), "declare_le": v.get("date_declaration")}
    return out


@app.get("/api/demo/{action}")
def api_demo(action: str):
    """Mode demonstration. On ecrit VRAIMENT pendant la demo — une simulation
    ne prouverait rien. Tout ce qui est cree porte le marqueur demo, et la
    sortie du mode purge ces lignes."""
    if action not in ("on", "off", "etat"):
        return {"erreur": "action inconnue"}
    try:
        if action == "on":
            q(DSN, "UPDATE mode_demo SET actif=true, active_le=NOW(), par='sam' WHERE id=1 RETURNING id")
            return {"actif": True, "message": "Mode demonstration actif. Les elements crees seront effaces a la sortie."}
        if action == "off":
            # Purge de tout ce qui porte le marqueur, puis sortie du mode.
            # Le registre des decisions est append-only par declencheur
            # (DH-COS-002) : on ne le supprime PAS, c'est ce qui garantit qu'il
            # ne peut pas etre reecrit. On classe donc les lignes de demo en
            # "annulee_demo", elles sortent des compteurs sans trouer l'histoire.
            d1 = q(DSN, """UPDATE decisions
                           SET statut = 'refusee',
                               texte  = '[DÉMONSTRATION — annulée automatiquement à la sortie du mode] ' || texte
                           WHERE demo = true AND statut <> 'refusee'
                           RETURNING id""")
            # signaux_publics vit dans la base PRODUCTION, pas celle du comite.
            # Le comite ny a quun acces lecture seule : rien a purger ici.
            d2 = []
            q(DSN, "UPDATE mode_demo SET actif=false WHERE id=1 RETURNING id")
            return {"actif": False, "purge": {"decisions_annulees": len(d1), "signaux_effaces": len(d2)},
                    "message": f"Mode demonstration termine. {len(d1)} decision(s) annulee(s), {len(d2)} signal(aux) efface(s)."}
        r = q(DSN, "SELECT actif, active_le, par FROM mode_demo WHERE id=1")
        e = dict(r[0]) if r else {"actif": False}
        if e.get("active_le"):
            e["active_le"] = str(e["active_le"])[:19]
        return e
    except Exception as ex:
        return {"erreur": str(ex)}


@app.get("/wip/{nom}")
def page_wip(nom: str):
    """Captures d'ecran des trois ecrans, pour le brief Claude Design."""
    from fastapi.responses import FileResponse
    import re
    if not re.match(r'^[a-z0-9.-]+\.png$', nom):
        return JSONResponse({"erreur": "nom invalide"}, status_code=400)
    return FileResponse(f"{BASE}/web/wip/{nom}", media_type="image/png")


@app.get("/wip", response_class=HTMLResponse)
def page_wip_index():
    import os as _os
    f = sorted(x for x in _os.listdir(f"{BASE}/web/wip") if x.endswith(".png"))
    liens = "".join(f'<li><a href="/wip/{x}">{x}</a></li>' for x in f)
    return HTMLResponse(
        '<html><head><meta charset="utf-8"><title>Captures WIP</title>'
        '<style>body{background:#0A0A0B;color:#F5F2EC;font-family:system-ui;padding:40px}'
        'a{color:#C8A97E}li{margin:8px 0}</style></head><body>'
        '<h1 style="font-weight:300">Captures des trois écrans</h1>'
        f'<ul>{liens}</ul></body></html>')


@app.get("/pilotage", response_class=HTMLResponse)
def page_pilotage():
    """Poste de pilotage (N0) — l'ecran d'ouverture : qu'est-ce qui m'attend ?"""
    with open(f"{BASE}/web/pilotage.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/gouvernance", response_class=HTMLResponse)
def page_gouvernance():
    """Page N1 du curseur d'autonomie — meme gabarit que les six directions."""
    with open(f"{BASE}/web/gouvernance.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/", response_class=HTMLResponse)
def index():
    with open(f"{BASE}/web/index.html", encoding="utf-8") as f:
        return f.read()
