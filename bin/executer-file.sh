#!/bin/bash
# Boucle d'execution d'une direction — LOT-04, 17/08/2026.
#
# LA PHRASE QUI FONDE CE FICHIER :
#
#     « Je suis bloque » n'est pas une sortie de session.
#     C'est un evenement qui genere du travail.
#
# POURQUOI CETTE REECRITURE. La version precedente prenait une DECISION accordee,
# la faisait traiter, et recommencait. Elle avait deja le bon rythme — executer
# plutot que rapporter — mais il lui manquait le mecanisme de persistance. Le
# scenario qui ramene a la V1 restait ouvert : tache, difficulte, « je suis
# bloque », fin de session, rapport. Rien ne forcait la difficulte a produire
# autre chose qu'un constat.
#
# CE QUE CA REMPLACE. Le traitement decision par decision, ou un blocage se
# racontait en prose dans le journal et n'engendrait rien. Desormais la boucle
# travaille sur des TACHES, et surtout : elle RECONCILIE. Apres chaque appel,
# elle relit l'etat de la tache en base. Si l'agent n'a rien declare — parce
# qu'il s'est arrete, parce qu'il a expose son blocage sans le poser — la boucle
# le fait a sa place : diagnostic, next_action, next_owner. Un agent ne peut plus
# terminer sur une difficulte sans laisser de suite, meme en ne faisant rien.
#
# POURQUOI PAS `set -e`. Une erreur ne doit pas interrompre la boucle : ce serait
# le defaut corrige ici, reproduit au niveau du shell. Chaque etape gere son
# echec et on continue. C'est deliberé.
#
# Usage : executer-file.sh <direction> [max_taches] [max_minutes]

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE" || exit 1
BIN="$RACINE/bin"

# Modele : lu dans config/cadence.yaml (routage_modele), jamais code en dur.
# Ajoute le 18/08 — le modele etait ecrit ici, ce qui rendait impossible de
# router une validation autrement qu'une execution. Le defaut du fichier
# s'applique si la nature n'est pas declaree.
MODELE=$(sed -n 's/^ *execution: *\([a-z0-9.-]*\).*/\1/p' \
         /workspace/config/cadence.yaml 2>/dev/null | head -1)
MODELE="${MODELE:-sonnet}"

DIR="${1:?usage: executer-file.sh <direction> [max_taches] [max_minutes]}"
MAX_TACHES="${2:-5}"
MAX_MIN="${3:-45}"
FIN=$(( $(date +%s) + MAX_MIN * 60 ))

mkdir -p "$RACINE/rondes"
JOURNAL="$RACINE/rondes/execution-$DIR-$(date -u +%F).log"
trace() { echo "$(date -u +%H:%M:%S) | $*" | tee -a "$JOURNAL"; }

psqlq() { psql "$COMITE_DB_DSN" -tA -c "$1" 2>/dev/null; }
esc()   { printf "%s" "$1" | sed "s/'/''/g"; }
# Comparaison de flottants sans bc, qui n'est pas garanti present.
sup()   { awk -v a="$1" -v b="$2" 'BEGIN{exit !(a>b)}'; }

export DH_DIRECTION="$DIR"

trace "=== session d'execution $DIR — max $MAX_TACHES taches, $MAX_MIN min ==="

# ---------------------------------------------------------------------------
# La base doit repondre AVANT de conclure quoi que ce soit
# ---------------------------------------------------------------------------
# Constate en validation le 17/08 : base injoignable, toutes les requetes
# renvoient du vide, la boucle ne trouve aucune tache due et conclut
# « TERMINEE — 0 tache ». Une panne se lisait comme une file vide. C'est le pire
# des rapports : faux, rassurant, et indistinguable d'une vraie fin de session.
# On echoue donc bruyamment, et on sort en code 1.
if [ "$(psqlq "SELECT 1;")" != "1" ]; then
  trace "ARRET : base injoignable (COMITE_DB_DSN). Une file vide et une panne ne"
  trace "        se ressemblent que si personne ne verifie laquelle des deux c'est."
  exit 1
fi

CURSEUR=$("$BIN/curseur-lire" "$DIR" 2>/dev/null)

