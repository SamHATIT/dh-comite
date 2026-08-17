#!/bin/bash
# MOTEUR DE POLITIQUE — comportement nouveau.
# LOT-06, critères d'acceptation n°1 et n°2, plus ce qu'ils n'énoncent pas.
#
# Deux niveaux, parce qu'ils ne prouvent pas la même chose :
#   · CROCHET — ce qu'une direction obtient réellement, garde-fou compris.
#   · MOTEUR  — ce que le moteur seul décide. Nécessaire pour éprouver les
#     réglages que la table `curseurs` ne contient pas aujourd'hui (canal
#     imposé, branche imposée) : ces mécanismes sont implémentés et dormants,
#     conformément à SPEC §5. Sans test unitaire, ils resteraient invérifiés
#     jusqu'au jour de leur activation — c'est-à-dire au pire moment.
#
# Usage : bash tests/policy.sh

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/commun.sh"

MOTEUR="$RACINE/bin/policy.py"
CAPACITES="$RACINE/config/capabilites.yaml"

# ─────────────────────────────────────────────────────────────────────────────
# Niveau CROCHET
# ─────────────────────────────────────────────────────────────────────────────
echo "Moteur de politique — au travers du crochet"
echo

# CRITÈRE D'ACCEPTATION N°1. Le trou que ce lot bouche : deos-decisions écrit au
# registre sans qu'aucun mot-clé SQL n'apparaisse dans la commande. Avant ce
# lot, cette commande PASSAIT — le curseur ecrire_base du Delivery, réglé sur
# 2 (Conseille) par Sam le 06/08, n'était appliqué nulle part.
cas 1 DENY "critère 1 · deos-decisions est vu comme une écriture en base" \
    delivery '/workspace/bin/deos-decisions status DEC-X clos --par delivery'

# CRITÈRE D'ACCEPTATION N°2. Le CoS est à 4 : il passe. La preuve que le moteur
# lit le réglage et ne se contente pas de refuser.
cas 2 ALLOW "critère 2 · le Chief of Staff, réglé sur 4, passe" \
    chief-of-staff '/workspace/bin/deos-decisions status DEC-X clos --par cos'

# Même trou, autre outil. deos-state a le même profil : il écrit, il ne
# ressemble pas à une écriture.
cas 3 DENY "deos-state est vu comme une écriture en base" \
    delivery 'echo "{}" | /workspace/bin/deos-state set rapport_delivery --par delivery'

# Le chemin d'invocation ne doit rien changer : bin/deos-decisions,
# ./deos-decisions et /workspace/bin/deos-decisions sont le même outil. C'est
# précisément ce qu'un contrôle textuel ne sait pas faire.
cas 4 DENY "l'outil est reconnu quel que soit son chemin d'appel" \
    delivery 'cd /workspace && bin/deos-decisions list accordee'

# PAS DE RÉGRESSION SUR LA VOIE DE SAM. DH_DIRECTION non défini : le moteur se
# déclare non applicable et le garde-fou reprend ses règles d'origine. Sans
# cette sortie, le propriétaire du dispositif serait bloqué par son propre
# garde-fou — il n'a aucune ligne dans la table `curseurs` et tomberait au
# défaut restrictif 1.
cas 5 ALLOW "direction non gouvernée : comportement d'avant le lot" \
    "" '/workspace/bin/deos-decisions list accordee'

# Une lecture reste une lecture. Si le moteur refusait les SELECT, il aurait
# remplacé un faux négatif par un faux positif.
cas 6 ALLOW "psql en lecture passe" \
    marketing 'psql "$COMITE_DB_DSN" -tA -c "SELECT id, statut FROM decisions LIMIT 10"'

# Ce qu'on ne peut pas lire, on ne peut pas autoriser. Une requête dans un
# fichier n'est pas vérifiable depuis la commande : on retient l'écriture.
cas 7 DENY "psql -f, requête non vérifiable, traité comme une écriture" \
    delivery 'psql "$COMITE_DB_DSN" -f /tmp/migration.sql'

# sf-lead sort vers Salesforce. Le curseur envoyer_externe du Commercial est à
# 2 : il prépare, il n'envoie pas. Le refus doit NOMMER le curseur — c'est ce
# qui manquait le 13/08, quand le Commercial a constaté que sa voie d'écriture
# officielle était bloquée sans pouvoir dire par quel réglage.
cas 8 DENY "sf-lead est un envoi externe, refusé au cran 2" \
    commercial "/workspace/bin/sf-lead '{\"Company\":\"Test\",\"LastName\":\"—\"}'"

