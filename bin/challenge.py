#!/usr/bin/env python3
"""Challenge — les trois mécanismes qui empêchent le comité d'exécuter parfaitement
une stratégie moyenne, plus le Strategic Yield qui les mesure.

LOT-11 de la refonte DEOS Governance V2, 17/08/2026.

POURQUOI CE SCRIPT EXISTE
-------------------------
Une organisation qui n'a que la dimension « livrer » exécute parfaitement une
stratégie moyenne (SPEC §4bis). Le comité savait produire des rapports d'état ; il
n'avait aucun support pour la dimension CHALLENGE. Une hypothèse formulée en ronde
vivait dans le texte du compte rendu, c'est-à-dire nulle part : rien ne portait son
coût, rien ne disait ce qui prouverait qu'elle est fausse, et personne ne pouvait
dire six semaines plus tard si elle avait été testée.

CE QUE CE SCRIPT NE FAIT PAS
----------------------------
Il ne pose aucun jugement à la place de qui décide. Sam juge l'acceptation d'une
proposition (SPEC §8, tranché le 17/08) ; le CEO et Sam statuent sur un challenge.
L'outil applique des garde-fous de FORME — trois champs, une preuve, une
alternative — et rien d'autre. C'est délibéré : un mécanisme qui trierait le fond
deviendrait le juge, et un comité qui confirme ne sert à rien.

LE GARDE-FOU, EN UNE PHRASE
---------------------------
Un challenge qui ne produit pas une hypothèse TESTABLE n'est pas rendu. Sans
formulation réfutable c'est une opinion, sans coût c'est un vœu, sans critère de
réfutation on ne saura jamais si elle était fausse. Sans lui, sept directions
produiraient une hypothèse de FORME chaque semaine — le risque est réel, il porte
un nom, et c'est celui que la refonte vient de supprimer ailleurs.

    challenge.py activation                      l'état des interrupteurs
    challenge.py collecter                       les deux questions de la semaine
    challenge.py soumettre <direction> …         rendre un challenge (3 champs)
    challenge.py contredire <direction> …        contredire le CEO ou Sam
    challenge.py liste                           les challenges rendus
    challenge.py statuer <CHA-…> …               retenu ou écarté, par le CEO ou Sam
    challenge.py strategic                       Strategic Challenge mensuel
    challenge.py proposer --texte …              une proposition stratégique
    challenge.py boucle <PROP-…>                 la boucle d'intelligence collective
    challenge.py avis <PROP-…> <direction> …     un avis sur son axe propre
    challenge.py repondre <PROP-…> --par sam …   l'arbitrage de Sam
    challenge.py etape <PROP-…> --etape …        expérimentée, résultat, impact
    challenge.py yield [--audit]                 le Strategic Yield
    challenge.py --autotest                      vérifie les garde-fous hors base

Codes de retour : 0 OK (ou mécanisme inactif) · 2 REFUS · 3 ERREUR.

REFUS et ERREUR sont distincts, comme dans bin/policy.py. REFUS veut dire « ta
demande n'est pas recevable, voici ce qui manque » ; ERREUR veut dire « je n'ai pas
pu décider » — base injoignable, configuration illisible. Confondre les deux ferait
lire une panne comme un refus, et un agent corrigerait sa saisie pendant que la base
est à terre.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEMIN_ACTIVATION = os.path.join(RACINE, "config", "activation.yaml")
CHEMIN_PREFLIGHT = os.path.join(RACINE, "config", "preflight.yaml")

OK, REFUS, ERREUR = 0, 2, 3
DELAI_SQL = 15

ETATS = ("actif", "essai", "inactif")

# Les deux questions de l'obligation hebdomadaire, mot pour mot (SPEC §4bis).
QUESTIONS_HEBDO = (
    "Quelle hypothèse actuelle penses-tu fausse, fragile ou insuffisamment "
    "exploitée ?",
    "Quelle opportunité personne n'est actuellement en train de regarder ?",
)

# La règle qui prime sur le Strategic Challenge (SPEC §4bis). Elle est citée par
# l'outil à chaque fois qu'il ouvre le mécanisme : une règle qu'on ne relit jamais
# est une règle qu'on n'applique pas.
REGLE_CONTRADICTION = (
    "Une direction doit pouvoir contredire le CEO et Sam. Une contradiction "
    "s'accompagne de ses preuves et d'une alternative. Un comité qui confirme les "
    "intuitions du dirigeant ne sert à rien."
)

REGLE_COMMUNE = (
    "Aucun directeur n'est uniquement responsable de son département ; tous sont "
    "responsables de la réussite de Digital·Humans."
)


class Refus(Exception):
    """Demande non recevable. Le message dit ce qui manque, jamais seulement que
    quelque chose manque."""


class ErreurTechnique(Exception):
    """Impossible de décider : base, configuration, environnement."""


# ═════════════════════════════════════════════════════════════════════════════════
#  Lecture de l'interrupteur
# ═════════════════════════════════════════════════════════════════════════════════
#
# POURQUOI UN PARSEUR DE REPLI. Même motif qu'au LOT-05, et il est vérifié plutôt que
# supposé (`--autotest` compare les deux lectures quand PyYAML est présent) : le
# conteneur dh-comite n'a pas PyYAML garanti, et rebâtir l'image pour une dépendance
# de confort supposerait de redémarrer le comité — un effet de bord plus coûteux que
# le problème. Le sous-ensemble suffisant pour activation.yaml tient en trente
# lignes : scalaires, un niveau de blocs, listes.


def _sans_commentaire(ligne):
    """Retire un commentaire # hors chaîne quotée."""
    dehors, quote = [], None
    for c in ligne:
        if quote:
            dehors.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            dehors.append(c)
        elif c == "#":
            break
        else:
            dehors.append(c)
    return "".join(dehors).rstrip()


def _scalaire(brut):
    t = brut.strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'":
        return t[1:-1]
    if t == "[]":
        return []
    if t.lstrip("-").isdigit():
        return int(t)
    return t


