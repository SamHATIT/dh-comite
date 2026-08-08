# Souveraineté des données — choix d'architecture

> Décision de Sam, confirmée le 08/08/2026. Ce n'est pas une conséquence
> d'attribution : la localisation a été **choisie** au moment de la commande.

## Ce qui est établi et vérifiable

| Élément | Localisation | Vérification |
| --- | --- | --- |
| **Serveur de production** | Paris, France | `ipinfo.io/72.61.161.222` → `FR / Paris` |
| **Sauvegardes** | Pays-Bas | panneau Hostinger, colonne « Emplacement » |
| **Hébergeur** | Hostinger International Ltd | certifié ISO/IEC 27001:2022 |

**Les données et leurs sauvegardes restent dans l'Union européenne**, sur deux
pays différents. La séparation géographique protège d'un sinistre local sans
sortir du cadre européen.

## Régime des sauvegardes

- **Fréquence** : hebdomadaire. Deux versions conservées, la plus ancienne
  remplacée automatiquement.
- **Évolution prévue** : passage au quotidien (22,99 €/mois) dès les premiers
  clients payants. Le coût n'est pas justifié avant.
- **Chiffrement au repos** : **non confirmé par Hostinger**. Leur support
  indique ne pas pouvoir l'attester ; ils confirment uniquement la certification
  ISO/IEC 27001:2022. **On ne l'affirme donc nulle part.** À réexaminer si une
  confirmation écrite est obtenue.

## Pourquoi cela compte commercialement

Un directeur informatique français ou européen pose systématiquement trois
questions avant d'ouvrir un compte : où sont les données, où sont les
sauvegardes, et qui peut y accéder. Les deux premières ont une réponse nette et
prouvable. C'est un **argument**, pas une contrainte — et il distingue
Digital·Humans de la plupart des plateformes concurrentes, hébergées aux
États-Unis.

À employer tel quel dans les échanges commerciaux, sans embellir : le jour où un
client vérifie, tout doit correspondre.

## Ce qui reste à établir

- Confirmation écrite du chiffrement des sauvegardes (demande à adresser au
  support Hostinger, ou via leur centre de confiance).
- Le sous-traitant Anthropic est aux États-Unis : couvert par des clauses
  contractuelles types, à documenter au registre des traitements.
