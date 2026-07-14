#!/bin/bash
# Composeur de contexte + génération du daily brief (GATE 4 §7.1)
set -euo pipefail
cd /workspace
TS=$(date -u +%Y-%m-%d)
# Répartition validée par Sam le 14/07 : Opus en semaine, Fable le lundi (comité hebdo)
# Le lundi, le comité hebdo (comite.sh, 08h00) remplace le daily.
if [ "$(date -u +%u)" = "1" ]; then echo "lundi : daily remplacé par le comité hebdo (08h00)"; exit 0; fi
CEO_MODEL=claude-opus-4-8
CTX=$(mktemp)

fresh() { # $1=cle : affiche le rapport avec son état de fraîcheur
  local ROW; ROW=$(psql "$COMITE_DB_DSN" -tA -c "SELECT extract(epoch FROM now()-updated_at)::int || '|' || valeur::text FROM deos_state WHERE cle='$1';")
  if [ -z "$ROW" ]; then echo "ABSENT — aucun rapport n'a jamais été produit pour ce domaine."
  else
    local AGE="${ROW%%|*}"; local VAL="${ROW#*|}"
    if [ "$AGE" -gt 86400 ]; then echo "PÉRIMÉ (dernière mise à jour il y a $((AGE/3600))h) — à traiter comme manquant, alertes hautes conservées avec leur date :"; fi
    echo "$VAL"
  fi
}

{
echo "# CONTEXTE DU DAILY — $TS (UTC)"
echo ""
echo "## B1. Rapports directeurs"
for D in delivery commercial marketing cs cos; do
  echo "### rapport_$D"; fresh "rapport_$D"; echo ""
done
echo "## B2. Décisions en cours (statut != clos)"
psql "$COMITE_DB_DSN" -tA -c "SELECT id||' | '||statut||' | '||origine||' | '||left(texte,80)||' | âge: '||(now()::date - date::date)||'j' FROM decisions WHERE statut NOT IN ('clos','refusee') OR updated_at > now()-interval '48 hours' ORDER BY date;" | sed 's/^/- /'
[ -z "$(psql "$COMITE_DB_DSN" -tA -c "SELECT 1 FROM decisions WHERE statut <> 'clos' LIMIT 1;")" ] && echo "(aucune décision ouverte)"
echo ""
echo "## B3. Brief J-1"
fresh brief
echo ""
echo "## B4. Curseurs et pondérations (agent_autonomy_map.yaml)"
cat config/agent_autonomy_map.yaml
echo ""
echo "## B6. Priorités de la semaine"
fresh priorites_semaine
} > "$CTX"

mkdir -p briefs
claude -p "$(cat ceo/prompt-ceo.md)

$(cat "$CTX")

INSTRUCTION DU JOUR : produis le daily brief du $TS.
1. D'abord le bloc JSON brief_data (schéma Gate 1), stocké via :
   echo '<json>' | /workspace/bin/deos-state set brief --par ceo
2. Puis le Markdown complet (8 sections), écrit dans /workspace/briefs/brief-$TS.md
3. Restitue aussi le Markdown dans ta réponse." \
  --model "$CEO_MODEL" \
  --allowedTools "Bash,Read,Grep,Glob,Write" \
  --output-format json > "briefs/daily-$TS.meta.json" 2> "briefs/daily-$TS.err"
RC=$?
rm -f "$CTX"
echo "daily terminé RC=$RC — brief: briefs/brief-$TS.md"
