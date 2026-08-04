# MISSION COLLECTIVE — Interface web globale
> Commandée par Sam le 04/08. Décision DEC-2026-0714-01, validée immédiatement.
> Séquence : expression des besoins en ronde du 05/08 → consolidation DSI dans la journée →
> arbitrage au comité du lundi 10/08 sur un document déjà instruit.

## Ce qui existe déjà (le socle, livré le 14/07)
Tableau de bord `/comite/` : poinçon de santé, loges par domaine, panneaux de rapport détaillé,
bloc exploitation temps réel (activité clients, capacité serveur), archives des dossiers,
liens sortants vers les outils sources.

## Ce que Sam demande maintenant
Un tableau de bord **par domaine** — commercial, marketing, technique, customer success,
exécution — avec les **outils d'interaction**, notamment la validation des décisions depuis
l'interface plutôt qu'en ligne de commande.

## Ce que chaque direction produit dans sa ronde du 05/08
Un bloc `besoin_interface` dans son rapport, contenant :
1. **INDISPENSABLE — trois éléments maximum.** Pour chacun : ce que je veux voir, à quelle
   fréquence je le regarde, et **quelle décision ou quelle action il déclenche**. Un indicateur
   qui ne change rien à ce que tu fais n'a rien à faire sur un tableau de bord.
2. **SOUHAITABLE** — le reste, sans limite de nombre mais clairement séparé.
3. **SOURCE DE CHAQUE ÉLÉMENT** : d'où vient la donnée (deos_state, vue prod, Salesforce,
   Ghost, fichier). Si la donnée n'existe nulle part, dis-le : c'est un prérequis, pas un widget.
4. **CE QUI EXISTE DÉJÀ AILLEURS** : si un outil affiche déjà cette information (console admin,
   dashboards Salesforce, blog), l'interface doit y RENVOYER, pas la reconstruire. Applique
   l'inventaire des capacités (config/outils_disponibles.md) avant de demander quoi que ce soit.
5. **INTERACTION** : quelle action tu aimerais pouvoir déclencher depuis l'interface, en
   respectant ton curseur d'autonomie — une action au-delà de ton cran reste soumise à validation.

## Ce que le Directeur Delivery (DSI) produit dans la journée du 05/08
Une **spécification consolidée** avec :
- l'inventaire des besoins des cinq directions, dédoublonné ;
- pour chaque élément : source de donnée confirmée, faisabilité, effort (S/M/L), dépendances ;
- ce qui est un **renvoi** vers un outil existant plutôt qu'un développement ;
- les prérequis techniques (vues à créer, accès à ouvrir) et leur statut ;
- un **planning en lots livrables**, du plus utile au moins utile, chaque lot ayant une valeur
  propre — pas de « tout ou rien » ;
- ce qui exige une décision de Sam (accès, budget, arbitrage de priorité).
Contrainte : la V1 existante n'est pas à refaire. On l'étend.

## Ce que le CEO digital fait au comité du 10/08
Arbitrage sur document instruit : croiser les besoins entre domaines (un même indicateur demandé
par deux directions = un seul widget), repérer les collisions et les dépendances, trancher ce qui
est réversible, remonter à Sam ce qui engage. Puis instruire chaque décision restante selon le
format habituel (argument, contre-argument, options, recommandation).

## Ce que Sam attend d'observer
C'est le **deuxième banc d'essai** de la coordination inter-directions, après l'Entracte. Le
compte rendu du comité doit dire ce qui a fonctionné et ce qui a frotté dans la collaboration —
c'est un livrable au même titre que la spécification.
