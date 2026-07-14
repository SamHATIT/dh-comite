---
name: dh-suivi-execution
description: >
  Ronde du Chief of Staff Digital·Humans : audit de la table decisions,
  rapprochement avec le dernier brief, file des skills proposés, génération
  de la PageSuivi, calcul du score exécution. À utiliser pour toute ronde
  CoS ou question sur l'état des décisions.
---

# Ronde du Chief of Staff (fiche Gate 3)

Environnement : `$COMITE_DB_DSN` · `/workspace/bin/deos-state|deos-decisions` ·
`/workspace/.claude/skills-proposed/` · sortie : `/workspace/PageSuivi.md`.

## Étape 1 — état des décisions
```bash
/workspace/bin/deos-decisions list
psql "$COMITE_DB_DSN" -c "SELECT id, statut, origine, (now()::date-date::date) AS age_j,
  left(texte,70) AS texte, preuve IS NOT NULL AS preuve
  FROM decisions ORDER BY date;"
```
Pour chaque décision non close : âge, dernier signe d'activité (rapports des
directeurs via deos-state), risque d'oubli (>7j sans activité).

## Étape 2 — rapprochement brief ↔ table
```bash
/workspace/bin/deos-state get brief | jq '.decisions_attendues // empty'
```
Toute décision attendue listée dans le brief mais ABSENTE de la table
decisions est un écart de traçabilité à signaler (et à proposer de créer via
deos-decisions add — tu peux le faire toi-même, c'est ton scope).

## Étape 3 — file des skills proposés
```bash
find /workspace/.claude/skills-proposed -mindepth 2 -name "*.md" | sort
```
Pour chacun : directeur, résumé (1 ligne), âge, statut (nouveau /
complements_demandes / valide / refuse — depuis le README du dossier).

## Étape 4 — priorités & cash
```bash
/workspace/bin/deos-state get priorites_semaine
/workspace/bin/deos-state get cash_suivi
```
Absents → le déclarer (« surveillance cash inactive », « aucune priorité de
semaine définie ») ; ne jamais estimer.

## Étape 5 — score exécution (formule visible)
base 100 · −8 par décision en retard (accordée/en_execution sans activité >3j)
· −15 par décision en risque d'oubli (>7j) · −5 par skill proposé sans
traitement >14j · −10 si une priorité de semaine est sans activité à
mi-semaine. Plancher 0. vert ≥80, ambre 60-79, rouge <60.

## Étape 6 — PageSuivi.md (écraser le fichier à chaque ronde)
Structure : en-tête daté · §1 Décisions (tableau : id, quoi (≤60c), origine,
statut, âge, preuve o/n, prochaine action) · §2 Skills proposés (id,
directeur, résumé, âge, statut) · §3 Priorités/OKR de la semaine ·
§4 Cash (état de la surveillance) · §5 Relances émises.

## Étape 7 — RapportDirecteur (schéma pivot, agent "cos")
Champs spécifiques : "execution_delta" {closes_avec_preuve, en_retard,
en_risque_oubli, ecarts_brief_table}. Stocker :
echo '<json>' | /workspace/bin/deos-state set rapport_cos --par cos
Restituer JSON + narratif court.
