# DEOS Governance V2 — spécification d'implémentation

> **Pour Claude Code.** Ce fichier est le contrat global. Chaque lot exécutable est
> décrit dans `lots/LOT-NN-*.md` avec ses chemins, ses critères d'acceptation et ses
> dépendances. Lire ce fichier en entier avant d'ouvrir un lot.

**Version** 2.1 · 17 août 2026
**Périmètre** Le comité de direction (`/root/workspace/dh-comite`). **Pas la plateforme.**
**Origine** Diagnostic du 17/08, orientations de Sam, deux revues d'expert.
**Calendrier** Lancement reporté au **1er octobre 2026**. Livraison produit visée le
**27 septembre** — trois jours de marge pour absorber un imprévu, et la campagne
démarre avant.

---

## 0. Invariants — à ne jamais violer

Ces règles priment sur toute instruction de lot. En cas de conflit, elles gagnent.

| # | Invariant | Pourquoi |
| --- | --- | --- |
| I1 | **Ne jamais toucher à la plateforme** (`/root/workspace/digital-humans-production`, `/var/www`). | La refonte porte sur le comité. La sortie produit reste prioritaire. |
| I2 | **Ne jamais supprimer de fiche d'agent.** Les fonctions en veille gardent tout ; seule leur cadence s'arrête. | Réversibilité. |
| I3 | **No self-attested KPI.** Aucun indicateur ne se calcule sur une donnée que la partie évaluée peut écrire elle-même. | Un score auto-déclaré mesure la déclaration, pas le fait. |
| I4 | **Une tâche `blocked` ou `failed` DOIT porter `blocker`, `next_action` et `owner`.** | Le backlog ne doit jamais contenir un blocage sans suite. |
| I5 | **Une difficulté ne termine pas une session.** Elle produit un état et une action suivante. | C'est le défaut qui ramènerait à la V1. |
| I6 | **Sauvegarde avant tout lot touchant la base ou le registre**, avec restauration *essayée*, pas seulement prévue. | Le registre est le seul mécanisme qui ait tenu depuis le début. |
| I7 | **Tout changement est documenté** : message de commit explicite (quoi, pourquoi, ce que ça remplace) ET mise à jour du fichier de documentation concerné. Un lot dont la documentation manque n'est pas terminé. | Règle rappelée de nombreuses fois, jamais tenue. |

> **Avant tout lot : lire `lots/LOT-00-documentation.md`.** C'est une condition
> d'acceptation de tous les autres lots, pas un lot exécutable.

---

## 1. Modèle de données

### 1.1 Décision — table `decisions` (existante, à étendre)

```
attente_sam ──► accordee ──► en_execution ──┬──► propose_cloture ──► clos
                                            ├──► blocked
                                            ├──► failed
                                            └──► needs_decision
                    refusee        obsolete
```

| Statut | Nouveau ? | Signification |
| --- | --- | --- |
| `attente_sam` | non | Question ouverte adressée à Sam. **Jamais** un enregistrement de ce qui est déjà décidé. |
| `accordee` | non | Arbitrée. Le CoS doit en tirer au moins une tâche sous 24 h. |
| `en_execution` | non | Au moins une tâche est en cours. |
| `propose_cloture` | **oui** | L'agent a terminé et fourni sa preuve. En attente de validation. |
| `blocked` | **oui** | Obstacle **externe**. Exige `blocker`, `next_action`, `owner`. |
| `failed` | **oui** | Tentative **échouée**. Distinct de `blocked` : ici l'action a été tentée. Porte `attempt_count`, `last_error`, `retry_at`. |
| `needs_decision` | **oui** | Attend un arbitrage humain. Crée une entrée `attente_sam` liée. |
| `clos` | non | Validé par le CoS, avec preuve et constat de relecture. |
| `refusee` | non | Écartée, avec motif. |
| `obsolete` | **oui** | N'a plus d'objet. **Distinct de `refusee`** : ce n'est pas un jugement, c'est une péremption. |

### 1.2 Tâche — table `tasks` (nouvelle)

