"""Comité DH — API lecture seule pour le tableau de bord (V1, 14/07/2026)."""
import os, glob, json
import psycopg2, psycopg2.extras
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

DSN = os.environ["COMITE_DB_DSN"]
BASE = "/workspace"
app = FastAPI(title="dh-comite-web", docs_url=None, redoc_url=None)

def q(sql, args=()):
    with psycopg2.connect(DSN) as c, c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, args)
        return cur.fetchall()

@app.get("/api/etat")
def etat():
    rows = q("SELECT cle, valeur, maj_par, updated_at FROM deos_state")
    state = {r["cle"]: {"valeur": r["valeur"], "maj": r["updated_at"].isoformat(), "par": r["maj_par"]} for r in rows}
    decisions = q("""SELECT id, statut, origine, texte, recommandation, porte_sur,
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
    })

@app.get("/api/brief/{nom}")
def brief(nom: str):
    nom = os.path.basename(nom)
    try:
        with open(f"{BASE}/briefs/{nom}", encoding="utf-8") as f:
            return JSONResponse({"nom": nom, "contenu": f.read()})
    except FileNotFoundError:
        return JSONResponse({"erreur": "brief introuvable"}, status_code=404)

@app.get("/", response_class=HTMLResponse)
def index():
    with open(f"{BASE}/web/index.html", encoding="utf-8") as f:
        return f.read()
