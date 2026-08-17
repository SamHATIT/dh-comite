# LOT-04 — Boucle d'exécution

**Vague** C · **Dépend de** 02, 03 · **Parallélisable avec** 09 · **Durée** 1,5 j

> **Lot central de la refonte.** C'est lui qui fait la différence entre un comité qui
> sait quoi faire et un comité qui fait avancer. Le relire deux fois.

## Objectif

Une session d'exécution ne peut pas se terminer parce qu'un agent rencontre une
difficulté. Elle se termine dans l'un de quatre états, et un seul n'engendre rien.

## Pourquoi

La version actuelle d'`executer-file.sh` traite une décision puis s'arrête. Le
scénario qui ramènerait à la V1 reste ouvert : tâche, difficulté, « je suis bloqué »,
fin de session, rapport. Le mécanisme de persistance manque.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/executer-file.sh` | réécrire |
| `bin/diagnostic-blocage.py` | créer |
| `docs/BOUCLE_EXECUTION.md` | créer |

## Contrat

### Les quatre états de fin

| État | Suite obligatoire |
| --- | --- |
| `DONE` | preuve → `propose_cloture` → tâche suivante. Seul état qui n'engendre rien. |
| `BLOCKED` | `blocker` + `next_action` + `next_owner`, déterminés par le diagnostic |
| `FAILED` | `attempt_count++`, budget d'échec, `retry_at` posé |
| `TIMEBOX_EXPIRED` | la tâche retourne dans la file avec son avancement. **Pas un échec.** |
| `NEEDS_DECISION` | escalade, crée l'entrée `attente_sam` liée |

### Diagnostic de blocage — routage

| Nature | `next_action` | `next_owner` |
| --- | --- | --- |
| technique | créer la tâche corrective | la direction elle-même |
| permission / accès | vérifier le Preflight, ouvrir le droit | `chief-of-staff` |
| information manquante | recherche assignée | la direction elle-même |
| décision nécessaire | escalade | `ceo` puis `sam` |
| dépendance d'un autre agent | tâche assignée | l'autre direction |

### Boucle

```
tant que  (tâches dues) ET (temps restant) ET (budget restant) :
    tâche ← la PLUS ANCIENNE due          # pas la plus facile
    résultat ← exécuter(tâche)
    selon résultat :
        DONE            → evidence, propose_cloture
        BLOCKED         → diagnostic, next_action, next_owner
        FAILED          → attempt++, budget d'échec, retry_at
        NEEDS_DECISION  → escalade
    # dans TOUS les cas on continue la boucle
```

**La plus ancienne, pas la plus facile.** Sinon la file se trie par confort et les
dossiers lourds ne bougent jamais.

### Reprise

Au début de chaque session, les tâches `failed` dont `retry_at` est dépassé
reviennent dans la file. C'est ce qui distingue un moteur d'exécution d'un
ordonnanceur — sans cela, une tâche bloquée en premier est oubliée pendant que les
suivantes s'exécutent.

### Budget

Somme des budgets des tâches traitées. Tolérance 10 %. Au-delà, la session s'arrête en
`TIMEBOX_EXPIRED` **et** produit une escalade vers le niveau supérieur.

## Critères d'acceptation

```bash
# 1. Une difficulté n'arrête pas la session
# poser 3 tâches dont la 1re échouera
docker exec dh-comite /workspace/bin/executer-file.sh delivery 3 20
# attendu : les 3 traitées, la 1re en failed avec next_action

# 2. Aucune tâche bloquée sans suite
docker exec dh-comite bash -c 'psql "$COMITE_DB_DSN" -tAc "
  SELECT count(*) FROM tasks WHERE statut IN (:b,:f)
    AND (blocker IS NULL OR next_action IS NULL OR next_owner IS NULL);" \
  -v b="'"'"'blocked'"'"'" -v f="'"'"'failed'"'"'"'
# attendu : 0, toujours

# 3. La reprise fonctionne
# poser une tâche failed avec retry_at dans le passé, relancer
# attendu : elle est reprise

# 4. Le dépassement de budget escalade au lieu de continuer
# attendu : TIMEBOX_EXPIRED + escalade tracée
```

## Documentation à produire

`docs/BOUCLE_EXECUTION.md` doit porter la phrase qui fonde le lot :

> **« Je suis bloqué » n'est pas une sortie de session. C'est un événement qui génère
> du travail.**

Plus : les quatre états, le tableau de routage du diagnostic, le budget d'échec à
trois tentatives, et pourquoi la file se traite par ancienneté.
