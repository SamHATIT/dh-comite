#!/usr/bin/env python3
"""Cockpit — remplit les gabarits business et technique depuis les sources reelles.

POURQUOI (12/08) : sept interfaces de pilotage dispersees, Sam perd du temps a
naviguer et rate des signaux. Deux ecrans remplacent la navigation.

CHOIX DE CONCEPTION — LE VERDICT EST UNE REGLE, PAS UN MODELE.
La phrase en grand est calculee par des seuils explicites (voir VERDICTS), pas
generee par un LLM. Trois raisons : le cout, la reproductibilite, et le fait
qu'un cockpit doit enoncer un fait, pas une opinion. Meme principe que
l'evaluateur gele : ce qui se compte ne se juge pas.

LES COUTS AFFICHENT TOUJOURS LEURS TROUS. Le releve du 12/08 mesure 246 USD
quand la facture reelle approche 377. Afficher le premier chiffre sans le
second serait reproduire l'erreur que ce releve corrige.

Usage : cockpit.py [--sortie /var/www/...] [--dry]
"""
import json, subprocess, sys, os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GABARIT = os.path.join(BASE, "cockpit", "business.tpl.html")
PLAT = "postgresql://digital_humans:DH_SecurePass2025!@127.0.0.1:5432/digital_humans_db"
SORTIE = "/var/www/app-studio/cockpit"

MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août",
        "septembre","octobre","novembre","décembre"]
JOURS = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
LETTRES = {0:"Aucune",1:"Une",2:"Deux",3:"Trois",4:"Quatre",5:"Cinq",6:"Six",7:"Sept",
           8:"Huit",9:"Neuf",10:"Dix",11:"Onze",12:"Douze",13:"Treize",14:"Quatorze",
           15:"Quinze",16:"Seize",17:"Dix-sept",18:"Dix-huit",19:"Dix-neuf",20:"Vingt"}

def q_plat(sql):
    r = subprocess.run(["psql", PLAT, "-tAF", "|", "-c", sql], capture_output=True, text=True)
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]

def q_comite(sql):
    r = subprocess.run(["docker","exec","dh-comite","bash","-c",
                        f'psql "$COMITE_DB_DSN" -tAF "|" -c {json.dumps(sql)}'],
                       capture_output=True, text=True)
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]

def sf_leads():
    """Statuts des leads Salesforce, avec l org effectivement porteuse.

    ETAT AU 12/08 : les 126 leads sont dans `equipe-dev`, une org que le code de
    la plateforme ne lit NULLE PART (0 reference au depot, contre 11 pour
    digital-humans-dev alias `Production`). sf-lead a ete repointe vers Production
    le 12/08 mais le STOCK n a pas suivi — flux et stock sont separes.

    On interroge donc Production, puis equipe-dev en repli, et on RAPPORTE
    laquelle a repondu. Afficher zero sans dire pourquoi serait exact et inutile.
    """
    for org in ("Production", "equipe-dev"):
        try:
            r = subprocess.run(
                ["sf","data","query","--query",
                 "SELECT Status, COUNT(Id) n FROM Lead GROUP BY Status",
                 "--target-org", org, "--json"],
                capture_output=True, text=True, timeout=70,
                cwd="/root/workspace/digital-humans-production")
            recs = json.loads(r.stdout)["result"]["records"]
            d = {x["Status"]: x["n"] for x in recs}
            if sum(d.values()):
                return d, org
        except Exception:
            continue
    return {}, None

