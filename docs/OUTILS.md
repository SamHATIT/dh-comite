# Les outils du comité

> Produit par **LOT-02**. Outil principal : `bin/deos-tasks`.
> Schéma : `docs/MODELE_DONNEES.md` · Registre des décisions : `docs/REGISTRE.md`.
> Dernière mise à jour : 17 août 2026.

---

## 1. `deos-tasks` — la file d'exécution

### Pourquoi cet outil existe

Le comité savait enregistrer des décisions, pas les exécuter. Une décision
`accordee` était un texte : rien ne portait le critère de fin, le porteur, la preuve
ni la reprise. Le suivi vivait dans de la prose, et **de la prose on ne tire pas une
file**.

```
décision  =  le contenant, ce qui est arbitré
tâche     =  ce qui se fait, se bloque, échoue, se prouve — et REVIENT
```

Ce dernier mot est l'essentiel. Une tâche `failed` dont `retry_at` est dépassé
revient d'elle-même dans la file (`deos-tasks list --dues`). C'est ce qui distingue
un moteur d'exécution d'un ordonnanceur, et c'est ce que la V1 n'avait pas.

### Les commandes

```bash
deos-tasks add --decision DEC-X --titre "..." --critere-fin "..." \
               --owner delivery [--echeance 2026-08-25] [--budget 0.50] [--par cos]

deos-tasks list [--owner X] [--statut Y] [--dues]   # --dues : retry_at dépassé
deos-tasks show TASK-X

deos-tasks start   TASK-X --par delivery [--cout 0.03]
deos-tasks block   TASK-X --blocker "..." --next-action "..." --next-owner cos
deos-tasks fail    TASK-X --erreur "..." [--retry-dans 10min] [--cout N]
deos-tasks cause   TASK-X --cause "..." [--retry-dans 10min]
deos-tasks done    TASK-X --evidence-type commit --evidence-ref abc1234
deos-tasks valider TASK-X --par cos --constat "..."
```

### Les six états

| État | Posé par | Signification |
| --- | --- | --- |
| `a_faire` | `add` | créée, pas commencée |
| `en_cours` | `start` | démarrée |
| `blocked` | `block` | obstacle **externe** — l'action n'a pas pu être tentée |
| `failed` | `fail` | l'action **a été tentée** et a échoué |
| `done` | `done` | finie, avec preuve — **en attente de validation** |
| `valide` | `valider` | relue et validée |

`a_faire`, `blocked` et `failed` sont imposés mot pour mot par `SPEC §1.2` : les
traduire casserait la contrainte `blocage_avec_suite`, qui les énumère. D'où un
vocabulaire mi-français mi-anglais, assumé plutôt que corrigé au prix d'une
incohérence plus grave.

> **`done` et `valide` sont distincts** pour la même raison que `propose_cloture` et
> `clos` sur les décisions : celui qui fait le travail atteste, celui qui relit
> valide. Un seul état terminal ferait de la tâche son propre juge — I3.

### Ce que l'outil refuse

| Refus | Motif |
| --- | --- |
| `block` sans les trois champs | I4 — un blocage sans suite est invisible, il ne repart jamais |
| `done` sans preuve | sans preuve, la clôture est une affirmation |
| `done` avec un type de preuve hors `commit`/`fichier`/`base`/`url` | une preuve non typée ne se vérifie pas |
| `valider --par <direction>` | on ne relit pas son propre travail |
| `valider` sans `--constat` | la validation **est** une relecture : elle se dit |
| `valider` une tâche qui n'est pas `done` | on ne valide que ce qui est déclaré fini |
| `add` sur une décision inconnue | une tâche orpheline est un travail que personne n'a arbitré |
| `start` sur une tâche hors budget | voir §2 |

Et un avis, non bloquant, sur un critère de fin déclaratif :

```
$ deos-tasks add ... --critere-fin "le depot est propre"
AVIS: "le depot est propre" semble declaratif — un critere de fin se verifie
      par une commande
```

