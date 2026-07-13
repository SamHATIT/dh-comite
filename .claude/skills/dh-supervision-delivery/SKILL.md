---
name: dh-supervision-delivery
description: >
  Ronde de supervision de la production Digital·Humans : requêtes types sur
  les vues deos_ro, lecture des logs, règle anti-fausse-alerte, calcul du
  domain_score, format du RapportDirecteur. À utiliser pour toute ronde de
  supervision ou diagnostic d'incident sur la plateforme.
---

# Ronde de supervision Digital·Humans (P1, fiche Gate 2)

Environnement : `$DEOS_RO_DSN` (prod, lecture seule) · `$COMITE_DB_DSN` (état
comité) · `/prodlogs/backend-24h.log` (logs backend, export 15 min) ·
`/workspace/bin/deos-state` et `deos-decisions`.

## Étape a — santé des services
```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 10 http://172.19.0.1:8002/health
```
200 = backend up. Autre code ou timeout = service dégradé (vérifier aussi les
logs avant de conclure). Ne JAMAIS tenter de redémarrer quoi que ce soit.

## Étape b — exécutions
```bash
# En cours (à surveiller de près)
psql "$DEOS_RO_DSN" -c "SELECT id, project_name, status, execution_state,
  last_completed_phase, progress, current_agent, started_at,
  now()-state_updated_at AS silence FROM v_deos_executions
  WHERE completed_at IS NULL AND status NOT IN ('COMPLETED','FAILED','CANCELLED')
  ORDER BY started_at;"
# Dernières 24h (terminées ou non)
psql "$DEOS_RO_DSN" -c "SELECT id, project_name, status, execution_state,
  total_tokens_used, round(total_cost::numeric,2) AS cout, duration_seconds
  FROM v_deos_executions WHERE created_at > now()-interval '24 hours'
  OR completed_at > now()-interval '24 hours' ORDER BY id DESC;"
# Sections vides sur les exécutions récentes
psql "$DEOS_RO_DSN" -c "SELECT execution_id, count(*) FILTER (WHERE vide) AS vides,
  count(*) AS total FROM v_deos_sections
  WHERE created_at > now()-interval '48 hours'
  GROUP BY execution_id HAVING count(*) FILTER (WHERE vide) > 0;"
# Phases BUILD en cours/échec
psql "$DEOS_RO_DSN" -c "SELECT execution_id, phase_number, phase_name, status,
  agent_id, completed_batches || '/' || total_batches AS batches, elena_verdict
  FROM v_deos_build_phases WHERE status NOT IN ('completed')
  ORDER BY execution_id DESC, phase_number LIMIT 20;"
```

## Étape c — logs (fenêtre 24h)
```bash
grep -cE '"level": "(ERROR|CRITICAL)"' /prodlogs/backend-24h.log
grep -E '"level": "(ERROR|CRITICAL)"' /prodlogs/backend-24h.log | tail -20
grep -ciE 'warning' /prodlogs/backend-24h.log
```
Rapprocher chaque erreur d'une exécution (id dans le message) quand possible.

## Règle anti-fausse-alerte (DH-DEL-003)
Une exécution en cours avec un long `silence` n'est PAS bloquée. Un appel LLM
peut durer >10 min sur certaines phases. Verdict « bloqué » UNIQUEMENT si les
trois preuves sont réunies : silence > 2× la baseline de la phase (baseline en
mémoire/rapport précédent ; si absente, PAS de verdict de lenteur) ET aucune
activité de cette exécution dans les logs récents ET rien d'autre n'explique
le silence. Sinon : « en cours, plus lent que la référence », surveillance.

## domain_score (formule affichée dans le rapport)
base 100 · −20 par incident critique ouvert · −12 par incident haute ouvert ·
−8 par exécution en erreur non résolue (FAILED < 48h sans décision associée) ·
−5 par exécution « plus lente que baseline » · −5 si un service est dégradé ·
−3 par évolution priorité 1 en retard. Plancher 0.
Statut : vert ≥ 80 · ambre 60-79 · rouge < 60.

## Sortie — RapportDirecteur (schéma pivot)
```json
{"agent":"delivery","date":"YYYY-MM-DD","fraicheur":"ISO8601",
 "domain_score":N,"statut":"vert|ambre|rouge",
 "calcul_score":"100 - ... = N",
 "faits":[{"texte":"...","source":"postgres:v_deos_executions#ID | logs:HH:MM"}],
 "kpis":[{"nom":"projets_en_cours_sains","valeur":"X/Y","statut":"...","source":"..."}],
 "alertes":[{"gravite":"haute|moyenne|basse","texte":"...","source":"..."}],
 "decisions_demandees":[],"opportunites":[],
 "donnees_manquantes":["..."],"hypotheses":[]}
```
Stockage : `echo '<json>' | /workspace/bin/deos-state set rapport_delivery --par delivery`
Puis restituer le JSON suivi d'un court narratif (5-10 lignes max).
