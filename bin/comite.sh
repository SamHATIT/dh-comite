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
# 09/08 : le Financier est ajoute. Il ne tourne PAS en ronde quotidienne
# (rien a observer chaque jour, et 45 EUR/mois de plus serait paradoxal pour
# la direction chargee des couts) mais il est PRESENT au comite avec une
# position preparee — arbitrage de Sam.
for D in delivery commercial marketing cs cos financier; do echo "### rapport_$D"; fresh "rapport_$D"; echo ""; done
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
PROMPT=$(mktemp)
{
  cat ceo/prompt-ceo.md
  echo ""
  cat ceo/prompt-comite-hebdo.md
  echo ""
  cat "$CTX"
  echo ""
  echo "INSTRUCTION : préside le comité hebdo du $TS — déroule les quatre temps, écris le CR dans /workspace/briefs/comite-$TS.md et restitue-le."
} > "$PROMPT"

  # ESSAI DU 10/08 (arbitrage Sam 09/08) : le comite bascule sur OPUS 5 pour
  # une semaine, afin de comparer a conditions egales avec les comites Fable
  # precedents — memes outils, meme prompt, donnees reelles.
  #
  # POURQUOI CET ESSAI. Deux motifs. (1) Fable 5 est un "modele couvert" qui
  # EXIGE 30 jours de retention et interdit la retention zero ; Opus la permet.
  # (2) La justification du choix de Fable etait QUALITATIVE, jamais mesuree.
  #
  # UN REJEU DU 09/08 N'A RIEN PROUVE : Opus, disposant des memes outils, est
  # alle lire l'etat vivant au lieu du contexte fourni. Il a produit un vrai
  # comite du jour — avec, spontanement, un tableau de position contre le plan
  # d'exploitation que Fable n'avait jamais produit. Interessant, mais pas une
  # comparaison. D'ou cet essai en conditions reelles.
  #
  # A REVOIR APRES LE COMITE DU 10/08. Si Opus tient, on garde et on gagne la
  # retention zero. Sinon, revenir a claude-fable-5 (sauvegarde : comite.sh.pre-opus).
cat "$PROMPT" | claude -p \
  --model claude-fable-5 \
--allowedTools "Task,Bash,Read,Grep,Glob,Write" \
  --output-format json > "briefs/comite-$TS.meta.json" 2> "briefs/comite-$TS.err"
RC=$?
rm -f "$CTX" "$PROMPT"
echo "comité terminé RC=$RC — CR: briefs/comite-$TS.md"

# Dossier illustre (format de reference) + notification Telegram courte
python3 /workspace/bin/dossier.py comite "$TS" > /tmp/dossier-path.txt 2>/tmp/dossier.err
DOC=$(cat /tmp/dossier-path.txt 2>/dev/null)

TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' /workspace/.env | cut -d= -f2)
CHAT=$(grep '^TELEGRAM_CHAT_ID=' /workspace/.env | cut -d= -f2)
if [ -n "${TOKEN:-}" ] && [ -n "${CHAT:-}" ]; then
  SANTE=$(/workspace/bin/deos-state get brief 2>/dev/null | jq -r '.sante.score // "?"')
  # 10/08 : meme correctif que daily.sh, oublie ici. Le compteur unique
  # melangeait les decisions qui attendent SAM et celles deja tranchees qui
  # attendent les DIRECTEURS — 68 affichees alors que Sam n'en avait que 10.
  # Ses decisions etaient noyees dans le travail des autres.
  NDEC=$(psql "$COMITE_DB_DSN" -tA -c "SELECT count(*) FROM decisions WHERE statut='attente_sam';" 2>/dev/null)
  NEXEC=$(psql "$COMITE_DB_DSN" -tA -c "SELECT count(*) FROM decisions WHERE statut IN ('accordee','en_execution');" 2>/dev/null)
  NALERTE=$(/workspace/bin/deos-state get brief 2>/dev/null | jq -r '[.alertes[]? | select((.gravite//"")|test("haute";"i"))] | length')
  MSG="Comite du $TS — sante $SANTE/100
Alertes hautes : ${NALERTE:-0}

A TON ARBITRAGE : ${NDEC:-0}
Accordees, cote directeurs : ${NEXEC:-0}
Dossier complet (graphiques, tableaux) :
https://app.digital-humans.fr/comite/dossier/$(basename "${DOC:-comite-$TS.docx}")"
  curl -s --max-time 15 "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d chat_id="$CHAT" --data-urlencode text="$MSG" > /dev/null && echo "notification Telegram envoyee"
fi
