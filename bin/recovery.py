#!/usr/bin/env python3
"""Recovery Sprint — trie les decisions accordees et repart d'une file propre.

LOT-09, 18/08/2026. Voir docs/RECOVERY_2026-08.md pour la trace du tri.

POURQUOI CET OUTIL EXISTE
-------------------------
Quarante decisions accordees, la plus ancienne a quatorze jours. Une partie n'a
plus d'objet, une autre est deja faite sans que rien ne le prouve, une troisieme
attend reellement. Tant que les trois cohabitent, aucun compteur du comite n'est
lisible : le score d'execution du 17/08 tombait a 0/100 sur un stock dont
personne ne savait quelle part decrivait du travail reel.

CE QUE L'OUTIL FAIT, ET CE QU'IL NE FAIT PAS
--------------------------------------------
Il pose a chaque decision les six questions du lot, dans l'ordre, et il ENREGISTRE
ce qui a ete decide. Il ne decide pas lui-meme. Deux etages, exactement comme la
detection de preuves de bin/cloturer-prouvees.py :

  1. MECANIQUE — le script cherche les empreintes disponibles (commit citant la
     decision, cle metier en base) et propose un classement.
  2. RELECTURE — le Chief of Staff lit et tranche. Il ne clot jamais sur la seule
     empreinte.

La lecon du 17/08 est la raison d'etre de cette separation : sur neuf decisions
que la detection croyait faites, la relecture n'en a valide qu'UNE SEULE. Les
autres etaient partielles — un commit qui prepare mais ne deploie pas, deux
volets demandes dont un seul traite.

CE QUI COMPTE COMME EMPREINTE
-----------------------------
Tout document qui PARLE des decisions ressemble a une preuve : rapports, briefs,
calendriers de suivi, fiches d'agents, et cette page de suivi meme. La premiere
version de la detection en trouvait trente-cinq au lieu de six. Seul le commit
porte un travail date et signe ; une cle de deos_state ne compte que si elle
porte un etat metier, pas un recit.

ON NE CROIT PAS LE COMPTE RENDU, ON RELIT LA BASE
-------------------------------------------------
Le verdict inscrit au journal n'est pas ce que le relecteur DIT avoir fait :
c'est l'ecart constate entre l'etat de la decision avant et apres. Un agent qui
annonce une cloture sans l'ecrire laisse une trace « sans decision », pas une
trace de cloture. C'est l'invariant I3 applique a l'outil qui mesure : un
indicateur calcule sur ce que l'evalue declare mesure la declaration.

USAGE
-----
  recovery.py                      simulation : le classement mecanique, rien d'ecrit
  recovery.py --appliquer          lance la relecture, decision par decision
  recovery.py --appliquer --limite 5 --decision DEC-2026-0802-01
  recovery.py --rapport            etat du tri, et les trois criteres du lot
  recovery.py --trace              (re)genere docs/RECOVERY_2026-08.md

ECRITURES
---------
Le script n'ecrit JAMAIS dans decisions ni dans tasks : la table decisions ne se
manipule que via bin/deos-decisions, les taches via bin/deos-tasks, et c'est le
relecteur qui les appelle. Le seul fichier que ce script ecrit est son journal.
"""
import argparse, json, os, re, shlex, subprocess, sys
from datetime import datetime, timezone

RACINE = os.environ.get("DH_RACINE", "/workspace")
JOURNAL = os.path.join(RACINE, "docs", "recovery-2026-08.json")
TRACE = os.path.join(RACINE, "docs", "RECOVERY_2026-08.md")

# Depots ou chercher un commit citant la decision. /workspace est present ici et
# absent de cloturer-prouvees.py : c'etait un angle mort. Les decisions qui
# portent sur le dispositif du comite lui-meme — garde-fou, tableau de bord,
# outils — laissent leur commit dans CE depot et nulle part ailleurs. Les
# chercher uniquement dans les depots de la plateforme revenait a les declarer
# sans empreinte par construction.
DEPOTS = os.environ.get("RECOVERY_DEPOTS", "/repo-delivery:/repo:" + RACINE).split(":")

