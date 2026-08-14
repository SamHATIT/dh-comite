# Mission Fable — attaquer les grilles de notation avant leur mise en service

> **Commanditaire :** Sam Hatit, 11/08/2026.
> **Nature : contradiction adversariale.** On ne demande pas d'améliorer les grilles.
> On demande de démontrer comment on peut les satisfaire **sans rien améliorer**.

## Contexte en dix lignes

Six directions IA (Delivery, Commercial, Marketing, Customer Success, Legal, Chief of
Staff) produisent chaque matin un rapport et se notent elles-mêmes sur 100. Vérification
du 11/08 sur douze rondes : **une seule direction produit un score**, avec une formule
inventée à chaque ronde. Sa série : 88 le 09/08, 68 le 10/08, 56 le 11/08.

On applique le principe de l'évaluateur gelé (pattern `autoresearch`, Karpathy, mars
2026) : le score n'est plus produit par l'agent mais calculé par des requêtes
déterministes, dans `bin/evaluer`, que les directions lisent sans pouvoir écrire.

Le risque est nommé : **loi de Goodhart.** Le gain de 53 % obtenu par Shopify avec
`autoresearch` n'a pas été mergé, signalé comme surajustement. Une étude de 403 commits
d'agents (MSR 2026) montre l'indice de maintenabilité en baisse dans 56,1 % des cas.
Le pattern produit fidèlement un optimum **au regard de la métrique** — ni plus, ni moins.

## Ce qu'on te demande

Pour **chaque métrique** ci-dessous, produire :

1. **Le contournement le moins coûteux.** Concrètement : quelle action un agent
   peut-il entreprendre, en restant dans son périmètre et sans mentir, qui améliore le
   score sans améliorer la situation réelle ?
2. **Le signal que la métrique masque.** Que peut-il se dégrader gravement pendant que
   le score reste au vert ?
3. **Le correctif proposé** : métrique de remplacement, contre-métrique appariée, ou
   suppression pure. Une métrique qu'on ne sait pas rendre robuste doit être retirée,
   pas affaiblie.

Une contre-métrique appariée est préférée quand elle existe : une mesure qui se dégrade
mécaniquement si l'on triche sur la première.

## Les grilles à attaquer

### Chief of Staff — score 61/100 au 11/08
| Métrique | Valeur | Seuil | Pénalité |
| --- | ---: | ---: | ---: |
| décisions accordées non exécutées | 61 | 10 | (n−10)/2, max 30 |
| âge de la plus vieille accordée (j) | 28 | 14 | n−14, max 20 |
| décisions en attente de Sam | 5 | 5 | (n−5)×2, max 10 |
| dont en attente depuis plus de 7 j | 0 | 0 | n×5, max 15 |

*Piste évidente à creuser, mais pas la seule : le Chief of Staff est la seule direction
qui écrit au registre des décisions. Il note donc un stock qu'il alimente lui-même.*

### Delivery — score 61/100 au 11/08
| Métrique | Valeur | Seuil | Pénalité |
| --- | ---: | ---: | ---: |
| exécutions FAILED sur 7 j | 0 | 0 | n×5, max 25 |
| jours depuis dernier SDS abouti | 0 | 3 | (n−3)×3, max 15 |
| jours depuis dernier BUILD abouti | 99 | 3 | (n−3)×3, max 25 |
| phases BUILD en échec | 0 | 0 | n×4, max 20 |
| exécutions bloquées en validation | 10 | 3 | (n−3)×2, max 15 |

*Le Delivery a, depuis le 11/08, le droit d'adapter les workflows et d'exécuter les
décisions accordées. Il peut donc agir sur ce qui est compté.*

### Commercial — score 75/100 au 11/08
| Métrique | Valeur | Seuil | Pénalité |
| --- | ---: | ---: | ---: |
| leads créés sur 30 j | 0 | 5 | (5−n)×5, max 25 |
| signaux non qualifiés | 16 | 20 | (n−20)/4, max 25 |
| âge du plus vieux signal non traité (j) | 8 | 30 | (n−30)/2, max 20 |

*Depuis le 11/08 il écrit dans Salesforce via `bin/sf-lead`. Il crée donc lui-même ce
qu'on compte. Antécédent réel : 112 prospects avaient été tenus hors système, en markdown.*

### Marketing — score 50/100 au 11/08
| Métrique | Valeur | Seuil | Pénalité |
| --- | ---: | ---: | ---: |
| contenus publiés sur 30 j | 0 | 4 | (4−n)×8, max 30 |
| jours depuis dernière publication | 99 | 10 | n−10, max 20 |
| jours depuis dernier rapport de veille | 5 | 10 | n−10, max 15 |

*Aucune métrique de qualité. Rien n'empêche de publier quatre textes vides.*

### Deux directions sans grille — à instruire
- **Customer Success** : zéro client à ce jour. Toute métrique serait creuse. Faut-il
  ne pas noter, ou noter la préparation ?
- **Legal** : aucune source d'échéances réglementaires en base. Trois échéances tombent
  le 1er septembre (AI Act art. 50, facturation électronique, compteur de jetons du
  palier gratuit). Quelle source créer, et que compter dessus ?

## Contraintes fermes

- Toute métrique se compte **en SQL**, sans jugement. Si elle demande une appréciation,
  elle est hors sujet.
- Sources disponibles — base comité : `decisions`, `curseurs`, `deos_state`,
  `v_deos_sante_histo`, `v_deos_scores_histo`. Base plateforme : `v_deos_executions`,
  `v_deos_build_phases`, `v_deos_leads`, `v_deos_signaux`, `v_deos_prospects` (vide),
  `v_deos_blog_articles` (vide), `v_deos_veille`, `v_deos_sections`, `v_deos_projects`.
- Salesforce est accessible en écriture par le Commercial via `bin/sf-lead` uniquement.
- **Ne pas proposer de faire noter par un LLM.** C'est précisément ce qu'on supprime.

## Livrable attendu

Un tableau par direction : métrique · contournement · signal masqué · correctif.
Puis une liste ordonnée des métriques à retirer avant mise en service.

Le succès de cette mission se mesure au nombre de failles trouvées, pas à la validation
des grilles. Une revue qui conclut que tout va bien aura échoué.
