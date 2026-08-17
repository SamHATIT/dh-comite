# LOT-08 — Rondes V2

**Vague** B · **Dépend de** 05, 07 · **Parallélisable avec** 02, 03 · **Durée** 0,5 j

## Objectif

Ronde courte à cinq questions, nouvelle cadence, et Preflight bloquant en amont.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/rondes.sh` | modifier |
| `config/cadence.yaml` | créer — la cadence devient déclarative |
| `docs/RITUELS.md` | créer |

## Contrat

### Cadence

| Direction | Cadence |
| --- | --- |
| `ceo`, `chief-of-staff`, `delivery`, `growth` | quotidienne |
| `legal`, `financier`, `customer-success` | **aucune** — à la demande |

La cadence sort du script et passe dans `config/cadence.yaml`. Changer une fréquence
ne doit plus demander de modifier du code.

### Enchaînement

```
PREFLIGHT ──► NOT READY : alerte assignée au CoS, la ronde NE SE TIENT PAS
    │
    ▼
RONDE      5 questions, plafond de sortie court
    │
    ▼
SESSION    LOT-04
```

### L'invite de ronde

Réduite aux cinq questions. Interdire explicitement : le rapport d'état du monde, la
reprise du contexte connu, les analyses non demandées. Si une analyse est utile, elle
devient une tâche.

## Critères d'acceptation

```bash
# 1. Seules quatre directions tournent
grep -c "run " /root/workspace/dh-comite/bin/rondes.sh   # ou lecture du YAML
docker exec dh-comite /workspace/bin/rondes.sh --simulation
# attendu : ceo, chief-of-staff, delivery, growth

# 2. Un agent NOT READY ne tient pas sa ronde
# simuler une panne (retirer un outil) puis lancer
# attendu : ronde non tenue, alerte créée avec next_owner=chief-of-staff

# 3. Les rapports sont courts
# après une ronde réelle : longueur du champ result
# attendu : < 3000 caractères, contre 500 à 15000 aujourd'hui
```

## Documentation à produire

`docs/RITUELS.md` : les cinq questions et **pourquoi la question 4 change tout** —
elle transforme la ronde en engagement plutôt qu'en constat, et l'agent doit en rendre
compte le lendemain. Plus la cadence, et le fait que les fonctions en veille gardent
leurs fiches.