# Cles de deos_state ou l'on PARLE des decisions au lieu de les appliquer. La
# liste vient de cloturer-prouvees.py (correctif du 17/08 : 35 candidats au lieu
# de 6) et s'allonge de trois entrees decouvertes par ce lot :
#   priorites_  — la liste des priorites de semaine cite les decisions par leur
#                 identifiant ; elle prouve qu'on les a classees, pas traitees.
#   recovery    — le journal de ce tri-ci. Sans cette exclusion, la deuxieme
#                 passe prendrait la premiere pour une preuve de travail.
#   page        — la page de suivi, meme motif que les rapports.
NARRATIVES = ("rapport_", "brief", "calendrier_", "journal", "suivi_",
              "priorites_", "recovery", "page", "ronde")

DIRECTIONS = ("commercial", "marketing", "delivery", "cs", "legal", "financier", "growth")

# Les six questions du lot, dans l'ordre. L'ordre n'est pas cosmetique : une
# decision sans objet ne merite pas qu'on cherche si elle est faite, et une
# decision faite ne merite pas qu'on lui ecrive une tache.
QUESTIONS = {
    1: ("Plus nécessaire ?", "`obsolete` avec motif"),
    2: ("Déjà réalisée ?", "demander la preuve, puis `propose_cloture`"),
    3: ("Partiellement réalisée ?", "créer les tâches restantes"),
    4: ("Bloquée ?", "nommer le `blocker`, poser `next_action` et `next_owner`"),
    5: ("Mal définie ?", "reformuler, ou renvoyer en `attente_sam`"),
    6: ("Encore pertinente ?", "au moins une tâche avec porteur et échéance"),
}

