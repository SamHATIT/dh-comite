# Gabarits de graphiques — Comité Digital·Humans

*Livraison du 10 août 2026. Dix gabarits autonomes + une page d'index.*

---

## 1 · Nature du livrable

**Contrairement au paquet des trois écrans du comité, ces fichiers ne sont pas des
maquettes à recréer. Ce sont des composants à intégrer tels quels.**

Chaque fichier est autonome : HTML, CSS et JavaScript dans le même document, aucune
bibliothèque externe, aucune étape de compilation. Ils sont conçus pour être servis
directement par l'application Python.

Trois usages possibles, du plus simple au plus intégré :

1. **Servir le fichier tel quel.** Le gabarit est une page complète et valide.
2. **Injecter les données côté serveur.** Remplacer le bloc `DATA` par un rendu
   Jinja/f-string. C'est le cas d'usage prévu — voir §3.
3. **Extraire le fragment.** Reprendre `.card` + son `<script>` de rendu et le
   monter dans une page existante. Le CSS est préfixé par classe et ne fuit pas,
   à l'exception des variables `:root` (à hisser au niveau de l'application).

**Ne pas réécrire les rendus en D3 ou Chart.js.** L'absence de dépendance est une
contrainte du brief, pas une simplification de circonstance : ce qui n'est pas
autonome ne sera jamais intégré.

## 2 · Les dix gabarits

| Fichier | Gabarit | Usage | Cas réel servi |
| --- | --- | --- | --- |
| `01-seuils.html` | Situer une valeur entre deux seuils | Bureau | Options de prix DEOS, plancher 31 800 € / parité 79 400 € |
| `02-divergence.html` | Deux courbes qui divergent | Bureau | Facture API à l'usage contre forfait GPU 299 $ |
| `03-dette.html` | Une dette qui vieillit | Bureau et mobile | Décisions en attente, dont une à 27 jours |
| `04-poincon.html` | Un poinçon de santé | Bureau et mobile | Score 68, assiette Σ poids 0,70 |
| `05-progression.html` | Une progression sur un objectif | Bureau et mobile | Quatre directions sur six ayant rapporté |
| `06-repartition.html` | Répartition d'un coût | Bureau | Dépense par poste, brief quotidien à un quart |
| `07-comparaison.html` | Comparaison de trois options | **Bureau uniquement** | Trois modèles sur coût, durée, densité, analyse |
| `08-evolution.html` | Évolution dans le temps | Bureau | Score de santé sur douze jours |
| `09-binaire.html` | Un état binaire | Bureau et mobile | Ce qui est démontrable fin août |
| `10-decision.html` | Une carte de décision | **Mobile d'abord** | Arbitrage à 21 jours, trois gestes |