# ---------------------------------------------------------------------------
# Reprise — SPEC §2.3
# ---------------------------------------------------------------------------
# Les taches failed dont retry_at est depasse reviennent d'elles-memes. C'est ce
# qui distingue un moteur d'execution d'un ordonnanceur : sans cela, une tache
# bloquee en premier est oubliee pendant que les suivantes s'executent.
REPRISES=$(psqlq "SELECT count(*) FROM tasks WHERE owner='$(esc "$DIR")'
  AND statut='failed' AND retry_at IS NOT NULL AND retry_at <= now();")
trace "reprise : ${REPRISES:-0} tache(s) dont l'echeance de reprise est passee"

TRAITEES=""          # taches deja vues dans CETTE session, pour ne pas boucler
N=0
BUDGET_SESSION=0     # somme des budgets des taches traitees
CONSOMME_SESSION=0
ETAT_SESSION="TERMINEE"

# Escalade : bloque une tache au niveau superieur, avec un motif explicite.
# Une escalade n'est pas un refus : c'est une demande d'arbitrage a qui peut
# engager davantage. Elle se pose donc DANS la file, pas dans un journal.
escalader() {
  local TID="$1" MOTIF="$2" VERS="$3"
  "$BIN/deos-tasks" block "$TID" \
    --blocker "$MOTIF" \
    --next-action "arbitrage : $MOTIF" \
    --next-owner "$VERS" >>"$JOURNAL" 2>&1
  trace "  ESCALADE -> $VERS : $MOTIF"
}

while :; do
  # --- conditions d'arret : nombre, temps, budget -------------------------
  [ "$N" -ge "$MAX_TACHES" ] && { trace "plafond de $MAX_TACHES taches atteint"; break; }
  if [ "$(date +%s)" -ge "$FIN" ]; then
    trace "temps ecoule avant de prendre une nouvelle tache"
    ETAT_SESSION="TIMEBOX_EXPIRED"; break
  fi
  if sup "$CONSOMME_SESSION" "$(awk -v b="$BUDGET_SESSION" 'BEGIN{print b*1.1}')" ; then
    trace "budget de session depasse : $CONSOMME_SESSION USD pour $BUDGET_SESSION budgetes (tolerance 10 %)"
    ETAT_SESSION="TIMEBOX_EXPIRED"
    SUIV=$(psqlq "SELECT id FROM tasks WHERE owner='$(esc "$DIR")'
       AND statut IN ('a_faire','en_cours') ORDER BY cree_le, id LIMIT 1;")
    [ -n "$SUIV" ] && escalader "$SUIV" \
      "budget de session depasse ($CONSOMME_SESSION USD pour $BUDGET_SESSION)" "ceo"
    break
  fi

  # --- la PLUS ANCIENNE due, pas la plus facile ---------------------------
  # Sinon la file se trie toute seule par confort et les dossiers lourds ne
  # bougent jamais. On exclut ce qui a deja ete vu dans cette session, sans quoi
  # une tache qu'on vient de bloquer serait reprise indefiniment.
  EXCL=""
  [ -n "$TRAITEES" ] && EXCL="AND id NOT IN ($TRAITEES)"
  TID=$(psqlq "SELECT id FROM tasks
    WHERE owner='$(esc "$DIR")' $EXCL
      AND ( statut IN ('a_faire','en_cours')
         OR (statut='failed'  AND retry_at IS NOT NULL AND retry_at <= now())
         OR (statut='blocked' AND next_owner='$(esc "$DIR")') )
    ORDER BY cree_le, id LIMIT 1;")

  [ -z "$TID" ] && { trace "file vide — rien de du pour $DIR"; break; }

  TRAITEES="$TRAITEES${TRAITEES:+,}'$(esc "$TID")'"
  IFS='|' read -r TITRE CRITERE DECISION BUDGET_T <<<"$(psqlq "SELECT titre || '|' || critere_fin || '|' || decision_id || '|' || budget_usd FROM tasks WHERE id='$(esc "$TID")';")"
  trace "--- $TID : $TITRE"
  BUDGET_SESSION=$(awk -v a="$BUDGET_SESSION" -v b="${BUDGET_T:-0}" 'BEGIN{printf "%.4f", a+b}')

  # --- demarrage : refuse si la TACHE elle-meme est hors budget -----------
  "$BIN/deos-tasks" start "$TID" --par "$DIR" >>"$JOURNAL" 2>&1
  if [ $? -eq 3 ]; then
    trace "  tache hors budget — escalade sans execution"
    escalader "$TID" "budget de la tache depasse" "ceo"
    N=$((N+1)); continue
  fi

  # --- execution ----------------------------------------------------------
  SORTIE="$RACINE/rondes/.sortie-$TID.json"
  claude -p "TON CURSEUR D AUTONOMIE EFFECTIF, lu en base a l instant :
$CURSEUR

Ce reglage fait autorite. Si tu es bloque, rapporte le refus, ne le contourne pas.

SESSION D EXECUTION — ce n'est pas ta ronde. Tu ne produis pas de rapport d'etat.

TACHE $TID : $TITRE
CRITERE DE FIN (verifiable) : $CRITERE
Elle porte la decision $DECISION.

Fais le travail. Puis DECLARE le resultat — c'est obligatoire, et c'est la seule
chose qui compte : ce que tu ecris ici n'est pas lu, l'etat en base l'est.

  bin/deos-tasks done  $TID --evidence-type commit|fichier|base|url --evidence-ref <ref>
  bin/deos-tasks block $TID --blocker \"...\" --next-action \"...\" --next-owner <qui>
  bin/deos-tasks fail  $TID --erreur \"...\"

Si tu es bloque, tu poses block AVEC sa suite. Un blocage sans action suivante
est invisible : personne ne le reprend, il ne repart jamais. Si tu ne sais pas a
qui adresser la suite, mets chief-of-staff — c'est son mandat.

Si la tache demande un arbitrage humain, dis-le en une phrase claire : la boucle
l'escaladera." \
    --model "$MODELE" --allowedTools "Task,Bash,Read,Grep,Glob" \
    --output-format json >"$SORTIE" 2>>"$JOURNAL"

  TEXTE=$(jq -r '.result // .[]?.result // ""' "$SORTIE" 2>/dev/null | head -c 4000)
  COUT=$(jq -r '.total_cost_usd // 0' "$SORTIE" 2>/dev/null)
  case "$COUT" in ''|null|*[!0-9.]*) COUT=0 ;; esac
  CONSOMME_SESSION=$(awk -v a="$CONSOMME_SESSION" -v b="$COUT" 'BEGIN{printf "%.4f", a+b}')
  cat "$SORTIE" >>"$JOURNAL" 2>/dev/null; rm -f "$SORTIE"

  # --- RECONCILIATION — le coeur du lot ----------------------------------
  # On ne croit pas le compte rendu : on relit l'etat en base. Si l'agent n'a
  # rien declare, la boucle declare a sa place. C'est ce qui rend impossible la
  # sortie « je suis bloque, fin de session ».
  ETAT=$(psqlq "SELECT statut FROM tasks WHERE id='$(esc "$TID")';")
  case "$ETAT" in
    done|valide)
      trace "  DONE — preuve posee, $COUT USD"
      # propose_cloture quand TOUTES les taches de la decision sont finies.
      RESTE=$(psqlq "SELECT count(*) FROM tasks WHERE decision_id='$(esc "$DECISION")'
                     AND statut NOT IN ('done','valide');")
      STATUT_DEC=$(psqlq "SELECT statut FROM decisions WHERE id='$(esc "$DECISION")';")
      if [ "${RESTE:-1}" = "0" ] && [ "$STATUT_DEC" = "en_execution" -o "$STATUT_DEC" = "accordee" ]; then
        PREUVE=$(psqlq "SELECT json_build_object('taches', json_agg(json_build_object(
                   'id', id, 'type', evidence_type, 'ref', evidence_ref)))::text
                   FROM tasks WHERE decision_id='$(esc "$DECISION")';")
        "$BIN/deos-decisions" status "$DECISION" propose_cloture --par "$DIR" \
          --preuve "$PREUVE" >>"$JOURNAL" 2>&1 \
          && trace "  $DECISION -> propose_cloture (toutes ses taches sont finies)"
      fi ;;

    blocked|failed)
      # L'agent a declare lui-meme. La contrainte en base garantit deja que la
      # suite est renseignee — deos-tasks refuse avant, la base refuse ensuite.
      SUITE=$(psqlq "SELECT next_owner || ' : ' || next_action FROM tasks WHERE id='$(esc "$TID")';")
      trace "  ${ETAT^^} declare par l'agent — suite chez $SUITE" ;;

    *)
      # RIEN N'A ETE DECLARE. C'est exactement le scenario que ce lot ferme.
      if [ "$(date +%s)" -ge "$FIN" ]; then
        # TIMEBOX_EXPIRED : la tache retourne dans la file avec son avancement.
        # PAS un echec — on n'incremente pas attempt_count, on ne pose pas de
        # blocage. Elle reste en_cours et sera la plus ancienne due au prochain
        # tour. L'avancement vit dans le journal (voir docs, point ouvert).
        trace "  TIMEBOX_EXPIRED — $TID retourne dans la file, sans compter d'echec"
        ETAT_SESSION="TIMEBOX_EXPIRED"
        N=$((N+1)); break
      fi
      IFS=$'\t' read -r NATURE NEXT_ACTION NEXT_OWNER <<<"$("$BIN/diagnostic-blocage.py" \
        --owner "$DIR" --tache "$TID" --texte "$TEXTE" 2>/dev/null)"
      NATURE="${NATURE:-indetermine}"
      NEXT_ACTION="${NEXT_ACTION:-qualifier le blocage et le reassigner}"
      NEXT_OWNER="${NEXT_OWNER:-chief-of-staff}"
      RESUME=$(printf "%s" "$TEXTE" | tr '\n' ' ' | cut -c1-180)
      [ -z "$RESUME" ] && RESUME="l'agent n'a rien declare"

      if [ "$NATURE" = "technique" ]; then
        # Une tentative a eu lieu et a echoue : c'est failed, pas blocked.
        #
        # ON NE PASSE VOLONTAIREMENT NI --next-action NI --next-owner ICI. La SPEC
        # a DEUX tables de routage, pour deux choses differentes : §2.1 route un
        # BLOCAGE selon sa nature, §2.2 route un ECHEC selon le rang de la
        # tentative. Les confondre, comme le faisait la premiere version de cette
        # boucle, ecrasait la seconde par la premiere : une 2e tentative se voyait
        # poser « creer la tache corrective » au lieu de « changer d'approche,
        # cause a nommer », et l'operateur ne pouvait plus comprendre pourquoi la
        # tache avait cesse de revenir. deos-tasks tient §2.2 : on le laisse faire.
        "$BIN/deos-tasks" fail "$TID" --erreur "$RESUME" --cout "$COUT" >>"$JOURNAL" 2>&1
        SUITE=$(psqlq "SELECT attempt_count || ' essai(s), suite chez ' || next_owner || ' : ' || next_action FROM tasks WHERE id='$(esc "$TID")';")
        trace "  FAILED (non declare, diagnostic: $NATURE) — $SUITE"
        # Reprise suspendue : la tache ne reviendra pas tant que la cause n'est
        # pas nommee. Le dire ici, sinon elle disparait de la file en silence.
        if [ -z "$(psqlq "SELECT retry_at FROM tasks WHERE id='$(esc "$TID")';")" ]; then
          trace "  reprise SUSPENDUE — \`deos-tasks cause $TID --cause \"...\"\` la remet en file"
        fi
      else
        "$BIN/deos-tasks" block "$TID" --blocker "$RESUME" \
          --next-action "$NEXT_ACTION" --next-owner "$NEXT_OWNER" --cout "$COUT" >>"$JOURNAL" 2>&1
        trace "  BLOCKED (non declare, diagnostic: $NATURE) — suite chez $NEXT_OWNER"
      fi

      # NEEDS_DECISION : l'escalade cree l'entree attente_sam liee, pour que la
      # question arrive reellement a Sam au lieu de rester dans un journal.
      if [ "$NATURE" = "decision" ]; then
        STATUT_DEC=$(psqlq "SELECT statut FROM decisions WHERE id='$(esc "$DECISION")';")
        case "$STATUT_DEC" in
          accordee|en_execution)
            "$BIN/deos-decisions" status "$DECISION" needs_decision --par "$DIR" \
              --question "$(printf '%s' "$RESUME" | cut -c1-200)" >>"$JOURNAL" 2>&1 \
              && trace "  NEEDS_DECISION — $DECISION escaladee, entree attente_sam creee" ;;
          *) trace "  arbitrage deja en cours sur $DECISION ($STATUT_DEC)" ;;
        esac
      fi ;;
  esac

  N=$((N+1))
  sleep 2