C'est I3 appliqué au niveau le plus bas. « La file contient 0 élément en erreur » se
vérifie ; « la file est assainie » se croit.

---

## 2. Le budget est récursif — c'est la règle centrale

```
tâche dépasse 10 %      ──►  la direction arbitre
direction dépasse 10 %  ──►  le CEO arbitre
CEO dépasse 10 %        ──►  Sam arbitre
```

**Le même mécanisme à chaque niveau, jusqu'à Sam.** Ce n'est pas une échelle de
sanctions ni trois règles différentes : c'est une seule règle appliquée
récursivement. Un dépassement se règle toujours de la même façon — en le portant à
qui peut engager davantage.

> **Une escalade n'est pas un refus. C'est une demande d'arbitrage à qui peut
> engager davantage.**

C'est la phrase qui compte. Un dépassement de budget ne dit pas « ce travail ne vaut
pas la peine » : il dit « ce travail coûte plus que ce que mon niveau peut décider
seul ». Traiter l'escalade comme un échec produirait exactement le comportement qu'on
ne veut pas — des agents qui rognent sur la tâche pour rester sous le seuil, ou qui
s'arrêtent sans le dire.

Le budget se pose sur la **tâche** (arbitrage de Sam). Le budget d'une session est la
somme des tâches qu'elle traite.

### Ce que l'outil fait voir

```
$ deos-tasks start TASK-2026-0817-01 --par delivery
REFUS: budget depasse — TASK-2026-0817-01 : 0.7000 USD consommes pour 0.5000 budgetes (+40 %)
       la tolerance est de 10 %. Escalade attendue : delivery arbitre.
       delivery deborde egalement (1.34 USD pour 1.00) : l'arbitrage remonte au ceo.
       et si le ceo deborde, a sam. Meme mecanisme a chaque niveau.
       Une escalade n'est pas un refus : c'est une demande d'arbitrage a
       qui peut engager davantage.
```

L'outil calcule les **deux niveaux qu'il peut voir** — la tâche, et le total de la
direction qui la porte. Le troisième (CEO → Sam) relève du tableau de bord (LOT-10),
mais le mécanisme est identique : c'est pour cela que le message le nomme au lieu de
s'arrêter au niveau constaté.

### Pourquoi seul `start` est refusé

`block`, `fail`, `cause`, `done` et `valider` ne sont **jamais** refusés pour
dépassement de budget.

`start` engage du travail à venir : le refuser demande un arbitrage avant de dépenser
davantage. Les autres commandes **enregistrent ce qui s'est déjà passé**. Refuser
d'enregistrer un fait reproduirait le défaut que toute cette refonte corrige : une
difficulté qui ne laisse pas de trace termine la session en silence (I5). On
n'empêche jamais de consigner.

---

## 3. Le budget d'échec — `SPEC §2.2`

| Tentative | Comportement |
| --- | --- |
| 1re | reprise directe, `retry_at = now() + 10 min` |
| 2e | **la reprise est suspendue** tant que la cause n'est pas nommée |
| 3e | `next_owner` passe au `chief-of-staff`, plus de reprise automatique |

### Comment « nommer la cause » est rendu mécanique

`SPEC §2.2` dit qu'à la 2ᵉ tentative l'agent « doit nommer la cause avant de
réessayer ». Deux implémentations venaient à l'esprit, **toutes deux fausses** :

| Implémentation | Pourquoi elle est fausse |
| --- | --- |
| Refuser un `fail` sans cause | on empêche d'enregistrer un fait. Une difficulté qui ne laisse pas de trace termine la session en silence — I5, le défaut même qu'on corrige |
| Exiger la cause dans un second `fail` | nommer la cause consommait alors une tentative, et faisait basculer au CoS au lieu de relancer. **Constaté en validation le 17/08.** |

D'où une commande distincte :

```bash
deos-tasks fail  TASK-X --erreur "timeout 30s"     # 2e échec : enregistré, reprise suspendue
deos-tasks cause TASK-X --cause "le pool de connexions sature a 20"
# OK: cause nommee — reprise dans 10min, sans consommer de tentative
```