def yaml_plat(texte):
    """Sous-ensemble YAML : scalaires de premier niveau, un niveau de blocs."""
    racine, bloc = {}, None
    for numero, brut in enumerate(texte.splitlines(), 1):
        ligne = _sans_commentaire(brut)
        if not ligne.strip():
            continue
        nu = ligne.strip()
        if ligne[0] not in " \t":
            if ":" not in nu:
                raise ErreurTechnique("activation.yaml ligne %d : « %s » n'est pas "
                                      "une clé" % (numero, nu))
            cle, _, valeur = nu.partition(":")
            cle = cle.strip()
            if valeur.strip() == "":
                racine[cle] = {}
                bloc = cle
            else:
                racine[cle] = _scalaire(valeur)
                bloc = None
            continue
        if bloc is None:
            raise ErreurTechnique("activation.yaml ligne %d : bloc sans clé "
                                  "parente" % numero)
        if nu.startswith("- "):
            if isinstance(racine[bloc], dict) and not racine[bloc]:
                racine[bloc] = []
            racine[bloc].append(_scalaire(nu[2:]))
        else:
            cle, _, valeur = nu.partition(":")
            racine[bloc][cle.strip()] = _scalaire(valeur)
    return racine


def charger_activation(chemin=CHEMIN_ACTIVATION):
    try:
        with open(chemin, encoding="utf-8") as fh:
            texte = fh.read()
    except OSError as e:
        raise ErreurTechnique("%s illisible : %s" % (chemin, e))
    try:
        import yaml
        conf = yaml.safe_load(texte)
    except ImportError:
        conf = yaml_plat(texte)
    if not isinstance(conf, dict):
        raise ErreurTechnique("%s : ce n'est pas un mapping" % chemin)
    return conf


def etat(conf, mecanisme):
    """État d'un mécanisme. FAIL-CLOSED : inconnu ou illisible vaut « inactif ».

    Une clé absente ou une valeur non reconnue ne doit jamais allumer un mécanisme.
    L'inverse — défaut « actif » — ferait tourner en production un dispositif qu'on
    croyait éteint, à cause d'une faute de frappe dans un fichier de configuration.
    """
    valeur = conf.get(mecanisme)
    if valeur in ETATS:
        return valeur
    return "inactif"


def charger_config_preflight():
    """Les directions et leur état, lus là où ils sont déjà déclarés (LOT-05).

    On ne redéclare PAS la liste des fonctions actives dans activation.yaml. Deux
    listes de directions divergent — c'est ce qui est arrivé au Financier, absent de
    la table des curseurs et de toutes les rondes alors que sa fiche existait
    (14/08). Une seule source, celle que le Preflight vérifie déjà.
    """
    try:
        with open(CHEMIN_PREFLIGHT, encoding="utf-8") as fh:
            texte = fh.read()
    except OSError as e:
        raise ErreurTechnique("%s illisible : %s" % (CHEMIN_PREFLIGHT, e))
    conf = None
    try:
        import yaml
        conf = yaml.safe_load(texte)
    except ImportError:
        # Parseur de repli de LOT-05, réutilisé plutôt que réécrit : preflight.yaml
        # est plus riche qu'activation.yaml, et deux parseurs du même fichier
        # divergeraient un jour sans que rien ne le signale.
        import importlib.util
        chemin = os.path.join(RACINE, "bin", "preflight.py")
        spec = importlib.util.spec_from_file_location("preflight_lot05", chemin)
        if spec is None or spec.loader is None:
            raise ErreurTechnique("bin/preflight.py introuvable : impossible de "
                                  "lire preflight.yaml sans PyYAML")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        conf = module.yaml_minimal(texte)
    if not isinstance(conf, dict) or "directions" not in conf:
        raise ErreurTechnique("%s : clé « directions » absente" % CHEMIN_PREFLIGHT)
    return conf


def directions_actives():
    conf = charger_config_preflight()
    return [nom for nom, spec in conf["directions"].items()
            if (spec or {}).get("etat") == "active"]


def directions_connues():
    return list(charger_config_preflight()["directions"].keys())


# ═════════════════════════════════════════════════════════════════════════════════
#  Accès à la base du comité
# ═════════════════════════════════════════════════════════════════════════════════

def litteral(valeur):
    """Rend une valeur Python sous forme de littéral SQL.

    Un seul point de mise en forme des valeurs : toute chaîne qui part en base passe
    ici. Le NUL est refusé plutôt que tronqué — PostgreSQL le rejetterait de toute
    façon, et le refus nommé se lit, l'erreur du pilote non.
    """
    if valeur is None:
        return "NULL"
    if isinstance(valeur, bool):
        return "true" if valeur else "false"
    texte = str(valeur)
    if "\x00" in texte:
        raise Refus("caractère NUL dans une valeur — saisie refusée")
    return "'" + texte.replace("'", "''") + "'"


def sql(requete):
    """Exécute une requête sur la base du comité. Rend une liste de listes.

    psql plutôt qu'un pilote Python : psycopg2 n'est pas installé dans le conteneur,
    et bin/deos-tasks, bin/deos-decisions et bin/preflight.py passent tous par psql.
    Un seul chemin d'accès à la base, donc un seul endroit à auditer.
    """
    dsn = os.environ.get("COMITE_DB_DSN", "")
    if not dsn:
        raise ErreurTechnique("COMITE_DB_DSN absente de l'environnement")
    try:
        r = subprocess.run(["psql", dsn, "-tA", "-F", "\x1f", "-v", "ON_ERROR_STOP=1",
                            "-c", requete],
                           capture_output=True, text=True, timeout=DELAI_SQL)
    except FileNotFoundError:
        raise ErreurTechnique("psql introuvable")
    except subprocess.TimeoutExpired:
        raise ErreurTechnique("base injoignable (pas de réponse en %d s)" % DELAI_SQL)
    if r.returncode != 0:
        lignes = [x for x in r.stderr.strip().splitlines() if x]
        raise ErreurTechnique(lignes[-1][:200] if lignes else "psql en échec")
    return [ligne.split("\x1f") for ligne in r.stdout.splitlines() if ligne]


def une_valeur(requete, defaut=None):
    lignes = sql(requete)
    return lignes[0][0] if lignes else defaut


def existe(table, identifiant):
    n = une_valeur("SELECT count(*) FROM %s WHERE id = %s;"
                   % (table, litteral(identifiant)), "0")
    if n != "1":
        raise Refus("%s inconnu dans %s" % (identifiant, table))


# ═════════════════════════════════════════════════════════════════════════════════
#  Le garde-fou — refus mécanique
# ═════════════════════════════════════════════════════════════════════════════════
#
# Il est ici ET en base (contrainte challenge_testable). Deux fois, parce que ce ne
# sont pas les mêmes lecteurs : la contrainte protège le fait, le message protège
# l'agent. Un message d'erreur PostgreSQL n'apprend rien à une direction qui vient
# de passer dix minutes sur son hypothèse — elle ne saura pas lequel des trois
# champs manque, ni pourquoi il est exigé.