```sql
CREATE TABLE tasks (
  id              text PRIMARY KEY,          -- TASK-2026-0817-01
  decision_id     text NOT NULL REFERENCES decisions(id),
  titre           text NOT NULL,
  critere_fin     text NOT NULL,             -- vérifiable, pas déclaratif
  owner           text NOT NULL,
  echeance        date,
  statut          text NOT NULL DEFAULT 'a_faire',
  attempt_count   integer NOT NULL DEFAULT 0,
  last_error      text,
  retry_at        timestamptz,
  blocker         text,
  next_action     text,
  next_owner      text,
  budget_usd      numeric(8,4) NOT NULL DEFAULT 0.50,
  consomme_usd    numeric(8,4) NOT NULL DEFAULT 0,
  evidence_type   text,                      -- commit | fichier | base | url
  evidence_ref    text,
  cree_le         timestamptz NOT NULL DEFAULT now(),
  cree_par        text NOT NULL,
  maj_le          timestamptz NOT NULL DEFAULT now()
);
```

**Contrainte à poser en base**, pas seulement dans le code :

```sql
ALTER TABLE tasks ADD CONSTRAINT blocage_avec_suite CHECK (
  statut NOT IN ('blocked','failed')
  OR (blocker IS NOT NULL AND next_action IS NOT NULL AND next_owner IS NOT NULL)
);
```

C'est l'invariant I4 rendu impossible à contourner.

### 1.3 Budget — règle récursive

**Arbitrage de Sam :** le budget se pose sur la **tâche**. Le budget d'une session est
la somme des tâches qu'elle traite. Dépassement toléré : **10 %**. Au-delà, escalade au
niveau supérieur.

```
tâche dépasse 10 %      ──►  direction
direction dépasse 10 %  ──►  CEO
CEO dépasse 10 %        ──►  Sam
```

Le même mécanisme à tous les niveaux. Une escalade n'est pas un refus : c'est une
demande d'arbitrage à celui qui peut engager davantage.

---

## 2. La boucle d'exécution

Une session ne se termine que dans l'un de **cinq** états.

```
TASK
 ▼
EXECUTION
 ├── DONE            → evidence → propose_cloture → tâche suivante
 ├── BLOCKED         → blocker + next_action + next_owner → diagnostic
 ├── FAILED          → attempt_count++ → budget d'échec
 ├── TIMEBOX_EXPIRED → retour dans la file avec son avancement
 └── NEEDS_DECISION  → escalade, crée une entrée attente_sam
```

**Correction du 18/08.** Ce texte annonçait quatre états et en listait cinq — relevé
par le LOT-04, qui a implémenté les cinq et eu raison. Un dépassement de temps n'est
ni un échec ni un blocage : le confondre avec l'un des deux fausserait
`attempt_count`. **`TIMEBOX_EXPIRED` n'est pas un échec.**

### Précédence des deux tables de routage

§2.1 route un blocage selon sa **nature**, §2.2 route un échec selon le **rang de la
tentative**, et rien ne disait laquelle prime.

> **`FAILED` suit §2.2. `BLOCKED` suit §2.1.** Elles ne s'appliquent jamais au même
> état, et la seconde n'écrase pas la première.

Sans cette précision, une deuxième tentative recevait « créer la tâche corrective » au
lieu de « changer d'approche, cause à nommer » — et l'opérateur ne pouvait plus
comprendre pourquoi la tâche avait cessé de revenir.

### La boucle ne croit pas le compte rendu

Principe posé par le LOT-04, à conserver au-delà du lot : **la boucle relit l'état en
base.** Si l'agent n'a rien déclaré, elle déclare à sa place — diagnostic,
`next_action`, `next_owner`.

Une règle demande la coopération de celui qu'elle contraint ; un mécanisme non. Un
agent muet ne peut plus terminer sans laisser de suite : le blocage porte alors
« l'agent n'a rien déclaré », et la suite va au Chief of Staff.

### 2.1 Diagnostic de blocage

| Nature du blocage | `next_action` | `next_owner` |
| --- | --- | --- |
| technique | créer la tâche corrective | la direction elle-même |
| permission / accès | vérifier le Preflight, ouvrir le droit | `chief-of-staff` |
| information manquante | recherche assignée | la direction elle-même |
| décision nécessaire | escalade | `ceo` puis `sam` |
| dépendance d'un autre agent | tâche assignée | l'autre direction |

