#!/bin/bash
# Comité de direction hebdomadaire (lundi 08h00) — GATE 4 §7.2
set -euo pipefail
cd /workspace
TS=$(date -u +%Y-%m-%d)
CTX=$(mktemp)

fresh() {
  local ROW; ROW=$(psql "$COMITE_DB_DSN" -tA -c "SELECT extract(epoch FROM now()-updated_at)::int || '|' || valeur::text FROM deos_state WHERE cle='$1';")
  if [ -z "$ROW" ]; then echo "ABSENT"
  else local AGE="${ROW%%|*}"; local VAL="${ROW#*|}"
    if [ "$AGE" -gt 86400 ]; then echo "PÉRIMÉ (il y a $((AGE/3600))h) :"; fi
    echo "$VAL"; fi
}
{
echo "# CONTEXTE DU COMITÉ HEBDO — $TS (UTC)"
echo ""; echo "## Rapports du matin (rondes du jour)"
for D in delivery commercial marketing cs cos; do echo "### rapport_$D"; fresh "rapport_$D"; echo ""; done
echo "## Référentiels"
echo "### okr_h2"; fresh okr_h2
echo "### objectifs_commerciaux"; fresh objectifs_commerciaux
echo "### cash_suivi"; fresh cash_suivi
echo "### priorites_semaine (semaine écoulée)"; fresh priorites_semaine
echo ""; echo "## Décisions (ouvertes + mouvements <7j)"
psql "$COMITE_DB_DSN" -tA -c "SELECT id||' | '||statut||' | '||origine||' | '||left(texte,80)||' | âge: '||(now()::date - date::date)||'j' FROM decisions WHERE statut NOT IN ('clos','refusee') OR updated_at > now()-interval '7 days' ORDER BY date;" | sed 's/^/- /'
echo ""; echo "## Briefs de la semaine écoulée (repères)"
ls -1 briefs/brief-2026-*.md 2>/dev/null | tail -6 | sed 's/^/- /'
} > "$CTX"

mkdir -p briefs
claude -p "$(cat ceo/prompt-ceo.md)

$(cat ceo/prompt-comite-hebdo.md)

$(cat "$CTX")

INSTRUCTION : préside le comité hebdo du $TS — déroule les quatre temps, écris le CR dans /workspace/briefs/comite-$TS.md et restitue-le." \
  --model claude-fable-5 \
  --allowedTools "Task,Bash,Read,Grep,Glob,Write" \
  --output-format json > "briefs/comite-$TS.meta.json" 2> "briefs/comite-$TS.err"
RC=$?
rm -f "$CTX"
echo "comité terminé RC=$RC — CR: briefs/comite-$TS.md"