CHAMPS_CHALLENGE = (
    ("hypothese", "--hypothese", "une formulation réfutable",
     "sans elle, c'est une opinion"),
    ("cout_experimentation", "--cout", "un coût d'expérimentation, en temps, en "
     "euros, ou les deux", "sans lui, c'est un vœu"),
    ("critere_refutation", "--refutation", "un critère de réfutation",
     "sans lui, on ne saura jamais si elle était fausse"),
)


def controler_challenge(valeurs):
    """Rend la liste des champs manquants. Fonction pure : testée par --autotest."""
    return [(option, exige, sans)
            for cle, option, exige, sans in CHAMPS_CHALLENGE
            if not (valeurs.get(cle) or "").strip()]


def exiger_challenge_complet(valeurs):
    manquants = controler_challenge(valeurs)
    if not manquants:
        return
    lignes = ["challenge refusé — un challenge qui ne produit pas une hypothèse "
              "TESTABLE n'est pas rendu.", "Il manque :"]
    for option, exige, sans in manquants:
        lignes.append("  %-14s %s — %s" % (option, exige, sans))
    lignes.append("Reformule et resoumets : le challenge est redemandé, pas perdu.")
    raise Refus("\n".join(lignes))


# ═════════════════════════════════════════════════════════════════════════════════
#  Mécanisme 1 — obligation de challenge hebdomadaire
# ═════════════════════════════════════════════════════════════════════════════════

def semaine_courante():
    return une_valeur("SELECT to_char(now(), 'IYYY-\"W\"IW');")


def cmd_collecter(a, conf):
    """Les deux questions, et qui doit encore répondre cette semaine.

    NE SANCTIONNE PAS, et sort toujours en 0. Une direction qui n'a pas rendu est
    nommée, pas punie : pendant l'essai, aucune sortie du mécanisme ne doit avoir de
    conséquence, sinon l'essai est déjà une activation.
    """
    regime = etat(conf, "challenge_hebdomadaire")
    if regime == "inactif":
        # Rien sur la sortie standard, rien en base, sortie 0. L'interrupteur coupe
        # le mécanisme ; il ne produit pas une erreur à traiter.
        return OK

    cibles = [a.direction] if a.direction else directions_actives()
    semaine = semaine_courante()
    rendus = {}
    for ligne in sql("SELECT direction, id FROM challenges "
                     "WHERE cycle = 'hebdomadaire' AND semaine = %s "
                     "ORDER BY soumis_le;" % litteral(semaine)):
        rendus.setdefault(ligne[0], []).append(ligne[1])

    etats = [{"direction": d,
              "rendu": bool(rendus.get(d)),
              "challenges": rendus.get(d, [])} for d in cibles]

    if a.json:
        print(json.dumps({"semaine": semaine, "regime": regime,
                          "questions": list(QUESTIONS_HEBDO),
                          "directions": etats}, ensure_ascii=False))
        return OK

    print("Challenge hebdomadaire — semaine %s · régime : %s" % (semaine, regime))
    if regime == "essai":
        print("(essai : les sorties du mécanisme ne comptent dans aucun indicateur)")
    print()
    for e in etats:
        marque = "rendu   " + ", ".join(e["challenges"]) if e["rendu"] else "ATTENDU"
        print("  %-18s %s" % (e["direction"], marque))
    print()
    for i, question in enumerate(QUESTIONS_HEBDO, 1):
        print("  %d. %s" % (i, question))
    print()
    print("  " + REGLE_COMMUNE)
    print()
    print("Un challenge n'est rendu que s'il porte les trois champs :")
    print("  bin/challenge.py soumettre <direction> --hypothese \"…\" "
          "--cout \"…\" --refutation \"…\"")
    return OK


def cmd_soumettre(a, conf):
    mecanisme = ("strategic_challenge" if a.cycle == "mensuel"
                 else "challenge_hebdomadaire")
    regime = etat(conf, mecanisme)
    if regime == "inactif":
        print("INACTIF: %s est inactif — rien n'a été enregistré." % mecanisme,
              file=sys.stderr)
        return OK

    valeurs = {"hypothese": a.hypothese or "",
               "cout_experimentation": a.cout or "",
               "critere_refutation": a.refutation or ""}
    exiger_challenge_complet(valeurs)

    if a.direction not in directions_connues():
        raise Refus("direction inconnue : %s — voir config/preflight.yaml"
                    % a.direction)

    # L'identifiant est calculé DANS l'insertion : deux directions qui soumettent en
    # même temps prendraient le même numéro si on comptait d'abord pour insérer
    # ensuite. Le défaut existe dans les outils antérieurs ; on ne le recopie pas.
    identifiant = une_valeur(
        "INSERT INTO challenges (id, direction, nature, cycle, hypothese, "
        "cout_experimentation, critere_refutation, opportunite, activation) "
        "SELECT 'CHA-' || to_char(now(),'YYYY-MMDD') || '-' || "
        "       lpad((count(*)+1)::text, 2, '0'), "
        "       %s, 'hypothese', %s, %s, %s, %s, %s, %s "
        "  FROM challenges "
        " WHERE id LIKE 'CHA-' || to_char(now(),'YYYY-MMDD') || '%%' "
        "RETURNING id;"
        % (litteral(a.direction), litteral(a.cycle), litteral(a.hypothese.strip()),
           litteral(a.cout.strip()), litteral(a.refutation.strip()),
           litteral((a.opportunite or "").strip() or None), litteral(regime)))
    print(identifiant)
    if regime == "essai":
        print("(essai : ce challenge ne compte dans aucun indicateur)",
              file=sys.stderr)
    return OK


def cmd_liste(a, conf):
    filtres = ["true"]
    if a.direction:
        filtres.append("direction = %s" % litteral(a.direction))
    if a.semaine:
        filtres.append("semaine = %s" % litteral(a.semaine))
    lignes = sql("SELECT id, direction, nature, cycle, statut, activation, semaine, "
                 "coalesce(hypothese, sujet) FROM challenges WHERE %s "
                 "ORDER BY soumis_le;" % " AND ".join(filtres))
    if a.json:
        print(json.dumps([{"id": l[0], "direction": l[1], "nature": l[2],
                           "cycle": l[3], "statut": l[4], "activation": l[5],
                           "semaine": l[6], "objet": l[7]} for l in lignes],
                         ensure_ascii=False))
        return OK
    if not lignes:
        print("aucun challenge")
        return OK
    for l in lignes:
        print("%-20s %-16s %-14s %-8s %-6s %s"
              % (l[0], l[1], l[2], l[4], l[5], l[7][:60]))
    return OK


