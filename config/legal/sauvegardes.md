# Sauvegardes — dispositif et preuve

> Mis en place le 08/08/2026. Ce n'est pas un confort : c'est une **obligation
> contractuelle** imposée par l'accord d'hébergement Hostinger.

## Pourquoi

L'accord d'hébergement de Hostinger, section « Storage and security », est
explicite :

- le client est **seul responsable** de « maintenir des copies d'archive et de
  sauvegarde indépendantes » de son contenu ;
- la sauvegarde de Hostinger « s'exécute une fois par semaine et écrase les
  précédentes », et n'est fournie qu'« à titre gracieux, modifiable à tout
  moment à la seule discrétion de Hostinger » ;
- « Hostinger n'est pas responsable des fichiers ni des données présentes sur
  votre compte » ; « nos serveurs ne sont pas une archive ».

Et sur la sécurité : le client est « seul responsable de l'installation des
mesures organisationnelles et techniques protégeant suffisamment les données
personnelles stockées ou traitées sur son serveur ».

**Conséquence** : le chiffrement nous incombe. Ce n'est pas une lacune de
l'hébergeur, c'est le partage de responsabilité normal d'un serveur auto-géré.

## Ce qui est en place

| Élément | Valeur |
| --- | --- |
| **Fréquence** | quotidienne, 03h15 UTC (`/etc/cron.d/dh-backup`) |
| **Portée** | base plateforme (`digital_humans_db`) + base comité |
| **Chiffrement** | **AES-256** symétrique, GnuPG |
| **Clé** | `/etc/dh-backup/passphrase`, 64 caractères aléatoires, lecture root seule |
| **Emplacement** | `/var/backups/dh`, droits 700, fichiers en 600 |
| **Rétention** | 30 jours, purge automatique |
| **Volume** | ~22 Mo par exécution |
| **Alerte** | Telegram **en cas d'échec seulement** — le silence vaut succès |
| **Journal** | `/var/log/dh-backup.log` |

## Vérification faite le 08/08

- Sauvegarde produite : plateforme 22 Mo, comité 156 Ko.
- **Restauration testée** : déchiffrement réussi, 5 tables retrouvées
  (`curseurs`, `decisions`, `deos_state`…), 604 lignes SQL cohérentes.
- Fichier illisible sans la clé : `PGP symmetric key encrypted data - AES`.

## ⚠️ Ce qu'il reste à faire, et c'est important

**La clé de chiffrement vit sur le serveur qu'elle protège.** Si le serveur est
perdu, les sauvegardes deviennent indéchiffrables — elles ne servent alors à
rien.

**Action pour Sam** : copier `/etc/dh-backup/passphrase` dans un endroit sûr et
distinct — gestionnaire de mots de passe, coffre-fort physique, second support
chiffré. Sans cela, le dispositif protège la confidentialité mais pas la
continuité.

**Deuxième point** : les sauvegardes restent sur le même serveur. Un sinistre
matériel les emporterait avec la base. Une copie hors-site (stockage objet
chiffré, ou simple synchronisation vers un autre emplacement) complèterait le
dispositif. À faire quand il y aura des clients — pas avant, le coût ne se
justifie pas.

## Ce qu'on peut désormais écrire, en vérité

> « Les sauvegardes de la base de données sont réalisées quotidiennement et
> chiffrées (AES-256) avec une clé dont nous avons le contrôle exclusif. »

Cette phrase est vraie, vérifiable, et la preuve est chez nous — elle ne dépend
d'aucun tiers.