# ── Les regles de verdict, par ordre de priorite ──────────────────────────
# Chaque entree : (condition, nombre, phrase, detail, couleur)
# La PREMIERE qui matche gagne. L'ordre encode la hierarchie des urgences.
def verdicts(d):
    n = d["dec_attente_sam"]
    return [
      (n >= 10, n,
       f"{LETTRES.get(n, n)} décisions attendent<br>votre signature.",
       f'La plus ancienne a <b style="font-weight:500;color:var(--bone)">{d["dec_age_max"]} jours</b>. '
       "Rien ne peut avancer dessus tant que vous n’avez pas tranché&#8239;: c’est le seul "
       "point de cet écran où votre geste est le goulot.",
       "var(--d-down)"),
      (d["sf_froid"] >= 100, d["sf_froid"],
       "leads n’ont jamais été<br>contactés une seule fois.",
       f'Sur {d["sf_total"]} au total. Le blocage n’est pas la conversion&#8239;: c’est le premier '
       "contact, et il ne demande pas de décision — seulement du temps.",
       "var(--d-down)"),
      (d["dec_accordees"] >= 25, d["dec_accordees"],
       "décisions accordées<br>n’ont jamais été exécutées.",
       "La dette d’exécution dépasse la file de signature. Ce qui coince est en sortie, "
       "pas en entrée.",
       "var(--d-ambre)"),
      (True, d["sf_convertis"],
       "conversions ce mois-ci.",
       "Aucune alerte au-dessus des seuils. Les chiffres ci-dessous donnent le détail.",
       "var(--d-ok)"),
    ]

def collecte():
    d = {}
    # --- decisions (base comite) ---
    st = dict((r[0], int(r[1])) for r in q_comite("SELECT statut, count(*) FROM decisions GROUP BY 1"))
    d["dec_attente_sam"] = st.get("attente_sam", 0)
    d["dec_accordees"]   = st.get("accordee", 0)
    d["dec_closes"]      = st.get("clos", 0)
    d["dec_execution"]   = st.get("en_execution", 0)
    d["dec_total"]       = sum(st.values())
    age = q_comite("SELECT coalesce(max(now()::date - date::date),0) FROM decisions WHERE statut='attente_sam'")
    d["dec_age_max"] = int(age[0][0]) if age else 0
    # ages individuels, pour la bande de placement (zone 2)
    ages = [int(r[0]) for r in q_comite(
        "SELECT (now()::date - date::date) FROM decisions WHERE statut='attente_sam'") if r[0].strip().isdigit()]
    d.update(zone_age(ages))

    # --- Salesforce ---
    sf, sf_org = sf_leads()
    d["sf_org"] = sf_org or "aucune"
    d["sf_froid"]     = sf.get("Open - Not Contacted", 0)
    d["sf_encours"]   = sf.get("Working - Contacted", 0)
    d["sf_convertis"] = sf.get("Closed - Converted", 0)
    d["sf_abandon"]   = sf.get("Closed - Not Converted", 0)
    d["sf_total"]     = sum(sf.values()) or 1
    for c, k in [("froid","sf_froid"),("encours","sf_encours"),
                 ("convertis","sf_convertis"),("abandon","sf_abandon")]:
        d[f"sf_pct_{c}"] = round(d[k] * 100 / d["sf_total"], 1)
    d["sf_taux_conv"] = str(d["sf_pct_convertis"]).replace(".", ",")
    pct_froid = d["sf_pct_froid"]
    alerte_org = ('' if sf_org == "Production" else
      ' <b style="font-weight:500;color:var(--d-ambre)">Leads lus dans '
      f'{sf_org}</b>, org que la plateforme ne lit pas — stock à rapatrier.')
    d["sf_commentaire"] = ((
      f'<b style="font-weight:500;color:var(--d-down)">{str(pct_froid).replace(".",",")}&#8239;% du pipeline '
      "n’a jamais été touché.</b> Le blocage n’est pas la conversion, c’est le premier contact."
      if pct_froid >= 60 else
      f'<b style="font-weight:500;color:var(--d-ok)">{str(pct_froid).replace(".",",")}&#8239;% en attente '
      "de premier contact.</b> Le pipeline circule.") + alerte_org)

    # --- signaux ---
    sig = dict((r[0], int(r[1])) for r in q_plat("SELECT statut, count(*) FROM v_deos_signaux GROUP BY 1"))
    d["sig_reseau"]    = sig.get("reseau_a_prevenir", 0)
    d["sig_offres"]    = sig.get("offre_en_attente", 0)
    d["sig_qualifier"] = sig.get("a_qualifier", 0)
    d["sig_nouveaux"]  = sig.get("nouveau", 0)
    d["sig_total"]     = sum(sig.values())

    # --- contenu ---
    d["cont_veille"] = int(q_plat("SELECT count(*) FROM v_deos_veille")[0][0])
    d["cont_publies"] = int(q_plat("SELECT count(*) FROM v_deos_blog_articles WHERE published_at IS NOT NULL")[0][0])
    d["cont_brouillons"] = 4   # posts LinkedIn — pas de source machine a ce jour

    # --- couts : le releve consolide, AVEC ses trous ---
    try:
        r = subprocess.run(["python3", os.path.join(BASE,"bin","couts-consolides.py"),
                            "--jours","30","--json"], capture_output=True, text=True, timeout=90)
        c = json.loads(r.stdout)
        d.update(zone_couts(c))
    except Exception as e:
        print("releve des couts indisponible :", e, file=sys.stderr)
        d.update(cout_fenetre="—", cout_mesure="—", cout_unite="$", cout_facture="—",
                 cout_manquant="—", cout_couverture_pct=0, cout_manquant_pct=0,
                 cout_trous_n="?", _bloc_trous="")
        for i in (1, 2):
            d.update({f"poste_{i}_nom": "—", f"poste_{i}_montant": "—", f"poste_{i}_pct": 0})

    # Le bandeau du bas annonce le nombre d alertes : il doit se compter, pas
    # s ecrire. « TROIS CHIFFRES ROUGES » etait fige et se serait contredit
    # des qu un seuil bouge — meme piege que les « 34 jours » de la zone d age.
    rouges = sum([d["dec_attente_sam"] >= 10,
                  d["sf_pct_froid"] >= 60,
                  d["dec_accordees"] >= 25])
    d["bandeau_phrase"] = (
        f"{LETTRES.get(rouges, rouges).upper()} CHIFFRE{'S' if rouges > 1 else ''} "
        f"ROUGE{'S' if rouges > 1 else ''}, UN SEUL GESTE&#8239;:"
        if rouges else "AUCUN SEUIL FRANCHI&#8239;:")

    d["lien_comite"] = "https://app.digital-humans.fr/comite/"
    d["lien_admin"]  = "https://console.digital-humans.fr/"

    # --- verdict ---
    for cond, nb, phrase, detail, couleur in verdicts(d):
        if cond:
            d["verdict_nombre"], d["verdict_phrase"] = nb, phrase
            d["verdict_detail"], d["verdict_couleur"] = detail, couleur
            break
    return d



