#!/usr/bin/env python3
"""Route un blocage vers sa suite : quelle action, et par qui.

POURQUOI CE FICHIER EXISTE (LOT-04, 17/08/2026).

Un blocage sans action suivante est invisible : il n'apparait dans aucune file,
personne ne le reprend, il ne repart jamais. La contrainte blocage_avec_suite
l'interdit en base, et deos-tasks le refuse avant. Mais interdire ne suffit pas :
il faut que la suite soit TROUVABLE, sinon l'agent bloque invente un
next_action pour satisfaire l'outil, et on obtient de la conformite sans effet.

Ce module tient la table de routage de SPEC §2.1 : selon la NATURE du blocage,
la suite et son porteur ne sont pas les memes. La distinction qui compte est
celle-ci — un agent prive de ses moyens NE PEUT PAS se debloquer lui-meme
(SPEC §3.1). Sans routage, on produit : « tu n'as pas les droits pour
travailler -> voici une tache -> obtiens les droits ». La suite doit alors
partir chez quelqu'un d'autre.

CE QUE CE MODULE N'EST PAS. Ce n'est pas un juge. Il ne decide pas si le
blocage est legitime, il ne note personne. Il lit le compte rendu de l'agent et
en deduit un ACHEMINEMENT. En cas de doute il ne devine pas : il route vers le
Chief of Staff, dont c'est precisement le mandat (SPEC §3.1).

Usage :
    diagnostic-blocage.py --texte "..." --owner delivery [--tache TASK-X] [--json]

Sortie par defaut, une ligne separee par des tabulations :
    nature<TAB>next_action<TAB>next_owner
"""

import argparse
import json
import re
import sys

# Les directions d'execution. Meme liste que bin/deos-tasks et bin/deos-decisions.
DIRECTIONS = ("commercial", "marketing", "delivery", "cs", "legal", "financier", "growth")

# Table de routage — SPEC §2.1, reprise telle quelle par LOT-04.
#
# L'ORDRE DES TESTS COMPTE, et il n'est pas alphabetique. On cherche d'abord ce
# que l'agent ne peut pas resoudre seul (permission, arbitrage, dependance),
# ensuite seulement ce qui lui revient (information, technique). Tester
# "technique" en premier attraperait presque tout : un refus de droit produit
# lui aussi une erreur, un message d'echec, parfois une trace. On classerait
# alors en technique un blocage que la direction ne peut pas lever, et on lui
# renverrait le travail — le defaut exact que le routage doit empecher.
ROUTAGE = {
    "permission": {
        "next_action": "verifier le Preflight et ouvrir le droit manquant",
        "next_owner": "chief-of-staff",
        # L'agent est prive de ses moyens : il ne peut pas se les rendre.
    },
    "decision": {
        "next_action": "escalade : arbitrage humain necessaire",
        "next_owner": "ceo",
        # ceo puis sam. Le CEO arbitre dans son mandat, Sam au-dela.
    },
    "dependance": {
        "next_action": "tache assignee a la direction dont depend le travail",
        "next_owner": None,  # rempli avec la direction detectee
    },
    "information": {
        "next_action": "recherche assignee : reunir l'information manquante",
        "next_owner": None,  # la direction elle-meme
    },
    "technique": {
        "next_action": "creer la tache corrective",
        "next_owner": None,  # la direction elle-meme
    },
    "indetermine": {
        "next_action": "qualifier le blocage et le reassigner",
        "next_owner": "chief-of-staff",
        # Le doute ne produit pas un silence : il produit un tri, par celui
        # dont c'est le mandat.
    },
}

