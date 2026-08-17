# LOT-03 — Évolution du registre

**Vague** B · **Dépend de** 01 · **Parallélisable avec** 02, 08 · **Durée** 0,5 j

## Objectif

`deos-decisions` accepte les nouveaux statuts et, surtout, autorise un agent à
**proposer** une clôture sans la valider.

## Pourquoi

Règle actuelle : seuls `cos`, `ceo` et `sam` changent un statut. Juste dans son
principe, paralysante en pratique — le Delivery a corrigé une décision le 15/08, elle
est restée ouverte six jours. Le contrôle croisé doit être préservé, le goulot supprimé.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/deos-decisions` | modifier |
| `docs/REGISTRE.md` | créer |

## Contrat

1. Nouveaux statuts acceptés : `propose_cloture`, `blocked`, `failed`,
   `needs_decision`, `obsolete`.
2. **Une direction peut passer une décision en `propose_cloture`**, avec preuve
   obligatoire. Elle ne peut toujours pas la passer en `clos`.
3. `clos` reste réservé à `cos`, `ceo` et `sam`.
4. `needs_decision` crée automatiquement une entrée liée en `attente_sam`, avec la
   question en une phrase.
5. Le passage en `obsolete` exige un motif.

## Matrice à implémenter

| Statut visé | Qui peut le poser |
| --- | --- |
| `propose_cloture` | la direction porteuse, avec preuve |
| `blocked`, `failed` | la direction porteuse |
| `needs_decision` | la direction porteuse |
| `clos` | `cos`, `ceo` (suppléance), `sam` |
| `obsolete`, `refusee` | `cos`, `ceo`, `sam` |
| `accordee`, `attente_sam` | `ceo`, `sam` |

## Critères d'acceptation

```bash
# 1. Une direction peut proposer une clôture
docker exec dh-comite /workspace/bin/deos-decisions status DEC-X propose_cloture \
  --par delivery --preuve '{"commit":"abc1234"}'
# attendu : OK

# 2. Elle ne peut pas clore
docker exec dh-comite /workspace/bin/deos-decisions status DEC-X clos --par delivery
# attendu : refus

# 3. Une proposition sans preuve est refusée
docker exec dh-comite /workspace/bin/deos-decisions status DEC-Y propose_cloture --par delivery
# attendu : refus

# 4. needs_decision crée bien l'entrée liée
docker exec dh-comite /workspace/bin/deos-decisions status DEC-Z needs_decision \
  --par delivery --question "faut-il X ou Y ?"
docker exec dh-comite bash -c 'psql "$COMITE_DB_DSN" -tAc "SELECT count(*) FROM decisions WHERE statut='"'"'attente_sam'"'"' AND texte ILIKE '"'"'%DEC-Z%'"'"';"'
# attendu : 1
```

## Documentation à produire

`docs/REGISTRE.md` : les neuf statuts, la matrice de droits, et **pourquoi
`propose_cloture` existe** — citer le cas du 15/08, six jours d'attente pour une
correction déjà faite. Plus la distinction entre `refusee` et `obsolete`.
