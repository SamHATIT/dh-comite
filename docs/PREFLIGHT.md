# Preflight — mandat ↔ capacité

> Vérifie, avant chaque ronde, qu'une direction a les **moyens** de tenir son mandat.
> Un agent NOT_READY ne rentre pas dans la ronde. Son alerte part au Chief of Staff,
> jamais à lui-même.
>
> `bin/preflight.py` · `config/capabilites.yaml` · LOT-05 · 17 août 2026

---

## 1. Pourquoi ce contrôle existe

Six pannes en douze jours, toutes de la même famille : **un mandat sans le moyen de
l'exercer**. Le mandat était écrit dans la fiche de l'agent. La capacité vivait
ailleurs — dans `docker-compose.yml`, dans un `.env`, dans la table `curseurs`. Rien
ne rapprochait les deux.

Ce qui rend cette famille de pannes coûteuse n'est pas la panne : c'est le **délai de
diagnostic**. Dans les trois premiers cas, c'est l'agent lui-même qui a fini par
trouver, après plusieurs jours pendant lesquels le comité a lu son silence comme de la
négligence. Le 14/08, trois feux verts donnés par Sam le 13/08 étaient inexécutables
faute d'accès en écriture ; le Delivery l'a dit — « BLOQUÉE, accès manquant » — dès
qu'on lui a demandé un état ligne par ligne, et pas avant, parce que personne ne lui
avait demandé. Ce qu'on lisait comme de l'inaction était une porte fermée.

Le Preflight déplace ce constat : **avant** la ronde, mécaniquement, plutôt qu'après
plusieurs jours et une relance personnelle.

### Le tableau qui justifie le lot

Chaque contrôle est né d'un incident précis. Sans cette colonne de droite, le
Preflight ressemblerait à de la bureaucratie ; avec elle, c'est un rattrapage de
pannes déjà payées.

| # | Panne constatée | Date | Trace dans le dépôt | Contrôle qui l'aurait vue |
| --- | --- | --- | --- | --- |
| 1 | **Backlog non monté.** Le Delivery tient le backlog des évolutions selon sa fiche, mais le conteneur ne montait pas le dépôt : il ne pouvait rien lire. Cause de son immobilisme sur ce point — signalée par lui-même. | 06/08 | `docker-compose.yml`, montage `/backlog` | `mounts` |
| 2 | **Dépôt en lecture seule.** Trois feux verts de Sam du 13/08 (correctif de sécurité B2, filtre de cloisonnement B3, garde-fou) supposaient d'écrire dans un dépôt monté en `ro`. Ils étaient INEXÉCUTABLES. | 13–14/08 | `docker-compose.yml`, montage `/repo-delivery` | `mounts` + `evidence` |
| 3 | **Route inexistante.** `bin/memoire` ne fonctionnait que depuis l'hôte : chromadb n'est pas dans le conteneur. Même semaine, le Commercial ne pouvait pas écrire dans Salesforce — ni le binaire `sf`, ni les identifiants côté conteneur. | 10/08 | `bin/memoire`, `bin/sf-lead` | `tools` + `apis` |
| 4 | **Clé absente.** Le dossier de conformité Hostinger est resté bloqué plusieurs jours : le lien d'accès arrivait par courriel et aucun agent ne pouvait relever la boîte. Le Juridique l'a constaté lui-même : « le lien arrive par un canal auquel je n'ai pas accès ». | 11/08 | `bin/mail-lire` | `credentials` |
| 5 | **Direction absente des rondes.** Le Juridique, créé le 02/08, n'était dans AUCUNE ronde — deux missions accordées, aucun livrable pendant quatre jours. Huit jours plus tard, le Financier : absent des rondes ET de la table `curseurs`, avec deux décisions assignées le 13/08 pour échéance au 15/08 qu'il n'aurait jamais vues. | 06/08 et 14/08 | `bin/rondes.sh`, FIX-LEGAL-001 et FIX-FINANCIER-001 | `permissions` |
| 6 | **Canal imposé sans outil derrière.** Un curseur annonce un canal ; la direction lit « passe par là » et n'a rien pour le faire. Consigne inapplicable, qu'aucun contrôle ne rattrapait. | — | `curseurs.canal_impose` | `policy` |
| 7 | **Aucun moyen de prouver.** Le Juridique n'avait aucun périmètre d'écriture dans `deos-state` : ses rapports étaient refusés **en silence**, d'où le « 0 rapport legal » constaté pendant cinq jours. Il travaillait ; rien n'arrivait. | 08/08 | `bin/deos-state`, table des scopes | `evidence` |
| 8 | **Plafond de budget franchi sans préavis.** 24 € d'Opus sur une journée contre 8 € de Sonnet, pour quatre missions lancées à la main. Personne ne l'a vu venir. | 08/08 | `bin/couts.py` | `budget` |

