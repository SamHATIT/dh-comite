# LOT-02 — Outil des tâches

**Vague** B · **Dépend de** 01 · **Parallélisable avec** 03, 08 · **Durée** 1 j

## Objectif

`bin/deos-tasks` : créer, lister, faire avancer et clore des tâches. C'est l'outil que
la boucle d'exécution appellera.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/deos-tasks` | créer |
| `docs/OUTILS.md` | étendre |

## Contrat — commandes

```
deos-tasks add --decision DEC-X --titre "..." --critere-fin "..." \
               --owner delivery [--echeance 2026-08-25] [--budget 0.50]

deos-tasks list [--owner X] [--statut Y] [--dues]      # --dues : retry_at dépassé
deos-tasks show TASK-X
deos-tasks start TASK-X --par delivery
deos-tasks block TASK-X --blocker "..." --next-action "..." --next-owner cos
deos-tasks fail  TASK-X --erreur "..." [--retry-dans 10min]
deos-tasks done  TASK-X --evidence-type commit --evidence-ref abc1234
deos-tasks valider TASK-X --par cos --constat "..."     # CoS et CEO suppléant seulement
```

## Règles à faire respecter par l'outil

1. `block` **exige** les trois champs. Refuser sinon — la contrainte en base est le
   filet, l'outil doit refuser avant.
2. `fail` incrémente `attempt_count` et applique le budget d'échec :
   - 1re : `retry_at = now() + 10 min`
   - 2e : message imposant de nommer la cause avant de réessayer
   - 3e : passe `next_owner = chief-of-staff` automatiquement
3. `valider` n'accepte que `--par cos` ou `--par ceo`. Refuser toute direction.
4. `done` sans preuve est refusé.
5. **Budget** : si `consomme_usd > budget_usd * 1.1`, l'outil refuse et affiche
   l'escalade attendue (direction → CEO → Sam).

## Critères d'acceptation

```bash
# 1. Un blocage sans suite est refusé par l'outil
docker exec dh-comite /workspace/bin/deos-tasks block TASK-TEST --blocker "x"
# attendu : refus, code 2

# 2. Trois échecs passent la main au CoS
for i in 1 2 3; do docker exec dh-comite /workspace/bin/deos-tasks fail TASK-TEST --erreur "essai $i"; done
docker exec dh-comite /workspace/bin/deos-tasks show TASK-TEST | grep next_owner
# attendu : chief-of-staff

# 3. Une direction ne peut pas valider
docker exec dh-comite /workspace/bin/deos-tasks valider TASK-TEST --par delivery
# attendu : refus

# 4. Le dépassement de budget escalade
```

## Documentation à produire

`docs/OUTILS.md` : la liste des commandes, et surtout **la règle du budget récursif** —
tâche → direction → CEO → Sam, avec 10 % de tolérance à chaque niveau. Expliquer que
c'est le même mécanisme partout, jusqu'à Sam.
