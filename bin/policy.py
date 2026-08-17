#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Policy Engine minimal — contrôle par CAPACITÉ, pas par motif textuel.

LOT-06 de la refonte DEOS Governance V2, 17/08/2026.

CE QUE ÇA REMPLACE
------------------
Le garde-fou demandait « la commande contient-elle UPDATE ? ». Deux
conséquences, dans les deux sens :

  · FAUX NÉGATIF — les deux outils par lesquels le comité écrit réellement,
    deos-decisions et deos-state, ne contiennent aucun motif SQL. Le curseur
    ecrire_base n'était donc appliqué nulle part. Il existait sur le papier.

  · FAUX POSITIF — chercher « curl … -d » n'importe où dans la commande refuse
    un DOCUMENT qui cite une ligne de journal. Le 11/08 le Marketing en a été
    victime ; le Commercial a reproduit le refus en direct en essayant de le
    documenter. Cinq faux positifs dans quatre directions le 17/08.

La cause est la même dans les deux cas : on cherchait des MOTS dans une chaîne,
là où il fallait identifier une COMMANDE INVOQUÉE. Ce moteur découpe la ligne en
commandes simples, retire les corps de heredoc, et ne regarde que le programme
réellement en position d'exécution.

CONTRAT (LOT-06 §Contrat)
-------------------------
Entrée, sur stdin : {"agent": "...", "outil": "...", "arguments": {...}}
Sortie, sur stdout : un verdict JSON.
Codes de retour :   0 ALLOW · 2 DENY · 3 ERREUR · 4 NON APPLICABLE

ERREUR et NON APPLICABLE sont distincts à dessein. NON APPLICABLE veut dire
« ce n'est pas à moi de trancher, reprends tes règles d'avant » ; ERREUR veut
dire « je n'ai pas pu décider », et le crochet doit alors refuser. Un moteur de
sécurité qui laisse passer quand il tombe en panne ne protège rien.