**Nommer la cause n'est pas une tentative : c'est ce qui autorise la suivante.** La
commande n'incrémente pas `attempt_count`, et la tâche ne revient dans
`list --dues` qu'une fois la cause nommée. La règle n'est donc pas un message
d'encouragement : elle est portée par l'état de la file.

*Ajout au contrat du lot, signalé comme tel.*

### Ce que `fail` déduit tout seul

La commande `fail` du contrat ne prend ni `--blocker` ni `--next-owner`, alors que la
contrainte en base les exige pour `failed`. Ils sont donc **déduits du rang de la
tentative**, selon le tableau de `SPEC §2.1` et `§2.2` :

| Tentative | `next_action` | `next_owner` |
| --- | --- | --- |
| 1re | reprise directe | l'owner de la tâche |
| 2e | changer d'approche — cause à nommer | l'owner de la tâche |
| 3e et au-delà | arbitrage du CoS : réassigner, changer d'approche, ou remonter | `chief-of-staff` |

C'est ce qui rend la règle applicable au lieu de la laisser dans un document.
`--next-action` et `--next-owner` restent acceptés pour surcharger la déduction.

---

## 4. Ce que ce lot a ajouté au schéma

LOT-02 dispose d'un budget DDL (`migrations/2026-08-17-v2-tasks-statut-motif.sql`).

| Ajout | Motif |
| --- | --- |
| `CHECK` sur `tasks.statut` | `SPEC §1.2` donnait un défaut sans énumérer le vocabulaire. LOT-01 avait refusé de l'inventer ; LOT-02 définit les commandes, donc les états. |
| `tasks.constat`, `tasks.valide_par` | `SPEC §1.1` définit `valide` comme « avec preuve **et constat de relecture** », mais `§1.2` n'avait pas donné de colonne. La preuve est celle de l'exécutant, le constat celui du relecteur. |
| `decisions.motif` | dette signalée par LOT-03, accordée le 17/08. Le motif était rangé dans `porte_sur`, qui désigne ce sur quoi la décision porte. |

### La reprise des motifs existants

L'`UPDATE` de reprise ne touche que les décisions `refusee` et `obsolete` : ce sont
les deux seuls statuts pour lesquels `porte_sur` a servi de motif. Ailleurs,
`porte_sur` veut dire ce qu'il dit, et le recopier **fabriquerait un motif là où il
n'y en a jamais eu**.

`porte_sur` n'est pas vidé après reprise. Effacer une donnée pour réussir un
déplacement fait perdre ce qu'on n'avait pas prévu de relire.

`bin/deos-decisions` écrit désormais dans `motif`. Une colonne que rien n'alimente
serait une demi-correction — pire que l'absence, parce qu'elle a l'air faite.

---

## 5. `--cout` : comment la consommation est enregistrée

Le contrat du lot exige que l'outil refuse au-delà de 110 % du budget, **sans dire
comment `consomme_usd` se remplit**. Aucune commande ne le prévoyait : la règle
était donc inatteignable.

`--cout N` est accepté sur `start`, `block`, `fail` et `done` — les commandes qui
suivent un travail effectué — et s'ajoute au consommé. C'est l'ajout minimal qui rend
la règle du budget applicable. *Signalé comme ajout au contrat.*

---

## 6. Ce qui reste ouvert

| Point | État |
| --- | --- |
| `SPEC §8.2` — ce qu'un commit doit modifier pour valoir preuve | **non tranché.** `done --evidence-type commit --evidence-ref <sha>` accepte aujourd'hui un commit vide. L'outil vérifie que la preuve *existe*, pas qu'elle *prouve*. Signalé, pas décidé. |
| Passage de la décision en `en_execution` au démarrage d'une tâche | `deos-tasks start` ne touche pas la décision. Le droit a été ouvert à la direction porteuse dans LOT-03 ; le déclenchement automatique relève de la boucle (LOT-04). |
| Concurrence entre agents sur une même tâche | `SPEC §8.3`, ouvert. Aucun verrou posé. |

---

