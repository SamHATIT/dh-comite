"""Comité DH — API lecture seule pour le tableau de bord (V1.1, 14/07/2026)."""
import os, glob
import html as _h   # echappement des contenus injectes dans le HTML
import psycopg2, psycopg2.extras
from fastapi import FastAPI, Request
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


@app.get("/api/brief_complet")
def api_brief_complet():
    """Acte I — tout ce que le comite a produit aujourd'hui, sans rien ecraser.
    Les champs longs sont transmis ENTIERS : c'est l'interface qui applique
    le motif de l'incipit, pas l'API qui tronque."""
    try:
        r = q(DSN, "SELECT valeur FROM deos_state WHERE cle='brief'")
        if not r:
            return {"erreur": "Aucun brief encore produit."}
        b = r[0]["valeur"] or {}
    except Exception as e:
        return {"erreur": str(e)}

    def txt(x):
        if isinstance(x, dict):
            return x.get("texte") or x.get("objet") or x.get("nom") or str(x)
        return str(x)

    # Les indicateurs portent leur direction d'origine, pour le regroupement.
    kpis = []
    for k in (b.get("kpis") or []):
        if not isinstance(k, dict):
            continue
        src = (k.get("source") or "").replace("rapport_", "").split()[0] if k.get("source") else ""
        kpis.append({"nom": k.get("nom", "—"),
                     "valeur": k.get("valeur") or k.get("value") or "",
                     "direction": src or "autres"})

    return {
        "date": b.get("date"),
        "sante": b.get("sante") or {},
        "kpis": kpis,
        "alertes": [txt(a) for a in (b.get("alertes") or [])],
        "decisions_attendues": [txt(d) for d in (b.get("decisions_attendues") or [])],
        "priorites_jour": [txt(p) for p in (b.get("priorites_jour") or [])],
    }


@app.get("/brief/{jour}", response_class=HTMLResponse)
def page_brief(jour: str):
    """Le brief du jour en HTML lisible et presentable — remplace le docx.
    Meme charte que les trois actes ; se montre a un client sans rougir."""
    import re as _r, os as _o
    if not _r.match(r'^\d{4}-\d{2}-\d{2}$', jour):
        return HTMLResponse("<p>date invalide</p>", status_code=400)
    f = f"{BASE}/briefs/brief-{jour}.md"
    if not _o.path.exists(f):
        return HTMLResponse(f"<p>Aucun brief pour le {jour}.</p>", status_code=404)
    md = open(f, encoding="utf-8", errors="replace").read()
    with open(f"{BASE}/web/brief.html", encoding="utf-8") as t:
        gabarit = t.read()
    import json as _j
    return HTMLResponse(gabarit.replace("__JOUR__", jour).replace("__MD__", _j.dumps(md)))


@app.get("/comite.css")
def feuille_style():
    from fastapi.responses import FileResponse
    return FileResponse(f"{BASE}/web/comite.css", media_type="text/css")


@app.get("/rapports", response_class=HTMLResponse)
def page_rapports():
    """Index des rapports produits par les directions, lisibles depuis un lien."""
    import os as _o, glob as _g
    fichiers = []
    for d in ("delivery", "legal", "commercial", "marketing"):
        for f in sorted(_g.glob(f"{BASE}/config/{d}/*.md"), reverse=True):
            n = _o.path.basename(f)
            fichiers.append((d, n, _o.path.getsize(f)))
    li = "".join(
        f'<li><span class="d">{d}</span> <a href="rapport/{d}/{n}">{n}</a>'
        f' <span class="t">{k//1024} Ko</span></li>' for d, n, k in fichiers)
    return HTMLResponse(
        '<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rapports du comité</title>'
        '<style>body{background:#0A0A0B;color:#B5B0A4;font-family:"JetBrains Mono",monospace;'
        'padding:48px 32px;font-size:13px;line-height:2}h1{font-family:Georgia,serif;'
        'font-weight:300;font-size:30px;color:#F5F2EC;font-style:italic;margin-bottom:28px}'
        'a{color:#C8A97E;text-decoration:none}a:hover{text-decoration:underline}'
        'li{list-style:none;border-bottom:1px solid #C8A97E1F;padding:9px 0}'
        '.d{display:inline-block;width:110px;font-size:9.5px;letter-spacing:.18em;'
        'text-transform:uppercase;color:#6F6B62}.t{color:#6F6B62;font-size:11px;float:right}'
        'ul{padding:0;max-width:900px}</style></head><body>'
        f'<h1>Rapports des directions</h1><ul>{li}</ul></body></html>')