### 2.2 Budget d'échec

| Tentative | Comportement |
| --- | --- |
| 1re | reprise directe, `retry_at = now() + 10 min` |
| 2e | **changement d'approche** — l'agent doit nommer la cause avant de réessayer |
| 3e | escalade au CoS, qui décide : réassigner, changer d'approche, ou remonter |

### 2.3 Reprise

Toute tâche `failed` dont `retry_at` est dépassé **revient automatiquement dans la
file**. C'est ce qui distingue un moteur d'exécution d'un ordonnanceur.

---

## 3. Preflight — mandat ↔ capacité

Huit contrôles avant chaque ronde. Un agent NOT READY **ne rentre pas dans la ronde**.

```
✓ Tools        les outils existent et répondent
✓ Credentials  les clés sont présentes et valides
✓ Permissions  le curseur autorise l'action
✓ Mounts       les chemins sont montés, en lecture ou écriture
✓ APIs         les services externes répondent
✓ Budget       il reste de quoi travailler
✓ Policy       le canal imposé est cohérent avec l'outil
✓ Evidence     il existe un moyen de prouver le travail
```

### 3.1 Le paradoxe du Preflight — règle obligatoire

> **Une alerte Preflight est automatiquement assignée au Chief of Staff**, qui
> détermine si elle doit être corrigée par l'agent concerné, par une autre fonction,
> ou par Sam.

Sans cette règle on obtient : « tu n'as pas les moyens de travailler → voici une tâche
→ travaille pour obtenir les moyens ». L'agent bloqué ne peut pas se débloquer seul.

---

## 4. Hiérarchie et droits

```
SAM   ──  stratégie, arbitrages majeurs, objectifs
CEO   ──  priorisation, arbitrage opérationnel dans son mandat,
          peut ordonner des tâches dans le cadre des objectifs approuvés
CoS   ──  séquencement, assignation, validation des clôtures
AGENTS ── exécution
```

### 4.0bis Les sept axes de curseur

`observer` · `ecrire_base` · `agir_production` · `engager_depense` ·
`envoyer_externe` · `modifier_dispositif` · **`ecrire_code`**

Le septième a été ajouté le 18/08 sur signalement du LOT-06. `modifier_dispositif`
désigne le dispositif du comité — fiches, scripts, garde-fous. Il est à 1 pour toutes
les directions. Y rattacher l'écriture de code rendait le mécanisme inopérant : le
Delivery n'aurait pas pu pousser sur `delivery/correctifs`, ce pour quoi le montage du
15/08 a été fait.

État en base au 18/08 : **neuf directions, sept axes chacune.** `ecrire_code` est à 3
pour le seul Delivery, canal imposé `/repo-delivery` branche `delivery/correctifs`.

### 4.1 Droits sur un objectif

| Acteur | Droit |
| --- | --- |
| Sam | crée, modifie, supprime |
| CEO | propose, avec motif |
| CoS | **aucun** |
| Direction | propose, avec motif et impact chiffré |
| Agent d'exécution | **jamais** |

Protection contre l'optimisation opportuniste : un agent ne doit pas pouvoir résoudre
son indicateur en modifiant son indicateur.

### 4.2 Suppléance du Chief of Staff

**Arbitrage de Sam.** Si le CoS est NOT READY ou indisponible :

```
CoS indisponible  ──►  alerte au CEO
                       CEO prend sa place momentanément
                       CEO alerte Sam
```

Suppléance tracée, qui prend fin au retour du CoS.

### 4.3 Escalade des validations

```
propose_cloture
   < 24 h  →  CoS valide
   > 24 h  →  alerte au CEO
   > 48 h  →  remontée à Sam
```

---

## 4bis. Les quatre dimensions d'un mandat

```
DELIVER      tenir ses objectifs opérationnels
IMPROVE      rendre son domaine plus rapide, moins cher, plus fiable
CHALLENGE    contester ce que l'entreprise tient pour acquis
ANTICIPATE   voir ce que personne ne regarde
```

