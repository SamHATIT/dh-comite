# Executive Health Score — les six composantes et leurs sources

**Lot** LOT-10 · **Date** 18 août 2026 · **Outil** `bin/health.py`
**Remplace** `bin/evaluer`, écrit le 11/08, jamais mis en service — voir §2.
**Contrat** `refonte-v2/lots/LOT-10-kpi.md` · **Invariant** I3.

> Tous les chemins sont relatifs à la racine du dépôt. `/prodlogs` est un point de
> montage du conteneur, pas un répertoire du dépôt.

---

## 1. La règle qui prime — et elle vaut pour tout DEOS, pas pour ce fichier

> **No self-attested KPI.** Aucun indicateur ne se calcule sur une donnée que la partie
> évaluée peut écrire elle-même. Un agent ne peut jamais être à la fois producteur et
> source de vérité de son propre indicateur.

C'est l'invariant I3, et ce n'est pas une précaution locale à la notation. C'est la
même règle que celle qui interdit à une direction de clore sa propre décision
(`propose_cloture` puis `clos`, deux acteurs), à un exécutant de valider sa propre
tâche (`done` puis `valide`), et à un agent de modifier l'objectif sur lequel il est
noté (`docs/MANDATS.md` §4). Trois applications, un seul principe.

**Le motif est plus fort qu'une question de confiance.** Un agent noté sur un
indicateur qu'il peut écrire a deux façons d'améliorer son score : améliorer le fait,
ou réécrire la mesure. La seconde est systématiquement moins coûteuse. Ce qu'on obtient
alors n'est pas de la triche — c'est une **dérive silencieuse des définitions** : le
seuil de qualification qui baisse d'un point, l'incident « critique » qui devient
« haut », l'échéance qui glisse d'une semaine. Chaque pas est défendable, et au bout de
deux mois l'indicateur ne mesure plus rien.

Dans `bin/health.py`, la règle n'est pas une consigne : **une mesure dont la source est
attestée par l'évalué est refusée à la construction**, avant tout calcul, par la seule
fonction qui fabrique une mesure. Il n'existe aucun chemin de code permettant d'en
ajouter une. `health.py --autotest` le démontre en essayant, plutôt qu'en l'affirmant.

---

## 2. Pourquoi l'évaluateur précédent a été gelé

`bin/evaluer` a été écrit le 11/08 pour sortir la notation des mains des directeurs.
Le constat qui l'a motivé tient toujours : sur les douze rondes des 10 et 11/08, **un
seul score exploitable**, avec une formule réinventée à chaque ronde — 88 le 09/08, 68
le 10/08, 56 le 11/08, sans qu'un fait ait bougé entre-temps. Ce n'était pas une
mesure.

Le même jour, Sam a commandé une **contradiction adversariale** des grilles
(`config/DOSSIER_FABLE_ATTAQUE_GRILLES.md`). Consigne : ne pas améliorer les grilles,
démontrer comment on peut les satisfaire **sans rien améliorer**. Verdict rendu le
11/08 (`config/REVUE_FABLE_GRILLES_RESULTAT.md`) : *ne pas mettre en service, ne pas
jeter l'approche*. La formulation retenue :

> « Ce n'est pas un évaluateur gelé, c'est un questionnaire auto-déclaratif avec une
> calculatrice au bout. »

**Geler la formule ne sert à rien tant que les données qu'elle lit sont écrites par les
évalués.** Le pattern `autoresearch` dont l'idée venait tient parce que sa suite de
tests vérifie des *résultats* que l'agent ne peut pas redéfinir. Les grilles du 11/08,
elles, lisaient des *champs de statut* que la direction évaluée pouvait poser
elle-même — depuis l'élargissement des droits du 11/08, le jour même de leur rédaction.

Six exploits ont été retenus, tous à coût quasi nul et sans mentir :

