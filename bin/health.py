#!/usr/bin/env python3
"""Executive Health Score — une vue d'entreprise, pas une pile de rapports.

POURQUOI CE SCRIPT (LOT-10, 18/08/2026). Le comité produisait six rapports par matin
et aucune vue. Chaque direction se notait elle-même : une seule y arrivait, avec une
formule réinventée à chaque ronde — 88 le 09/08, 68 le 10/08, 56 le 11/08, sans qu'un
fait ait bougé entre-temps. `bin/evaluer` a figé la formule en SQL le 11/08 ; la revue
adversariale du même jour (`config/REVUE_FABLE_GRILLES_RESULTAT.md`) a conclu de ne pas
le mettre en service, et il ne l'a jamais été. Motif retenu, mot pour mot :

    « Ce n'est pas un évaluateur gelé, c'est un questionnaire auto-déclaratif
      avec une calculatrice au bout. »

Geler la formule ne sert à rien tant que les données qu'elle lit sont écrites par les
évalués. C'est l'invariant I3, et c'est la seule chose que ce script ajoute vraiment :

    ┌───────────────────────────────────────────────────────────────────────┐
    │  NO SELF-ATTESTED KPI                                                 │
    │  Un agent ne peut jamais être à la fois producteur et source de       │
    │  vérité de son propre indicateur.                                     │
    └───────────────────────────────────────────────────────────────────────┘

Ici, ce n'est pas une consigne : c'est un mécanisme. Toute mesure déclare sa source et
son mode d'attestation ; une mesure dont l'attestation est une déclaration de l'évalué
est REFUSÉE à la construction, avant tout calcul. Aucun chemin de code ne permet d'en
ajouter une. `--autotest` le démontre en essayant.

    health.py                     le score, ses six composantes, leurs sources
    health.py --direction growth  le score d'une direction, même calcul restreint
    health.py --audit-sources     chaque source, qui l'écrit, pourquoi elle est admise
    health.py --coherence         vérifie que les scores par direction et le global
                                  sont le même calcul (critère d'acceptation n° 3)
    health.py --json              même contenu, pour le cockpit
    health.py --autotest          éprouve I3, l'agrégation et le tri-état
    health.py --sans-preflight    n'appelle pas bin/preflight.py (composante Risques)

Codes de sortie : 0 calcul rendu · 1 couverture incomplète (au moins une source
manquante) · 2 erreur d'usage.

CE SCRIPT N'ÉCRIT RIEN — ni en base, ni sur la plateforme, ni dans `deos_state`. Il
lit, il calcule, il affiche. Les directions le LISENT ; aucune ne l'alimente.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, datetime, timezone

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DSN_COMITE = os.environ.get("COMITE_DB_DSN", "")
DSN_PLATEFORME = os.environ.get("DEOS_RO_DSN", "")
LOG_BACKEND = "/prodlogs/backend-24h.log"

DELAI_SQL = 20        # secondes
DELAI_OUTIL = 90      # couts-consolides.py interroge la base plateforme et parcourt les JSON
DELAI_PREFLIGHT = 60  # 0,8 s mesuré pour les quatre directions actives ; large de reste

# Les quatre fonctions actives (SPEC §5). Les trois dormantes ne sont pas notées : leur
# cadence est à zéro, une note sur une fonction qu'on a délibérément mise en veille
# mesurerait la décision de Sam, pas leur travail. Elles ne disparaissent pas pour
# autant — I2 : leur mandat reste écrit, et le jour où elles s'activent, elles entrent
# ici sans qu'on ait à reconstruire quoi que ce soit.
DIRECTIONS = ["ceo", "chief-of-staff", "delivery", "growth"]
ENTREPRISE = "entreprise"   # ce qui n'est imputable à aucune direction

# UNE DIRECTION PORTE PLUSIEURS NOMS, ET LE CONTRÔLE I3 DOIT LES CONNAÎTRE TOUS.
# Trouvé en relisant la sortie d'--audit-sources : le contrôle comparait « la direction
# notée » aux acteurs qui écrivent la source, mot à mot. `tasks.valide_par` est écrite
# par « cos » ; la direction, elle, s'appelle `chief-of-staff` dans les fiches. Les deux
# chaînes ne se ressemblent pas, donc le contrôle ne voyait aucun conflit là où l'évalué
# et l'écrivain sont la même personne. Un garde-fou qui ne reconnaît pas son sujet ne
# garde rien.
#
# Growth cumule commercial et marketing (SPEC §5, fusion temporaire) : les scopes de
# `deos-state` et la table `curseurs` connaissent encore les deux anciens noms.
ALIAS = {
    "ceo": {"ceo"},
    "chief-of-staff": {"chief-of-staff", "cos"},
    "delivery": {"delivery"},
    "growth": {"growth", "commercial", "marketing"},
}


def _ecrit_par_l_evalue(direction, ecrit_par):
    """La direction évaluée figure-t-elle parmi les acteurs qui écrivent la source ?"""
    mots = set(re.findall(r"[a-z-]+", " ".join(ecrit_par).lower()))
    return bool(ALIAS.get(direction, {direction}) & mots)


# ═══════════════════════════════════════════════════════════════════════════════════
#  1. Les quatre états d'une mesure — et pourquoi un nombre nu est interdit
# ═══════════════════════════════════════════════════════════════════════════════════
#
# « FAILED sur 7 jours : 0 » ne distingue pas *sain* de *aucune donnée*, *mauvais DSN*
# ou *aucune tentative*. C'est la faille structurelle n° 1 de la revue du 11/08, et
# c'est elle qui a produit le brouillon notant le Delivery 100/100 le matin où son
# directeur se notait 56 avec ses preuves. Corriger la colonne fautive n'a pas corrigé
# la classe d'erreur : un résultat valide, incomplet, rendu sans erreur.
#
#   MESURE   la valeur est mesurée sur une source vivante
#   PARTIEL  la valeur est vraie mais la source déclare elle-même ce qu'elle omet
#            (c'est une BORNE, pas un total) — ou elle est reconstruite
#   INCONNU  la source n'existe pas, n'est pas atteignable, ou n'a jamais rien reçu
#   PERIME   la source existe mais n'a plus été alimentée dans sa fenêtre de fraîcheur
#
# INCONNU et PERIME ne valent JAMAIS vert. Ils ne valent pas rouge non plus — ils
# sortent du calcul et retirent leur poids de la couverture. Un tiret attire moins
# l'œil qu'un rouge : c'est le plus gros angle mort relevé le 11/08, et la raison pour
# laquelle la couverture est imprimée à côté du score, toujours, sans option.

MESURE, PARTIEL, INCONNU, PERIME = "MESURE", "PARTIEL", "INCONNU", "PERIME"
ETATS_CALCULABLES = (MESURE, PARTIEL)


# ═══════════════════════════════════════════════════════════════════════════════════
#  2. Registre des sources — qui écrit quoi
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Une source se déclare au CHAMP, pas à la table. `tasks` est écrite par tout le monde ;
# `tasks.valide_par` ne l'est que par le relecteur, et `tasks.cree_le` par personne —
# c'est un défaut de colonne posé par PostgreSQL. Déclarer « la table tasks » aurait
# rendu l'invariant invérifiable au moment précis où il compte.
#
# `ecrit_par` est la liste des acteurs qui peuvent écrire la donnée. `attestation` dit
# POURQUOI la source échappe à l'évalué :
#
#   horloge    la base pose la valeur (DEFAULT now(), déclencheur). Un agent écrit un
#              statut, il n'écrit pas l'heure.
#   tiers      un autre acteur que l'évalué l'écrit (Sam, le CEO, la plateforme).
#   croisee    deux acteurs distincts sont nécessaires, et la requête l'impose par un
#              prédicat. Aucun ne peut déplacer la mesure seul.
#   externe    l'artefact est vérifiable du dehors (page publiée, facture, dépôt).
#   declaration  l'évalué l'écrit seul. INADMISSIBLE — voir §3.

SOURCES = {
    "tasks.horloge": dict(
        libelle="tasks.cree_le / tasks.maj_le",
        ou="base comité",
        ecrit_par=["postgres (DEFAULT now(), déclencheur trg_tasks_touch)"],
        attestation="horloge",
        note="LOT-01 a posé le déclencheur précisément pour que maj_le ne mente pas."),
    "tasks.valide_par": dict(
        libelle="tasks.valide_par + tasks.constat",
        ou="base comité",
        ecrit_par=["cos", "ceo (suppléance)"],
        attestation="croisee",
        note="`deos-tasks valider` exige statut='done' — posé par l'exécutant — ET un "
             "--par restreint à cos/ceo. Deux acteurs distincts, aucun ne suffit."),
    "decisions.accordee": dict(
        libelle="decisions.statut = 'accordee'",
        ou="base comité",
        ecrit_par=["ceo", "sam"],
        attestation="tiers",
        note="Matrice de droits du registre : accordee et attente_sam sont des actes de "
             "direction. Le Chief of Staff, qui est noté dessus, ne peut pas les poser."),
    "decisions.horloge": dict(
        libelle="decisions.date / decisions.updated_at",
        ou="base comité",
        ecrit_par=["postgres (DEFAULT now(), déclencheur trg_decisions_touch)"],
        attestation="horloge"),
    # DÉFAUT TROUVÉ PAR CE LOT, le 18/08, et par le mécanisme lui-même : la mesure du
    # Strategic Yield avait été écrite en supposant que « accordee » venait de Sam. Le
    # constructeur de mesure l'a refusée — `accordee` se pose par `ceo` OU `sam`
    # (matrice de droits du registre), et `validation_par` n'est PAS renseignée pour ce
    # statut : rien en base ne dit lequel des deux a accordé. Le CEO pourrait donc
    # accorder ses propres propositions et faire monter son rendement seul.
    # Le manque est petit et le correctif l'est aussi — voir docs/KPI.md §5.
    "absente.arbitrage_sam": dict(
        libelle="qui a posé 'accordee' sur une décision d'origine 'ceo'",
        ou="base comité — colonne existante, NON RENSEIGNÉE pour ce statut",
        # Écrite par Sam UNE FOIS LE CORRECTIF POSÉ : la mesure ne comptera que les
        # acceptations portant validation_par='sam'. Aujourd'hui le statut se pose
        # aussi par le CEO et rien ne les distingue — d'où `absente`, et non une
        # source « tiers » qu'on prendrait pour bonne.
        ecrit_par=["sam, une fois le correctif posé"],
        attestation="tiers",
        absente="Strategic Yield : c'est Sam qui juge de l'acceptation (arbitrage du "
                "17/08), mais rien ne trace QUI accorde. `bin/deos-decisions` écrit "
                "validation_par pour clos, obsolete et refusee, pas pour accordee. "
                "Correctif : l'y écrire aussi, ou réserver `accordee` à `sam` quand "
                "l'origine est `ceo`. Une ligne dans l'outil, et l'objectif devient "
                "mesurable."),
    "plateforme.executions": dict(
        libelle="v_deos_executions (status, created_at, completed_at)",
        ou="base plateforme, rôle deos_ro",
        ecrit_par=["la plateforme (pipeline Sophie→Lucas)"],
        attestation="tiers",
        note="Le comité y a un accès en LECTURE SEULE. Il n'existe aucun chemin "
             "d'écriture du comité vers ces vues — c'est l'invariant I1 qui le garantit."),
    "plateforme.build_phases": dict(
        libelle="v_deos_build_phases (status, elena_verdict, agent_id)",
        ou="base plateforme, rôle deos_ro",
        ecrit_par=["la plateforme (agents Raj/Diego/Zara, revue Elena)"],
        attestation="croisee",
        note="Une phase aboutie porte le travail d'un agent ET le verdict d'Elena, qui "
             "est un autre agent. C'est l'attestation croisée demandée le 11/08."),
    "plateforme.blog": dict(
        libelle="v_deos_blog_articles (published_at)",
        ou="base plateforme, rôle deos_ro",
        ecrit_par=["la chaîne de publication"],
        attestation="externe",
        note="Publié, pas rédigé. Un contenu qui vit dans un rapport n'existe pas."),
    "logs.backend": dict(
        libelle="/prodlogs/backend-24h.log (niveaux ERROR et CRITICAL)",
        ou="montage /prodlogs, lecture seule",
        ecrit_par=["le backend de la plateforme"],
        attestation="tiers",
        note="Export toutes les 15 min. Au-delà de 2 h sans écriture, la source est "
             "PERIME : un fichier figé compterait zéro erreur pour de mauvaises raisons."),
    "outil.couts": dict(
        libelle="bin/couts-consolides.py --json",
        ou="base plateforme + fichiers de session",
        ecrit_par=["le moteur d'exécution (costUSD)", "la plateforme (v_deos_couts_pipeline)"],
        attestation="tiers",
        note="Le coût d'un appel est écrit par ce qui l'exécute, jamais par l'agent qui "
             "le passe. L'outil déclare lui-même ses trous : la mesure est une BORNE "
             "INFÉRIEURE, donc PARTIEL en permanence — voir §5."),
    "outil.preflight": dict(
        libelle="bin/preflight.py --toutes",
        ou="environnement (montages, clés, curseurs, API)",
        ecrit_par=["le programme lui-même, à partir de l'état réel du système"],
        attestation="tiers",
        note="Un agent ne peut pas déclarer qu'il a ses moyens : le Preflight les essaie."),

    # ── Sources qui N'EXISTENT PAS ENCORE ────────────────────────────────────────────
    # Elles sont déclarées ici avec leur manque. Une source absente doit se lire dans
    # l'outil, pas seulement dans un document : c'est la différence entre une lacune
    # connue et une lacune oubliée. Le jour où elle est créée, la mesure s'allume sans
    # qu'on touche au code de calcul.
    "absente.salesforce": dict(
        libelle="v_deos_salesforce_pipeline (comptes qualifiés)",
        ou="base plateforme — À CRÉER",
        ecrit_par=["Salesforce, via la synchronisation de la plateforme"],
        attestation="tiers",
        absente="Proposée le 02/08 par l'audit des capacités (effort M, risque faible), "
                "jamais créée. Sans elle, le pipeline ne se compte que dans un rapport, "
                "c'est-à-dire nulle part : règle de Sam du 10/08."),
    "absente.echeances": dict(
        libelle="table echeances_reglementaires (libellé, date, statut)",
        ou="base comité — À CRÉER",
        ecrit_par=["le Juridique, relu par Sam"],
        attestation="externe",
        absente="Arbitrée par Sam le 11/08 comme action immédiate à coût quasi nul, "
                "jamais créée. C'est la faille n° 5 de la revue : la seule direction "
                "portant une échéance dure au 1er septembre est la seule non mesurée."),
    "absente.pages_publiees": dict(
        libelle="URL des trois sites et marqueurs de contenu attendus",
        ou="dispositif — À DÉCLARER",
        ecrit_par=["personne : aucune URL publique n'est déclarée dans le dépôt"],
        attestation="externe",
        absente="Le 12/08, les trois pages légales répondaient en 200 SANS contenu "
                "légal, et c'était compté comme livré. Un contrôle mécanique demande "
                "l'URL ET le marqueur de contenu ; ni l'une ni l'autre n'est déclarée."),
    "absente.lecture_sam": dict(
        libelle="accusé de lecture du brief par Sam",
        ou="base comité — À CRÉER",
        ecrit_par=["sam"],
        attestation="tiers",
        absente="L'objectif O1 du CEO dit « Sam confirme l'avoir lu et décidé dessus ». "
                "Le brief, lui, est écrit par le CEO : le compter reviendrait à noter "
                "l'auteur sur sa propre production. Rien n'enregistre la lecture."),
    "absente.initiative_fosse": dict(
        libelle="marqueur d'initiative de différenciation sur une décision",
        ou="base comité — À CRÉER",
        # Le marqueur ne vaut que posé par Sam : proposé par le CEO, il noterait le
        # CEO sur ce que le CEO a bien voulu appeler une initiative de fossé.
        ecrit_par=["sam, à la validation d'une proposition"],
        absente="O3 du CEO vise une initiative de fossé par trimestre, testée. Rien ne "
                "distingue une telle initiative des autres décisions : la reconnaître "
                "au texte serait un jugement, donc hors de ce qui se compte ici.",
        attestation="tiers"),
}


# ═══════════════════════════════════════════════════════════════════════════════════
#  3. I3 rendu mécanique — le seul constructeur de mesure
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Même dispositif que la règle du paradoxe dans bin/preflight.py : une seule fonction
# fabrique l'objet, et elle refuse ce que la règle interdit. Une consigne demande la
# coopération de celui qu'elle contraint ; un mécanisme non.
#
# Trois refus, tous à la construction et tous bruyants :
#   · source inconnue du registre       — on ne mesure pas sur une source anonyme
#   · attestation = declaration          — c'est exactement I3
#   · l'évalué figure dans `ecrit_par`   — le cas subtil : source déclarée « tiers »
#                                          alors que la direction notée l'écrit aussi
#
# Le troisième est celui qui aurait attrapé les grilles du 11/08.

class MesureInadmissible(Exception):
    """Levée quand une mesure violerait I3. Jamais rattrapée en fonctionnement normal."""


def mesure(cle, libelle, composante, source, direction, etat, valeur, score,
           detail="", partagee_avec=None):
    """Fabrique une mesure. SEUL constructeur — voir la règle ci-dessus."""
    src = SOURCES.get(source)
    if src is None:
        raise MesureInadmissible(
            f"{cle} : source '{source}' absente du registre. Une mesure sans source "
            f"nommée est une affirmation.")
    if src["attestation"] == "declaration":
        raise MesureInadmissible(
            f"{cle} : source '{source}' attestée par déclaration de l'évalué. "
            f"I3 — un score auto-déclaré mesure la déclaration, pas le fait.")
    if direction != ENTREPRISE and _ecrit_par_l_evalue(direction, src["ecrit_par"]) \
            and src["attestation"] != "croisee":
        raise MesureInadmissible(
            f"{cle} : '{direction}' est notée sur une source qu'elle écrit "
            f"({src['libelle']}). I3 — sauf attestation croisée imposée par la "
            f"requête, ce qui n'est pas le cas ici.")
    return {
        "cle": cle, "libelle": libelle, "composante": composante, "direction": direction,
        "source": source, "source_libelle": src["libelle"], "ecrit_par": src["ecrit_par"],
        "attestation": src["attestation"], "etat": etat,
        "valeur": valeur, "score": score, "detail": detail,
        "partagee_avec": partagee_avec or [],
    }


def inconnue(cle, libelle, composante, source, direction, motif):
    """Mesure dont la source manque. Elle EXISTE dans la sortie — c'est tout l'objet."""
    return mesure(cle, libelle, composante, source, direction,
                  etat=INCONNU, valeur=None, score=None, detail=motif)


# ═══════════════════════════════════════════════════════════════════════════════════
#  4. Barème — et pourquoi la valeur brute reste imprimée à côté du score
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Un barème linéaire entre un seuil « bon » et un seuil « mauvais », borné à [0, 100].
# Il a une zone morte, comme tous les barèmes bornés : au-delà de `mauvais`, cent de
# plus ne coûtent rien. C'est la faille n° 4 du 11/08 — à 61 décisions accordées, la
# pénalité du Chief of Staff saturait, et la métrique la plus dégradée cessait
# d'informer là où c'était le plus grave.
#
# On ne prétend pas la supprimer : un score borné a nécessairement un plancher. On la
# rend inoffensive en imprimant TOUJOURS la valeur mesurée à côté du score. Au-delà du
# plancher, c'est le nombre qui informe, et il est là.

def bareme(valeur, bon, mauvais):
    if bon == mauvais:
        return 100.0 if valeur <= bon else 0.0
    if bon < mauvais:                       # plus c'est petit, mieux c'est
        r = (mauvais - valeur) / (mauvais - bon)
    else:                                   # plus c'est grand, mieux c'est
        r = (valeur - mauvais) / (bon - mauvais)
    return round(max(0.0, min(1.0, r)) * 100, 1)


# ═══════════════════════════════════════════════════════════════════════════════════
#  5. Accès aux sources — chaque lecture rend un état, jamais un nombre nu
# ═══════════════════════════════════════════════════════════════════════════════════

class Lecture:
    """Résultat d'un accès : lignes + état. `.absente` distingue les trois zéros."""

    def __init__(self, lignes=None, etat=MESURE, motif=""):
        self.lignes = lignes or []
        self.etat = etat
        self.motif = motif

    @property
    def ok(self):
        return self.etat in ETATS_CALCULABLES

    def un(self, defaut=0):
        """Première colonne de la première ligne, en nombre."""
        if not self.lignes or not self.lignes[0] or self.lignes[0][0] in ("", None):
            return defaut
        v = self.lignes[0][0]
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                return defaut


