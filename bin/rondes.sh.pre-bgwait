#!/bin/bash
# Rondes des directeurs (cadence validée par Sam le 14/07) :
# Delivery 7j/7 ; CRO/CMO/CSM/CoS lun-ven. Parallèle, Sonnet.
set -uo pipefail
cd /workspace
mkdir -p rondes
TS=$(date -u +%F)
DOW=$(date -u +%u)
run() {
  local AGENT="$1" EXTRA="$2"
  claude -p "Lance le subagent $AGENT pour sa ronde quotidienne complète (suis ton skill). Restitue son RapportDirecteur intégralement." \
    --model sonnet --allowedTools "Task,Bash,Read,Grep,Glob$EXTRA" \
    --output-format json > "rondes/$AGENT-$TS.json" 2> "rondes/$AGENT-$TS.err" &
}
run directeur-delivery ""
if [ "$DOW" -le 5 ]; then
  run directeur-commercial ""
  run directeur-customer-success ""
  run directeur-marketing ""
  run chief-of-staff ",Write"
fi
wait

# Contrôle post-rondes : toute ronde en échec (crédit, erreur API, timeout) est signalée
# immédiatement sur Telegram. Le comité doit savoir dire quand il est muet.
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' /workspace/.env | cut -d= -f2)
CHAT=$(grep '^TELEGRAM_CHAT_ID=' /workspace/.env | cut -d= -f2)
ECHECS=""
for f in rondes/*-$TS.json; do
  [ -f "$f" ] || continue
  if [ ! -s "$f" ] || [ "$(jq -r '.is_error // false' "$f" 2>/dev/null)" = "true" ]; then
    RAISON=$(jq -r '.result // "sortie vide"' "$f" 2>/dev/null | head -c 90)
    ECHECS="$ECHECS\n• $(basename "$f" .json) : $RAISON"
  fi
done
if [ -n "$ECHECS" ] && [ -n "${TOKEN:-}" ] && [ -n "${CHAT:-}" ]; then
  curl -s --max-time 15 "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id="$CHAT" \
    --data-urlencode text="🔴 RONDES EN ÉCHEC ($TS) — le comité sera partiel ce matin :$(printf "$ECHECS")" > /dev/null
fi
echo "$TS rondes terminées (DOW=$DOW)$ECHECS" >> rondes/rondes.log
