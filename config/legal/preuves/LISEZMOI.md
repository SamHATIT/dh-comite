# Dossier de preuves — hébergement et sous-traitance

> Pièces à produire quand un client, un DSI ou un auditeur pose la question.
> Chaque affirmation de nos pages légales doit trouver ici sa justification.

## Hostinger — notre hébergeur et sous-traitant

### Certificat ISO/IEC 27001:2022 ✅ PIÈCE FORTE

`Hostinger_ISO_IEC_27001_2022.pdf` — à demander à Sam s'il manque au dépôt
(exclu du dépôt Git par prudence, document tiers).

| Élément | Valeur |
| --- | --- |
| **Entité certifiée** | HOSTINGER operations, UAB — Vilnius, Lituanie |
| **Périmètre** | Vente et gestion de domaines, hébergement web, **hébergement VPS**, constructeur de sites, services de messagerie et support |
| **Organisme certificateur** | TÜV Thüringen e.V., accrédité DAkkS (D-ZM-16006-03-00) |
| **N° d'enregistrement** | 1512124260 |
| **Rapport d'audit** | 3330/3GBH/B0 |
| **Déclaration d'applicabilité** | révision du 11/04/2025 |
| **Validité** | du 07/10/2025 au **26/06/2027** |

**Pourquoi cette pièce compte** : le périmètre nomme explicitement
« VPS hosting ». Ce n'est pas une certification générique — elle couvre le
service que nous utilisons. Et elle est **vérifiable par un tiers** sur
`www.tuev-thueringen.de`, ce qu'un DSI fera.

**Échéance à surveiller** : renouvellement avant le 26/06/2027.

### Ce que Hostinger s'engage à faire — et ce qu'il ne fait pas

**Accord d'hébergement** (`hostinger.com/legal/hosting-agreement`), section
« Storage and security » — **le document contractuellement opposable** :

- le client est **seul responsable** de maintenir des copies de sauvegarde
  indépendantes ;
- la sauvegarde de Hostinger est **hebdomadaire**, écrase la précédente, et
  n'est fournie qu'**à titre gracieux, modifiable à tout moment** ;
- « Hostinger n'est pas responsable des fichiers ni des données présentes sur
  votre compte » ; « nos serveurs ne sont pas une archive » ;
- la sécurité des données stockées sur le serveur **incombe au client** ;
- les services **ne fournissent pas un environnement conforme PCI ou HIPAA**.
  → à retenir pour les prospects bancaires et santé.

**Addendum de traitement des données** (`hostinger.com/legal/dpa`) : mesures
couvrant la sécurité de leur réseau, la sécurité physique des installations, le
contrôle des accès de leur personnel, et l'évaluation de ces mesures. **Aucun
engagement de chiffrement des données clients au repos.**

### Fiche « Disk Encryption » du centre de confiance — à manier avec prudence

Elle indique un chiffrement de disque pour « appareils mobiles, ordinateurs
portables et supports amovibles », puis que « les bases contenant des
informations confidentielles ou personnelles sont également chiffrées au repos,
là où c'est possible », et que « cet engagement s'étend aux sauvegardes ».

**Ne pas s'appuyer dessus pour nos pages légales**, pour trois raisons : la
fiche est classée sous *Endpoint Security* — le contexte est celui de leurs
propres actifs, pas des instantanés de VPS clients ; la réserve « là où c'est
possible » n'engage à rien ; et une fiche de centre de confiance **n'est pas
contractuelle**, contrairement à l'accord d'hébergement qui dit l'inverse.

## Ce que nous pouvons affirmer, et sur quelle base

| Affirmation | Preuve |
| --- | --- |
| Hébergeur certifié ISO/IEC 27001:2022, périmètre incluant le VPS | certificat TÜV ci-dessus |
| Serveur en France | `ipinfo.io/72.61.161.222` → FR / Paris |
| Sauvegardes conservées dans l'UE | panneau Hostinger → Pays-Bas |
| **Sauvegardes quotidiennes chiffrées AES-256, clé sous notre contrôle exclusif** | **notre propre dispositif** — `config/legal/sauvegardes.md`, restauration testée le 08/08 |

La dernière ligne est la plus solide : elle ne dépend d'aucun tiers.
