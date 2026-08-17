# Moteur de politique — contrôle par capacité

**LOT-06 de la refonte DEOS Governance V2 · 17 août 2026**
Fichiers : `bin/policy.py` · `config/capabilites.yaml` ·
`.claude/hooks/pretooluse-guard.sh` · `tests/garde-fou.sh` · `tests/policy.sh`

---

## 1. Pourquoi le contrôle syntaxique échoue — dans les deux sens

Le garde-fou posait une question sur une **chaîne de caractères** : « cette
commande contient-elle `UPDATE` ? », « contient-elle `curl … -d` ? ». La question
juste porte sur une **action** : « cette commande écrit-elle en base ? »,
« expédie-t-elle quelque chose au dehors ? ». L'écart entre les deux produit des
erreurs dans les deux directions, et c'est le même défaut qui les cause.

### Faux négatif — le curseur qui n'existait que sur le papier

Les deux outils par lesquels le comité écrit réellement en base, `deos-decisions`
et `deos-state`, ne contiennent **aucun motif SQL**. Le contrôle ne les voyait
pas. Conséquence exacte, vérifiée avant modification :

```
$ printf '%s' '{"tool_name":"Bash","tool_input":{"command":"bin/deos-decisions status DEC-X clos --par delivery"}}' \
  | DH_DIRECTION=delivery bash .claude/hooks/pretooluse-guard.sh.pre-policy
$ echo $?
0
```

Le curseur `ecrire_base` du Delivery est réglé sur 2 — « Propose, n'écrit pas »
(réglage de Sam du 06/08). Ce réglage était **affiché au tableau de bord et
appliqué nulle part**. Le seul contrôle qui fonctionnait était le blocage du SQL
brut, c'est-à-dire la voie que personne n'emprunte.

C'est ce que le Delivery avait lui-même constaté le 14/08 : *« le garde-fou ne
bloque que le SQL brut INSERT/UPDATE/DELETE, pas les CLI dédiées »*. Le constat
était juste ; il n'a pas été suivi d'effet pendant trois jours.

### Faux positif — le document pris pour un acte

Symétriquement, chercher `curl … --data` **n'importe où** dans la commande
refuse un document qui *cite* un appel. Le 11/08, le Marketing a vu l'écriture
de son support visuel refusée : son fichier reproduisait, à titre d'exemple, une
ligne de journal contenant cette séquence. Aucun appel n'était tenté. Le
Commercial a ensuite reproduit le refus **en direct** en rédigeant l'addendum qui
l'expliquait — il a dû retirer la séquence littérale de son propre document pour
pouvoir l'écrire.

Le 17/08, cinq faux positifs dans quatre directions en un matin, dont le blocage
d'un correctif de sécurité que Sam avait validé le 13/08. La règle de vidage par
redirection cherchait un `>` et un chemin protégé sans regarder **de quel côté du
chevron** se trouvait le chemin : `cat /workspace/config/offre_dh.md >
/tmp/copie.md` — une lecture — était refusé.

### Ce que les deux ont en commun

Un faux négatif et un faux positif semblent opposés ; ils ont ici la même cause.
Chercher des mots dans une chaîne, c'est confondre le **texte** de la commande
avec ce qu'elle **fait**. Un outil peut agir sans le mot, un document peut porter
le mot sans agir. Tant qu'on ne distingue pas le programme invoqué de la donnée
qu'il transporte, on se trompe des deux côtés — et le durcissement d'un côté
aggrave l'autre.

**Coût observé du côté faux positif** : 87 refus journalisés au total, dont 24
`DH-FS-001` sur la seule semaine du 11 au 17/08. Une direction qui apprend qu'un
refus est probablement une erreur cesse de traiter les refus comme des limites.
C'est le vrai danger : le contrôle qui crie trop souvent finit ignoré, y compris
quand il a raison.

---

## 2. Ce que le moteur contrôle

Trois capacités — celles où le contrôle était faux (SPEC §7).

