---
name: dh-charte-documents
description: >
  Règles de sortie des documents Digital·Humans — structure, mise en forme,
  graphiques. À charger AVANT d'écrire tout rapport, toute étude, tout
  livrable destiné à être lu par un humain. Contient la charte visuelle, les
  gabarits Word et matplotlib prêts à l'emploi, et les interdits.
---

# Charte des documents — Digital·Humans

> Posée le 09/08/2026 sur ce constat de Sam : *« regarde toi-même, c'est
> illisible »*. Une étude commerciale excellente sur le fond était devenue
> illisible parce qu'elle s'ouvrait sur un bloc JSON de plusieurs milliers de
> caractères.

## La règle qui prime

**Un document destiné à un humain ne commence jamais par une structure de
données.**

Le JSON, le YAML, les tableaux de résultats bruts ne sont pas des livrables :
ce sont des sous-produits. S'ils doivent figurer, ils vont **en annexe, à la
fin**, jamais en tête.

**Test avant de rendre** : est-ce que les cinq premières lignes disent ce que le
lecteur doit retenir ? Si elles décrivent la méthode, l'outillage ou le format,
on réécrit.

---

## Structure obligatoire

1. **Titre** — ce dont il s'agit, en une ligne.
2. **Statut** — proposition, constat, décision ? Et qui tranche.
3. **Ce qu'il faut retenir** — trois à cinq affirmations, avant toute
   justification. Le lecteur qui s'arrête là doit avoir l'essentiel.
4. **Le corps** — titres de niveau 2 maximum, jamais de niveau 4.
5. **Les réserves** — ce qu'on ne sait pas, ce qui manque, ce qui pourrait
   invalider. Jamais noyé au milieu.
6. **Annexes** — méthode détaillée, données brutes, JSON.

**Longueur** : si le corps dépasse 15 000 caractères, produire **deux**
documents — une synthèse de trois pages et l'étude complète. Sam lit la
synthèse, l'étude sert de preuve.

---

## Charte visuelle

| Élément | Valeur |
| --- | --- |
| Encre | `#2B2B2E` |
| Laiton (accents, filets) | `#C8A97E` |
| Gris secondaire | `#6B6B70` |
| Alerte / plancher | `#9B2C2C` |
| Favorable / seuil atteint | `#2F6B4F` |
| Fond d'encadré | `#FBF9F5` |
| Fond d'en-tête de tableau | `#F7F5F1` |
| Filets de tableau | `#EDEAE4` |
| Police | Calibri (documents), JetBrains Mono (écrans du comité) |

**Titres** : 28 demi-gras avec filet laiton en dessous pour le niveau 1,
23 demi-gras pour le niveau 2. **Corps** : 21. **Tableaux** : 19, en-têtes 17.

---

## Les graphiques — quand et comment

**Quand** : dès qu'un chiffre doit être *comparé* ou *situé par rapport à un
seuil*. Une marge, une projection, une répartition. Sam l'a dit le 09/08 :
« un graphique ou une illustration aide réellement à projeter ».

**Quand PAS** : trois valeurs qui tiennent dans une phrase. Un graphique à deux
barres est une perte de temps pour tout le monde.

**Comment** : matplotlib, style sobre, aucune fioriture. Le gabarit est dans
`charte.py` de ce skill — il pose les couleurs, la police, la grille et les
seuils. L'utiliser tel quel.

**Trois types suffisent** :

- **barres horizontales** pour comparer des canaux ou des options ;
- **ligne avec zone de seuil** pour situer une valeur par rapport à un plancher
  et une parité — c'est le cas d'usage le plus fréquent chez nous ;
- **empilement** pour une répartition de coûts.

Jamais de camembert : l'œil compare mal les angles.

---

## Interdits

- **Aucun JSON, YAML ou dictionnaire Python en tête de document.**
- Aucun titre de niveau 4 ou plus.
- Aucun tableau de plus de six colonnes — au-delà, il faut deux tableaux.
- Aucun graphique sans son unité et sa source.
- Aucune couleur hors charte.
- Aucun camembert.
- Aucun chiffre sans sa source ou sa mention `Hypothèse`.

---

## Production Word

Le gabarit `gabarit_docx.js` de ce skill contient les fonctions prêtes :
`h1`, `h2`, `table`, `encadre`, `rich`. Marges 1250/1150/1400/1400,
largeur de tableau 9360.

**Vérification obligatoire avant de rendre** : convertir en PDF, rasteriser,
et **regarder les pages**. Un document qu'on n'a pas vu n'est pas fini.

```bash
soffice --headless --convert-to pdf doc.docx
pdftoppm -jpeg -r 85 doc.pdf page
```