def _psql(dsn, requete, delai=DELAI_SQL):
    if not dsn:
        return Lecture(etat=INCONNU, motif="DSN absent de l'environnement")
    try:
        r = subprocess.run(["psql", dsn, "-tAF", "|", "-c", requete],
                           capture_output=True, text=True, timeout=delai)
    except FileNotFoundError:
        return Lecture(etat=INCONNU, motif="psql introuvable")
    except subprocess.TimeoutExpired:
        return Lecture(etat=INCONNU, motif=f"pas de réponse en {delai} s")
    if r.returncode != 0:
        # Le message de PostgreSQL est conservé : « relation does not exist » et
        # « permission denied » ne demandent pas la même suite, et un INCONNU qui ne
        # dit pas lequel des deux oblige à re-diagnostiquer.
        detail = (r.stderr or "").strip().split("\n")[0][:160]
        return Lecture(etat=INCONNU, motif=detail or f"psql a rendu {r.returncode}")
    lignes = [l.split("|") for l in r.stdout.strip().split("\n") if l.strip()]
    return Lecture(lignes)


def comite(requete):
    return _psql(DSN_COMITE, requete)


def plateforme(requete):
    return _psql(DSN_PLATEFORME, requete)


def volume(lecture_totale, minimum=1):
    """Invariant de volume : une table qui n'a JAMAIS rien reçu ne vaut pas zéro.

    Correctif systémique de l'incident v_deos_signaux (audit valide, incomplet, sans
    erreur) : avant de compter sur une fenêtre, on vérifie que la source a déjà reçu
    des écritures. Sinon on ne sait pas distinguer « rien ne s'est passé » de « rien
    n'arrive jamais ici », et les deux n'appellent pas la même conduite.
    """
    if not lecture_totale.ok:
        return False
    return lecture_totale.un() >= minimum