**Motif.** Une organisation qui n'a que la première dimension exécute parfaitement une
stratégie moyenne.

> **Aucun directeur n'est uniquement responsable de son département. Tous sont
> responsables de la réussite de Digital·Humans.**

### Obligation de challenge — hebdomadaire

1. Quelle hypothèse actuelle penses-tu fausse, fragile ou insuffisamment exploitée ?
2. Quelle opportunité personne n'est actuellement en train de regarder ?

**Garde-fou obligatoire :**

> **Un challenge qui ne produit pas une hypothèse TESTABLE n'est pas rendu.**

| Élément exigé | Sans quoi |
| --- | --- |
| une formulation réfutable | c'est une opinion |
| un coût d'expérimentation | c'est un vœu |
| un critère de réfutation | on ne saura jamais si elle était fausse |

Même mécanisme que `next_action` pour les blocages. **Vérifiable mécaniquement.**

### Strategic Yield — et le seuil de rappel

```
proposition ──► acceptée ? ──► expérimentée ? ──► résultat ? ──► impact ?
```

**Qui juge : Sam.** Ce sont des propositions d'amélioration, pas des points bloquants.

> **Une proposition sans réponse n'est pas un refus.**

| Délai | Comportement |
| --- | --- |
| 14 jours sans réponse | le CEO le rappelle **une fois** |
| au-delà | veille : **ni perdue, ni comptée comme refusée**, sort du calcul |

### Droit du CEO de sortir du backlog

Le CEO peut proposer une initiative absente du backlog. **Arbitrage de Sam : c'est un
droit de PROPOSITION, pas d'initiative.** Le CEO soumet, Sam valide. Précaution de
départ, réexaminable.

### Strategic Challenge mensuel — activable

Sept questions du CEO à chaque direction. Et une règle qui prime :

> **Une direction doit pouvoir contredire le CEO et Sam.** Avec ses preuves et une
> alternative. Un comité qui confirme les intuitions du dirigeant ne sert à rien.

### Innovation Budget — activable

10 à 15 % de la capacité peut aller à des initiatives hors feuille de route. Sans cette
réserve, tout est aspiré par le lancement et personne ne construit le Digital·Humans
de 2027.

---

## 5. Organisation cible

| Fonction | État | Cadence |
| --- | --- | --- |
| CEO | active | quotidienne |
| Chief of Staff | active | quotidienne |
| Delivery | active | quotidienne |
| Growth (Commercial + Marketing, **temporaire**) | active | quotidienne |
| Juridique | veille | à la demande |
| Financier | veille | à la demande + passe hebdomadaire |
| Customer Success | veille | au premier client |

### Principe d'activation — fondement DEOS

> **On prépare et on valide tout. On active selon la situation.**

| Mécanisme | État à la livraison | Condition d'activation |
| --- | --- | --- |
| Rondes des 4 fonctions actives | actif | — |
| Mandats Finance, Legal, CS | écrits, dormants | bascule sur matériel dédié |
| Challenge hebdomadaire | implémenté, en essai | validation après quelques tours |
| Strategic Challenge mensuel | implémenté, inactif | décision après le lancement |
| Boucle d'intelligence collective | implémentée, inactive | idem |
| Innovation Budget | implémenté, inactif | idem |

**Motif :** éviter tout effet de bord avant le lancement, tout en ayant la certitude
que le mécanisme fonctionne le jour où on l'active.

---

## 6. La ronde V2

Cinq questions, quelques centaines de mots. **Pas de rapport d'état du monde.**

1. Où suis-je par rapport à mes objectifs ?
2. Qu'est-ce qui a avancé depuis hier ?
3. Qu'est-ce qui est bloqué, et par quoi ?
4. **Quelle action est-ce que j'entreprends maintenant ?**
5. Quelle décision humaine m'est nécessaire ?

Puis la session d'exécution, distincte, qui traite la file.

---

## 7. Dette explicitement acceptée

> **P0 — dette de sécurité connue, tolérance temporaire explicitement acceptée.**

Le Policy Engine complet ne fait pas partie du socle V2. Un Policy Engine **minimal**
couvre les trois capacités où le contrôle actuel est faux : écriture en base, écriture
dans les dépôts, envoi externe.

