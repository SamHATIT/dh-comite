# dh-comite — Comité de direction augmenté Digital·Humans
Ce repo est le serveur du comité (CEO digital + 5 directeurs subagents).
Références : Gates 1-4 (specs des fiches), plan d'exploitation H2 2026.
Conventions : lecture seule vers la prod ($DEOS_RO_DSN, /prodlogs:ro, health
172.19.0.1:8002) · état local via bin/deos-state et bin/deos-decisions
uniquement · jamais de « fait » sans preuve sourcée · les hooks bloquent et
loggent, un refus se rapporte, ne se contourne pas.
