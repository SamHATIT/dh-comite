#!/bin/bash
# Rondes du comité — V2. LOT-08, 17/08/2026.
#
# CE QUE CA REMPLACE. Une ronde était un rapport d'état du monde : le directeur se
# réveillait, décrivait sa situation, et s'arrêtait. Les sorties allaient de 500 à
# 15 000 caractères, et l'essentiel s'y noyait — l'agent reprenait un contexte déjà
# connu, produisait des analyses que personne n'avait demandées, et concluait
# rarement sur un engagement. La cadence, elle, vivait en dur dans ce fichier sous
# forme de conditions sur le jour de la semaine.
#
# LA V2 TIENT EN TROIS CHANGEMENTS :
#
# 1. PREFLIGHT BLOQUANT EN AMONT. Un agent NOT_READY ne rentre pas dans la ronde,
#    et son alerte part au Chief of Staff — jamais à lui-même. Un agent privé de
#    ses moyens ne peut pas se les rendre (SPEC §3.1). Tranché le 18/08 : le
#    Preflight passe AVANT CHAQUE RONDE, pas une fois par jour — une passe
#    quotidienne laisserait une fenêtre d'une journée pendant laquelle un montage
#    perdu passe inaperçu, soit la durée exacte des pannes qu'il supprime.
#
# 2. CINQ QUESTIONS, PAS UN RAPPORT. Et la quatrième change tout : « quelle action
#    est-ce que j'entreprends maintenant ? » transforme la ronde en engagement
#    plutôt qu'en constat. L'agent la pose comme une TÂCHE, dont il rendra compte.
#
# 3. LA CADENCE EST DECLARATIVE. Elle est lue dans config/preflight.yaml via
#    `preflight.py --lister` — source unique, voir config/cadence.yaml pour le
#    motif. L'historique de ce fichier dit ce que coûte une cadence en dur : le
#    Juridique absent de toute ronde pendant quatre jours, le Financier pendant
#    douze, chaque fois parce qu'une fiche existait sans sa ligne de `if`.
#
# ─── incidents dont ce fichier garde la mémoire ──────────────────────────────
#
# FIX-BGWAIT-001 (06/08) : le CoS rendait la main en 14 s en annonçant le
# lancement de son subagent, dont le travail était ensuite tué à 600 s.
#
# FIX-BGWAIT-002 (14/08) : MÊME INCIDENT SUR LE DELIVERY, huit jours plus tard.
# Sa ronde a rendu la main en 14 s sur une promesse, son subagent a été tué à
# 1200 s. Le fichier de sortie annonçait pourtant subtype=success, is_error=false :
# l'échec n'était QUE dans le .err, que rien ne lisait. Conséquence — le CEO a
# compté la ronde comme absente, la santé globale est tombée à 25/100, et le brief
# de Sam portait en première ligne « silence de Delivery face à une relance
# personnelle ». Le travail avait eu lieu, il venait d'être jeté.
#
# FIX-LEGAL-001 (06/08) : le Juridique n'était dans AUCUNE ronde. Créé le 02/08 en
# régime « à la demande », jamais invoqué — deux missions accordées sans aucun
# livrable pendant quatre jours.
#
# FIX-FINANCIER-001 (14/08) : le Financier n'était dans AUCUNE ronde ni dans la
# table des curseurs. Il existait uniquement sous forme de fiche. Exactement le
# même défaut que FIX-LEGAL-001, huit jours plus tard. Deux décisions lui avaient
# été assignées le 13/08 avec échéance au 15/08 : il ne les aurait jamais vues.
#
# Ces deux derniers incidents sont la raison d'être de la cadence déclarative :
# une fonction absente d'un fichier de configuration se voit, une fonction absente
# d'un `if` ne se voit pas.
#
# Usage : rondes.sh [--simulation]

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE" || exit 1
BIN="$RACINE/bin"
SIMULATION=0
[ "${1:-}" = "--simulation" ] && SIMULATION=1

CADENCE_YAML="$RACINE/config/cadence.yaml"
lire_param() {  # $1 = chemin pointé, $2 = valeur par défaut
  python3 - "$CADENCE_YAML" "$1" "$2" <<'PY' 2>/dev/null || echo "$2"
import sys, yaml
try:
    d = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
    for k in sys.argv[2].split("."):
        d = d[k]
    print(d)
except Exception:
    print(sys.argv[3])
PY
}

PLAFOND_CAR=$(lire_param "ronde.plafond_caracteres" 3000)
MODELE=$(lire_param "ronde.modele" sonnet)
OUTILS=$(lire_param "ronde.outils" "Task,Bash,Read,Grep,Glob")
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=$(lire_param "ronde.plafond_attente_ms" 2400000)