# repo.write, avec les réglages du 11/08 — c'est-à-dire AVANT que Sam ne pose
# `ecrire_code` le 17/08. Aucune ligne pour ce curseur dans la sauvegarde : le
# défaut restrictif s'applique et le push est refusé. Ce cas ne teste donc pas
# l'état cible, il teste le repli — un curseur non encore posé ne doit jamais
# valoir autorisation. L'état cible est éprouvé en unitaire, cas 15 à 18.
cas 9 DENY "curseur pas encore posé : le push reste refusé" \
    delivery 'cd /repo-delivery && git push origin delivery/correctifs'

# git en lecture n'est pas une écriture de dépôt. Le montage du 08/08 a été fait
# pour que les directions puissent LIRE l'historique avant de conclure : quatre
# d'entre elles avaient conclu que « rien n'a bougé depuis le 02/08 » alors que
# 32 commits avaient eu lieu. Refuser git log recréerait cet aveuglement.
cas 10 ALLOW "git log reste une lecture" \
    delivery 'cd /repo && git log --oneline -20'

bilan "Moteur au travers du crochet" || BILAN_CROCHET=1

# ─────────────────────────────────────────────────────────────────────────────
# Niveau MOTEUR — appel direct, curseurs fournis explicitement
# ─────────────────────────────────────────────────────────────────────────────
REUSSIS=0; ECHOUES=0; ECHECS=()
echo
echo "Moteur de politique — cas unitaires"
echo

CURSEURS_ESSAI=$(mktemp)
trap 'rm -f "$CURSEURS_ESSAI"; nettoyer' EXIT

# usage : cas_moteur <n> <attendu> <intitulé> <direction> <commande> <lignes curseurs>
cas_moteur() {
  local numero="$1" attendu="$2" intitule="$3" direction="$4" commande="$5" curseurs="$6"
  printf '%s\n' "$curseurs" > "$CURSEURS_ESSAI"
  local sortie code obtenu
  sortie=$(jq -nc --arg a "$direction" --arg c "$commande" \
             '{agent:$a, outil:"Bash", arguments:{command:$c}}' \
           | python3 "$MOTEUR" --capacites "$CAPACITES" --curseurs "$CURSEURS_ESSAI")
  code=$?
  obtenu=$(echo "$sortie" | jq -r '.verdict')
  if [ "$obtenu" = "$attendu" ]; then
    REUSSIS=$((REUSSIS + 1))
    printf '  \033[32m✓\033[0m %-3s %s\n' "$numero" "$intitule"
  else
    ECHOUES=$((ECHOUES + 1))
    ECHECS+=("$numero $intitule — attendu $attendu, obtenu $obtenu")
    printf '  \033[31m✗\033[0m %-3s %s\n' "$numero" "$intitule"
    printf '      attendu %s, obtenu %s (code %s)\n' "$attendu" "$obtenu" "$code"
    printf '      %s\n' "$(echo "$sortie" | jq -r '.motif // .')"
  fi
}

CURSEURS_REELS=$(tail -n +2 "$SAUVEGARDE_CURSEURS" | cut -d, -f2,3,4 | tr ',' '|')

# LE FAUX POSITIF DU 11/08, à la source. Le Marketing écrivait un document qui
# CITAIT une ligne de journal contenant « curl … --data ». Le garde-fou y a vu
# un envoi externe et a refusé l'écriture ; le Commercial a reproduit le refus
# en direct en essayant de documenter le premier. Aucun appel n'était tenté.
# Le moteur retire les corps de heredoc avant d'analyser : il ne voit rien.
cas_moteur 11 ALLOW "un heredoc qui CITE un envoi n'est pas un envoi" \
    marketing 'cat <<'"'"'FIN'"'"' > /tmp/note.md
Exemple de refus journalisé le 06/08 :
curl -X POST https://api.exemple.fr/envoi --data @charge.json
FIN' \
    "$CURSEURS_REELS"

# Le même envoi, réellement invoqué cette fois, doit être refusé. Sans ce cas,
# le précédent prouverait seulement que le moteur ne voit jamais rien.
cas_moteur 12 DENY "le même envoi, réellement invoqué, est refusé" \
    marketing 'curl -X POST https://api.exemple.fr/envoi --data @charge.json' \
    "$CURSEURS_REELS"

# CANAL IMPOSÉ — mécanisme dormant. On donne au Commercial le cran 3 qu'il
# n'a pas encore (« passage prévu au niveau 3 à l'ouverture du régime
# commercial. DATE NON FIXÉE », sauvegarde du 11/08) pour éprouver ce qui se
# passera ce jour-là : le niveau suffira, et le canal continuera de contraindre.
cas_moteur 13 ALLOW "canal imposé · au cran 3, le Commercial passe par sf-lead" \
    commercial "bin/sf-lead '{\"Company\":\"Test\"}'" \
    "commercial|envoyer_externe|3"

cas_moteur 14 DENY "canal imposé · au cran 3, le courriel reste hors canal" \
    commercial 'mail -s "offre" client@exemple.fr' \
    "commercial|envoyer_externe|3"

