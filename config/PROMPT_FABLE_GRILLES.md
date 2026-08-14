Tu es sollicité comme contradicteur sur un dispositif de notation qui n'est pas encore
en service. Rien n'est figé : si tu conclus que l'approche entière est mauvaise, dis-le.

## La situation

Six directions IA — Delivery, Commercial, Marketing, Customer Success, Legal, Chief of
Staff — tiennent une ronde quotidienne et produisent un rapport. Elles se notent
elles-mêmes sur 100, avec une formule qu'elles écrivent dans leur réponse.

Vérification faite sur douze rondes (six directions, 10 et 11 août) : **une seule
direction produit effectivement un score.** Sa série : 88 le 9 août, 68 le 10, 56 le 11.
Trente-deux points en deux jours, avec une pondération réinventée à chaque fois et qui
n'existe dans aucun fichier. Les cinq autres n'en produisent aucun.

On veut remplacer ça par un évaluateur que les directions lisent sans pouvoir l'écrire :
un script qui interroge la base et calcule le score par requêtes déterministes. Le
principe vient du pattern `autoresearch` publié par Karpathy en mars 2026 — un fichier
éditable, un évaluateur gelé, une métrique scalaire, une boucle garder-ou-annuler. On
n'implémente pas la boucle, seulement l'évaluateur.

## Pourquoi on te demande d'attaquer plutôt que de valider

Le point faible du pattern est documenté. Le gain de 53 % obtenu par Shopify sur son
moteur Liquid avec `autoresearch` n'a jamais été mergé : signalé comme surajustement.
Une étude de 403 commits d'agents présentée à MSR 2026 (Horikawa et al.) montre que
l'indice de maintenabilité baisse dans 56,1 % des cas et la complexité cyclomatique
augmente dans 42,7 %. Le pattern produit fidèlement un optimum **au regard de la
métrique** — ce qui vaut exactement ce que vaut la métrique. Loi de Goodhart.

Une grille fausse est plus dangereuse qu'une absence de grille : elle produit du vert
avec l'autorité du calcul. C'est arrivé pendant la rédaction — une première version
notait le Delivery 100/100 le jour où son directeur se notait rouge à 56, faits
sourcés à l'appui. Cause : une valeur cherchée dans la mauvaise colonne, et une
confusion entre deux étapes du pipeline. Corrigé, mais l'épisode est le sujet.

## Les grilles, telles qu'elles sont aujourd'hui

**Chief of Staff — 61/100**
- décisions accordées non exécutées : 61 (seuil 10) → (n−10)/2, plafond 30
- âge de la plus vieille accordée : 28 j (seuil 14) → n−14, plafond 20
- décisions en attente du dirigeant : 5 (seuil 5) → (n−5)×2, plafond 10
- dont en attente depuis plus de 7 j : 0 (seuil 0) → n×5, plafond 15

**Delivery — 61/100**
- exécutions FAILED sur 7 j : 0 (seuil 0) → n×5, plafond 25
- jours depuis dernier SDS abouti : 0 (seuil 3) → (n−3)×3, plafond 15
- jours depuis dernier BUILD abouti : 99 (seuil 3) → (n−3)×3, plafond 25
- phases BUILD en échec : 0 (seuil 0) → n×4, plafond 20
- exécutions bloquées en validation client : 10 (seuil 3) → (n−3)×2, plafond 15

**Commercial — 75/100**
- leads créés sur 30 j : 0 (seuil 5) → (5−n)×5, plafond 25
- signaux non qualifiés : 16 (seuil 20) → (n−20)/4, plafond 25
- âge du plus vieux signal non traité : 8 j (seuil 30) → (n−30)/2, plafond 20

**Marketing — 50/100**
- contenus publiés sur 30 j : 0 (seuil 4) → (4−n)×8, plafond 30
- jours depuis dernière publication : 99 (seuil 10) → n−10, plafond 20
- jours depuis dernier rapport de veille : 5 j (seuil 10) → n−10, plafond 15

**Customer Success** et **Legal** n'ont aucune grille. Zéro client pour l'un ; aucune
source d'échéances réglementaires en base pour l'autre, alors que trois échéances
tombent le 1er septembre.

## Ce qu'on a observé et qui inquiète

À prendre comme des observations, pas comme un plan de travail. Tu es libre de les
écarter si tu vois plus important ailleurs.

Le même jour où ces grilles ont été écrites, les droits des six directions ont été
élargis : elles peuvent désormais exécuter les décisions déjà accordées, le Commercial
peut écrire dans le CRM, le Delivery peut adapter les workflows d'automatisation. Ce
qui veut dire que **chaque direction a maintenant prise sur ce qu'on lui compte.** Le
Chief of Staff note un stock de décisions qu'il alimente lui-même. Le Commercial compte
des enregistrements CRM qu'il crée. Le Delivery peut modifier les automatisations dont
on mesure les défaillances. Les droits qui les débloquent sont ceux qui rendent les
mesures manipulables.

Antécédent réel : 112 prospects ont été tenus hors du CRM, dans des fichiers texte,
pendant des semaines. Une règle interne dit que ce qui n'est pas dans le CRM n'existe
pas — elle a été contournée sans que personne ne mente.

Le Marketing ne comporte aucune métrique de qualité : rien n'empêche de publier quatre
textes vides.

## Contraintes

Toute métrique doit se compter en SQL, sans jugement. Si elle demande une appréciation,
elle est hors sujet. Ne propose pas de faire noter par un modèle de langage : c'est
précisément ce qu'on supprime.

Sources disponibles. Base de gouvernance : décisions, curseurs de droits, état,
historiques de score et de santé. Base applicative : exécutions, phases de build, leads,
signaux commerciaux, prospects (vide), articles de blog (vide), rapports de veille,
sections, projets. Le CRM externe est accessible en écriture par le Commercial via un
script dédié, et en lecture par tous.

## Ce qu'on attend

Choisis ton angle et ta méthode. Le format du rendu est le tien.

Ce qui compte : qu'on sache, avant de mettre ce dispositif en service, ce qu'il permet
de faire semblant. Une revue qui conclut que les grilles sont bonnes aura échoué —
non parce qu'on veut du négatif, mais parce que la question posée est celle des angles
morts, et qu'un dispositif de notation en a toujours.
