---
name: dh-supervision-delivery
description: >
  Ronde de supervision de la production Digital·Humans : requêtes types sur
  les vues deos_ro, lecture des logs, checks anti-fausse-alerte, calcul du
  domain_score. À utiliser pour toute ronde, tout diagnostic, toute question
  sur l'état des exécutions SDS/BUILD.
---

# Ronde de supervision Digital·Humans

Environnement : tout est en LECTURE SEULE. DSN prod : variable `$DEOS_RO_DSN`
(vues uniquement). Logs : `/prodlogs/backend-24h.log` (JSON par ligne,
rafraîchi toutes les 15 min). Santé : `http://172.19.0.1:8002/health`.

## Ordre de la ronde

### 1. Santé des services
```bash
curl -s -m 5 http://172.19.0.1:8002/health          # attendu {"status":"healthy"}
stat -c '%y' /prodlogs/backend-24h.log               # fraîcheur export logs (< 20 min)
```
Le log contient aussi les lignes `[RAG HEALTH]` (ChromaDB, nb de chunks).

### 2. Exécutions — en cours et 24h
```bash
psql "$DEOS_RO_DSN" -c "SELECT id, project_name, status, execution_state,
  last_completed_phase, progress, current_agent, total_tokens_used,
  round(total_cost::numeric,2) AS cost, duration_seconds, started_at, state_updated_at
  FROM v_deos_executions
  WHERE completed_at IS NULL OR completed_at > now() - interval '24 hours'
  ORDER BY id DESC;"
```
Statuts « en cours » : RUNNING / IN_PROGRESS / WAITING_* (une attente de
validation client n'est PAS une anomalie). Sections d'une exécution :
```bash
psql "$DEOS_RO_DSN" -c "SELECT agent_id, deliverable_type, content_length, vide
  FROM v_deos_sections WHERE execution_id = <ID> ORDER BY id;"
```
Phases BUILD : `v_deos_build_phases` (statut par phase, verdict Elena).

### 3. Logs 24h — erreurs et signaux
```bash
grep -c '"level": "ERROR"' /prodlogs/backend-24h.log
grep '"level": "ERROR"' /prodlogs/backend-24h.log | tail -5
grep -iE 'truncat|max_tokens|timeout|retry' /prodlogs/backend-24h.log | tail -5
```

### 4. Anti-fausse-alerte (DH-DEL-003) — avant tout verdict « bloqué »
Une exécution silencieuse n'est PAS bloquée. Vérifier les TROIS conditions :
1. `state_updated_at` sans changement depuis > 2× la baseline de la phase
   (baselines dans MEMORY.md ; si absentes → pas de verdict, observer) ;
2. aucune ligne de log liée à l'exécution dans les 15 dernières minutes ;
3. pas d'appel LLM ouvert visible dans les logs (les phases LLM longues
   >10 min sont NORMALES, ex. WBS ~13 min sans écriture).
Deux conditions sur trois → « plus lent que baseline, surveillance
renforcée », jamais « bloqué ».

### 5. domain_score
Appliquer la formule de l'agent (base 100, malus), MONTRER le calcul dans
le rapport. Toute donnée manquante va dans `donnees_manquantes`, jamais
comblée.

## Pièges connus
- `WAITING_BR_VALIDATION` = le client n'a pas validé ses BR : attente
  normale, potentiellement longue (jours). À signaler en fait, pas en alerte
  (sauf > 7 jours : opportunité de relance côté CSM).
- L'export logs a jusqu'à 15 min de retard : ne pas conclure « aucune
  activité » sur la seule absence de lignes récentes si < 20 min.
- Ne JAMAIS interroger les tables brutes ni utiliser d'autres credentials
  que $DEOS_RO_DSN [DH-DEL-002].
