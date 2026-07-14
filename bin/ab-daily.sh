#!/bin/bash
# A/B unique Fable vs Opus sur contexte STRICTEMENT identique
set -euo pipefail
cd /workspace
TS=$(date -u +%Y-%m-%d)
CTX=/workspace/briefs/ab-context-$TS.md

fresh() {
  local ROW; ROW=$(psql "$COMITE_DB_DSN" -tA -c "SELECT extract(epoch FROM now()-updated_at)::int || '|' || valeur::text FROM deos_state WHERE cle='$1';")
  if [ -z "$ROW" ]; then echo "ABSENT — aucun rapport n'a jamais été produit pour ce domaine."
  else local AGE="${ROW%%|*}"; local VAL="${ROW#*|}"
    if [ "$AGE" -gt 86400 ]; then echo "PÉRIMÉ (il y a $((AGE/3600))h) :"; fi
    echo "$VAL"; fi
}
{
echo "# CONTEXTE DU DAILY — $TS (UTC) — second daily du jour (5 rapports)"
echo ""; echo "## B1. Rapports directeurs"
for D in delivery commercial marketing cs cos; do echo "### rapport_$D"; fresh "rapport_$D"; echo ""; done
echo "## B2. Décisions en cours (statut != clos et != refusee)"
psql "$COMITE_DB_DSN" -tA -c "SELECT id||' | '||statut||' | '||origine||' | '||left(texte,80)||' | âge: '||(now()::date - date::date)||'j' FROM decisions WHERE statut NOT IN ('clos','refusee') ORDER BY date;" | sed 's/^/- /'
echo ""; echo "## B3. Brief J-1 (celui du matin)"; fresh brief
echo ""; echo "## B4. Curseurs et pondérations"; cat config/agent_autonomy_map.yaml
echo ""; echo "## B6. Priorités de la semaine"; fresh priorites_semaine
} > "$CTX"

INSTR_COMMUNE="INSTRUCTION : produis le daily brief (second du jour, les 5 directeurs ont maintenant rapporté). Bloc JSON brief_data d'abord, puis le Markdown complet (8 sections) dans ta réponse."

for M in claude-fable-5 claude-opus-4-8; do
  SHORT=$(echo $M | cut -d- -f2)
  claude -p "$(cat ceo/prompt-ceo.md)

$(cat "$CTX")

$INSTR_COMMUNE
Écris le Markdown dans /workspace/briefs/brief-$TS-AB-$SHORT.md. NE stocke RIEN via deos-state (test A/B, le brief officiel du matin reste en place)." \
    --model $M --allowedTools "Bash,Read,Grep,Glob,Write" \
    --output-format json > "briefs/ab-$SHORT.meta.json" 2> "briefs/ab-$SHORT.err"
  echo "=== $M : RC=$? coût=$(jq -r .total_cost_usd briefs/ab-$SHORT.meta.json 2>/dev/null)"
done
