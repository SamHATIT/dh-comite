#!/bin/bash
# Composeur de contexte + génération du daily brief (GATE 4 §7.1)
set -euo pipefail
cd /workspace
TS=$(date -u +%Y-%m-%d)
# Répartition validée par Sam le 14/07 : Opus en semaine, Fable le lundi (comité hebdo)
# Le lundi, le comité hebdo (comite.sh, 08h00) remplace le daily.
if [ "$(date -u +%u)" = "1" ]; then echo "lundi : daily remplacé par le comité hebdo (08h00)"; exit 0; fi
# REGLE (06/08) : toujours l'ALIAS, jamais une version datee. L'alias pointe
# vers la derniere version du modele — on beneficie des ameliorations sans
# rien changer, et on evite de payer une generation obsolete.
# Une version figee ne se justifie que pour reproduire un resultat a
# l'identique, et doit alors porter la raison en commentaire.
# COUT (11/08) : le brief tournait sur Opus quand les rondes des directeurs, qui
# font le travail d'analyse, tournent sur Sonnet. Personne n'avait arbitre cela.
# Mesure du 11/08 : 5,48 USD, dont 47% relecture de contexte, 33% sortie,
# 20% ecriture de cache. Bascule Sonnet : ~2,19 USD.
# Surchargeable pour un A/B : CEO_MODEL=haiku bin/daily.sh
CEO_MODEL=${CEO_MODEL:-sonnet}
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

# FIX-ARGLIST-001 (05/08) : le prompt complet passait en argument de commande et a
# depasse la limite du shell des que les 5 directions ont rapporte ("Argument list
# too long", brief perdu le 05/08). Il transite desormais par un fichier lu sur
# l'entree standard — aucune limite de taille.
PROMPT=$(mktemp)
{
  cat ceo/prompt-ceo.md
  echo ""
  cat "$CTX"
  echo ""
  echo "INSTRUCTION DU JOUR : produis le daily brief du $TS."
  echo "1. D'abord le bloc JSON brief_data (schéma Gate 1), stocké via :"
  echo "   echo '<json>' | /workspace/bin/deos-state set brief --par ceo"
  echo "2. Puis le Markdown complet (8 sections), écrit dans /workspace/briefs/brief-$TS.md"
  # COUT (11/08) : cette ligne demandait de restituer le brief ENTIER dans la
  # reponse, en plus du fichier deja ecrit — 26 Ko produits deux fois. Rien ne lit
  # cette reponse : alerte Telegram, dossier illustre et score de sante partent
  # tous du fichier ou de la base. Verifie avant suppression le 11/08.
  echo "3. Ne restitue PAS le Markdown dans ta réponse : le fichier fait foi."
  echo "   Termine par une seule ligne : sections écrites et nombre d'alertes hautes."
} > "$PROMPT"

cat "$PROMPT" | claude -p \
  --model "$CEO_MODEL" \
  --max-turns "${CEO_MAX_TURNS:-20}" \
  --allowedTools "Bash,Read,Grep,Glob,Write" \
  --output-format json > "briefs/daily-$TS.meta.json" 2> "briefs/daily-$TS.err"
RC=$?
rm -f "$CTX" "$PROMPT"
echo "daily terminé RC=$RC — brief: briefs/brief-$TS.md"

# FIX-ALERTE-BRIEF (05/08) : le brief a echoue silencieusement le 05/08 (Argument
# list too long) et personne n'a ete prevenu — l'alerte ne couvrait que les rondes.
# Desormais, un brief absent ou perime declenche une alerte Telegram immediate.
TOKEN_A=$(grep '^TELEGRAM_BOT_TOKEN=' /workspace/.env | cut -d= -f2)
CHAT_A=$(grep '^TELEGRAM_CHAT_ID=' /workspace/.env | cut -d= -f2)
FRAICHEUR=$(psql "$COMITE_DB_DSN" -tA -c "SELECT round(extract(epoch FROM now()-updated_at)/3600) FROM deos_state WHERE cle='brief';" 2>/dev/null)
if [ ! -f "briefs/brief-$TS.md" ] || [ "${FRAICHEUR:-999}" -gt 3 ]; then
  RAISON=$(tail -c 200 "briefs/daily-$TS.err" 2>/dev/null | tr '\n' ' ')
  if [ -n "${TOKEN_A:-}" ] && [ -n "${CHAT_A:-}" ]; then
    curl -s --max-time 15 "https://api.telegram.org/bot$TOKEN_A/sendMessage" -d chat_id="$CHAT_A" \
      --data-urlencode text="🔴 BRIEF NON PRODUIT ($TS) — les rondes ont peut-etre reussi, mais le brief a echoue.
