#!/bin/bash
# GATE 4 §5 — garde-fou exécutable (PreToolUse). Exit 2 = blocage + raison.
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
LOG=/workspace/hooks.log
# ─────────────────────────────────────────────────────────────────────
# CURSEUR D'AUTONOMIE — lecture du réglage effectif (06/08/2026)
#
# Avant : les règles étaient FIGÉES dans ce script. Le curseur n'existait
# que comme texte dans les prompts — une convention, pas un dispositif.
# Maintenant : le blocage lit la valeur déclarée en base. Le réglage
# affiché au tableau de bord EST celui qui bloque. C'est ce qui rend la
# gouvernance démontrable et non plus seulement affirmée.
#
# Niveaux : 1 Observe · 2 Conseille · 3 Agit sous validation · 4 Autonomie
# Un blocage survient quand le niveau requis par l'action dépasse le
# niveau réglé pour cette direction et ce type de tâche.
# ─────────────────────────────────────────────────────────────────────

DIRECTION="${DH_DIRECTION:-inconnue}"
CURSEUR_CACHE=/tmp/curseurs.cache

# Le cache évite d'interroger la base à chaque appel d'outil. Rafraîchi
# toutes les 60 s : un changement de curseur prend effet en moins d'une minute.
charger_curseurs() {
    if [ ! -f "$CURSEUR_CACHE" ] || [ $(( $(date +%s) - $(stat -c %Y "$CURSEUR_CACHE" 2>/dev/null || echo 0) )) -gt 60 ]; then
        psql "$COMITE_DB_DSN" -tA -F'|' -c \
          "SELECT direction, type_tache, niveau FROM curseurs" > "$CURSEUR_CACHE" 2>/dev/null
    fi
}

# Renvoie le niveau réglé, ou 1 (le plus restrictif) si introuvable.
# Le défaut restrictif est délibéré : une direction sans curseur déclaré
# ne doit rien pouvoir faire, plutôt que tout.
niveau_curseur() {
    local tache="$1"
    charger_curseurs
    local n
    n=$(grep -E "^${DIRECTION}\|${tache}\|" "$CURSEUR_CACHE" 2>/dev/null | cut -d'|' -f3 | head -1)
    echo "${n:-1}"
}

# Bloque si le niveau réglé est inférieur au niveau requis par l'action.
verifier_curseur() {
    local tache="$1" requis="$2" libelle="$3"
    local regle
    regle=$(niveau_curseur "$tache")
    if [ "$regle" -lt "$requis" ]; then
        local nom_regle nom_requis
        case "$regle"  in 1) nom_regle="Observe";; 2) nom_regle="Conseille";; 3) nom_regle="Agit sous validation";; 4) nom_regle="Autonomie";; esac
        case "$requis" in 1) nom_requis="Observe";; 2) nom_requis="Conseille";; 3) nom_requis="Agit sous validation";; 4) nom_requis="Autonomie";; esac
        echo "$(date -Is) CURSEUR-DENY [$TOOL] $DIRECTION/$tache regle=$regle requis=$requis :: $CMD" >> "$LOG"
        echo "BLOQUÉ PAR LE CURSEUR D'AUTONOMIE — $libelle.
Ton curseur pour « $tache » est réglé sur « $nom_regle » ; cette action exige « $nom_requis ».
Prépare et propose, mais n'exécute pas. Rapporte ce refus dans ton rapport plutôt que de contourner." >&2
        exit 2
    fi
}

CMD=""
deny() { echo "$(date -Is) DENY [$TOOL] $1 :: $CMD" >> "$LOG"; echo "BLOQUÉ ($1) — rapporte ce refus au lieu de contourner." >&2; exit 2; }

