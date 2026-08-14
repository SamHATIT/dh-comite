#!/bin/bash
# A/B multi-fournisseurs sur les rondes de directeurs, contexte identique.
#
# Pourquoi ce script : ab-daily.sh compare deux modeles Anthropic sur le daily.
# Ici on compare Sonnet 5 a un modele tiers sur les rondes, qui sont le vrai
# poste de cout (delivery 20,81 + marketing 14,48 + CoS 17,61 = 52,90 USD/30j).
#
# CONTRAINTE DE HARNAIS : les rondes lancent des subagents via l outil Task.
# Seul un fournisseur qui parle le tool-calling au format Anthropic peut etre
# substitue par bascule de ANTHROPIC_BASE_URL. GLM-5.2 et Kimi K3 le font.
# GPT-5.6 Terra/Luna ne le font PAS : ils exigent un autre harnais.
#
# CONTRAINTE DE JURIDICTION : ne lancer QUE sur delivery, marketing et
# chief-of-staff. Le commercial, le CS et le juridique portent du pipeline
# nominatif — arbitrage Sam du 09/08, un fournisseur hors UE/US est exclu.
#
# Usage : bin/ab-modeles.sh            (temoin Sonnet seul, aucune cle requise)
#         GLM_KEY=xxx bin/ab-modeles.sh  (temoin + challenger GLM-5.2)
set -uo pipefail
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=1200000
cd /workspace
TS=$(date -u +%FT%H%M)
OUT=rondes/ab-$TS; mkdir -p "$OUT"

AGENTS="directeur-delivery directeur-marketing chief-of-staff"

lancer() {
  local AGENT="$1" ETIQ="$2" EXTRA=""
  [ "$AGENT" = "chief-of-staff" ] && EXTRA=",Write"
  local DIR_CURSEUR="${AGENT#directeur-}" CURSEUR
  CURSEUR=$(/workspace/bin/curseur-lire "$DIR_CURSEUR" 2>/dev/null)
  [ -z "$CURSEUR" ] && CURSEUR="  (curseur indisponible — considere que tu es en OBSERVE sur tout)"
  export DH_DIRECTION="$DIR_CURSEUR"
  claude -p "TON CURSEUR D AUTONOMIE EFFECTIF, lu en base a l instant :
$CURSEUR

Ce reglage fait autorite : il est applique techniquement par le garde-fou avant chaque appel d outil. Si tu es bloque, rapporte le refus, ne le contourne pas.

Lance le subagent $AGENT pour sa ronde quotidienne complète (suis ton skill). Restitue son RapportDirecteur intégralement.
TEST A/B — NE stocke RIEN via deos-state ni en base. Ta sortie est evaluee, pas publiee." \
    --model "$MODELE" --allowedTools "Task,Bash,Read,Grep,Glob$EXTRA" \
    --output-format json > "$OUT/$AGENT.$ETIQ.json" 2> "$OUT/$AGENT.$ETIQ.err"
  echo "  $AGENT [$ETIQ] cout=$(jq -r '.total_cost_usd // "?"' "$OUT/$AGENT.$ETIQ.json" 2>/dev/null) tours=$(jq -r '.num_turns // "?"' "$OUT/$AGENT.$ETIQ.json" 2>/dev/null)"
}

echo "== TEMOIN : Sonnet 5 =="
MODELE=sonnet
for A in $AGENTS; do lancer "$A" temoin & done; wait

if [ -n "${GLM_KEY:-}" ]; then
  echo "== CHALLENGER : GLM-5.2 =="
  export ANTHROPIC_BASE_URL="${GLM_BASE_URL:-https://api.z.ai/api/anthropic}"
  export ANTHROPIC_AUTH_TOKEN="$GLM_KEY"
  unset ANTHROPIC_API_KEY
  MODELE="${GLM_MODEL:-glm-5.2}"
  for A in $AGENTS; do lancer "$A" glm & done; wait
else
  echo "== CHALLENGER ignore : GLM_KEY absente =="
fi

echo; echo "== BILAN =="
for f in "$OUT"/*.json; do
  printf "%-46s %8s USD  %4s tours  %7s jetons sortie\n" "$(basename "$f")" \
    "$(jq -r '(.total_cost_usd//0)|.*100|round/100' "$f" 2>/dev/null)" \
    "$(jq -r '.num_turns // "?"' "$f" 2>/dev/null)" \
    "$(jq -r '[.modelUsage[]?.outputTokens]|add // 0' "$f" 2>/dev/null)"
done
echo "Sorties comparables : $OUT/"