Les six pannes annoncées par le lot sont les lignes 1 à 6. Les lignes 7 et 8 sont les
deux incidents qui ont donné leur forme aux deux contrôles restants — le contrat en
demande huit, et chacun devait tenir à un fait, pas à une idée de complétude.

---

## 2. La règle du paradoxe

> **Une alerte Preflight est automatiquement assignée au Chief of Staff**, qui
> détermine si elle doit être corrigée par l'agent concerné, par une autre fonction,
> ou par Sam.

Sans cette règle, on obtient :

> « Tu n'as pas les moyens de travailler → voici une tâche → travaille pour obtenir
> les moyens. »

L'agent bloqué ne peut pas se débloquer seul, **par construction** : un montage se
répare dans `docker-compose.yml`, une clé dans un `.env`, un curseur dans une table
que seul Sam alimente. Trois endroits hors de sa portée — et hors de son curseur, qui
le tient en `Observe` sur `modifier_dispositif`. Lui assigner l'alerte reviendrait à
enregistrer une tâche dont on sait qu'elle ne peut pas aboutir.

**Comment la règle est tenue dans le code, et non seulement écrite ici.** Il existe
une seule fonction qui fabrique une alerte (`echec()`, `bin/preflight.py`). Elle
calcule le destinataire elle-même ; aucun appelant ne le fournit. Il n'y a donc pas de
chemin de code permettant d'assigner une alerte à la direction qu'elle bloque. Deux
filets doublent ce point unique : une vérification après chaque passe, qui lève une
erreur bruyante plutôt que d'émettre une alerte qui n'irait nulle part, et `--autotest`
qui rejoue la règle sur les sept directions déclarées.

**Une exception, et elle est spécifiée** (SPEC §4.2) : si c'est le CoS lui-même qui est
NOT_READY, l'alerte remonte au **CEO**, qui prend sa place momentanément et alerte Sam.
La règle tient dans les deux cas — jamais l'agent que l'alerte bloque.

**Ce que le Preflight ne fait pas.** Il n'enregistre pas de tâche. Il émet l'alerte,
avec `next_action` et `next_owner` renseignés, au format que consommera la boucle
d'exécution (LOT-04) et l'outil des tâches (LOT-02). Le Preflight ne dépend d'aucun
autre lot et n'écrit rien en base : c'est ce qui permet de le poser en vague A, avant
que la table `tasks` existe.

---

## 3. Les huit contrôles

