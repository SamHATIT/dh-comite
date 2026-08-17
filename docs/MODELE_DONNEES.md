# Modèle de données du comité — V2

> Produit par **LOT-01**. Migration : `migrations/2026-08-17-v2-tasks.sql`.
> Contrat : `refonte-v2/SPEC.md` §1.1 et §1.2.
> Dernière mise à jour : 17 août 2026.

Ce fichier explique **pourquoi le schéma est ainsi et pas autrement**. Le schéma
lui-même se lit dans la migration ; ce qui ne se lit nulle part ailleurs, c'est le
raisonnement — et c'est ce qui manquait quand un correctif posé en août se
re-diagnostiquait de zéro quelques jours plus tard.

---

## 1. Le changement de fond : la décision n'était pas une unité d'exécution

Avant ce lot, le comité tenait une table `decisions` et rien d'autre. Une décision
`accordee` était un texte. Rien ne portait :

- **le critère de fin** — donc « c'est fait » restait une affirmation ;
- **le porteur** — donc une décision pouvait n'appartenir à personne ;
- **la preuve** — sauf à la clôture, trop tard pour piloter ;
- **la reprise** — donc un échec sortait du champ de vision et n'y revenait jamais.

Le suivi se faisait dans le texte libre des décisions et dans `PageSuivi.md`,
régénérés à la main. Un blocage s'y écrivait en prose. De la prose, on ne peut pas
tirer une file.

**La table `tasks` est l'unité d'exécution qui manquait.** À partir d'ici :

```
decision  =  le contenant, ce qui est arbitré
tâche     =  ce qui se fait, se bloque, échoue, se prouve et se reprend
```

Une décision sans tâche n'avance pas — et cela devient visible, ce qui était tout
l'objet.

---

## 2. Table `tasks`

| Champ | Rôle |
| --- | --- |
| `id` | Identifiant `TASK-2026-0817-01`. Daté, donc lisible sans requête. |
| `decision_id` | Rattachement obligatoire à une décision (clé étrangère). Une tâche orpheline serait un travail que personne n'a arbitré. |
| `titre` | Ce qui est à faire, en une ligne. |
| `critere_fin` | **Condition de fin vérifiable, pas déclarative.** « le hook refuse un DELETE » et non « le hook est amélioré ». |
| `owner` | Qui exécute. |
| `echeance` | Date visée. Nullable : toutes les tâches ne sont pas datées. |
| `statut` | État courant. Vocabulaire fixé par LOT-02 (voir §6). |
| `attempt_count` | Nombre de tentatives. Pilote le budget d'échec. |
| `last_error` | Dernière erreur constatée, en clair. |
| `retry_at` | Date de remise en file automatique. |
| `blocker` | Obstacle **externe** constaté. Obligatoire si `blocked` ou `failed`. |
| `next_action` | Action suivante concrète. Obligatoire si `blocked` ou `failed`. |
| `next_owner` | Qui porte `next_action`. Obligatoire si `blocked` ou `failed`. |
| `budget_usd` | Budget de la tâche. Défaut 0,50 USD. |
| `consomme_usd` | Consommé réel. |
| `evidence_type` | `commit` \| `fichier` \| `base` \| `url`. |
| `evidence_ref` | La référence elle-même. |
| `cree_le`, `cree_par`, `maj_le` | Traçabilité. |

### Ce que porte `critere_fin`

C'est le champ qui applique l'invariant I3 au niveau le plus bas. Un critère
déclaratif (« la file est assainie ») se valide par une affirmation de celui qu'on
évalue. Un critère vérifiable (« la file contient 0 élément en erreur ») se valide
par une commande. Le premier mesure la déclaration, le second mesure le fait.

### Trois champs de reprise, une seule intention

`attempt_count`, `last_error` et `retry_at` existent pour une raison unique : **une
tâche `failed` dont `retry_at` est dépassé revient automatiquement dans la file**
(`SPEC §2.3`). Sans eux, un échec est un cul-de-sac : il faut qu'un humain se
souvienne. C'est précisément ce qui distingue un moteur d'exécution d'un
ordonnanceur, et c'est ce que la V1 n'avait pas.