| Direction | Exploit le moins cher | Gain |
| --- | --- | ---: |
| Chief of Staff | basculer les plus vieilles accordées en « exécutée » | 14 à 25,5 pts |
| Delivery | relancer un vieux BUILD sur un projet de test | 25 pts |
| Delivery | annuler les exécutions en attente plutôt que les faire avancer | 14 pts |
| Commercial | cinq `INSERT` de leads, sans clé étrangère vers un signal entrant | 25 pts |
| Marketing | quatre textes vides ; un seul remet le compteur à zéro | 30 à 50 pts |

Et une symétrie qui résume tout : les 112 prospects tenus hors CRM étaient l'exploit
inverse — **cacher**. La grille créait l'incitation opposée — **injecter**. Même faille,
sens contraire.

**Fait vérifié pendant ce lot, et qui n'était consigné nulle part** : `bin/evaluer
--ecrire` n'a jamais pu écrire. Il appelle `deos-state set scores_calcules --par
evaluateur`, or `evaluateur` ne figure dans aucun scope de `bin/deos-state` :

```
$ echo '{"test":1}' | bin/deos-state set scores_calcules --par evaluateur
REFUS: scope — 'evaluateur' ne peut pas écrire 'scores_calcules' (DH scopes)
```

L'outil était donc doublement hors service : refusé en écriture par le contrôle de
scope, et mis en observation par l'arbitrage du 11/08. **Il n'est pas supprimé** — sa
grille reste une source d'inspiration et son en-tête porte l'histoire du 11/08. Il n'est
simplement plus la référence.

---

## 3. Ce que « hors de portée de l'évalué » veut dire exactement

C'est le point qui décide de tout le reste, et il se formule mal si on le pose en
« l'agent ne doit pas pouvoir influencer le chiffre ». Le Delivery *doit* pouvoir faire
monter la livrabilité — en livrant. Ce qu'il ne doit pas pouvoir faire, c'est **écrire
la mesure**.

> **La source doit être un FAIT, pas une DÉCLARATION.** Un fait se change en changeant
> le monde ; une déclaration se change en écrivant une ligne.

`bin/health.py` n'admet que quatre modes d'attestation. Il n'en existe aucun autre dans
le code, et le cinquième — `declaration` — est refusé par le constructeur.

| Mode | Ce qui protège la mesure | Exemple employé ici |
| --- | --- | --- |
| `horloge` | la base pose la valeur : un agent écrit un statut, il n'écrit pas l'heure | `tasks.cree_le`, `decisions.updated_at` |
| `tiers` | un autre acteur l'écrit — Sam, le CEO, la plateforme, un programme | `decisions.statut='accordee'`, posé par `ceo`/`sam`, jamais par le CoS qui est noté dessus |
| `croisee` | deux acteurs distincts sont nécessaires, **et la requête l'impose** | `tasks.valide_par <> owner` : il faut que l'exécutant déclare `done` ET qu'un relecteur valide |
| `externe` | l'artefact est vérifiable du dehors | une page publiée, une facture |

**L'attestation croisée est celle qui demande le plus de vigilance.** Elle admet des
mesures dont l'évalué écrit une partie de la donnée — c'est le cas du Chief of Staff,
noté sur `tasks.valide_par` qu'il écrit lui-même. Elle n'est valable que parce que le
prédicat SQL exige le concours d'un second acteur : le CoS ne peut valider que ce qu'une
direction a d'abord déclaré fini, et `deos-tasks valider` refuse toute tâche qui n'est
pas en `done`. **Si ce prédicat disparaît un jour, l'admission tombe avec lui.**
`--audit-sources` imprime ce cas en toutes lettres plutôt que de le ranger avec les
autres.

### Le contrôle connaît la direction sous tous ses noms

Défaut trouvé en relisant la sortie de `--audit-sources` pendant l'implémentation : le
contrôle comparait la direction notée aux acteurs qui écrivent la source, mot à mot.
`tasks.valide_par` est écrite par « cos » ; la direction s'appelle `chief-of-staff` dans
les fiches. Les deux chaînes ne se ressemblent pas — **le contrôle ne voyait donc aucun
conflit là où l'évalué et l'écrivain sont la même fonction.** Une table d'alias corrige :
`chief-of-staff` ≡ `cos`, et `growth` ≡ `commercial` ≡ `marketing` (fusion temporaire,
SPEC §5, que la table `curseurs` et les scopes de `deos-state` connaissent encore sous
les anciens noms). Deux cas de l'autotest le vérifient.

*Un garde-fou qui ne reconnaît pas son sujet ne garde rien.*

---

## 4. Les six composantes et leurs sources

Les poids viennent du contrat du lot. Dans chaque composante, les mesures pèsent
également ; pour Objectifs, les douze objectifs pèsent également, ce qui donne un quart
de la composante à chacune des quatre fonctions actives.

### 4.1 Exécution — 30 %

| Mesure | Source | Écrite par | Attestation |
| --- | --- | --- | --- |
| tâches validées / créées sur 14 j, par direction | `tasks.valide_par`, avec `valide_par <> owner` | le relecteur (`cos`, ou `ceo` en suppléance) | croisée |
| dette d'exécution et son sens de variation | `tasks.cree_le`, `tasks.maj_le` | PostgreSQL (défaut et déclencheur `trg_tasks_touch`) | horloge |
| âge moyen des tâches ouvertes | idem | idem | horloge |

**Le piège tenait dans le mot « terminées ».** Le contrat dit « tâches terminées /
créées ». `tasks.statut` est écrit par le porteur : compter les `done` reviendrait à lui
demander s'il a fini. On compte donc les tâches **validées**, et le prédicat
`valide_par <> owner` écarte le cas où une direction serait son propre relecteur. Sur le
jeu d'essai, une tâche auto-validée est bien exclue du numérateur.

**La dette est reconstruite, pas relevée.** Il n'existe pas de table d'historique. Une
tâche créée avant J-7 était ouverte à J-7 si elle n'était pas déjà terminale à cette
date — ce que `maj_le` permet de dire, puisque LOT-01 a posé le déclencheur exactement
pour que ce champ ne mente pas. La reconstruction se trompe dans un seul cas : une tâche
terminée puis rouverte dans la fenêtre. D'où l'état **PARTIEL** — la valeur est utile,
la méthode est dite, et elle n'est pas présentée comme un historique qui n'existe pas.

### 4.2 Objectifs — 25 %

Les douze objectifs des quatre fonctions actives, tels qu'écrits dans `.claude/agents/`
et motivés dans `docs/MANDATS.md`. **Six se mesurent aujourd'hui, six non.**

| Objectif | Source | État |
| --- | --- | --- |
| CEO O1 — brief lu et décidé par Sam | accusé de lecture | **absente** |
| CEO O2 — Strategic Yield | qui a posé `accordee` | **absente**, voir §5.1 |
| CEO O3 — initiative de fossé testée | marqueur d'initiative | **absente** |
| CoS O1 — tâche spécifiée sous 24 h | `decisions.statut='accordee'` + horloge | mesurée |
| CoS O2 — 95 % d'états terminaux | `tasks.valide_par` sur les tâches de plus de 14 j | mesurée |
| CoS O3 — la dette diminue | `tasks.horloge` | mesurée (partagée avec Exécution) |
| Delivery O1 — produit livrable au 27/09 | URL et marqueurs de contenu | **absente** |
| Delivery O2 — zéro incident critique > 24 h | `v_deos_executions` + logs backend | mesurée |
| Delivery O3 — la chaîne SDS → BUILD aboutit | `v_deos_build_phases` + verdict Elena | mesurée (partielle) |
| Growth O1 — positionnement en ligne | URL et marqueurs de contenu | **absente** |
| Growth O2 — pipeline qualifié | `v_deos_salesforce_pipeline` | **absente** |
| Growth O3 — contenus publiés | `v_deos_blog_articles.published_at` | mesurée |

**Le CEO n'a aujourd'hui aucun objectif mesurable.** Ce n'est pas un oubli du lot, c'est
le constat : ses trois objectifs se jugent chez Sam, et rien n'enregistre ce jugement.
La conséquence est à regarder en face — la fonction qui arbitre tout le reste est celle
que le dispositif sait le moins mesurer.

**Le cas du Chief of Staff est le plus délicat, et il est traité comme sa fiche
l'engage.** Il est la seule fonction qui écrit au registre et il est noté sur l'état de
ce registre : il compte un stock qu'il alimente. Faiblesse relevée en revue externe le
11/08, conservée telle quelle avec sa contrepartie, écrite dans sa fiche : *le calcul de
ses trois objectifs est fait par `bin/health.py` directement sur les tables, jamais
repris d'un chiffre qu'il déclare*. C'est ici que cette promesse se tient — O1 lit un
statut que seuls le CEO et Sam peuvent poser, O2 et O3 ne lisent aucun statut du tout,
seulement des validations croisées et l'horloge.

**Une mesure partagée est signalée, pas cachée.** La dette d'exécution compte dans deux
composantes : Exécution (30 %) et l'objectif O3 du CoS (un douzième de 25 %). C'est
délibéré — la dette est à la fois la réalité de l'exécution et un objectif explicite —
mais un fait compté deux fois pèse deux fois, et cela doit se lire. Le champ
`partagee_avec` le porte dans les deux sorties.

### 4.3 Produit — 20 %

| Mesure | Source | Écrite par |
| --- | --- | --- |
| incidents ouverts | `v_deos_executions` (échecs > 24 h) et `/prodlogs/backend-24h.log` | la plateforme et son backend |
| jours depuis la dernière chaîne aboutie | `v_deos_build_phases`, phase `completed` **portant un verdict d'Elena** | agents de la plateforme, deux au moins |
| livrabilité | URL des sites et marqueurs de contenu | **absente** |

**Rien n'est lu dans le rapport du Delivery.** Le `domain_score` de sa fiche compte des
incidents dont il fixe lui-même la gravité : c'est une appréciation, et elle est du côté
de l'évalué. Le Delivery avait d'ailleurs signalé le défaut lui-même — « mon score à 100
est trompeur, la formule ne compte que les incidents opérationnels, pas la dette
d'exécution ». Il avait raison, et c'est ce lot qui devait y répondre.

**Le taux d'échec est apparié à son volume de tentatives.** Sans cet appariement, la
stratégie optimale sous cette métrique est de **ne plus rien tenter** : zéro échec
garanti, note maximale, plateforme à l'arrêt. C'est la faille n° 2 du 11/08, et elle ne
se corrige pas en changeant un seuil — seulement en refusant de conclure quand il n'y a
pas eu d'essais. En dessous de trois exécutions sur sept jours, la mesure rend INCONNU.

**La chaîne aboutie demande deux acteurs**, comme la revue du 11/08 le recommandait : une
phase `completed` **et** un verdict d'Elena. Elle reste PARTIEL, parce que le troisième
maillon — le journal de déploiement de Jordan — n'est pas atteignable depuis le comité.
La chaîne est donc prouvée jusqu'à la revue, pas jusqu'au déploiement, et l'outil le dit
à chaque ligne plutôt qu'une fois dans un document.

### 4.4 Trésorerie — 10 %

Source : `bin/couts-consolides.py --json`. Le coût d'un appel est écrit par ce qui
l'exécute, jamais par l'agent qui le passe.

**La mesure est une borne inférieure, et elle le reste.** L'outil déclare lui-même ses
trous : embeddings du RAG sans compteur, sessions de développement hors de toute base,
GPU à relever à la main. L'écart constaté avec la facture réelle le 11/08 était d'environ
185 USD/mois. Conséquence stricte sur la notation :

> **Une borne inférieure peut prouver un dépassement, jamais une bonne tenue.**

Si le mesuré dépasse déjà la référence (196 USD/mois pour le comité, SPEC §8), le réel
la dépasse aussi : la dégradation est certaine. Dans l'autre sens, un chiffre bas ne
prouve rien. La composante est donc **PARTIEL en permanence**, et `--audit-sources`
imprime ce que la source ne mesure pas.

**Et le relevé rend INCONNU quand `DEOS_RO_DSN` est absent.** Sans lui, le poste
« pipeline » vaut zéro sans qu'aucune erreur ne le dise : le total tombe et la trésorerie
passerait au vert parce qu'on ne voit plus la dépense. C'est l'incident du 14/08 — *« ce
n'est pas une dépense nulle, c'est un outil aveugle depuis cet environnement »*, trouvé
par le Directeur Financier lors de sa première ronde. Reconnu ici plutôt que découvert
une seconde fois.

### 4.5 Pipeline — 10 %

Le contrat dit « comptes qualifiés **en base Salesforce** ». Salesforce n'est pas
interrogeable depuis le comité : ni binaire `sf`, ni identifiants — c'est la raison
d'être de `bin/sf-lead`, qui passe par une file relayée vers l'hôte. La vue qui
l'exposerait, `v_deos_salesforce_pipeline`, a été proposée le 02/08 par l'audit des
capacités du Delivery (effort M, risque faible) et n'a jamais été créée.

**On ne se rabat pas sur `v_deos_leads`.** Deux raisons, et la seconde suffirait : la
revue du 11/08 a montré qu'un lead s'y insère sans clé étrangère vers un signal entrant
— cinq `INSERT` valaient 25 points ; et Sam a tranché le 10/08 que *les contacts, suivis
de contact et campagnes qui ne sont pas dans Salesforce n'existent pas*. Mesurer
ailleurs serait mesurer autre chose en l'appelant pipeline.

La composante rend donc INCONNU, avec la source à créer nommée. **La requête est déjà
écrite** : le jour où la vue existe, la mesure s'allume sans qu'on touche au calcul.

### 4.6 Risques — 5 %

Il n'existe pas de registre des risques. Ce qui existe et se compte sans jugement, c'est
ce qu'un programme constate à la place des agents :

| Mesure | Source | Pourquoi elle échappe à l'évalué |
| --- | --- | --- |
| alertes Preflight ouvertes | `bin/preflight.py --toutes` | une direction ne déclare pas qu'elle a ses moyens : le Preflight les essaie |
| escalades et reprises hors délai | `decisions` et `tasks`, à l'horloge | SPEC §4.3 : clôture en attente > 24 h, `attente_sam` > 7 j, `retry_at` échu jamais relancé |
| échéances réglementaires non couvertes | table `echeances_reglementaires` | **absente** — voir §5 |

Les alertes Preflight sont imputées au **Chief of Staff**, par construction et non par
choix de présentation : SPEC §3.1 lui assigne toute alerte, à charge pour lui de décider
qui corrige. Les compter chez la direction bloquée reproduirait le paradoxe — *« tu n'as
pas les moyens de travailler, débrouille-toi »*.

---

## 5. Les six sources qui manquent — et ce que coûte chacune

Elles sont déclarées **dans l'outil**, avec leur motif, et sortent en INCONNU à chaque
exécution. Une lacune qui ne se lit que dans un document est une lacune qu'on oublie.

| Source | Ce qu'elle débloquerait | Coût apparent |
| --- | --- | --- |
| `validation_par` sur `accordee` | CEO O2, Strategic Yield | une ligne dans `bin/deos-decisions` |
| `v_deos_salesforce_pipeline` | la composante Pipeline entière (10 %) + Growth O2 | effort M, chiffré le 02/08 |
| table `echeances_reglementaires` | le seul risque daté du dispositif | trois lignes saisies à la main |
| URL des sites + marqueurs de contenu | Delivery O1, Growth O1, livrabilité | une déclaration, pas un développement |
| accusé de lecture du brief par Sam | CEO O1 | un champ, et l'habitude de le poser |
| marqueur d'initiative de différenciation | CEO O3 | un champ, posé par Sam à la validation |

### 5.1 Le défaut trouvé par le mécanisme lui-même

La mesure du Strategic Yield avait été écrite en supposant qu'`accordee` venait de Sam.
**Le constructeur de mesure l'a refusée** : `accordee` se pose par `ceo` **ou** `sam`
(matrice de droits, `docs/REGISTRE.md` §3), et `validation_par` n'est renseignée que pour
`clos`, `obsolete` et `refusee` — jamais pour `accordee`. Rien en base ne dit lequel des
deux a accordé, donc **le CEO pourrait accorder ses propres propositions et faire monter
son rendement seul**.

C'est exactement la faille qui a tué les grilles du 11/08, sur un objectif écrit six
jours plus tard. Elle n'a pas été trouvée par relecture : elle a été trouvée parce que le
code refuse ce que la règle interdit. **C'est le meilleur argument pour un mécanisme
plutôt qu'une consigne**, et il vaut la peine d'être consigné.

Correctif proposé, non appliqué ici — il touche `bin/deos-decisions`, hors du périmètre
de ce lot : écrire `validation_par` aussi pour `accordee`, ou réserver `accordee` à `sam`
quand l'origine est `ceo`. La mesure est écrite et attend sa source.

### 5.2 L'échéance réglementaire, deux fois signalée

La table `echeances_reglementaires` a été **arbitrée par Sam le 11/08** comme action
immédiate à coût quasi nul, avec son motif : trois échéances tombent le 1er septembre
(AI Act art. 50, facturation électronique, compteur de jetons du palier gratuit). Elle
n'existe toujours pas.

C'est la faille n° 5 de la revue, la plus grave parce qu'elle ne demande aucun exploit :
**la seule direction portant une échéance dure est la seule qui ne soit pas mesurée.** Un
tiret attire moins l'œil qu'un rouge. C'est la raison pour laquelle cet outil affiche
INCONNU et compte la lacune dans la couverture, au lieu de laisser une case vide.

---

## 6. Tri-état, couverture, et le refus de rendre un score

### 6.1 Quatre états, jamais un nombre nu

`FAILED sur 7 jours : 0` ne distingue pas *sain* de *aucune donnée*, *mauvais DSN* ou
*aucune tentative*. C'est la faille structurelle n° 1 du 11/08, et c'est elle qui a
produit le brouillon notant le Delivery 100/100 le matin où son directeur se notait 56,
preuves à l'appui. **Corriger la colonne fautive n'a pas corrigé la classe d'erreur** :
un résultat valide, incomplet, rendu sans erreur.

| État | Signification | Effet sur le calcul |
| --- | --- | --- |
| `MESURE` | valeur mesurée sur une source vivante | comptée |
| `PARTIEL` | valeur vraie, mais la source déclare ce qu'elle omet, ou elle est reconstruite | comptée, et signalée |
| `INCONNU` | source absente, injoignable, ou n'ayant jamais rien reçu | **retirée du calcul** |
| `PERIME` | source existante, plus alimentée dans sa fenêtre de fraîcheur | **retirée du calcul** si elle est la seule source de la mesure |

Une seule source a aujourd'hui une fenêtre de fraîcheur : le journal backend, exporté
toutes les 15 minutes, périmé au-delà de 2 h. Il n'est jamais la seule source d'une
mesure — les incidents se lisent aussi dans `v_deos_executions` — donc en pratique un
journal figé fait passer la mesure en `PARTIEL` et imprime pourquoi, au lieu de compter
zéro erreur pour une mauvaise raison.

Chaque requête vérifie en outre un **invariant de volume** avant de conclure : une table
qui n'a jamais reçu d'écriture ne vaut pas zéro. Sans cela, « aucun contenu publié » et
« la table des contenus n'est pas alimentée » se lisent pareil, et les deux n'appellent
pas la même conduite.

### 6.2 La couverture s'imprime toujours

Le poids d'une composante est réduit au prorata de ce qui s'y mesure. Le score global est
la moyenne pondérée sur le poids **réellement mesuré**, et la couverture — la somme de
ces poids sur 100 — s'affiche à côté, sans option pour la masquer. Un score de 82 sur
40 % de couverture et un score de 82 sur 95 % ne disent pas la même chose.

### 6.3 En dessous de 50 %, aucun score global n'est rendu

Défaut constaté au premier essai à blanc de ce lot, sans accès aux bases : une seule
source répondait, et l'en-tête affichait **« SCORE 100,0/100 — couverture 10 % »**. Le
nombre était juste et la lecture fausse. Un lecteur pressé retient le 100, pas le 10 %.

L'outil refuse donc de rendre un score global sous 50 % de couverture, et affiche à la
place ce qu'il aurait valu, avec sa couverture. Le détail par composante, lui, reste
imprimé : ce qui est su reste lisible. La sortie `--json` applique la même règle — `score`
est nul, et `score_brut` reste disponible pour qui veut suivre la série en le sachant.

50 % est un **seuil de jugement, pas une mesure** : c'est le point où la moitié du poids
manque et où ce qu'on ne voit pas peut renverser la moyenne. À réexaminer quand les six
sources absentes auront été créées.

### 6.4 Le plancher du barème, et ce qui informe au-delà

Chaque mesure est notée par un barème linéaire entre un seuil « bon » et un seuil
« mauvais », borné à [0, 100]. Il a une zone morte, comme tout barème borné : au-delà du
seuil mauvais, cent de plus ne coûtent rien. C'est la faille n° 4 du 11/08 — à 61
décisions accordées, la pénalité du CoS saturait, et **la métrique la plus dégradée
cessait d'informer là où c'était le plus grave**.

On ne prétend pas la supprimer : un score borné a nécessairement un plancher. On la rend
inoffensive en imprimant **toujours la valeur mesurée à côté du score**. Au-delà du
plancher, c'est le nombre qui informe, et il est là.

---

## 7. Le score par direction, et sa cohérence avec le global

Chaque mesure est imputée à une direction ou à `entreprise` quand elle n'est imputable à
personne. Le score d'une direction est **le même calcul que le global**, restreint à ce
qui lui revient — pas une seconde formule.

Cela se vérifie par une identité, pas par une affirmation : les quatre directions et
`entreprise` partitionnent les mesures calculables, donc la moyenne de leurs scores,
repondérée par leur poids mesuré, doit redonner le global.

```bash
health.py --coherence     # sortie 0 si l'écart est nul et la partition complète
```

**Ces scores trient l'attention — « où regarder en premier ». Ils ne comparent pas des
performances.** Deux directions ne sont pas mesurées sur le même nombre de sources
vivantes : le CEO à 0 % de couverture et le Delivery à 74 % ne sont pas comparables, et
la couverture affichée à côté de chaque score est là pour l'empêcher. C'est le correctif
de la faille n° 3 du 11/08 (échelles non comparables), et il est assumé comme une
renonciation : on renonce à classer les directions entre elles.

---

## 8. Ce que cet outil ne fait pas

| Point | Pourquoi |
| --- | --- |
| **Il n'écrit rien** — ni en base, ni dans `deos_state`, ni sur la plateforme | Les directions le lisent ; aucune ne l'alimente. C'est la condition pour que le score reste hors de leur portée. Corollaire : pas de série temporelle tant qu'aucun acteur autorisé ne l'enregistre. |
| Il ne compare pas l'auto-score au score calculé | Correctif recommandé le 11/08 (écart > 20 → investiguer). Il suppose un auto-score des directions, qui n'existe pas de façon reproductible. À reprendre quand les rondes V2 auront tourné. |
| Il ne note pas les trois fonctions dormantes | Cadence à zéro (SPEC §5). Noter une fonction délibérément mise en veille mesurerait la décision de Sam, pas son travail. I2 : leur mandat reste écrit, elles entreront ici sans rien reconstruire. |
| Il ne crée aucune des six sources absentes | Elles touchent d'autres fichiers que les deux de ce lot. Le découpage en vagues du WBS ne tient que si chaque lot s'y astreint. |
| Il n'est pas référencé dans `docs/OUTILS.md` | Même raison : `OUTILS.md` est un fichier partagé, et LOT-11 tourne en parallèle sur la même vague. À ajouter par le premier lot qui en aura la charge. |

---

## 9. Vérification

L'environnement d'implémentation n'a ni démon Docker ni DSN. Comme pour LOT-01, les
contrôles ont été passés sur un **réplica fidèle** : schéma `db/init/01_schema.sql`, la
dérive `demo` constatée, les deux migrations dans l'ordre de dépendance
(`docs/APPLICATION_MIGRATIONS.md`), un jeu de décisions et de tâches couvrant les cas qui
décident du calcul, et une base plateforme portant les vues `v_deos_*` réellement
interrogées.

### Les trois critères du lot

```bash
# 1. Le score se calcule et affiche ses sources
docker exec dh-comite /workspace/bin/health.py
# attendu : score global + 6 composantes + source et écrivain de chaque mesure

