---
name: dh-conformite-juridique
description: >
  Conformité RGPD et AI Act pour Digital·Humans : sources faisant foi,
  méthode de vérification par la preuve, mentions obligatoires d'un site,
  cadre du sous-traitant, et pièges déjà rencontrés. À utiliser pour toute
  ronde juridique, audit de conformité, rédaction de mentions légales, ou
  question sur le traitement des données clients.
---

# Conformité — Digital·Humans

Environnement : `$COMITE_DB_DSN` · périmètre d'écriture `rapport_legal`,
`conformite_ia`, `registre_traitements` · livrables dans
`/workspace/config/legal/`.

## La règle qui prime sur tout

**On n'affirme jamais une mesure qu'on ne peut pas prouver.**

Le risque juridique n'est pas l'absence de protection — c'est la **déclaration
inexacte**. En cas d'incident, c'est ce qu'on a écrit qui est opposé, pas le
niveau réel de protection.

Cas réel du 08/08 : la politique de confidentialité affirmait « les secrets
d'API sont gérés via un coffre dédié » et « les sauvegardes sont chiffrées au
repos ». Ni l'un ni l'autre n'existait. Corrigé par une **description exacte**
de ce qui est fait, pas par la construction du coffre.

**Méthode** : pour chaque affirmation, exiger la preuve — une requête, un
document contractuel, une configuration. Si elle n'existe pas, retirer
l'affirmation ou produire la preuve. Jamais laisser en l'état.

## Ce qui est établi et sourcé (ne pas ré-instruire)

| Sujet | État | Source |
| --- | --- | --- |
| Localisation | Serveur **Paris**, sauvegardes **Pays-Bas** — deux pays UE | `config/legal/souverainete_donnees.md` |
| Chiffrement des sauvegardes par l'hébergeur | **Non garanti.** Le contrat ne l'engage pas ; la sauvegarde hebdomadaire est une « courtoisie » révocable | accord d'hébergement Hostinger, section *Storage and security* |
| Sauvegarde propre | **Quotidienne, AES-256, clé sous notre contrôle**, restauration testée | `config/legal/sauvegardes.md` |
| Entraînement des modèles | Anthropic : « les données conservées ne sont **jamais** utilisées pour l'entraînement sans permission expresse » | documentation API Anthropic, rétention des données |
| Rétention zéro | **Pas le comportement par défaut** — s'obtient sur demande, par organisation | idem |
| Modèle du comité | Fable 5 **exige 30 jours** de rétention, rétention zéro indisponible. Acceptable : aucune donnée client n'y transite | arbitrage Sam 08/08 |
| Coffre à secrets | **Pas une obligation légale.** L'article 32 exige des mesures « appropriées », pas un outil précis | arbitrage Sam 08/08 |

## Le partage de responsabilité avec l'hébergeur

Sur un serveur auto-géré, **la sécurité de ce qui vit dans le serveur incombe
au client**. C'est écrit dans le contrat, et c'est la règle constante chez tous
les hébergeurs.

Conséquences pratiques : le chiffrement nous incombe · les sauvegardes
indépendantes nous incombent · nous restons **responsable de traitement**, sans
transfert de responsabilité vers l'hébergeur.

À savoir pour les prospects bancaires : les services Hostinger **ne sont pas
destinés à fournir un environnement conforme PCI ou HIPAA**. Un DSI de banque
posera la question.

## Mentions obligatoires d'un site (LCEN, art. 6-III-1)

Identité de l'éditeur · statut et immatriculation · adresse · contact ·
directeur de publication · **hébergeur avec ses coordonnées**.

Pour Digital·Humans : entrepreneur individuel, SIREN 343172490, RNE, APE 6202A,
TVA en franchise (art. 293 B), hébergeur Hostinger International Ltd.

**Vaut pour TOUS les sites**, y compris une simple vitrine sans collecte.
Manquement constaté le 08/08 sur `samhatit-consulting.cloud` et `deos.cloud`.

## AI Act — ce qui nous concerne

**Article 50 — transparence.** Un système conversationnel doit indiquer qu'il
est une IA. Fait sur le widget Sophie, dans les deux langues.

**Conséquence sur la communication** : les agents ne doivent jamais être
présentés comme un effectif humain. D'où l'interdiction du portrait
photoréaliste (`CONT-2026-0804-03`) — contrainte qui a orienté toute la
campagne vidéo, et pour le mieux.

**Article 14 — contrôle humain.** Notre curseur d'autonomie y répond
directement : 36 réglages en base, garde-fou branché, journal des refus.

## Le consentement à l'inscription

**Séparer** ce qui est accepté (le contrat) de ce qui est porté à connaissance
(l'information sur les données). Une acceptation globale mélangeant CGV et
données n'est pas valable (art. 4.11 et 7). Une case pré-cochée n'est pas un
consentement.

**Nuance qui simplifie** : le traitement des données du client repose sur
l'**exécution du contrat** (art. 6.1.b), pas sur le consentement. On informe,
on ne quémande pas.

## Pièges rencontrés

**Le canal d'écriture peut être cassé sans le dire.** Le Juridique n'avait
aucun périmètre dans `deos-state` du 02 au 08/08 : ses rapports étaient refusés
en silence. Vérifier qu'on peut écrire avant de travailler.

**Une fiche de centre de confiance n'est pas contractuelle.** Elle décrit une
intention commerciale ; le contrat engage. En cas d'écart, **le contrat prime**.

**Attention au périmètre d'une affirmation.** Hostinger annonce chiffrer « les
bases contenant des informations confidentielles » — mais la fiche est classée
sous *sécurité des postes de travail*. Il s'agit de leurs systèmes internes,
pas des instantanés de VPS clients. Toujours vérifier de quoi on parle.

**Un réglage d'interface n'est pas une preuve contractuelle.** Désactiver
l'entraînement sur un compte personnel ne dit rien du régime applicable à
l'API commerciale. Deux contrats, deux régimes.

## Format de sortie

Chaque avis porte : le constat, sa **preuve** (requête, document, configuration),
sa gravité, et l'action précise. Un point non prouvable est déclaré comme tel —
« non vérifiable avec mes accès » est une réponse acceptable et utile.

Signaler ce qui doit passer par un avocat. Nous préparons une mise en
conformité, nous ne délivrons pas de conseil juridique.