L'index `idx_tasks_retry_at` est partiel (`WHERE retry_at IS NOT NULL`) : seules les
tâches en attente de reprise y figurent, ce qui est la question posée à chaque tour
par `deos-tasks list --dues`.

### Le déclencheur `trg_tasks_touch`

`maj_le` a un défaut à l'insertion mais ne se met pas à jour tout seul. Sans
déclencheur, le champ ment dès la première modification — et la question 2 de la
ronde V2 (« qu'est-ce qui a avancé depuis hier ? ») devient fausse en silence. La
fonction existante `touch_updated_at()` n'est pas réutilisable telle quelle : elle
écrit `updated_at`, et la colonne s'appelle ici `maj_le`. D'où `touch_maj_le()`.

---

## 3. Pourquoi la contrainte `blocage_avec_suite` est en base

```sql
CHECK (statut NOT IN ('blocked','failed')
       OR (blocker IS NOT NULL AND next_action IS NOT NULL AND next_owner IS NOT NULL))
```

C'est l'invariant I4 rendu impossible à contourner, et c'est le cœur du lot.

**Pourquoi pas dans le code applicatif.** Le registre est écrit par plusieurs
chemins : `bin/deos-tasks`, la boucle d'exécution de LOT-04, et `psql` à la main
pendant un incident — c'est-à-dire exactement au moment où la discipline cède. Un
contrôle applicatif n'est vrai que pour le chemin qui le traverse. Il y en a trois,
il y en aura d'autres.

**Ce qu'on empêche concrètement.** Une tâche bloquée sans action suivante est
*invisible* : elle n'apparaît dans aucune file, personne ne la reprend, elle ne
repart jamais. Elle a l'air d'un enregistrement honnête — « on a noté que c'était
bloqué » — alors que c'est un abandon. La contrainte force la question « et
ensuite, par qui ? » au moment précis où l'on constate le blocage, pas trois
semaines plus tard.

**Et on ne peut pas la retirer après coup.** Le cas a été testé : passer la tâche en
`blocked` avec les trois champs, puis vider `next_owner` par un `UPDATE`, échoue
aussi. La contrainte porte sur l'état de la ligne, pas sur la transition.

C'est le même mécanisme que le garde-fou du challenge (`SPEC §4bis` : une hypothèse
sans critère de réfutation n'est pas rendue). Dans les deux cas : **une obligation
vérifiable mécaniquement, pas une consigne.**

### `next_owner` est souvent quelqu'un d'autre

Le champ n'est pas une redite d'`owner`. `SPEC §3.1` — le paradoxe du Preflight —
dit qu'un agent privé de ses moyens ne peut pas se débloquer lui-même. Sans cette
distinction on obtient : « tu n'as pas les droits pour travailler → voici une tâche
→ obtiens les droits ». Le diagnostic de blocage (`SPEC §2.1`) attribue donc
`next_owner` selon la nature de l'obstacle : au `chief-of-staff` pour une question
de permission, à une autre direction pour une dépendance, au `ceo` pour un
arbitrage.

---

## 4. Pourquoi `blocked` et `failed` sont distincts

| | `blocked` | `failed` |
| --- | --- | --- |
| L'action a-t-elle été tentée ? | **Non** | **Oui** |
| Cause | obstacle externe | la tentative n'a pas abouti |
| Ce qu'on en fait | lever l'obstacle | changer d'approche |
| Champs propres | `blocker`, `next_action`, `next_owner` | + `attempt_count`, `last_error`, `retry_at` |

Les confondre coûterait la seule chose qui compte ici : **savoir s'il faut retirer un
obstacle ou changer de méthode.** Un `blocked` qu'on réessaie à l'identique
échouera à l'identique, l'obstacle n'ayant pas bougé. Un `failed` qu'on traite comme
un blocage attend un déblocage qui ne viendra pas — personne d'extérieur n'a rien à
lever.

C'est aussi ce qui rend le budget d'échec (`SPEC §2.2`) applicable : il ne se compte
que sur `failed`. Un blocage externe ne consomme pas de tentative, sans quoi un
agent serait escaladé au CoS pour trois obstacles qu'il n'a pas créés.

---

## 5. Pourquoi `obsolete` n'est pas `refusee`

| `refusee` | `obsolete` |
| --- | --- |
| **Un jugement.** Quelqu'un a examiné et écarté. | **Une péremption.** Le contexte a changé, la question n'a plus d'objet. |
| Porte un motif d'arbitrage. | Porte un motif de caducité. |
| Dit quelque chose sur la proposition. | Ne dit rien sur la proposition. |

**Ce que coûterait la confusion.** Sur les quelque quarante décisions ouvertes,
une partie n'a simplement plus d'objet — le report du lancement au 1er octobre en
périme mécaniquement plusieurs. Les marquer `refusee` **salirait le signal** : on
lirait ensuite un taux de refus élevé et on en tirerait une conclusion fausse sur la
qualité de ce qui est proposé, alors que rien n'a été jugé. Le tri des décisions
ouvertes est l'objet de LOT-09 (Recovery Sprint) : il a besoin des deux sorties,
distinctes.

Symétriquement, `obsolete` ne doit pas devenir la sortie commode pour ce qu'on ne
veut pas arbitrer. D'où l'exigence d'un motif, portée par LOT-03.

---

## 6. Les dix statuts de `decisions`

```
attente_sam ──► accordee ──► en_execution ──┬──► propose_cloture ──► clos
                                            ├──► blocked
                                            ├──► failed
                                            └──► needs_decision
                    refusee        obsolete
```

Cinq existaient (`attente_sam`, `accordee`, `en_execution`, `clos`, `refusee`), cinq
sont nouveaux (`propose_cloture`, `blocked`, `failed`, `needs_decision`,
`obsolete`). La matrice de droits — qui a le droit de poser quel statut — est
l'objet de LOT-03 et sera documentée dans `docs/REGISTRE.md`.

**Ce qui a été préservé.** La contrainte `clos_avec_preuve` reste en place : une
clôture sans preuve est toujours refusée par la base. Le déclencheur append-only
`trg_decisions_no_delete` (DH-COS-002) aussi. Les deux ont été vérifiés après
migration.

**Comment l'ancienne contrainte a été remplacée.** Elle était déclarée en ligne dans
`db/init/01_schema.sql`, donc nommée automatiquement par PostgreSQL. La migration ne
la nomme pas en dur : elle cherche toute contrainte `CHECK` de `decisions` dont la
définition mentionne `attente_sam`, et la remplace. Raison : **le schéma réel a
dérivé du fichier d'init** — `bin/deos-decisions` écrit une colonne `demo` qui n'y
figure pas. On ne peut donc pas supposer que la base ressemble à son fichier
d'origine.

---

## 7. Ce que ce lot ne fait délibérément pas

Ces points sont laissés ouverts **sciemment**, pour que leur absence se lise comme
une décision et non comme un oubli.

| Point | Pourquoi laissé ouvert |
| --- | --- |
| Pas de `CHECK` sur `tasks.statut` | `SPEC §1.2` définit un défaut (`a_faire`) mais **n'énumère pas** le vocabulaire. Les commandes de LOT-02 en impliquent un (`start`, `block`, `fail`, `done`, `valider`). L'inventer ici produirait une contrainte que LOT-02 devrait défaire. **À poser par LOT-02**, une fois le vocabulaire arrêté. |
| Pas d'obligation de preuve sur `propose_cloture` en base | LOT-03 l'exige au niveau de l'outil. L'ajouter à `clos_avec_preuve` reviendrait à modifier une contrainte hors du contrat de ce lot. À trancher avec LOT-03. |
| Pas de champs de blocage sur `decisions` | Voir §8 ci-dessous. |
| Pas de déclencheur append-only sur `tasks` | `decisions` est append-only (DH-COS-002) ; rien dans la SPEC ne l'exige pour `tasks`, dont la nature est d'être modifiée à chaque tour. |

---

## 8. Points à trancher — signalés, non inventés

### 8.1 Les champs de blocage sur `decisions` (à arbitrer avant LOT-03)

`SPEC §1.1` décrit le statut `blocked` d'une décision comme exigeant « `blocker`,
`next_action`, `owner` », et `failed` comme portant « `attempt_count`,
`last_error`, `retry_at` ». **Ces colonnes n'ont pas été créées sur `decisions`.**

Raisonnement retenu : cette phrase de §1.1 reprend mot pour mot l'invariant I4, qui
est écrit au niveau de la **tâche** (« Une tâche `blocked` ou `failed` DOIT
porter… »), et les champs sont définis en §1.2 sur `tasks`. La lecture retenue est
donc que le blocage d'une décision se **matérialise par ses tâches** : la décision
est le contenant, la tâche porte la suite. C'est cohérent avec le reste du modèle.

**Mais LOT-03 autorise une direction à passer une décision en `blocked` ou `failed`
directement**, sans mentionner de tâche. Si c'est bien l'intention, il manque de
quoi porter la suite à ce niveau, et LOT-03 n'a pas de budget DDL — ses fichiers
sont `bin/deos-decisions` et `docs/REGISTRE.md`.

Deux issues possibles, à trancher par Sam :

1. **Statu quo** (retenu par défaut) : une décision `blocked` doit avoir au moins une
   tâche `blocked` qui porte la suite. LOT-03 le vérifie côté outil.
2. **Symétrie** : ajouter les six colonnes à `decisions` et une contrainte miroir.
   C'est une migration d'une dizaine de lignes, sans risque pour l'existant.

### 8.2 Neuf ou dix statuts

`LOT-03` annonce « les neuf statuts » ; le tableau de `SPEC §1.1` en énumère **dix**.
Les dix ont été implémentés, l'énumération faisant foi sur le décompte. À corriger
dans le texte de LOT-03.

### 8.3 Rappel du point ouvert `SPEC §8.2`

`evidence_type` et `evidence_ref` existent, mais **ce qu'un commit doit modifier pour
valoir preuve n'est pas tranché** — un commit vide passerait aujourd'hui. Le schéma
ne peut pas trancher cela seul : c'est une règle de validation, pas une contrainte de
type. Signalé, non inventé.

---

## 9. Application et vérification

> **La migration n'a PAS été appliquée à la base de production du comité.** Le
> conteneur d'implémentation n'a ni démon Docker ni `$COMITE_DB_DSN`. Elle a été
> écrite, appliquée et vérifiée sur un **réplica fidèle** (schéma
> `db/init/01_schema.sql` + la dérive `demo` constatée, jeu de décisions couvrant
> les cinq statuts d'origine).

### Sauvegarde obligatoire avant application — invariant I6

Le répertoire de sauvegarde est une décision de déploiement, pas un chemin du
dépôt : il se pose en variable, hors de l'arbre versionné (`*.pre-*` et `*.bak*`
sont d'ailleurs ignorés par `.gitignore` — Git assure déjà cette fonction pour ce
qui est versionné, pas pour la base).

```bash
SAUVEGARDES="${DEOS_SAUVEGARDES:?definir le repertoire de sauvegarde}"
mkdir -p "$SAUVEGARDES"

docker exec dh-comite bash -c 'pg_dump "$COMITE_DB_DSN"' \
  > "$SAUVEGARDES/comite-$(date +%F-%H%M)-avant-LOT01.sql"

# Restauration ESSAYEE, sur une base jetable — pas seulement prevue.
# Comparer le nombre de decisions ET l'empreinte avant/apres :
psql -tAc "SELECT md5(string_agg(id||statut||coalesce(preuve::text,''), chr(10) ORDER BY id)) FROM decisions;"
```

**Ne pas appliquer si la restauration échoue.** Lors de la répétition sur réplica,
le premier essai a d'ailleurs échoué : le répertoire de sauvegarde n'était pas
lisible par l'utilisateur `postgres`. Un échec de ce genre ne se voit que si l'on
essaie vraiment — il était invisible tant que la sauvegarde seule était contrôlée.

### Application

```bash
docker exec -i dh-comite bash -c 'psql "$COMITE_DB_DSN" -v ON_ERROR_STOP=1' \
  < migrations/2026-08-17-v2-tasks.sql
```

La migration est **transactionnelle et rejouable** : un second passage ne produit que
des `NOTICE ... already exists, skipping`. Vérifié.

### Vérifications d'acceptation

> **Vérifier sans salir le registre.** `decisions` est append-only
> (`trg_decisions_no_delete`, DH-COS-002) : une ligne de test insérée en production
> **ne peut plus être supprimée**. Les contrôles 2 et 3 se font donc dans une
> transaction explicitement annulée. Une contrainte `CHECK` se déclenche à
> l'insertion, avant le `ROLLBACK` : le refus est bien constaté, la ligne ne
> survit pas.

```bash
# 1. La table existe, 20 champs conformes a SPEC §1.2
psql "$COMITE_DB_DSN" -c "\d tasks"

# 2. La contrainte refuse un blocage sans suite — DOIT echouer
psql "$COMITE_DB_DSN" <<'SQL'
BEGIN;
INSERT INTO tasks (id,decision_id,titre,critere_fin,owner,cree_par,statut)
SELECT 'TASK-VERIF-LOT01', id, 'verification', 'verification', 'delivery', 'cos', 'blocked'
  FROM decisions LIMIT 1;
ROLLBACK;
SQL
# attendu : ERROR ... violates check constraint "blocage_avec_suite"

# 3. Les dix statuts sont acceptes, un statut invente reste refuse.
#    statut est un text sous contrainte CHECK, pas un type enumere : la liste se
#    lit dans la definition de la contrainte.
psql "$COMITE_DB_DSN" -tAc "SELECT pg_get_constraintdef(oid) FROM pg_constraint
  WHERE conname='decisions_statut_check';"

psql "$COMITE_DB_DSN" <<'SQL'
BEGIN;
INSERT INTO decisions (id,origine,texte,statut) VALUES ('DEC-VERIF-01','cos','v','obsolete');
ROLLBACK;                                    -- attendu : INSERT 0 1, puis annule
BEGIN;
INSERT INTO decisions (id,origine,texte,statut) VALUES ('DEC-VERIF-02','cos','v','statut_invente');
ROLLBACK;                                    -- attendu : ERROR decisions_statut_check
SQL

# 4. Aucune decision perdue. Comparer au comptage pris AVANT la sauvegarde,
#    et pas seulement au nombre attendu.
psql "$COMITE_DB_DSN" -tAc "SELECT count(*) FROM decisions;"
psql "$COMITE_DB_DSN" -tAc "SELECT md5(string_agg(id||statut||coalesce(preuve::text,''), chr(10) ORDER BY id)) FROM decisions;"
```

### Résultat sur réplica — 17 août 2026

| Contrôle | Résultat |
| --- | --- |
| Sauvegarde + restauration essayée | **réussie** au 2ᵉ essai, empreinte identique |
| `tasks` créée, 20 champs | conforme `SPEC §1.2` |
| Blocage sans suite (6 variantes) | **refusé** dans les 6 cas |
| Blocage avec les 3 champs | accepté |
| Retrait de la suite après coup | **refusé** |
| 5 nouveaux statuts de `decisions` | acceptés |
| Statut inventé | refusé |
| `clos_avec_preuve` | préservée |
| Append-only `decisions` | préservé |
| Clé étrangère `tasks → decisions` | active |
| Décisions existantes | **5 avant, 5 après, empreinte inchangée** |
| Rejouabilité | seconde passe sans erreur |