def fraicheur_fichier(chemin, heures):
    """MESURE / PERIME / INCONNU selon l'existence et l'âge du dernier écrit."""
    if not os.path.exists(chemin):
        return INCONNU, f"{chemin} absent (montage non présent hors du conteneur)"
    age = (time.time() - os.path.getmtime(chemin)) / 3600.0
    if age > heures:
        return PERIME, f"dernier écrit il y a {age:.1f} h (fenêtre {heures} h)"
    return MESURE, f"dernier écrit il y a {age:.1f} h"


def outil(argv, delai):
    """Lance un outil du dépôt et rend (sortie, motif d'échec)."""
    chemin = os.path.join(RACINE, argv[0])
    if not os.path.exists(chemin):
        return None, f"{argv[0]} absent du dépôt"
    try:
        r = subprocess.run([sys.executable, chemin] + argv[1:],
                           capture_output=True, text=True, timeout=delai)
    except subprocess.TimeoutExpired:
        return None, f"{argv[0]} n'a pas rendu la main en {delai} s"
    if r.returncode not in (0, 1):   # 1 = « au moins une alerte », pas une panne
        return None, (r.stderr or "").strip().split("\n")[0][:160] or "code inattendu"
    return r.stdout, ""


# ═══════════════════════════════════════════════════════════════════════════════════
#  6. Composante EXÉCUTION — 30 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Contrat du lot : tâches terminées / créées, dette en évolution, âge moyen.
#
# Le piège tenait dans « terminées ». `tasks.statut` est écrit par le porteur : compter
# les `done` reviendrait à lui demander s'il a fini. On compte donc les tâches VALIDÉES
# — statut posé par le relecteur, sur une tâche que le porteur a d'abord déclarée finie.
# Il faut deux acteurs pour bouger ce nombre, et la requête impose valide_par <> owner :
# une direction qui serait son propre relecteur ne compterait pas.

FENETRE_EXEC = 14   # jours


def composante_execution():
    m = []
    creees = comite(
        f"SELECT owner, count(*) FROM tasks "
        f"WHERE cree_le > now() - interval '{FENETRE_EXEC} days' GROUP BY 1")
    validees = comite(
        f"SELECT owner, count(*) FROM tasks "
        f"WHERE cree_le > now() - interval '{FENETRE_EXEC} days' "
        f"  AND valide_par IS NOT NULL AND valide_par <> owner GROUP BY 1")
    total_tasks = comite("SELECT count(*) FROM tasks")

    if not creees.ok or not volume(total_tasks):
        m.append(inconnue(
            "exec.validees", f"tâches validées / créées sur {FENETRE_EXEC} j",
            "execution", "tasks.valide_par", ENTREPRISE,
            creees.motif or "la table tasks n'a jamais reçu de ligne — "
                            "aucune conclusion possible, ni bonne ni mauvaise"))
    elif not creees.lignes:
        # La table est alimentée, mais rien n'a été créé sur la fenêtre. Le ratio n'a
        # pas de dénominateur — et surtout, sans cette branche, la mesure disparaîtrait
        # de la composante et son poids se redistribuerait en silence sur les deux
        # autres. Une mesure qui s'évapore vaut mieux affichée qu'absente.
        m.append(inconnue(
            "exec.validees", f"tâches validées / créées sur {FENETRE_EXEC} j",
            "execution", "tasks.valide_par", ENTREPRISE,
            f"aucune tâche créée sur {FENETRE_EXEC} j — le ratio n'a pas de "
            f"dénominateur. Ce n'est pas zéro, c'est indéfini."))
    else:
        nb_c = {l[0]: int(l[1]) for l in creees.lignes}
        nb_v = {l[0]: int(l[1]) for l in validees.lignes} if validees.ok else {}
        for direction in sorted(set(nb_c) | set(nb_v)):
            c, v = nb_c.get(direction, 0), nb_v.get(direction, 0)
            cible = direction if direction in DIRECTIONS else ENTREPRISE
            m.append(mesure(
                f"exec.validees.{direction}",
                f"tâches validées / créées — {direction}", "execution",
                "tasks.valide_par", cible, MESURE, f"{v}/{c}",
                # 95 % est l'objectif O2 du Chief of Staff ; 0 % vaut 0. Linéaire entre.
                bareme(v / c if c else 0, bon=0.95, mauvais=0.0),
                detail="validation par un tiers, valide_par <> owner"))

    m.append(_dette())

    age = comite(
        "SELECT coalesce(round(avg(extract(epoch from now() - cree_le) / 86400)::numeric, 1), 0), "
        "       count(*) FROM tasks WHERE statut NOT IN ('done','valide')")
    if not age.ok or not volume(total_tasks):
        m.append(inconnue("exec.age", "âge moyen des tâches ouvertes", "execution",
                          "tasks.horloge", ENTREPRISE, age.motif or "aucune tâche en base"))
    else:
        ouvertes = int(age.lignes[0][1])
        jours = float(age.lignes[0][0])
        m.append(mesure(
            "exec.age", "âge moyen des tâches ouvertes (j)", "execution",
            "tasks.horloge", ENTREPRISE, MESURE, jours if ouvertes else 0,
            bareme(jours, bon=3, mauvais=21),
            detail=f"{ouvertes} tâche(s) ouverte(s) — l'horloge est posée par la base"))
    return m


# La dette est calculée UNE fois : elle sert à la composante Exécution et à l'objectif
# O3 du Chief of Staff, qui est littéralement « la dette diminue ». Le partage est
# imprimé dans les deux sorties (`partagee_avec`) plutôt que caché : un fait compté à
# deux endroits pèse deux fois, et il vaut mieux que ça se lise.
_DETTE_CALCULEE = None


def _dette():
    """Dette d'exécution et son sens de variation, reconstruits faute d'historique.

    Une tâche créée avant J-7 était ouverte à J-7 si elle n'était pas déjà terminale à
    cette date — ce que `maj_le` permet de dire, puisque le déclencheur l'entretient.
    La reconstruction se trompe dans un seul cas : une tâche terminée puis rouverte
    dans la fenêtre. D'où PARTIEL — la valeur est utile, la méthode est dite, et on ne
    la présente pas comme un relevé d'historique qui n'existe pas.
    """
    global _DETTE_CALCULEE
    if _DETTE_CALCULEE is not None:
        return _DETTE_CALCULEE
    total_tasks = comite("SELECT count(*) FROM tasks")
    dette = comite(
        "SELECT "
        "  count(*) FILTER (WHERE statut NOT IN ('done','valide')), "
        "  count(*) FILTER (WHERE statut NOT IN ('done','valide') "
        "                   AND cree_le < now() - interval '7 days') "
        "     + count(*) FILTER (WHERE statut IN ('done','valide') "
        "                   AND cree_le < now() - interval '7 days' "
        "                   AND maj_le > now() - interval '7 days') "
        "FROM tasks")
    if not dette.ok or not volume(total_tasks):
        _DETTE_CALCULEE = inconnue(
            "exec.dette", "dette d'exécution, évolution sur 7 j", "execution",
            "tasks.horloge", ENTREPRISE, dette.motif or "aucune tâche en base")
    else:
        aujourdhui = int(dette.lignes[0][0])
        il_y_a_7j = int(dette.lignes[0][1])
        delta = aujourdhui - il_y_a_7j
        _DETTE_CALCULEE = mesure(
            "exec.dette", "dette d'exécution, évolution sur 7 j", "execution",
            "tasks.horloge", ENTREPRISE, PARTIEL, f"{aujourdhui} ({delta:+d})",
            # En baisse ou stable : 100. Chaque tâche ouverte de plus coûte 10 points,
            # zéro à +10. L'objectif O3 du CoS porte sur une DIRECTION, pas sur un
            # stock : c'est le signe du delta qui est noté.
            bareme(delta, bon=0, mauvais=10),
            detail="dette à J-7 reconstruite depuis cree_le et maj_le — pas un historique",
            partagee_avec=["objectifs.cos.O3"])
    return _DETTE_CALCULEE


