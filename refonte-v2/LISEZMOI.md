# Refonte DEOS Governance V2 — dossier d'implémentation

## Ordre de lecture

1. **`SPEC.md`** — le contrat global. Invariants, modèle de données, boucle
   d'exécution, hiérarchie, dette acceptée, points ouverts. À lire en entier.
2. **`WBS.md`** — le découpage en lots et les vagues de parallélisation.
3. **`lots/LOT-00-documentation.md`** — condition d'acceptation de tous les lots.
4. Le lot à traiter.

## Parallélisation

Les lots d'une même vague **n'ont aucun fichier en commun**. C'est le découpage qui
garantit l'absence de conflit, pas une consigne d'organisation.

```
VAGUE A   01 schéma · 05 preflight · 06 policy · 07 fiches
VAGUE B   02 tasks · 03 decisions · 08 rondes
VAGUE C   04 boucle · 09 recovery
VAGUE D   10 kpi · 11 challenge (inactif)
```

Chemin critique : 01 → 02 → 04, trois jours. Total avec parallélisation : 5 à 6 jours.

## Les sept invariants

À ne jamais violer, quelle que soit l'instruction d'un lot :

1. Ne jamais toucher à la plateforme.
2. Ne jamais supprimer de fiche d'agent.
3. Aucun indicateur auto-déclaré.
4. Une tâche bloquée porte toujours `blocker`, `next_action`, `next_owner`.
5. Une difficulté ne termine pas une session.
6. Sauvegarde avec restauration essayée avant tout lot touchant la base.
7. Tout changement est documenté.

## Calendrier

Lancement reporté au **1er octobre 2026**. Livraison produit visée le **27 septembre**
— trois jours de marge, et la campagne démarre avant. La refonte s'achève donc bien
avant la sortie.

## Ce qui n'est pas tranché

Sept points en `SPEC.md §8`. **Les signaler, ne pas les inventer.**