| Capacité | Ce qui la déclenche | Curseur | Cran requis |
| --- | --- | --- | --- |
| `db.write` | `deos-decisions`, `deos-state`, `deos-tasks`, `psql` non-lecture | `ecrire_base` | 3 |
| `repo.write` | `git` avec une sous-commande qui mute | `modifier_dispositif` | 4 |
| `external.send` | `curl`/`wget` expédiant des données, `mail`/`sendmail`/`mutt`/`msmtp`, `sf-lead` | `envoyer_externe` | 3 |

Les crans requis **reprennent à l'identique** ceux que le garde-fou exigeait déjà.
Ce lot ne durcit ni n'assouplit la politique : il la rend applicable. La seule
chose qui change, c'est que le réglage affiché est désormais celui qui décide.

`deos-tasks` (LOT-02) est déclaré avant d'exister. C'est le sens d'une
correspondance déclarative : l'outil naîtra contrôlé au lieu d'être rattrapé
après coup — le scénario qui a produit le trou qu'on rebouche ici.

---

## 3. Comment il décide

### Trois gestes, dans cet ordre

1. **Retirer les corps de heredoc.** Un heredoc n'est pas du code, c'est de la
   donnée écrite dans un fichier. C'est la citation d'un `curl -d` *dans* un
   heredoc qui a fait refuser le support visuel du Marketing.
2. **Découper en commandes simples**, sur `;`, `&&`, `||`, `|`, `(`, `$(`.
3. **Identifier le programme en position d'exécution**, dépouillé de son chemin
   et des affectations d'environnement qui le précèdent. `bin/deos-decisions`,
   `./deos-decisions` et `/workspace/bin/deos-decisions` sont le même outil.

Une règle appliquée à la bonne sous-chaîne vaut mieux qu'une règle savante
appliquée à la ligne entière.

### Les analyseurs — distinguer deux usages d'un même programme

`psql` lit ou écrit. `git` observe ou mute. `curl` consulte ou expédie. Sans
cette distinction il faudrait choisir entre refuser tous les `SELECT` et laisser
passer tous les `UPDATE` : remplacer un faux négatif par un faux positif.

Trois analyseurs, nommés dans le YAML, implémentés dans `policy.py` :
`psql_ecriture`, `git_ecriture`, `envoi_http`.

**Règle de doute, uniforme :** on ne classe en lecture que ce qu'on a pu lire et
reconnaître comme tel. `psql -f fichier.sql` est traité comme une écriture — la
requête n'est pas vérifiable depuis la commande. Une session interactive aussi.
Se tromper vers la lecture ouvre la base ; se tromper vers l'écriture coûte un
refus motivé, que la direction rapporte.

### Ce qui reste déclaratif

Ajouter un outil, c'est ajouter une ligne `programme:` dans
`config/capabilites.yaml`. Aucun code à toucher — contrat du lot, point 2. Les
sous-commandes git qui mutent y sont aussi : c'est une donnée de politique, pas
une règle de langage.

Ce qui n'y est **pas** : les niveaux des curseurs. Ils restent en base, réglés
par Sam. Le fichier dit quel curseur gouverne quelle capacité ; il ne dit jamais
à quel cran il est réglé. Une direction qui lirait ce fichier n'y trouve pas de
quoi élever ses droits.

---

## 4. Le crochet — qui décide quoi

```
commande Bash
   │
   ├─ MOTEUR ─────────────────────────────────────────────────
   │    DENY  → refus immédiat, motif nommant le curseur
   │    ALLOW → on continue, les interdictions absolues suivent
   │    NON APPLICABLE (direction hors périmètre)
   │          → le garde-fou reprend ses règles d'origine
   │    ERREUR → repli sur les règles d'origine + alerte au CoS
   │
   └─ INTERDICTIONS ABSOLUES, inchangées ──────────────────────
        DH-DEL-001 (systemctl, docker, kill) · DH-DEL-002 (prod)
        DH-FS-001 (destruction de fichiers) · DH-COS-002 · R14
```

**Un ALLOW du moteur ne dispense d'aucune interdiction absolue.** Le cas 6 de
`tests/garde-fou.sh` le prouve : joué avec le Chief of Staff, dont
`ecrire_base` vaut 4, le moteur autorise — et `DH-COS-002` refuse quand même le
SQL direct sur `decisions`. C'est exactement ce qu'énonce la justification de son
curseur : *« aucune écriture SQL directe : elle est bloquée par DH-COS-002 même
au niveau autonomie »*.

