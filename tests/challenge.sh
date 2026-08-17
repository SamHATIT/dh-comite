#!/bin/bash
# Suite d'acceptation du LOT-11 — mécanismes de challenge et Strategic Yield.
# 17/08/2026.
#
# POURQUOI UNE BASE JETABLE, ET PAS CELLE DU COMITÉ
# -------------------------------------------------
# Cette suite écrit des propositions et des challenges. Les passer dans la base du
# comité fabriquerait des lignes qui compteraient dans le Strategic Yield — un
# indicateur alimenté par ses propres tests mesure ses tests. C'est l'invariant I3
# rencontré par le côté le plus bête : non pas déclarer son résultat, mais le
# polluer. Le script REFUSE donc de tourner sur $COMITE_DB_DSN.
#
#   createdb challenge_test
#   CHALLENGE_TEST_DSN=postgresql:///challenge_test tests/challenge.sh
#
# La base est préparée automatiquement (migration du lot appliquée si les tables
# manquent). Les critères 1 à 5 de LOT-11 sont couverts, dans l'ordre du lot, plus
# ce que le lot exige sans le mettre en critère : le garde-fou EN BASE, l'ordre des
# quatre étapes, la reprise d'une proposition en veille, l'append-only.

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTIL="$RACINE/bin/challenge.py"
MIGRATION="$RACINE/migrations/2026-08-17-v2-challenge.sql"

DSN="${CHALLENGE_TEST_DSN:-}"
[ -n "$DSN" ] || {
  echo "CHALLENGE_TEST_DSN non définie." >&2
  echo "  createdb challenge_test && CHALLENGE_TEST_DSN=postgresql:///challenge_test $0" >&2
  exit 2
}
if [ -n "${COMITE_DB_DSN:-}" ] && [ "$DSN" = "$COMITE_DB_DSN" ]; then
  echo "REFUS: CHALLENGE_TEST_DSN pointe sur la base du comité." >&2
  echo "       Un test qui écrit là fabrique des propositions qui compteront" >&2
  echo "       dans le Strategic Yield." >&2
  exit 2
fi

export COMITE_DB_DSN="$DSN"
q() { psql "$DSN" -tAq -c "$1"; }

# Interrupteur de test : copie du fichier réel, jamais le fichier réel. Voir
# l'option --config de bin/challenge.py.
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
CONF="$TMP/activation.yaml"

interrupteur() {  # usage : interrupteur <hebdo> <strategic> <boucle>
  sed -e "s/^challenge_hebdomadaire:.*/challenge_hebdomadaire: $1/" \
      -e "s/^strategic_challenge:.*/strategic_challenge: $2/" \
      -e "s/^boucle_collective:.*/boucle_collective: $3/" \
      "$RACINE/config/activation.yaml" > "$CONF"
}

REUSSIS=0; ECHOUES=0; declare -a ECHECS
verifier() {  # usage : verifier <intitulé> <condition déjà évaluée : 0 ou 1>
  if [ "$2" = "0" ]; then
    REUSSIS=$((REUSSIS+1)); printf '  \033[32m✓\033[0m %s\n' "$1"
  else
    ECHOUES=$((ECHOUES+1)); ECHECS+=("$1"); printf '  \033[31m✗\033[0m %s\n' "$1"
  fi
}

# ── Préparation ─────────────────────────────────────────────────────────────────
if [ "$(q "SELECT count(*) FROM information_schema.tables WHERE table_name='propositions';")" != "1" ]; then
  psql "$DSN" -q -v ON_ERROR_STOP=1 -f "$MIGRATION" || {
    echo "migration non appliquée" >&2; exit 2; }
fi
# Remise à zéro. LES TROIS DÉCLENCHEURS append-only doivent être coupés, pas deux :
# un seul DELETE refusé fait échouer toute la transaction, la base reste peuplée du
# tour précédent, et les cas qui comptent des lignes échouent sans dire pourquoi.
# Constaté en écrivant cette suite — la table `avis` avait été oubliée.
psql "$DSN" -q -v ON_ERROR_STOP=1 -c \
  "ALTER TABLE avis         DISABLE TRIGGER trg_avis_no_delete;
   ALTER TABLE challenges   DISABLE TRIGGER trg_challenges_no_delete;
   ALTER TABLE propositions DISABLE TRIGGER trg_propositions_no_delete;
   DELETE FROM avis; DELETE FROM challenges; DELETE FROM propositions;
   ALTER TABLE avis         ENABLE TRIGGER trg_avis_no_delete;
   ALTER TABLE challenges   ENABLE TRIGGER trg_challenges_no_delete;
   ALTER TABLE propositions ENABLE TRIGGER trg_propositions_no_delete;" >/dev/null || {
  echo "remise à zéro impossible" >&2; exit 2; }

interrupteur essai inactif inactif

echo
echo "Garde-fous hors base"
"$OUTIL" --config "$CONF" --autotest >/dev/null 2>&1; verifier "--autotest passe" $?

echo
echo "Critère 1 — un challenge sans critère de réfutation est refusé"
SORTIE=$("$OUTIL" --config "$CONF" soumettre delivery \
           --hypothese "on sous-exploite le RAG" 2>&1); CODE=$?
