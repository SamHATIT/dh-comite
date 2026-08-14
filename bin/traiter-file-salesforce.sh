#!/bin/bash
# Traite la file des leads deposes par le Commercial depuis le conteneur.
#
# POURQUOI (14/08) : sf-lead appelait depuis le conteneur une route web qui
# n'a jamais existe. Verifie ce jour — le Commercial n'a pu creer aucun lead
# depuis le 11/08. Le binaire `sf` n'est present que sur l'hote, et le service
# web tourne lui aussi dans un conteneur.
#
# Ce script tourne sur l'HOTE, toutes les 5 minutes. Il lit la file, cree les
# leads, et deplace chaque demande dans traites/ ou echecs/ avec sa reponse.
# Rien n'est perdu : un echec reste consultable.
set -uo pipefail
cd /root/workspace/dh-comite/file-salesforce 2>/dev/null || exit 0
export PATH="$PATH:/usr/local/bin:/usr/bin"
ORG="${SF_ORG:-Production}"
DEPOT="/root/workspace/digital-humans-production"
N=0

for f in *.json; do
  [ -e "$f" ] || break
  JSON=$(cat "$f")
  VALEURS=$(python3 -c "
import json, sys
d = json.loads(sys.argv[1])
print(' '.join(f'{k}={json.dumps(str(v))}' for k, v in d.items()))
" "$JSON" 2>/dev/null) || { mv "$f" "echecs/$f"; echo "json illisible" > "echecs/$f.err"; continue; }

  R=$(cd "$DEPOT" && eval timeout 90 sf data create record --sobject Lead \
        --values "\"$VALEURS\"" --target-org "$ORG" --json 2>&1)
  if echo "$R" | grep -q '"status": *0'; then
    printf '%s\n' "$R" > "traites/$f.reponse"
    mv "$f" "traites/$f"
    N=$((N+1))
  else
    printf '%s\n' "$R" > "echecs/$f.err"
    mv "$f" "echecs/$f"
  fi
done
[ "$N" -gt 0 ] && echo "$(date -u +%F' '%T) : $N lead(s) crees" >> /var/log/file-salesforce.log
exit 0
