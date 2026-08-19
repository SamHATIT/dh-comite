# Architecture multi-modèle — offre installée chez le client

> Note du 19/08. **Pas une décision**, un cadrage à instruire quand l'offre
> on-site sera travaillée.

## Ce qui est acquis

**Le SDS reste sur un modèle de premier plan, et c'est assumé.** Il est vendu : un
client à 79 € qui reçoit une spécification de qualité justifie ce coût. L'économie se
fait sur le comité et le palier gratuit, pas sur ce qui produit la valeur vendue.

**Le multi-modèle ne concerne que le déploiement chez le client.** Ce n'est pas une
optimisation de coût, c'est une exigence commerciale : un grand compte voudra choisir
son fournisseur — souveraineté, contrat-cadre existant, politique interne.

## Le principe retenu

> **On ouvre les accès. Le client configure. S'il veut une adaptation, c'est une
> prestation.**

Concrètement : on s'engage à rendre le fournisseur paramétrable — type OpenRouter ou
équivalent — et le client branche ce qu'il veut. Il connaît ses modèles mieux que
nous.

**Ce que cela évite :** garantir le comportement de modèles qu'on n'a pas qualifiés.
Sur des dizaines de fournisseurs, la promesse serait intenable.

**Ce que cela ouvre :** une prestation d'adaptation quand un client a un besoin
particulier. C'est du service facturable, pas une obligation contractuelle.

## Le point dur, à ne pas sous-estimer

**L'appel d'outils.** Le pipeline BUILD invoque des commandes, lit des fichiers,
délègue à des sous-agents. Un modèle qui ne sait pas appeler un outil dans le format
attendu ne dégrade pas la qualité — **il casse le pipeline**.

C'est exactement ce qui bloquait le fournisseur essayé la semaine dernière, où deux
modèles seulement étaient confirmés compatibles.

Conséquence pour l'offre : distinguer clairement

| Ce qu'on garantit | Ce qu'on n'engage pas |
| --- | --- |
| le fournisseur est paramétrable | que tout modèle fonctionne |
| une liste de modèles **qualifiés**, avec ce qui a été vérifié pour chacun | le comportement d'un modèle hors liste |
| une prestation d'adaptation si besoin | l'adaptation gratuite |

## Ce qu'il faudra qualifier, par modèle

Trois vérifications, pas plus — mais les trois :

1. **Appel d'outils** — le seul point bloquant. Sans lui, rien ne fonctionne.
2. **Français** — pour les agents en contact, Sophie en premier.
3. **Apex et métadonnées Salesforce** — aucun banc d'essai public ne le teste.

## À instruire plus tard

- Le format de la liste de modèles qualifiés, et qui la tient à jour.
- Ce qui se passe quand un client impose un modèle non qualifié : refus, avertissement,
  ou dégradation acceptée et documentée ?
- Le tarif de la prestation d'adaptation.
