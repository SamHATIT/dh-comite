# Recovery Sprint — la trace du tri

> Genere le 2026-08-17 par `bin/recovery.py --trace`.
> Ne pas modifier à la main : régénéré depuis `docs/recovery-2026-08.json`
> et la base. LOT-09.

## Pourquoi ce tri

Quarante décisions accordées, la plus ancienne de quatorze jours. Une partie n'a plus
d'objet, une autre est déjà faite sans que rien ne le prouve, une troisième attend
réellement. Tant que les trois cohabitent, aucun compteur du comité n'est lisible :
le score d'exécution du 17/08 tombait à 0/100 sur un stock dont personne ne savait
quelle part décrivait du travail réel. Traiter ce passif n'est pas du rangement —
c'est la condition pour que le nouveau tableau de bord (LOT-10) mesure quelque chose.

## Pourquoi ce document existe

Dans trois mois, personne ne se souviendra pourquoi telle décision de début août a
été marquée obsolète. Une décision qui sort de la file sans motif écrit revient sous
une autre forme, et le même travail se refait depuis zéro. C'est un document
d'archive : il est fait pour être relu longtemps après, par quelqu'un qui n'était
pas là.

Il est **généré** par `bin/recovery.py --trace`, jamais tenu à la main. Une trace
recopiée diverge de la base dès la première correction — et c'est alors la trace
qu'on croit.

## La méthode : deux étages

1. **Mécanique.** Le script cherche les empreintes disponibles et propose un
   classement. Il ne répond qu'à une seule des six questions, et seulement par
   « il existe une empreinte » — jamais par « c'est fait ».
2. **Relecture.** Le Chief of Staff lit la décision, lit ce que l'empreinte
   désigne réellement, et tranche. **Il ne clôt jamais sur la seule empreinte.**

La séparation vient d'un constat daté. Le 17/08, sur neuf décisions que la détection
croyait faites, la relecture n'en a validé qu'**une seule**. Les autres étaient
partielles : un commit qui prépare mais ne déploie pas, deux volets demandés dont un
seul traité. Une empreinte prouve qu'un travail a eu lieu, pas qu'il fait ce que la
décision demandait — et aucune règle mécanique ne vérifie cela.

## Ce qui compte comme preuve, et ce qui n'en est pas

Tout document qui **parle** des décisions ressemble à une preuve : rapports, briefs,
calendriers de suivi, priorités de la semaine, fiches d'agents, page de suivi du
Chief of Staff. La première version de la détection en trouvait trente-cinq au lieu
de six. **Seul le commit porte un travail daté et signé** ; une clé de `deos_state`
ne compte que si elle porte un état métier, pas un récit.

Le journal de ce tri est exclu au même titre : sans cela, une seconde passe prendrait
la première pour une preuve de travail.

Les dépôts fouillés sont `/repo-delivery`, `/repo` et le dépôt du comité lui-même.
Ce dernier manquait à `bin/cloturer-prouvees.py` : les décisions qui portent sur le
dispositif du comité — garde-fou, tableau de bord, outils — laissent leur commit là
et nulle part ailleurs. Les chercher uniquement dans les dépôts de la plateforme
revenait à les déclarer sans empreinte par construction.

## `obsolete` n'est pas `refusee`

`refusee` est un jugement : la chose a été examinée et écartée. `obsolete` est une
péremption : elle n'a plus d'objet. Marquer `refusee` ce qui est périmé salit le
signal — on croit relire un arbitrage là où il n'y a eu qu'un calendrier qui a
tourné.

## Ce que « traitée » veut dire ici

Une décision est traitée si son statut a changé **ou** si elle porte désormais au
moins une tâche. Ce n'est pas mesuré au journal mais **en base** : un relecteur qui
annonce une clôture sans l'écrire laisse une trace « sans decision ». Le verdict est
l'écart constaté, jamais le compte rendu — c'est l'invariant I3 appliqué à l'outil
qui mesure.

La **file active** compte les statuts qui portent encore du travail : `accordee`,
`en_execution`, `blocked`, `failed`. `propose_cloture` attend une relecture,
`needs_decision` et `attente_sam` attendent Sam : ce sont des attentes, pas du
travail en cours.

## Où en est le tri

**Le tri n'a pas encore été conduit.** L'outil est livré et sa répétition
est passée : `tests/recovery.sh`, 14 cas.

La file de départ sera figée au premier passage sur la base du
comité, et ne bougera plus ensuite.

Il se conduit depuis le conteneur du comité, en quatre temps :

```bash
/workspace/bin/recovery.py                 # le classement mécanique, rien d'écrit
/workspace/bin/recovery.py --appliquer     # la relecture, décision par décision
/workspace/bin/recovery.py --rapport       # les trois critères du lot
/workspace/bin/recovery.py --trace         # ce document, rempli
```

Commencer par `--limite 3` : la première passe coûte quelques appels de
modèle, et se relit en entier avant d'engager le reste de la file.

## Les six questions, dans l'ordre

L'ordre n'est pas cosmétique : une décision sans objet ne mérite pas qu'on
cherche si elle est faite, et une décision faite ne mérite pas qu'on lui
écrive une tâche. On s'arrête à la première question qui répond oui.

| Question | Action si oui | Décisions |
| --- | --- | ---: |
| 1. Plus nécessaire ? | `obsolete` avec motif | 0 |
| 2. Déjà réalisée ? | demander la preuve, puis `propose_cloture` | 0 |
| 3. Partiellement réalisée ? | créer les tâches restantes | 0 |
| 4. Bloquée ? | nommer le `blocker`, poser `next_action` et `next_owner` | 0 |
| 5. Mal définie ? | reformuler, ou renvoyer en `attente_sam` | 0 |
| 6. Encore pertinente ? | au moins une tâche avec porteur et échéance | 0 |
| — | sans decision | 0 |

Les questions 2, 3 et 6 peuvent produire le même fait en base — une tâche de
plus : la 2 quand la preuve est *demandée* au porteur au lieu d'être
constatée, la 3 pour ce qui reste, la 6 pour le premier pas. On garde alors
le numéro annoncé par le relecteur ; le fait, lui, reste vérifié des trois
côtés.

## Ce que chaque décision est devenue

*Vide tant que le tri n'a pas été conduit : cette table se remplit
décision par décision, au fur et à mesure des passes.*

| Décision | Âge au départ | Question | Devenue | Pourquoi |
| --- | ---: | ---: | --- | --- |