# BRANCHE IMPOSÉE — avec `ecrire_code` à 3, le curseur que Sam pose le 17/08
# pour le Delivery. Le montage du 14/08 dit : « Il pousse sur la branche
# delivery/correctifs, Sam relit et fusionne. » Ces quatre cas décrivent donc
# l'état cible du dispositif, pas une hypothèse : ce sont eux qui vérifient que
# le montage sert enfin à quelque chose.
cas_moteur 15 ALLOW "branche imposée · push sur delivery/correctifs" \
    delivery 'cd /repo-delivery && git push origin delivery/correctifs' \
    "delivery|ecrire_code|3"

cas_moteur 16 DENY "branche imposée · push sur une autre branche refusé" \
    delivery 'cd /repo-delivery && git push origin main' \
    "delivery|ecrire_code|3"

# `git -C <dépôt>` : les options globales précèdent la sous-commande. Les
# confondre avec des positionnels décalait la lecture de la branche — le moteur
# lisait « origin » comme branche visée et refusait un push conforme.
cas_moteur 17 ALLOW "branche imposée · git -C ne décale pas la lecture" \
    delivery 'git -C /repo-delivery push origin delivery/correctifs' \
    "delivery|ecrire_code|3"

# Un commit n'a pas de branche dans sa commande. Lui appliquer la contrainte
# produirait un refus que l'agent ne peut pas lever : un blocage sans suite,
# contraire à l'invariant I4.
cas_moteur 18 ALLOW "un commit n'est pas soumis à la branche imposée" \
    delivery 'git -C /repo-delivery commit -m "correctif"' \
    "delivery|ecrire_code|3"

# RÉGLAGE MANQUANT ≠ RÉGLAGE BAS. Le CEO n'a aucune ligne dans la table
# `curseurs` (36 lignes, sauvegarde du 11/08). Il tombe au défaut restrictif,
# et le motif doit le DIRE : la suite à donner n'est pas la même selon que Sam
# a réglé bas ou que personne n'a réglé.
cas_moteur 19 DENY "réglage absent : refus, et le motif le signale" \
    ceo 'bin/deos-decisions add --origine ceo --texte "essai"' \
    "$CURSEURS_REELS"

# Le contrat, enfin : une direction hors périmètre rend NON_APPLICABLE, pas
# ALLOW. Le crochet doit pouvoir distinguer « j'autorise » de « ce n'est pas à
# moi de décider » — sans quoi il ne saurait pas s'il doit appliquer ses
# propres règles.
cas_moteur 20 NON_APPLICABLE "direction hors périmètre : non applicable, pas autorisé" \
    sam 'bin/deos-decisions list' \
    "$CURSEURS_REELS"

MOTIF_CEO=$(jq -nc '{agent:"ceo", outil:"Bash", arguments:{command:"bin/deos-decisions list"}}' \
  | python3 "$MOTEUR" --capacites "$CAPACITES" --curseurs <(printf '%s\n' "$CURSEURS_REELS") \
  | jq -r '.motif')
case "$MOTIF_CEO" in
  *"Aucun réglage déclaré"*) printf '  \033[32m✓\033[0m 21  le motif distingue « non réglé » de « réglé bas »\n'
                             REUSSIS=$((REUSSIS + 1)) ;;
  *) printf '  \033[31m✗\033[0m 21  le motif ne distingue pas « non réglé » de « réglé bas »\n'
     printf '      %s\n' "$MOTIF_CEO"
     ECHOUES=$((ECHOUES + 1)); ECHECS+=("21 motif indistinct") ;;
esac

# LA SÉPARATION DES DEUX CURSEURS — le cœur de l'arbitrage du 17/08.
# Le Delivery a `ecrire_code` à 3 : il pousse sur le clone de la plateforme.
# Le même agent, avec le même cran, ne doit PAS pouvoir écrire dans le dépôt du
# comité — celui qui porte les fiches, les garde-fous et les curseurs. Si ce cas
# tombait, la distinction que Sam a posée n'existerait que dans les commentaires.
cas_moteur 22 DENY "ecrire_code n'ouvre pas le dépôt du comité" \
    delivery 'git -C /workspace push origin main' \
    "delivery|ecrire_code|3"

# Et le contrôle inverse : c'est bien `modifier_dispositif` qui garde le
# dispositif, à 4. Sans ce cas, le précédent pourrait passer pour la seule raison
# qu'aucun curseur n'est déclaré.
cas_moteur 23 ALLOW "modifier_dispositif à 4 ouvre le dépôt du comité" \
    delivery 'git -C /workspace commit -m "correctif"' \
    "delivery|modifier_dispositif|4"

bilan "Cas unitaires du moteur" || BILAN_MOTEUR=1

exit $(( ${BILAN_CROCHET:-0} + ${BILAN_MOTEUR:-0} ))