# ═══════════════════════════════════════════════════════════════════════════════════
#  7. Composante OBJECTIFS — 25 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Les douze objectifs des quatre fonctions actives, tels qu'écrits dans .claude/agents/
# et documentés dans docs/MANDATS.md. Trois par direction, poids égal : c'est ce qui
# rend le score par direction comparable au global sans arithmétique cachée.
#
# Sept se mesurent aujourd'hui. Cinq non, et ils sortent en INCONNU avec la source à
# créer NOMMÉE. C'est délibéré : un objectif qu'on ne sait pas mesurer doit se voir. La
# fiche du Chief of Staff engage ce script à calculer ses trois objectifs « directement
# sur les tables, jamais repris d'un chiffre qu'il déclare » — c'est ici, et nulle part
# ailleurs, que cette promesse se tient.

def composante_objectifs():
    m = []

    # ── CEO ─────────────────────────────────────────────────────────────────────────
    m.append(inconnue(
        "objectifs.ceo.O1", "CEO O1 — brief lu et décidé par Sam", "objectifs",
        "absente.lecture_sam", "ceo",
        "le brief est écrit par le CEO ; sa lecture par Sam n'est enregistrée nulle part"))

    # O2 — Strategic Yield. La mesure existait, écrite puis REFUSÉE par le constructeur :
    # rien en base ne dit qui a accordé une proposition du CEO. Le compte des
    # propositions en attente est quand même rendu, parce qu'il informe Sam et
    # qu'il n'est pas un score : c'est un fait, pas une note.
    #
    # La règle du 17/08 s'appliquerait telle quelle le jour où la source existe : une
    # proposition sans réponse n'est pas un refus, au-delà de 14 jours elle passe en
    # veille et SORT du calcul. Sans cette sortie, le silence de Sam dégraderait
    # mécaniquement le score du CEO — on mesurerait la disponibilité de Sam.
    attente = comite(
        "SELECT count(*), count(*) FILTER (WHERE statut = 'attente_sam' "
        "                                  AND date < now() - interval '14 days') "
        "FROM decisions WHERE origine = 'ceo'")
    contexte = ""
    if attente.ok and attente.lignes:
        total, veille = (int(x) for x in attente.lignes[0])
        contexte = (f" — {total} proposition(s) d'origine 'ceo' en base, dont {veille} "
                    f"sans réponse depuis plus de 14 j (en veille, hors calcul)")
    m.append(inconnue(
        "objectifs.ceo.O2", "CEO O2 — Strategic Yield", "objectifs",
        "absente.arbitrage_sam", "ceo",
        SOURCES["absente.arbitrage_sam"]["absente"] + contexte))

    m.append(inconnue(
        "objectifs.ceo.O3", "CEO O3 — une initiative de fossé testée par trimestre",
        "objectifs", "absente.initiative_fosse", "ceo",
        "rien ne distingue mécaniquement une initiative de différenciation d'une autre décision"))

    # ── Chief of Staff ──────────────────────────────────────────────────────────────
    # O1 : toute décision accordée porte une tâche sous 24 h. `accordee` est posé par le
    # CEO ou Sam, l'horloge par la base : le CoS est noté sur deux choses qu'il n'écrit
    # ni l'une ni l'autre, alors même qu'il est la seule fonction qui écrit au registre.
    o1 = comite(
        "WITH a AS (SELECT d.id, d.updated_at, min(t.cree_le) AS premiere "
        "           FROM decisions d LEFT JOIN tasks t ON t.decision_id = d.id "
        "           WHERE d.statut IN ('accordee','en_execution') GROUP BY 1,2) "
        "SELECT count(*), count(*) FILTER ("
        "  WHERE premiere IS NOT NULL AND premiere <= updated_at + interval '24 hours') "
        "FROM a")
    accordees_total = comite("SELECT count(*) FROM decisions WHERE statut IN ('accordee','en_execution')")
    if not o1.ok or not volume(accordees_total):
        m.append(inconnue("objectifs.cos.O1", "CoS O1 — tâche spécifiée sous 24 h",
                          "objectifs", "decisions.accordee", "chief-of-staff",
                          o1.motif or "aucune décision accordée en base"))
    else:
        total, dans_les_temps = (int(x) for x in o1.lignes[0])
        m.append(mesure(
            "objectifs.cos.O1", "CoS O1 — décisions accordées portant une tâche sous 24 h",
            "objectifs", "decisions.accordee", "chief-of-staff", MESURE,
            f"{dans_les_temps}/{total}", bareme(dans_les_temps / total, bon=1.0, mauvais=0.0),
            detail="délai mesuré entre decisions.updated_at et la première tasks.cree_le"))

    # O2 : « sans rester indéfiniment dans le backlog ». On ne lit pas le statut — écrit
    # par le porteur — mais la validation par un tiers, sur les tâches assez vieilles
    # pour avoir dû aboutir.
    o2 = comite(
        f"SELECT count(*), count(*) FILTER (WHERE valide_par IS NOT NULL AND valide_par <> owner) "
        f"FROM tasks WHERE cree_le < now() - interval '{FENETRE_EXEC} days'")
    if not o2.ok or o2.un() == 0:
        m.append(inconnue("objectifs.cos.O2", "CoS O2 — 95 % d'états terminaux",
                          "objectifs", "tasks.valide_par", "chief-of-staff",
                          o2.motif or f"aucune tâche de plus de {FENETRE_EXEC} j — "
                                      f"la question ne se pose pas encore"))
    else:
        total, abouties = (int(x) for x in o2.lignes[0])
        m.append(mesure(
            "objectifs.cos.O2",
            f"CoS O2 — tâches de plus de {FENETRE_EXEC} j validées par un tiers",
            "objectifs", "tasks.valide_par", "chief-of-staff", MESURE,
            f"{abouties}/{total}", bareme(abouties / total, bon=0.95, mauvais=0.0),
            detail="le statut posé par le porteur n'est pas lu : seule la validation compte"))

    dette = _dette()
    if dette["etat"] in ETATS_CALCULABLES:
        d = dict(dette)
        d.update(cle="objectifs.cos.O3", libelle="CoS O3 — la dette d'exécution diminue",
                 composante="objectifs", direction="chief-of-staff",
                 partagee_avec=["exec.dette"])
        m.append(d)
    else:
        m.append(inconnue("objectifs.cos.O3", "CoS O3 — la dette d'exécution diminue",
                          "objectifs", "tasks.horloge", "chief-of-staff",
                          "dette non calculable — voir la composante Exécution"))

    # ── Delivery ────────────────────────────────────────────────────────────────────
    m.append(inconnue(
        "objectifs.delivery.O1", "Delivery O1 — produit livrable au 27/09", "objectifs",
        "absente.pages_publiees", "delivery",
        "aucune URL publique ni marqueur de contenu déclaré : « la page répond » ne "
        "prouve rien, c'est l'erreur du 12/08"))

    incidents = _incidents_ouverts()
    if incidents["etat"] in ETATS_CALCULABLES:
        m.append(mesure(
            "objectifs.delivery.O2", "Delivery O2 — zéro incident critique ouvert > 24 h",
            "objectifs", "plateforme.executions", "delivery", incidents["etat"],
            incidents["valeur"], bareme(incidents["nombre"], bon=0, mauvais=3),
            detail=incidents["detail"], partagee_avec=["produit.incidents"]))
    else:
        m.append(inconnue("objectifs.delivery.O2", "Delivery O2 — zéro incident critique > 24 h",
                          "objectifs", "plateforme.executions", "delivery", incidents["detail"]))

    chaine = _chaine_aboutie()
    if chaine["etat"] in ETATS_CALCULABLES:
        m.append(mesure(
            "objectifs.delivery.O3", "Delivery O3 — la chaîne SDS → BUILD aboutit",
            "objectifs", "plateforme.build_phases", "delivery", chaine["etat"],
            chaine["valeur"], chaine["score"], detail=chaine["detail"],
            partagee_avec=["produit.chaine"]))
    else:
        m.append(inconnue("objectifs.delivery.O3", "Delivery O3 — la chaîne SDS → BUILD aboutit",
                          "objectifs", "plateforme.build_phases", "delivery", chaine["detail"]))

    # ── Growth ──────────────────────────────────────────────────────────────────────
    m.append(inconnue(
        "objectifs.growth.O1", "Growth O1 — positionnement en ligne, sans écart avec les CGV",
        "objectifs", "absente.pages_publiees", "growth",
        "même manque que Delivery O1 : ni URL ni marqueur déclaré"))

    pipeline = _pipeline_qualifie()
    if pipeline["etat"] in ETATS_CALCULABLES:
        m.append(mesure("objectifs.growth.O2", "Growth O2 — pipeline qualifié", "objectifs",
                        "absente.salesforce", "growth", pipeline["etat"], pipeline["valeur"],
                        pipeline["score"], detail=pipeline["detail"],
                        partagee_avec=["pipeline.comptes"]))
    else:
        m.append(inconnue("objectifs.growth.O2", "Growth O2 — pipeline qualifié", "objectifs",
                          "absente.salesforce", "growth", pipeline["detail"]))

    publies = plateforme(
        "SELECT count(*) FROM v_deos_blog_articles "
        "WHERE published_at > now() - interval '30 days'")
    jamais = plateforme("SELECT count(*) FROM v_deos_blog_articles WHERE published_at IS NOT NULL")
    if not publies.ok or not volume(jamais):
        m.append(inconnue(
            "objectifs.growth.O3", "Growth O3 — contenus publiés sur 30 j", "objectifs",
            "plateforme.blog", "growth",
            publies.motif or "v_deos_blog_articles n'a jamais reçu de publication : "
                             "on ne peut pas distinguer « rien publié » de « table non alimentée »"))
    else:
        n = publies.un()
        m.append(mesure(
            "objectifs.growth.O3", "Growth O3 — contenus publiés sur 30 j", "objectifs",
            "plateforme.blog", "growth", MESURE, n, bareme(n, bon=4, mauvais=0),
            detail="publiés, pas rédigés — published_at renseigné"))
    return m