def cmd_statuer(a, conf):
    """Retenir ou écarter un challenge. Jamais par la direction qui l'a rendu.

    Une hypothèse jugée par son auteur ne serait jamais écartée, et le stock des
    challenges non statués deviendrait ce qu'était le registre avant le tri du
    11/08 : un tas qui ne décroît pas et qu'on cesse de lire.
    """
    if a.par not in ("ceo", "sam"):
        raise Refus("seuls le ceo et sam statuent sur un challenge — %s l'a rendu, "
                    "il ne le juge pas (I3)" % a.par)
    existe("challenges", a.id)
    auteur = une_valeur("SELECT direction FROM challenges WHERE id = %s;"
                        % litteral(a.id))
    if auteur == a.par:
        raise Refus("%s a rendu ce challenge : il ne le juge pas" % a.par)
    if not (a.motif or "").strip():
        raise Refus("--motif est requis — « écarté » sans motif est un abandon "
                    "silencieux, pas un arbitrage")
    sql("UPDATE challenges SET statut = %s, motif = %s, statue_par = %s "
        "WHERE id = %s;" % (litteral(a.statut), litteral(a.motif.strip()),
                            litteral(a.par), litteral(a.id)))
    print("OK: %s → %s (par %s)" % (a.id, a.statut, a.par))
    return OK


# ═════════════════════════════════════════════════════════════════════════════════
#  Mécanisme 2 — Strategic Challenge mensuel, et la contradiction
# ═════════════════════════════════════════════════════════════════════════════════

def cmd_strategic(a, conf):
    """Les sept questions du CEO à chaque direction.

    LEUR CONTENU N'EST PAS SPÉCIFIÉ. SPEC §4bis et LOT-11 §2 donnent leur NOMBRE et
    la règle qui prime, jamais leur texte. SPEC §8 impose de signaler plutôt que
    d'inventer : la liste vit dans config/activation.yaml, elle est vide, et cette
    commande refuse de tourner tant qu'elle l'est. Sept questions inventées ici
    auraient pris force de spécification au premier usage.
    """
    regime = etat(conf, "strategic_challenge")
    if regime == "inactif":
        return OK

    questions = conf.get("questions_strategic_challenge") or []
    if not questions:
        raise Refus(
            "les sept questions du Strategic Challenge ne sont pas spécifiées.\n"
            "SPEC §4bis en donne le nombre et la règle qui prime, pas le contenu — "
            "point signalé,\nà trancher par Sam puis à écrire dans "
            "config/activation.yaml (questions_strategic_challenge).\n"
            "Ce qui EST spécifié et fonctionne dès maintenant : la contradiction "
            "argumentée,\n  bin/challenge.py contredire <direction> --cible ceo "
            "--sujet \"…\" --preuve \"…\" --alternative \"…\"")

    # Le CEO pose les questions : il n'est pas dans la liste de ceux qui répondent.
    cibles = [a.direction] if a.direction else [d for d in directions_actives()
                                                if d != "ceo"]
    print("Strategic Challenge mensuel — régime : %s" % regime)
    print()
    print("  " + REGLE_CONTRADICTION)
    print()
    for direction in cibles:
        print("  %s" % direction)
        for i, question in enumerate(questions, 1):
            print("    %d. %s" % (i, question))
        print()
    return OK


def cmd_contredire(a, conf):
    """Contredire le CEO ou Sam, avec ses preuves et une alternative.

    Le garde-fou est le même que celui de l'hypothèse, appliqué à l'autre forme du
    challenge : contester ne suffit pas, il faut apporter de quoi trancher. Une
    contradiction sans alternative arrête une direction sans rien mettre à la place.
    """
    manquants = []
    if a.cible not in ("ceo", "sam"):
        manquants.append(("--cible", "ceo ou sam", "on contredit quelqu'un"))
    if not (a.sujet or "").strip():
        manquants.append(("--sujet", "ce qui est contredit",
                          "sans lui, personne ne sait sur quoi porte le désaccord"))
    if not (a.preuve or "").strip():
        manquants.append(("--preuve", "de quoi étayer",
                          "sans elle, c'est une préférence"))
    if not (a.alternative or "").strip():
        manquants.append(("--alternative", "ce que tu proposes à la place",
                          "sans elle, on arrête sans rien mettre à la place"))
    if manquants:
        lignes = ["contradiction refusée — " + REGLE_CONTRADICTION, "Il manque :"]
        for option, exige, sans in manquants:
            lignes.append("  %-14s %s — %s" % (option, exige, sans))
        raise Refus("\n".join(lignes))

    regime = etat(conf, "strategic_challenge")
    # La contradiction reste possible quand le Strategic Challenge est inactif : ce
    # n'est pas une cérémonie mensuelle, c'est un droit permanent (SPEC §4bis). Ce
    # que l'interrupteur coupe, ce sont les sept questions, pas le droit de dire non.
    if regime == "inactif":
        regime = "essai"

    identifiant = une_valeur(
        "INSERT INTO challenges (id, direction, nature, cycle, cible, sujet, "
        "preuve, alternative, activation) "
        "SELECT 'CHA-' || to_char(now(),'YYYY-MMDD') || '-' || "
        "       lpad((count(*)+1)::text, 2, '0'), %s, 'contradiction', 'mensuel', "
        "       %s, %s, %s, %s, %s "
        "  FROM challenges "
        " WHERE id LIKE 'CHA-' || to_char(now(),'YYYY-MMDD') || '%%' "
        "RETURNING id;"
        % (litteral(a.direction), litteral(a.cible), litteral(a.sujet.strip()),
           litteral(a.preuve.strip()), litteral(a.alternative.strip()),
           litteral(regime)))
    print(identifiant)
    return OK


# ═════════════════════════════════════════════════════════════════════════════════
#  Mécanisme 3 — boucle d'intelligence collective
# ═════════════════════════════════════════════════════════════════════════════════