[ "$CODE" = "2" ]; verifier "code 2 (REFUS, pas ERREUR)" $?
grep -q -- "--refutation" <<<"$SORTIE"; verifier "le champ manquant est nommé" $?
grep -q -- "--cout" <<<"$SORTIE"; verifier "les autres champs manquants aussi" $?
[ "$(q "SELECT count(*) FROM challenges;")" = "0" ]; verifier "rien n'est écrit" $?

echo
echo "Critère 2 — un challenge complet est accepté"
ID=$("$OUTIL" --config "$CONF" soumettre delivery \
       --hypothese "le RAG est sous-exploité sur les SDS" \
       --cout "2 jours" --refutation "si le rappel n'augmente pas, elle est fausse" 2>/dev/null)
[[ "$ID" == CHA-* ]]; verifier "un identifiant CHA- est rendu ($ID)" $?
[ "$(q "SELECT activation FROM challenges WHERE id='$ID';")" = "essai" ]
verifier "le régime d'essai est enregistré sur la ligne" $?

echo
echo "Le garde-fou est EN BASE, pas seulement dans l'outil"
psql "$DSN" -q -v ON_ERROR_STOP=1 -c \
  "INSERT INTO challenges (id, direction, hypothese, cout_experimentation, activation)
   VALUES ('CHA-CONTOURNEMENT','delivery','h','2 j','essai');" >/dev/null 2>&1
[ $? -ne 0 ]; verifier "un INSERT direct sans critère de réfutation est refusé" $?
psql "$DSN" -q -v ON_ERROR_STOP=1 -c \
  "INSERT INTO challenges (id, direction, hypothese, cout_experimentation,
                           critere_refutation, activation)
   VALUES ('CHA-VIDE','delivery','h','2 j','   ','essai');" >/dev/null 2>&1
[ $? -ne 0 ]; verifier "un critère rempli d'espaces est refusé aussi" $?

echo
echo "Critère 3 — l'interrupteur coupe bien le mécanisme"
interrupteur inactif inactif inactif
SORTIE=$("$OUTIL" --config "$CONF" collecter 2>/dev/null); CODE=$?
[ "$CODE" = "0" ]; verifier "collecter sort en 0" $?
[ -z "$SORTIE" ]; verifier "collecter n'affiche rien" $?
AVANT=$(q "SELECT count(*) FROM challenges;")
"$OUTIL" --config "$CONF" soumettre delivery --hypothese h --cout c --refutation r \
  >/dev/null 2>&1
[ "$(q "SELECT count(*) FROM challenges;")" = "$AVANT" ]
verifier "soumettre n'écrit rien quand le mécanisme est inactif" $?
interrupteur essai inactif inactif
"$OUTIL" --config "$CONF" collecter 2>/dev/null | grep -q "ATTENDU"
verifier "rallumé, collecter nomme les directions qui n'ont pas rendu" $?

echo
echo "Contradiction — spécifiée, donc implémentée"
"$OUTIL" --config "$CONF" contredire delivery --cible ceo --sujet "la priorité" \
  --preuve "trois incidents" >/dev/null 2>&1
[ $? = 2 ]; verifier "une contradiction sans alternative est refusée" $?
"$OUTIL" --config "$CONF" contredire delivery --cible ceo --sujet "la priorité" \
  --preuve "trois incidents" --alternative "inverser l'ordre" >/dev/null 2>&1
verifier "avec preuve et alternative, elle est enregistrée" $?
"$OUTIL" --config "$CONF" strategic >/dev/null 2>&1
[ $? = 0 ]; verifier "strategic inactif sort en 0 sans rien dire" $?

echo
echo "Critère 4 — le Strategic Yield suit une proposition sur ses quatre étapes"
P=$("$OUTIL" --config "$CONF" proposer --texte "basculer le comité sur matériel dédié" 2>/dev/null)
[[ "$P" == PROP-* ]]; verifier "proposition créée ($P)" $?
"$OUTIL" --config "$CONF" repondre "$P" --par ceo --reponse acceptee >/dev/null 2>&1
[ $? = 2 ]; verifier "le CEO ne peut pas accepter sa propre proposition (I3)" $?
"$OUTIL" --config "$CONF" etape "$P" --etape impact --texte "x" >/dev/null 2>&1
[ $? = 2 ]; verifier "l'impact avant le résultat est refusé" $?
"$OUTIL" --config "$CONF" repondre "$P" --par sam --reponse acceptee >/dev/null 2>&1
verifier "étape 1 — acceptée par Sam" $?
"$OUTIL" --config "$CONF" etape "$P" --etape experimentee \
  --evidence-type commit --evidence-ref abc1234 >/dev/null 2>&1
