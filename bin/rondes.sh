#!/bin/bash
# Rondes des directeurs (cadence validée par Sam le 14/07) :
# Delivery 7j/7 ; CRO/CMO/CSM/CoS lun-ven. Parallèle, Sonnet.
set -uo pipefail

# FIX-BGWAIT-001 (06/08) : le CoS rendait la main en 14 s en annoncant le
# lancement de son subagent, dont le travail etait ensuite tue a 600 s
# ("Background tasks still running after 600s; terminating"). Son perimetre a
# grossi (33 decisions, rapprochement brief, page de suivi) : il lui faut plus.
# Plafond porte a 20 minutes — pas illimite, pour qu'un blocage reel soit vu.
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=1200000

cd /workspace
mkdir -p rondes
TS=$(date -u +%F)
DOW=$(date -u +%u)
run() {
  local AGENT="$1" EXTRA="$2"
  # CURSEUR-001 (06/08) : le curseur effectif est LU EN BASE et injecte dans le
  # prompt. Sans cela, une direction decrirait le texte fige de sa fiche, qui
  # pourrait diverger du reglage reellement applique par le garde-fou.
  local DIR_CURSEUR="${AGENT#directeur-}"
  local CURSEUR
  CURSEUR=$(/workspace/bin/curseur-lire "$DIR_CURSEUR" 2>/dev/null)
  [ -z "$CURSEUR" ] && CURSEUR="  (curseur indisponible — considere que tu es en OBSERVE sur tout)"
  export DH_DIRECTION="$DIR_CURSEUR"
  claude -p "TON CURSEUR D AUTONOMIE EFFECTIF, lu en base a l instant :
$CURSEUR

Ce reglage fait autorite : il est applique techniquement par le garde-fou avant chaque appel d outil. Si tu es bloque, rapporte le refus, ne le contourne pas.

Lance le subagent $AGENT pour sa ronde quotidienne complète (suis ton skill). Restitue son RapportDirecteur intégralement." \
    --model sonnet --allowedTools "Task,Bash,Read,Grep,Glob$EXTRA" \
    --output-format json > "rondes/$AGENT-$TS.json" 2> "rondes/$AGENT-$TS.err" &
}
run directeur-delivery ""
if [ "$DOW" -le 5 ]; then
  run directeur-commercial ""
  run directeur-customer-success ""
  run directeur-marketing ""
  run chief-of-staff ",Write"
  # FIX-LEGAL-001 (06/08) : le Directeur Juridique n'etait dans AUCUNE ronde.
  # Cree le 02/08 en "regime a la demande", il n'a jamais ete invoque — d'ou
  # deux missions accordees sans aucun livrable pendant quatre jours.
  # Il tourne desormais le LUNDI uniquement : son perimetre est ponctuel, une
  # ronde quotidienne serait du gaspillage. Il peut aussi etre invoque a la
  # demande par le CEO quand un sujet juridique surgit.
  # 08/08 (Sam) : passe en QUOTIDIEN le temps de la mise en conformite. Trois
  # chantiers l'attendent en parallele — validation du parcours client avant
  # mise en ligne, audit des deux sites vitrines jamais audites, et cadre de
  # securite des donnees clients (cloisonnement, chiffrement, engagement de
  # non-utilisation). A rebasculer sur le lundi seul quand ce sera termine.
  run directeur-legal ""
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