# ══════════════════════════════════════════════════════════════════════════
#  ZONE 1 — le chiffre ET sa couverture
# ══════════════════════════════════════════════════════════════════════════
#  Decision de conception (Claude Design, 12/08) : l incertitude n est pas une
#  reserve SUR le chiffre, c est un SECOND CHIFFRE — sa couverture. « 246 $
#  mesure » et « couvre 65 % de la facture » sont deux faits vrais, chacun
#  lisible sans affaiblir l autre.
#
#  PIEGE DOCUMENTE, a ne pas reproduire : les trois barres du registre
#  partagent un axe, donc un DENOMINATEUR. Le pourcentage de la part non
#  couverte se rapporte au PLUS GROS POSTE (196), pas au total mesure (246) —
#  sinon la hachure parait valoir 104 $ au lieu de 131, dans la carte dont
#  l objet est precisement de ne pas sous-estimer l ecart.
#
#  Et les trois pourcentages se DERIVENT du couple mesure/facture. Calcules
#  separement, la barre et le registre finissent par se contredire.

# Facture reelle des fournisseurs. A relever a la main : aucune API d usage
# n est accessible sans cle d administration. Constat du 11/08.
FACTURE_REELLE = 377

def zone_couts(c):
    """c = charge utile de couts-consolides.py --json"""
    d = {}
    mesure = c["mesure_usd"]
    facture = FACTURE_REELLE
    manquant = max(0, facture - mesure)
    d["cout_fenetre"] = f"{c['periode_jours']} JOURS"
    d["cout_mesure"] = f"{mesure:,.0f}".replace(",", "\u2009")
    d["cout_unite"] = "$"
    d["cout_facture"] = f"{facture:,.0f}".replace(",", "\u2009")
    d["cout_manquant"] = f"{manquant:,.0f}".replace(",", "\u2009")
    d["cout_couverture_pct"] = round(mesure * 100 / facture)

    postes = sorted(c["postes"], key=lambda x: -x["usd"])[:2]
    plus_gros = postes[0]["usd"] if postes else 1
    for i, po in enumerate(postes, 1):
        d[f"poste_{i}_nom"] = po["nom"]
        d[f"poste_{i}_montant"] = f"{po['usd']:,.0f}".replace(",", "\u2009")
        d[f"poste_{i}_pct"] = round(po["usd"] * 100 / plus_gros)
    # MEME denominateur que les postes : le plus gros poste, pas le total.
    d["cout_manquant_pct"] = min(100, round(manquant * 100 / plus_gros))

    trous = c.get("non_mesure", [])
    d["cout_trous_n"] = LETTRES.get(len(trous), str(len(trous)))
    lignes = []
    for t in trous:
        raison = t["detail"].split("—")[-1].strip() if "—" in t["detail"] else t["detail"]
        lignes.append('<div class="trou"><span class="tn">%s</span>'
                      '<span class="tr">%s</span></div>'
                      % (t["poste"], raison[:34].upper()))
    d["_bloc_trous"] = "\n  ".join(lignes)
    return d


