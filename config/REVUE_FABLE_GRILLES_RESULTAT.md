# Revue adversariale des grilles — verdict et suites

> **Contradicteur :** Fable, 11/08/2026. Commande : Sam.
> **Verdict : ne pas mettre en service. Ne pas jeter l'approche.**

## Le point central

Geler l'évaluateur ne sert à rien si les données qu'il lit sont écrites par les évalués.
Le pattern `autoresearch` tient parce que la suite de tests vérifie des *résultats* que
l'agent ne peut pas redéfinir. Ici, la quasi-totalité des métriques lit des *champs de
statut* que la direction évaluée peut poser elle-même — depuis l'élargissement des
droits du 11/08, le jour même de la rédaction des grilles.

Formulation du contradicteur : « ce n'est pas un évaluateur gelé, c'est un questionnaire
auto-déclaratif avec une calculatrice au bout. »

## Exploits retenus, par direction

| Direction | Exploit le moins cher | Gain |
| --- | --- | ---: |
| Chief of Staff | basculer les plus vieilles accordées en « exécutée » — la règle de clôture sur preuve est une consigne de prompt, pas une contrainte SQL | 14 à 25,5 pts |
| Delivery | relancer un vieux BUILD sur un projet de test : « jours depuis dernier BUILD abouti » retombe à 0 | 25 pts |
| Delivery | annuler les exécutions en attente de validation plutôt que les faire avancer — la métrique pénalise la file d'attente du client | 14 pts |
| Commercial | cinq INSERT de leads : aucune contrainte de source, aucune clé étrangère vers un signal entrant | 25 pts |
| Commercial | qualifier les 16 signaux en masse « rejeté » — simple bascule de statut | jusqu'à 25 |
| Marketing | quatre textes vides ; un seul suffit à remettre « jours depuis publication » à zéro | 30 à 50 |

**Symétrie à retenir** : les 112 prospects hors CRM étaient l'exploit inverse — cacher.
La grille crée l'incitation opposée — injecter. Même faille, sens contraire.

## Failles structurelles — plus graves que les exploits

**1. Le zéro ambigu.** « FAILED sur 7 j : 0 » ne distingue pas *sain* de *aucune donnée*,
*mauvaise base*, ou *aucune tentative*. Même classe d'erreur que le faux audit
`v_deos_signaux` : résultat valide, incomplet, sans erreur. Le brouillon qui notait
Delivery 100/100 le jour de son rouge auto-déclaré à 56 n'était pas un bug de colonne —
c'était cette classe qui se manifestait. Corriger la colonne n'a pas corrigé la classe.

**2. La grille punit l'essai.** Stratégie optimale sous cette grille : un BUILD trivial
réussi, puis ne plus rien tenter. Zéro FAILED garanti. Elle récompense l'inaction
ponctuée d'un geste symbolique.

**3. Échelles non comparables.** Somme des plafonds : Delivery 100 (plancher 0),
CoS 75 (plancher 25), Commercial 70 (plancher 30), Marketing 65 (plancher 35). Deux
directions à 50 ne décrivent pas la même gravité. Trier son attention par score biaise
le tri par construction.

**4. Zones mortes des plafonds.** À 61 décisions accordées, la pénalité CoS sature à
25,5 sur 30. Cent décisions de plus ne coûtent rien. La métrique la plus dégradée cesse
d'informer là où c'est le plus grave.

**5. L'absence rendue verte — le plus gros angle mort.** CS et Legal sans grille : un
tiret attire moins l'œil qu'un rouge. Or **Legal est la seule direction avec une échéance
dure au 1er septembre, et la seule non mesurée.** Le tableau affichera un système sans
alerte pendant qu'une obligation légale expire. Aucun exploit nécessaire : omission pure.

## Correctifs proposés, tous compatibles SQL-sans-jugement

- **Attestation croisée par jointure.** Ne compter que des événements qu'une direction ne
  peut pas produire seule. BUILD abouti = phase Raj/Diego/Zara ET revue Elena ET log de
  déploiement Jordan. Décision exécutée = statut ET clé étrangère non nulle vers un
  artefact écrit par un autre acteur. Lead = clé étrangère vers un signal antérieur.
- **Métriques tri-état** : `valeur | INCONNU | PERIME`, jamais un nombre nu. Si la table
  source n'a reçu aucune écriture sur la fenêtre → INCONNU, pas vert. Chaque requête
  vérifie le DSN et un invariant de volume avant de calculer — correctif systémique de
  l'incident `v_deos_signaux`, pas seulement son correctif ponctuel.
- **Conserver l'auto-score en regard du calcul**, et faire de l'écart le signal :
  |auto − calculé| > 20 → investiguer. Aucun des deux n'est seul la référence, donc
  résistant à Goodhart.
- **Renoncer à la comparaison inter-directions** : normaliser à 100 partout, ou traiter
  le score comme pointeur de triage — « où regarder en premier » — et non comme mesure
  de performance.

## Ce qui a été nuancé côté Claude

- L'exploit du wrapper retry sur Delivery est plus difficile qu'annoncé : les FAILED
  comptés viennent de la base plateforme, pas de n8n, et le droit d'adapter le dispositif
  est borné aux workflows n8n et scripts de supervision. **L'objection tient néanmoins** :
  29 exécutions sont déjà en CANCELLED contre 33 en FAILED — la porte de reclassement
  existe indépendamment de ce droit.
- Le test d'acceptation proposé — jouer soi-même chaque exploit — est juste, mais « une
  heure de travail » est optimiste : il n'existe pas de sandbox. Base unique. Il faut
  dupliquer la base de gouvernance au préalable.
- **La revue ne chiffre pas le coût.** Tri-état, gardes de base et attestation croisée
  sont plusieurs soirées, pas une. À trois semaines du 1er septembre, avec 60 décisions
  accordées non exécutées et trois échéances réglementaires, ce n'est pas neutre.

## Suites arbitrées par Sam le 11/08

**Immédiat — coût quasi nul :**
1. Table `echeances_reglementaires` (libellé, date, statut) saisie à la main. Métrique =
   jours restants sur échéance non couverte. Trois lignes suffisent pour le 1er septembre.
   Utile en soi, indépendamment des grilles.
2. Auto-score conservé en regard du score calculé, écart > 20 en alerte. Suppose
   d'obtenir un auto-score des cinq directions qui n'en produisent pas : une ligne de
   consigne dans les fiches.

**Après le 1er septembre :** tri-état, gardes de base, attestation croisée par jointure,
en commençant par CoS et Commercial — les deux où l'écrivain et le mesuré sont confondus.

**D'ici là :** les grilles tournent en observation, sans affichage ni conséquence. Coût
nul, et ça construit la série temporelle qui manque aujourd'hui.