def axes(conf):
    valeur = conf.get("axes_boucle_collective")
    return valeur if isinstance(valeur, dict) else {}


def cmd_boucle(a, conf):
    """Une proposition, challengée par chaque direction sur son axe propre.

    La boucle NE DUPLIQUE PAS le cycle de vie d'une proposition : elle s'y branche.
    Synthèse → arbitrage de Sam (`repondre`) → exécution et mesure (`etape`). Une
    seconde table d'arbitrage aurait fabriqué deux vérités sur le même objet.
    """
    regime = etat(conf, "boucle_collective")
    if regime == "inactif":
        return OK
    existe("propositions", a.id)
    texte = une_valeur("SELECT texte FROM propositions WHERE id = %s;"
                       % litteral(a.id))
    rendus = {l[0]: l for l in sql(
        "SELECT direction, axe, verdict, preuve, coalesce(alternative,'') "
        "FROM avis WHERE proposition_id = %s ORDER BY donne_le;" % litteral(a.id))}

    actives = directions_actives()
    attribues = axes(conf)

    if a.synthese:
        print("Synthèse — %s : %s" % (a.id, texte))
        print()
        if not rendus:
            print("  aucun avis rendu")
        for direction, l in rendus.items():
            print("  %-18s %-24s %s" % (direction, l[1], l[2]))
            print("      preuve      : %s" % l[3])
            if l[4]:
                print("      alternative : %s" % l[4])
        manquants = [d for d in attribues if d in actives and d not in rendus]
        if manquants:
            print()
            print("  attendus : %s" % ", ".join(manquants))
        print()
        print("  Arbitrage : bin/challenge.py repondre %s --par sam "
              "--reponse acceptee|refusee" % a.id)
        return OK

    print("Boucle d'intelligence collective — %s · régime : %s" % (a.id, regime))
    print("  %s" % texte)
    print()
    for direction, axe in attribues.items():
        if direction not in actives:
            # Une fonction en veille garde son axe (I2) ; elle n'est pas sollicitée
            # tant que sa cadence est arrêtée, et la boucle le dit plutôt que de
            # faire disparaître l'axe en silence.
            print("  %-18s %-24s (en veille — non sollicitée)" % (direction, axe))
            continue
        if direction in rendus:
            print("  %-18s %-24s %s" % (direction, axe, rendus[direction][2]))
        else:
            print("  %-18s %-24s ATTENDU" % (direction, axe))
    print()
    print("  Chaque direction répond SUR SON AXE, avec sa preuve. Un avis "
          "défavorable\n  exige une alternative : arrêter sans rien mettre à la "
          "place est un blocage\n  sans suite (I4).")
    print("  bin/challenge.py avis %s <direction> --verdict favorable|reserve|"
          "defavorable \\\n      --preuve \"…\" [--alternative \"…\"]" % a.id)
    return OK


def cmd_avis(a, conf):
    regime = etat(conf, "boucle_collective")
    if regime == "inactif":
        print("INACTIF: boucle_collective est inactive — rien n'a été enregistré.",
              file=sys.stderr)
        return OK
    existe("propositions", a.id)
    if a.verdict == "defavorable" and not (a.alternative or "").strip():
        raise Refus("avis défavorable refusé — un avis défavorable exige "
                    "--alternative.\nArrêter une proposition sans rien mettre à la "
                    "place est la version collective\ndu blocage sans suite (I4).")
    if not (a.preuve or "").strip():
        raise Refus("--preuve est requise — un avis sans preuve est une préférence")
    axe = axes(conf).get(a.direction)
    if not axe:
        raise Refus("aucun axe déclaré pour %s dans config/activation.yaml "
                    "(axes_boucle_collective) — la boucle challenge sur un axe "
                    "propre, pas en général" % a.direction)
    sql("INSERT INTO avis (proposition_id, direction, axe, verdict, preuve, "
        "alternative, activation) VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (proposition_id, direction) DO UPDATE SET "
        "axe = excluded.axe, verdict = excluded.verdict, preuve = excluded.preuve, "
        "alternative = excluded.alternative, donne_le = now();"
        % (litteral(a.id), litteral(a.direction), litteral(axe),
           litteral(a.verdict), litteral(a.preuve.strip()),
           litteral((a.alternative or "").strip() or None), litteral(regime)))
    print("OK: avis de %s sur %s (%s) — %s" % (a.direction, a.id, axe, a.verdict))
    return OK


# ═════════════════════════════════════════════════════════════════════════════════
#  Strategic Yield — les quatre étapes, le rappel, la veille
# ═════════════════════════════════════════════════════════════════════════════════
#
# LE STRATEGIC YIELD N'A PAS D'INTERRUPTEUR, et c'est délibéré : une proposition
# stratégique relève du mandat du CEO (SPEC §4bis), pas d'un mécanisme optionnel.
# Ce que l'interrupteur gouverne, c'est la BOUCLE qui la challenge.

ETAPES_ACCEPTEES = ("acceptee", "experimentee", "resultat", "impact")
ETAPES_JUGEES = ("acceptee", "refusee", "experimentee", "resultat", "impact")


def cmd_proposer(a, conf):
    if a.par != "ceo" and a.par not in directions_connues():
        raise Refus("origine inconnue : %s" % a.par)
    if not (a.texte or "").strip():
        raise Refus("--texte est requis")
    identifiant = une_valeur(
        "INSERT INTO propositions (id, origine, texte, hors_backlog) "
        "SELECT 'PROP-' || to_char(now(),'YYYY-MMDD') || '-' || "
        "       lpad((count(*)+1)::text, 2, '0'), %s, %s, %s "
        "  FROM propositions "
        " WHERE id LIKE 'PROP-' || to_char(now(),'YYYY-MMDD') || '%%' "
        "RETURNING id;"
        % (litteral(a.par), litteral(a.texte.strip()), litteral(bool(a.hors_backlog))))
    print(identifiant)
    if a.hors_backlog:
        print("(hors backlog : droit de PROPOSITION, pas d'initiative — Sam valide)",
              file=sys.stderr)
    return OK


