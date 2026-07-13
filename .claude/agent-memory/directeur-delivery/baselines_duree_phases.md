---
name: baselines-duree-phases
description: Baselines de durée observées pour les phases SDS/BUILD, construites faute de baseline initiale (première ronde 2026-07-13)
metadata:
  type: project
---

Baselines construites à partir de l'historique des exécutions COMPLETED/phases via
`v_deos_executions` et `v_deos_build_phases` ($DEOS_RO_DSN), ronde du 2026-07-13.

**Phase 1 PM (started_at → state_updated_at, jusqu'à `waiting_br_validation`)** :
échantillon de 6 exécutions (id 140, 149, 150, 151, 152, 158) entre 2026-02-10 et
2026-06-08 → durée quasi constante **50 s à 1 min 40 s**. Baseline provisoire :
~1 minute. Fiable (faible variance).

**Durée totale SDS complet (started_at → completed_at, jusqu'à `sds_complete`)** :
échantillon de 8 exécutions (id 141, 142, 144, 146, 148, 155, 159, 160) entre
2026-02-10 et 2026-06-13 → très variable : **18 min (id 146) à 1 h 44 (id 148)**,
moyenne approximative ~55 min. Échantillon trop hétérogène pour fixer un seuil
2× fiable — à affiner sur les prochaines rondes avant d'invoquer un verdict de
lenteur (DH-DEL-003) sur ce total.

**Phases BUILD (raj/diego/zara/aisha, `v_deos_build_phases`)** : seulement 2
lignes en base au 2026-07-13, toutes deux `status=failed` (agent raj, phase
data_model, exécutions 24 et 131) → échantillon insuffisant pour toute baseline.
Ne pas utiliser tant qu'aucune phase BUILD n'aura complété avec succès.

**Comment appliquer** : ne jamais qualifier une exécution de "plus lente que
baseline" sur la seule durée totale SDS (variance trop grande) ; la baseline
phase1_pm (~1 min) est en revanche exploitable pour ce jalon précis. Réévaluer
et resserrer ces chiffres à chaque ronde où de nouvelles exécutions complètent
des phases. Voir aussi [[etat-plateforme-2026-07]].