TS=$(date -u +%F)
mkdir -p "$RACINE/rondes"
JOURNAL="$RACINE/rondes/rondes-$TS.log"
trace() { echo "$(date -u +%H:%M:%S) | $*" | tee -a "$JOURNAL"; }
esc() { printf "%s" "$1" | sed "s/'/''/g"; }

# ---------------------------------------------------------------------------
# Qui tourne aujourd'hui — lu, jamais codé
# ---------------------------------------------------------------------------
# `preflight.py --lister` rend « id  etat  cadence ». On ne retient que les
# quotidiennes. Les fonctions en veille gardent fiche, mandat et droits : seule
# leur cadence s'arrête (I2), et elles restent invocables à la demande.
ACTIVES=$(python3 "$BIN/preflight.py" --lister 2>/dev/null | awk '$3=="quotidienne"{print $1}')

if [ -z "$ACTIVES" ]; then
  trace "ARRET : aucune direction quotidienne lue dans config/preflight.yaml."
  trace "        Une liste vide et une configuration illisible se ressemblent —"
  trace "        on ne conclut pas « rien a faire » sans avoir pu lire."
  exit 1
fi

trace "=== rondes du $TS — directions quotidiennes : $(echo $ACTIVES | tr '\n' ' ')"

# La fiche de l'agent : <id>.md, sinon directeur-<id>.md. On VERIFIE qu'elle
# existe. Une fiche manquante est une panne, pas une ronde qu'on saute.
fiche_de() {
  local ID="$1"
  if   [ -f "$RACINE/.claude/agents/$ID.md" ];            then echo "$ID"
  elif [ -f "$RACINE/.claude/agents/directeur-$ID.md" ];  then echo "directeur-$ID"
  else return 1; fi
}

if [ "$SIMULATION" = "1" ]; then
  echo "--- simulation : rondes qui se tiendraient le $TS ---"
  for ID in $ACTIVES; do
    AGENT=$(fiche_de "$ID") && echo "  $ID  ->  $AGENT" || echo "  $ID  ->  FICHE MANQUANTE"
  done
  echo "--- fonctions sans cadence (fiches conservees, invocables a la demande) ---"
  python3 "$BIN/preflight.py" --lister 2>/dev/null | awk '$3!="quotidienne"{printf "  %s (%s, %s)\n", $1, $2, $3}'
  exit 0
fi

