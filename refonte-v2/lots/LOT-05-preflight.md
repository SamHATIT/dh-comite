# LOT-05 — Preflight

**Vague** A · **Dépend de** rien · **Parallélisable avec** 01, 06, 07 · **Durée** 1 j

## Objectif

Vérifier avant chaque ronde qu'un agent a les moyens de tenir son mandat. Un agent
NOT READY ne rentre pas dans la ronde — et son alerte va au Chief of Staff, pas à
lui-même.

## Pourquoi ce lot existe

Six pannes en douze jours, toutes de la même famille : un mandat sans le moyen de
l'exercer. Backlog non monté, dépôt en lecture seule, route inexistante, clé absente,
direction absente des rondes, curseurs annonçant des canaux qui n'existent pas. Dans
les trois premiers cas, c'est l'agent lui-même qui a fini par trouver la panne —
après plusieurs jours d'apparente inaction.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/preflight.py` | créer |
| `config/capabilites.yaml` | créer — ce dont chaque direction a besoin |
| `docs/PREFLIGHT.md` | créer |

## Contrat

Huit contrôles, par direction :

| Contrôle | Ce qu'il vérifie concrètement |
| --- | --- |
| `tools` | chaque outil déclaré existe, est exécutable, répond à `--help` sans effet de bord |
| `credentials` | chaque clé déclarée est présente et non vide |
| `permissions` | les curseurs existent en base pour les six axes |
| `mounts` | chaque chemin est monté, et dans le bon mode (lecture / écriture) |
| `apis` | chaque service externe répond — délai court, échec non bloquant si marqué optionnel |
| `budget` | il reste du budget sur la période |
| `policy` | le canal imposé du curseur désigne un outil qui existe |
| `evidence` | l'agent a un moyen de produire une preuve (dépôt accessible en écriture, ou table) |

### Règle du paradoxe — obligatoire

Une alerte Preflight est **automatiquement assignée au `chief-of-staff`**, qui décide
qui corrige. Ne jamais assigner une alerte Preflight à l'agent qu'elle bloque.

### Format de sortie

```json
{"direction":"delivery","statut":"NOT_READY",
 "echecs":[{"controle":"mounts","detail":"/repo-delivery non monte en ecriture",
            "next_action":"monter le volume en rw","next_owner":"chief-of-staff"}]}
```

## Critères d'acceptation

```bash
# 1. Toutes les directions actives passent, ou échouent en nommant le maillon
docker exec dh-comite /workspace/bin/preflight.py --toutes

# 2. Un échec simulé est détecté et assigné au CoS
docker exec dh-comite bash -c 'mv /workspace/bin/sf-lead /tmp/ && \
  /workspace/bin/preflight.py growth; mv /tmp/sf-lead /workspace/bin/'
# attendu : NOT_READY, controle=tools, next_owner=chief-of-staff

# 3. Le code de sortie distingue les deux cas
docker exec dh-comite /workspace/bin/preflight.py delivery; echo "sortie=$?"
# attendu : 0 si READY, 1 si NOT_READY
```

## Documentation à produire

`docs/PREFLIGHT.md` : les huit contrôles, ce que chacun vérifie, **et le tableau des
six pannes historiques avec le contrôle qui les aurait détectées**. C'est ce tableau
qui justifie le lot — sans lui, le Preflight ressemble à de la bureaucratie.

Expliquer aussi la règle du paradoxe, en citant sa formulation : « tu n'as pas les
moyens de travailler → voici une tâche → travaille pour obtenir les moyens ».
