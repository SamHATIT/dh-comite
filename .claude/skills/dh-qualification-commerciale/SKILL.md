---
name: dh-qualification-commerciale
description: >
  Ronde du Directeur Commercial Digital·Humans : structure du pipeline,
  scoring de qualification, sources de leads (concierge Sophie), formats
  DossierCommercial. À utiliser pour toute ronde CRO ou travail commercial.
---

# Ronde commerciale Digital·Humans (fiche Gate 3)

## Étape 1 — pipeline
`/workspace/bin/deos-state get pipeline_commercial` — structure attendue :
{"stades":{"lead":[],"qualifie":[],"demo":[],"proposition":[],"negociation":[],"signe":[],"perdu":[]},
 "maj":"date"}. Chaque entrée : {societe, contact, source, stade, valeur_estimee,
 tier_vise, score_qualification, prochaine_action, echeance, historique:[]}.
Si vide/embryonnaire : structurer, ne rien inventer.

## Étape 2 — sources de leads réelles
- Références livrables : psql "$DEOS_RO_DSN" -c "SELECT id, name, status FROM v_deos_projects ORDER BY created_at DESC LIMIT 15;"
  (projets de TEST internes avant sept. 2026 — utilisables comme cas d'usage anonymisés, PAS comme prospects)
- Leads concierge : pas encore branché (phase 2, annexe A) — le déclarer.
- Objectifs hebdo : /workspace/bin/deos-state get objectifs_commerciaux — si absent,
  domain_score non calculable : le déclarer et demander à Sam de les fixer (décision attendue).

## Étape 3 — scoring /10
besoin Salesforce réel et récurrent (0-3) · taille/maturité org SF (0-2) ·
budget plausible pour le tier visé (0-2) · sponsor identifié (0-2) · urgence (0-1).
≥7 → dossier démo ; 4-6 → nurturing (revoir 30j) ; <4 → sortie motivée.

## Étape 4 — domain_score
Si objectifs hebdo présents : part des objectifs tenus (leads qualifiés,
dossiers produits, relances préparées) rapportée à 100 ; −10 par relance en
retard >7j ; −15 par engagement hors validation (doit être 0). Sinon : "non
calculable", statut ambre, formule affichée quand même.

## Étape 5 — RapportDirecteur (agent "commercial")
Champ spécifique "pipeline_delta" : {entrees:[], sorties:[], changements_stade:[]},
chaque mouvement sourcé. Stocker via deos-state set rapport_commercial --par commercial.
JSON + narratif court.
