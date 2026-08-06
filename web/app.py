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


@app.get("/gouvernance", response_class=HTMLResponse)
def page_gouvernance():
    """Page N1 du curseur d'autonomie — meme gabarit que les six directions."""
    with open(f"{BASE}/web/gouvernance.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/", response_class=HTMLResponse)
def index():
    with open(f"{BASE}/web/index.html", encoding="utf-8") as f:
        return f.read()