# ═══════════════════════════════════════════════════════════════════════════════════
#  8. Composante PRODUIT — 20 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Incidents ouverts, état de la chaîne, livrabilité. Rien n'est lu dans le rapport du
# Delivery : le `domain_score` de sa fiche compte des incidents dont il fixe lui-même
# la gravité — c'est un jugement, et il est du côté de l'évalué.
#
# Le taux d'échec est apparié à son volume de tentatives. Sans cet appariement, la
# stratégie optimale sous cette métrique est de ne plus rien tenter : zéro échec
# garanti, note maximale, plateforme à l'arrêt. C'est la faille n° 2 du 11/08, et elle
# ne se corrige pas en changeant le seuil — seulement en refusant de conclure quand il
# n'y a pas eu d'essais.

VOLUME_MINIMAL_EXEC = 3


def _incidents_ouverts():
    ex = plateforme(
        "SELECT count(*) FILTER (WHERE status = 'FAILED' "
        "         AND coalesce(completed_at, created_at) < now() - interval '24 hours' "
        "         AND coalesce(completed_at, created_at) > now() - interval '7 days'), "
        "       count(*) FILTER (WHERE created_at > now() - interval '7 days') "
        "FROM v_deos_executions")
    if not ex.ok:
        return {"etat": INCONNU, "detail": ex.motif, "nombre": None, "valeur": None}
    echecs, tentatives = (int(x) for x in ex.lignes[0])
    if tentatives < VOLUME_MINIMAL_EXEC:
        return {"etat": INCONNU, "nombre": None, "valeur": None,
                "detail": f"{tentatives} exécution(s) sur 7 j — sous le volume minimal de "
                          f"{VOLUME_MINIMAL_EXEC}, un zéro ne dirait pas si c'est sain ou à l'arrêt"}
    etat, note = fraicheur_fichier(LOG_BACKEND, heures=2)
    erreurs = None
    if etat == MESURE:
        try:
            with open(LOG_BACKEND, "r", errors="replace") as f:
                erreurs = sum(1 for l in f if '"level": "ERROR"' in l or '"level": "CRITICAL"' in l)
        except OSError as e:
            erreurs, etat, note = None, INCONNU, str(e)[:120]
    detail = f"{echecs} échec(s) ouvert(s) > 24 h sur {tentatives} exécution(s) en 7 j"
    if erreurs is not None:
        detail += f" · {erreurs} ERROR/CRITICAL dans les logs 24 h"
    else:
        detail += f" · logs backend : {note}"
    return {"etat": MESURE if erreurs is not None else PARTIEL,
            "nombre": echecs, "valeur": f"{echecs}/{tentatives}", "detail": detail,
            "erreurs_log": erreurs}


def _chaine_aboutie():
    """Une chaîne aboutie demande le travail d'un agent ET le verdict d'un autre."""
    ph = plateforme(
        "SELECT coalesce(extract(day from now() - max(completed_at))::int, -1) "
        "FROM v_deos_build_phases "
        "WHERE status = 'completed' AND coalesce(elena_verdict, '') <> ''")
    total = plateforme("SELECT count(*) FROM v_deos_build_phases")
    if not ph.ok or not volume(total):
        return {"etat": INCONNU, "valeur": None, "score": None,
                "detail": ph.motif or "v_deos_build_phases n'a jamais reçu de phase"}
    jours = ph.un(defaut=-1)
    if jours < 0:
        return {"etat": MESURE, "valeur": "jamais", "score": 0.0,
                "detail": "aucune phase aboutie ET revue par Elena — la chaîne "
                          "ne s'est jamais fermée de bout en bout"}
    return {"etat": PARTIEL, "valeur": f"{jours} j", "score": bareme(jours, bon=3, mauvais=14),
            "detail": "phase 'completed' portant un verdict d'Elena. Le journal de "
                      "déploiement de Jordan manque : la chaîne est prouvée jusqu'à la "
                      "revue, pas jusqu'au déploiement"}


def composante_produit():
    m = []
    inc = _incidents_ouverts()
    if inc["etat"] in ETATS_CALCULABLES:
        score = bareme(inc["nombre"], bon=0, mauvais=3)
        if inc.get("erreurs_log") is not None:
            # Les deux signaux comptent : une plateforme sans exécution en échec mais
            # qui déverse des CRITICAL n'est pas saine. On prend le moins bon des deux.
            score = min(score, bareme(inc["erreurs_log"], bon=0, mauvais=50))
        m.append(mesure("produit.incidents", "incidents ouverts (échecs > 24 h, logs)",
                        "produit", "plateforme.executions", "delivery", inc["etat"],
                        inc["valeur"], score, detail=inc["detail"],
                        partagee_avec=["objectifs.delivery.O2"]))
    else:
        m.append(inconnue("produit.incidents", "incidents ouverts (échecs > 24 h, logs)",
                          "produit", "plateforme.executions", "delivery", inc["detail"]))

    ch = _chaine_aboutie()
    if ch["etat"] in ETATS_CALCULABLES:
        m.append(mesure("produit.chaine", "jours depuis la dernière chaîne aboutie",
                        "produit", "plateforme.build_phases", "delivery", ch["etat"],
                        ch["valeur"], ch["score"], detail=ch["detail"],
                        partagee_avec=["objectifs.delivery.O3"]))
    else:
        m.append(inconnue("produit.chaine", "jours depuis la dernière chaîne aboutie",
                          "produit", "plateforme.build_phases", "delivery", ch["detail"]))

    m.append(inconnue("produit.livrabilite", "livrabilité — pages en ligne et parcours",
                      "produit", "absente.pages_publiees", "delivery",
                      "aucune URL ni marqueur de contenu déclaré dans le dispositif ; "
                      "un code 200 n'est pas une livraison (12/08)"))
    return m


# ═══════════════════════════════════════════════════════════════════════════════════
#  9. Composante TRÉSORERIE — 10 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Le relevé consolidé est une BORNE INFÉRIEURE, et il le dit lui-même : embeddings du
# RAG sans compteur, sessions de développement hors de toute base, GPU à relever à la
# main. L'écart constaté avec la facture réelle le 11/08 était d'environ 185 USD/mois.
#
# Conséquence sur la notation, et elle est stricte : **une borne inférieure ne prouve
# jamais le vert.** Elle peut prouver un dépassement — si le mesuré dépasse déjà la
# référence, le réel aussi — jamais une bonne tenue. La composante reste donc PARTIEL
# en permanence, et l'audit imprime ce que la source ne mesure pas.

REFERENCE_COMITE_USD_MOIS = 196   # SPEC §8, point ouvert n° 1 : 196 sur 253 de facture


def composante_tresorerie():
    sortie, motif = outil(["bin/couts-consolides.py", "--jours", "30", "--json"], DELAI_OUTIL)
    if sortie is None:
        return [inconnue("tresorerie.cout", "coût consolidé sur 30 j", "tresorerie",
                         "outil.couts", ENTREPRISE, motif)]
    try:
        d = json.loads(sortie)
    except json.JSONDecodeError:
        return [inconnue("tresorerie.cout", "coût consolidé sur 30 j", "tresorerie",
                         "outil.couts", ENTREPRISE, "sortie JSON illisible")]
    mesure_usd = float(d.get("mesure_usd") or 0)
    manquants = [p.get("poste", "?") for p in d.get("non_mesure", [])]
    # Le relevé additionne le comité (fichiers de session) et le pipeline (base
    # plateforme). Sans DEOS_RO_DSN, le second poste vaut zéro sans qu'aucune erreur
    # ne le dise : le total tombe, et la trésorerie passerait au vert parce qu'on ne
    # voit plus la dépense. C'est l'incident du 14/08 — « ce n'est pas une dépense
    # nulle, c'est un outil aveugle depuis cet environnement » — reconnu ici plutôt
    # que découvert une seconde fois.
    if not DSN_PLATEFORME:
        return [inconnue("tresorerie.cout", "coût consolidé sur 30 j", "tresorerie",
                         "outil.couts", ENTREPRISE,
                         f"relevé aveugle : DEOS_RO_DSN absent, le poste pipeline est "
                         f"compté à zéro. Le {mesure_usd:.2f} USD lu ne couvre que les "
                         f"fichiers de session du comité — ce n'est pas un total")]
    if mesure_usd <= 0:
        return [inconnue("tresorerie.cout", "coût consolidé sur 30 j", "tresorerie",
                         "outil.couts", ENTREPRISE,
                         "relevé à 0,00 USD — un compteur aveugle depuis cet environnement, "
                         "pas une dépense nulle (correctif du 14/08)")]
    return [mesure(
        "tresorerie.cout", "coût consolidé sur 30 j (borne inférieure)", "tresorerie",
        "outil.couts", ENTREPRISE, PARTIEL, f"{mesure_usd:.2f} USD",
        bareme(mesure_usd, bon=REFERENCE_COMITE_USD_MOIS, mauvais=REFERENCE_COMITE_USD_MOIS * 2),
        detail=f"référence {REFERENCE_COMITE_USD_MOIS} USD/mois · non mesuré : "
               + ", ".join(manquants[:4]))]


