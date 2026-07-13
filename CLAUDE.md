# dh-comite — Comité de direction augmenté Digital·Humans

Ce repo héberge le comité de direction IA de Digital·Humans (Sam Hatit) :
un CEO digital + 5 directeurs (subagents). Spécifications : Gates 1-4
(GATE*.md à la racine quand présents). La plateforme de delivery client
(Sophie→Lucas) est un système SÉPARÉ qui tourne en production — le comité
l'observe en lecture seule, ne la modifie jamais.

Règles non négociables :
- Toute affirmation porte une source datée. Jamais de « fait » sans preuve.
- Production en lecture seule (rôle deos_ro, vues v_deos_*). Jamais de
  systemctl/kill/docker. Le hook PreToolUse bloque et logge les violations —
  rapporter un refus, jamais le contourner.
- La table decisions ne se manipule que via /workspace/bin/deos-decisions.
- deos_state ne s'écrit que via /workspace/bin/deos-state (scopes par agent).
- Skills : proposition en .claude/skills-proposed/<agent>/, jamais
  d'écriture directe dans .claude/skills/ (promotion par Sam, commit).

Environnement : $DEOS_RO_DSN (prod RO) · $COMITE_DB_DSN (état comité) ·
/prodlogs/backend-24h.log (logs backend) · /workspace/bin dans le PATH à
ajouter si besoin.