## 7. Vérification

```bash
# 1. Un blocage sans suite est refuse par l'outil
deos-tasks block TASK-TEST --blocker "x"                 # attendu : refus, code 2

# 2. Trois echecs passent la main au CoS
for i in 1 2 3; do deos-tasks fail TASK-TEST --erreur "essai $i"; done
deos-tasks show TASK-TEST | grep next_owner              # attendu : chief-of-staff

# 3. Une direction ne peut pas valider
deos-tasks valider TASK-TEST --par delivery --constat "x"  # attendu : refus

# 4. Le depassement de budget escalade
deos-tasks start TASK-TEST --par delivery --cout 0.60    # attendu : refus, code 3
```

### Résultat — 17 août 2026

Instance PostgreSQL locale jetable : schéma d'init + dérive (`demo`, `mode_demo`) +
migrations LOT-01 et LOT-02.

| Contrôle | Résultat |
| --- | --- |
| Sauvegarde + restauration essayée avant DDL | **réussie**, empreinte identique |
| Les 4 critères officiels du lot | **passés** |
| Escalade de budget — niveau tâche | refus, code 3 |
| Escalade de budget — **niveau direction**, récursion | message d'escalade au CEO |
| Budget dans la tolérance (+8 %) | accepté |
| `done` sans preuve / type invalide / après validation | refusés |
| `valider` sans constat / par une direction / hors `done` | refusés |
| 1re tentative → `retry_at` à +10 min | conforme |
| 2e tentative sans cause → **hors de `--dues`** | conforme |
| `cause` → retour dans la file, **sans consommer de tentative** | conforme |
| 3e tentative → `chief-of-staff`, plus de reprise auto | conforme |
| Statut hors vocabulaire | refusé par `tasks_statut_check` |
| Reprise `motif` — sélective (`refusee`/`obsolete` seulement) | conforme |
| Reprise `motif` — `porte_sur` préservé | conforme |
| Migration rejouable | second passage sans erreur |
| `bash -n` sur les deux outils | sans erreur |

> **Non appliqué en production.** Le SQL et l'outil sont produits et vérifiés ici ;
> l'application se fera séparément, après sauvegarde.

---

## 8. `challenge.py` — les mécanismes de challenge et le Strategic Yield

> Ajouté par **LOT-11**. Documentation complète : `docs/CHALLENGE.md`.
> **Essentiellement inactif à la livraison** — l'état réel se lit par
> `bin/challenge.py activation`, jamais par supposition.

```bash
bin/challenge.py activation                  l'état des interrupteurs
bin/challenge.py collecter                   les deux questions de la semaine
bin/challenge.py soumettre <direction> …     rendre un challenge (3 champs exigés)
bin/challenge.py contredire <direction> …    contredire le CEO ou Sam
bin/challenge.py proposer --texte …          une proposition stratégique
bin/challenge.py repondre PROP-… --par sam … l'arbitrage de Sam
bin/challenge.py etape PROP-… --etape …      expérimentée, résultat, impact
bin/challenge.py yield [--audit]             le Strategic Yield, rappel et veille
bin/challenge.py --autotest                  les garde-fous, sans toucher la base
```

**Trois codes de retour, comme `bin/policy.py`** : `0` OK ou mécanisme inactif, `2`
REFUS, `3` ERREUR. La distinction n'est pas cosmétique : REFUS veut dire « ta demande
n'est pas recevable, voici ce qui manque », ERREUR veut dire « je n'ai pas pu
décider » — base injoignable, configuration illisible. Les confondre ferait lire une
panne comme un refus, et une direction corrigerait sa saisie pendant que la base est à
terre.

**Un mécanisme inactif sort en 0 sans rien écrire.** L'interrupteur coupe le
mécanisme ; il ne produit pas une erreur à traiter.

**Le garde-fou refuse un challenge incomplet en nommant les champs manquants**, et la
base le refuserait de toute façon. Deux fois, parce que ce ne sont pas les mêmes
lecteurs : la contrainte protège le fait, le message protège l'agent.
