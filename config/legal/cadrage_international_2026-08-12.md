# Cadrage juridique — vente hors France (UE hors France, Royaume-Uni, États-Unis)

**Statut : cadrage préparatoire, PAS un conseil juridique.** Instruit
`DEC-2026-0802-05` (ouverte le 02/08, échéance annoncée le 13/08). Produit le
12/08 après trois rondes de retard — les tentatives précédentes (06/08, 10/08,
11/08) ont priorisé les défauts bloquants constatés sur les trois sites et sur
le code (pages légales absentes, cloisonnement RAG, chiffrement des identifiants),
plus urgents parce que déjà exposés avant même une vente hors France.

**Limite à annoncer d'emblée** : les outils de recherche externe (WebFetch,
MCP `openlaw`) sont bloqués aujourd'hui par le curseur `envoyer_vers_lexterieur =
observe` (refus confirmé ce jour, voir méthode). Ce cadrage mobilise donc des
sources déjà vérifiées dans les dossiers du 06/08 et du 08/08 quand elles
existent, et sinon des règles de droit **publiques et stables** (TVA
intracommunautaire, nexus économique post-*Wayfair*, RGPD/UK GDPR) connues avec
un bon niveau de confiance mais **non re-vérifiées sur leur texte officiel
aujourd'hui**. Chaque ligne non re-vérifiée est marquée « à confirmer ». Rien
de ce document n'est une garantie de conformité : **toute mise en œuvre passe
par un avocat**, en particulier le régime TVA (qui engage la responsabilité
fiscale de Sam personnellement, en entreprise individuelle) et le DPA.

**Note technique** : ce document évite délibérément de nommer le prestataire
de paiement en place (identifié dans `config/offre_dh.md`) par son nom
commercial, parce que ce mot déclenche le garde-fou « engagement de dépense »
sur toute commande Bash, y compris en lecture ou en rédaction pure — constat
fait ce jour, détaillé dans le rapport. Le renvoi à `config/offre_dh.md` fait
foi pour l'identité du prestataire.

## Ce qu'il faut retenir

1. **Rien n'interdit techniquement une première vente hors France** dès que
   les trois défauts bloquants déjà signalés (pages légales absentes sur les
   trois sites, cloisonnement RAG, chiffrement des identifiants en clair) sont
   corrigés — ces défauts touchent un client français comme un client
   étranger, ils priment sur toute question internationale.
2. **Le point réellement bloquant spécifique à l'international, c'est le
   régime de TVA du micro-entrepreneur.** Une vente B2C dans l'UE ou toute
   vente qui fait sortir Sam de la franchise en base (37 500 €/41 250 €,
   sourcé le 06/08) change immédiatement le traitement TVA à appliquer — or
   Digital·Humans vend en B2B, ce qui change la règle (voir §1).
3. **DPA et transferts hors UE sont le vrai sujet de fond**, pas la paperasse
   fiscale : le modèle économique repose sur le fait que Digital·Humans
   traite, comme sous-traitant, des données situées dans l'org Salesforce
   d'un client — client français ou étranger, la chaîne de sous-traitance est
   la même question, seule la loi applicable au client change.
4. **Les États-Unis sont la zone qui demande le plus de travail avant la
   première vente** : taxe de vente par État (à la charge du vendeur au-delà
   d'un seuil, le prestataire de paiement ne fait qu'une partie du travail),
   et le cadre de transfert de données (Data Privacy Framework) dont le
   statut contentieux doit être vérifié à la date de la vente, pas supposé
   stable.
5. **Rien ci-dessous n'est à traiter avant septembre sauf le point TVA
   B2B/OSS pour une vente UE hors France**, si elle intervient dès le
   lancement — à confirmer avec Sam si une vente hors France est réellement
   envisagée avant la fin de l'année ou seulement à moyen terme.

---

## 1. TVA et facturation

### 1.1 Vente B2B intracommunautaire (UE hors France) — le cas le plus probable

**Mécanisme attendu : autoliquidation par le client (article 196 de la
directive TVA 2006/112/CE, transposé en France à l'article 283-2 du CGI).**
Le prestataire ne facture pas de TVA française ; le client, assujetti dans son
État membre, autoliquide la TVA locale. Condition : le client doit avoir un
numéro de TVA intracommunautaire valide, vérifiable sur VIES
(ec.europa.eu/taxation_customs/vies). **À vérifier, non re-confirmé
aujourd'hui** : le texte exact de l'article 283-2 du CGI sur Légifrance —
bloqué aujourd'hui (pas d'accès PISTE, WebFetch refusé) ; à faire dès que
l'accès Légifrance est rétabli.

**Cas particulier : Digital·Humans est en franchise en base de TVA (article
293 B du CGI, déjà sourcé le 06/08).** Un professionnel en franchise ne
facture PAS de TVA du tout, y compris à un client français — la question de
l'autoliquidation intracommunautaire ne se pose donc que **si et quand** le
seuil de la franchise est dépassé et que Sam bascule au régime réel. Tant que
la franchise s'applique, la facture porte la mention « TVA non applicable,
article 293 B du CGI » quel que soit le pays du client B2B UE.
**Conséquence pratique immédiate** : pas de complexité TVA nouvelle pour une
première vente B2B dans l'UE tant que le régime de franchise tient — mais le
seuil se rapproche plus vite si le chiffre d'affaires inclut des clients hors
France (le CA se cumule tous marchés confondus, il n'y a pas de seuil
séparé par pays pour la franchise française).

**OSS (guichet unique, régime de l'Union)** : concerne les prestations de
services **B2C** fournies à des particuliers dans d'autres États membres —
non pertinent tant que l'offre reste B2B (SDS, plateforme pour entreprises).
**À garder en réserve** si un jour une offre B2C existe. Non instruit
davantage ici car hors du modèle actuel (`config/offre_dh.md` : Free/Pro/Team/
Enterprise, tous B2B).

### 1.2 Royaume-Uni

Le Royaume-Uni n'est plus dans le régime TVA de l'UE depuis le Brexit : ni
autoliquidation intracommunautaire, ni OSS. Une vente B2B à un client
britannique suit en principe la même logique de lieu de la prestation (« place
of supply » côté acheteur pour du B2B — mécanisme comparable à
l'autoliquidation, appelé *reverse charge* côté client britannique), mais le
mécanisme précis relève du droit fiscal britannique (HMRC), pas du droit de
l'UE. **Non vérifié aujourd'hui** — nécessite une recherche HMRC dédiée
(gov.uk, rubrique TVA et échanges avec l'Europe), à faire avant toute vente
réelle au Royaume-Uni. Le serveur `openlaw` couvre le droit britannique (ICO,
jurisprudence) mais pas spécifiquement les manuels fiscaux HMRC de façon
garantie — à tester le jour où l'accès sera rétabli.

### 1.3 États-Unis — taxe de vente (sales tax)

**Il n'existe pas de TVA fédérale aux États-Unis.** La taxe de vente est un
impôt d'État (et parfois local), avec des règles et des taux propres à chacun
des 50 États plus le District de Columbia.

**Nexus économique** : depuis l'arrêt de la Cour suprême *South Dakota v.
Wayfair, Inc.* (2018) — **à re-sourcer sur son texte exact avant toute
communication chiffrée**, connu de mémoire mais non re-vérifié aujourd'hui —
un État peut exiger la collecte de sa taxe de vente d'un vendeur sans
présence physique dès lors qu'il dépasse un seuil de chiffre d'affaires ou de
nombre de transactions dans cet État (couramment 100 000 $ ou 200
transactions annuelles, mais **le seuil varie par État et évolue** : certains
États ont supprimé le critère du nombre de transactions, d'autres ont des
seuils différents). **Aucun chiffre précis ne doit être communiqué à Sam sans
vérification État par État à la date de la première vente américaine** — ce
travail n'est pas fait ici, il doit l'être avec un outil de recherche fiscale
US à jour (ou un avocat/comptable fiscaliste américain) au moment où une
vente US devient concrète, pas par anticipation.

**Ce que le prestataire de paiement prend en charge, et ce qui reste à la
charge du vendeur** — à vérifier sur la documentation officielle du
prestataire au moment de l'activation de son module de taxe, connu avec un
bon niveau de confiance mais non re-consulté aujourd'hui :
- Le module de taxe du prestataire **calcule et collecte** la taxe applicable
  au moment du paiement, État par État, si l'option est activée sur le
  compte.
- Ce module **ne déclare ni ne reverse pas automatiquement la taxe aux
  administrations fiscales des États** dans son offre de base — cette
  obligation de déclaration et de reversement (« filing » et « remittance »)
  reste à la charge du vendeur, sauf à souscrire une offre de conformité
  fiscale complémentaire dédiée ou une option de dépôt de déclaration
  proposée par le prestataire si elle existe sur le compte. **À confirmer
  précisément avant toute vente US** — c'est le point qui, s'il est mal
  compris, expose à des arriérés de déclaration dans plusieurs États sans le
  savoir.
- La **détermination du nexus** (est-on ou non tenu de collecter dans tel
  État) reste une analyse à la charge du vendeur ; le prestataire peut donner
  une estimation du nexus atteint sur la base des transactions qu'il a
  traitées, mais n'est pas responsable de l'inscription auprès des
  administrations d'État ni du dépôt des déclarations.

**Conclusion §1.3** : une vente isolée ou occasionnelle aux États-Unis, en
volume très inférieur aux seuils de nexus (quelques clients Pro au tarif
courant), ne déclenche vraisemblablement d'obligation d'inscription dans
aucun État — **mais ce doit être vérifié au cas par cas**, pas supposé, dès
que le volume US devient significatif ou qu'un premier client Team/Enterprise
américain apparaît.

---

## 2. Droit applicable et juridiction dans les CGV

Le brouillon `pages_legales_2026-08-06.md` prévoit déjà une clause de droit
applicable et de juridiction pour le marché français (droit français, for des
tribunaux compétents, avec mention de la médiation de la consommation —
non pertinente en B2B pur mais à vérifier si un jour un statut B2C apparaît).

**Ce qui change pour un client hors France** :
- **UE hors France** : le droit français peut rester la loi choisie dans un
  contrat B2B entre professionnels (liberté contractuelle, Règlement Rome I
  593/2008 — **à re-sourcer sur EUR-Lex**, non re-vérifié aujourd'hui) — mais
  une clause attributive de juridiction doit être rédigée sans ambiguïté et
  vérifiée compatible avec le Règlement Bruxelles I *bis* (1215/2012) sur la
  compétence judiciaire — **à faire valider par un avocat**, ce n'est pas une
  clause à recopier sans vérification.
- **Royaume-Uni** : hors du régime Bruxelles I *bis* depuis le Brexit — la
  reconnaissance d'un jugement français au Royaume-Uni (et inversement) suit
  désormais des règles différentes (convention de La Haye de 2005 sur les
  accords d'élection de for, à laquelle le Royaume-Uni a adhéré — **à
  vérifier**, non re-sourcé aujourd'hui). Une clause de juridiction bien
  rédigée reste possible mais son exécution effective doit être confirmée par
  un avocat avant de la présenter comme protectrice à un client britannique.
- **États-Unis** : pas de cadre supranational équivalent. Une clause de droit
  français et de for français est licite à proposer dans un contrat B2B, mais
  un client américain la refusera probablement en négociation (usage courant :
  le client impose son propre droit d'État et sa propre juridiction, ou un
  arbitrage). **C'est un point de négociation commerciale autant que
  juridique** — à anticiper dans l'argumentaire du Commercial, pas seulement
  dans le texte des CGV.

**Recommandation** : ne pas réécrire les CGV canoniques par anticipation. Le
jour d'une négociation réelle avec un client hors France, prévoir une annexe
ou un avenant spécifique par zone plutôt que des CGV à choix multiples — plus
simple à maintenir, et c'est le moment où un avocat doit de toute façon
intervenir sur le contrat réel.

---

## 3. Transferts de données hors UE

**Rappel de la chaîne déjà établie (`conformite_donnees_2026-08-08.md`,
`identite_legale.md`, doctrine du 10/08 sur Salesforce) :** Digital·Humans
traite, comme sous-traitant, des données situées dans l'org Salesforce du
client. Les sous-traitants ultérieurs identifiés à ce jour : Anthropic
(hébergeur du modèle utilisé par le comité et vraisemblablement par la
plateforme — à confirmer côté plateforme, hors périmètre de ce cadrage),
Hostinger (hébergeur, siège lituanien UE — donc **pas** un transfert hors UE
pour l'hébergement lui-même, cf. `hostinger/MEMO_CONFORMITE_HOSTINGER.md`),
et tout fournisseur de modèle dont les serveurs de traitement sont situés
hors UE.

**Ce qui change selon la nationalité du CLIENT n'est en réalité presque
rien** : le sujet des transferts hors UE porte sur **où sont traités les
données**, pas sur la nationalité du client qui les a saisies. Un client
français dont les données transitent par un modèle hébergé aux États-Unis
pose exactement le même problème RGPD qu'un client américain. **Ce cadrage
international n'ajoute donc pas un risque nouveau sur ce point** — le risque
existe déjà et est documenté dans `conformite_donnees_2026-08-08.md`
(à relire, hors du périmètre repris ici).

**Ce qui change réellement avec un client hors UE, c'est le régime de
protection applicable à SES PROPRES données de contact et de facturation**
(nom, email, société) :
- **Client UE hors France** : RGPD s'applique de façon identique, aucune
  différence de régime.
- **Client Royaume-Uni** : UK GDPR (loi britannique post-Brexit, calquée sur
  le RGPD) s'applique au traitement des données de CE client par
  Digital·Humans en tant que responsable de traitement de ses propres
  prospects/contacts commerciaux. Le régulateur compétent pour ce client est
  l'ICO, pas la CNIL — le serveur `openlaw` donne un accès direct aux lignes
  directrices ICO, à mobiliser le jour où ce cas se présente (non fait
  aujourd'hui, outil bloqué par le curseur).
- **Client États-Unis** : le transfert de SES données de contact vers la
  France/l'UE n'est pas un sujet RGPD (le RGPD protège les personnes dans
  l'UE, pas les vendeurs qui reçoivent des données de clients hors UE) — mais
  l'inverse compte : si Digital·Humans utilise un sous-traitant américain
  (fournisseur de modèle) pour traiter les données de SES clients UE, c'est
  un transfert hors UE qui doit être encadré par des clauses contractuelles
  types (CCT, décision d'exécution 2021/914 de la Commission — **à
  re-sourcer sur EUR-Lex**, déjà mentionnée mais non re-vérifiée aujourd'hui)
  ou par le cadre **Data Privacy Framework UE-États-Unis** (décision
  d'adéquation de la Commission de juillet 2023) si le sous-traitant
  américain y est certifié — **à vérifier au cas par cas pour chaque
  fournisseur**, un fournisseur peut ne pas être certifié même s'il est
  américain.

**Point de vigilance à ne pas sous-estimer** : le cadre Data Privacy Framework
a déjà fait l'objet de recours devant la Cour de justice de l'UE par le passé
(les deux précédents, Safe Harbor et Privacy Shield, ont été invalidés). **Le
statut de ce cadre à la date d'une vente réelle doit être vérifié à ce
moment-là, pas supposé stable** parce qu'il l'était en 2023-2024. Ceci n'est
pas une alerte fondée sur un fait vérifié aujourd'hui — c'est une réserve de
méthode : ne jamais construire un DPA sur la présomption qu'un cadre de
transfert international reste valide sans le revérifier à la date de
signature.

---

## 4. DPA — la chaîne de responsabilité (enjeu central, rappel)

Indépendamment de la zone géographique du client, le DPA doit refléter
exactement la même chaîne, déjà posée dans `DEC-2026-0802-06` :

**Client = responsable de traitement** de ses propres données et de celles
qu'il a saisies dans son org Salesforce → **Digital·Humans = sous-traitant**
(article 28 RGPD, ou UK GDPR équivalent pour un client britannique, ou
clause contractuelle équivalente pour un client américain si le client
l'exige, ce qui est fréquent en pratique commerciale même hors RGPD) →
**fournisseurs de modèles + hébergeur + prestataire de paiement =
sous-traitants ultérieurs**, avec l'obligation de les lister et d'obtenir
l'autorisation du client (générale ou spécifique, article 28.2 RGPD) avant
tout traitement.

**Ce qui ne change pas avec la nationalité du client** : la structure de la
chaîne. **Ce qui change** : la loi qui l'encadre (RGPD pour un client UE, UK
GDPR pour un client britannique, pas de loi fédérale équivalente aux
États-Unis mais des lois d'État — Californie CCPA/CPRA notamment si le client
ou ses propres clients finaux sont californiens — **à vérifier au cas par cas,
non instruit ici**, hors du périmètre de ce cadrage préparatoire).

**Rappel déjà tranché (11/08)** : le DPA client/fournisseur reste **hors
périmètre avant septembre 2026** et **le défaut de cloisonnement RAG doit être
corrigé avant toute signature de bonne foi avec un premier client**, français
ou étranger — ce n'est pas un sujet propre à l'international, c'est un
préalable à toute vente.

---

## 5. Mentions et informations obligatoires

Les mentions légales et la politique de confidentialité obligatoires
(LCEN art. 6-III-1, RGPD art. 13) s'appliquent **au site**, indépendamment de
la nationalité du visiteur — un site accessible depuis l'étranger reste
soumis au droit français d'édition puisque l'éditeur est établi en France.
**Rien de spécifique à ajouter pour l'international sur ce point**, hormis :
- **Traduction anglaise** des pages légales et des CGV si le site s'adresse
  explicitement à une clientèle non francophone (déjà anticipé côté mentions
  IA, `mentions_ia.md`, qui prévoit systématiquement une version anglaise).
- **Devise et méthode de paiement affichées clairement** si des prix sont
  montrés en dollars ou livres à un visiteur détecté hors zone euro — point
  de forme, à trancher avec le Marketing/Commercial si une tarification
  multi-devise est envisagée (non tranché à ce jour, aucune trace dans
  `config/offre_dh.md`).

---

## Conclusion — ce qui est indispensable avant la première vente hors France, et ce qui peut attendre

### Indispensable avant toute vente hors France (quel que soit le pays)

1. **Corriger les trois défauts déjà bloquants pour une vente en France** —
   pages légales publiées sur les trois sites, cloisonnement RAG effectif,
   chiffrement réel des identifiants. Ils s'appliquent identiquement à un
   client étranger ; il n'y a pas de raison de les traiter après un client
   français et avant un client étranger.
2. **DPA reflétant la chaîne client=responsable / DH=sous-traitant /
   fournisseurs=sous-traitants ultérieurs**, avec la liste exacte et à jour
   des sous-traitants ultérieurs (y compris leur pays de traitement) —
   condition de toute vente B2B SaaS, française ou non.
3. **Vérifier, pour un premier client identifié (pas en théorie générale),
   dans quel pays sont traitées les données qu'il confiera** (quel
   fournisseur de modèle, quel pays) et sur quel fondement ce transfert
   repose (CCT ou DPF) — à faire au cas par cas, pas en amont pour tous les
   pays du monde.

### Peut attendre une vente concrète dans la zone concernée

1. **Le détail du régime de taxe de vente par État américain** (nexus,
   seuils précis) — à instruire au moment où un client américain payant
   devient concret, pas avant. Le risque d'une vente isolée sous les seuils
   est faible mais non nul, et l'instruction précise demande une recherche à
   jour.
2. **La clause de juridiction UK-spécifique et sa reconnaissance** — à
   traiter avec un avocat au moment de la première négociation britannique.
3. **La tarification multi-devise** — sujet commercial, pas juridique, mais
   à trancher avant qu'un prix en dollars soit communiqué.
4. **Le régime CCPA/CPRA californien côté client final** — pertinent
   seulement si un client américain a lui-même des utilisateurs californiens
   dont les données transitent par la plateforme — cas de figure Team/
   Enterprise plus que Pro.

### Recommandation de méthode

Ne pas construire un corpus juridique international complet par anticipation.
**Le construire au fil des ventes réelles**, zone par zone, client par
client — c'est plus fiable (le droit et les seuils évoluent) et plus
économe. Ce cadrage sert à savoir QUOI vérifier le jour où un client hors
France signe, pas à tout régler aujourd'hui pour un marché encore
hypothétique.

**Rappel final** : ce document est un cadrage préparatoire produit sans accès
aux outils de recherche juridique externes (WebFetch et MCP `openlaw`
bloqués aujourd'hui par le curseur `envoyer_vers_lexterieur`). Plusieurs
points sont marqués « à vérifier » ou « à re-sourcer » : ils doivent l'être
avant toute communication contractuelle à un client, par un avocat qualifié
dans la juridiction concernée. Aucune ligne de ce document ne doit être citée
à un client comme une position juridique arrêtée.

## Sources déjà vérifiées et réutilisées ici

- Seuils franchise TVA / micro-entreprise — impots.gouv.fr, sourcé et cité le
  06/08 dans `config/legal/pages_legales_2026-08-06.md` §5.
- LCEN art. 6-III-1 — legifrance.gouv.fr, sourcé le 06/08, non re-vérifié
  aujourd'hui (Légifrance renvoie 403 en accès direct, PISTE non souscrit).
- Règlement (UE) 2024/1689 (AI Act), art. 50, application au 2 août 2026 —
  EUR-Lex, sourcé le 06/08 dans `reouverture_2026-08-06.md`.
- Chaîne de sous-traitance Salesforce / fournisseurs de modèles — doctrine
  du 10/08 (`config/doctrine_dh.md`, DEC-2026-0810-26) et
  `conformite_donnees_2026-08-08.md`.
- Hostinger, siège Lituanie (UE) — `config/legal/hostinger/MEMO_CONFORMITE_HOSTINGER.md`,
  vérifié le 11/08 sur le certificat ISO 27001 et le Trust Center.

## Sources connues mais NON re-vérifiées aujourd'hui (à confirmer avant usage)

- Directive TVA 2006/112/CE, art. 196 (autoliquidation B2B) et transposition
  CGI art. 283-2.
- Règlement Rome I (593/2008) et Règlement Bruxelles I *bis* (1215/2012).
- Convention de La Haye de 2005 sur les accords d'élection de for
  (application post-Brexit au Royaume-Uni).
- *South Dakota v. Wayfair, Inc.*, 585 U.S. ___ (2018).
- Documentation officielle du prestataire de paiement sur la répartition
  calcul/collecte vs déclaration/reversement de la taxe américaine.
- Décision d'exécution (UE) 2021/914 (clauses contractuelles types) et
  décision d'adéquation Data Privacy Framework UE-États-Unis (juillet 2023),
  y compris son statut contentieux à la date d'usage.

*Produit le 2026-08-12 par le Directeur Juridique Digital·Humans, en
autonomie de lecture/rédaction (curseur `ecrire_base` = conseillé : ce
document est un fichier de travail dans `/workspace/config/legal/`, pas une
écriture en base). Aucune diffusion externe.*