def cmd_repondre(a, conf):
    """L'arbitrage de Sam. Lui seul, y compris quand le CEO est pressé.

    Une proposition EN VEILLE est reprenable : répondre la fait ressortir de la
    veille et la remet dans le calcul. La veille n'est pas un cimetière, c'est une
    file d'attente sans échéance.
    """
    if a.par != "sam":
        raise Refus("seul sam juge de l'acceptation d'une proposition (arbitrage du "
                    "17/08).\nLe Strategic Yield mesure le CEO : s'il pouvait "
                    "écrire l'acceptation, l'indicateur\nmesurerait la déclaration, "
                    "pas le fait (I3).")
    existe("propositions", a.id)
    statut = une_valeur("SELECT statut FROM propositions WHERE id = %s;"
                        % litteral(a.id))
    if statut not in ("soumise", "en_veille"):
        raise Refus("%s est en « %s » — la réponse de Sam se pose sur une "
                    "proposition soumise ou en veille" % (a.id, statut))
    sql("UPDATE propositions SET statut = %s, repondue_le = now(), "
        "repondue_par = 'sam', motif = %s WHERE id = %s;"
        % (litteral(a.reponse), litteral((a.motif or "").strip() or None),
           litteral(a.id)))
    print("OK: %s → %s (par sam)" % (a.id, a.reponse))
    if statut == "en_veille":
        print("    sortie de veille : elle revient dans le calcul du Strategic Yield")
    return OK


def cmd_etape(a, conf):
    """Expérimentée → résultat → impact. Chaque étape porte sa preuve.

    L'ORDRE EST IMPOSÉ. Une proposition ne peut pas avoir un impact sans résultat ni
    un résultat sans expérimentation : le Strategic Yield mesure des TAUX DE PASSAGE,
    et un passage sauté fabriquerait un taux supérieur à 1 sur l'étape suivante.
    """
    existe("propositions", a.id)
    statut = une_valeur("SELECT statut FROM propositions WHERE id = %s;"
                        % litteral(a.id))
    precedent = {"experimentee": "acceptee", "resultat": "experimentee",
                 "impact": "resultat"}[a.etape]
    if statut != precedent:
        raise Refus("%s est en « %s » — l'étape « %s » suit « %s »"
                    % (a.id, statut, a.etape, precedent))
    if a.par not in ("ceo", "cos", "chief-of-staff", "sam"):
        raise Refus("l'étape est enregistrée par le ceo, le chief-of-staff ou sam")

    champs = ["statut = %s" % litteral(a.etape),
              "etape_par = %s" % litteral(a.par)]
    if a.etape == "experimentee":
        if not a.evidence_type or not (a.evidence_ref or "").strip():
            raise Refus("--evidence-type et --evidence-ref sont requis.\n"
                        "Sans preuve, « expérimentée » est une affirmation de la "
                        "partie évaluée (I3).")
        champs.append("experimentee_le = now()")
        champs.append("evidence_type = %s" % litteral(a.evidence_type))
        champs.append("evidence_ref = %s" % litteral(a.evidence_ref.strip()))
    elif a.etape == "resultat":
        if not (a.texte or "").strip():
            raise Refus("--texte est requis : le résultat constaté, en une phrase")
        champs.append("resultat = %s" % litteral(a.texte.strip()))
        if a.evidence_type and (a.evidence_ref or "").strip():
            champs.append("evidence_type = %s" % litteral(a.evidence_type))
            champs.append("evidence_ref = %s" % litteral(a.evidence_ref.strip()))
    else:
        if not (a.texte or "").strip():
            raise Refus("--texte est requis : l'impact constaté, en une phrase")
        champs.append("impact = %s" % litteral(a.texte.strip()))

    sql("UPDATE propositions SET %s WHERE id = %s;"
        % (", ".join(champs), litteral(a.id)))
    print("OK: %s → %s" % (a.id, a.etape))
    return OK


def taux(numerateur, denominateur):
    """Rend None quand le dénominateur est nul. NULL N'EST PAS 0.

    Piège documenté le 10/08 sur les gabarits de graphiques : une valeur absente ne
    se dessine pas comme un zéro. Un taux d'impact affiché « 0 % » alors qu'aucune
    proposition n'a encore de résultat se lit comme un échec du CEO ; c'est une
    étape que personne n'a atteinte.
    """
    if not denominateur:
        return None
    return round(100.0 * numerateur / denominateur, 1)


def strategic_yield():
    comptes = {l[0]: int(l[1]) for l in
               sql("SELECT statut, count(*) FROM propositions GROUP BY statut;")}
    en_veille = comptes.get("en_veille", 0)
    total = sum(comptes.values())
    jugees = sum(comptes.get(s, 0) for s in ETAPES_JUGEES)
    acceptees = sum(comptes.get(s, 0) for s in ETAPES_ACCEPTEES)
    experimentees = sum(comptes.get(s, 0) for s in ("experimentee", "resultat",
                                                    "impact"))
    avec_resultat = sum(comptes.get(s, 0) for s in ("resultat", "impact"))
    avec_impact = comptes.get("impact", 0)
    return {
        "propositions": total,
        "en_veille_hors_calcul": en_veille,
        "dans_le_calcul": total - en_veille,
        "sans_reponse": comptes.get("soumise", 0),
        "jugees": jugees,
        "acceptees": acceptees,
        "experimentees": experimentees,
        "avec_resultat": avec_resultat,
        "avec_impact": avec_impact,
        "taux_acceptation": taux(acceptees, jugees),
        "taux_experimentation": taux(experimentees, acceptees),
        "taux_resultat": taux(avec_resultat, experimentees),
        "taux_impact": taux(avec_impact, avec_resultat),
        "note": "Le CEO n'est pas mesuré au volume de propositions. Les "
                "propositions en veille sont hors calcul : ni bonus, ni malus.",
    }


