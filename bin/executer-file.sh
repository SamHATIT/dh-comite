#!/bin/bash
# Session d'EXECUTION d'une direction — distincte de sa ronde.
#
# POURQUOI (17/08) : constat de Sam. « On a validé plus de vingt décisions
# depuis une semaine, pas une des tâches n'est faite. » Verification faite :
# c'est en partie inexact — le Delivery a produit deux commits depuis le 15/08,
# le chiffrement des identifiants et la journalisation. Mais 40 decisions
# accordees ont plus de trois jours, sur 41 au total.
#
# LA CAUSE EST MECANIQUE, PAS COMPORTEMENTALE. Une ronde est un appel unique :
# le directeur se reveille, produit un rapport, traite au mieux une ou deux
# decisions, et s'arrete. C'est un rythme de REPORTING, pas d'EXECUTION. A deux
# taches tous les trois jours contre quarante en file, il faudrait deux mois.
#
# Ce script fait l'inverse : il prend UNE decision accordee, la fait traiter,
# et recommence tant qu'il reste du travail, du temps et du budget. Le rapport
# quotidien reste ou il est ; ceci vient apres.
#
# Usage : executer-file.sh <direction> [nombre max de decisions] [minutes max]
set -uo pipefail
cd /workspace

DIR="${1:?usage: executer-file.sh <direction> [max_decisions] [max_minutes]}"
MAX_DEC="${2:-4}"
MAX_MIN="${3:-45}"
TS=$(date -u +%F)
FIN=$(( $(date +%s) + MAX_MIN * 60 ))
JOURNAL="rondes/execution-$DIR-$TS.log"

CURSEUR=$(/workspace/bin/curseur-lire "$DIR" 2>/dev/null)
[ -z "$CURSEUR" ] && { echo "curseur introuvable pour $DIR"; exit 1; }
export DH_DIRECTION="$DIR"

echo "=== session d'execution $DIR — $(date -u +%H:%M) ===" >> "$JOURNAL"
N=0

while [ "$N" -lt "$MAX_DEC" ] && [ "$(date +%s)" -lt "$FIN" ]; do
  # La plus ANCIENNE decision accordee qui porte cette direction.
  # On prend la plus ancienne, pas la plus facile : sinon la file se trie
  # toute seule par confort et les dossiers lourds ne bougent jamais.
  DEC=$(psql "$COMITE_DB_DSN" -tAc "
    SELECT id FROM decisions
    WHERE statut = 'accordee' AND (origine = '$DIR' OR preuve::text ILIKE '%\"porteur\": \"$DIR\"%')
    ORDER BY date LIMIT 1;" 2>/dev/null | tr -d ' ')

  [ -z "$DEC" ] && { echo "file vide — rien a traiter" >> "$JOURNAL"; break; }

  echo "--- $DEC ($(date -u +%H:%M))" >> "$JOURNAL"

  claude -p "TON CURSEUR D AUTONOMIE EFFECTIF, lu en base a l instant :
$CURSEUR

Ce reglage fait autorite. Si tu es bloque, rapporte le refus, ne le contourne pas.

SESSION D EXECUTION — ce n'est pas ta ronde. Tu ne produis pas de rapport d'etat.

Traite la decision $DEC, et elle seule. Lis-la avec deos-decisions, fais le
travail qu'elle demande, et rends compte en TROIS lignes maximum :
  1. ce que tu as fait, verifiable
  2. ou (fichier, commit, table)
  3. termine / partiellement fait / bloque par quoi

Si le travail touche au code, tu ecris dans /repo-delivery sur la branche
delivery/correctifs, un commit par decision, avec la reference dans le message.

Si tu termines, passe la decision en clos avec la preuve :
  deos-decisions status $DEC clos --par $DIR --preuve '{...}'
Si tu es bloque, laisse-la accordee et DIS PAR QUOI. Un blocage nomme vaut
mieux qu'un silence — c'est ainsi qu'on a trouve que /repo etait en lecture
seule pendant trois jours." \
    --model sonnet --allowedTools "Task,Bash,Read,Grep,Glob" \
    --output-format json >> "$JOURNAL" 2>&1

  N=$((N+1))
  sleep 3
done

echo "=== $N decision(s) traitee(s) — $(date -u +%H:%M) ===" >> "$JOURNAL"