# Statuts qui portent encore du travail. C'est la definition de « file active »
# du critere 3. propose_cloture n'en fait pas partie : elle attend une relecture,
# pas un travail. needs_decision et attente_sam non plus : elles attendent Sam.
ACTIFS = ("accordee", "en_execution", "blocked", "failed")


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sql(requete):
    """Lecture seule. Toute ecriture passe par deos-decisions ou deos-tasks."""
    dsn = os.environ.get("COMITE_DB_DSN")
    if not dsn:
        sys.exit("REFUS: COMITE_DB_DSN absent — l'outil lit la base du comite")
    r = subprocess.run(["psql", dsn, "-tAF", "|", "-v", "ON_ERROR_STOP=1", "-c", requete],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        sys.exit("REFUS: lecture impossible — " + r.stderr.strip()[:300])
    return [l.split("|") for l in r.stdout.strip().split("\n") if l]


# ── Etage 1 : les empreintes ────────────────────────────────────────────────

def commit_citant(dec):
    """Un commit dont le message cite la decision et qui a touche des fichiers.
    C'est la seule empreinte forte : datee, signee, et son contenu est lisible."""
    for depot in DEPOTS:
        if not os.path.isdir(os.path.join(depot, ".git")):
            continue
        r = subprocess.run(["git", "log", "--all", "--format=%H|%s", f"--grep={dec}"],
                           cwd=depot, capture_output=True, text=True, timeout=30)
        for ligne in r.stdout.strip().split("\n"):
            if "|" not in ligne:
                continue
            h, sujet = ligne.split("|", 1)
            n = subprocess.run(["git", "show", "--stat", "--format=", h],
                               cwd=depot, capture_output=True, text=True, timeout=20)
            if n.stdout.strip():
                return {"genre": "commit", "depot": depot,
                        "ref": h[:8], "sujet": sujet[:70]}
    return None


def cle_metier(dec):
    """Une decision reglee par une ecriture en base laisse une cle dans
    deos_state. On ne retient que les cles qui portent un ETAT METIER : les
    cles narratives sont exclues, sinon un brief qui mentionne la decision
    passerait pour la preuve qu'elle est traitee."""
    for (cle,) in [(x[0],) for x in sql(
            f"SELECT cle FROM deos_state WHERE valeur::text ILIKE '%{dec}%' LIMIT 10")]:
        if not any(cle.startswith(n) for n in NARRATIVES):
            return {"genre": "base", "ref": "deos_state / " + cle}
    return None


def citee_par_plus_recente(dec):
    """Une decision plus recente qui cite celle-ci : soit elle la remplace, soit
    elle la precise. Ce n'est PAS une preuve de travail — c'est un signal de
    doublon ou de peremption, a verifier par la relecture. La proposition de tri
    du 11/08 avait identifie quatre groupes de doublons exactement ainsi."""
    r = sql(f"""SELECT id FROM decisions
                 WHERE id <> '{dec}' AND date > (SELECT date FROM decisions WHERE id='{dec}')
                   AND (texte ILIKE '%{dec}%' OR porte_sur = '{dec}')
                 ORDER BY date LIMIT 3""")
    return [x[0] for x in r] or None


def etat(dec):
    r = sql(f"""SELECT d.statut, (now()::date - d.date::date),
                       coalesce((SELECT count(*) FROM tasks t WHERE t.decision_id = d.id), 0),
                       d.origine,
                       coalesce((SELECT t.owner FROM tasks t WHERE t.decision_id = d.id
                                  ORDER BY t.id LIMIT 1), d.origine)
                  FROM decisions d WHERE d.id = '{dec}'""")
    if not r:
        return None
    statut, age, taches, origine, porteuse = r[0]
    return {"statut": statut, "age_j": int(age), "taches": int(taches),
            "origine": origine, "porteuse": porteuse}


def classement(dec):
    """Le classement MECANIQUE. Il ne repond qu'a la question 2, et seulement
    par « il existe une empreinte » — pas par « c'est fait ». Les questions 1,
    3, 4, 5 et 6 demandent de lire la decision et le travail : aucune regle
    mecanique ne les tranche, et pretendre le contraire est le defaut meme que
    la relecture du 17/08 a mis au jour."""
    e = commit_citant(dec) or cle_metier(dec)
    proches = citee_par_plus_recente(dec)
    return {"empreinte": e, "citee_par": proches,
            "proposition": "candidate deja faite" if e else
                           "candidate doublon ou peremption" if proches else
                           "sans empreinte — les six questions"}


# ── Le journal ──────────────────────────────────────────────────────────────

def charger(chemin):
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    return None


def enregistrer(chemin, j):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")


def depart(chemin):
    """La liste de depart est figee au premier passage et ne bouge plus.

    POURQUOI. Sans instantane, « 40 traitees » se mesurerait contre la file du
    jour — qui retrecit a mesure qu'on la traite. Le compteur afficherait alors
    toujours 100 %, y compris apres avoir ne rien fait : il suffirait qu'une
    decision sorte du statut accordee pour disparaitre du denominateur. Un
    indicateur qui se recalcule sur la population survivante ne mesure rien."""
    j = charger(chemin)
    if j:
        return j
    lignes = sql("SELECT id, origine, left(replace(texte, '|', '/'), 120), "
                 "(now()::date - date::date), date::date "
                 "FROM decisions WHERE statut = 'accordee' ORDER BY date")
    j = {"ouvert_le": maintenant(), "decisions": {}}
    for id_, origine, texte, age, d in lignes:
        j["decisions"][id_] = {"origine": origine, "texte": texte,
                               "age_depart_j": int(age), "date": d,
                               "avant": {"statut": "accordee"}, "passages": []}
    enregistrer(chemin, j)
    return j


# ── Etage 2 : la relecture ──────────────────────────────────────────────────

INVITE = """Tu es le Chief of Staff. Tu traites UNE decision du Recovery Sprint : {dec}.

{contexte}

Empreinte trouvee mecaniquement : {empreinte}
{doublon}
Pose-lui les six questions DANS CET ORDRE, arrete-toi a la premiere qui repond oui :

1. Plus necessaire ?        -> deos-decisions status {dec} obsolete --par cos --motif "..."
2. Deja realisee ?          -> lis l'empreinte (git show, la cle en base). Si elle couvre
                               VRAIMENT tout ce que la decision demandait :
                               deos-decisions status {dec} clos --par cos \\
                                 --preuve '{{"relu_par":"cos","empreinte":"...","constat":"..."}}'
                               Si tu as le moindre doute, ou s'il manque un volet, NE CLOS PAS :
                               demande la preuve au porteur en creant la tache
                               deos-tasks add --decision {dec} --titre "fournir la preuve de realisation" \\
                                 --critere-fin "la decision est en propose_cloture avec preuve" \\
                                 --owner {porteuse} --echeance {echeance_courte} --par cos
3. Partiellement realisee ? -> deos-tasks add ... pour CE QUI RESTE, une tache par volet
4. Bloquee ?                -> deos-decisions status {dec} blocked --par {porteuse} \\
                                 --blocker "..." --next-action "..." --next-owner "..."
5. Mal definie ?            -> reformule si c'est evident, sinon
                               deos-decisions status {dec} needs_decision --par {porteuse} --question "..."
6. Encore pertinente ?      -> deos-tasks add --decision {dec} --titre "..." \\
                                 --critere-fin "<verifiable par une commande>" --owner <direction> \\
                                 --echeance {echeance} --par cos

Pour lire la decision : psql "$COMITE_DB_DSN" -x -c "SELECT * FROM decisions WHERE id='{dec}';"

TROIS INTERDITS
- Ne clos JAMAIS dans le doute. Une decision close sort du radar et personne n'y
  revient. Laisser trainer est moins grave que fermer a tort.
- Ne marque JAMAIS refusee ce qui est obsolete : refusee est un jugement,
  obsolete est une peremption. Confondre les deux salit le signal.
- Une empreinte prouve qu'un travail a eu lieu, PAS qu'il fait ce que la decision
  demandait. Le 17/08, sur neuf decisions que la detection croyait faites, une
  seule l'etait.

Une decision qui reste accordee DOIT porter au moins une tache : sans cela elle
retourne exactement dans le stock qu'on est en train de vider.

Termine par exactement deux lignes :
QUESTION: <le numero de la question a laquelle tu as repondu oui>
MOTIF: <une phrase, ce que devient la decision et pourquoi>"""


def relire(dec, cl, e, args):
    """Lance le relecteur, puis RELIT LA BASE. Le verdict vient de l'ecart
    constate, jamais du compte rendu."""
    empreinte = "aucune"
    if cl["empreinte"]:
        c = cl["empreinte"]
        empreinte = f"[{c['genre']}] " + (f"{c['ref']} — {c.get('sujet','')} (depot {c['depot']})"
                                          if c["genre"] == "commit" else c["ref"])
    doublon = ""
    if cl["citee_par"]:
        doublon = ("Decision(s) plus recente(s) qui la citent : " + ", ".join(cl["citee_par"]) +
                   "\nCe n'est pas une preuve de travail : c'est un signal de doublon ou de\n"
                   "peremption. Va lire ces decisions avant de repondre a la question 1.\n")
    contexte = (f"Elle a {e['age_j']} jours, elle vient de {e['origine']}, "
                f"la direction porteuse est {e['porteuse']}, "
                f"elle porte {e['taches']} tache(s).")

    invite = INVITE.format(dec=dec, contexte=contexte, empreinte=empreinte, doublon=doublon,
                           porteuse=e["porteuse"] if e["porteuse"] in DIRECTIONS else "delivery",
                           echeance=args.echeance, echeance_courte=args.echeance_courte)

    # RECOVERY_RELECTEUR permet de rejouer le tri avec un autre relecteur — et
    # surtout de tester ce script sans depenser un appel de modele. La commande
    # recoit l'invite en dernier argument, comme claude -p.
    cmd = shlex.split(os.environ["RECOVERY_RELECTEUR"]) if os.environ.get("RECOVERY_RELECTEUR") else [
        "claude", "-p", "--model", args.modele,
        "--allowedTools", "Bash,Read,Grep,Glob", "--output-format", "json"]
    r = subprocess.run(cmd + [invite], capture_output=True, text=True, timeout=args.delai,
                       env={**os.environ, "DH_DIRECTION": "chief-of-staff",
                            "PATH": os.environ.get("PATH", "") + ":" + os.path.join(RACINE, "bin")})
    sortie = r.stdout
    try:
        sortie = json.loads(r.stdout).get("result") or ""
    except Exception:
        pass
    question = re.search(r"^QUESTION:\s*([1-6])", sortie, re.M)
    motif = re.search(r"^MOTIF:\s*(.+)", sortie, re.M)
    return {"question_declaree": int(question.group(1)) if question else None,
            "motif": (motif.group(1).strip()[:300] if motif else sortie.strip()[-300:]),
            "code_retour": r.returncode}


def verdict(avant, apres, declaree=None):
    """Le verdict est l'ecart constate en base, et lui seul.

    « sans decision » n'est pas un echec du relecteur, c'est un fait a inscrire :
    le critere 1 du lot compte precisement ces cas. Les masquer en reprenant le
    dire de l'agent transformerait le rapport en autoportrait.

    UNE SEULE AMBIGUITE EST LEVEE PAR LA DECLARATION. Trois questions
    aboutissent au meme fait en base — une tache de plus : la 2 quand la preuve
    est DEMANDEE au porteur plutot que constatee, la 3 pour ce qui reste d'un
    travail commence, la 6 pour le premier pas d'un travail encore pertinent.
    Une ligne de tasks ne les distingue pas, et il n'y a rien a inventer pour
    les departager. On garde donc le numero annonce dans ce cas precis, et dans
    celui-la seulement : le FAIT reste verifie en base des trois cotes."""
    if apres["statut"] != avant["statut"]:
        return {"obsolete": 1, "clos": 2, "propose_cloture": 2,
                "blocked": 4, "failed": 4,
                "needs_decision": 5, "attente_sam": 5,
                "refusee": 5, "en_execution": 6}.get(apres["statut"], 6), apres["statut"]
    if apres["taches"] > avant["taches"]:
        return (declaree if declaree in (2, 3, 6) else 6), "taches creees"
    return None, "sans decision"


# ── Les trois modes ─────────────────────────────────────────────────────────

def simuler(j, ids, args):
    print(f"{len(ids)} decision(s) a trier — SIMULATION, rien n'est ecrit")
    print()
    seaux = {}
    for dec in ids:
        cl = classement(dec)
        e = etat(dec)
        seaux.setdefault(cl["proposition"], []).append((dec, e, cl))
    for prop, lignes in seaux.items():
        print(f"— {prop} ({len(lignes)})")
        for dec, e, cl in lignes:
            ref = ""
            if cl["empreinte"]:
                ref = f"[{cl['empreinte']['genre']}] {cl['empreinte'].get('sujet') or cl['empreinte']['ref']}"
            elif cl["citee_par"]:
                ref = "citee par " + ", ".join(cl["citee_par"])
            print(f"   {dec}  {e['age_j']:>2}j  {e['porteuse']:<10} {ref[:60]}")
        print()
    print("Le classement mecanique ne DECIDE rien : il propose. Relancer avec")
    print("--appliquer pour que le Chief of Staff lise et tranche.")


def appliquer(j, ids, args):
    print(f"{len(ids)} decision(s) — relecture par le Chief of Staff")
    print()
    for dec in ids:
        e = etat(dec)
        if e is None:
            print(f"  {dec} : introuvable en base — ignoree")
            continue
        avant = {"statut": e["statut"], "taches": e["taches"]}
        cl = classement(dec)
        rel = relire(dec, cl, e, args)
        apres_e = etat(dec)
        apres = {"statut": apres_e["statut"], "taches": apres_e["taches"]}
        q, devenue = verdict(avant, apres, rel["question_declaree"])

        passage = {"le": maintenant(), "avant": avant, "apres": apres,
                   "empreinte": cl["empreinte"], "citee_par": cl["citee_par"],
                   "question": q, "question_declaree": rel["question_declaree"],
                   "devenue": devenue, "motif": rel["motif"]}
        # L'ecart entre la question annoncee et le changement constate se garde :
        # c'est le signal le plus utile pour relire ce tri dans trois mois. Le cas
        # ou il compte le plus est justement celui ou rien n'a bouge — un relecteur
        # qui annonce une cloture sans l'ecrire. Le tester sur « q non nul »
        # laissait passer exactement ce cas-la.
        if rel["question_declaree"] and rel["question_declaree"] != q:
            passage["ecart"] = (f"annonce la question {rel['question_declaree']}, "
                                f"la base montre {devenue}")
        j["decisions"].setdefault(dec, {"passages": []})["passages"].append(passage)
        enregistrer(args.journal, j)   # apres CHAQUE decision : une relecture
                                       # interrompue ne doit pas perdre les
                                       # precedentes. C'est arrive le 17/08.
        marque = "!" if q is None else " "
        print(f" {marque}{dec}  {avant['statut']} -> {devenue}  ({rel['motif'][:70]})")
    print()
    print(f"Journal : {args.journal}")
    print("Verifier avec --rapport, puis produire la trace avec --trace.")


def rapport(j, args):
    total = len(j["decisions"])
    traitees, sans, par_devenir = 0, [], {}
    for dec, d in j["decisions"].items():
        e = etat(dec)
        if e is None:
            continue
        avant = d.get("avant", {"statut": "accordee"})
        # « Traitee » se mesure en base, pas au journal : une decision dont le
        # statut a bouge OU qui porte desormais une tache a recu un traitement.
        # Une decision encore accordee et sans tache n'en a pas recu, meme si le
        # journal contient un passage disant le contraire.
        if e["statut"] != avant["statut"] or e["taches"] > 0:
            traitees += 1
            cle = e["statut"] if e["statut"] != avant["statut"] else "accordee + tache"
            par_devenir[cle] = par_devenir.get(cle, 0) + 1
        else:
            sans.append(dec)

    print(f"Recovery Sprint — ouvert le {j['ouvert_le'][:10]}")
    print()
    print(f"  {total} de depart · {traitees} traitees · {len(sans)} sans decision")
    print()
    for k in sorted(par_devenir, key=lambda x: -par_devenir[x]):
        print(f"    {par_devenir[k]:>3}  {k}")
    if sans:
        print()
        print("  Sans decision — encore accordees et sans tache :")
        for dec in sans:
            print(f"    {dec}")

    orphelines = int(sql("SELECT count(*) FROM decisions d WHERE d.statut = 'accordee' "
                         "AND NOT EXISTS (SELECT 1 FROM tasks t WHERE t.decision_id = d.id)")[0][0])
    active = int(sql("SELECT count(*) FROM decisions WHERE statut IN ("
                     + ", ".join("'" + s + "'" for s in ACTIFS) + ")")[0][0])
    print()
    print("  Criteres du lot")
    print(f"    1. chaque decision de depart traitee ......... {traitees}/{total}"
          f"  {'OK' if len(sans) == 0 else 'NON — ' + str(len(sans)) + ' sans decision'}")
    print(f"    2. accordees sans tache ..................... {orphelines}"
          f"       {'OK' if orphelines == 0 else 'NON'}")
    print(f"    3. file active (accordee, en_execution, blocked, failed) ... {active}"
          f"   {'OK' if 10 <= active <= 15 else 'hors de la fourchette 10-15'}")


METHODE = """## Pourquoi ce tri

Quarante décisions accordées, la plus ancienne de quatorze jours. Une partie n'a plus
d'objet, une autre est déjà faite sans que rien ne le prouve, une troisième attend
réellement. Tant que les trois cohabitent, aucun compteur du comité n'est lisible :
le score d'exécution du 17/08 tombait à 0/100 sur un stock dont personne ne savait
quelle part décrivait du travail réel. Traiter ce passif n'est pas du rangement —
c'est la condition pour que le nouveau tableau de bord (LOT-10) mesure quelque chose.

## Pourquoi ce document existe

Dans trois mois, personne ne se souviendra pourquoi telle décision de début août a
été marquée obsolète. Une décision qui sort de la file sans motif écrit revient sous
une autre forme, et le même travail se refait depuis zéro. C'est un document
d'archive : il est fait pour être relu longtemps après, par quelqu'un qui n'était
pas là.

Il est **généré** par `bin/recovery.py --trace`, jamais tenu à la main. Une trace
recopiée diverge de la base dès la première correction — et c'est alors la trace
qu'on croit.

## La méthode : deux étages

1. **Mécanique.** Le script cherche les empreintes disponibles et propose un
   classement. Il ne répond qu'à une seule des six questions, et seulement par
   « il existe une empreinte » — jamais par « c'est fait ».
2. **Relecture.** Le Chief of Staff lit la décision, lit ce que l'empreinte
   désigne réellement, et tranche. **Il ne clôt jamais sur la seule empreinte.**

La séparation vient d'un constat daté. Le 17/08, sur neuf décisions que la détection
croyait faites, la relecture n'en a validé qu'**une seule**. Les autres étaient
partielles : un commit qui prépare mais ne déploie pas, deux volets demandés dont un
seul traité. Une empreinte prouve qu'un travail a eu lieu, pas qu'il fait ce que la
décision demandait — et aucune règle mécanique ne vérifie cela.

## Ce qui compte comme preuve, et ce qui n'en est pas

Tout document qui **parle** des décisions ressemble à une preuve : rapports, briefs,
calendriers de suivi, priorités de la semaine, fiches d'agents, page de suivi du
Chief of Staff. La première version de la détection en trouvait trente-cinq au lieu
de six. **Seul le commit porte un travail daté et signé** ; une clé de `deos_state`
ne compte que si elle porte un état métier, pas un récit.

Le journal de ce tri est exclu au même titre : sans cela, une seconde passe prendrait
la première pour une preuve de travail.

Les dépôts fouillés sont `/repo-delivery`, `/repo` et le dépôt du comité lui-même.
Ce dernier manquait à `bin/cloturer-prouvees.py` : les décisions qui portent sur le
dispositif du comité — garde-fou, tableau de bord, outils — laissent leur commit là
et nulle part ailleurs. Les chercher uniquement dans les dépôts de la plateforme
revenait à les déclarer sans empreinte par construction.

## `obsolete` n'est pas `refusee`

`refusee` est un jugement : la chose a été examinée et écartée. `obsolete` est une
péremption : elle n'a plus d'objet. Marquer `refusee` ce qui est périmé salit le
signal — on croit relire un arbitrage là où il n'y a eu qu'un calendrier qui a
tourné.

## Ce que « traitée » veut dire ici

Une décision est traitée si son statut a changé **ou** si elle porte désormais au
moins une tâche. Ce n'est pas mesuré au journal mais **en base** : un relecteur qui
annonce une clôture sans l'écrire laisse une trace « sans decision ». Le verdict est
l'écart constaté, jamais le compte rendu — c'est l'invariant I3 appliqué à l'outil
qui mesure.

La **file active** compte les statuts qui portent encore du travail : `accordee`,
`en_execution`, `blocked`, `failed`. `propose_cloture` attend une relecture,
`needs_decision` et `attente_sam` attendent Sam : ce sont des attentes, pas du
travail en cours.
"""


def trace(j, args):
    """Le document d'archive. Il porte le raisonnement autant que le resultat :
    un fichier qui listerait les issues sans dire pourquoi elles ont ete
    retenues ne compte pas comme documentation (LOT-00)."""
    traites = sum(1 for d in j["decisions"].values() if d.get("passages"))
    ouverture = (f"Ouvert le {j['ouvert_le'][:10]}, genere" if j["decisions"]
                 else "Genere")
    lignes = ["# Recovery Sprint — la trace du tri",
              "",
              f"> {ouverture} le {maintenant()[:10]} par `bin/recovery.py --trace`.",
              "> Ne pas modifier à la main : régénéré depuis `docs/recovery-2026-08.json`",
              "> et la base. LOT-09.",
              "",
              METHODE]

    if traites == 0:
        # La file de depart n'est figee qu'au premier passage sur la base reelle.
        # Annoncer un compte avant ce passage donnerait un chiffre pris ailleurs
        # — sur une base de repetition — et c'est exactement le genre de chiffre
        # qu'on relit six mois plus tard en le croyant reel.
        etat_file = (f"La file de départ est figée : **{len(j['decisions'])} décisions",
                     f"accordées** au {j['ouvert_le'][:10]}.") if j["decisions"] else (
                    "La file de départ sera figée au premier passage sur la base du",
                    "comité, et ne bougera plus ensuite.")
        lignes += ["## Où en est le tri",
                   "",
                   "**Le tri n'a pas encore été conduit.** L'outil est livré et sa répétition",
                   "est passée : `tests/recovery.sh`, 14 cas.",
                   "",
                   etat_file[0], etat_file[1],
                   "",
                   "Il se conduit depuis le conteneur du comité, en quatre temps :",
                   "",
                   "```bash",
                   "/workspace/bin/recovery.py                 # le classement mécanique, rien d'écrit",
                   "/workspace/bin/recovery.py --appliquer     # la relecture, décision par décision",
                   "/workspace/bin/recovery.py --rapport       # les trois critères du lot",
                   "/workspace/bin/recovery.py --trace         # ce document, rempli",
                   "```",
                   "",
                   "Commencer par `--limite 3` : la première passe coûte quelques appels de",
                   "modèle, et se relit en entier avant d'engager le reste de la file.",
                   ""]

    lignes += ["## Les six questions, dans l'ordre", "",
               "L'ordre n'est pas cosmétique : une décision sans objet ne mérite pas qu'on",
               "cherche si elle est faite, et une décision faite ne mérite pas qu'on lui",
               "écrive une tâche. On s'arrête à la première question qui répond oui.",
               "",
               "| Question | Action si oui | Décisions |", "| --- | --- | ---: |"]
    compte = {}
    for dec, d in j["decisions"].items():
        p = d["passages"][-1] if d.get("passages") else None
        k = p["question"] if p and p["question"] else None
        compte[k] = compte.get(k, 0) + 1
    for n, (que, act) in QUESTIONS.items():
        lignes.append(f"| {n}. {que} | {act} | {compte.get(n, 0)} |")
    lignes.append(f"| — | sans decision | {compte.get(None, 0)} |")
    lignes += ["",
               "Les questions 2, 3 et 6 peuvent produire le même fait en base — une tâche de",
               "plus : la 2 quand la preuve est *demandée* au porteur au lieu d'être",
               "constatée, la 3 pour ce qui reste, la 6 pour le premier pas. On garde alors",
               "le numéro annoncé par le relecteur ; le fait, lui, reste vérifié des trois",
               "côtés.",
               ""]

    lignes += ["## Ce que chaque décision est devenue", ""]
    if not j["decisions"]:
        lignes += ["*Vide tant que le tri n'a pas été conduit : cette table se remplit",
                   "décision par décision, au fur et à mesure des passes.*", ""]
    lignes += ["| Décision | Âge au départ | Question | Devenue | Pourquoi |",
               "| --- | ---: | ---: | --- | --- |"]
    sans = []
    for dec in sorted(j["decisions"]):
        d = j["decisions"][dec]
        p = d["passages"][-1] if d.get("passages") else None
        e = etat(dec)
        devenue = e["statut"] if e else "introuvable"
        if e and e["statut"] == "accordee" and e["taches"] > 0:
            devenue = f"accordee, {e['taches']} tâche(s)"
        que = str(p["question"]) if p and p["question"] else "—"
        motif = (p["motif"] if p else "pas encore triée").replace("|", "/")
        if e and e["statut"] == "accordee" and e["taches"] == 0 and p:
            sans.append(dec)
        lignes.append(f"| {dec} | {d.get('age_depart_j','—')} j | {que} | {devenue} | {motif} |")

    if sans:
        lignes += ["", "## Restées sans décision", "",
                   "Relues, et encore `accordee` sans tâche. Elles sont nommées ici plutôt que",
                   "passées sous silence : le lot demande que chaque décision de départ reçoive",
                   "un traitement, et ne pas l'avoir obtenu est un fait du tri, pas un détail",
                   "de mise en œuvre.",
                   ""]
        lignes += [f"- {d}" for d in sans]
    lignes.append("")

    os.makedirs(os.path.dirname(args.trace) or ".", exist_ok=True)
    with open(args.trace, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    print(f"{args.trace} — {len(j['decisions'])} decisions, {traites} triees")


def main():
    p = argparse.ArgumentParser(description="Recovery Sprint — LOT-09")
    p.add_argument("--appliquer", action="store_true", help="lance la relecture (ecrit)")
    p.add_argument("--rapport", action="store_true", help="etat du tri et criteres du lot")
    p.add_argument("--trace", nargs="?", const=TRACE, default=None,
                   help="(re)genere le document d'archive")
    p.add_argument("--decision", action="append", help="restreindre a une decision")
    p.add_argument("--limite", type=int, help="ne traiter que les N plus anciennes")
    p.add_argument("--journal", default=JOURNAL)
    p.add_argument("--modele", default="sonnet")
    p.add_argument("--delai", type=int, default=420, help="secondes par relecture")
    p.add_argument("--echeance", default="", help="echeance des taches creees (AAAA-MM-JJ)")
    p.add_argument("--echeance-courte", default="", help="echeance des demandes de preuve")
    args = p.parse_args()
    # Les identifiants entrent dans des requetes construites par concatenation.
    # Ceux qui viennent de la base sont surs par construction ; celui-ci vient de
    # la ligne de commande, donc il se verifie avant d'y entrer.
    for d in args.decision or []:
        if not re.fullmatch(r"DEC-\d{4}-\d{4}-\d{2}", d):
            sys.exit(f"REFUS: identifiant mal forme : {d}")
    if not args.echeance:
        args.echeance = sql("SELECT (now() + interval '7 days')::date")[0][0]
    if not args.echeance_courte:
        args.echeance_courte = sql("SELECT (now() + interval '2 days')::date")[0][0]

    j = depart(args.journal)

    if args.trace is not None:
        return trace(j, args)
    if args.rapport:
        return rapport(j, args)

    ids = args.decision or sorted(j["decisions"],
                                  key=lambda d: -j["decisions"][d].get("age_depart_j", 0))
    # Une decision deja traitee n'est pas relue : le tri se reprend en plusieurs
    # passes sans repayer les precedentes, et sans risquer de revenir sur une
    # decision que le Chief of Staff a deja tranchee.
    if not args.decision:
        ids = [d for d in ids
               if (e := etat(d)) and e["statut"] == "accordee" and e["taches"] == 0]
    if args.limite:
        ids = ids[:args.limite]

    if args.appliquer:
        return appliquer(j, ids, args)
    return simuler(j, ids, args)


if __name__ == "__main__":
    main()
