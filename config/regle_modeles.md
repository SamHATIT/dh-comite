# Règle des modèles — arbitrage de Sam du 06/08/2026

> **Toujours la dernière version d'une famille, sauf raison explicite.**

## Pourquoi

Le 6 août, la facture du jour montrait **six modèles différents pour 8,90 $** —
dont deux générations obsolètes. Trois causes distinctes, toutes évitables :

- des versions **figées et datées** dans les scripts (`claude-opus-4-8`,
  `claude-fable-5`), écrites une fois puis jamais revues ;
- une **table de routage** épinglée sur Opus 4.8 alors qu'Opus 5 est disponible ;
- une **invocation ponctuelle** lancée sur `claude-opus-4-5-20251101`, une
  version d'octobre — erreur de Claude lors de la mission du Directeur Juridique.

Une génération obsolète coûte autant ou plus, rend moins, et empêche toute
comparaison entre exécutions.

## La règle

**Dans les scripts du terminal** (`claude -p`) : utiliser l'**alias court** —
`opus`, `sonnet`, `haiku`. Il pointe toujours vers la dernière version. Ne
jamais écrire de version datée.

**Dans la table de routage de la plateforme** (`llm_routing.yaml`) : l'API
n'accepte pas les alias courts, il faut donc épingler — mais **la dernière
version disponible**. La vérifier par `GET /v1/models` avant toute décision, ne
jamais la supposer.

**Exception** : une version figée n'est admise que pour reproduire un résultat à
l'identique, **ou pour un usage qui justifie un tier particulier**. Elle doit
alors porter, en commentaire à côté, la raison.

**L'exception en vigueur** : le **comité hebdomadaire** tourne sur
`claude-fable-5`, et c'est délibéré. Son analyse croisée en quatre phases —
incohérences factuelles, collisions de plans, synergies manquées, décisions
orphelines — justifie le tier supérieur. Les rondes quotidiennes restent sur
`sonnet`, le brief du jour sur `opus`.

**Le principe réel n'est donc pas « toujours le plus récent » mais « le modèle
adapté au besoin, dans sa dernière version »** : Haiku pour l'extraction
mécanique, Sonnet pour les rondes, Opus pour le brief, Fable pour l'analyse
croisée hebdomadaire.

## État au 06/08/2026

| Usage | Modèle | Forme |
| --- | --- | --- |
| CEO digital, brief quotidien | `opus` | alias |
| **Comité hebdomadaire** | **`claude-fable-5`** | **épinglé — exception documentée** |
| Rondes des six directions | `sonnet` | alias |
| Plateforme — tier orchestrateur | `claude-opus-5` | épinglé, dernière version |
| Plateforme — tier ouvrier | `claude-sonnet-5` | épinglé, dernière version |
| Plateforme — extraction mécanique | `claude-haiku-4-5-20251001` | épinglé, dernière de la famille Haiku |

## Contrôle

À chaque relevé de coût, si plus de trois modèles apparaissent sur une journée,
c'est le signe qu'une version obsolète subsiste quelque part. Chercher d'abord
dans les scripts, puis dans la table de routage, puis dans les invocations
ponctuelles.