if [ "$TOOL" = "Bash" ]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

  # ── Le curseur decide EN PREMIER. Les blocages en dur qui suivent restent
  # comme filet de securite : si la base est injoignable, on refuse quand meme.
  if echo "$CMD" | grep -qE 'systemctl|(^|[;&| ])(docker|kill|pkill|killall|reboot|shutdown)([ ]|$)'; then
      verifier_curseur "agir_production" 3 "action sur les services ou conteneurs de production"
  fi
  if echo "$CMD" | grep -qiE '\b(INSERT[[:space:]]+INTO|UPDATE|DELETE[[:space:]]+FROM|DROP|ALTER|TRUNCATE)\b'; then
      verifier_curseur "ecrire_base" 3 "ecriture en base de donnees"
  fi

  # ── DH-FS-001 (14/08) : PROTECTION DU SYSTEME DE FICHIERS ──────────────
  # Verifie ce jour a la demande de Sam : le garde-fou bloquait correctement
  # le SQL et les envois externes, et laissait passer TOUTES les destructions
  # de fichiers. `rm -rf /workspace` etait AUTORISE — comme `mv`, `find -delete`
  # ou vider un fichier par redirection. Une direction pouvait effacer la
  # configuration entiere du comite : fiches, offre, dossiers juridiques,
  # contenus. C'est la meme cause que DEC-2026-0811-02 : on controlait des
  # motifs SQL, jamais des effets sur le disque.
  #
  # Les chemins proteges sont ceux dont la perte serait irreversible.
  # /repo-delivery n'y figure PAS : c'est l'espace de travail du Delivery,
  # un clone dont la perte ne coute qu'un reclonage.
  ZONES_PROTEGEES='/workspace(/|[[:space:]]|"|$)|/repo(/|[[:space:]]|"|$)|/backlog|/prodlogs|/root/\.claude'

  # EXCEPTION DU 17/08 : la file de depot Salesforce n est pas une zone a
  # proteger, c est une BOITE AUX LETTRES. Le Commercial y a depose par erreur
  # un fichier contenant le texte « --help », a voulu le retirer, et le
  # garde-fou l en a empeche. Il a rapporte le refus sans le contourner — le
  # comportement attendu — mais il ne pouvait pas reparer sa propre erreur.
  # Celui qui depose doit pouvoir retirer.
  case "$CMD" in
    *file-salesforce*) ZONES_PROTEGEES='NE_CORRESPOND_A_RIEN_XYZZY' ;;
  esac

  # Destruction ou deplacement massif
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(rm|mv|shred|dd)([[:space:]])' \
     && echo "$CMD" | grep -qE "$ZONES_PROTEGEES"; then
      deny "DH-FS-001 destruction ou deplacement dans une zone protegee — passe par une decision"
  fi
  # Suppression en masse par find
  if echo "$CMD" | grep -qE 'find[[:space:]]' \
     && echo "$CMD" | grep -qE '\-delete|\-exec[[:space:]]+rm' \
     && echo "$CMD" | grep -qE "$ZONES_PROTEGEES"; then
      deny "DH-FS-001 suppression en masse dans une zone protegee"
  fi
  # Vidage par redirection.
  # CORRECTIF DU 17/08 : cette regle cherchait un « > » et un chemin protege
  # N IMPORTE OU dans la commande, sans regarder de quel COTE du chevron se
  # trouvait le chemin. Consequence : `cat /workspace/config/offre_dh.md >
  # /tmp/copie.md` etait refuse — une simple LECTURE. Cinq faux positifs
  # rapportes dans quatre directions le 17/08, dont le blocage du correctif de
  # securite RAG que Sam avait valide le 13/08.
  # On n examine desormais que la CIBLE de la redirection.
  CIBLE=$(echo "$CMD" | grep -oE '[^>]>[[:space:]]*[^[:space:];&|]+' | grep -oE '[^[:space:]>]+$' | head -1)
  if [ -n "$CIBLE" ] && ! echo "$CMD" | grep -q '>>' \
     && echo "$CIBLE" | grep -qE '^/workspace/(config|bin|\.claude)|^/repo/'; then
      deny "DH-FS-001 ecriture directe dans une zone protegee — utilise un editeur"
  fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])truncate' \
     && echo "$CMD" | grep -qE "$ZONES_PROTEGEES"; then
      deny "DH-FS-001 troncature dans une zone protegee"
  fi
  # Modification des droits ou du proprietaire
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(chmod|chown|chgrp)([[:space:]])' \
     && echo "$CMD" | grep -qE "$ZONES_PROTEGEES"; then
      verifier_curseur "modifier_dispositif" 4 "modification des droits sur une zone protegee"
  fi
  if echo "$CMD" | grep -qE '(curl|wget)[^|;]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|-d[[:space:]])|(^|[;&| ])(mail|sendmail|mutt|msmtp)([ ]|$)'; then
      verifier_curseur "envoyer_externe" 3 "envoi vers l exterieur"
  fi
  # DH-BUDGET-001 (06/08) : engagement de depense. Les directions doivent
  # chiffrer et faire approuver, jamais engager. Sans ce garde-fou, la regle
  # n existait que sur le papier.
  if echo "$CMD" | grep -qiE 'stripe|paddle|checkout\.session|api\.anthropic\.com/v1/messages|openai\.com/v1|generativelanguage\.googleapis|billing|subscription|/v1/(charges|payment)'; then
      verifier_curseur "engager_depense" 3 "engagement de depense ou appel a un service payant"
  fi
  if echo "$CMD" | grep -qE '(>|>>|cp[[:space:]]|mv[[:space:]]|tee[[:space:]])[^;|&]*(\.claude/(agents|hooks|skills)|/curseurs)'; then
      verifier_curseur "modifier_dispositif" 4 "modification du dispositif (prompts, garde-fous, curseurs)"
  fi

  # DH-DEL-001 : jamais toucher aux services/processus
  if echo "$CMD" | grep -qE 'systemctl[[:space:]]+(restart|stop|start|reload|kill|disable|enable|mask)'; then deny "DH-DEL-001 systemctl"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(kill|pkill|killall|reboot|shutdown|halt)([[:space:]]|$)'; then deny "DH-DEL-001 kill/reboot"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])docker([[:space:]]|$)'; then deny "DH-DEL-001 docker"; fi

  # DH-DEL-002 : prod en lecture seule — jamais les credentials applicatifs
  if echo "$CMD" | grep -qE 'DH_SecurePass|-U[[:space:]]*digital_humans([[:space:]]|$)|user=digital_humans'; then deny "DH-DEL-002 credentials prod interdits"; fi
  # FIX-GUARD-001 (04/08) : limites de mot obligatoires. Sans elles, 'updated_at',
  # 'deleted', 'last_updated' declenchaient le blocage — 5 rondes perdues le 04/08.
  if echo "$CMD" | grep -qiE '\b(INSERT[[:space:]]+INTO|UPDATE|DELETE[[:space:]]+FROM|DROP|ALTER|TRUNCATE|GRANT)\b' && echo "$CMD" | grep -qE 'DEOS_RO_DSN|172\.19\.0\.1'; then deny "DH-DEL-002 écriture prod"; fi

  # DH-CRO/CMO/CSM-001 : aucun envoi externe
  if echo "$CMD" | grep -qE '(curl|wget)[^|;]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|--form|-d[[:space:]]|-F[[:space:]])'; then deny "DH-x-001 envoi externe"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(mail|sendmail|mutt|msmtp)([[:space:]]|$)'; then deny "DH-x-001 email"; fi

  # DH-COS-002 : decisions uniquement via deos-decisions
  if echo "$CMD" | grep -qE 'psql' && echo "$CMD" | grep -qiE '\b(INSERT[[:space:]]+INTO|UPDATE|DELETE[[:space:]]+FROM)\b[^;]*\bdecisions\b'; then deny "DH-COS-002 decisions via deos-decisions uniquement"; fi

  # R14 : promotion de skills réservée à Sam
  if echo "$CMD" | grep -qE '(>|>>|cp[[:space:]]|mv[[:space:]]|tee[[:space:]])[^;|&]*\.claude/skills/'; then deny "R14 promotion de skill réservée à Sam"; fi
fi

if [ "$TOOL" = "Write" ] || [ "$TOOL" = "Edit" ]; then
  FP=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty'); CMD="$FP"
  if echo "$FP" | grep -qE '^/workspace/\.claude/skills/'; then deny "R14 promotion de skill réservée à Sam"; fi
  if echo "$FP" | grep -qE '^/prodlogs'; then deny "DH-DEL-002 prodlogs RO"; fi
fi
exit 0