# ═══════════════════════════════════════════════════════════════════════════════════
#  10. Composante PIPELINE — 10 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# « Comptes qualifiés en base Salesforce », dit le contrat. Salesforce n'est pas
# interrogeable depuis le comité : ni binaire `sf`, ni identifiants — c'est pour cela
# que bin/sf-lead passe par une file relayée vers l'hôte. La vue qui l'exposerait,
# v_deos_salesforce_pipeline, a été proposée le 02/08 et n'a jamais été créée.
#
# On ne se rabat PAS sur v_deos_leads. Deux raisons, et la seconde suffit : la revue du
# 11/08 a montré qu'un lead s'y insère sans clé étrangère vers un signal entrant — cinq
# INSERT valaient 25 points ; et Sam a tranché le 10/08 que ce qui n'est pas dans
# Salesforce n'existe pas. Mesurer ailleurs serait mesurer autre chose en le nommant
# pipeline. INCONNU est la réponse honnête, avec la source à créer nommée.

def _pipeline_qualifie():
    lecture = plateforme(
        "SELECT count(*) FROM v_deos_salesforce_pipeline "
        "WHERE statut_qualification IS NOT NULL")
    if not lecture.ok:
        return {"etat": INCONNU, "valeur": None, "score": None,
                "detail": SOURCES["absente.salesforce"]["absente"] + f" [{lecture.motif}]"}
    n = lecture.un()
    return {"etat": MESURE, "valeur": n, "score": bareme(n, bon=5, mauvais=0),
            "detail": "comptes qualifiés, source Salesforce"}


def composante_pipeline():
    p = _pipeline_qualifie()
    if p["etat"] in ETATS_CALCULABLES:
        return [mesure("pipeline.comptes", "comptes qualifiés en base Salesforce", "pipeline",
                       "absente.salesforce", "growth", p["etat"], p["valeur"], p["score"],
                       detail=p["detail"], partagee_avec=["objectifs.growth.O2"])]
    return [inconnue("pipeline.comptes", "comptes qualifiés en base Salesforce", "pipeline",
                     "absente.salesforce", "growth", p["detail"])]


# ═══════════════════════════════════════════════════════════════════════════════════
#  11. Composante RISQUES — 5 %
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Il n'existe pas de registre des risques. Ce qui existe, et qui se compte sans
# jugement, c'est ce qu'un programme constate à la place des agents :
#   · les alertes Preflight — une direction ne déclare pas qu'elle a ses moyens, le
#     Preflight les essaie ;
#   · les escalades hors délai — SPEC §4.3, mesurées à l'horloge ;
#   · les échéances réglementaires — et cette source-là n'existe pas, ce qui est le
#     risque ouvert le plus documenté du dispositif.

def composante_risques(avec_preflight=True):
    m = []
    if avec_preflight:
        sortie, motif = outil(["bin/preflight.py", "--toutes"], DELAI_PREFLIGHT)
        if sortie is None:
            m.append(inconnue("risques.preflight", "alertes Preflight ouvertes", "risques",
                              "outil.preflight", "chief-of-staff", motif))
        else:
            # LE COMPTAGE LIT `echecs`, ET LE FORMAT EST VÉRIFIÉ AVANT D'ÊTRE CRU.
            # Première version : `.get("alertes", [])` — une clé qui n'existe pas dans
            # la sortie du Preflight. Elle rendait 0 pendant que les quatre directions
            # étaient NOT_READY, sans la moindre erreur. C'est le zéro ambigu, dans le
            # code même du script qui existe pour l'interdire. D'où la vérification :
            # une ligne qui ne porte pas la forme attendue rend INCONNU, jamais zéro.
            alertes, directions_hs, formats_lus = 0, [], 0
            for ligne in sortie.strip().split("\n"):
                if not ligne.strip():
                    continue
                try:
                    o = json.loads(ligne)
                except json.JSONDecodeError:
                    continue
                if "statut" not in o or "echecs" not in o:
                    continue
                formats_lus += 1
                alertes += len(o["echecs"])
                if o["statut"] == "NOT_READY":
                    directions_hs.append(o.get("direction", "?"))
            if formats_lus == 0:
                m.append(inconnue(
                    "risques.preflight", "alertes Preflight ouvertes", "risques",
                    "outil.preflight", "chief-of-staff",
                    "sortie du Preflight non reconnue — un format qui change en silence "
                    "ne doit pas se lire comme « aucune alerte »"))
            else:
                # Toute alerte Preflight est assignée au Chief of Staff (SPEC §3.1) :
                # c'est lui qui décide qui corrige. La compter chez la direction bloquée
                # reproduirait le paradoxe — « tu n'as pas les moyens, débrouille-toi ».
                detail = (f"{formats_lus} direction(s) contrôlée(s)"
                          + (f" · NOT_READY : {', '.join(directions_hs)}" if directions_hs
                             else " · toutes READY")
                          + " · assignées au CoS par construction (paradoxe du Preflight)")
                m.append(mesure("risques.preflight", "alertes Preflight ouvertes", "risques",
                                "outil.preflight", "chief-of-staff", MESURE, alertes,
                                bareme(alertes, bon=0, mauvais=6), detail=detail))
    else:
        m.append(inconnue("risques.preflight", "alertes Preflight ouvertes", "risques",
                          "outil.preflight", "chief-of-staff", "--sans-preflight demandé"))

    esc = comite(
        "SELECT count(*) FILTER (WHERE statut = 'propose_cloture' "
        "                        AND updated_at < now() - interval '24 hours'), "
        "       count(*) FILTER (WHERE statut = 'attente_sam' "
        "                        AND date < now() - interval '7 days') "
        "FROM decisions")
    reprises = comite(
        "SELECT count(*) FROM tasks WHERE statut = 'failed' AND retry_at < now()")
    if not esc.ok:
        m.append(inconnue("risques.escalades", "escalades et reprises hors délai", "risques",
                          "decisions.horloge", "chief-of-staff", esc.motif))
    else:
        cloture, attente = (int(x) for x in esc.lignes[0])
        oubliees = reprises.un() if reprises.ok else 0
        total = cloture + attente + oubliees
        m.append(mesure(
            "risques.escalades", "escalades et reprises hors délai", "risques",
            "decisions.horloge", "chief-of-staff", MESURE, total,
            bareme(total, bon=0, mauvais=8),
            detail=f"{cloture} clôture(s) en attente > 24 h · {attente} attente_sam > 7 j "
                   f"· {oubliees} reprise(s) échue(s) jamais relancée(s)"))

    m.append(inconnue("risques.echeances", "échéances réglementaires non couvertes", "risques",
                      "absente.echeances", ENTREPRISE,
                      SOURCES["absente.echeances"]["absente"]))
    return m


# ═══════════════════════════════════════════════════════════════════════════════════
#  12. Agrégation — et pourquoi la couverture s'imprime toujours
# ═══════════════════════════════════════════════════════════════════════════════════
#
# Poids du contrat. Dans une composante, les mesures pèsent également ; pour Objectifs,
# les douze objectifs pèsent également, ce qui donne un quart de la composante à chaque
# direction, quel que soit le nombre d'objectifs qu'on sait mesurer chez elle.
#
# Le poids d'une composante est réduit au prorata de ce qui s'y mesure : une composante
# dont la moitié des mesures est INCONNUE n'apporte que la moitié de son poids. Le score
# global est la moyenne pondérée sur le poids RÉELLEMENT mesuré, et la couverture — la
# somme de ces poids sur 100 — s'imprime à côté, toujours. Un score de 82 sur 40 % de
# couverture et un score de 82 sur 95 % ne disent pas la même chose ; les confondre
# serait rendre l'absence verte, ce qui est l'angle mort n° 5 de la revue du 11/08.

POIDS = {"execution": 30, "objectifs": 25, "produit": 20,
         "tresorerie": 10, "pipeline": 10, "risques": 5}

# En dessous de ce taux de couverture, AUCUN score global n'est rendu. Le détail par
# composante l'est toujours — ce qui est su reste lisible.
#
# Le motif est le défaut que ce lot corrige, dans sa forme la plus insidieuse : lors du
# premier essai à blanc, sans accès aux bases, une seule source répondait et le tableau
# affichait « SCORE 100,0/100 — couverture 10 % ». Le nombre était juste et la lecture
# fausse. Une moyenne sur un dixième du poids n'est pas une vue d'entreprise, et un
# lecteur pressé retient le 100, pas le 10 %.
#
# 50 % est un seuil de jugement, pas une mesure : c'est le point où la moitié du poids
# manque et où la moyenne peut être renversée par ce qu'on ne voit pas. À réexaminer
# quand les six sources absentes auront été créées.
SEUIL_COUVERTURE = 50.0

LIBELLES = {"execution": "Exécution", "objectifs": "Objectifs", "produit": "Produit",
            "tresorerie": "Trésorerie", "pipeline": "Pipeline", "risques": "Risques"}


def collecter(avec_preflight=True):
    return (composante_execution() + composante_objectifs() + composante_produit()
            + composante_tresorerie() + composante_pipeline()
            + composante_risques(avec_preflight))


def poids_unitaire(mesures, cle_composante):
    """Poids d'une mesure au sein de sa composante, mesurée ou non."""
    dans = [x for x in mesures if x["composante"] == cle_composante]
    return POIDS[cle_composante] / len(dans) if dans else 0.0