Formulation délibérée : elle empêche qu'un compromis temporaire devienne une dette
permanente. À réexaminer à date fixe.

---

## 8. Ce qui reste ouvert

Ne pas inventer en cours d'implémentation : **signaler**.

> **Ce fichier fait foi.** Quand un point est tranché, il l'est ici. Les lots et les
> fiches peuvent le citer, jamais le contredire. Un lot qui présente comme ouvert un
> point tranché ci-dessous a tort — signalez-le.

### Encore ouverts

1. Coût cible du comité (aujourd'hui 196 USD/mois sur 253 de facture). Piste : bascule
   sur matériel dédié pour passer d'un coût variable à un forfait.
2. Ce qu'un commit doit modifier pour valoir preuve — un commit vide passerait.
3. Concurrence entre agents sur un même périmètre : verrou ou séquencement ? Cas précisé
   par le LOT-04 : **deux sessions sur la même direction prendraient la même tâche.**
4. Obligations réglementaires datées du Juridique pendant sa veille.
5. Canal imposé de Growth, qui cumule Salesforce et Ghost.
6. Date ou condition de re-séparation de Growth.
7. Avancement d'une tâche `TIMEBOX_EXPIRED` : il ne vit que dans le journal, faute de
   colonne. Signalé par le LOT-04.

### Tranchés — ne plus les rouvrir

| Point | Arbitrage | Date |
| --- | --- | --- |
| Droit du CEO à sortir du backlog | Droit de **proposition** soumis à Sam, pas d'initiative. Précaution de départ, réexaminable. | 17/08 |
| Qui juge l'acceptation dans le Strategic Yield | **Sam.** Avec seuil de rappel : 14 jours sans réponse → un rappel unique, puis veille — ni perdue, ni comptée comme refusée. | 17/08 |
| Fréquence du Preflight | **Avant chaque ronde.** Mesure du LOT-05 : 0,8 s pour les quatre directions actives. Une passe quotidienne laisserait une fenêtre d'une journée pendant laquelle un montage perdu ou une clé expirée passe inaperçu — soit la durée exacte des pannes que le lot supprime. | 18/08 |
| Rattachement de `repo.write` | **Nouvel axe `ecrire_code`**, distinct de `modifier_dispositif`. Ce dernier désigne le dispositif du comité, pas un dépôt de la plateforme. Sous `modifier_dispositif` (à 1 partout), le mécanisme était implémenté, testé et inopérant. | 18/08 |
| Champs de blocage sur `decisions` | **Ajoutés.** Une décision peut être bloquée avant qu'aucune tâche n'existe — cas fréquent au sortir du Recovery Sprint. Sans ces colonnes, le LOT-03 ne pouvait pas appliquer sa propre règle. | 18/08 |
| Qui peut poser `en_execution` | **La direction porteuse**, en plus de `cos`, `ceo`, `sam`. Sinon la boucle d'exécution ne peut pas démarrer sans passer par le CoS, et le goulot renaît au premier pas. | 18/08 |
| Définition de « la direction porteuse » | Celle nommée `owner` d'au moins une tâche de la décision ; à défaut de tâche, l'origine. En cas d'écart, **accepter et signaler** plutôt que refuser : durcir plus tard est trivial, débloquer un refus injustifié coûte des jours. | 18/08 |
| Date de réexamen de la dette P0 | **1er novembre 2026**, un mois après le lancement. | 18/08 |
| Nombre d'états de fin | **Cinq**, `TIMEBOX_EXPIRED` compris. Ni un échec, ni un blocage. Relevé par le LOT-04. | 18/08 |
| Précédence des tables de routage | `FAILED` suit §2.2 (rang de tentative), `BLOCKED` suit §2.1 (nature). Jamais le même état. | 18/08 |
| Fichiers de configuration | **Séparés** : `config/preflight.yaml` et `config/policy.yaml`. Un fichier partagé recréerait le conflit à chaque évolution. | 18/08 |
| Ordre d'application des migrations | Celui de la **dépendance**, pas de l'alphabet. Voir `docs/APPLICATION_MIGRATIONS.md`. | 18/08 |