verifier "étape 2 — expérimentée, avec preuve" $?
"$OUTIL" --config "$CONF" etape "$P" --etape experimentee >/dev/null 2>&1
[ $? = 2 ]; verifier "sans preuve, l'étape est refusée" $?
"$OUTIL" --config "$CONF" etape "$P" --etape resultat --texte "coût divisé par deux" >/dev/null 2>&1
verifier "étape 3 — résultat" $?
"$OUTIL" --config "$CONF" etape "$P" --etape impact --texte "196 USD/mois -> 90" >/dev/null 2>&1
verifier "étape 4 — impact" $?
Y=$("$OUTIL" --config "$CONF" yield --json 2>/dev/null)
python3 -c "
import json,sys
y=json.loads('''$Y''')['strategic_yield']
sys.exit(0 if y['taux_acceptation']==100.0 and y['taux_impact']==100.0 else 1)"
verifier "les quatre taux se calculent" $?

echo
echo "Critère 5 — 14 jours sans réponse : UN rappel, puis la veille"
V=$("$OUTIL" --config "$CONF" proposer --texte "proposition laissée sans réponse" 2>/dev/null)
q "UPDATE propositions SET soumise_le = now() - interval '20 days' WHERE id='$V';" >/dev/null
"$OUTIL" --config "$CONF" yield --audit 2>/dev/null | grep -q "RAPPEL.*$V"
verifier "à 20 jours, un rappel est émis" $?
[ "$(q "SELECT rappele_le IS NOT NULL FROM propositions WHERE id='$V';")" = "t" ]
verifier "rappele_le est posé" $?
"$OUTIL" --config "$CONF" yield --audit 2>/dev/null | grep -q "RAPPEL.*$V"
[ $? -ne 0 ]; verifier "le rappel n'est émis QU'UNE FOIS" $?
q "UPDATE propositions SET rappele_le = now() - interval '8 days' WHERE id='$V';" >/dev/null
"$OUTIL" --config "$CONF" yield --audit 2>/dev/null | grep -q "VEILLE.*$V"
verifier "au-delà du délai, elle passe en veille" $?
Y=$("$OUTIL" --config "$CONF" yield --json 2>/dev/null)
python3 -c "
import json,sys
y=json.loads('''$Y''')['strategic_yield']
sys.exit(0 if y['en_veille_hors_calcul']==1 and y['taux_acceptation']==100.0 else 1)"
verifier "la veille sort du calcul : ni bonus, ni malus" $?
psql "$DSN" -q -v ON_ERROR_STOP=1 -c \
  "UPDATE propositions SET statut='en_veille', rappele_le=NULL WHERE id='$V';" >/dev/null 2>&1
[ $? -ne 0 ]; verifier "on ne met pas en veille sans avoir rappelé (contrainte)" $?
"$OUTIL" --config "$CONF" repondre "$V" --par sam --reponse acceptee >/dev/null 2>&1
verifier "une proposition en veille reste reprenable" $?
[ "$(q "SELECT statut FROM propositions WHERE id='$V';")" = "acceptee" ]
verifier "répondue, elle revient dans le calcul" $?

echo
echo "Boucle d'intelligence collective"
interrupteur essai inactif essai
"$OUTIL" --config "$CONF" avis "$P" delivery --verdict defavorable \
  --preuve "le socle n'est pas prêt" >/dev/null 2>&1
[ $? = 2 ]; verifier "un avis défavorable sans alternative est refusé (I4)" $?
"$OUTIL" --config "$CONF" avis "$P" delivery --verdict defavorable \
  --preuve "le socle n'est pas prêt" --alternative "attendre le 1er novembre" >/dev/null 2>&1
verifier "avec alternative, il est enregistré" $?
[ "$(q "SELECT axe FROM avis WHERE proposition_id='$P' AND direction='delivery';")" \
  = "techniquement réaliste" ]
verifier "l'axe vient de config/activation.yaml" $?
"$OUTIL" --config "$CONF" boucle "$P" --synthese 2>/dev/null | grep -q "defavorable"
verifier "la synthèse rend les avis" $?
interrupteur essai inactif inactif
AVANT=$(q "SELECT count(*) FROM avis;")
"$OUTIL" --config "$CONF" avis "$P" growth --verdict favorable --preuve "x" >/dev/null 2>&1
[ "$(q "SELECT count(*) FROM avis;")" = "$AVANT" ]
verifier "boucle inactive : aucun avis n'est enregistré" $?

echo
echo "Append-only — on n'efface pas ce qui fait un indicateur"
psql "$DSN" -q -v ON_ERROR_STOP=1 -c "DELETE FROM propositions WHERE id='$P';" >/dev/null 2>&1
[ $? -ne 0 ]; verifier "DELETE sur propositions est refusé" $?
psql "$DSN" -q -v ON_ERROR_STOP=1 -c "DELETE FROM challenges;" >/dev/null 2>&1
[ $? -ne 0 ]; verifier "DELETE sur challenges est refusé" $?

echo
TOTAL=$((REUSSIS+ECHOUES))
if [ "$ECHOUES" -eq 0 ]; then
  printf '\033[32mLOT-11 : %d/%d\033[0m\n' "$REUSSIS" "$TOTAL"; exit 0
fi
printf '\033[31mLOT-11 : %d/%d\033[0m\n' "$REUSSIS" "$TOTAL"
for e in "${ECHECS[@]}"; do printf '  · %s\n' "$e"; done
exit 1