def auditer_delais(conf, simuler):
    """Le rappel unique, puis la veille. Idempotent : rejouable sans effet.

    « Une proposition sans réponse n'est pas un refus. » Sans cette passe,
    l'indicateur mesurerait la disponibilité de Sam plutôt que la qualité des
    propositions — et le CEO serait pénalisé pour un silence qui n'est pas le sien.
    """
    delai_rappel = int(conf.get("delai_rappel_jours") or 14)
    delai_veille = int(conf.get("delai_veille_jours") or 7)
    lignes = sql(
        "SELECT id, "
        "       floor(extract(epoch from now() - soumise_le) / 86400)::int, "
        "       coalesce(floor(extract(epoch from now() - rappele_le) / 86400)::int, "
        "                -1), "
        "       (rappele_le IS NOT NULL)::int "
        "  FROM propositions WHERE statut = 'soumise' ORDER BY soumise_le;")
    actions = []
    for identifiant, age, depuis_rappel, rappelee in lignes:
        age, depuis_rappel, rappelee = int(age), int(depuis_rappel), int(rappelee)
        if not rappelee and age >= delai_rappel:
            actions.append({"id": identifiant, "action": "rappel", "jours": age,
                            "detail": "sans réponse depuis %d jours — le CEO "
                                      "rappelle UNE FOIS" % age})
            if not simuler:
                sql("UPDATE propositions SET rappele_le = now() WHERE id = %s;"
                    % litteral(identifiant))
        elif rappelee and depuis_rappel >= delai_veille:
            actions.append({"id": identifiant, "action": "veille",
                            "jours": depuis_rappel,
                            "detail": "rappelée il y a %d jours, toujours sans "
                                      "réponse — mise en veille : ni perdue, ni "
                                      "comptée comme refusée"
                                      % depuis_rappel})
            if not simuler:
                sql("UPDATE propositions SET statut = 'en_veille' WHERE id = %s;"
                    % litteral(identifiant))
    return actions


def cmd_yield(a, conf):
    actions = auditer_delais(conf, a.simuler) if a.audit else []
    resultat = strategic_yield()
    if a.json:
        print(json.dumps({"strategic_yield": resultat, "audit": actions},
                         ensure_ascii=False))
        return OK

    if a.audit:
        print("Audit des délais — %d j sans réponse → rappel unique · +%d j → veille"
              % (int(conf.get("delai_rappel_jours") or 14),
                 int(conf.get("delai_veille_jours") or 7)))
        if a.simuler:
            print("(simulation : rien n'est écrit)")
        if not actions:
            print("  rien à rappeler, rien à mettre en veille")
        for action in actions:
            print("  %-7s %-22s %s" % (action["action"].upper(), action["id"],
                                       action["detail"]))
        print()

    def pourcent(valeur):
        return "—" if valeur is None else "%.0f %%" % valeur

    print("Strategic Yield — %s" % datetime.now().strftime("%d/%m/%Y"))
    print()
    print("  propositions              %d" % resultat["propositions"])
    print("  dans le calcul            %d   (%d en veille, hors calcul)"
          % (resultat["dans_le_calcul"], resultat["en_veille_hors_calcul"]))
    print("  sans réponse              %d" % resultat["sans_reponse"])
    print()
    print("  acceptées      %3d / %-3d  %s"
          % (resultat["acceptees"], resultat["jugees"],
             pourcent(resultat["taux_acceptation"])))
    print("  expérimentées  %3d / %-3d  %s"
          % (resultat["experimentees"], resultat["acceptees"],
             pourcent(resultat["taux_experimentation"])))
    print("  avec résultat  %3d / %-3d  %s"
          % (resultat["avec_resultat"], resultat["experimentees"],
             pourcent(resultat["taux_resultat"])))
    print("  avec impact    %3d / %-3d  %s"
          % (resultat["avec_impact"], resultat["avec_resultat"],
             pourcent(resultat["taux_impact"])))
    print()
    print("  Le CEO n'est pas mesuré au volume de propositions : ce sont les taux")
    print("  de passage d'une étape à la suivante qui font le Strategic Yield.")
    print("  « — » signale un dénominateur nul : personne n'a atteint l'étape.")
    print("  Ce n'est pas 0 %.")
    return OK


# ═════════════════════════════════════════════════════════════════════════════════
#  État des interrupteurs, et autotest
# ═════════════════════════════════════════════════════════════════════════════════

MECANISMES = ("challenge_hebdomadaire", "strategic_challenge", "boucle_collective",
              "innovation_budget")


def cmd_activation(a, conf):
    if a.json:
        print(json.dumps({m: etat(conf, m) for m in MECANISMES}, ensure_ascii=False))
        return OK
    print("Interrupteurs — config/activation.yaml")
    print()
    for mecanisme in MECANISMES:
        valeur = conf.get(mecanisme)
        marque = "" if valeur in ETATS else "   (valeur illisible → inactif)"
        print("  %-24s %s%s" % (mecanisme, etat(conf, mecanisme), marque))
    print("  %-24s %s %%" % ("budget_innovation_pct",
                             conf.get("budget_innovation_pct")))
    print()
    print("  actif    ses sorties comptent dans les indicateurs")
    print("  essai    le mécanisme tourne, ses sorties ne comptent nulle part")
    print("  inactif  le mécanisme ne tourne pas — sortie 0, rien n'est écrit")
    return OK


def cmd_autotest(a, conf):
    """Vérifie ce qui se vérifie SANS base : parseur, fail-closed, garde-fous."""
    echecs = []

    def verifier(intitule, condition):
        print("  %s %s" % ("✓" if condition else "✗", intitule))
        if not condition:
            echecs.append(intitule)

    print("Parseur de repli")
    with open(a.config, encoding="utf-8") as fh:
        texte = fh.read()
    interne = yaml_plat(texte)
    try:
        import yaml
        verifier("le parseur de repli lit activation.yaml comme PyYAML",
                 interne == yaml.safe_load(texte))
    except ImportError:
        verifier("PyYAML absent — comparaison impossible, parseur de repli seul",
                 isinstance(interne, dict))

    print("Lecture fail-closed de l'interrupteur")
    verifier("une clé absente vaut inactif", etat({}, "boucle_collective") == "inactif")
    verifier("une valeur illisible vaut inactif",
             etat({"boucle_collective": "oui"}, "boucle_collective") == "inactif")
    verifier("essai est lu tel quel",
             etat({"boucle_collective": "essai"}, "boucle_collective") == "essai")

    print("Garde-fou du challenge — refus mécanique")
    complet = {"hypothese": "h", "cout_experimentation": "2 j",
               "critere_refutation": "si X alors fausse"}
    verifier("un challenge complet passe", controler_challenge(complet) == [])
    for cle, option, _, _ in CHAMPS_CHALLENGE:
        partiel = dict(complet)
        partiel[cle] = ""
        manquants = [m[0] for m in controler_challenge(partiel)]
        verifier("sans %s, le challenge est refusé" % option, manquants == [option])
    espaces = dict(complet, critere_refutation="   ")
    verifier("un champ rempli d'espaces ne satisfait pas le garde-fou",
             [m[0] for m in controler_challenge(espaces)] == ["--refutation"])

    print("Taux — un dénominateur nul n'est pas zéro")
    verifier("0 sur 0 rend None, pas 0", taux(0, 0) is None)
    verifier("1 sur 2 rend 50,0", taux(1, 2) == 50.0)

    print()
    if echecs:
        print("autotest : %d échec(s)" % len(echecs))
        return REFUS
    print("autotest : tout passe")
    return OK


