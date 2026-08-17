# LOT-01 — Schéma de données

**Vague** A · **Dépend de** rien · **Parallélisable avec** 05, 06, 07 · **Durée** 0,5 j

## Objectif

Créer la table `tasks`, étendre les statuts de `decisions`, et poser la contrainte qui
rend l'invariant I4 impossible à contourner.

## Avant de commencer

```bash
docker exec dh-comite bash -c 'pg_dump "$COMITE_DB_DSN"' > /root/sauvegardes/comite-$(date +%F-%H%M).sql
# Vérifier que la restauration fonctionne, sur une base jetable
```

**Ne pas continuer si la restauration échoue.** Invariant I6.

## Fichiers

| Chemin | Action |
| --- | --- |
| `migrations/2026-08-17-v2-tasks.sql` | créer |
| `docs/MODELE_DONNEES.md` | créer |

## Contrat

1. Table `tasks` conforme à `SPEC.md §1.2`, avec tous les champs.
2. Contrainte `blocage_avec_suite` posée **en base**, pas dans le code applicatif.
3. Les statuts `propose_cloture`, `blocked`, `failed`, `needs_decision`, `obsolete`
   acceptés par `decisions`.
4. Aucune décision existante modifiée.

## Critères d'acceptation

```bash
# 1. La table existe
docker exec dh-comite bash -c 'psql "$COMITE_DB_DSN" -c "\d tasks"'

# 2. La contrainte refuse un blocage sans suite — DOIT échouer
# insérer une tâche statut=blocked sans blocker → attendu : ERROR blocage_avec_suite

# 3. Les nouveaux statuts sont acceptés

# 4. Aucune décision perdue
docker exec dh-comite bash -c 'psql "$COMITE_DB_DSN" -tAc "SELECT count(*) FROM decisions;"'
```

## Documentation à produire

`docs/MODELE_DONNEES.md` doit contenir :

- le schéma des deux tables, avec le **rôle** de chaque champ ;
- **pourquoi** la contrainte existe : une tâche bloquée sans action suivante est
  invisible et ne repart jamais ;
- pourquoi `failed` et `blocked` sont **distincts** : l'un a été tenté, l'autre non ;
- pourquoi `obsolete` n'est pas `refusee` : péremption contre jugement.

## Commit attendu

```
LOT-01 — table tasks, statuts etendus, contrainte de blocage

POURQUOI LA CONTRAINTE EN BASE. L'invariant I4 dit qu'une tache bloquee doit
porter blocker, next_action et next_owner. Le poser dans le code applicatif ne
suffit pas : le registre est ecrit par plusieurs outils, et une tache bloquee
sans suite est invisible — elle ne repart jamais.

FAILED ET BLOCKED SONT DISTINCTS. blocked = obstacle externe, l'action n'a pas
pu etre tentee. failed = l'action a ete tentee et a echoue.

OBSOLETE N'EST PAS REFUSEE. Sur 40 decisions ouvertes, une partie n'a plus
d'objet — le contexte a change. Les marquer refusees salirait le signal.
```