# 2. Aucune composante ne lit un champ auto-déclaré
docker exec dh-comite /workspace/bin/health.py --audit-sources
# attendu : chaque source nommée, avec qui l'écrit et son mode d'attestation

# 3. Le score par direction est cohérent avec le global
docker exec dh-comite /workspace/bin/health.py --coherence
# attendu : écart 0.0, partition complète, sortie 0
```

### Ce qui a été éprouvé sur réplica, le 18 août 2026

| Contrôle | Résultat |
| --- | --- |
| `--autotest` (17 cas, sans base) | 17/17 |
| une source auto-déclarée est refusée à la construction | refusée |
| une direction notée sur un champ qu'elle écrit est refusée | refusée |
| l'alias `cos` / `chief-of-staff` est reconnu | refusé comme il se doit |
| l'alias `commercial` / `growth` est reconnu | refusé comme il se doit |
| tâche auto-validée (`valide_par = owner`) | **exclue** du numérateur |
| dette reconstruite à J-7 | conforme au jeu d'essai (3, −1) |
| exécution sans DSN | tout INCONNU, **aucun score rendu**, sortie 1 |
| trésorerie sans `DEOS_RO_DSN` | INCONNU, et non 5,31 USD au vert |
| couverture < 50 % | score non rendu, valeur brute affichée avec sa couverture |
| `--coherence` sur le réplica | global 58,0 = recomposé 58,0, écart 0,0, partition complète |
| couverture atteinte avec les deux bases | 69 % — six sources manquent |
| alertes Preflight comptées | 13, quatre directions NOT_READY (montages absents hors conteneur) |

Codes de sortie : **0** si la couverture est complète, **1** si une source manque —
c'est-à-dire aujourd'hui, à chaque exécution — et **2** sur erreur d'usage. Un appelant
qui traite tout code non nul comme une panne lira donc une panne permanente : c'est
délibéré, la couverture incomplète n'est pas un état normal qu'on veut voir s'installer.

### Le zéro ambigu, rencontré deux fois dans ce lot même

Il faut le consigner, parce qu'il montre que la classe d'erreur ne se corrige pas en la
connaissant.

1. **Le comptage des alertes Preflight lisait la clé `alertes`.** Elle n'existe pas : la
   sortie du Preflight porte `echecs`. Le compteur rendait **0 pendant que les quatre
   directions étaient NOT_READY**, sans la moindre erreur — dans le script écrit pour
   interdire ce genre de zéro. Le comptage vérifie désormais la forme de chaque ligne
   avant de la croire, et rend INCONNU si elle n'est pas reconnue.
2. **Le relevé de coûts rendait 5,31 USD sans `DEOS_RO_DSN`**, en ne voyant que les
   fichiers de session. Trésorerie au vert, alors que la mesure était aveugle. Traité
   au §4.4.

Dans les deux cas, la commande rendait un nombre juste dans son périmètre, faux dans sa
lecture, et **sans erreur**. C'est la seule forme de panne que ce fichier demande de
craindre par défaut.