# ---------------------------------------------------------------------------
# Alerte Preflight — le paradoxe, SPEC §3.1
# ---------------------------------------------------------------------------
# L'alerte n'est jamais adressée à la direction en panne : elle ne peut pas se
# rendre ses propres moyens. preflight.py fournit déjà next_action et next_owner
# pour chaque échec ; on ne les recalcule pas, on les pose dans la file.
#
# Une alerte qui ne vit que dans un journal n'est pas une alerte, c'est une note.
# Elle devient donc une décision (la trace) et une tâche (l'assignation).
alerte_preflight() {
  local ID="$1" JSON="$2"
  local RESUME
  RESUME=$(printf '%s' "$JSON" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read() or "{}")
except Exception:
    d = {}
e = d.get("echecs", [])
print(" | ".join("%s: %s" % (x.get("controle",""), x.get("detail","")) for x in e[:4])[:400])
' 2>/dev/null)
  [ -z "$RESUME" ] && RESUME="preflight NOT_READY, detail illisible"

  local PROPRIETAIRE
  PROPRIETAIRE=$(printf '%s' "$JSON" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read() or "{}")
except Exception:
    d = {}
e = d.get("echecs", [])
print(e[0].get("next_owner","chief-of-staff") if e else "chief-of-staff")
' 2>/dev/null)
  [ -z "$PROPRIETAIRE" ] && PROPRIETAIRE="chief-of-staff"

  # Idempotence : une seule alerte par direction et par jour. Sans cela une
  # panne durable produirait une décision par ronde, et le registre deviendrait
  # illisible au moment précis où il doit servir.
  local DEJA
  DEJA=$(psql "$COMITE_DB_DSN" -tA -c "SELECT count(*) FROM decisions
    WHERE texte LIKE 'PREFLIGHT $(esc "$ID") %' AND date::date = current_date;" 2>/dev/null)
  if [ "${DEJA:-0}" != "0" ]; then
    trace "  alerte deja ouverte aujourd'hui pour $ID — pas de doublon"
    return 0
  fi

  local DEC
  DEC=$("$BIN/deos-decisions" add --origine "$ID" \
        --texte "PREFLIGHT $ID $TS — NOT_READY : $RESUME" 2>/dev/null | tail -1)
  if [ -z "$DEC" ]; then trace "  ECHEC de creation de l'alerte pour $ID"; return 1; fi

  "$BIN/deos-tasks" add --decision "$DEC" \
    --titre "Retablir la capacite de $ID" \
    --critere-fin "bin/preflight.py $ID sort en code 0" \
    --owner "$PROPRIETAIRE" --par "$ID" >>"$JOURNAL" 2>&1
  trace "  alerte $DEC creee, tache assignee a $PROPRIETAIRE"
}

# ---------------------------------------------------------------------------
# La ronde
# ---------------------------------------------------------------------------
TENUES=0; REFUSEES=0
IDS_TENUES=""   # les directions qui ont REELLEMENT tourne dans CETTE execution
for ID in $ACTIVES; do
  AGENT=$(fiche_de "$ID")
  if [ -z "${AGENT:-}" ]; then
    trace "--- $ID : FICHE MANQUANTE (.claude/agents/) — ronde non tenue"
    REFUSEES=$((REFUSEES+1)); continue
  fi

  # --- Preflight, avant chaque ronde -------------------------------------
  PF=$(python3 "$BIN/preflight.py" "$ID" 2>/dev/null)
  if [ $? -ne 0 ]; then
    trace "--- $ID : NOT_READY — la ronde NE SE TIENT PAS"
    alerte_preflight "$ID" "$PF"
    REFUSEES=$((REFUSEES+1)); continue
  fi

  trace "--- $ID : READY, ronde de $AGENT"
  CURSEUR=$("$BIN/curseur-lire" "$ID" 2>/dev/null)
  [ -z "$CURSEUR" ] && CURSEUR="  (curseur indisponible — considere que tu es en OBSERVE sur tout)"
  export DH_DIRECTION="$ID"
  EXTRA=$(python3 - "$CADENCE_YAML" "$ID" <<'PY' 2>/dev/null
import sys, yaml
try:
    d = yaml.safe_load(open(sys.argv[1], encoding="utf-8")) or {}
    print((d.get("outils_extra") or {}).get(sys.argv[2], ""))
except Exception:
    print("")
PY
)

  # L'INVITE DE RONDE. Cinq questions, et rien d'autre. Les interdits sont
  # explicites parce que l'implicite n'a pas suffi : la consigne « sois bref »
  # a produit des rapports de 15 000 caracteres.
  claude -p "TON CURSEUR D AUTONOMIE EFFECTIF, lu en base a l instant :
$CURSEUR

Ce reglage fait autorite : il est applique techniquement par le garde-fou avant
chaque appel d outil. Si tu es bloque, rapporte le refus, ne le contourne pas.

RONDE — $ID. Tu reponds a CINQ questions, dans cet ordre, et a rien d'autre.

  1. Ou suis-je par rapport a mes objectifs ?
  2. Qu'est-ce qui a avance depuis hier ? — A LIRE, PAS A SE SOUVENIR
  3. Qu'est-ce qui est bloque, et par quoi ?
  4. QUELLE ACTION EST-CE QUE J ENTREPRENDS MAINTENANT ?
  5. Quelle decision humaine m'est necessaire ?

LA DEUXIEME SE LIT, ELLE NE SE DEVINE PAS. Tu n'as aucune memoire d'hier : tu
ne peux donc pas savoir ce qui a avance sans le lire. Avant d'y repondre, lance :

  bin/deos-tasks list --owner $ID --statut propose_cloture
  bin/deos-decisions list --depuis hier

S'il n'y a rien, ECRIS-LE : « rien n'a avance depuis hier » est une reponse
juste et attendue. L'inventer ne l'est pas.

  Constat du 19/08 : lors du premier essai sur modele local, le Financier a
  ecrit que « le reporting quotidien des depenses a ete mis a jour ». Cela
  n'avait pas eu lieu. La question l'y poussait — il n'avait aucun moyen de
  savoir, et il a comble. Un modele moins capable comble davantage.

LA QUATRIEME N'EST PAS UNE PHRASE, C'EST UN ENGAGEMENT. Tu la poses comme une
tache, et tu en rendras compte demain :

  bin/deos-tasks add --decision <DEC-X> --titre \"...\" \\
                     --critere-fin \"<verifiable par une commande>\" --owner $ID

Un critere de fin se verifie : « la vue renvoie 0 ligne », pas « c'est ameliore ».

INTERDITS, explicitement :
  - le rapport d'etat du monde — on ne te demande pas de decrire la situation ;
  - la reprise du contexte deja connu — personne ne le relit ;
  - les analyses non demandees. Si une analyse est utile, elle devient une
    TACHE, pas un paragraphe.

Plafond : $PLAFOND_CAR caracteres. Au-dela, tu ecris un rapport, pas une ronde.

Pour la question 5, si un arbitrage humain est necessaire :
  bin/deos-decisions status <DEC-X> needs_decision --par $ID --question \"...\"" \
    --model "$MODELE" --allowedTools "$OUTILS$EXTRA" \
    --output-format json > "$RACINE/rondes/$AGENT-$TS.json" 2> "$RACINE/rondes/$AGENT-$TS.err" &
  TENUES=$((TENUES+1)); IDS_TENUES="$IDS_TENUES $ID"
done
wait

# ---------------------------------------------------------------------------
# Controle post-rondes
# ---------------------------------------------------------------------------
# FIX-BGWAIT-002 : une ronde tuee au plafond sort en subtype=success. Sans ce
# controle, l'echec reste invisible jusqu'a ce qu'un humain compare des tailles
# de fichiers. On mesure aussi la LONGUEUR — critere d'acceptation 3.
#
# ON NE PARCOURT QUE LES RONDES DE CETTE EXECUTION, pas toutes les directions
# actives. Constate le 17/08 : apres une execution ou aucune ronde ne s'est
# tenue, la passe de controle relisait les fichiers du tour precedent et
# rapportait « ceo : ronde de 4501 caracteres » — un rapport d'hier presente
# comme celui d'aujourd'hui. Un fichier qui existe ne prouve pas qu'un travail
# vient d'avoir lieu.
ECHECS=""
for ID in $IDS_TENUES; do
  AGENT=$(fiche_de "$ID") || continue
  F="$RACINE/rondes/$AGENT-$TS.json"
  [ -f "$F" ] || continue
  if [ ! -s "$F" ] || [ "$(jq -r '.is_error // false' "$F" 2>/dev/null)" = "true" ]; then
    RAISON=$(jq -r '.result // "sortie vide"' "$F" 2>/dev/null | head -c 90)
    ECHECS="$ECHECS\n• $AGENT : $RAISON"
    trace "  $ID : ronde EN ECHEC — $RAISON"
    continue
  fi
  LONG=$(jq -r '.result // ""' "$F" 2>/dev/null | wc -c)
  if [ "$LONG" -gt "$PLAFOND_CAR" ]; then
    # Avertissement, jamais un rejet : le travail a eu lieu. FIX-BGWAIT-002 a
    # montre ce que coute de jeter un travail fait.
    trace "  $ID : ronde de $LONG caracteres, au-dela du plafond de $PLAFOND_CAR"
  else
    trace "  $ID : ronde de $LONG caracteres"
  fi
done

# Le comite doit savoir dire quand il est muet.
if [ -n "$ECHECS" ]; then
  TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' "$RACINE/.env" 2>/dev/null | cut -d= -f2)
  CHAT=$(grep '^TELEGRAM_CHAT_ID=' "$RACINE/.env" 2>/dev/null | cut -d= -f2)
  if [ -n "${TOKEN:-}" ] && [ -n "${CHAT:-}" ]; then
    curl -s --max-time 15 "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id="$CHAT" \
      --data-urlencode text="🔴 RONDES EN ÉCHEC ($TS) — le comité sera partiel ce matin :$(printf "$ECHECS")" >/dev/null
  fi
fi

trace "=== $TENUES ronde(s) tenue(s), $REFUSEES non tenue(s) (preflight ou fiche) ==="

# controle-rondes.py compare les rapports produits a ceux attendus. Il n'a de sens
# que si une ronde s'est tenue : appele apres zero ronde, il conclut « toutes les
# rondes ont produit un rapport » — vrai au sens strict, et parfaitement trompeur.
# Constate le 17/08 : quatre rondes refusees par le Preflight, et un journal qui
# se terminait sur une ligne rassurante. On ne laisse pas un comite muet se lire
# comme un comite en bonne sante.
if [ "$TENUES" -gt 0 ]; then
  [ -x "$BIN/controle-rondes.py" ] && "$BIN/controle-rondes.py" "$TS" || true
else
  trace "COMITE MUET aujourd'hui : aucune ronde tenue. $REFUSEES alerte(s) en file."
  trace "Le controle des rapports n'est pas lance — il n'y a rien a controler."
fi
exit 0
