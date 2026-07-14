---
name: dh-calendrier-editorial
description: >
  Ronde du Directeur Marketing Digital·Humans : structure du calendrier
  éditorial, séquence LinkedIn de lancement, format BrouillonContenu,
  score marketing. À utiliser pour toute ronde CMO.
---

# Ronde marketing Digital·Humans (fiche Gate 3)

## Étape 1 — calendrier
/workspace/bin/deos-state get calendrier_editorial — structure :
{"sequence_lancement":[{rang, type, titre, statut: a_produire|brouillon|
en_validation|valide|publie, date_cible, id_contenu}], "publies":[], "maj":""}.
Séquence de lancement actée (avant fin oct.) : 1. refonte page About ·
2. post pivot · 3-13. série des 11 portraits d'agents (Sophie, Olivia, Emma,
Marcus, Raj, Diego, Zara, Aisha, Elena, Jordan, Lucas — ordre à proposer).
Si calendrier vide : proposer la séquence complète datée en décision attendue.

## Étape 2 — performance
/workspace/bin/deos-state get perf_contenu — absent : recommandations
marquées hypothese:true, protocole de test proposé (1 contenu, mesurer, généraliser).

## Étape 3 — matière réelle
psql "$DEOS_RO_DSN" -c "SELECT name, status FROM v_deos_projects ORDER BY created_at DESC LIMIT 10;"
→ cas d'usage anonymisés citables (projets de test : les présenter comme
démonstrations, jamais comme références clients).

## Étape 4 — domain_score
cadence tenue vs calendrier (50) + contenus validés sans reprise majeure (30)
+ progression livre blanc (20) ; −10 par contenu en attente de validation >5j.
Calendrier vide : « non calculable », la valeur du jour = proposer la séquence.

## Étape 5 — sorties
RapportDirecteur (agent "marketing", champ calendrier_delta) via
deos-state set rapport_marketing --par marketing.
BrouillonContenu : {type, id, canal, place_dans_sequence, contenu,
faits_cites:[{affirmation, source}], conformite_marque:{transcreation,
lexique_dh, skill_applique}, decision_demandee}. Tout contenu applique
dh-fr-copywriting (vouvoiement, registre tech×luxe, zéro calque).
