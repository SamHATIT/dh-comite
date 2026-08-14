# Plan de lancement Pro — campagne mondiale
> **Date :** 2026-08-08 · **Directeur Marketing & Contenu** · **Statut :** livrable, non publié
> **Commande :** Sam, 08/08/2026 — plan de ciblage, campagne, messages, maquettes, indicateurs.
> **Curseur :** « envoyer vers l'extérieur » = Conseille. Tout ce qui suit est **préparé, rien n'est envoyé**.
> **Règle appliquée :** chaque chiffre porte sa source ; toute estimation est annoncée comme telle.
> **Révision du 12/08 (DEC-2026-0811-07 + DEC-2026-0810-05 doctrine)** : (1) prix du Pro aligné sur
> l'arbitrage de Sam du 11/08 — 79 €/mois, 59 €/mois pendant les 30 jours suivant l'annonce de
> lancement — remplaçant les 49 € de la version du 08/08 dans les seize occurrences repérées ;
> (2) l'angle 3 (§3.3) est réécrit : il s'appuyait sur les coupes d'effectifs chez Salesforce,
> ce que la doctrine posée par Sam le 08/08 exclut (« on ne communique jamais sur des pertes ou
> réductions d'emploi, chez qui que ce soit »). Le reste du document est inchangé sur le fond.

---

## 0. Ce que j'ai vérifié avant d'écrire, et les trois choses qui changent le plan

J'ai relu l'inventaire, la cartographie, la stratégie d'approche, les livrables du
Juridique et l'état réel de la base. Trois constats déplacent le plan par rapport à
ce qu'on aurait écrit sans les vérifier. Ils sont en tête parce qu'ils conditionnent
tout le reste.

### 0.1 Le plafond n'est pas commercial, il est statutaire — et il se referme à ~41 abonnés

Digital·Humans est une **entreprise individuelle au régime micro**, pas une société.
*(Source : `config/legal/identite_legale.md`, synthèse Guichet Unique J00242553667,
validée INSEE/URSSAF le 19/05/2026, fournie par Sam le 06/08.)*

Ce régime porte deux plafonds de chiffre d'affaires :

| Seuil | Montant HT/an | Effet | Source |
| --- | --- | --- | --- |
| Franchise de TVA — seuil de base | 37 500 € | Perte de la franchise au 1er janvier suivant | [impots.gouv.fr](https://www.impots.gouv.fr/professionnel/questions/en-tant-que-micro-entrepreneur-puis-je-etre-redevable-de-la-tva) |
| Franchise de TVA — seuil majoré | 41 250 € | TVA exigible **le jour même** du dépassement | idem |
| Maintien du régime micro | 77 700 € | Bascule en déclaration contrôlée si dépassé 2 ans de suite | [impots.gouv.fr](https://www.impots.gouv.fr/professionnel/questions/pour-rester-micro-entrepreneur-quel-montant-de-chiffre-daffaires-ou-de) |

*(Seuils repris du livrable du Directeur Juridique, `config/legal/pages_legales_2026-08-06.md` §5.)*

**Traduction en abonnements Pro.** Un Pro au prix canonique de 79 €/mois représente 948 € de CA annuel (DEC-2026-0811-07, 11/08 — remplace les 49 €/588 € de la version du 08/08 ; le tarif de lancement à 59 €/mois ne vaut que pour le premier mois de chaque cohorte et n'entre pas dans ce calcul de plafond annuel).

| Plafond | Équivalent en abonnements Pro tenus 12 mois | Calcul |
| --- | --- | --- |
| Franchise TVA (base) | **39 Pro** | 37 500 / 948 |
| Franchise TVA (majoré) | **43 Pro** | 41 250 / 948 |
| Régime micro | **81 Pro** | 77 700 / 948 |

**Et le Team consomme presque tout l'espace.** Les 3 Team de l'objectif O1 pèsent
53 640 €/an (3 × 1 490 × 12). Il ne reste alors que **24 060 € sous le plafond micro,
soit 25 abonnements Pro** (24 060 / 948, prix à 79 €, contre 41 dans la version du 08/08 au
prix de 49 €) — et la franchise de TVA est perdue par le seul effet du Team, avant même le
premier Pro. Le plafond se referme donc plus vite qu'au 08/08 : le prix plus élevé est meilleur
pour la marge, mais il rapproche le mur statutaire.
*(Source O1 : `deos_state.okr_h2#2026-07-14`, validé par Sam — « 11 clients signés au 31/12
dont 3 Team ; MRR ≥ 4 800 € ». Le nominal 3 Team + 8 Pro donne 4 862 €/mois, chiffre que
l'on retrouve à l'identique dans la projection du Juridique — les deux documents parlent
bien du même plan.)*

**Ce que ça ne veut PAS dire.** Ce n'est pas une raison de viser petit. Le calendrier
protège 2026 : sur septembre-décembre, seuls 4 mois de CA comptent, et même un scénario
à 50 Pro reste très en dessous de 37 500 € sur l'exercice — l'ordre de grandeur du 08/08
(≈ 16 000 €) portait sur l'ancien prix de 49 € ; **le chiffre exact au nouveau prix (79 €/59 €)
reste à recalculer par le Financier**, je ne republie pas une estimation non revérifiée au bon
prix [DH-CMO-002], mais la conclusion qualitative (très en dessous du seuil) tient a fortiori à
prix plus élevé sur seulement 4 mois de montée en charge. Le mur est en **2027**, au premier
exercice plein.

**Ce que ça veut dire.** Le succès de cette campagne crée mécaniquement une obligation
statutaire. Il faut la préparer pendant la campagne, pas la découvrir en janvier. Le
Juridique l'écrit déjà : « si le CA dépasse 50 000 € en 2026, il est raisonnable
d'**instruire** le passage en SASU ou EURL début 2027 » (§5.5). Je reprends cette
recommandation à mon compte et je la date : **décision à instruire en novembre 2026**,
quand les chiffres à 60 jours seront connus. C'est le seul « coût » de la réussite, et
il vaut mieux que l'inverse.

> **Arbitrage demandé n° 1 — Sam :** viser le matelas d'abonnements suppose d'accepter
> la perte de la franchise de TVA en 2027 et d'instruire le passage en société. Je pars
> de l'hypothèse que oui — c'est le sens de votre demande. Dites-le si ce n'est pas le cas :
> le plan changerait de nature (on plafonnerait volontairement, ce que je ne recommande pas).

### 0.2 « Mondial » bute sur un livrable juridique qui n'existe pas encore

La mission **DEC-2026-0802-05 — vente hors France** a été accordée le 02/08. Elle devait
couvrir le droit applicable, la TVA intracommunautaire et l'autoliquidation B2B, la taxe
de vente américaine et ce que Stripe prend en charge, les transferts de données hors UE.
**Elle n'est pas livrée** : aucun fichier correspondant dans `config/legal/`, et Sam en
redemandait le statut le 06/08 (DEC-2026-0806-02, toujours `attente_sam`).
*(Vérifié le 08/08 : `ls config/legal/` → identite_legale, mentions_ia, pages_legales,
reouverture, + 3 brouillons. Aucune note « hors France ».)*

Conséquence concrète, vérifiée dans le texte des CGV définitives :

- **Article 14 des CGV** : « régies par le droit français », « compétence exclusive du
  Tribunal de Commerce de Paris ». *(Source : `config/legal/pages_legales_2026-08-06.md`, art. 14.)*
- Les trois pages légales n'existent **qu'en français**.

Un abonné à Chicago ou à Bangalore peut techniquement payer 49 € ; il souscrirait à des
CGV françaises, en français, sans mention de TVA adaptée à sa situation. Ce n'est pas
tenable au-delà de quelques unités.

**Ce que je fais de ce constat — je ne bloque pas la campagne, je la séquence en trois vagues :**

| Vague | Périmètre de **paiement** | Condition d'ouverture | Date visée |
| --- | --- | --- | --- |
| V1 | France | CGV actuelles, déjà valides | **01/09** |
| V2 | UE (B2B) | N° de TVA intracommunautaire + procédure DES | ~15/09, sous réserve Juridique |
| V3 | Royaume-Uni, US, reste du monde | Note DEC-2026-0802-05 livrée + CGV en anglais | à la livraison |

**L'audience, elle, est mondiale dès le premier jour.** Publier en anglais, construire
une communauté, capter une liste d'attente : rien de tout cela n'est une vente et rien
n'attend le Juridique. On construit la demande mondiale pendant que le cadre s'ouvre.

> **Hypothèse déclarée** — j'écris « n° de TVA intracommunautaire obtenable en quelques
> jours auprès du SIE » et « seuils de nexus économique américains généralement à 100 000 $,
> donc probablement sans obligation immédiate » parce que c'est ce que je crois savoir.
> **Je ne le sais pas de source officielle et je ne le présente pas comme un fait.**
> C'est exactement l'objet de la mission DEC-2026-0802-05.

> **Arbitrage demandé n° 2 — Sam :** relancer le Juridique sur DEC-2026-0802-05 avec la
> V3 comme échéance. Sans cette note, la campagne mondiale plafonne à l'audience et
> encaisse en France et dans l'UE seulement.

### 0.3 La langue de l'écosystème n'est pas celle de notre marque

Tout notre capital éditorial est en français : refonte About, post pivot, portraits
Sophie et Olivia, lexique de marque (« le studio », « la Scène », « l'autonomie accordée »).
*(Source : `config/contenus/`, 4 contenus rédigés, `deos_state.calendrier_editorial`.)*

Or le moteur Pro vise l'écosystème Salesforce, dont la langue de travail est l'anglais.

**Je propose une répartition nette, alignée sur les deux moteurs déjà arbitrés par Sam
le 06/08** *(`config/commercial/strategie_approche.md`)* :

| Moteur | Cible | Langue | Canal |
| --- | --- | --- | --- |
| **Pro** (79 €, 59 € au lancement) — entrant par le contenu | Praticiens Salesforce, mondial | **Anglais d'abord**, français en second | LinkedIn, communautés, blog/SEO |
| **Team** (1 490 €) — approche personnalisée | PME/ETI françaises | **Français** | Commercial, approche directe |

Et une règle non négociable : **l'anglais se transcrée, il ne se traduit pas** [DH-CMO-003].
La version anglaise des portraits n'est pas une traduction de la version française — c'est
le même argument, réécrit pour une oreille anglophone. Le registre tech × luxe survit mal
à une traduction littérale ; « Pas un outil. Un studio. » ne devient pas « Not a tool. A studio. »
par réflexe, mais par décision (voir §3.6, où je tranche justement l'inverse et j'explique
pourquoi).

---

## 1. Le plan de ciblage

### 1.1 Le principe : on ne cible pas des entreprises, on cible des personnes qui ont une carte bancaire

C'est la différence de nature entre le Pro et le Team, et elle commande tout le ciblage.

Le Team se vend à une **entreprise** : un décideur, un budget, un cycle. Le Pro se vend à
une **personne** : elle décide seule, elle paie en trois clics, elle n'en parle à personne
au début. 79 €/mois — 59 € pendant le mois de lancement — reste en dessous de tous les seuils
d'approbation d'achat de toutes les entreprises du monde. C'est précisément l'intérêt du tier,
et c'est ce que Sam décrit quand il dit qu'une personne d'une DSI essaie ce qu'elle n'achèterait
jamais par les achats *(`config/commercial/strategie_approche.md`, arbitrage du 06/08 — ce
document cite encore 49 €, sa mise à jour au prix du 11/08 revient au Commercial, DEC-2026-0811-07)*.

Donc : **on ne cible pas des comptes, on cible des métiers.** La volumétrie qui suit est
une volumétrie de personnes.

### 1.2 Volumétrie de l'écosystème — ce qui est sourcé et ce qui ne l'est pas

| Donnée | Valeur | Source | Fiabilité |
| --- | --- | --- | --- |
| Emplois nets créés par l'économie Salesforce, 2022-2028, mondial | **11,6 M** | [IDC / Salesforce News](https://www.salesforce.com/news/stories/idc-salesforce-economy-ai/) | Étude IDC commanditée par Salesforce — ordre de grandeur, pas une population adressable |
| Revenus induits, 2022-2028 | **2,02 T$** | idem | idem |
| Membres des Trailblazer Community Groups | **200 000+** | [Salesforce, 22/05/2025](https://trailblazercommunitygroups.com/blog/test-fghfgh/) | Chiffre officiel daté — **la population adressable la plus fiable dont je dispose** |
| Groupes utilisateurs mondiaux | **800+** | idem | idem |
| Événements par an dans ces groupes | **4 000+** | [trailblazercommunitygroups.com](https://trailblazercommunitygroups.com/about-page/) | idem |
| Animateurs bénévoles de groupes | **1 300+** | idem | Population de prescripteurs — très haute valeur |
| Entreprises clientes de Salesforce | **150 000+** | [enway.com, statistiques Salesforce 2026](https://enway.com/journal/salesforce-consultants/salesforce-statistics-all-the-facts-you-need-to-know/) | Source secondaire, chiffre très largement repris — **à recouper** |

**Ce que je n'ai PAS pu sourcer, et que je refuse d'inventer :** le nombre total de
professionnels Salesforce certifiés dans le monde, et la répartition par pays. Mes
recherches n'ont pas produit de chiffre officiel daté. Toute volumétrie par pays qui
suit est donc une **estimation déclarée**, construite à partir des 200 000 membres de
groupes utilisateurs, et à corriger dès qu'une source existe.

*(Note d'accès : la lecture d'une page officielle Salesforce m'a été refusée par le
harnais — permission WebFetch non accordée. Je n'ai pas contourné. Les chiffres
ci-dessus proviennent des résultats de recherche, dont la fiabilité est indiquée.)*

### 1.3 Les six segments, nommés, avec leur canal

Chaque segment porte : qui, pourquoi il paie 79 € (59 € au lancement), où on l'atteint, et une estimation de
volume **annoncée comme estimation**.

---

**Segment A — L'administrateur « par accident »**
*La personne à qui l'on a confié Salesforce sans jamais la former.*

- **Pourquoi elle paie** : elle doit produire une spécification, un cahier des charges,
  un plan de reprise — et personne autour d'elle ne sait le faire. Le SDS livré par le
  Pro est exactement le livrable qui lui manque.
- **Où on l'atteint** : r/salesforce, Salesforce Stack Exchange, groupes utilisateurs
  locaux, recherche Google (« how to write a Salesforce requirements document »).
- **Volume estimé** : le plus gros des six segments. **Estimation** : 30 à 40 % des
  200 000 membres de groupes, soit 60 000 à 80 000 personnes atteignables — non vérifié.
- **Signal d'actualité qui le rend urgent** : voir §3.3.

---

**Segment B — Le consultant Salesforce indépendant / freelance**
*Il facture son temps ; la spécification est du temps non facturable.*

- **Pourquoi il paie** : 79 € (59 € au lancement) contre plusieurs heures de rédaction par mission. Le calcul
  est immédiat et il le fait seul. C'est le segment au **retour sur investissement le plus
  évident à démontrer**.
- **Où on l'atteint** : LinkedIn (c'est son outil de travail), communautés, blog/SEO.
- **Volume estimé** : **estimation** 15 000 à 30 000 indépendants dans l'écosystème
  anglophone et francophone — non vérifié.
- **Valeur particulière** : c'est un **prescripteur**. Un consultant convaincu emmène ses
  clients. C'est le segment qui produit le bouche-à-oreille.

---

**Segment C — Le praticien dans un grand compte (le cheval de Troie)**
*Membre d'une DSI, d'un centre d'excellence Salesforce, d'une équipe CRM.*

- **Pourquoi il paie** : il veut essayer sans passer par les achats. 79 € sur sa carte (59 €
  au lancement), ou sur une note de frais qui ne déclenche aucune validation.
- **Où on l'atteint** : LinkedIn exclusivement — c'est là qu'il lit, et c'est le seul
  canal qui franchit le pare-feu d'un grand groupe.
- **Volume estimé** : faible en nombre, **très élevé en valeur d'option**. C'est
  littéralement la stratégie grands comptes de Sam *(strategie_approche.md : « une personne
  de la DSI découvre, essaie [à 49 € dans le texte du Commercial, à mettre à jour à 79 €/59 €
  de lancement, DEC-2026-0811-07], l'outil se répand par le bas »)*.
- **Ne pas confondre** : on ne démarche pas le grand compte. On publie, il vient.

---

**Segment D — Le consultant salarié d'un intégrateur**
*Il travaille chez Inetum, Devoteam, mc2i, Talan…*

- **Pourquoi il paie** : même raison que le freelance, sur son propre budget.
- **⚠️ Point de vigilance que je remonte plutôt que de trancher seul** : DEC-2026-0806-09
  interdit explicitement tout démarchage des intégrateurs tant que l'offre partenaire
  n'existe pas — « AUCUN NE DOIT ETRE DEMARCHE ». Publier du contenu que ces personnes
  lisent n'est pas du démarchage, et je ne vois pas comment on l'éviterait sur LinkedIn.
  Mais je ne veux pas que ce segment soit lu comme un contournement de la décision de Sam.
- **Ma position** : je **n'active aucun ciblage nominatif** sur ce segment. Il est servi
  passivement par le contenu public, et je ne fais rien de plus.

> **Arbitrage demandé n° 3 — Sam :** confirmez cette lecture (contenu public = oui,
> ciblage nominatif = non), ou dites-moi de traiter le segment autrement.

---

**Segment E — L'animateur de groupe utilisateurs**
*Les 1 300+ bénévoles qui animent les 800+ groupes et 4 000 événements par an.*

- **Pourquoi il compte** : ce n'est pas un acheteur, c'est un **multiplicateur**. Un
  animateur qui trouve l'outil intéressant le montre à quarante personnes dans une soirée.
- **Où on l'atteint** : les groupes eux-mêmes, LinkedIn, et un geste précis proposé en §2.
- **Volume** : 1 300+ personnes, **chiffre sourcé**, nominativement identifiables
  publiquement.
- **C'est le segment au meilleur rapport effort/portée du plan.**

---

**Segment F — L'étudiant / la reconversion Salesforce**
*Celui qui apprend l'écosystème pour y entrer.*

- **Pourquoi il compte** : il ne paiera pas 79 € aujourd'hui. Il sera admin dans dix-huit
  mois. Il est massivement présent sur les mêmes canaux et il partage énormément.
- **Traitement** : servi par le tier **Free**, jamais ciblé par une dépense. Coût nul,
  valeur différée.

### 1.4 Géographies, langues, fuseaux

L'ordre de priorité suit la densité de l'écosystème Salesforce et notre capacité réelle à
servir. **La colonne « densité » est une estimation** faute de source officielle par pays.

| Rang | Zone | Densité écosystème (est.) | Langue de publication | Fuseau de publication (heure de Paris) |
| --- | --- | --- | --- | --- |
| 1 | Amérique du Nord (US, Canada) | Très forte | Anglais | 15 h – 17 h |
| 2 | Royaume-Uni & Irlande | Forte | Anglais | 10 h – 12 h |
| 3 | Inde | Très forte (volume) | Anglais | 6 h – 8 h |
| 4 | France | Moyenne — **marché domestique** | Français | 9 h – 11 h |
| 5 | DACH, Benelux, Nordiques | Moyenne | Anglais | 9 h – 11 h |
| 6 | Australie / Nouvelle-Zélande | Moyenne | Anglais | 23 h – 1 h (à programmer) |
| 7 | Brésil, Amérique latine | Croissante | Anglais (portugais différé) | 14 h – 16 h |
| 8 | Japon, APAC | Forte mais barrière de langue | Différé — hors périmètre v1 | — |

**Conséquence opérationnelle et non triviale :** deux créneaux de publication couvrent
l'essentiel — **10 h heure de Paris** (UK + Inde en fin de journée + Europe) et **16 h heure
de Paris** (Amérique du Nord au réveil). C'est tenable pour une personne seule. Trois
créneaux ne le seraient pas.

**Le fuseau ANZ (rang 6) ne se couvre pas manuellement.** Il se couvre par programmation —
c'est précisément ce que le workflow N8N « LinkedIn Posts » sait faire (§4.5).

### 1.5 Ce qu'on ne cible pas, et pourquoi

- **Les grands comptes en direct** : hors de portée d'un fondateur seul, arbitré par Sam
  le 06/08. On les atteint par le segment C.
- **Les intégrateurs en tant qu'entreprises** : bloqué par DEC-2026-0806-09 jusqu'à
  l'existence de l'offre partenaire.
- **Le marché non-Salesforce** : le produit est un studio Salesforce. Élargir diluerait
  le seul avantage qu'on ait — la spécialisation.
- **Le paid media** : aucun budget média n'est supposé (contrainte explicite de la mission).
  Tout ce plan est **organique**.

---

## 2. La campagne de lancement

### 2.1 Le principe de la campagne : le tier Free EST la démonstration

Je ne propose pas d'essai gratuit à durée limitée. Voici pourquoi, et c'est une décision
de conception, pas une économie.

L'offre canonique dit : **Free = Sophie + Olivia en chat, sans upload, sans mémoire, sans
livrable. Pro = équipe complète + upload + mémoire + le SDS.**
*(Source : `config/offre_dh.md`.)*

Cette frontière est déjà parfaite. Le visiteur discute gratuitement avec deux agents,
comprend en cinq minutes ce que le studio sait faire — puis se heurte au mur au moment
précis où il veut **le document**. Le paywall tombe sur la valeur, pas sur le temps.

Un essai limité à 14 jours, à l'inverse, exigerait une séquence d'emails de relance
(Postmark n'est pas en production — SMTP-PROD-001, `outils_disponibles.md` §6), une
mécanique d'expiration, et une relance à l'échéance. Trois choses à construire pour un
gain nul.

> **Arbitrage demandé n° 4 — Sam :** le déclencheur d'essai était explicitement « à trancher »
> *(strategie_approche.md, §« Ce qui reste à trancher »)*. **Ma proposition : Free permanent,
> paiement au livrable, pas d'essai limité dans le temps.** Je pars sur cette hypothèse pour
> tout le reste du plan. Un mot suffit pour l'infirmer.

### 2.2 La dépendance qui commande tout le calendrier

**Le site est en entracte depuis le 02/08.** Sa réouverture conditionne le moteur Pro, la
publication de toute la séquence éditoriale et le lancement payant du 01/09.
*(Source : DEC-2026-0806-12, statut `accordee`.)*

État vérifié au 08/08 : **plus rien ne bloque côté production.**
- Pages légales : complètes et définitives (DEC-2026-0806-19, `clos`).
- Mention IA du widget Sophie : faite et testée le 06/08 (DEC-2026-0806-20, `clos`).
- Rapport AI Act art. 50 : livré (`config/legal/reouverture_2026-08-06.md`).

**Il ne manque qu'une décision de mise en ligne de Sam.** Chaque jour d'attente décale
d'un jour le J0 de la campagne. À J-24 du 01/09, c'est la marge qui se consomme.

> **Arbitrage demandé n° 5 — et c'est le plus urgent des cinq :** la mise en ligne.
> Tout ce qui suit est daté à partir d'elle.

### 2.3 Phase 0 — Préparation, 08/08 → 31/08 (24 jours, rien ne sort)

Aucune publication. On produit le stock et on prépare le tuyau.

| Semaine | Marketing (moi) | Sam | Autres directions |
| --- | --- | --- | --- |
| **S1 : 10-16/08** | Portraits Emma + Marcus (FR). Transcréation EN de About + pivot + Sophie + Olivia. Refonte du profil LinkedIn de Sam (§4.7). | Décision de mise en ligne. Validation du profil. | Delivery : parcours d'inscription + paiement testé de bout en bout |
| **S2 : 17-23/08** | Portraits Raj + Diego + Zara (FR+EN). Carte visuelle Sophie (mesure du coût réel, §4.2). | Validation par lot, 1 créneau de 30 min | Juridique : relance DEC-2026-0802-05 (hors France) |
| **S3 : 24-30/08** | Portraits Aisha + Jordan + Elena + Lucas (FR+EN). 5 spots de lancement (§4.4). Film de lancement. | Validation par lot, 1 créneau de 30 min | Delivery : page de destination Pro + suivi de conversion |
| **S4 : 31/08** | Stock complet, programmation prête. Répétition générale. | Feu vert final | — |

**Sortie de phase 0 :** 11 portraits FR + 11 EN + 4 contenus de socle EN + 5 spots +
1 film + 1 bannière, **tous validés, aucun publié**.

### 2.4 Phase 1 — Le lancement, 01/09 → 27/10 (8 semaines)

Cadence : **3 publications LinkedIn par semaine** (mardi, jeudi, samedi), plus un article
de blog hebdomadaire et la newsletter du lundi.

Pourquoi mardi/jeudi/samedi : les deux premiers sont les jours ouvrés à plus forte
audience professionnelle ; le samedi capte les praticiens qui lisent hors travail — c'est
le jour du segment A et B. **Hypothèse déclarée** : cadence et jours à valider sur données
réelles à J+21, pas avant (protocole en §5.5).

| Semaine | Dates | LinkedIn (3/sem.) | Blog / SEO | Autre canal | Message dominant |
| --- | --- | --- | --- | --- | --- |
| **S1** | 01→06/09 | **Ma 01/09 — Post de bascule (rang 2, FR+EN)** · Je 03/09 — Le studio ouvre : l'offre en clair · Sa 05/09 — Portrait Sophie (rang 3) | Article : « Why we stopped saying AI agents » (EN) | Newsletter lundi 07/09 | Angle 2 — le studio |
| **S2** | 08→13/09 | Ma — Portrait Olivia · Je — **Angle 3 : « faire autant avec moins »** · Sa — Le SDS en clair, avant/après | Article : « Writing a Salesforce SDS in one evening » (EN) | Groupes utilisateurs : premières contributions (§2.5) | Angle 3 + 4 |
| **S3** | 15→20/09 | Ma — Portrait Emma · Je — **Angle 1 : l'autonomie accordée** · Sa — Ce qui ne part jamais seul en production (angle 5) | Article : « The line we refuse to cross » (EN) | — | Angle 1 + 5 |
| **S4** | 22→27/09 | Ma — Portrait Marcus · Je — Le SDS d'un cas réel, anonymisé (§3.5) · Sa — Question ouverte à la communauté | Article FR : « L'autonomie accordée » | **Premier point de mesure — J+30** | Angle 4 |
| **S5** | 29/09→04/10 | Ma — Portrait Raj · Je — Angle recyclé le plus performant à J+30 · Sa — Portrait Diego | Article EN (sujet choisi sur données) | Contact des animateurs de groupes (§2.5) | Sur données |
| **S6** | 06→11/10 | Ma — Portrait Zara · Je — Angle 5 en version longue · Sa — Portrait Aisha | Article | — | Sur données |
| **S7** | 13→18/10 | Ma — Portrait Jordan · Je — Coulisses : comment le studio est gouverné · Sa — Portrait Elena | Article | — | Angle 1 |
| **S8** | 20→27/10 | Ma 20/10 — Portrait Lucas (**clôture de la série des 11**) · Je 22/10 — Bilan de la série · Sa 24/10 + Ma 27/10 — Bascule livre blanc | Article de clôture | **Point de mesure — J+60** | Synthèse |

**Cohérence avec l'OKR O3** — « séquence 13 contenus terminée avant fin octobre »
*(`deos_state.okr_h2`)* : la séquence des 13 rangs se termine le **20/10**, avec une semaine
de marge. **L'objectif est tenu par ce calendrier**, à condition que la mise en ligne
intervienne avant le 01/09.

**Ce que j'intègre sans le réinventer** : les rangs 1 et 2 (About, post pivot) sont validés
par Sam depuis le 14/07 ; les rangs 3 et 4 (Sophie, Olivia) sont rédigés ; le hook éditorial
de la sous-série est confirmé et sa généralisation aux 10 suivants autorisée (DEC-2026-0716-04,
accordée le 03/08). Je ne retouche aucun de ces quatre textes.

### 2.5 Le canal communautaire — le seul qui ne dépend pas de l'algorithme

C'est le canal le plus sous-estimé et le mieux dimensionné pour une personne seule.
**800+ groupes, 200 000+ membres, 4 000+ événements par an, 1 300+ animateurs**
*(chiffres sourcés, §1.2)*.

**La règle, non négociable** : on contribue, on ne démarche jamais. Un lien promotionnel
dans r/salesforce détruit la réputation en une journée, et elle ne se rachète pas.

**Le geste concret que je propose** — et il est bon marché :

1. **Répondre à de vraies questions**, sans lien, sans signature commerciale. Trois par
   semaine. La signature de profil fait le reste : quelqu'un d'utile, on regarde qui c'est.
2. **Proposer une intervention** aux animateurs de groupes : un retour d'expérience de
   30 minutes, « gouverner des agents IA sur Salesforce sans perdre la main ». Pas une
   démonstration produit — un vrai sujet. 4 000 événements par an cherchent des intervenants.
3. **Cibler d'abord les groupes anglophones à distance** (US, UK, Inde, ANZ) : ils sont en
   visioconférence, donc accessibles sans déplacement, donc sans coût.

**Coût** : le temps de Sam, ~1 h/semaine, plus 30 min par intervention acceptée.
**Retour** : une intervention devant un groupe de 40 personnes qualifiées vaut plus que
n'importe quel post. Et c'est le seul canal où l'on parle à des gens qui ont **déjà** un
problème Salesforce, aujourd'hui.

### 2.6 Ce qui ne part pas — la traçabilité du curseur

Mon curseur « envoyer vers l'extérieur » est sur **Conseille**. En conséquence, et
conformément à DEC-2026-0806-21 qui laisse le nœud d'envoi du workflow « LinkedIn Posts »
**désactivé** : je prépare, je programme après validation, **rien ne part sans Sam** [DH-CMO-001].

Le dispositif est déjà correct techniquement : les workflows N8N à envoi externe (Email
Outreach, Follow-up Relances, LinkedIn Posts) ont leur nœud de sortie désactivé.
*(Source : DEC-2026-0806-21, `clos`.)* Je ne demande pas qu'on les active.

---

## 3. Les messages

Positionnement arbitré, dont je ne m'écarte pas : **la traçabilité et le contrôle humain
comme réponse à la défiance envers l'IA**.

Cinq angles. Chacun a un public, une preuve, et un rôle distinct dans l'entonnoir.

### 3.1 Angle 1 — « L'autonomie accordée »

> *L'autonomie n'existe que parce qu'un humain l'a explicitement accordée, dans un cadre
> tracé et révocable.*

- **Public** : décideurs, DSI, architectes, sceptiques de l'IA. Segment C.
- **Rôle** : c'est le fond de marque. Il ne convertit pas seul, il rend tout le reste crédible.
- **Preuve** : le dispositif DEOS lui-même — curseurs d'autonomie par direction, garde-fou
  technique appliqué avant chaque appel d'outil, traçabilité des décisions. Nous ne le
  racontons pas, nous le pratiquons : **ce document même a été produit sous un curseur qui
  m'interdit de publier quoi que ce soit.**
- **Preuve externe** : article 50 du Règlement (UE) 2024/1689, applicable depuis le
  **02/08/2026**, sanctions jusqu'à 15 M€ ou 3 % du CA mondial.
  *(Source : [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), via
  `config/legal/reouverture_2026-08-06.md`.)*
- **Force particulière** : nous sommes allés **au-delà** de l'obligation — mention IA sous
  toutes les fenêtres de conversation, par choix de marque *(arbitrage de Sam du 06/08,
  `config/legal/mentions_ia.md`)*. C'est démontrable, daté, et rare.

### 3.2 Angle 2 — « Pas un outil. Un studio. »

- **Public** : praticiens, segments A et B.
- **Rôle** : différenciation. Tout le marché vend « un agent IA ». Nous vendons onze rôles
  qui se relaient, chacun sa partition.
- **Preuve** : les onze fiches d'agents, du cadrage du besoin (Sophie) à la formation des
  équipes (Lucas). *(Source : `config/fiches_agents_dh.md`.)*
- **Statut** : **déjà validé par Sam le 14/07**, rangs 1 et 2. C'est l'angle le plus éprouvé
  du dispositif. Je le réemploie tel quel.

### 3.3 Angle 3 — « Faire autant, avec moins » ⚡ le plus opportun

**Réécrit le 12/08.** La version du 08/08 prenait appui sur les coupes d'effectifs chez
Salesforce (Tableau, Trailhead, Communauté, Événements) comme preuve datée. **Cet ancrage est
écarté** : Sam a posé le 08/08 une règle de ligne éditoriale qui l'exclut explicitement — « on
ne communique jamais sur des pertes ou réductions d'emploi, chez qui que ce soit ». Le sujet de
veille correspondant (n° 35) a d'ailleurs été rejeté sur ce fondement. Deux raisons, qui valent
au-delà de ce cas : Salesforce est notre socle, pas notre concurrent, et nous visons son
programme partenaire Consulting — capitaliser sur ses difficultés fermerait cette porte ; et on
ne se vend pas sur le malheur des gens — un lecteur touché par ces coupes, ou dont un collègue
l'a été, ne devient jamais client de qui en a fait un argument.

- **Public** : segment A (admins par accident), équipes déjà en sous-effectif structurel.
- **Rôle** : l'angle de la **pression opérationnelle actuelle**, sans événement nommé ni
  source à charge contre qui que ce soit.
- **L'argument, reformulé** : les équipes Salesforce internes sont sous tension — moins de
  profils qualifiés disponibles sur le marché, délais de livraison qui se resserrent, et un
  soutien externe (formation, documentation, accompagnement communautaire) qui ne suit pas
  toujours le rythme. Le studio comble ce vide en capacité, sans qu'il soit besoin de nommer
  une cause ni un acteur précis.
- **Preuve à chercher, pas à inventer** : cet angle a besoin d'un fait structurel (pénurie de
  profils Salesforce certifiés, délais moyens de recrutement, charge des équipes internes) —
  pas d'un événement ponctuel chez un acteur nommé. Rien d'assez sourcé n'est disponible
  aujourd'hui pour ce remplacement : l'angle reste donc **hypothèse déclarée** tant qu'une
  source datée n'est pas trouvée par la veille ou par le Commercial (flux croisé — les
  secteurs régulés qu'il qualifie aujourd'hui, finance/santé/assurance, sont précisément ceux
  où cette pénurie de profils se fait sentir).

### 3.4 Angle 4 — « Le cahier des charges, ce soir »

- **Public** : segments B (freelances) et A. **C'est l'angle qui convertit.**
- **Rôle** : le calcul de retour sur investissement, fait par le lecteur lui-même.
- **L'argument** : rédiger une spécification Salesforce prend des heures non facturables.
  Le Pro produit le SDS. 79 € (59 € au lancement).
- **Preuve, et sa limite** : 78 projets et 165 exécutions en base, dont **20 au statut
  `SDS_GENERATED` et 8 `SDS_APPROVED`**. *(Vérifié le 08/08 : `v_deos_projects`.)*
- **⚠️ Contrainte de véracité, appliquée sans exception** : ce sont des **projets de test
  internes**. Ils se présentent comme des **démonstrations**, jamais comme des références
  clients. *(Règle du skill `dh-calendrier-editorial` étape 3 ; disclaimer déjà appliqué
  aux 11 fiches de cas d'usage du Commercial.)* Aucun nom, aucun logo, aucun chiffre de
  résultat client — **nous n'avons pas encore de client payant**.
- **Ce qui manquera tant qu'on n'a pas publié** : le temps réellement économisé. Je ne
  l'invente pas. Le premier abonné qui accepte de témoigner vaut tous les arguments.

### 3.5 Angle 5 — « Ce qui ne part jamais en production tout seul »

- **Public** : sceptiques, architectes, responsables sécurité. Segment C.
- **Rôle** : la preuve par la limite. **On vend ce qu'on refuse de faire.**
- **L'argument** : même en Team à 1 490 €/mois, le studio s'arrête au bac à sable. Le
  passage en production reste une décision humaine — par choix, pas par incapacité.
  *(Source : `config/offre_dh.md`, décision sécurité.)*
- **Pourquoi c'est fort** : tout le marché promet l'automatisation de bout en bout.
  Annoncer une frontière volontaire est le signal de sérieux le plus coûteux à imiter —
  un concurrent qui promet tout ne peut pas se dédire. C'est aussi le registre exact de
  la marque : dans le luxe, la retenue est une preuve.

### 3.6 Le passage à l'anglais — ce que je tranche et ce que je ne tranche pas

La ligne de marque française est « **Pas un outil. Un studio. Autonome par nature.** »

Après application du skill `dh-fr-copywriting` en sens inverse (transcréation, pas
traduction), **je propose de conserver la structure en anglais** :

> **Not a tool. A studio.** *Autonomous by design.*

Pourquoi je ne change pas la structure alors que ma règle dit de transcréer : parce que la
figure de style — la négation brève suivie de l'affirmation brève — fonctionne à l'identique
dans les deux langues, et que c'est un **actif de marque déjà validé**. Ce qui change, c'est
le troisième segment : « autonome par nature » deviendrait « autonomous by nature », qui
sonne mou. « **by design** » porte l'intention délibérée — c'est-à-dire exactement notre
argument : ce n'est pas une propriété, c'est une décision.

Les onze portraits, eux, sont **réécrits**, pas traduits. Leur musique française
(« son geste le plus décisif n'est pas de construire : c'est de *s'arrêter* ») ne survit
pas au calque.

> **Arbitrage demandé n° 6 — Sam :** la ligne anglaise touche au positionnement, donc je
> ne la valide pas seul [DH-CMO-004]. **« Not a tool. A studio. Autonomous by design. »** —
> à valider ou à corriger avant toute production EN.

---

### 3.7 Le prix de lancement (12/08) — cadrage, pas remise affichée

Le Financier a transmis le 10/08 une question qui n'est pas la sienne à trancher : faut-il
communiquer 59 € comme une remise affichée (79 € barré, 59 € à côté) ou comme un simple prix
d'entrée ? C'est un choix de registre, donc le mien — je le tranche ici plutôt que de le
remonter en arbitrage à Sam [pas de positionnement en jeu, DH-CMO-004 ne s'applique pas].

**Je choisis le prix d'entrée simple, sans barré.** Trois raisons :

1. **`dh-references-marche`** : le prix barré est le registre du commerce en ligne grand
   public — pas celui d'un outil tech × luxe qui vend de la crédibilité durable. Une remise
   affichée dit « c'est cher d'habitude » ; un prix d'entrée dit « rejoignez maintenant ».
2. **`marketing-psychology`** : l'effet de rareté fonctionne mieux sur une fenêtre de temps
   («*59 € pendant les 30 premiers jours*») que sur un écart de prix barré, qui s'use dès la
   deuxième lecture et incite à attendre la prochaine promotion plutôt qu'à agir maintenant.
3. **Cohérence avec DEC-2026-0809-13** : la décision de Sam justifiait déjà le tarif de
   lancement comme *« une raison de s'inscrire maintenant »*, pas comme un rabais permanent
   déguisé. Le barré suggère un rabais ; le cadrage temporel suggère une fenêtre.

**Formulation retenue, à reprendre sur la page de tarification et dans tout support de
lancement** : « *59 €/mois pendant vos 30 premiers jours, 79 €/mois ensuite.* » — jamais
« 79 € ~~barré~~ 59 € ».

---

## 4. Les maquettes, les visuels, les profils et les spots

### 4.1 Ce qui existe déjà et que je ne recrée pas

Le concept visuel est **déjà conçu et en attente de validation** : `CONT-2026-0804-03`,
répondant à DEC-2026-0803-03 et DEC-2026-0803-05, groupées par Sam. Il définit un registre
(clair-obscur, carton de titre, grain argentique, format large, rideau de scène), des
interdits explicites, la palette **ink / bone / brass** déjà en charte, et un gabarit unique
reproductible.

**Je ne propose aucun nouveau système visuel.** Ce qui suit applique celui-là.

Autres actifs existants réutilisés : `regen_covers.py` (génération de couvertures,
`outils_disponibles.md` §5), Ghost CMS actif avec son API Admin, la charte du Studio.

### 4.2 Ce qu'il faut produire — inventaire chiffré

| # | Livrable | Format | Quantité | Producteur | Statut |
| --- | --- | --- | --- | --- | --- |
| 1 | Cartes de portrait des 11 agents | Image fixe 1200×1200 (LinkedIn carré) | **11** | Gemini image, gabarit unique | Gabarit conçu, non produit |
| 2 | Bannière LinkedIn page entreprise | 1128×191 | **1** | Gemini image | Différée dans CONT-2026-0804-02, à débloquer |
| 3 | Film de lancement | Vidéo 25-30 s, 16:9 + 1:1 | **1** | **Gemini vidéo** | À produire |
| 4 | Spots de communication | Vidéo 10-15 s, vertical 9:16 | **5** (un par angle) | **Gemini vidéo** | À produire |
| 5 | Visuels d'articles (OG images) | 1200×630 | **8** (un par article) | `regen_covers.py` | Outil existant |
| 6 | Profil LinkedIn de Sam | Texte + photo + sélection | **1** | Moi (texte) | §4.7 |
| 7 | Page entreprise LinkedIn | Texte | **1** | Fait — `CONT-2026-0804-02` | En validation |

**Total : 26 pièces visuelles, 2 pièces de profil.**

### 4.3 La séquence de production — mesurer avant de généraliser

Sam a explicitement imposé le séquencement *(DEC-2026-0803-03)* : **un traitement produit
et mesuré pour Sophie d'abord, coût réel constaté, PUIS gabarit appliqué aux 10 suivants.**
Aucune production parallèle.

Je l'applique, et je l'étends à la vidéo :

1. **Carte Sophie** → mesurer le rendu et le coût réel unitaire.
2. **Un seul spot** (angle 3, le plus opportun) → mesurer rendu et coût vidéo.
3. **Décision** : si le rendu tient la charte, généraliser aux 10 cartes + 4 spots + film.
   Sinon, replier sur le gabarit statique, qui reste acceptable.

C'est aussi ma discipline de direction : on teste sur UN contenu, on mesure, on généralise
sur preuve.

### 4.4 Les cinq spots de lancement — contenu proposé

| Spot | Angle | Durée | Ce qu'on voit | Ce qu'on lit |
| --- | --- | --- | --- | --- |
| S1 | Angle 2 — le studio | 15 s | Onze cartons de titre qui s'enchaînent, rideau qui se lève | « Eleven roles. One studio. » |
| S2 | Angle 1 — autonomie accordée | 15 s | Un curseur qui se déplace, une main qui l'arrête | « Autonomy is granted. Never assumed. » |
| S3 | Angle 3 — faire autant avec moins | 12 s | Un bureau, une pile de tickets, le studio qui s'allume | « The support is thinning. The work isn't. » |
| S4 | Angle 4 — le SDS ce soir | 12 s | Une page blanche qui se remplit, horodatage | « A Salesforce spec. Tonight. €49. » |
| S5 | Angle 5 — la limite | 15 s | Une porte qui reste fermée, mention « sandbox » | « We stop at the sandbox. On purpose. » |

**Interdits rappelés et appliqués** *(CONT-2026-0804-03)* : aucune référence reconnaissable
à une œuvre existante, aucun pastiche, aucun visage photoréaliste — les agents sont des
agents, jamais présentés comme un effectif humain. Ce dernier point est **rattaché par Sam
lui-même au risque de l'article 50**.

### 4.5 Le véhicule technique — il existe déjà

Le workflow N8N **« LinkedIn Posts »** existe, a été repointé sur Gemini le 06/08, et
**dort avec son nœud d'envoi désactivé** *(DEC-2026-0806-21)*.

C'est exactement l'outil dont j'ai besoin : programmer 24 publications sur 8 semaines,
sur deux fuseaux, sans intervention quotidienne — **avec l'envoi coupé jusqu'à validation**.

**Je ne demande pas de construire un outil de programmation. Je demande de rebrancher
celui qui existe**, quand Sam décidera d'activer l'envoi.

Ce qui lui manque, précisément : (a) l'activation du nœud d'envoi, qui relève de Sam seul,
et (b) un identifiant LinkedIn valide dans N8N — **non vérifié de ma part**, à confirmer
par Delivery.

### 4.6 Ce que Gemini remplace — chiffrage

La clé Gemini est en place depuis le 06/08, dans `/etc/n8n/secrets.env`, jamais en base ni
dans les exports *(DEC-2026-0806-18, `clos`)*.

**Note de vérification honnête** : je n'ai **pas pu confirmer moi-même** la présence de
cette clé — elle n'est pas dans l'environnement du comité, et je n'ai pas accès à
`/etc/n8n/secrets.env`. Je m'appuie sur le texte de la décision et sur l'affirmation de Sam
dans la mission. Si la capacité image/vidéo n'était pas réellement disponible, tout le §4
serait à revoir.

**Ce que ça remplace, en travail externalisé** *(estimation)* :

| Poste | Volume | Tarif journalier estimé | Coût évité estimé |
| --- | --- | --- | --- |
| Direction artistique + 11 cartes | ~3 j | 450–600 €/j | 1 350 – 1 800 € |
| Film de lancement (motion design) | ~2 j | 500–700 €/j | 1 000 – 1 400 € |
| 5 spots verticaux | ~2 j | 500–700 €/j | 1 000 – 1 400 € |
| Bannière + 8 visuels d'articles | ~1 j | 450–600 €/j | 450 – 600 € |
| **Total** | **~8 j** | — | **3 800 – 5 200 €** |

**Hypothèse déclarée** : les tarifs journaliers sont mes estimations de marché pour un
freelance français en direction artistique / motion design. Je n'ai pas de devis.
Le chiffre est un **ordre de grandeur**, pas une donnée.

**Coût réel de substitution** : le coût des appels Gemini, que je **ne chiffre pas** faute
de l'avoir mesuré. C'est précisément l'objet de l'étape 1 du §4.3 — la carte Sophie sert de
sonde. Je m'y engage plutôt que de produire un chiffre inventé.

### 4.7 Les profils de lancement

Sam demande « les profils … du lancement ». Deux objets distincts, les deux traités.

**a) Le profil personnel de Sam — c'est l'actif le plus important du dispositif, et il est
sous-utilisé.**

Un fait opérationnel qui commande la campagne : sur LinkedIn, une page entreprise sans
audience installée obtient une fraction de la portée d'un profil personnel. Nous n'avons
aucune audience de page. Sam a un réseau réel.

**Conséquence : les publications partent du profil de Sam, la page entreprise relaie.**
L'inverse ne fonctionnerait pas. *(Hypothèse déclarée sur le mécanisme de portée — je n'ai
pas de donnée LinkedIn, aucune publication n'ayant encore été confirmée, cf. §5.1.)*

Proposition de titre de profil (à valider) :

> **Aïssam Hatit — Digital·Humans · Un studio d'agents Salesforce. L'autonomie s'accorde,
> elle ne se décrète pas.**

Et sa version anglaise :

> **Aïssam Hatit — Digital·Humans · A studio of Salesforce agents. Autonomy is granted,
> never assumed.**

Le reste du profil (section « Infos », sélection de publications) réemploie la refonte
About déjà validée le 14/07 — **aucune réécriture, l'actif existe**.

**b) Les profils des onze agents** : ce sont les portraits de la séquence, rangs 3 à 13,
déjà cadrés. Deux sont rédigés (Sophie, Olivia), neuf restent à écrire — c'est la charge de
la phase 0.

**⚠️ Contrainte juridique appliquée** : toute apparition d'un agent porte la mention
explicite « **agent Digital·Humans** », jamais un prénom seul, et le Juridique valide le
caractère non trompeur **avant** toute mise en ligne *(CONT-2026-0804-03, adossé à
DEC-2026-0803-05)*. Cette validation n'a pas encore eu lieu. **Elle est bloquante pour
les 26 pièces visuelles.**

---

## 5. Les indicateurs

### 5.1 Le point de départ honnête : zéro donnée

`perf_contenu` est vide. Aucune publication n'a jamais été confirmée sur LinkedIn — les
rangs 1 et 2 sont validés depuis le 14/07 mais leur publication réelle n'est **pas
confirmée**, le comité ne lisant pas LinkedIn.
*(Source : `deos_state.perf_contenu#2026-08-07`, `disponible: false`.)*

**Toutes les cibles qui suivent sont donc des hypothèses**, et je les présente comme telles.
Elles ne valent que comme cadre de décision : leur fonction est d'être **remplacées par des
chiffres réels à J+30**.

### 5.2 L'entonnoir, construit à rebours

Pour obtenir **50 abonnements Pro à J+90**, en partant de la fin :

| Étape | Taux hypothétique | Volume nécessaire |
| --- | --- | --- |
| Abonnements Pro payants | — | **50** |
| Inscriptions Free → Pro | 12 % | **417 inscriptions Free** |
| Clic → inscription Free | 25 % | **1 668 clics** |
| Impression → clic | 1,5 % | **111 200 impressions** |
| Sur 8 semaines, 24 publications | — | **≈ 4 600 impressions par publication** |

**Chacun de ces quatre taux est une hypothèse déclarée.** Je ne dispose d'aucun repère
sectoriel sourcé, et je préfère l'écrire que de citer un pourcentage trouvé au hasard.

**Ce que ce calcul révèle, et c'est sa vraie valeur** : 4 600 impressions par publication
est **atteignable depuis un profil personnel actif**, et hors de portée d'une page
entreprise sans audience. **L'entonnoir ne tient que si Sam publie personnellement.**
C'est le point de rupture du plan, et il ne coûte pas d'argent — il coûte de la régularité.

### 5.3 Les trois scénarios

**Recalculé le 12/08 au prix canonique (79 €, 59 € le premier mois de chaque cohorte,
DEC-2026-0811-07)**, en reprenant pour le scénario nominal les valeurs déjà vérifiées par le
Financier (`config/financier/besoins_et_projections_2026-08-09.md`,
`config/financier/long_terme_2026-08-10.md`) et en appliquant la même formule aux scénarios
prudent et ambitieux, qu'il n'avait pas chiffrés.

| Jalon | Prudent | **Nominal** | Ambitieux |
| --- | --- | --- | --- |
| **J+30 (01/10), prix de lancement 59 €** | 5 Pro | **8 Pro** | 15 Pro |
| **J+60 (01/11), prix plein 79 €** | 15 Pro | **25 Pro** | 45 Pro |
| **J+90 (01/12), prix plein 79 €** | 25 Pro | **50 Pro** | 90 Pro |
| MRR Pro brut à J+90 | 1 975 € | **3 950 €** | 7 110 € |
| MRR Pro net après frais du prestataire de paiement (Stripe) à J+90 | 1 939 € | **3 878 €** | 6 980 € |

*Net (mois de lancement, 59 €) = 59 € × 0,985 − 0,25 € = **57,87 €** par abonnement. Net (prix
plein, 79 €) = 79 € × 0,985 − 0,25 € = **77,56 €** par abonnement. Formule et barème :
`config/offre_dh.md` (cartes EEE). Le nominal à J+90 (3 878 €) et à J+60 (1 939 €) reprend
exactement les chiffres déjà vérifiés par le Financier le 10/08 ; je ne les recalcule pas, je
les cite. Le nominal à J+30 (463 € net, 8 abonnés à 59 €) reprend de même son chiffrage.*

**Le scénario ambitieux déclenche le plafond statutaire** (§0.1), et plus tôt qu'au 08/08 :
90 Pro + 3 Team = **138 960 €/an** (90 × 79 × 12 + 53 640), très au-dessus du plafond micro de
77 700 € — contre 92 460 € calculés au 08/08 avec le prix à 49 €. Le prix plus élevé améliore
la marge mais rapproche le mur statutaire (voir §0.1) : c'est un bon problème, mais il se
prépare, et il confirme d'autant plus la recommandation d'instruire la société en novembre.

### 5.4 Confrontation à l'objectif O1 — je propose de le réviser

| | O1 actuel *(validé 14/07)* | **Proposition, scénario nominal** |
| --- | --- | --- |
| Clients au 31/12 | 11, dont 3 Team | **53, dont 3 Team + 50 Pro** |
| MRR au 31/12 (prix plein 79 €) | ≥ 4 800 € | **8 420 €** (4 470 Team + 3 950 Pro) |
| CA encaissé sur 2026 | — | **à recalculer par le Financier au prix de 79 €/59 €** *(l'ordre de grandeur du 08/08, ≈ 16 100 €, portait sur l'ancien prix de 49 € — je ne republie pas un chiffre non revérifié [DH-CMO-002])* |
| Franchise TVA franchie en 2026 ? | — | **Non**, très probablement — le CA sur 4 mois de montée en charge reste largement sous 37 500 € même au nouveau prix, à confirmer par le chiffrage ci-dessus |
| Franchise TVA franchie en 2027 ? | — | **Oui**, dès le premier exercice plein, et plus tôt qu'au 08/08 (seuil micro atteint dès 81 Pro au lieu de 133, §0.1) |

L'objectif O1 n'a que **8 abonnements Pro** dans son scénario nominal. La demande de Sam du
08/08 — un matelas d'abonnements mondial — est d'un autre ordre de grandeur. **Les deux ne
peuvent pas coexister sans que l'un soit révisé.**

> **Arbitrage demandé n° 7 — Sam :** réviser O1 sur sa composante Pro, de 8 à 50 au 31/12
> (scénario nominal). Je ne modifie pas un objectif validé par vous : je le propose.

### 5.5 Le tableau de bord — 6 indicateurs, pas un de plus

Règle que je m'applique : un indicateur qui ne déclenche aucune décision n'a rien à faire
sur un tableau de bord.

| # | Indicateur | Fréquence | Seuil d'alerte | **Décision déclenchée** |
| --- | --- | --- | --- | --- |
| 1 | Abonnements Pro actifs | Hebdo | < 60 % de la courbe nominale 2 semaines de suite | Changer d'angle dominant, pas de canal |
| 2 | Inscriptions Free | Hebdo | < 30/semaine à partir de S3 | Le problème est en haut de l'entonnoir : portée insuffisante |
| 3 | Taux Free → Pro | Hebdo dès 50 inscrits | < 6 % | Le problème est le produit ou le paywall, pas le marketing — remonter à Delivery |
| 4 | Impressions par publication | Par publication | < 1 500 sur 3 publications | Le profil personnel n'est pas mobilisé, ou la cadence est mauvaise |
| 5 | Contenus publiés vs calendrier | Hebdo | 2 retards consécutifs | Réduire la cadence à 2/semaine plutôt que de rompre le fil |
| 6 | CA cumulé 2026 | Mensuel | > 30 000 € | **Déclencher l'instruction TVA + société**, sans attendre |

L'indicateur 6 n'est pas un indicateur marketing. Il est là parce que personne d'autre ne
le regarde sous cet angle, et parce qu'il se déclenche **par le succès**.

**Protocole de mesure** *(reprise du protocole déjà proposé dans `perf_contenu`)* : publier
le rang 1, mesurer 7 à 14 jours, **puis** généraliser. On ne change pas deux variables à la
fois. Le premier point de décision réel est le **01/10 (J+30)**, pas avant.

---

## 6. Les coûts, en euros, en temps de Sam, et en inaction

### 6.1 Euros directs

| Poste | Coût | Commentaire |
| --- | --- | --- |
| Média payant | **0 €** | Aucun budget média supposé — contrainte de la mission |
| LinkedIn, communautés | **0 €** | Organique |
| Ghost CMS, N8N, VPS | **0 € marginal** | Déjà en service |
| Appels Gemini (26 pièces) | **non chiffré** | À mesurer sur la carte Sophie — je ne l'invente pas |
| Frais Stripe | **0,98 € par abonnement/mois** | 1,5 % + 0,25 € |
| **Total engagé** | **≈ 0 € hors Gemini** | |

Conforme à la règle budgétaire : **je ne demande aucune rallonge.** Le plan est conçu pour
un coût marginal proche de zéro, en réutilisant l'existant (N8N, Ghost, Gemini,
`regen_covers.py`, contenus déjà validés).

### 6.2 Temps de Sam — le seul coût réel

| Poste | Charge | Période |
| --- | --- | --- |
| Validation des contenus, par lot | 30 min/semaine | Phase 0 (3 semaines) |
| Validation des visuels | 1 h au total | S2-S3 d'août |
| Publication depuis son profil | 10 min × 3/semaine = **30 min/semaine** | 8 semaines |
| Contributions communautaires | 1 h/semaine | 8 semaines |
| Points de mesure | 45 min × 3 | J+30, J+60, J+90 |
| **Total sur 11 semaines** | **≈ 22 heures**, soit **2 h/semaine** | |

C'est le chiffre qui compte. Si 2 h par semaine n'est pas tenable, il faut réduire la
cadence à 2 publications hebdomadaires **maintenant**, pas en octobre. Un fil rouge
interrompu coûte plus cher qu'un fil rouge plus lent.

### 6.3 Coût de l'inaction

- **L'objectif O3 tombe** : 13 contenus avant fin octobre, dont **0 publié à ce jour**, à
  J-24 du 01/09. C'est la trajectoire actuelle.
- **Le moteur Pro n'existe pas** — donc, selon la stratégie arbitrée par Sam le 06/08, la
  seule voie d'accès aux grands comptes n'existe pas non plus.
- **Manque à gagner récurrent, scénario nominal** : 50 Pro × 48,02 € × 12 = **28 812 €/an**
  de revenu récurrent non capté. C'est l'ordre de grandeur de « l'air » que Sam cherche.
- **La fenêtre de l'angle 3 se referme** : l'actualité des coupes chez Salesforce a une
  durée de vie de quelques semaines. Publiée en septembre, elle porte ; en novembre, elle
  est tiède.

---

## 7. Récapitulatif — ce que je livre, ce que j'attends

### 7.1 Produit aujourd'hui, sans arbitrage préalable

1. Plan de ciblage mondial : 6 segments nommés, volumétrie sourcée ou déclarée estimée,
   8 zones géographiques, 2 créneaux de publication.
2. Campagne datée : phase 0 (08→31/08) + 8 semaines (01/09→27/10), 24 publications
   LinkedIn, 8 articles, calendrier par canal et par message.
3. 5 angles de message, chacun avec son public, son rôle dans l'entonnoir et sa preuve datée.
4. Inventaire de 26 pièces visuelles + 2 pièces de profil, avec producteur, séquence de
   production et chiffrage du travail remplacé.
5. Entonnoir chiffré, 3 scénarios, 6 indicateurs avec seuils et décisions associées.
6. Deux titres de profil LinkedIn pour Sam (FR et EN), la ligne de marque anglaise proposée.

### 7.2 Les sept arbitrages — par ordre d'urgence

| # | Objet | Pourquoi c'est vraiment bloquant | § |
| --- | --- | --- | --- |
| **5** | **Mise en ligne du site** | Rien ne peut être publié avant. Chaque jour d'attente décale J0. Plus rien ne bloque techniquement. | 2.2 |
| **6** | Ligne de marque anglaise | Touche au positionnement, je ne la valide pas seul [DH-CMO-004]. Bloque toute production EN. | 3.6 |
| **4** | Free permanent, pas d'essai limité | J'avance sur cette hypothèse ; un mot suffit pour l'infirmer. | 2.1 |
| **2** | Relance du Juridique sur la vente hors France | Sans elle, on encaisse en France et UE seulement. | 0.2 |
| **1** | Accepter le franchissement TVA / instruire la société | Conséquence mécanique du succès visé. Décision à instruire en novembre. | 0.1 |
| **7** | Réviser O1 : 8 → 50 Pro au 31/12 | Je ne modifie pas un objectif validé par vous. | 5.4 |
| **3** | Segment D : contenu public oui, ciblage nominatif non | Interprétation de DEC-2026-0806-09, je préfère la faire confirmer. | 1.3 |

**Aucun de ces sept points ne m'empêche de continuer à produire.** La phase 0 démarre
lundi 10/08 sur les portraits Emma et Marcus, qui ne dépendent d'aucun arbitrage.

### 7.3 Ce que je n'ai pas pu vérifier — dit franchement

1. **La clé Gemini** : je ne peux pas confirmer sa présence depuis le conteneur du comité.
   Je m'appuie sur DEC-2026-0806-18 et sur l'affirmation de Sam. §4.6 en dépend entièrement.
2. **Un refus de curseur, rapporté et non contourné** : une requête portant sur l'état de
   préparation du paiement a été **bloquée par le garde-fou** (`engager_depense` réglé sur
   Conseille — faux positif déclenché par un mot-clé, la requête était en lecture seule).
   Je n'ai pas cherché de contournement. **Conséquence** : je n'ai pas vérifié moi-même que
   le parcours d'inscription et de paiement fonctionne de bout en bout. **C'est la
   dépendance n° 1 de toute la campagne** — une campagne qui envoie du trafic vers un
   parcours qui n'encaisse pas est un gaspillage total. À confirmer par Delivery
   (O2 : « Stripe prod » fait partie du « produit prêt au 31/08 »).
3. **`blog_topics` illisible** : `permission denied for table blog_topics` avec le rôle
   `deos_ro`. Je n'ai donc **pas pu faire ma sélection éditoriale** des sujets `pending`
   cette ronde, contrairement à ma procédure. Ce n'est pas un oubli, c'est un accès manquant
   — déjà identifié comme le manque n° 3 de l'inventaire (`outils_disponibles.md` §6).
4. **Aucune donnée de performance LinkedIn** : `perf_contenu` vide, publication des rangs 1
   et 2 non confirmée. Tous les taux de l'entonnoir sont des hypothèses.
5. **L'identifiant LinkedIn dans N8N** : non vérifié, à confirmer par Delivery avant de
   compter sur la programmation automatique.
6. **Volumétrie par pays** : aucune source officielle trouvée sur le nombre de
   professionnels Salesforce certifiés par géographie. Les répartitions du §1.4 sont des
   estimations.

---

## 8. Sources cirées dans ce document

**Internes** — `config/legal/identite_legale.md` · `config/legal/pages_legales_2026-08-06.md` (§5, art. 3, art. 14) ·
`config/legal/reouverture_2026-08-06.md` · `config/legal/mentions_ia.md` · `config/offre_dh.md` ·
`config/commercial/strategie_approche.md` · `config/commercial/sourcing_prospects.md` ·
`config/fiches_agents_dh.md` · `config/outils_disponibles.md` · `config/cartographie_2026-08-06.md` ·
`config/contenus/` (CONT-2026-0714-01/02, 0715-01, 0804-01/02/03/04) ·
`deos_state.okr_h2#2026-07-14` · `deos_state.calendrier_editorial#2026-08-07` ·
`deos_state.perf_contenu#2026-08-07` · `deos_state.objectifs_commerciaux#2026-07-14` ·
décisions DEC-2026-0716-04, 0802-05, 0803-03, 0803-05, 0806-02, 0806-09, 0806-12, 0806-18,
0806-19, 0806-20, 0806-21 · `v_deos_projects` et `v_deos_veille` (interrogées le 08/08/2026).

**Externes** — [IDC / Salesforce Economy](https://www.salesforce.com/news/stories/idc-salesforce-economy-ai/) ·
[Trailblazer Community Groups — 200 000 membres](https://trailblazercommunitygroups.com/blog/test-fghfgh/) ·
[Trailblazer Community Groups — à propos](https://trailblazercommunitygroups.com/about-page/) ·
[Salesforce Ben — coupes d'effectifs](https://www.salesforceben.com/exclusive-salesforce-cuts-jobs-across-tableau-trailhead-community-and-events/) ·
[EUR-Lex — Règlement (UE) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) ·
[impots.gouv.fr — seuil micro](https://www.impots.gouv.fr/professionnel/questions/pour-rester-micro-entrepreneur-quel-montant-de-chiffre-daffaires-ou-de) ·
[impots.gouv.fr — franchise TVA](https://www.impots.gouv.fr/professionnel/questions/en-tant-que-micro-entrepreneur-puis-je-etre-redevable-de-la-tva) ·
[Statistiques Salesforce 2026](https://enway.com/journal/salesforce-consultants/salesforce-statistics-all-the-facts-you-need-to-know/) *(source secondaire, à recouper)*.

---

*Document préparé par le Directeur Marketing & Contenu. Rien de ce qui précède n'a été
publié, envoyé, ni programmé [DH-CMO-001]. Curseur « envoyer vers l'extérieur » : Conseille.*