CE QUE CE MOTEUR NE FAIT PAS
----------------------------
Il ne lit aucun niveau de curseur en base : il reçoit le cache déjà chargé par
le crochet (même fichier, même logique de fraîcheur qu'avant ce lot). Le bash
garde la base, le python garde la décision. Un seul chemin d'accès aux curseurs,
donc un seul endroit à auditer.
"""

import argparse
import json
import os
import re
import shlex
import sys

NOMS_NIVEAUX = {
    1: "Observe",
    2: "Conseille",
    3: "Agit sous validation",
    4: "Autonomie",
}

# Défaut restrictif, repris à l'identique du garde-fou : une direction sans
# curseur déclaré ne doit rien pouvoir faire, plutôt que tout.
NIVEAU_DEFAUT = 1

ALLOW, DENY, ERREUR, NON_APPLICABLE = 0, 2, 3, 4


# ─────────────────────────────────────────────────────────────────────────────
# Découpage de la ligne de commande
#
# Tout le moteur repose là-dessus. Une règle appliquée à la bonne sous-chaîne
# vaut mieux qu'une règle savante appliquée à la ligne entière.
# ─────────────────────────────────────────────────────────────────────────────

# Un heredoc n'est pas du code : c'est de la donnée que l'on écrit dans un
# fichier. C'est la citation d'un `curl -d` DANS un heredoc qui a fait refuser
# le support visuel du Marketing le 11/08, puis l'addendum du Commercial qui
# l'expliquait. On retire donc les corps avant toute analyse.
_HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")


def retirer_heredocs(commande):
    """Retire le CORPS des heredocs, garde la ligne qui les ouvre.

    La ligne d'ouverture reste analysable (`cat <<EOF > cible` doit continuer
    d'être vue comme une écriture vers `cible`) ; seul le texte livré disparaît.
    """
    lignes = commande.split("\n")
    sortie = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        sortie.append(ligne)
        marques = [m.group(2) for m in _HEREDOC.finditer(ligne)]
        i += 1
        for delimiteur in marques:
            while i < len(lignes) and lignes[i].strip() != delimiteur:
                i += 1
            if i < len(lignes):  # on saute aussi la ligne du délimiteur
                i += 1
    return "\n".join(sortie)


# Séparateurs qui ouvrent une nouvelle position de commande. `>` et `<` n'y sont
# pas : une redirection ne lance pas de programme.
_SEPARATEURS = re.compile(r"(?:\|\||&&|[;&|\n()]|\$\()")


def commandes_simples(commande):
    """Découpe une ligne shell en commandes simples.

    Approximation assumée : on ne réimplémente pas bash. Elle suffit parce
    qu'elle ne sert qu'à répondre à « quel programme est invoqué ici ». Un
    séparateur à l'intérieur d'une chaîne entre guillemets peut produire un
    fragment de trop — au pire on analyse un fragment qui n'invoque rien, ce qui
    ne déclenche aucune capacité.
    """
    sans_heredoc = retirer_heredocs(commande)
    return [f.strip() for f in _SEPARATEURS.split(sans_heredoc) if f and f.strip()]


# Un fragment peut commencer par des affectations d'environnement
# (`DH_DIRECTION=x outil …`) : elles ne sont pas le programme.
_AFFECTATION = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def decouper_fragment(fragment):
    """Rend (programme, arguments) pour une commande simple, ou (None, []).

    Le programme est rendu SANS son chemin : `bin/deos-decisions`,
    `./deos-decisions` et `deos-decisions` sont le même outil. C'est exactement
    ce que le contrôle textuel ne savait pas faire.
    """
    try:
        jetons = shlex.split(fragment, comments=False)
    except ValueError:
        # Guillemet non refermé — fréquent quand on a coupé au milieu d'une
        # chaîne. On retombe sur un découpage grossier plutôt que d'abandonner :
        # renoncer à analyser serait laisser passer.
        jetons = fragment.split()
    while jetons and (_AFFECTATION.match(jetons[0]) or jetons[0] in ("sudo", "command", "env", "nohup", "time", "exec")):
        jetons = jetons[1:]
    if not jetons:
        return None, []
    return os.path.basename(jetons[0]), jetons[1:]


# ─────────────────────────────────────────────────────────────────────────────
# Analyseurs — nommés dans le YAML, implémentés ici
#
# La correspondance outil → capacité reste déclarative (ajouter un outil =
# ajouter une ligne `programme:`). Un analyseur ne sert qu'à distinguer, POUR UN
# MÊME PROGRAMME, l'usage qui écrit de l'usage qui lit. Sans eux il faudrait
# choisir entre refuser tous les SELECT et laisser passer tous les UPDATE.
# ─────────────────────────────────────────────────────────────────────────────

_MOTS_LECTURE = ("select", "with", "explain", "show", "table", "values")
_MOTS_ECRITURE = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|grant|revoke|copy|"
    r"comment|reindex|vacuum|refresh|call|do)\b",
    re.IGNORECASE,
)


def analyseur_psql_ecriture(programme, arguments, contexte):
    """psql écrit-il ? Rendre False laisse passer la lecture.

    Règle : on ne classe en LECTURE que ce qu'on a pu lire et reconnaître comme
    tel. Tout le reste — `-f fichier.sql`, session interactive, requête qu'on
    n'arrive pas à extraire — est traité comme une écriture. Se tromper vers la
    lecture ouvrirait la base ; se tromper vers l'écriture coûte un refus
    motivé, que la direction rapporte.
    """
    requete = None
    lecture_seule_declaree = False
    i = 0
    while i < len(arguments):
        a = arguments[i]
        if a in ("-c", "--command"):
            requete = arguments[i + 1] if i + 1 < len(arguments) else ""
            i += 2
            continue
        if a.startswith("--command="):
            requete = a.split("=", 1)[1]
            i += 1
            continue
        if a in ("-l", "--list", "-V", "--version", "--help", "-?"):
            lecture_seule_declaree = True
        if a in ("-f", "--file") or a.startswith("--file="):
            return True, "requête lue dans un fichier, contenu non vérifiable"
        i += 1

    if requete is None:
        if lecture_seule_declaree:
            return False, None
        return True, "aucune requête explicite : session interactive ou script"

    nue = requete.strip().lstrip("(").lstrip()
    premier = nue.split()[0].lower() if nue.split() else ""
    if premier.startswith("\\"):  # méta-commandes psql : \d, \dt, \l…
        return False, None
    if premier in _MOTS_LECTURE and not _MOTS_ECRITURE.search(requete):
        return False, None
    return True, "requête modifiant la base"


# Ce qui EXPÉDIE quelque chose. Un GET va chercher, il n'envoie pas : le
# distinguer évite de refuser une consultation de documentation.
_OPTIONS_ENVOI = {
    "-d", "--data", "--data-raw", "--data-binary", "--data-urlencode",
    "--data-ascii", "-F", "--form", "--form-string", "-T", "--upload-file",
    "--post-data", "--post-file", "--body-data", "--body-file", "--method",
    "-X", "--request", "--mail-from", "--mail-rcpt",
}
_METHODES_ENVOI = {"POST", "PUT", "PATCH", "DELETE"}


def analyseur_envoi_http(programme, arguments, contexte):
    """curl/wget expédient-ils des données ?"""
    for i, a in enumerate(arguments):
        cle = a.split("=", 1)[0]
        if cle in _OPTIONS_ENVOI:
            if cle in ("-X", "--request", "--method"):
                valeur = a.split("=", 1)[1] if "=" in a else (arguments[i + 1] if i + 1 < len(arguments) else "")
                if valeur.upper() not in _METHODES_ENVOI:
                    continue
            return True, "appel sortant expédiant des données"
    return False, None


def sous_commande_git(arguments):
    """Première sous-commande de git, en sautant les options globales.

    `git -C /repo-delivery push …` : sans ce saut, on prendrait le chemin pour
    la sous-commande. Les options globales qui consomment une valeur sont
    listées explicitement — les confondre décalait toute la lecture des
    arguments, et donc la branche détectée.
    """
    i = 0
    while i < len(arguments):
        a = arguments[i]
        if a in ("-C", "--git-dir", "--work-tree", "-c", "--namespace"):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        return a
    return None


def analyseur_git_ecriture(programme, arguments, contexte):
    """git mute-t-il un dépôt ?

    Les sous-commandes qui mutent sont DÉCLARÉES dans le YAML, pas ici : la
    liste est une donnée de politique, pas une règle de langage.
    """
    mutantes = set(contexte.get("sous_commandes_ecriture") or [])
    sous_commande = sous_commande_git(arguments)
    if sous_commande is None:
        return False, None
    if sous_commande in mutantes:
        return True, "sous-commande git modifiant le dépôt : %s" % sous_commande
    return False, None


ANALYSEURS = {
    "psql_ecriture": analyseur_psql_ecriture,
    "envoi_http": analyseur_envoi_http,
    "git_ecriture": analyseur_git_ecriture,
}


# ─────────────────────────────────────────────────────────────────────────────
# Chargement
# ─────────────────────────────────────────────────────────────────────────────

def racine_depot():
    """Racine du dépôt, déduite de l'emplacement de ce fichier.

    Jamais de chemin absolu en dur : le clone de Sam, le serveur
    (/root/workspace/dh-comite) et le conteneur (/workspace) ont trois racines
    différentes. Écrire l'une des trois casserait les deux autres.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def charger_capacites(chemin):
    import yaml  # importé ici : une absence de PyYAML doit produire une ERREUR
    with open(chemin, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not isinstance(config, dict) or "capacites" not in config:
        raise ValueError("%s : clé « capacites » absente" % chemin)
    return config


def charger_curseurs(chemin):
    """Lit le cache écrit par le crochet : direction|type_tache|niveau.

    Le crochet reste seul responsable d'aller en base et de rafraîchir ce
    fichier. Le moteur ne fait que le lire — une seule voie d'accès aux
    curseurs, donc un seul endroit à auditer.
    """
    curseurs = {}
    if not os.path.exists(chemin):
        return curseurs
    with open(chemin, "r", encoding="utf-8", errors="replace") as f:
        for ligne in f:
            morceaux = ligne.rstrip("\n").split("|")
            if len(morceaux) < 3:
                continue
            direction, tache, niveau = morceaux[0], morceaux[1], morceaux[2]
            try:
                curseurs[(direction, tache)] = int(niveau)
            except ValueError:
                continue
    return curseurs


# ─────────────────────────────────────────────────────────────────────────────
# Décision
# ─────────────────────────────────────────────────────────────────────────────

def detecter(commande, capacites):
    """Rend la liste des (nom_capacite, definition, outil, motif_detection)."""
    trouvees = []
    for fragment in commandes_simples(commande):
        programme, arguments = decouper_fragment(fragment)
        if not programme:
            continue
        for nom_capacite, definition in capacites.items():
            for outil in definition.get("outils", []):
                if outil.get("programme") != programme:
                    continue
                nom_analyseur = outil.get("analyseur")
                precision = None
                if nom_analyseur:
                    analyseur = ANALYSEURS.get(nom_analyseur)
                    if analyseur is None:
                        raise ValueError(
                            "analyseur inconnu dans capabilites.yaml : %s" % nom_analyseur
                        )
                    concerne, precision = analyseur(programme, arguments, outil)
                    if not concerne:
                        continue
                trouvees.append((nom_capacite, definition, outil, arguments, precision))
    return trouvees


def depot_vise(commande, definition):
    """Quel dépôt déclaré la commande vise-t-elle ?

    Indéterminable → le dépôt par défaut, c'est-à-dire le plus strict.
    """
    depots = definition.get("depots") or {}
    for chemin in depots:
        if chemin == ".":
            continue
        if re.search(r"(?<![\w/])%s(?![\w-])" % re.escape(chemin), commande):
            return chemin
    return definition.get("depot_par_defaut", ".")


def branche_poussee(arguments):
    """Branche visée par un `git push`, si elle est explicite dans la commande.

    On repart de la position de `push` plutôt que du début : les options
    globales de git (`-C <dépôt>`) précèdent la sous-commande et décaleraient le
    comptage des positionnels.
    """
    if "push" not in arguments:
        return None
    positionnels = []
    i = arguments.index("push") + 1
    while i < len(arguments):
        a = arguments[i]
        if a in ("-o", "--push-option", "--repo", "--receive-pack", "--exec"):
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        positionnels.append(a)
        i += 1
    # `git push <distant> <refspec>` — la branche est le second positionnel.
    # `HEAD:delivery/correctifs` : c'est la partie DROITE qui dit où ça atterrit.
    if len(positionnels) >= 2:
        return positionnels[1].split(":")[-1]
    return None


def decider(entree, capacites_config, curseurs):
    agent = (entree.get("agent") or "").strip()
    outil_appelant = entree.get("outil") or ""
    arguments_appel = entree.get("arguments") or {}

    gouvernees = capacites_config.get("directions_gouvernees") or []
    if agent not in gouvernees:
        return {
            "verdict": "NON_APPLICABLE",
            "agent": agent,
            "motif": "direction non gouvernée par le moteur — le garde-fou "
                     "applique ses règles d'origine",
        }, NON_APPLICABLE

    # Les trois capacités du socle minimal portent toutes sur une commande.
    # Write et Edit restent au garde-fou : le LOT-06 ne les couvre pas.
    if outil_appelant != "Bash":
        return {
            "verdict": "NON_APPLICABLE",
            "agent": agent,
            "motif": "outil %s hors du périmètre des trois capacités" % outil_appelant,
        }, NON_APPLICABLE

    commande = arguments_appel.get("command") or ""
    if not commande.strip():
        return {"verdict": "ALLOW", "agent": agent, "motif": "commande vide"}, ALLOW

    for nom_capacite, definition, outil, arguments, precision in detecter(
        commande, capacites_config["capacites"]
    ):
        curseur = definition["curseur"]
        requis = int(definition["niveau_requis"])
        regle = curseurs.get((agent, curseur), NIVEAU_DEFAUT)
        libelle_outil = outil.get("libelle") or outil.get("programme")

        base = {
            "agent": agent,
            "capacite": nom_capacite,
            "outil_detecte": outil.get("programme"),
            "curseur": curseur,
            "niveau_regle": regle,
            "niveau_requis": requis,
        }

        if regle < requis:
            declare = (agent, curseur) in curseurs
            motif = "%s — %s. Curseur « %s » réglé sur « %s » (%d), " \
                    "cette action exige « %s » (%d)." % (
                        definition.get("libelle", nom_capacite),
                        libelle_outil,
                        curseur,
                        NOMS_NIVEAUX.get(regle, str(regle)),
                        regle,
                        NOMS_NIVEAUX.get(requis, str(requis)),
                        requis,
                    )
            if not declare:
                # Distinguer « Sam a réglé bas » de « personne n'a réglé » : le
                # second est une lacune de configuration, pas une décision, et
                # il appelle une action différente.
                motif += (" Aucun réglage déclaré pour %s/%s : le défaut "
                          "restrictif s'applique." % (agent, curseur))
            if precision:
                motif += " (%s)" % precision
            base.update({"verdict": "DENY", "motif": motif})
            return base, DENY

        # Le niveau suffit. Reste le CANAL : le niveau dit « as-tu le droit
        # d'envoyer », le canal dit « par où ».
        canaux_imposes = (definition.get("canaux_imposes") or {}).get(agent)
        if canaux_imposes is not None:
            canal = outil.get("canal")
            if canal not in canaux_imposes:
                base.update({
                    "verdict": "DENY",
                    "canal_impose": canaux_imposes,
                    "canal_detecte": canal,
                    "motif": "canal imposé — %s doit sortir par %s ; « %s » "
                             "n'est pas ce canal." % (
                                 agent, ", ".join(canaux_imposes),
                                 outil.get("programme")),
                })
                return base, DENY

        if nom_capacite == "repo.write":
            depot = depot_vise(commande, definition)
            reglage = (definition.get("depots") or {}).get(depot) or {}
            imposee = reglage.get("branche_imposee")
            # La branche imposée gouverne ce qui SORT du dépôt, donc `push`.
            # L'appliquer à `commit` obligerait à nommer une branche là où la
            # commande n'en prend pas : un refus que l'agent ne pourrait pas
            # lever, c'est-à-dire un blocage sans suite (invariant I4).
            if imposee and sous_commande_git(arguments) == "push":
                cible = branche_poussee(arguments)
                if cible is None:
                    base.update({
                        "verdict": "DENY",
                        "depot": depot,
                        "branche_imposee": imposee,
                        "motif": "branche imposée — %s n'accepte que « %s », et "
                                 "la commande ne nomme aucune branche. Pousse "
                                 "explicitement sur %s." % (depot, imposee, imposee),
                    })
                    return base, DENY
                if cible != imposee:
                    base.update({
                        "verdict": "DENY",
                        "depot": depot,
                        "branche_imposee": imposee,
                        "branche_visee": cible,
                        "motif": "branche imposée — %s n'accepte que « %s », "
                                 "pas « %s »." % (depot, imposee, cible),
                    })
                    return base, DENY

    return {"verdict": "ALLOW", "agent": agent,
            "motif": "aucune des trois capacités contrôlées n'est engagée"}, ALLOW


def principal():
    analyseur = argparse.ArgumentParser(
        description="Policy Engine minimal — ALLOW/DENY par capacité."
    )
    analyseur.add_argument(
        "--capacites",
        default=os.path.join(racine_depot(), "config", "capabilites.yaml"),
        help="correspondance outil → capacité (défaut : config/capabilites.yaml)",
    )
    analyseur.add_argument(
        "--curseurs",
        default="/tmp/curseurs.cache",
        help="cache des curseurs écrit par le crochet (direction|type_tache|niveau)",
    )
    options = analyseur.parse_args()

    try:
        entree = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({"verdict": "ERREUR", "motif": "entrée illisible : %s" % e},
                         ensure_ascii=False))
        return ERREUR

    try:
        capacites_config = charger_capacites(options.capacites)
        curseurs = charger_curseurs(options.curseurs)
        verdict, code = decider(entree, capacites_config, curseurs)
    except Exception as e:
        # Fail-closed. Un moteur de sécurité qui laisse passer quand il tombe en
        # panne ne protège rien : le crochet traduira ERREUR en refus.
        print(json.dumps(
            {"verdict": "ERREUR", "motif": "%s : %s" % (type(e).__name__, e)},
            ensure_ascii=False))
        return ERREUR

    print(json.dumps(verdict, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(principal())
