# WBS — refonte DEOS Governance V2

> Onze lots, quatre vagues. Les lots d'une même vague **n'ont aucun fichier en commun** :
> ils s'exécutent en parallèle sans conflit. C'est le découpage qui garantit la
> parallélisation, pas une consigne d'organisation.

## Vue d'ensemble

```
VAGUE A  ─ parallèle ─────────────────────────────────────
  LOT-01  schéma de données          base + migrations
  LOT-05  Preflight                  bin/preflight.py
  LOT-06  Policy Engine minimal      bin/policy.py + hook
  LOT-07  fiches d'agents            .claude/agents/

VAGUE B  ─ parallèle ─ dépend de A ───────────────────────
  LOT-02  outil des tâches           bin/deos-tasks
  LOT-03  évolution du registre      bin/deos-decisions
  LOT-08  rondes V2                  bin/rondes.sh

VAGUE C  ─ parallèle ─ dépend de B ───────────────────────
  LOT-04  boucle d'exécution         bin/executer-file.sh
  LOT-09  Recovery Sprint            bin/recovery.py

VAGUE D  ─ parallèle ─ après tout ────────────────────────
  LOT-10  tableau de bord            bin/health.py
  LOT-11  mécanismes de challenge    bin/challenge.py  (inactif)
```

## Table des lots

| Lot | Objet | Vague | Dépend de | Fichiers | Durée |
| --- | --- | --- | --- | --- | --- |
| 01 | Schéma : table `tasks`, statuts, contrainte I4 | A | — | migrations SQL | 0,5 j |
| 05 | Preflight : 8 contrôles + assignation CoS | A | — | `bin/preflight.py` | 1 j |
| 06 | Policy Engine minimal : 3 capacités | A | — | `bin/policy.py`, hook | 1,5 j |
| 07 | Fiches : CEO, CoS, Delivery, Growth + 3 dormantes | A | — | `.claude/agents/` | 1 j |
| 02 | `deos-tasks` : CRUD, budget, reprise | B | 01 | `bin/deos-tasks` | 1 j |
| 03 | `deos-decisions` : nouveaux statuts, `propose_cloture` | B | 01 | `bin/deos-decisions` | 0,5 j |
| 08 | Rondes V2 : 5 questions, cadence, Preflight | B | 05, 07 | `bin/rondes.sh` | 0,5 j |
| 04 | Boucle : 4 états, diagnostic, budget d'échec | C | 02, 03 | `bin/executer-file.sh` | 1,5 j |
| 09 | Recovery Sprint : tri des 40 décisions | C | 03 | `bin/recovery.py` | 1 j |
| 10 | Executive Health Score | D | 01, 02 | `bin/health.py` | 1 j |
| 11 | Challenge, Strategic Yield — **inactifs** | D | 02, 07 | `bin/challenge.py` | 1 j |

**Chemin critique** : 01 → 02 → 04. Trois jours.
**Total séquentiel** : 10,5 jours. **Avec parallélisation** : 5 à 6 jours.

**Calendrier.** Lancement reporté au 1er octobre, livraison produit visée le
27 septembre. La refonte du comité s'achève donc bien avant, et non plus en
concurrence avec la sortie.

## Règles communes à tous les lots

1. **Sauvegarde avant.** Tout lot touchant la base : `pg_dump` horodaté, et
   restauration essayée avant de commencer.
2. **Un commit par lot**, message expliquant quoi, pourquoi, ce que ça remplace.
3. **Documentation obligatoire** : un lot dont la documentation manque n'est pas
   terminé. Voir `lots/LOT-00-documentation.md`.
4. **Critères d'acceptation vérifiables par commande**, jamais par affirmation.
5. **Ne jamais toucher à la plateforme.** Voir I1.
6. **Signaler, ne pas inventer** : les sept points ouverts de `SPEC.md §8` restent ouverts.