| Contrôle | Ce qu'il vérifie concrètement | Échoue quand |
| --- | --- | --- |
| `tools` | chaque outil déclaré existe, porte le bit exécutable, et répond à `--help` sans effet de bord | absent · non exécutable · code 126/127 · ne rend pas la main en 10 s · trace d'exception |
| `credentials` | chaque clé déclarée est présente et non vide — dans l'environnement ou dans un fichier `.env` désigné | variable absente ou vide · fichier illisible · clé sans valeur |
| `permissions` | les six axes de `curseurs` existent en base **pour la clé que lira le garde-fou** | un axe manque pour cette direction |
| `mounts` | chaque chemin est monté, et dans le mode déclaré | répertoire absent · `ro` illisible · `rw` non inscriptible |
| `apis` | chaque service externe répond, délai court (5 s) | pas de réponse — sauf `optionnel: true`, qui dégrade en avertissement |
| `budget` | ce qui a été consommé sur la période, face au plafond | plafond atteint (voir §5, le plafond n'est pas tranché) |
| `policy` | le canal imposé du curseur désigne un outil qui existe | canal reconnu dont l'outil est absent ou non exécutable |
| `evidence` | il existe **au moins un** moyen de prouver le travail : un dépôt inscriptible ou une table accessible | aucun moyen déclaré · aucun moyen utilisable |

### Ce qui a été tranché en écrivant ces contrôles, et pourquoi

**`tools` — « répond à `--help` sans effet de bord » n'exige pas un code 0.**
Le 17/08 au matin, le Commercial a appelé `sf-lead --help`. Le script ne reconnaissait
aucun drapeau et a déposé le texte littéral « --help » dans la file Salesforce. Depuis
le correctif du même jour, `sf-lead --help` imprime son usage et sort en **2** : un
refus propre, pas une panne. Exiger un code 0 déclarerait cet outil cassé alors qu'il
vient d'être réparé. On exige donc que le processus **rende la main sans planter**.

Cette même journée impose le corollaire : `--help` n'est déclenché que sur les outils
qui savent le lire. `mail-lire` ouvre une session IMAP dès son lancement, `memoire`
consomme une requête d'index, `curseur-lire` prendrait « --help » pour un nom de
direction. Ces outils portent `verifier_aide: false` dans `capabilites.yaml`, chacun
avec la raison en commentaire. Un contrôle qui déclenche l'effet de bord qu'il prétend
éviter serait pire que pas de contrôle.

**`mounts` — on écrit vraiment.**
`os.access(W_OK)` ment sur un montage read-only quand on tourne en root : les bits de
permission sont satisfaits, et c'est le système de fichiers qui refuse, au moment de
l'écriture. Un contrôle fondé sur `os.access` aurait déclaré `/repo-delivery`
inscriptible le 13/08 — exactement la conclusion qui a rendu trois feux verts
inexécutables sans que personne ne le voie. Le contrôle crée donc un fichier témoin et
le supprime.

**Et il ne l'écrit jamais sous la plateforme.** Un montage `ro` n'est pas testé en
écriture, même pour vérifier qu'on ne peut pas : les chemins concernés sont ceux de la
plateforme, et I1 l'interdit. Ce n'est pas une convention d'écriture : la liste
`ZONES_PLATEFORME` refuse le test au niveau du code, quoi que déclare la configuration,
et `--autotest` vérifie qu'aucun montage `rw` ne pointe sous la plateforme.

**`permissions` — on vérifie la clé que lira le garde-fou, pas une clé théorique.**
`pretooluse-guard.sh` lit `DH_DIRECTION`, cherche la ligne dans `curseurs`, et retombe
sur le niveau 1 (`Observe`) s'il ne la trouve pas. Ce défaut restrictif est délibéré
côté garde-fou — mieux vaut tout refuser que tout permettre. Mais côté direction, il
produit une fonction **muette dont personne ne sait qu'elle est muette** : elle n'est
pas bloquée bruyamment, elle est réglée sur Observe sans que quiconque l'ait voulu.
C'est ce qui est arrivé au Juridique le 06/08 et au Financier le 14/08.

Le cas de Growth en est la version à venir : SPEC §5 fusionne Commercial et Marketing,
la table ne connaît que les deux anciennes clés. Si une ronde tourne sous
`DH_DIRECTION=growth`, le garde-fou ne trouvera rien. Le contrôle le dit dans ces
termes, avec les deux issues possibles — reporter les curseurs, ou faire tourner la
ronde sous les anciennes clés — sans choisir : le report des curseurs est une écriture
dans une table dont la colonne `maj_par` porte `sam` sur les 36 lignes.

**`policy` — corrigé pendant l'implémentation, et c'est la correction la plus utile
du lot.**
La première version associait une **clé** de canal à un outil, en supposant que
`curseurs.canal_impose` contenait un identifiant. Vérification faite sur la sauvegarde
du 11/08 : la colonne contient de la **prose**. « Exclusivement via loutil
deos-decisions, qui trace auteur, date, preuve et justification. » « Lecture seule sur
les vues v_deos_* uniquement. » Le contrôle aurait donc déclaré inconnu chacun des
sept canaux réellement en base, et rendu NOT_READY toutes les directions dès la
première ronde.

C'est le défaut du 17/08 au matin, à l'identique : un garde-fou qui bloque le travail
normal, cinq faux positifs dans quatre directions en une matinée, dont le blocage d'un
correctif que Sam avait validé. Un contrôle qui crie faux n'est pas cru la troisième
fois — et il n'y a rien de plus coûteux qu'un dispositif de sécurité qu'on a appris à
ignorer.

La reconnaissance se fait donc par **motifs** cherchés dans la prose, avec trois
issues : motif reconnu et outil déclaré → l'outil doit exister ; motif reconnu sans
outil (le canal est une contrainte d'accès, comme les vues `v_deos_*`) → rien à
vérifier ; **aucun motif reconnu → avertissement, jamais échec**. On ne bloque pas une
ronde sur une phrase qu'on n'a pas su lire. On dit qu'on n'a pas su la lire.

**`evidence` — au moins un moyen, pas tous.**
Une direction peut prouver par un dépôt ou par une table ; exiger les deux
produirait des NOT_READY sur des fonctions parfaitement capables de travailler. Les
moyens indisponibles restants sont reportés en avertissement, pour qu'une dégradation
progressive reste visible avant de devenir bloquante.

---

## 4. Configuration — `config/capabilites.yaml`

Le fichier déclare, par direction : `outils`, `credentials`, `mounts`, `apis`,
`budget`, `evidence`, la clé `curseurs_direction`, l'`etat` et la `cadence`.

**Règle de tenue.** Quand on donne un moyen à une direction — un montage, une clé, un
outil — on le déclare ici. Sinon le Preflight ne saura pas qu'il manque le jour où il
disparaîtra. **Un moyen non déclaré est un moyen dont la perte sera silencieuse**, et
c'est précisément la propriété qui a coûté douze jours.

**Chemins.** Tout ce qui vit dans le dépôt est écrit **relativement à sa racine** :
`.`, `bin/sf-lead`, `PageSuivi.md`. Le serveur et un clone n'ont pas la même racine ;
un absolu recopié ne serait vrai qu'à un seul endroit. Restent absolus les seuls
chemins qui n'ont pas d'équivalent relatif : les points de montage du conteneur
(`/repo`, `/backlog`, `/prodlogs`, `/repo-delivery`), déclarés dans
`docker-compose.yml`. Ils n'existent pas dans un clone, et le Preflight le signale —
ce qui est exact, et non un faux positif.

**Fonctions en veille.** Juridique, Financier et Customer Success sont déclarés en
entier, avec tous leurs moyens, et marqués `etat: veille` (SPEC §5). Ils sortent de
`--toutes` et se vérifient à la demande ou avec `--dormantes`. Les retirer du fichier
violerait I2 : **on préserve tout, on arrête seulement la cadence**. Le jour de leur
réactivation, le Preflight saura immédiatement ce qui leur manque — c'est le contraire
du 06/08, où le Juridique a été activé sans que personne ne vérifie ses moyens.

### Pourquoi un parseur de repli

Le conteneur `dh-comite` est bâti sur `ubuntu:24.04` avec `postgresql-client`, `jq` et
un `python3` arrivé par `python3-matplotlib`. **PyYAML n'y est pas garanti**, et
rebâtir l'image pour une dépendance de confort supposerait de recréer le conteneur du
comité — un effet de bord plus coûteux que le problème qu'il règle, à six semaines du
lancement.

`preflight.py` utilise donc PyYAML s'il est présent, et sinon un parseur du
sous-ensemble YAML strictement employé par `capabilites.yaml` : mappings, listes de
scalaires, listes de mappings, commentaires, chaînes quotées, `null`/`true`/`false`,
entiers, listes en ligne `[a, b]`. Tout ce qui sort de ce sous-ensemble lève une erreur
nommée avec son numéro de ligne, plutôt que d'être lu de travers en silence.

`--autotest` compare les deux lectures du fichier livré quand PyYAML est disponible :
**l'équivalence est vérifiée, pas supposée.** Si un jour la configuration s'enrichit
au-delà du sous-ensemble, l'autotest le dira avant la ronde.

---

## 5. Points ouverts rencontrés — signalés, non tranchés

Trois des sept points ouverts de `SPEC.md §8` ont été touchés par ce lot. Aucun n'a été
tranché ici ; chacun est visible dans la sortie du Preflight plutôt que résolu par
défaut.

**SPEC §8.1 — coût cible du comité.** Le contrôle `budget` est implémenté et
fonctionnel, mais son seuil n'existe pas. `plafond_usd_mois` vaut `null` pour les sept
directions : le contrôle rapporte alors la consommation constatée et se déclare
**INDETERMINE**, sans bloquer. Un plafond inventé aurait deux défauts — il donnerait
l'apparence d'une décision qui n'a pas été prise, et il finirait par être cité comme si
elle l'avait été. Le jour où Sam fixe le chiffre, il se pose dans le fichier de
configuration, sans toucher au code.

**SPEC §8.6 — canal imposé de Growth**, qui cumule Salesforce et Ghost, et **SPEC §8.7
— date ou condition de re-séparation.** Aucun canal imposé n'est écrit pour Growth : le
contrôle `policy` lit ce qui est **en base**. Les deux points sont déclarés dans
`points_ouverts` et remontent dans chaque sortie JSON de la direction, à chaque ronde.

**SPEC §8.2 — ce qu'un commit doit modifier pour valoir preuve.** Rencontré à la
frontière du contrôle `evidence`, et laissé intact. `evidence` vérifie qu'un **moyen**
de preuve existe — un dépôt inscriptible, une table accessible. Il ne dit rien de ce
qui **constitue** une preuve suffisante : un commit vide passerait ce contrôle, comme
il passerait tout autre. La question appartient à la clôture des tâches (LOT-02,
LOT-04), pas au Preflight. Elle est ici signalée, pas préemptée.

**SPEC §8.4 — fréquence du Preflight : avant chaque ronde, ou une fois par jour ?**
Non tranché, et le lot n'a pas eu à le trancher : `preflight.py` est un exécutable sans
état, sûr à relancer aussi souvent qu'on veut. Le choix de cadence appartient à
`bin/rondes.sh`, donc au LOT-08. Ordre de grandeur pour arbitrer : mesuré le 17/08 sur
l'instance de validation, **0,8 s** pour les quatre directions actives, 1,3 s avec les
trois fonctions en veille. Le coût est donc négligeable devant une ronde ; dans le
conteneur, il faut y ajouter au pire le délai des services externes joignables mais
lents, plafonné à 5 s par service.

---

## 6. Ce que le Preflight a trouvé dès sa première exécution

Vérification du 17/08 sur une instance PostgreSQL jetable, chargée avec le schéma du
dépôt et les 36 curseurs de la sauvegarde du 11/08.

| Direction | Constat | Nature |
| --- | --- | --- |
| `ceo` | aucun curseur en base pour les six axes | réel — le CEO n'a jamais figuré dans la table |
| `ceo` | `bin/couts.py` lève une exception sur `--help` | réel — `int(sys.argv[1])` sur « --help » |
| `growth` | aucun curseur ; les réglages vivent sous `commercial` et `marketing` | réel — bascule SPEC §5 non répercutée |
| `delivery` | `/backlog`, `/repo`, `/prodlogs`, `/repo-delivery` non montés · `DEOS_RO_DSN` absente | exact hors conteneur — ce sont des montages et une variable du conteneur |
| `chief-of-staff` | READY | — |

Les deux premières lignes sont des trouvailles, pas des faux positifs : elles nomment
un maillon manquant, avec l'action et le destinataire. **Leur correction ne relève pas
du LOT-05** — le curseur du CEO demande un arbitrage de Sam, `couts.py` appartient à
personne dans ce lot. Elles sont exactement ce que le Preflight est censé produire :
une alerte assignée au Chief of Staff, qui décidera qui corrige.

---

## 7. Vérification

```bash
# Les huit contrôles, sur les directions actives
bin/preflight.py --toutes --texte

# Un échec simulé est détecté et assigné au CoS
mv bin/sf-lead /tmp/ && bin/preflight.py growth; mv /tmp/sf-lead bin/
# attendu : NOT_READY, controle=tools, next_owner=chief-of-staff

# Le code de sortie distingue les deux cas
bin/preflight.py delivery >/dev/null; echo "sortie=$?"   # 1 si NOT_READY
bin/preflight.py chief-of-staff >/dev/null; echo "sortie=$?"  # 0 si READY

# Parseur de repli, règle du paradoxe, cohérence de la configuration
bin/preflight.py --autotest
```

Depuis le conteneur, préfixer par `docker exec dh-comite /workspace/bin/…`.

**Codes de sortie** : `0` toutes READY · `1` au moins une NOT_READY · `2` erreur
d'usage ou de configuration. La distinction compte : un appelant doit pouvoir
différencier « une direction n'est pas prête » de « le Preflight lui-même est cassé ».

---

## 8. Ce que ce lot ne fait pas

- **Il n'enregistre aucune tâche.** L'alerte porte `next_action` et `next_owner` ; sa
  transformation en tâche appartient au LOT-02 et au LOT-04.
- **Il ne branche pas le Preflight sur les rondes.** `bin/rondes.sh` appartient au
  LOT-08, qui décidera de la cadence (SPEC §8.4).
- **Il n'écrit rien en base.** Seulement des `SELECT` sur `curseurs` et un test
  d'existence sur les tables de preuve. Aucune migration : c'est pourquoi l'invariant
  I6 ne s'applique pas au dépôt réel pour ce lot. Il a néanmoins été appliqué à
  l'instance jetable de validation — sauvegarde, restauration essayée, empreinte
  comparée avant et après.
- **Il ne touche pas à la plateforme** (I1), et le code refuse de le faire même si la
  configuration le lui demandait.