`index.html` les montre tous en aperçu vivant (iframes à l'échelle 0,5), avec la
palette et les quatre règles de fond. C'est la page à ouvrir en premier.

## 3 · Comment brancher des données

Chaque fichier ouvre sur un objet `DATA` dans son premier `<script>`. **Rien
n'est codé en dur plus bas** : le script de rendu ne lit que `DATA`.

```python
# FastAPI + Jinja, ou simple remplacement de chaîne
html = template.replace(
    "const DATA = {…};",
    "const DATA = " + json.dumps(payload, ensure_ascii=False) + ";"
)
```

Les clés de chaque `DATA` sont documentées par l'exemple lui-même : les valeurs
livrées sont des cas réels, pas des remplissages. Points d'attention :

- **`01-seuils`** — `plancher` et `parite` sont des faits métier, pas des cibles
  calculées. La couleur d'une barre découle de sa position, jamais d'un jugement
  saisi à la main.
- **`03-dette`** — `tranches` doit rester trié par `min` décroissant ; le premier
  seuil atteint gagne. `seuil` est une règle de gouvernance et ne bouge pas avec
  les données.
- **`04-poincon`** — `score: null` est un état valide : arc à zéro, tiret à la
  place du chiffre. **Ne jamais passer `0` pour signifier « non calculable ».**
- **`08-evolution`** — un point `{v: null}` interrompt le trait et affiche
  « N.C. ». Ne pas interpoler côté serveur pour « faire propre ».
- **`10-decision`** — un bloc `{texte: null}` affiche `n.c.` et garde sa place.

## 4 · Ce qui décide de la mise en page

### Bureau pour comprendre, mobile pour décider

Ce ne sont pas deux tailles, ce sont deux usages. **Chaque gabarit porte son
usage en haut à droite**, et l'annonce est tenue :

- `03` et `05` **se recomposent** sous 640 px — libellé sur sa ligne, barre pleine
  largeur dessous, valeur à droite. Ils ne réduisent pas un SVG large.
  La bascule est un `window.matchMedia('(max-width: 640px)')` en tête de rendu.
- `07` **dit qu'il est de bureau** plutôt que de se réduire mal. Sur téléphone il
  doit devenir une pile de fiches, une option par écran — non implémenté ici,
  c'est un autre gabarit à écrire si le besoin apparaît.
- `10` est dimensionné pour le pouce : zones tactiles de 48 px, carte à 420 px.

### Un chiffre n'est pas un feu tricolore

Le laiton `#C8A97E` porte l'accent. Le vert et le rouge ne servent **qu'aux seuils
franchis** — jamais à qualifier une valeur en soi. C'est ce qui empêche l'ensemble
de virer au tableau de bord d'aéroport.

Une valeur absente s'affiche `n.c.` ou en trame hachurée et **garde sa place**.
Jamais un zéro à la place d'un manque : le principe est le même que sur les trois
écrans du comité.

## 5 · Charte

| Rôle | Valeur | Variable CSS |
| --- | --- | --- |
| Fond | `#0E0E10` | `--bg` |
| Fond secondaire (cartes) | `#16161A` | `--bg-2` |
| Texte principal | `#CFCAC0` | `--fg` |
| Texte accentué | `#F5F2EC` | `--fg-strong` |
| Texte discret | `#6E6B66` | `--fg-mute` |
| Laiton | `#C8A97E` | `--brass` |
| Laiton foncé | `#7A6647` | `--brass-dk` |
| Favorable | `#4E8C6A` | `--good` |
| Alerte | `#9B4A4A` | `--bad` |
| Filets | `#FFFFFF14` | `--rule` |

**Typographies** : Cormorant Garamond (titres, italique pour les sous-titres et
les valeurs qualitatives) · Inter (texte courant, graisse 300) · JetBrains Mono
(chiffres, étiquettes, tout ce qui est technique).

Chargées depuis Google Fonts. Pour un fonctionnement hors ligne, les héberger
localement et remplacer le `<link>` — il est identique dans les onze fichiers.

Formes : rayon 2 px (boutons, jauges) et 4 px (cartes). Filets à 1 px. **Aucune
ombre portée, aucun dégradé.** Trames hachurées à 135°, pas de dégradé.

Équivalence avec `charte.py` (matplotlib) : mêmes couleurs, mêmes seuils, mêmes
conventions de manque. Les deux familles doivent rester alignées — toute évolution
de palette se répercute dans les deux.

## 6 · Ce qui existe déjà et qu'il ne faut pas refaire

Six écrans tournent sous `/comite/`. Deux gabarits en sont issus :

- **`04-poincon`** reprend le poinçon du tableau de bord, avec deux ajouts : les
  repères de quart sur l'anneau (une échelle sans légende) et la ligne d'assiette
  sous le mot. Un score calculé sur base réduite doit le dire, sinon il ment.
- **`10-decision`** harmonise la carte d'arbitrage mobile existante avec le reste
  du système. Une seule action pleine — accorder.

Les substituer aux implémentations actuelles plutôt que de les faire cohabiter.

## 7 · Ce que le paquet ne contient pas

- Pas de couche de récupération de données. Les gabarits ne connaissent pas les
  endpoints ; c'est délibéré.
- Pas de variante mobile pour `07`.
- Pas de gestion d'erreur réseau. Un `DATA` absent laisse la zone de rendu vide —
  à l'appelant de décider ce qu'il affiche alors.
- Pas d'accessibilité au-delà du contraste et du HTML sémantique : les SVG
  mériteraient un `<title>` et un `role="img"`, et une table de repli pour lecteur
  d'écran. À prévoir si le produit vise une conformité.

## 8 · Fichiers

```
graphiques/
├── index.html            ← ouvrir en premier
├── 01-seuils.html
├── 02-divergence.html
├── 03-dette.html
├── 04-poincon.html
├── 05-progression.html
├── 06-repartition.html
├── 07-comparaison.html
├── 08-evolution.html
├── 09-binaire.html
└── 10-decision.html
```
