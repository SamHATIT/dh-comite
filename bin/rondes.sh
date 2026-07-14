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
echo "$TS rondes terminées (DOW=$DOW)" >> rondes/rondes.log