### Pourquoi ERREUR ne refuse pas tout

Un moteur de sécurité qui laisse passer quand il tombe en panne ne protège rien.
Mais un moteur qui refuse **tout** arrête les rondes pour un YAML mal formé — et
la commande refusée serait alors `ls` autant que `deos-decisions`.

Le repli retenu est le contrôle **d'avant ce lot** : faux dans les deux sens,
mais borné, connu, et jamais plus permissif qu'hier. Il est journalisé
(`POLICY-ERREUR`) et annoncé à l'agent comme une **alerte de capacité**, à
remonter au Chief of Staff — application de SPEC §3.1 : *une alerte de capacité
est assignée au CoS*, jamais à l'agent qu'elle bloque.

### Pourquoi les directions non gouvernées échappent au moteur

`config/capabilites.yaml` liste les directions gouvernées. Une direction absente
de cette liste rend `NON_APPLICABLE`, et le garde-fou applique ses règles
d'origine, à l'identique.

Sans cette sortie, la session de **Sam** serait bloquée par son propre garde-fou :
`DH_DIRECTION` n'y est pas défini, et Sam n'a aucune ligne dans la table
`curseurs` — il tomberait au défaut restrictif 1 et ne pourrait plus lancer
`deos-decisions`. On aurait bloqué le propriétaire du dispositif en croyant
durcir la sécurité des agents.

**Limite connue**, à lire avec la dette P0 : un agent dont `DH_DIRECTION` ne
serait pas défini échapperait au moteur. La variable est posée par
l'orchestrateur (`bin/rondes.sh`), pas par l'agent, et une commande ne peut pas
modifier l'environnement du crochet qui l'inspecte. Le repli reste le garde-fou
textuel — jamais plus permissif qu'avant ce lot.

---

## 5. Ce que le moteur ne remplace pas

### `DH-x-001` reste un refus inconditionnel

Le contrôle **par curseur** de l'envoi externe est délégué au moteur. Le refus
**inconditionnel** `DH-x-001` (`curl -X POST`, `mail`) ne l'est pas : il subsiste
après le moteur, pour toutes les directions.

Conséquence, à connaître avant de régler un curseur : relever
`envoyer_externe` à 3 **ne suffira pas** à ouvrir l'envoi par `curl` ou par
courriel — `DH-x-001` refusera encore. Lever cette interdiction est une décision
distincte, qui revient à Sam. Elle est cohérente avec
`config/agent_autonomy_map.yaml`, qui range `envoi_externe_engageant` parmi les
`toujours_validation`.

Le moteur ne peut donc, sur `external.send`, qu'**ajouter** des refus — jamais en
lever un. Là où il agit réellement dès aujourd'hui : `sf-lead`, que `DH-x-001` ne
couvrait pas, et la contrainte de canal.

*Note d'exécution : la délégation de `DH-x-001` au moteur a été tentée puis
abandonnée — la couche de permissions de la session a refusé la modification, au
motif qu'elle supprimait une interdiction inconditionnelle d'envoi externe. Le
refus n'a pas été contourné. Le faux positif du 11/08 est donc corrigé **dans le
moteur** et subsiste **dans `DH-x-001`** : un document citant `curl … --data`
sera toujours refusé à l'écriture. C'est une correction à porter séparément, avec
l'accord explicite de Sam.*

### Ce qui reste au garde-fou, et pourquoi

`agir_production`, `engager_depense`, la protection du système de fichiers
(`DH-FS-001`), la modification du dispositif par redirection, `R14`,
`DH-DEL-001/002`, `DH-COS-002`. Aucune de ces règles ne relève des trois axes du
socle minimal. Les toucher aurait élargi le lot sans nécessité — et chaque règle
touchée est une régression possible.

---

## 6. Ce qui est implémenté et dormant

Application de SPEC §5 : *on prépare et on valide tout, on active selon la
situation.*

| Mécanisme | État | Ce qui l'activera |
| --- | --- | --- |
| Canal imposé (`external.send`) | implémenté, testé, sans effet | un curseur `envoyer_externe` ≥ 3 |
| Branche imposée (`repo.write`) | implémenté, testé, sans effet | un curseur `modifier_dispositif` ≥ 4 |

