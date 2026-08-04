#!/bin/bash
# GATE 4 §5 — garde-fou exécutable (PreToolUse). Exit 2 = blocage + raison.
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name // empty')
LOG=/workspace/hooks.log
CMD=""
deny() { echo "$(date -Is) DENY [$TOOL] $1 :: $CMD" >> "$LOG"; echo "BLOQUÉ ($1) — rapporte ce refus au lieu de contourner." >&2; exit 2; }

if [ "$TOOL" = "Bash" ]; then
  CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

  # DH-DEL-001 : jamais toucher aux services/processus
  if echo "$CMD" | grep -qE 'systemctl[[:space:]]+(restart|stop|start|reload|kill|disable|enable|mask)'; then deny "DH-DEL-001 systemctl"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(kill|pkill|killall|reboot|shutdown|halt)([[:space:]]|$)'; then deny "DH-DEL-001 kill/reboot"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])docker([[:space:]]|$)'; then deny "DH-DEL-001 docker"; fi

  # DH-DEL-002 : prod en lecture seule — jamais les credentials applicatifs
  if echo "$CMD" | grep -qE 'DH_SecurePass|-U[[:space:]]*digital_humans([[:space:]]|$)|user=digital_humans'; then deny "DH-DEL-002 credentials prod interdits"; fi
  if echo "$CMD" | grep -qiE '(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|GRANT)[[:space:]]' && echo "$CMD" | grep -qE 'DEOS_RO_DSN|172\.19\.0\.1'; then deny "DH-DEL-002 écriture prod"; fi

  # DH-CRO/CMO/CSM-001 : aucun envoi externe
  if echo "$CMD" | grep -qE '(curl|wget)[^|;]*(-X[[:space:]]*(POST|PUT|PATCH|DELETE)|--data|--form|-d[[:space:]]|-F[[:space:]])'; then deny "DH-x-001 envoi externe"; fi
  if echo "$CMD" | grep -qE '(^|[;&|[:space:]])(mail|sendmail|mutt|msmtp)([[:space:]]|$)'; then deny "DH-x-001 email"; fi

  # DH-COS-002 : decisions uniquement via deos-decisions
  if echo "$CMD" | grep -qE 'psql' && echo "$CMD" | grep -qiE '(INSERT|UPDATE|DELETE)[^;]*decisions'; then deny "DH-COS-002 decisions via deos-decisions uniquement"; fi

  # R14 : promotion de skills réservée à Sam
  if echo "$CMD" | grep -qE '(>|>>|cp[[:space:]]|mv[[:space:]]|tee[[:space:]])[^;|&]*\.claude/skills/'; then deny "R14 promotion de skill réservée à Sam"; fi
fi

if [ "$TOOL" = "Write" ] || [ "$TOOL" = "Edit" ]; then
  FP=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty'); CMD="$FP"
  if echo "$FP" | grep -qE '^/workspace/\.claude/skills/'; then deny "R14 promotion de skill réservée à Sam"; fi
  if echo "$FP" | grep -qE '^/prodlogs'; then deny "DH-DEL-002 prodlogs RO"; fi
fi
exit 0
