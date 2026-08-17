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

## Une seule source de vérité

`SPEC.md` fait foi. Quand un point est tranché, il l'est là — dans le tableau
« Tranchés » de la section 8. Les lots et les fiches peuvent le **citer**, jamais le
contredire.

Un lot qui présente comme ouvert un point tranché dans SPEC a tort : signalez-le
plutôt que de le suivre. C'est arrivé le 18/08 sur le droit du CEO à sortir du
backlog, et c'est le LOT-07 qui l'a vu.

**Les lots ne modifient jamais `SPEC.md`** — les autres sessions le lisent en
parallèle. Signalez, Sam porte la modification.

## Ce qui n'est pas tranché

Sept points en `SPEC.md §8`. **Les signaler, ne pas les inventer.**