Sans effet aujourd'hui parce qu'**aucune direction n'atteint le cran requis** :
la contrainte de niveau refuse avant que celle de canal ou de branche ne soit
examinée. Les cas 13 à 18 de `tests/policy.sh` les éprouvent en fournissant au
moteur les crans qu'aucune direction n'a encore — sans quoi ces mécanismes
resteraient invérifiés jusqu'au jour de leur activation, c'est-à-dire au pire
moment.

---

## 7. Dette P0

> **P0 — dette de sécurité connue, tolérance temporaire explicitement acceptée.**
>
> Le Policy Engine complet ne fait pas partie du socle V2. Un Policy Engine
> **minimal** couvre les trois capacités où le contrôle actuel est faux :
> écriture en base, écriture dans les dépôts, envoi externe.

Formulation reprise de SPEC §7, délibérément. Elle empêche qu'un compromis
temporaire devienne une dette permanente.

**Date de réexamen proposée : 1er novembre 2026** — un mois après le lancement du
1er octobre, quand la sortie ne mobilise plus toute la capacité. La SPEC exige
une date fixe sans en donner une ; celle-ci est **proposée, à confirmer par Sam**,
et adossée au calendrier connu plutôt que choisie au hasard.

Ce que la dette recouvre concrètement :

- le découpage shell est une approximation, pas un interpréteur bash ;
- une capacité obtenue par un chemin non déclaré (un script maison qui appelle
  `psycopg2`, par exemple) n'est pas vue — le contrôle porte sur les outils
  connus, pas sur les effets ;
- `Write` et `Edit` ne passent pas par le moteur ;
- la limite de la direction non déclarée, décrite au §4.

---

## 8. Ce qui n'est pas tranché — à arbitrer par Sam

Signalé, pas décidé.

**a. `repo.write` et le curseur `modifier_dispositif`.** Le lot rattache
l'écriture git à ce curseur. Il est à 1 pour **toutes** les directions (*« peut
proposer une évolution, ne la pose jamais »*, R14). Appliqué tel quel, le
Delivery ne peut pas pousser sur `delivery/correctifs` — alors que le montage du
14/08 a été fait exactement pour ça : *« Il pousse sur la branche
delivery/correctifs, Sam relit et fusionne. »*

Le mécanisme est implémenté et inopérant en l'état. Deux issues possibles :
relever `modifier_dispositif` pour le Delivery, ou créer un curseur distinct pour
l'écriture de code — `modifier_dispositif` désigne le dispositif du comité
(prompts, garde-fous, curseurs), pas un dépôt de la plateforme. **Je n'ai pas
créé ce curseur** : ce serait inventer une ligne de gouvernance à la place de Sam.

**b. Le CEO n'avait aucun curseur — tranché le 17/08.** La table `curseurs`
(36 lignes, sauvegarde du 11/08) ne contenait aucune ligne pour lui, alors que
`config/agent_autonomy_map.yaml` lui donne `arbitrage_operationnel: autonomie`.
Signalé le jour même ; **Sam pose le réglage en base, avec celui de Growth**.

Le moteur gouverne donc `ceo` et `growth` **avant** que leurs lignes n'existent.
C'est délibéré : une fonction absente de `directions_gouvernees` n'est pas
contrôlée du tout. Tant que la base ne porte pas les réglages, le défaut
restrictif s'applique et le motif le dit — *« aucun réglage déclaré »*. Une
direction qui ne travaille pas encore et qui est bloquée se voit ; une direction
qui travaille sans contrôle ne se voit pas.

Growth y figure pour la même raison, bien que sa fiche relève du LOT-07 : si sa
fonction naissait avant que le moteur ne la connaisse, elle cumulerait les
capacités du Commercial et du Marketing sans curseur opposable. **Reste ouvert :
son canal** — voir le point c.

La divergence de fond subsiste et n'est pas de ce lot : `agent_autonomy_map.yaml`
et la table `curseurs` emploient deux taxonomies différentes (`arbitrage_
operationnel` d'un côté, `ecrire_base` de l'autre) sans correspondance écrite.
Le garde-fou n'a jamais lu que la table. Le YAML décrit une gouvernance que rien
n'applique.