def agreger(mesures, filtre_direction=None):
    """Rend (score, couverture, détail par composante). Un seul calcul, deux usages.

    `filtre_direction` restreint aux mesures imputées à une direction. Le score par
    direction est donc le MÊME calcul que le global, sur un sous-ensemble — c'est ce
    que vérifie --coherence, et c'est pour ça que les deux sont comparables.
    """
    total_pondere, poids_mesure, poids_total, par_composante = 0.0, 0.0, 0.0, {}
    for c in POIDS:
        dans = [x for x in mesures if x["composante"] == c]
        if not dans:
            continue
        unitaire = POIDS[c] / len(dans)
        retenues = [x for x in dans
                    if filtre_direction is None or x["direction"] == filtre_direction]
        if not retenues:
            continue
        calculables = [x for x in retenues if x["etat"] in ETATS_CALCULABLES]
        pm = unitaire * len(calculables)
        pt = unitaire * len(retenues)
        poids_total += pt
        poids_mesure += pm
        if calculables:
            score_c = sum(x["score"] for x in calculables) / len(calculables)
            total_pondere += pm * score_c
        else:
            score_c = None
        par_composante[c] = {
            "poids": round(pt, 2), "poids_mesure": round(pm, 2),
            "score": round(score_c, 1) if score_c is not None else None,
            "mesures": retenues,
        }
    score = round(total_pondere / poids_mesure, 1) if poids_mesure else None
    couverture = round(100 * poids_mesure / poids_total, 1) if poids_total else 0.0
    return score, couverture, par_composante


def scores_par_direction(mesures):
    res = {}
    for d in DIRECTIONS + [ENTREPRISE]:
        s, c, _ = agreger(mesures, filtre_direction=d)
        if s is not None or any(x["direction"] == d for x in mesures):
            res[d] = {"score": s, "couverture": c}
    return res


def verifier_coherence(mesures):
    """Critère d'acceptation n° 3, vérifié par une identité, pas par une affirmation.

    Le global est la moyenne pondérée de toutes les mesures calculables. Les groupes
    (quatre directions + entreprise) partitionnent ces mesures. La moyenne pondérée des
    scores de groupe, repondérée par leur poids mesuré, doit donc redonner le global —
    au centième près, la tolérance ne couvrant que les arrondis d'affichage.
    """
    global_score, _, _ = agreger(mesures)
    numerateur, denominateur, lignes = 0.0, 0.0, []
    for d in DIRECTIONS + [ENTREPRISE]:
        s, _, comp = agreger(mesures, filtre_direction=d)
        pm = sum(c["poids_mesure"] for c in comp.values())
        if s is None or pm == 0:
            lignes.append((d, None, round(pm, 2)))
            continue
        numerateur += s * pm
        denominateur += pm
        lignes.append((d, s, round(pm, 2)))
    recompose = round(numerateur / denominateur, 1) if denominateur else None
    ecart = None if (recompose is None or global_score is None) else abs(recompose - global_score)
    return {"global": global_score, "recompose": recompose, "ecart": ecart,
            "coherent": ecart is not None and ecart <= 0.05, "lignes": lignes,
            "partition_complete": _partition_complete(mesures)}


def _partition_complete(mesures):
    """Aucune mesure ne doit être hors de tout groupe, ni dans deux groupes."""
    connus = set(DIRECTIONS) | {ENTREPRISE}
    orphelines = [x["cle"] for x in mesures if x["direction"] not in connus]
    return {"orphelines": orphelines, "ok": not orphelines}


# ═══════════════════════════════════════════════════════════════════════════════════
#  13. Sorties
# ═══════════════════════════════════════════════════════════════════════════════════

L = 78


def _etiquette(m):
    if m["etat"] == MESURE:
        return f"{m['score']:5.1f}"
    if m["etat"] == PARTIEL:
        return f"{m['score']:5.1f}~"
    return f"{m['etat']:>6}"


def sortie_texte(mesures, direction=None):
    score, couverture, comps = agreger(mesures, filtre_direction=direction)
    titre = "SANTÉ — " + (direction.upper() if direction else "DIGITAL·HUMANS")
    print("=" * L)
    print(f"{titre}   {date.today().isoformat()}".center(L))
    print("=" * L)
    if score is None:
        print("\n  SCORE : INCONNU — aucune source calculable.")
    elif couverture < SEUIL_COUVERTURE:
        print(f"\n  SCORE NON RENDU     couverture {couverture:.0f} % "
              f"(seuil {SEUIL_COUVERTURE:.0f} %)")
        print(f"  Le calcul donnerait {score:.1f} sur {couverture:.0f} % du poids : la part")
        print("  manquante suffirait à le renverser. Le détail par composante,")
        print("  lui, reste vrai — c'est là qu'il faut regarder.")
    else:
        print(f"\n  SCORE {score:.1f}/100     couverture {couverture:.0f} % "
              f"du poids mesurable")
    if 0 < couverture < 100:
        print("  Ce qui manque est listé ci-dessous en INCONNU. Une source absente")
        print("  n'est pas un feu vert : elle est retirée du calcul, et elle se voit.")
    for c, poids in POIDS.items():
        if c not in comps:
            continue
        bloc = comps[c]
        s = f"{bloc['score']:.1f}" if bloc["score"] is not None else "INCONNU"
        print("\n" + "-" * L)
        print(f"{LIBELLES[c].upper()}  {poids} %   score {s}"
              f"   mesuré {bloc['poids_mesure']:.1f}/{bloc['poids']:.1f} pt")
        print("-" * L)
        for m in bloc["mesures"]:
            val = "—" if m["valeur"] is None else str(m["valeur"])
            print(f"  {_etiquette(m)}  {m['libelle'][:52]:52} {val:>12}")
            print(f"          source : {m['source_libelle']}")
            print(f"          écrite par : {', '.join(m['ecrit_par'])}  [{m['attestation']}]")
            if m["detail"]:
                for bout in _plier(m["detail"], 66):
                    print(f"          {bout}")
    if direction is None:
        print("\n" + "=" * L)
        print("PAR DIRECTION — même calcul, restreint à ce qui lui est imputable")
        print("=" * L)
        for d, v in scores_par_direction(mesures).items():
            s = f"{v['score']:.1f}" if v["score"] is not None else "INCONNU"
            # Sous le seuil, le score d'une direction reste affiché — il sert au tri,
            # pas au jugement — mais il est marqué. Un chiffre nu à 40 % de couverture
            # se lirait comme un verdict.
            marque = "   ← à lire avec sa couverture" \
                if v["score"] is not None and v["couverture"] < SEUIL_COUVERTURE else ""
            print(f"  {d:16} {s:>7}   couverture {v['couverture']:3.0f} %{marque}")
        print("\n  Ces scores trient l'attention — « où regarder en premier ». Ils ne")
        print("  comparent pas des performances : deux directions ne sont pas mesurées")
        print("  sur le même nombre de sources vivantes, et la couverture le dit.")
    print("=" * L)


def _plier(texte, largeur):
    mots, ligne, out = texte.split(), "", []
    for mot in mots:
        if len(ligne) + len(mot) + 1 > largeur:
            out.append(ligne)
            ligne = mot
        else:
            ligne = f"{ligne} {mot}".strip()
    if ligne:
        out.append(ligne)
    return out


def sortie_json(mesures, avec_preflight):
    score, couverture, comps = agreger(mesures)
    print(json.dumps({
        "date": date.today().isoformat(),
        "genere": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        # `score` est nul tant que la couverture n'atteint pas le seuil : le cockpit ne
        # doit pas pouvoir afficher un chiffre que la sortie humaine refuse de rendre.
        # `score_brut` reste disponible pour qui veut suivre la série, en sachant.
        "score": score if couverture >= SEUIL_COUVERTURE else None,
        "score_brut": score,
        "couverture_pct": couverture,
        "seuil_couverture_pct": SEUIL_COUVERTURE,
        "avertissement": (
            f"Couverture {couverture:.0f} % < {SEUIL_COUVERTURE:.0f} % : aucun score "
            f"global n'est rendu. Le détail par composante reste valable."
            if couverture < SEUIL_COUVERTURE else
            "Score partiel : il ne porte que sur les sources calculables. Une "
            "composante INCONNUE n'est pas verte, elle est absente du calcul."
        ) if couverture < 100 else None,
        "composantes": {
            c: {"poids": POIDS[c], "score": comps[c]["score"],
                "poids_mesure": comps[c]["poids_mesure"],
                "mesures": [{k: v for k, v in m.items() if k != "composante"}
                            for m in comps[c]["mesures"]]}
            for c in comps},
        "directions": scores_par_direction(mesures),
        "coherence": {k: v for k, v in verifier_coherence(mesures).items() if k != "lignes"},
        "preflight_interroge": avec_preflight,
    }, ensure_ascii=False, indent=2))


def sortie_audit(mesures):
    """Critère d'acceptation n° 2 : chaque source nommée, avec qui l'écrit."""
    print("=" * L)
    print("AUDIT DES SOURCES — qui écrit la donnée sur laquelle on note".center(L))
    print("=" * L)
    print("\nRègle : une mesure n'est admise que si l'évalué ne peut pas déplacer sa")
    print("valeur seul. Quatre modes d'attestation, aucun autre n'existe dans le code :")
    print("  horloge  la base pose la valeur — un agent écrit un statut, pas l'heure")
    print("  tiers    un autre acteur l'écrit (Sam, le CEO, la plateforme, un programme)")
    print("  croisee  deux acteurs distincts sont nécessaires, imposé par la requête")
    print("  externe  l'artefact est vérifiable du dehors (page publiée, facture)")
    print("\nUne cinquième valeur existe — `declaration` — et elle est REFUSÉE à la")
    print("construction. C'est le mécanisme, et non la consigne, qui applique I3.")

    utilisees = {}
    for m in mesures:
        utilisees.setdefault(m["source"], []).append(m)
    for cle, src in SOURCES.items():
        prises = utilisees.get(cle, [])
        absente = src.get("absente")
        print("\n" + "-" * L)
        drapeau = "SOURCE ABSENTE" if absente else "en service"
        print(f"{cle}   [{drapeau}]")
        print(f"  donnée        {src['libelle']}")
        print(f"  emplacement   {src['ou']}")
        print(f"  écrite par    {', '.join(src['ecrit_par'])}")
        print(f"  attestation   {src['attestation']}")
        for bout in _plier(src.get("note") or absente or "", 60):
            print(f"                {bout}")
        if prises:
            print(f"  notée sur     {', '.join(sorted(x['cle'] for x in prises))}")
            for x in prises:
                if x["direction"] != ENTREPRISE and x["etat"] in ETATS_CALCULABLES:
                    conflit = _ecrit_par_l_evalue(x["direction"], src["ecrit_par"])
                    if conflit:
                        # Le cas qu'il ne faut pas taire : l'évalué écrit bien la
                        # donnée, et la mesure n'est admise que parce que la requête
                        # exige la concurrence d'un second acteur. Si ce prédicat
                        # disparaît un jour, l'admission tombe avec lui.
                        verdict = ("l'évalué écrit cette donnée — admis SEULEMENT par "
                                   "l'attestation croisée imposée dans la requête")
                    else:
                        verdict = "hors de portée de l'évalué"
                    print(f"      {x['direction']:14} → {verdict}")
    print("\n" + "=" * L)
    manquantes = [c for c, s in SOURCES.items() if s.get("absente")]
    print(f"{len(manquantes)} source(s) à créer avant que la vue soit complète :")
    for c in manquantes:
        print(f"  · {c:26} {SOURCES[c]['libelle']}")
    print("=" * L)


