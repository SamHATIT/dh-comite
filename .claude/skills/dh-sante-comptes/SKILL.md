---
name: dh-sante-comptes
description: >
  Ronde du Directeur Customer Success Digital·Humans : structure des comptes,
  usage réel par projet (deos_ro), calcul de santé, formats ReponseClient et
  AlerteChurn. À utiliser pour toute ronde CS.
---

# Ronde Customer Success Digital·Humans (fiche Gate 3)

## Étape 1 — comptes
/workspace/bin/deos-state get comptes_clients — structure attendue :
{"comptes":[{id, societe, tier, date_signature, echeance_renouvellement,
contacts:[], sla, baseline_usage, notes}], "maj":"date"}.
AUCUN client réel avant sept. 2026 : si vide, structurer le format + parcours
d'onboarding type, le déclarer, ne rien inventer.

## Étape 2 — usage réel (disponible dès aujourd'hui, sur les tests)
psql "$DEOS_RO_DSN" -c "SELECT p.user_id, count(e.id) AS executions,
  max(e.created_at) AS dernier_usage FROM v_deos_projects p
  LEFT JOIN v_deos_executions e ON e.project_id=p.id
  GROUP BY p.user_id ORDER BY dernier_usage DESC NULLS LAST;"
Sert aujourd'hui à construire les baselines de la formule ; demain au calcul réel.

## Étape 3 — tickets
/workspace/bin/deos-state get tickets — absent/vide : le déclarer
(« aucun canal de tickets actif »), ne pas estimer.

## Étape 4 — santé de compte (/100, formule visible)
usage vs baseline du compte : 40 pts · tickets : 30 pts (aucun ouvert = 30 ;
−10 par ticket >72h sans réponse validée) · renouvellement <45j sans contact
récent : −15 · incident delivery touchant le client non résolu (rapport
delivery, impact_client) : −20. Rouge <60 → AlerteChurn.
domain_score = moyenne des santés pondérée par tier (Team ×3, Pro ×1) ;
sans compte réel : « non calculable », statut declaré, structuration = la valeur du jour.

## Étape 5 — RapportDirecteur (agent "cs")
Champ spécifique "sante_comptes": [{compte, score, calcul, statut}].
Stocker via deos-state set rapport_cs --par cs. JSON + narratif court.
