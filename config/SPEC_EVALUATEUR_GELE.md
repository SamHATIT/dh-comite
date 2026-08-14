# Évaluateur gelé — sortir la notation des directeurs de leurs propres mains

> **Origine :** Sam, 11/08, à partir du pattern `autoresearch` de Karpathy (mars 2026).
> **Statut : instruction, pas décision.** Rien n'est implémenté.

## Le pattern, et ce qu'on en retient

`autoresearch` tient en trois pièces : un fichier éditable, **un évaluateur gelé**, une
métrique scalaire. L'agent modifie, l'évaluateur note, git garde ou annule. 630 lignes.

La pièce qui compte ici est la deuxième. Le gain de 53 % obtenu par Shopify sur Liquid
**n'a pas été mergé et a été signalé comme surajustement**. Une étude de 403 commits
d'agents (MSR 2026) montre l'indice de maintenabilité en baisse dans 56,1 % des cas.
Le pattern produit fidèlement un optimum **au regard de la métrique** — loi de Goodhart.
Sans évaluateur gelé, un agent optimise sa note, pas la réalité.

## Constat du 11/08 : le problème est en amont

Vérification faite sur les 12 rondes des 10 et 11/08 (6 directeurs × 2 jours) :

- **Un seul score exploitable** : Delivery, 56/100, le 11/08.
- Les cinq autres directeurs **n'en produisent aucun**.
- La seule consigne existante est dans la fiche du Delivery : « calcul du domain_score
  avec sa formule visible ». Autrement dit : invente ta formule et montre-la.
  **Aucune grille n'est définie nulle part.**
- Formule employée ce matin : 100 −20 (critique) −12 (haute) −12 (haute) = 56. Elle
  vit dans la réponse du modèle, pas dans un fichier. Rien n'empêche une autre
  pondération demain, remontant le score sans qu'un fait ait changé.

**Il n'y a donc rien à geler : il n'y a pas de mesure.** Le chantier n'est pas de
verrouiller une grille, c'est d'en créer une.

## Ce que ça vaut

Sans mesure comparable, trois choses sont impossibles, et les trois sont demandées
ailleurs dans le dispositif :

1. **Suivre une tendance.** Le brief annonce un « score de santé » qu'aucune ronde
   n'alimente de façon reproductible.
2. **Tenir R11.** Le dossier de revue externe engage le CEO à assurer la continuité
   pendant l'absence de Sam du 7 au 20 septembre. Sans métrique stable, « ça va » ou
   « ça ne va pas » dépend du modèle du jour.
3. **Mesurer l'effet d'un changement.** Les curseurs ont été rouverts le 11/08. On ne
   pourra pas dire si ça a amélioré quoi que ce soit : il n'y a pas de point de départ.

## Comment — l'évaluateur est du SQL, pas un LLM

M�me principe que le pré-calcul de `daily.sh` : ce qui est calculable de façon
déterministe ne doit pas être confié au modèle. Un script `bin/evaluer` lit la base,
calcule le score de chaque direction, l'écrit en base. **Les directeurs le LISENT.
Ils ne l'écrivent jamais.** Le garde-fou de curseur l'interdit techniquement.

M�triques candidates, toutes comptables sans jugement :

| Direction | Métriques non négociables |
| --- | --- |
| Delivery | exécutions FAILED < 48 h sans décision ; jours depuis dernier BUILD abouti ; workflows en échec ; services down |
| Commercial | leads créés dans Salesforce (pas ailleurs) ; âge du plus vieux lead non traité ; signaux non qualifiés |
| Marketing | contenus publiés vs planifiés ; jours depuis dernière publication |
| Customer Success | tickets ouverts ; délai de première réponse |
| Legal | échéances réglementaires à moins de 30 j non couvertes |
| Chief of Staff | décisions accordées non exécutées ; âge médian ; décisions en attente de Sam |

Le dernier est le plus parlant : **60 accordées pour 5 en exécution au 11/08**. Ce
nombre se compte, il ne se négocie pas.

## Séquence

1. Écrire `bin/evaluer` pour **une seule** direction — le Chief of Staff, dont les
   métriques sont déjà toutes en base et ne demandent aucune source nouvelle.
2. Le faire tourner en parallèle des rondes pendant une semaine, sans rien changer
   aux fiches. Comparer le score calculé au ressenti du directeur.
3. Si l'écart est instructif, étendre aux cinq autres et retirer des fiches toute
   consigne d'auto-notation.

**Ce qu'on n'implémente PAS** : la boucle nocturne garder-ou-annuler d'`autoresearch`.
Elle suppose un artefact modifiable en sécurité et une métrique fidèle. Ni l'un ni
l'autre n'existe ici. L'évaluateur d'abord ; la boucle est une question distincte,
qui ne se posera que si la mesure tient.