done

# ---------------------------------------------------------------------------
# Garantie de fin de session — critere d'acceptation 2
# ---------------------------------------------------------------------------
# Aucune tache bloquee sans suite, jamais. La contrainte en base rend l'etat
# impossible ; on le VERIFIE quand meme, parce qu'un invariant qu'on n'observe
# jamais est un invariant qu'on croit tenu.
ORPHELINES=$(psqlq "SELECT count(*) FROM tasks
  WHERE statut IN ('blocked','failed')
    AND (blocker IS NULL OR next_action IS NULL OR next_owner IS NULL);")
trace "controle : ${ORPHELINES:-?} tache(s) bloquee(s) sans suite (attendu 0)"
[ "${ORPHELINES:-1}" != "0" ] && trace "ALERTE : invariant I4 viole — a corriger avant tout autre travail"

trace "=== $ETAT_SESSION — $N tache(s), $CONSOMME_SESSION USD pour $BUDGET_SESSION budgetes ==="
psqlq "SELECT '  reste du : ' || count(*) FROM tasks WHERE owner='$(esc "$DIR")'
  AND ( statut IN ('a_faire','en_cours')
     OR (statut='failed' AND retry_at IS NOT NULL AND retry_at <= now()) );" | tee -a "$JOURNAL"
exit 0