@app.get("/rapport/{direction}/{nom}", response_class=HTMLResponse)
def page_rapport(direction: str, nom: str):
    """Rend un rapport markdown en HTML lisible, dans la charte."""
    import re as _r, html as _h, os as _o
    if not _r.match(r'^[a-z-]+$', direction) or not _r.match(r'^[\w.-]+\.md$', nom):
        return HTMLResponse("<p>nom invalide</p>", status_code=400)
    chemin = f"{BASE}/config/{direction}/{nom}"
    if not _o.path.exists(chemin):
        return HTMLResponse("<p>introuvable</p>", status_code=404)
    md = open(chemin, encoding="utf-8").read()
    # Rendu markdown minimal : titres, gras, code, tableaux, listes.
    h = _h.escape(md)
    h = _r.sub(r'^### (.+)$', r'<h3>\1</h3>', h, flags=_r.M)
    h = _r.sub(r'^## (.+)$', r'<h2>\1</h2>', h, flags=_r.M)
    h = _r.sub(r'^# (.+)$', r'<h1>\1</h1>', h, flags=_r.M)
    h = _r.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', h)
    h = _r.sub(r'`([^`]+)`', r'<code>\1</code>', h)
    h = _r.sub(r'^- (.+)$', r'<li>\1</li>', h, flags=_r.M)
    h = _r.sub(r'^\|(.+)\|$', lambda m: '<tr>' + ''.join(
        f'<td>{c.strip()}</td>' for c in m.group(1).split('|')) + '</tr>', h, flags=_r.M)
    h = _r.sub(r'(<tr>.*?</tr>\n?)+', lambda m: f'<table>{m.group(0)}</table>', h, flags=_r.S)
    h = _r.sub(r'<td>[-: ]+</td>', '', h)
    h = h.replace('\n\n', '</p><p>')
    return HTMLResponse(
        '<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + _h.escape(nom) + '</title>'
        '<style>body{background:#0A0A0B;color:#B5B0A4;font-family:"JetBrains Mono",monospace;'
        'font-size:13px;line-height:1.9;padding:44px 28px 90px;max-width:1000px;margin:0 auto}'
        'h1,h2,h3{font-family:Georgia,serif;font-weight:300;color:#F5F2EC;font-style:italic;'
        'line-height:1.2;margin:34px 0 12px}h1{font-size:30px}h2{font-size:22px;color:#E5E1D8;'
        'border-bottom:1px solid #C8A97E3D;padding-bottom:8px}h3{font-size:17px}'
        'b{color:#F5F2EC;font-weight:400}code{color:#C8A97E;font-size:12px}'
        'table{width:100%;border-collapse:collapse;margin:14px 0}'
        'td{border-bottom:1px solid #C8A97E1F;padding:8px 10px;vertical-align:top;font-size:12px}'
        'li{margin-left:18px;margin-bottom:4px}p{margin:10px 0}'
        'a{color:#C8A97E}.retour{font-size:10px;letter-spacing:.2em;text-transform:uppercase;'
        'color:#6F6B62;text-decoration:none;display:inline-block;margin-bottom:20px}'
        '</style></head><body><a class="retour" href="../rapports">← Tous les rapports</a><p>'
        + h + '</p></body></html>')


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
    liens = "".join(f'<li><a href="wip/{x}">{x}</a></li>' for x in f)
    return HTMLResponse(
        '<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Captures WIP</title>'
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


# ═══════════════════════════════════════════════════════════════════════════
# ARBITRAGE DEPUIS LE WEB — DEC-2026-0714-01, partie interaction
# ═══════════════════════════════════════════════════════════════════════════
# Les 14 routes precedentes sont TOUTES en lecture. Sam pouvait tout
# consulter, rien valider — il dictait donc ses arbitrages en conversation.
# D'ou le cercle vicieux releve le 10/08 : la decision qui rendrait les
# arbitrages faciles attendait depuis 27 jours, parce que l'arbitrer
# demandait justement le mecanisme qu'elle devait creer.
#
# Concu pour le TELEPHONE d'abord : c'est la que Sam arbitre, entre deux
# rendez-vous. Une decision par ecran, trois boutons, rien d'autre.

@app.get("/arbitrer")
def page_arbitrage():
    lignes = q(DSN, """
        SELECT id, origine, date, texte, recommandation,
               (now()::date - date::date) AS jours
        FROM decisions WHERE statut = 'attente_sam'
        ORDER BY date
    """)

    if not lignes:
        corps = ('<div class="vide"><p>Aucune décision en attente.</p>'
                 '<p class="sec">Tout est tranché.</p></div>')
    else:
        cartes = []
        for d in lignes:
            j = d["jours"]
            urgence = "vieux" if j >= 14 else "moyen" if j >= 7 else "recent"
            texte = _h.escape(d["texte"] or "")
            reco = _h.escape(d["recommandation"] or "") if d.get("recommandation") else ""
            cartes.append(f"""
            <article class="dec {urgence}" id="{d['id']}">
              <header>
                <span class="ref">{d['id']}</span>
                <span class="age">{j} jour{'s' if j > 1 else ''}</span>
              </header>
              <div class="txt">{texte}</div>
              {f'<div class="reco"><span class="lab">Recommandation</span>{reco}</div>' if reco else ''}
              <div class="actions">
                <button class="b ok"  onclick="trancher('{d['id']}','accordee')">Accorder</button>
                <button class="b non" onclick="trancher('{d['id']}','refusee')">Refuser</button>
                <button class="b att" onclick="trancher('{d['id']}','differee')">Différer</button>
              </div>
              <div class="etat" id="etat-{d['id']}"></div>
            </article>""")
        corps = "".join(cartes)

    return HTMLResponse(f"""<!doctype html><html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Arbitrer — {len(lignes)} décision(s)</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}}
body{{background:#0E0E10;color:#CFCAC0;font:400 16px/1.65 -apple-system,BlinkMacSystemFont,
  'Segoe UI',Roboto,sans-serif;padding:18px 14px 60px}}
h1{{font-size:1.45rem;font-weight:400;color:#F5F2EC;margin-bottom:4px}}
.compte{{font-size:13px;color:#6E6B66;margin-bottom:22px;
  padding-bottom:16px;border-bottom:1px solid #C8A97E33}}
.dec{{background:#16161A;border:1px solid #FFFFFF14;border-left:3px solid #C8A97E;
  padding:16px 16px 14px;margin-bottom:16px;border-radius:3px}}
.dec.vieux{{border-left-color:#9B4A4A}}
.dec.moyen{{border-left-color:#C8A97E}}
.dec.recent{{border-left-color:#4E8C6A}}
.dec.fait{{opacity:.35}}
header{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:10px}}
.ref{{font:500 11px/1 ui-monospace,monospace;letter-spacing:.06em;color:#A98C63}}
.age{{font:400 11px/1 ui-monospace,monospace;color:#6E6B66}}
.txt{{font-size:14.5px;color:#CFCAC0;line-height:1.6;margin-bottom:12px}}
.reco{{background:#C8A97E0D;border-left:2px solid #7A6647;padding:10px 12px;
  margin-bottom:14px;font-size:13.5px;color:#9A968E;line-height:1.55}}
.lab{{display:block;font:500 9.5px/1 ui-monospace,monospace;letter-spacing:.16em;
  text-transform:uppercase;color:#7A6647;margin-bottom:5px}}
.actions{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}}
.b{{font:500 14px/1 inherit;padding:13px 8px;border:1px solid;background:none;
  border-radius:3px;cursor:pointer;transition:all .18s}}
.b.ok{{color:#6FA98A;border-color:#4E8C6A66}}
.b.ok:active{{background:#4E8C6A2A}}
.b.non{{color:#C87A7A;border-color:#9B4A4A66}}
.b.non:active{{background:#9B4A4A2A}}
.b.att{{color:#9A968E;border-color:#FFFFFF1F}}
.b.att:active{{background:#FFFFFF14}}
.etat{{font-size:13px;margin-top:10px;min-height:0}}
.etat.ok{{color:#6FA98A}} .etat.err{{color:#C87A7A}}
.vide{{text-align:center;padding:60px 20px;color:#6E6B66}}
.vide .sec{{font-size:13px;margin-top:8px;color:#4A4845}}
@media(min-width:700px){{body{{max-width:720px;margin:0 auto;padding:36px 24px 80px}}}}
</style></head><body>
<h1>Décisions à trancher</h1>
<p class="compte">{len(lignes)} en attente · la plus ancienne remonte à
   {max((d['jours'] for d in lignes), default=0)} jours</p>
{corps}
<script>
async function trancher(id, verdict) {{
  const carte = document.getElementById(id);
  const etat = document.getElementById('etat-' + id);
  carte.querySelectorAll('.b').forEach(b => b.disabled = true);
  etat.className = 'etat';
  etat.textContent = 'Enregistrement…';
  try {{
    // Chemin RELATIF : nginx sert le comite sous /comite/. Une adresse
    // commencant par / sortirait du comite et n'atteindrait jamais le
    // service — meme defaut que les liens de rapports, corrige le 10/08.
    const r = await fetch('api/arbitrer', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{id: id, verdict: verdict}})
    }});
    const d = await r.json();
    if (d.ok) {{
      etat.className = 'etat ok';
      etat.textContent = d.message;
      carte.classList.add('fait');
    }} else {{
      etat.className = 'etat err';
      etat.textContent = d.message || 'Échec';
      carte.querySelectorAll('.b').forEach(b => b.disabled = false);
    }}
  }} catch (e) {{
    etat.className = 'etat err';
    etat.textContent = 'Erreur réseau — non enregistré';
    carte.querySelectorAll('.b').forEach(b => b.disabled = false);
  }}
}}
</script></body></html>""")


@app.post("/api/arbitrer")
async def api_arbitrer(requete: Request):
    """Enregistre un arbitrage de Sam. SEULE route en ecriture du service.

    Trois garde-fous, parce qu'elle modifie l'etat du dispositif :
      · verdict limite a trois valeurs, jamais de texte libre en base
      · on verifie que la decision EST en attente — sinon on refuse plutot
        que d'ecraser un arbitrage deja rendu
      · l'origine est tracee comme 'sam-web', pour distinguer d'un arbitrage
        dicte en conversation
    """
    VERDICTS = {
        "accordee": "Accordée",
        "refusee":  "Refusée",
        "differee": "Différée",
    }
    try:
        corps = await requete.json()
    except Exception:
        return JSONResponse({"ok": False, "message": "requête illisible"}, status_code=400)

    did = (corps.get("id") or "").strip()
    verdict = (corps.get("verdict") or "").strip()

    if not did or verdict not in VERDICTS:
        return JSONResponse({"ok": False, "message": "verdict inconnu"}, status_code=400)

    try:
        with psycopg2.connect(DSN) as c, c.cursor() as cur:
            # On ne tranche que ce qui attend REELLEMENT — evite d'ecraser
            # un arbitrage deja rendu depuis un autre canal.
            cur.execute(
                "UPDATE decisions SET statut = %s, validation_par = 'sam', "
                "  updated_at = now(), "
                "  preuve = COALESCE(preuve, '{}'::jsonb) || jsonb_build_object("
                "    'arbitre_par', 'sam-web', "
                "    'arbitre_le', now()::text) "
                "WHERE id = %s AND statut = 'attente_sam' RETURNING id",
                (verdict, did),
            )
            touche = cur.fetchone()
            c.commit()

        if not touche:
            return JSONResponse({"ok": False,
                                 "message": "déjà tranchée ailleurs"}, status_code=409)

        return JSONResponse({"ok": True, "message": VERDICTS[verdict] + " — enregistré"})

    except Exception as e:
        return JSONResponse({"ok": False, "message": f"erreur : {str(e)[:90]}"},
                            status_code=500)
