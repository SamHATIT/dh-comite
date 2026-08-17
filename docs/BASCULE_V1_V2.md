# Bascule V1 → V2

> Le jour où la V2 remplace la V1. Écrit avant, pour que rien ne repose sur la
> mémoire au moment où le dispositif est à l'arrêt.

## Principe

**On ne bascule pas un dispositif en marche.** Les rondes s'arrêtent, on migre, on
nettoie, on redémarre. Arbitrage de Sam le 17/08 : les rondes actuelles répètent ce
qui est déjà connu, une journée d'arrêt ne coûte rien.

**Ce qui ne s'arrête jamais** — ce sont des mécanismes, pas des rituels :

| Mécanisme | Pourquoi il continue |
| --- | --- |
| `controle-depots.py` (18 h 30) | un travail qui ne vit que sur le serveur disparaît avec lui |
| `traiter-file-salesforce.sh` (5 min) | des prospects déposés attendraient sans être créés |

## L'ordre

```
1. ARRÊT          les rondes V1 cessent
2. SAUVEGARDE     avec restauration essayée (I6)
3. MIGRATIONS     dans l'ordre de dépendance, pas alphabétique
4. RECOVERY       tri des décisions ouvertes
5. PREFLIGHT      les quatre directions actives sont-elles aptes ?
6. DÉMARRAGE      rondes V2
```

Chaque étape se vérifie avant la suivante. **Aucune ne se rattrape après coup.**

---

### 1. Arrêt des rondes V1

```bash
crontab -l > /root/sauvegardes/crontab-avant-v2-$(date -u +%F).txt
crontab -l | grep -vE "rondes\.sh|daily\.sh|comite\.sh" | crontab -
crontab -l | grep -cE "controle-depots|file-salesforce"   # attendu : 2
```

La sauvegarde du cron est le retour en arrière de cette étape.

### 2. Sauvegarde et restauration essayée

Voir `docs/APPLICATION_MIGRATIONS.md`. **Un fichier de 0 octet est un piège connu** :
vérifier la taille, pas seulement l'existence.

### 3. Migrations

**Ordre de dépendance, jamais `migrations/*.sql`** — l'ordre alphabétique place
`tasks-statut-motif` avant `tasks` et échoue.

```bash
for m in migrations/2026-08-17-v2-tasks.sql \
         migrations/2026-08-17-v2-tasks-statut-motif.sql; do
  docker exec -i dh-comite-db psql -U comite -d dh_comite -v ON_ERROR_STOP=1 -q < "$m"
done
```

Contrôles : 22 colonnes sur `tasks`, 20 sur `decisions`, 2 contraintes de blocage,
nombre de décisions inchangé.

### 4. Recovery Sprint

```bash
docker exec dh-comite /workspace/bin/recovery.py --rapport      # simulation
docker exec dh-comite /workspace/bin/recovery.py --appliquer
```

**Deux étages, toujours.** La détection mécanique propose, le Chief of Staff relit.
Le 17/08, sur neuf décisions que la détection croyait faites, la relecture n'en a
validé qu'**une seule**. Ne jamais clore sur la seule empreinte.

Attendu : dix à quinze décisions actives, chacune avec un porteur et une échéance.
Aucune décision `accordee` sans tâche.

### 5. Preflight

```bash
docker exec dh-comite /workspace/bin/preflight.py --toutes
```

**Une direction NOT_READY ne démarre pas.** Son alerte va au Chief of Staff, jamais à
elle-même — un agent bloqué ne peut pas se débloquer seul.

### 6. Démarrage des rondes V2

Cadence cible : CEO, Chief of Staff, Delivery et Growth en quotidien. Juridique,
Financier et Customer Success en veille — leurs fiches restent, seule la cadence
tombe à zéro.

---

## Retour en arrière

| Étape | Comment revenir |
| --- | --- |
| 1 arrêt | restaurer le cron sauvegardé |
| 2–3 migrations | restaurer la sauvegarde SQL |
| 4 recovery | la sauvegarde de l'étape 2 — **c'est le seul retour** |
| 5–6 | remettre l'ancien `rondes.sh` (`git show`) |

**Le point de non-retour est l'étape 4.** Après le Recovery Sprint, la file des
décisions a changé de forme. La sauvegarde de l'étape 2 est alors la seule voie de
retour — d'où l'exigence de restauration *essayée*, pas seulement prévue.

## Ce qui ne se fait pas ce jour-là

- Toucher à la plateforme. La refonte porte sur le comité.
- Activer les mécanismes de challenge. Ils sont livrés inactifs, c'est voulu.
- Réveiller les fonctions en veille. Leur condition est la bascule sur matériel dédié.