**c. SPEC §8 point 6 — canal imposé de Growth.** Non tranché, non inventé. Ni
Growth ni le Marketing n'ont de canal déclaré dans `capabilites.yaml`. Le dépôt
de brouillons Ghost n'a pas d'outil dédié dans `bin/` : il n'y a rien de nommable
comme canal sans décider à la place de Sam. Une direction sans canal déclaré
n'est soumise qu'à son niveau de curseur.

**d. Observation, hors périmètre de ce lot.** `charger_curseurs` écrit le
résultat de `psql` dans le cache par redirection : si la base est injoignable, le
cache est **vidé**, et toutes les directions retombent au cran 1. Le repli est
restrictif, donc sûr, mais il est silencieux — un incident de base se manifeste
comme un blocage général inexpliqué. Signalé, non corrigé : ce n'est pas un des
trois axes.

---

## 9. Vérification

```bash
bash tests/garde-fou.sh    # non-régression, attendu 12/12
bash tests/policy.sh       # moteur, attendu 10/10 puis 11/11
```

Les douze cas de non-régression **n'existaient pas** avant ce lot : ni script, ni
liste. Le garde-fou avait été corrigé quatre fois — `FIX-GUARD-001` le 04/08, le
curseur le 06/08, `DH-FS-001` le 14/08, la redirection le 17/08 — sans qu'aucune
de ces corrections soit protégée par un test. C'est ainsi qu'un correctif se
perd puis se re-diagnostique depuis zéro quelques jours plus tard.

Ils ont donc été **reconstitués** à partir du code du garde-fou et des incidents
que ses commentaires citent, un cas par règle. À lire comme une reconstitution,
pas comme un héritage.

Preuve que c'est bien une non-régression et non une suite écrite pour le code
neuf — les douze cas passent aussi sur la sauvegarde d'avant :

```bash
DH_CROCHET="$PWD/.claude/hooks/pretooluse-guard.sh.pre-policy" bash tests/garde-fou.sh
# 12/12
```

La sauvegarde `.pre-policy` est locale : `.gitignore` écarte les `*.pre-*`
depuis le 14/08, au motif que git assure déjà cette fonction. Elle n'est donc
pas dans le dépôt, et la commande ci-dessus ne rejouera pas telle quelle sur un
clone neuf. Pour la reconstituer :

```bash
git show <commit-du-LOT-06>^:.claude/hooks/pretooluse-guard.sh > /tmp/garde-fou-avant.sh
DH_CROCHET=/tmp/garde-fou-avant.sh bash tests/garde-fou.sh
```

Les curseurs utilisés par les tests proviennent de
`config/curseurs_sauvegarde_2026-08-11.csv` — les réglages réels de Sam. Une
suite qui inventerait ses propres niveaux prouverait que le moteur sait lire un
fichier, pas qu'il applique la gouvernance réelle.

---

## 10. Journal des fichiers

| Fichier | Action | Sauvegarde |
| --- | --- | --- |
| `bin/policy.py` | créé — le moteur | — |
| `config/capabilites.yaml` | créé — le lot le disait « à étendre », il n'existait pas | — |
| `.claude/hooks/pretooluse-guard.sh` | modifié — délégation des 3 capacités | `.pre-policy` |
| `tests/commun.sh`, `tests/garde-fou.sh`, `tests/policy.sh` | créés | — |
| `Dockerfile` | modifié — ajout de `python3-yaml` | — |
| `docs/POLICY_ENGINE.md` | créé — ce fichier | — |

Deux changements de forme dans le crochet, motivés :

- **la racine se déduit** de l'emplacement du fichier au lieu d'être écrite en
  dur. Le serveur (`/root/workspace/dh-comite`), le conteneur (`/workspace`) et
  un clone de travail ont trois racines différentes : en fixer une rendait le
  crochet inexécutable ailleurs, donc **intestable hors production**. C'est la
  raison pour laquelle il n'avait jamais été testé.
- **le journal suit la racine** (`$RACINE/hooks.log`), pour la même raison. Sur
  le serveur et dans le conteneur, le chemin résolu est inchangé.
