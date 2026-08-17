# LOT-00 — Règle de documentation

> **À lire avant tout autre lot. Ce n'est pas un lot exécutable : c'est une condition
> d'acceptation de tous les autres.**

## La règle

**Un lot dont la documentation manque n'est pas terminé.** Ce n'est pas une bonne
intention, c'est un critère d'acceptation au même titre que les tests.

## Pourquoi elle est écrite ici

Elle a été rappelée de nombreuses fois, et elle n'a jamais tenu. Le crochet
`post-commit` régénère bien le journal à partir des messages de commit — mais rien
n'oblige à documenter **ce qui a changé et pourquoi**. La conséquence s'est vue
plusieurs fois : un correctif posé, oublié, puis re-diagnostiqué quelques jours plus
tard depuis zéro.

## Ce que « documenté » veut dire

### 1. Le message de commit

| Élément | Question à laquelle il répond |
| --- | --- |
| **Quoi** | qu'est-ce qui change concrètement |
| **Pourquoi** | quel défaut, quel incident, quelle demande — avec la date |
| **Ce que ça remplace** | quel comportement disparaît, et pourquoi il était faux |

Le troisième est le plus souvent omis et le plus utile : sans lui, on ne sait pas si
un comportement absent est un oubli ou une décision.

### 2. Le fichier de documentation

Chaque lot nomme le sien. Il doit contenir le **raisonnement**, pas seulement le
résultat : un lecteur qui arrive dans trois mois doit comprendre pourquoi la chose est
faite ainsi et pas autrement.

### 3. Le commentaire dans le code

Pour toute règle non évidente, une phrase expliquant l'incident qui l'a motivée.

## Ce qui ne compte pas comme documentation

- Un message de commit qui décrit le diff (« ajout de la fonction X »).
- Un fichier qui liste les commandes sans dire à quoi elles servent.
- Un « voir la décision DEC-XXXX » sans reprendre le motif.

## Vérification

```bash
test -f docs/<FICHIER_DU_LOT>.md && wc -l docs/<FICHIER_DU_LOT>.md
git log -1 --format=%B | head -20
```