# ═════════════════════════════════════════════════════════════════════════════════
#  Ligne de commande
# ═════════════════════════════════════════════════════════════════════════════════

def construire_analyseur():
    ap = argparse.ArgumentParser(
        prog="challenge.py",
        description="Mécanismes de challenge et Strategic Yield (LOT-11).")
    ap.add_argument("--autotest", action="store_true",
                    help="vérifie les garde-fous sans toucher la base")
    # Même raison que --capacites dans bin/policy.py : la suite de tests doit pouvoir
    # rejouer l'interrupteur sans modifier le fichier réel du comité. Un test qui
    # écrit dans config/activation.yaml laisse le dispositif dans l'état du dernier
    # cas exécuté si la suite s'interrompt — c'est-à-dire un mécanisme éteint sans
    # que personne ne l'ait décidé.
    ap.add_argument("--config", default=CHEMIN_ACTIVATION,
                    help="interrupteur à lire (défaut : config/activation.yaml)")
    sous = ap.add_subparsers(dest="commande")

    p = sous.add_parser("activation", help="état des interrupteurs")
    p.add_argument("--json", action="store_true")

    p = sous.add_parser("collecter", help="les deux questions de la semaine")
    p.add_argument("--direction")
    p.add_argument("--json", action="store_true")

    p = sous.add_parser("soumettre", help="rendre un challenge")
    p.add_argument("direction")
    p.add_argument("--hypothese", default="")
    p.add_argument("--cout", default="")
    p.add_argument("--refutation", default="")
    p.add_argument("--opportunite", default="")
    p.add_argument("--cycle", choices=("hebdomadaire", "mensuel"),
                   default="hebdomadaire")

    p = sous.add_parser("contredire", help="contredire le CEO ou Sam")
    p.add_argument("direction")
    p.add_argument("--cible", default="")
    p.add_argument("--sujet", default="")
    p.add_argument("--preuve", default="")
    p.add_argument("--alternative", default="")

    p = sous.add_parser("liste", help="les challenges rendus")
    p.add_argument("--direction")
    p.add_argument("--semaine")
    p.add_argument("--json", action="store_true")

    p = sous.add_parser("statuer", help="retenir ou écarter un challenge")
    p.add_argument("id")
    p.add_argument("--statut", choices=("retenu", "ecarte"), required=True)
    p.add_argument("--par", required=True)
    p.add_argument("--motif", default="")

    p = sous.add_parser("strategic", help="Strategic Challenge mensuel")
    p.add_argument("--direction")

    p = sous.add_parser("proposer", help="une proposition stratégique")
    p.add_argument("--texte", default="")
    p.add_argument("--par", default="ceo")
    p.add_argument("--hors-backlog", action="store_true", dest="hors_backlog")

    p = sous.add_parser("boucle", help="boucle d'intelligence collective")
    p.add_argument("id")
    p.add_argument("--synthese", action="store_true")

    p = sous.add_parser("avis", help="avis d'une direction sur son axe")
    p.add_argument("id")
    p.add_argument("direction")
    p.add_argument("--verdict", choices=("favorable", "reserve", "defavorable"),
                   required=True)
    p.add_argument("--preuve", default="")
    p.add_argument("--alternative", default="")

    p = sous.add_parser("repondre", help="l'arbitrage de Sam")
    p.add_argument("id")
    p.add_argument("--par", required=True)
    p.add_argument("--reponse", choices=("acceptee", "refusee"), required=True)
    p.add_argument("--motif", default="")

    p = sous.add_parser("etape", help="expérimentée, résultat, impact")
    p.add_argument("id")
    p.add_argument("--etape", choices=("experimentee", "resultat", "impact"),
                   required=True)
    p.add_argument("--par", default="ceo")
    p.add_argument("--texte", default="")
    p.add_argument("--evidence-type", dest="evidence_type",
                   choices=("commit", "fichier", "base", "url"))
    p.add_argument("--evidence-ref", dest="evidence_ref", default="")

    p = sous.add_parser("yield", help="le Strategic Yield")
    p.add_argument("--audit", action="store_true",
                   help="passe les délais : rappel unique, puis veille")
    p.add_argument("--simuler", action="store_true",
                   help="avec --audit : montre sans écrire")
    p.add_argument("--json", action="store_true")

    return ap


COMMANDES = {
    "activation": cmd_activation,
    "collecter": cmd_collecter,
    "soumettre": cmd_soumettre,
    "contredire": cmd_contredire,
    "liste": cmd_liste,
    "statuer": cmd_statuer,
    "strategic": cmd_strategic,
    "proposer": cmd_proposer,
    "boucle": cmd_boucle,
    "avis": cmd_avis,
    "repondre": cmd_repondre,
    "etape": cmd_etape,
    "yield": cmd_yield,
}


def main(argv=None):
    ap = construire_analyseur()
    a = ap.parse_args(argv)
    try:
        conf = charger_activation(a.config)
        if a.autotest:
            return cmd_autotest(a, conf)
        if not a.commande:
            ap.print_help()
            return OK
        return COMMANDES[a.commande](a, conf)
    except Refus as e:
        print("REFUS: %s" % e, file=sys.stderr)
        return REFUS
    except ErreurTechnique as e:
        # ERREUR, pas REFUS : la demande était peut-être recevable, on n'a pas pu
        # trancher. Voir l'en-tête du fichier.
        print("ERREUR: %s" % e, file=sys.stderr)
        return ERREUR
    except BrokenPipeError:
        # `challenge.py yield | head` ou `| grep -q` ferme le tuyau avant la fin de
        # l'écriture. Sans ce rattrapage, Python imprime une trace et sort en 1 :
        # une commande parfaitement correcte passe alors pour un échec. Relevé en
        # validation le 17/08 — la suite d'acceptation rendait un faux négatif sur
        # le rappel du Strategic Yield, dont la seule faute était d'être lu par
        # grep. On referme stderr pour que l'interpréteur ne rejoue pas l'erreur.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stderr.fileno())
        return OK


if __name__ == "__main__":
    sys.exit(main())