def sortie_coherence(mesures):
    r = verifier_coherence(mesures)
    print("=" * L)
    print("COHÉRENCE — le score par direction et le global sont-ils le même calcul ?".center(L))
    print("=" * L)
    print("\n  groupe            score   poids mesuré")
    for d, s, pm in r["lignes"]:
        print(f"  {d:16} {('—' if s is None else f'{s:.1f}'):>6}   {pm:6.2f} pt")
    print(f"\n  global affiché        {r['global']}")
    print(f"  global recomposé      {r['recompose']}   (moyenne des groupes, pondérée)")
    print(f"  écart                 {r['ecart']}")
    print(f"\n  partition complète    {'oui' if r['partition_complete']['ok'] else 'NON'}"
          f"   {r['partition_complete']['orphelines'] or ''}")
    verdict = r["coherent"] and r["partition_complete"]["ok"]
    print("\n  " + ("COHÉRENT — les deux vues sortent du même calcul."
                    if verdict else "INCOHÉRENT — à corriger avant tout usage."))
    print("=" * L)
    return 0 if verdict else 1


# ═══════════════════════════════════════════════════════════════════════════════════
#  14. Autotest — la règle I3 se prouve, elle ne s'affirme pas
# ═══════════════════════════════════════════════════════════════════════════════════

def autotest():
    ok, ko = 0, []

    def cas(intitule, condition):
        nonlocal ok
        if condition:
            ok += 1
            print(f"  \033[32m✓\033[0m {intitule}")
        else:
            ko.append(intitule)
            print(f"  \033[31m✗\033[0m {intitule}")

    print("I3 — le constructeur refuse ce que la règle interdit")
    SOURCES["_essai_declaration"] = dict(
        libelle="rapport_delivery dans deos_state", ou="base comité",
        ecrit_par=["delivery"], attestation="declaration")
    try:
        mesure("essai", "auto-déclaré", "produit", "_essai_declaration", "delivery",
               MESURE, 100, 100.0)
        cas("une source auto-déclarée est refusée", False)
    except MesureInadmissible:
        cas("une source auto-déclarée est refusée", True)
    finally:
        del SOURCES["_essai_declaration"]

    SOURCES["_essai_tiers_menteur"] = dict(
        libelle="champ écrit par le Delivery mais déclaré tiers", ou="base comité",
        ecrit_par=["delivery"], attestation="tiers")
    try:
        mesure("essai", "tiers de façade", "produit", "_essai_tiers_menteur", "delivery",
               MESURE, 100, 100.0)
        cas("une direction notée sur un champ qu'elle écrit est refusée", False)
    except MesureInadmissible:
        cas("une direction notée sur un champ qu'elle écrit est refusée", True)
    finally:
        del SOURCES["_essai_tiers_menteur"]

    try:
        mesure("essai", "source anonyme", "produit", "source_qui_nexiste_pas", "delivery",
               MESURE, 1, 100.0)
        cas("une source absente du registre est refusée", False)
    except MesureInadmissible:
        cas("une source absente du registre est refusée", True)

    cas("l'attestation croisée reste possible (deux acteurs requis)",
        mesure("essai", "croisée", "execution", "tasks.valide_par", "chief-of-staff",
               MESURE, "1/1", 100.0)["score"] == 100.0)

    # Le contrôle doit reconnaître la direction sous TOUS ses noms. Sans la table
    # d'alias, `chief-of-staff` noté sur une donnée écrite par « cos » passait sans
    # que rien ne s'allume — l'évalué et l'écrivain étaient la même fonction.
    SOURCES["_essai_alias"] = dict(
        libelle="donnée écrite par le cos, déclarée tiers", ou="base comité",
        ecrit_par=["cos"], attestation="tiers")
    try:
        mesure("essai", "alias", "execution", "_essai_alias", "chief-of-staff",
               MESURE, 1, 100.0)
        cas("l'alias cos / chief-of-staff est reconnu", False)
    except MesureInadmissible:
        cas("l'alias cos / chief-of-staff est reconnu", True)
    finally:
        del SOURCES["_essai_alias"]

    SOURCES["_essai_alias_growth"] = dict(
        libelle="donnée écrite par le commercial, déclarée tiers", ou="base comité",
        ecrit_par=["commercial"], attestation="tiers")
    try:
        mesure("essai", "alias", "pipeline", "_essai_alias_growth", "growth", MESURE, 1, 100.0)
        cas("l'alias commercial / growth est reconnu (fusion SPEC §5)", False)
    except MesureInadmissible:
        cas("l'alias commercial / growth est reconnu (fusion SPEC §5)", True)
    finally:
        del SOURCES["_essai_alias_growth"]

    print("\nBarème — pas d'inversion, bornes tenues")
    cas("plus petit vaut mieux : 0 → 100", bareme(0, bon=0, mauvais=10) == 100.0)
    cas("plus petit vaut mieux : au-delà du seuil → 0", bareme(50, bon=0, mauvais=10) == 0.0)
    cas("plus grand vaut mieux : 4 → 100", bareme(4, bon=4, mauvais=0) == 100.0)
    cas("borné à [0,100]", 0 <= bareme(-99, bon=4, mauvais=0) <= 100)

    print("\nTri-état — l'absence ne vaut pas vert")
    faux = [
        mesure("a", "mesurée", "produit", "plateforme.executions", "delivery", MESURE, 1, 40.0),
        inconnue("b", "absente", "produit", "absente.pages_publiees", "delivery", "pas de source"),
    ]
    s, couv, _ = agreger(faux)
    cas("une mesure INCONNUE ne relève pas le score", s == 40.0)
    cas("elle réduit la couverture (50 %)", couv == 50.0)
    cas("une composante entièrement inconnue rend un score nul",
        agreger([inconnue("c", "x", "pipeline", "absente.salesforce", "growth", "-")])[0] is None)

    print("\nAgrégation — le global se recompose depuis les groupes")
    jeu = [
        mesure("d1", "x", "execution", "tasks.valide_par", "delivery", MESURE, 1, 80.0),
        mesure("d2", "y", "execution", "tasks.valide_par", "growth", MESURE, 1, 40.0),
        mesure("d3", "z", "produit", "plateforme.executions", "delivery", MESURE, 1, 60.0),
    ]
    r = verifier_coherence(jeu)
    cas("écart global / recomposé nul", r["coherent"])
    cas("aucune mesure orpheline", r["partition_complete"]["ok"])

    print("\nRegistre — toutes les sources sont exploitables")
    cas("aucune source du registre n'est en attestation 'declaration'",
        all(s["attestation"] != "declaration" for s in SOURCES.values()))
    cas("toute source absente porte son motif",
        all(s.get("absente") for s in SOURCES.values() if "absente." in _cle_de(s)))

    print()
    if ko:
        print(f"\033[31mAUTOTEST : {ok}/{ok + len(ko)}\033[0m")
        for k in ko:
            print(f"  · {k}")
        return 1
    print(f"\033[32mAUTOTEST : {ok}/{ok}\033[0m")
    return 0


def _cle_de(source_dict):
    for k, v in SOURCES.items():
        if v is source_dict:
            return k
    return ""


# ═══════════════════════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(
        description="Executive Health Score — LOT-10. Ne calcule que sur des sources "
                    "hors de portée de l'évalué (invariant I3).",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--direction", choices=DIRECTIONS + [ENTREPRISE],
                   help="restreint le calcul à ce qui est imputable à une direction")
    p.add_argument("--json", action="store_true", help="sortie machine, pour le cockpit")
    p.add_argument("--audit-sources", action="store_true",
                   help="chaque source, qui l'écrit, pourquoi elle est admise")
    p.add_argument("--coherence", action="store_true",
                   help="vérifie que score global et scores par direction sont un seul calcul")
    p.add_argument("--autotest", action="store_true",
                   help="éprouve I3, le barème, le tri-état et l'agrégation — sans base")
    p.add_argument("--sans-preflight", action="store_true",
                   help="n'appelle pas bin/preflight.py")
    args = p.parse_args()

    if args.autotest:
        return autotest()

    mesures = collecter(avec_preflight=not args.sans_preflight)

    if args.audit_sources:
        sortie_audit(mesures)
    elif args.coherence:
        return sortie_coherence(mesures)
    elif args.json:
        sortie_json(mesures, avec_preflight=not args.sans_preflight)
    else:
        sortie_texte(mesures, direction=args.direction)

    _, couverture, _ = agreger(mesures, filtre_direction=args.direction)
    return 0 if couverture >= 100 else 1


if __name__ == "__main__":
    sys.exit(main())