Raison : ${RAISON:-inconnue}
Les rapports bruts restent consultables sur https://app.digital-humans.fr/comite/" > /dev/null
  fi
  echo "$TS ALERTE : brief non produit — $RAISON" >> briefs/incidents.log
fi

# Dossier illustre (format de reference) + notification Telegram courte
# ROBUSTESSE (07/08) : le script tourne avec set -e. Le 07/08, le generateur
# de dossier a plante (modules Python perdus a la recreation du conteneur) et
# a emporte la notification avec lui — Sam n'a rien recu alors que le brief
# etait produit. Desormais l'echec du dossier n'empeche plus la notification :
# on previent quand meme, en signalant que le document manque.
DOSSIER_OK=1
python3 /workspace/bin/dossier.py daily "$TS" > /tmp/dossier-path.txt 2>/tmp/dossier.err || DOSSIER_OK=0
DOC=$(cat /tmp/dossier-path.txt 2>/dev/null)
if [ "$DOSSIER_OK" = "0" ]; then
  echo "$TS ALERTE : dossier non genere — $(tail -1 /tmp/dossier.err 2>/dev/null)" >> briefs/incidents.log
fi

TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' /workspace/.env | cut -d= -f2)
CHAT=$(grep '^TELEGRAM_CHAT_ID=' /workspace/.env | cut -d= -f2)
if [ -n "${TOKEN:-}" ] && [ -n "${CHAT:-}" ]; then
  SANTE=$(/workspace/bin/deos-state get brief 2>/dev/null | jq -r '.sante.score // "?"')
  # 09/08 : le compteur unique melangeait DEUX choses tres differentes — les
  # decisions qui attendent l'arbitrage de Sam, et celles deja tranchees qui
  # attendent d'etre executees. Resultat affiche : 39, alors que Sam n'en a que
  # 10 a traiter. Ses decisions etaient noyees dans la masse.
  # Le CEO l'avait pourtant signale le 07/08 : « deux compteurs, jamais
  # additionnes ». On les separe donc a la source.
  NDEC=$(psql "$COMITE_DB_DSN" -tA -c "SELECT count(*) FROM decisions WHERE statut='attente_sam';" 2>/dev/null)
  NEXEC=$(psql "$COMITE_DB_DSN" -tA -c "SELECT count(*) FROM decisions WHERE statut IN ('accordee','en_execution');" 2>/dev/null)
  # Les trois plus anciennes en attente de Sam : pour qu'il voie QUOI, pas seulement COMBIEN.
  TOP3=$(psql "$COMITE_DB_DSN" -tA -c "SELECT '  · '||id||' — '||left(regexp_replace(texte, E'[\n\r]+', ' ', 'g'), 62) FROM decisions WHERE statut='attente_sam' ORDER BY date LIMIT 3;" 2>/dev/null)
  NALERTE=$(/workspace/bin/deos-state get brief 2>/dev/null | jq -r '[.alertes[]? | select((.gravite//"")|test("haute";"i"))] | length')
  MSG="Brief du $TS — sante $SANTE/100
Alertes hautes : ${NALERTE:-0}

A TON ARBITRAGE : ${NDEC:-0}
${TOP3:-  (aucune)}

Accordees, en attente d'execution : ${NEXEC:-0}
Brief lisible (HTML, presentable) :
https://app.digital-humans.fr/comite/brief/$TS
$(if [ "$DOSSIER_OK" = "1" ]; then
    echo "Dossier complet (graphiques, tableaux) :"
    echo "https://app.digital-humans.fr/comite/dossier/$(basename "${DOC:-brief-$TS.docx}")"
  else
    echo "ATTENTION : le dossier illustre n'a pas pu etre genere."
    echo "Le brief reste lisible ici : https://app.digital-humans.fr/comite/"
  fi)"
  curl -s --max-time 15 "https://api.telegram.org/bot$TOKEN/sendMessage" \
    -d chat_id="$CHAT" --data-urlencode text="$MSG" -o /tmp/tg.json
  if grep -q '"ok":true' /tmp/tg.json 2>/dev/null; then
    echo "notification Telegram envoyee"
  else
    # Sans cette trace, un echec de notification serait invisible : Sam ne le
    # decouvrirait qu'en constatant l'absence de brief, c'est-a-dire trop tard.
    echo "$TS ALERTE : notification Telegram ECHOUEE — $(head -c 200 /tmp/tg.json 2>/dev/null)" >> briefs/incidents.log
  fi
fi