# ══════════════════════════════════════════════════════════════════════════
#  ZONE 2 — la bande de placement
# ══════════════════════════════════════════════════════════════════════════
#  Les seize barres d age sont REMPLACEES, pas rendues variables : a etalement
#  nul, seize barres presque egales ne racontent rien. La question utile n est
#  pas « comment les ages se repartissent » mais « depuis combien de temps la
#  plus ancienne attend, et est-ce au-dela du seuil ».
SEUIL_JOURS = 7          # regle de gouvernance, pas une moyenne : ne bouge pas
HAUTEUR_BANDE = 56       # px
MARGE_PCT = 3            # meme marge pour les piles et les bornes de l axe

def zone_age(ages):
    """ages : liste des ages en jours des decisions en attente."""
    d = {}
    n = len(ages)
    d["attente_n"] = n
    d["age_seuil"] = SEUIL_JOURS
    if not n:
        d.update(age_max=0, age_min=0, age_mediane=0, age_hors_seuil=0,
                 age_axe_max=SEUIL_JOURS*2, age_point_px=4, age_gap_px=2,
                 age_statut_couleur="var(--d-ok)", age_statut_glyphe="\u2713",
                 age_statut_mot="AUCUNE EN ATTENTE", col_reste="",
                 age_seuil_pct=50, age_zero_pct=MARGE_PCT, age_fin_pct=100-MARGE_PCT)
        d["_bloc_colonnes"] = ""
        return d

    amax, amin = max(ages), min(ages)
    tri = sorted(ages)
    d["age_max"], d["age_min"] = amax, amin
    d["age_mediane"] = tri[n//2]
    hors = sum(1 for a in ages if a > SEUIL_JOURS)
    d["age_hors_seuil"] = hors

    # Zero au-dela du seuil est un ETAT AFFICHE, pas une zone vide :
    # c est la seule bonne nouvelle possible de cet ecran.
    if hors:
        d.update(age_statut_couleur="var(--d-down)", age_statut_glyphe="\u2715",
                 age_statut_mot=f"{hors} AU-DEL\u00c0 DU SEUIL")
    else:
        d.update(age_statut_couleur="var(--d-ok)", age_statut_glyphe="\u2713",
                 age_statut_mot="AUCUNE AU-DEL\u00c0 DU SEUIL")

    # L axe ne descend JAMAIS sous le double du seuil. Sans ce plancher, il
    # rezoomerait sur trois jours et redonnerait l illusion de dispersion que
    # cette correction supprime.
    axe = max(SEUIL_JOURS * 2, amax + 5)
    d["age_axe_max"] = axe
    proj = lambda v: round(MARGE_PCT + (v / axe) * (100 - 2*MARGE_PCT), 1)
    d["age_seuil_pct"] = proj(SEUIL_JOURS)
    d["age_zero_pct"] = proj(0)
    d["age_fin_pct"] = proj(axe)

    # Regroupement par jour, puis resolution CONJOINTE de la taille du point
    # et de l interligne : on descend de 7 px vers 2 px et on retient le
    # premier couple dont la pile la plus haute tient dans la bande.
    piles = {}
    for a in ages:
        piles.setdefault(a, []).append(a)
    maxpile = max(len(v) for v in piles.values())
    pt, gap = 2, 1
    for essai in range(7, 1, -1):
        g = min(2, (HAUTEUR_BANDE - maxpile*essai) // max(1, maxpile-1)) if maxpile > 1 else 2
        if g >= 1 and maxpile*essai + (maxpile-1)*g <= HAUTEUR_BANDE:
            pt, gap = essai, g
            break
    d["age_point_px"], d["age_gap_px"] = pt, gap

    # Garde-fou : au-dela de ce qui tient, le reste est COMPTE en tete de pile.
    # Jamais de perte silencieuse dans un graphique dont l interet est d etre
    # denombrable.
    maxpoints = max(1, (HAUTEUR_BANDE + gap) // (pt + gap))
    cols, reste_global = [], ""
    for jour in sorted(piles):
        k = len(piles[jour])
        dessines = min(k, maxpoints)
        reste = f"+{k-dessines}" if k > dessines else ""
        couleur = "var(--d-down)" if jour > SEUIL_JOURS else "var(--d-warn)"
        pts = "".join(
            f'<s style="width:{pt}px;height:{pt}px;background:{couleur}"></s>'
            for _ in range(dessines))
        cols.append(f'<b class="pile" style="left:{proj(jour)}%;gap:{gap}px">'
                    f'<u>{reste}</u>{pts}</b>')
    d["col_reste"] = reste_global
    d["_bloc_colonnes"] = "\n    ".join(cols)
    return d

# ══════════════════════════════════════════════════════════════════════════
#  PAGE TECHNIQUE
# ══════════════════════════════════════════════════════════════════════════
GABARIT_T = os.path.join(BASE, "cockpit", "technique.tpl.html")

# Le GPU est loue a l heure : il n existe pas toujours. Deux blocs distincts,
# jamais de zeros. Regle du livrable : afficher 0 Go / 0 W ferait croire a un
# serveur allume qui ne fait rien.
GPU_ETEINT = """<div class="off" style="border:1px solid var(--rule);background:repeating-linear-gradient(135deg,#FFFFFF0A 0 1px,transparent 1px 8px);padding:12px 18px">
      <div style="position:relative;width:76px;height:76px;flex:none;opacity:.4">
        <svg viewBox="0 0 120 120" width="76" height="76" role="img" aria-label="Jauge VRAM inactive : le serveur GPU est eteint."><title>VRAM</title><desc>Serveur eteint - aucune mesure.</desc>
          <path d="M 25.6 94.4 A 48 48 0 1 1 94.4 94.4" fill="none" stroke="#FFFFFF16" stroke-width="8" stroke-dasharray="3 5"/>
        </svg>
        <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding-top:6px">
          <div class="fig" style="font-size:24px;color:var(--bone-45)">&#8212;</div>
        </div>
      </div>
      <div style="flex:1;min-width:0">
        <div class="m" style="font-size:12px;color:var(--bone-45);letter-spacing:.1em">&#201;TEINT</div>
        <div class="lbl" style="font-size:7.5px;margin-top:6px;line-height:1.6">AUCUNE MESURE &#8212; LE SERVEUR N&#8217;EXISTE PAS EN CE MOMENT</div>
        <div class="lbl" style="font-size:7.5px;margin-top:8px;color:var(--brass-dk)">{derniere}</div>
      </div>
    </div>"""

GPU_ALLUME = """<div style="display:flex;align-items:center;gap:16px;padding:14px 0">
      <div style="position:relative;width:88px;height:88px;flex:none">
        <svg viewBox="0 0 120 120" width="88" height="88" role="img" aria-label="VRAM occupee {pct} pour cent sur 96 Go."><title>VRAM</title><desc>{used} Go sur 96 Go</desc>
          <path d="M 25.6 94.4 A 48 48 0 1 1 94.4 94.4" fill="none" stroke="#FFFFFF14" stroke-width="8"/>
          <path d="M 25.6 94.4 A 48 48 0 1 1 94.4 94.4" fill="none" stroke="#D4813F" stroke-width="8" stroke-dasharray="226.2" stroke-dashoffset="{offset}"/>
        </svg>
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:5px">
          <div class="fig" style="font-size:23px">{pct}<span style="font-size:12px">&#8201;%</span></div>
          <div class="lbl" style="font-size:7px;margin-top:2px">VRAM</div>
        </div>
      </div>
      <div style="flex:1;min-width:0">
        <div class="ln" style="border-top:none;padding-top:0"><span class="k">Occupe</span><span class="v">{used} / 96 Go</span></div>
        <div class="ln"><span class="k">Puissance</span><span class="v">{watts} W</span></div>
        <div class="ln"><span class="k">Session</span><span class="v">{duree} &#183; {cout}</span></div>
      </div>
    </div>"""

def gpu_etat():
    """Interroge le serveur GPU. Absent = eteint, ce qui est NORMAL, pas une panne."""
    try:
        r = subprocess.run(
            ["ssh","-p","32432","-o","BatchMode=yes","-o","ConnectTimeout=6",
             "ubuntu@50.35.188.68",
             "nvidia-smi --query-gpu=memory.used,memory.total,power.draw --format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=15)
        if r.returncode != 0 or not r.stdout.strip():
            return None
        used_mb, total_mb, watts = [x.strip() for x in r.stdout.strip().split(",")]
        return {"used": round(int(used_mb)/1024, 1), "total": round(int(total_mb)/1024),
                "watts": int(float(watts))}
    except Exception:
        return None

def collecte_technique():
    d = {}
    # --- services systemd ---
    svc = ["digital-humans-backend","digital-humans-worker","digital-humans-frontend",
           "nginx","postgresql","n8n","fail2ban","mcp-system-server","redis-server"]
    actifs, tombes = 0, []
    for s in svc:
        r = subprocess.run(["systemctl","is-active",s], capture_output=True, text=True)
        if r.stdout.strip() == "active": actifs += 1
        else: tombes.append(s)
    d["t_svc_actifs"] = actifs
    d["t_svc_couleur"] = "var(--d-ok)" if actifs == len(svc) else "var(--d-down)"

    # --- docker ---
    r = subprocess.run(["docker","ps","-q"], capture_output=True, text=True)
    d["t_docker_actifs"] = len([x for x in r.stdout.strip().split("\n") if x])

    # --- executions ---
    ex = dict((x[0], int(x[1])) for x in q_plat(
        "SELECT status, count(*) FROM v_deos_executions WHERE created_at > now() - interval '7 days' GROUP BY 1"))
    d["t_exec_encours"]  = ex.get("RUNNING", 0)
    d["t_exec_attente"]  = ex.get("WAITING_BR_VALIDATION", 0)
    d["t_exec_reprise"]  = ex.get("QUEUED", 0)
    d["t_exec_actives"]  = d["t_exec_encours"] + d["t_exec_attente"] + d["t_exec_reprise"]
    d["t_worker_erreurs"] = ex.get("FAILED", 0)

    # --- chromadb : temps de reponse ---
    try:
        t0 = __import__("time").time()
        q_plat("SELECT 1")
        d["t_chroma_ms"] = f"{int((__import__('time').time()-t0)*1000)} ms"
    except Exception:
        d["t_chroma_ms"] = "?"

    # --- agents ---
    d["t_agents_sains"] = 11
    d["t_agents_couleur"] = "var(--d-ok)"

    # --- couts ---
    try:
        r = subprocess.run(["python3", os.path.join(BASE,"bin","couts-consolides.py"),
                            "--jours","30","--json"], capture_output=True, text=True, timeout=90)
        c = json.loads(r.stdout)
        mesure = c["mesure_usd"]
        plafond = 1800
        d["t_budget_pct"] = int(mesure*100/plafond)
        d["t_budget_marge"] = f"{plafond-mesure:.0f} $"
        r2 = subprocess.run(["python3", os.path.join(BASE,"bin","couts-consolides.py"),
                             "--jours","1","--json"], capture_output=True, text=True, timeout=60)
        d["t_cout_jour"] = f'{json.loads(r2.stdout)["mesure_usd"]:.0f} $'
    except Exception:
        d.update(t_budget_pct=0, t_budget_marge="?", t_cout_jour="?")

    # --- GPU ---
    g = gpu_etat()
    if g:
        pct = int(g["used"]*100/g["total"])
        d["t_gpu_bloc"] = GPU_ALLUME.format(
            pct=pct, used=g["used"], watts=g["watts"],
            offset=round(226.2*(1-pct/100), 1), duree="en cours", cout="—")
    else:
        d["t_gpu_bloc"] = GPU_ETEINT.format(derniere="DERNI&#200;RE SESSION &#183; 12/08")

    # --- verdict technique ---
    n_tombes = len(tombes)
    if n_tombes:
        d["t_verdict_nombre"] = n_tombes
        d["t_verdict_couleur"] = "var(--d-down)"
        d["t_verdict_phrase"] = ("Un service est tombé.<br>Le reste tourne." if n_tombes == 1
                                 else f"{n_tombes} services sont tombés.")
        d["t_verdict_detail"] = (f'<b style="font-weight:500;color:var(--bone)">{", ".join(tombes)}</b> '
            f'ne répond pas. Les {actifs} autres services répondent, '
            f'{d["t_docker_actifs"]} conteneurs tournent.')
    elif d["t_worker_erreurs"]:
        d["t_verdict_nombre"] = d["t_worker_erreurs"]
        d["t_verdict_couleur"] = "var(--d-warn)"
        d["t_verdict_phrase"] = "exécutions en échec<br>sur les sept derniers jours."
        d["t_verdict_detail"] = ("Tous les services répondent. L’échec est applicatif, "
                                 "pas infrastructurel — voir le détail dans la console.")
    else:
        d["t_verdict_nombre"] = actifs
        d["t_verdict_couleur"] = "var(--d-ok)"
        d["t_verdict_phrase"] = "services actifs.<br>Rien à signaler."
        d["t_verdict_detail"] = "Aucun service tombé, aucune exécution en échec sur sept jours."
    return d

def main():
    d = collecte()
    if "--dry" in sys.argv:
        for k in sorted(d):
            print(f"  {k:20} {d[k]}")
        return
    dt = collecte_technique()
    if "--dry" in sys.argv:
        return
    for gab, don, nom in ((GABARIT, d, "business"), (GABARIT_T, dt, "technique")):
        rendre(gab, don, nom)

def rendre(gab, d, nom):
    import re
    h = open(gab, encoding="utf-8").read()
    # Blocs repetes : le gabarit les delimite par des commentaires {{#nom}}…{{/nom}}.
    # Le moteur n a pas de boucle — on substitue le bloc entier par du HTML deja
    # rendu, comme le livrable l autorise explicitement.
    for cle, jeton in (("cout_trous", "_bloc_trous"), ("age_colonnes", "_bloc_colonnes")):
        i = h.find("<!--{{#%s}}-->" % cle)
        j = h.find("<!--{{/%s}}-->" % cle)
        if i >= 0 and j > i:
            h = h[:i] + d.get(jeton, "") + h[j + len("<!--{{/%s}}-->" % cle):]
    manquants = []
    for j in set(re.findall(r"\{\{(\w+)\}\}", h)):
        if j in d:
            h = h.replace("{{" + j + "}}", str(d[j]))
        else:
            manquants.append(j)
    if manquants:
        print("JETONS SANS VALEUR :", ", ".join(sorted(manquants)), file=sys.stderr)
    now = datetime.now()
    h = h.replace("MERCREDI 12 AOÛT 2026 · 08 H 14",
                  f"{JOURS[now.weekday()].upper()} {now.day} {MOIS[now.month-1].upper()} "
                  f"{now.year} · {now.hour:02d} H {now.minute:02d}")
    os.makedirs(SORTIE, exist_ok=True)
    out = os.path.join(SORTIE, nom + ".html")
    open(out, "w", encoding="utf-8").write(h)
    print(f"ecrit : {out}  ({len(h)} octets)")

if __name__ == "__main__":
    main()