# Indices textuels. Volontairement larges : rater un blocage de permission coute
# plus cher qu'en sur-detecter un. Un faux positif envoie la suite au CoS, qui
# la requalifie ; un faux negatif renvoie a l'agent un travail qu'il ne peut pas
# faire, et la tache tourne.
INDICES = {
    "permission": [
        r"\bpermission", r"\bdroits?\b", r"acc[eè]s refus", r"\bdenied\b", r"\bforbidden\b",
        r"lecture seule", r"read[- ]only", r"\b40[13]\b", r"non autoris", r"unauthorized",
        r"\bcredentials?\b", r"\btokens?\b", r"cl[eé] (?:api|manquante)", r"authentifica",
        r"pretooluse", r"bloqu[eé] par le hook", r"\bsudo\b", r"operation not permitted",
    ],
    "decision": [
        r"\barbitrage\b", r"\btrancher\b", r"faut-il", r"quelle option", r"je ne sais pas s[i']",
        r"\bsam doit\b", r"d[eé]cision (?:humaine|necessaire|n[eé]cessaire)", r"\bvalider avec\b",
        r"deux options", r"ambigu",
    ],
    "dependance": [
        r"\bd[eé]pend de\b", r"en attente (?:de|du|d')", r"\bbloqu[eé] par (?:le|la|l')",
        r"tant que .* n'a pas", r"il faut que .* fasse",
    ],
    "information": [
        r"introuvable", r"je ne trouve pas", r"information manquante", r"pas de donn[eé]es",
        r"aucune (?:source|trace|donn[eé]e)", r"\binconnu\b", r"\bmanque\b", r"non document",
    ],
    "technique": [
        r"\berreur\b", r"\bexception\b", r"traceback", r"\btimeout\b", r"\b[eé]chec\b",
        r"\bfailed\b", r"syntax", r"\bcrash", r"segmentation", r"\bstack\b", r"\btest[s]? (?:ko|rouge)",
        r"ne compile pas", r"\bbug\b",
    ],
}

ORDRE = ("permission", "decision", "dependance", "information", "technique")


def direction_citee(texte, sauf):
    """La direction mentionnee dans le texte, autre que celle qui est bloquee."""
    for d in DIRECTIONS:
        if d != sauf and re.search(r"\b" + re.escape(d) + r"\b", texte, re.I):
            return d
    return None


def diagnostiquer(texte, owner):
    t = texte or ""
    for nature in ORDRE:
        for motif in INDICES[nature]:
            if re.search(motif, t, re.I):
                route = dict(ROUTAGE[nature])
                if nature == "dependance":
                    autre = direction_citee(t, owner)
                    if autre is None:
                        # Une dependance dont on ne sait pas de qui elle depend
                        # n'est pas routable. Le CoS tranche — c'est son mandat,
                        # et c'est preferable a un renvoi a l'expediteur.
                        route = dict(ROUTAGE["indetermine"])
                        nature = "indetermine"
                    else:
                        route["next_owner"] = autre
                        route["next_action"] = (
                            "tache assignee a %s, dont depend le deblocage" % autre)
                elif route["next_owner"] is None:
                    route["next_owner"] = owner
                route["nature"] = nature
                route["motif_detecte"] = motif
                return route
    route = dict(ROUTAGE["indetermine"])
    route["nature"] = "indetermine"
    route["motif_detecte"] = None
    return route


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--texte", default=None, help="compte rendu de l'agent ; a defaut, stdin")
    p.add_argument("--owner", required=True, help="direction bloquee")
    p.add_argument("--tache", default="", help="identifiant de la tache, pour la trace")
    p.add_argument("--json", action="store_true", help="sortie JSON complete")
    a = p.parse_args()

    # UN --texte VIDE N'EST PAS UN --texte ABSENT. La premiere version testait la
    # verite de la chaine : `--texte ""` retombait donc sur stdin, qui n'est pas
    # redirige quand la boucle appelle ce script — le processus attendait
    # indefiniment. Or un compte rendu VIDE est precisement le cas que ce module
    # existe pour rattraper : l'agent qui s'arrete sans rien dire. Le mecanisme
    # cense attraper le silence se bloquait dessus. Constate le 17/08.
    if a.texte is not None:
        texte = a.texte
    elif not sys.stdin.isatty():
        texte = sys.stdin.read()
    else:
        texte = ""
    r = diagnostiquer(texte, a.owner)
    r["tache"] = a.tache

    if a.json:
        print(json.dumps(r, ensure_ascii=False))
    else:
        # Une ligne, separateurs tabulations : lisible par `IFS=$'\t' read`.
        # Les champs ne contiennent jamais de tabulation, ils sont construits ici.
        print("%s\t%s\t%s" % (r["nature"], r["next_action"], r["next_owner"]))


if __name__ == "__main__":
    main()
