# Application des migrations V2 sur la base réelle

> Procédure **répétée le 18/08 sur une copie fidèle** de la base de production —
> 150 décisions, avec sa dérive et son déclencheur en ajout seul. Ce n'est pas un
> plan : c'est un enchaînement qui a été exécuté et qui a fonctionné.

## Pourquoi une répétition

La base réelle a **dérivé du fichier d'initialisation** : `bin/deos-decisions` écrit une
colonne `demo` absente de `db/init/01_schema.sql`, constat du LOT-01. Valider une
migration sur une base neuve ne prouve donc rien sur celle qui existe.

## L'ORDRE COMPTE — défaut trouvé pendant la répétition

L'ordre alphabétique est **faux** :

```
2026-08-17-v2-tasks-statut-motif.sql     ← se place AVANT
2026-08-17-v2-tasks.sql                  ← alors qu'elle en dépend
```

Un `for m in migrations/*.sql` échoue sur `relation "tasks" does not exist`. L'ordre
correct est celui de la dépendance, pas celui du nom :

```
1. 2026-08-17-v2-tasks.sql                 crée tasks, étend decisions
2. 2026-08-17-v2-tasks-statut-motif.sql    contraint tasks.statut, ajoute motif
3. 2026-08-17-v2-challenge.sql             crée challenges, propositions, avis
```

**La troisième (LOT-11) ne dépend d'aucune des deux** : ses tables sont neuves et ne
référencent ni `decisions` ni `tasks`. Elle est applicable seule, et recrée
`touch_maj_le()` seulement si la fonction manque — LOT-01 en reste propriétaire. Elle
se place en dernier parce qu'elle est arrivée en dernier, pas parce qu'elle attend
quelque chose.

## La procédure

### 1. Sauvegarde

```bash
H=$(date -u +%F-%H%M)
mkdir -p /root/sauvegardes
docker exec dh-comite bash -c 'pg_dump "$COMITE_DB_DSN"' > /root/sauvegardes/comite-$H.sql
ls -lh /root/sauvegardes/comite-$H.sql
```

**Un fichier de 0 octet est un piège connu** — le LOT-01 l'a rencontré quand le cluster
s'était arrêté. Vérifier la taille, pas seulement l'existence.

### 2. Restauration essayée — invariant I6

La base vit dans le conteneur `dh-comite-db`, pas dans `dh-comite`.

```bash
docker exec dh-comite-db psql -U comite -d postgres -q -c "DROP DATABASE IF EXISTS repetition;"
docker exec dh-comite-db psql -U comite -d postgres -q -c "CREATE DATABASE repetition;"
docker exec -i dh-comite-db psql -U comite -d repetition -q < /root/sauvegardes/comite-$H.sql
docker exec dh-comite-db psql -U comite -d repetition -tAc "SELECT count(*) FROM decisions;"
```

**Ne pas continuer si le compte diffère de la base réelle.**

### 3. Répétition sur la copie

```bash
for m in migrations/2026-08-17-v2-tasks.sql \
         migrations/2026-08-17-v2-tasks-statut-motif.sql; do
  docker exec -i dh-comite-db psql -U comite -d repetition -v ON_ERROR_STOP=1 -q < "$m"
done
```

Contrôles attendus après passage :

| Contrôle | Attendu |
| --- | --- |
| décisions | inchangé |
| colonnes `tasks` | 22 |
| colonnes `decisions` | 20 |
| contraintes de blocage | 2 |
| blocage sans suite | **refusé** |
| blocage avec suite | accepté |

### 4. Application réelle

Seulement si l'étape 3 est passée **sans aucune erreur**. Même ordre, base réelle.

### 5. Après

```bash
docker exec dh-comite-db psql -U comite -d postgres -q -c "DROP DATABASE repetition;"
```

Garder la sauvegarde. Elle est le seul retour en arrière.

## Résultat de la répétition du 18/08

| Étape | Résultat |
| --- | --- |
| Sauvegarde | 1,6 Mo, 786 lignes |
| Restauration | 0 erreur, 150 décisions |
| Migration 1 | OK |
| Migration 2 | OK |
| Structure | 22 + 20 colonnes, 2 contraintes |
| Reprise des motifs | 2 décisions retrouvées, `porte_sur` non vidé |
| Contrainte | refuse un blocage sans suite, accepte avec |

**Quand appliquer.** Après le LOT-04. Deux lots ont déjà découvert qu'une colonne
manquait — `motif`, puis `constat`. Une seule passe propre vaut mieux que deux
migrations successives sur une base déjà modifiée.
