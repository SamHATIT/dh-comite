# Dossier de revue externe — SH Conseil · Digital·Humans · DEOS

> **Direction financière · 10/08/2026 · Statut : dossier soumis à revue externe.**
> Destinataire : directrice financière en entreprise, sollicitée par Sam Hatit pour un
> avis indépendant. Périmètre : les trois marques portées par une seule personne et,
> comme on le verra au §2, par une seule entité juridique.
> **Chaque chiffre porte sa source ou la mention `Hypothèse`.** Ce qui n'est pas mesuré
> est signalé comme tel, y compris quand c'est gênant.

## Ce qu'il faut retenir

1. **Le revenu récurrent est nul et le revenu réel n'est pas mesuré.** Zéro abonné,
   zéro euro récurrent (`deos_state.cash_suivi.mrr_reel`, maj 02/08). Le seul revenu
   réel est le conseil facturé par Sam — et **son montant ne figure nulle part au
   dossier.** C'est la donnée manquante n°1, avant même le solde bancaire.
2. **Ce n'est pas une entreprise à court de trésorerie, c'est une entreprise à court de
   jours.** La dépense mesurée est de **360 $/mois** (`bin/couts.py`, 68 exécutions sur
   30 jours au 10/08). Le vrai coût est ailleurs : sur les 120 jours annuels de Sam,
   **52 sont déjà engagés dans le scénario médian, 72 dans le scénario haut.** À ce
   niveau de burn, un « nombre de mois de piste » n'a aucun sens : la contrainte est le
   calendrier, pas la caisse.
3. **L'enveloppe fiscale n'est pas partagée avec le conseil — correction majeure du
   10/08.** Le revenu de conseil est perçu **en portage salarial** (déclaré par Sam,
   10/08) : il est facturé par la société de portage et perçu en salaire. **Il n'entre
   pas dans le chiffre d'affaires de l'entité** (SIREN 343 172 490, entrepreneur
   individuel, BNC, franchise en base) et ne consomme donc **ni la franchise de TVA
   (37 500 €), ni le plafond micro (77 700 €)**. Les deux plafonds sont **intégralement
   disponibles pour Digital·Humans et DEOS**. Le régime ne sature que si le logiciel
   vend — ce qui déclasse le risque R3 et repousse la question de la société.
   *La version antérieure de ce dossier posait l'inverse ; c'était faux.*
4. **Ce qui bloque le revenu logiciel ne coûte pas d'argent.** Six constats bloquants
   juridiques, établis par preuve technique le 08/08, interdisent l'ouverture des
   inscriptions ; je n'ai trouvé au dossier **aucune preuve de levée à ce jour**. Tant
   qu'ils tiennent, toute projection de revenu logiciel vaut zéro.
5. **Ce qu'on demande à cette revue** : un avis sur **la structure** (une entité pour
   trois marques, et à quel seuil scinder), sur **la séquence** de développement, et
   sur **la méthode de projection** d'une activité mono-personne. **On ne demande pas
   de financement** — il n'y a rien à lever pour un burn de 331 €/mois.

---

## 1. Synthèse — où on en est

| | Valeur | Source |
| --- | ---: | --- |
| Revenu récurrent | **0 €** | `cash_suivi.mrr_reel`, maj 02/08 |
| Clients payants, toutes marques | **0** | idem ; zéro référence client (étude 08/08) |
| Revenu de conseil (portage) | **700 €/j facturés → ~350 €/j nets** | déclaré par Sam, 10/08 — voir §2.5 |
| Solde bancaire déclaré | **0 €, provisoire** | `cash_suivi`, déclaré le 14/07, non mis à jour depuis 27 j |
| Dépense mesurée du dispositif | **360 $/mois** (11,99 $/j) | `bin/couts.py` 30 j au 10/08, 68 exécutions |
| Régime de temps du fondateur | **mission à temps plein** ; DH construit hors temps de mission | déclaré par Sam, 10/08 — voir §3 |
| Coût d'opportunité d'un jour ouvré perdu | **350 € nets** (`H3` corrigée) | déclaré par Sam, 10/08 |
| Jours de mission manqués, juillet-août | **11 j ≈ 3 850 € nets**, imputés à DH | déclaré par Sam, 10/08 |
| Décisions en attente d'arbitrage | **3** (contre ~20 le 07/08) | table `decisions`, `$COMITE_DB_DSN` |
| Blocages juridiques ouverts | **6 sur 6** | `conformite_donnees_2026-08-08.md` |

**Le seul élément de traction vérifiable est interne, pas commercial.** Le 10/08,
34 lignes de la table `decisions` ont reçu une validation de Sam : la file d'attente est
passée d'une vingtaine de décisions gelées jusqu'à 27 jours à **trois**. Le dispositif
de gouvernance qu'on vend (§2.3) vient de faire la preuve de son propre usage.

**Ce qui inquiète, dans l'ordre.** Le revenu réel dépend à 100 % d'un **intermédiaire
unique**, lui-même exposé à un client final unique (§2.5, R9). Le rythme de mission
s'érode : 11 jours manqués en deux mois, soit environ 3 850 € nets, absorbés par le
développement du produit (§3) — c'est le premier coût du projet, très au-delà de sa
facture technique. Et la mention « SH Conseil », sous laquelle il est prévu de facturer
8 000 € à un établissement financier, **ne correspond à aucune entité documentée** —
point soulevé par la direction juridique le 08/08, escaladé à Sam, non résolu.

---

## 2. Une entité, trois marques

### 2.1 Ce que chacune rapporte par jour de Sam

Le seul dénominateur commun aux trois marques n'est ni le chiffre d'affaires ni la
marge : c'est **le jour de Sam**, seule ressource qu'elles se disputent réellement.

![Marge de contribution par jour de Sam consommé, par offre, scénario bas](graphiques/economie_unitaire_marque_2026-08-10.png)

> **Réserve — graphique non régénéré.** Sa ligne de référence est tracée à 800 €, valeur
> corrigée à **350 € nets** le 10/08 (§2.5). **La barre baisse de moitié** : plusieurs
> offres classées en rouge passent au-dessus du seuil. À régénérer avant diffusion.

*Lecture : en rouge, ce qui rapporte moins qu'un jour facturé (barre tracée à 800 € —
lire 350 €).
Sources : marge Pro reconstruite depuis la formule vérifiée le 09/08 ; DEOS SaaS =
86 400 €/an à 56,9 % de marge sur 20 jours (étude 08/08 §4.2) ; DEOS installé =
182 928 € de recette an 1 à 38,6 % (étude 09/08 §2), sur **35 jours — `Hypothèse`** :
le nombre de jours de la première affaire installée n'est pas chiffré au dossier.*

| Marque | Ce qu'elle est | Économie unitaire | État |
| --- | --- | --- | --- |
| **SH Conseil** | prestation de jours, **en sous-traitance via portage** (§2.5) | **700 €/j facturés → ~350 €/j nets** | **seul revenu réel** ; perçu en salaire, hors CA de l'entité |
| **Digital·Humans** | plateforme en libre-service, Pro 79 €/mois, Team 1 490 €/mois | Pro : **+44,0 % à 100 abonnés** (bas), −31,6 % (haut) ; seuil **38 abonnés** | 0 client · gatée par Salesforce · 6 blocages |
| **DEOS** | gouvernance d'agents, SaaS ou installé | **2 458 €/jour** à 86 400 €/an ; plancher **31 800 €**, parité Team **79 400 €** | 0 client, 0 référence, 0 installation |

*Prix Pro : 79 €/mois, tarif de lancement 59 € le premier mois (DEC-2026-0809-13,
accordée, `validation_par = sam`). Net encaissé 77,56 €/mois après frais de carte
(0,985 × prix − 0,25 €, barème EEE, `config/offre_dh.md`).*

**Un chiffre est systématiquement mal lu, et je le corrige ici.** On lit ailleurs que
« le Pro perd de l'argent en dessous de 38 abonnés ». C'est vrai **en coût complet et
faux en trésorerie** : le coût fixe de 25 200 €/an qui produit ce seuil se compose de
10 500 € de **temps de Sam** (30 jours de production de contenu à 350 €, `H3` corrigée
le 10/08 — le chiffre de 24 000 € qui figurait ici reposait sur 800 €) et de 1 200 €
d'outillage. **C'est un coût d'opportunité, pas une sortie de caisse.**

| Scénario d'ingénierie | Coût variable par abonné | Contribution nette mensuelle |
| --- | ---: | ---: |
| **Bas** — downgrade Pro branché, Free sur Haiku | 15,36 €/mois | **+62,20 €** |
| **Haut** — régime actuel non filtré, Free sur Sonnet | 75,10 €/mois | **+2,46 €** |

*Source : structure de coût variable du 09/08 (184,28 €/abonné/an en bas, 901,16 € en
haut), rapportée au mois.*

**Ce tableau dit où est le vrai levier, et ce n'est pas le prix.** La contribution d'un
abonné varie d'un facteur 25 entre les deux scénarios, et aucun prix raisonnable en
euros ou en dollars ne rend le Pro rentable dans le scénario haut. **Financer un
lancement sur l'hypothèse basse sans obtenir l'engagement d'ingénierie correspondant
(downgrade du Pro, modèle du tier gratuit), c'est parier la trésorerie sur une décision
non prise.**

### 2.2 Ce que chacune apporte aux deux autres — la dispersion

C'est le reproche attendu : trois marques pour une personne. La réponse honnête est
**qu'il y a une synergie réelle et une dispersion réelle, sur deux axes différents.**

**La synergie est du côté des actifs, et elle est vérifiable.** Le dispositif de
gouvernance que DEOS vend *est* le comité de direction qui produit ce dossier :
36 curseurs d'autonomie en base, un registre de 108 décisions, un journal des refus. La
démonstration prévue au Crédit Logement ne montre pas une maquette, elle montre l'outil
en service. Rien n'a été construit deux fois. Et la relation qui ouvre ce compte — le
DSI est connu personnellement de Sam — est un actif de SH Conseil, pas de la plateforme.

**La dispersion est du côté du calendrier et de l'enveloppe fiscale.** Les trois marques
ne se disputent pas des clients : elles se disputent des jours (§3) et un seul plafond
de recettes (§2.4).

**Le sens des portes, tranché le 08/08** : DEOS → Digital·Humans oui (un client DEOS
équipé de Salesforce est un client Team naturel) ; l'inverse non (l'acheteur Team est un
dirigeant de PME, il n'a pas de comité à gouverner). L'expansion est à sens unique et
part du haut de gamme.

**Ce qui se casserait si l'une disparaissait**, et la réponse n'est pas celle qu'on
attend : sans **SH Conseil**, tout s'arrête (seul revenu, seule relation grand compte,
seul véhicule de facturation). Sans **DEOS**, on perd l'accès aux grands comptes — c'est
la seule offre non gatée par Salesforce — et la meilleure marge par jour. Sans la
**plateforme Digital·Humans**, les deux autres survivent : DEOS repose sur le dispositif
de gouvernance, pas sur la chaîne de delivery Salesforce. **La marque la plus fragile
est donc celle qui porte le nom de l'ensemble** — zéro client, six blocages juridiques,
et la seule dont la disparition ne casserait rien.

### 2.3 DEOS installé — ce qui est chiffré et ce qui ne l'est pas

Pour les grands comptes qui refusent le SaaS par doctrine (cas du Crédit Logement :
internalisation, contrat LLM Microsoft déjà signé), le modèle est licence + maintenance :
**licence 129 600 à 259 200 €**, **maintenance 23 000 à 57 000 €/an**, installation
30 000 à 50 000 €, marge 38,6 % sur la première affaire et 55,0 % sur la suivante
(étude 09/08). Trois réserves, que je préfère poser moi-même :

- **Aucun consentement à payer n'a été mesuré** : ces niveaux viennent d'analogies de
  marché (maintenance à 18–22 % de la licence, licence à trois ans de valeur SaaS), pas
  d'un client interrogé.
- **Une condition de livraison n'est pas chiffrée** : le connecteur Azure OpenAI
  n'existe pas (vérifié dans `backend/config/llm_routing.yaml` le 09/08). Sans effet sur
  la démonstration d'août ; bloquant le jour d'un contrat.
- **La marge de la première affaire suppose une deuxième affaire** pour amortir
  l'intégration. Une affaire installée unique en paie seule la totalité.

### 2.4 Le point que je place au centre du dossier : une seule entité

**Les trois marques ne sont pas trois entités. Il n'y en a qu'une.**

| Élément | Valeur | Source |
| --- | --- | --- |
| Forme | entrepreneur individuel, micro-entreprise, BNC | Guichet Unique J00242553667, validée INSEE/URSSAF 19/05/2026 |
| SIREN / SIRET | 343 172 490 / 343 172 490 00033 | idem |
| Nom commercial déclaré | **Digital-Humans** | idem |
| TVA | franchise en base (art. 293 B CGI) | idem |
| « SH Conseil » | **aucune entité documentée** | `conformite_donnees_2026-08-08.md` §4.2 — escaladé à Sam, non résolu |

![Recettes des trois marques sur 12 mois face aux deux plafonds de l'entité unique](graphiques/plafonds_entite_2026-08-10.png)

*Lecture : les recettes de chaque scénario du §4, comparées aux deux plafonds légaux
applicables à l'entité — franchise de TVA 37 500 € (seuil majoré 41 250 €) et régime
micro 77 700 € (`pages_legales_2026-08-06.md` §5.1, impots.gouv.fr). Le conseil, les
abonnements et le cadrage s'additionnent dans le même compteur.*

1. **Le conseil ne compte pas dans ces plafonds.** Perçu en portage salarial, il est
   hors du chiffre d'affaires de l'entité (§2.5). Les recettes à comparer aux deux
   seuils sont **celles du logiciel et du cadrage seuls** — ce que le graphique
   ci-dessus n'isole pas encore.
2. **La franchise de TVA ne tombe plus dans le scénario bas.** Sans vente logicielle et
   sans cadrage conclu, les recettes de l'entité sont proches de zéro. Elle tombe en
   médian et en haut, **par le logiciel** : environ 45 000 € de recettes d'entité en
   médian (37 464 € d'abonnements + 8 000 € de cadrage) et environ 126 000 € en haut.
3. **Le plafond micro ne tombe plus que dans le scénario haut.** En médian, les
   ~45 000 € d'entité restent nettement sous 77 700 €. C'est un an de marge de manœuvre
   qui n'existait pas dans la version précédente de ce dossier.
4. **Ce qui reste vrai, et qui ne dépend pas du régime** : la responsabilité illimitée
   sur le patrimoine personnel dans un contrat d'installation avec un établissement
   financier supervisé. Le motif de passer en société est là, pas dans la fiscalité.

**Ma recommandation, en distinguant le motif du déclencheur.** Le motif décisif de
passer en société n'est pas fiscal : c'est **la responsabilité illimitée sur le
patrimoine personnel** dans un contrat d'installation avec un établissement financier
supervisé. Le déclencheur, lui, est chiffrable : **instruire dès 30 000 € de recettes
cumulées sur l'année civile** (l'indicateur n°6 du plan de lancement du 08/08 pose déjà
ce seuil), **trancher avant 41 250 €** — au-delà, la TVA devient exigible le jour même
du dépassement. *Ce point relève de l'expert-comptable et de l'avocat ; je pose
l'arithmétique, je ne rends pas l'avis.*

**Et une échéance à trois semaines que personne n'a rapprochée du reste** : au
**1er septembre 2026**, toute entreprise doit être en capacité de *recevoir* des
factures électroniques (aife.economie.gouv.fr, via l'étude juridique du 06/08). C'est la
semaine de la démonstration Crédit Logement.

---

### 2.5 La chaîne du revenu réel — ajoutée le 10/08

Le dossier décrivait « SH Conseil » comme une pratique de conseil facturant ses clients.
**Ce n'est pas la structure réelle**, et l'écart change plusieurs conclusions.

| Maillon | Rôle | Ce qui circule |
| --- | --- | --- |
| Crédit Logement | client final | commande la prestation |
| Éric | titulaire du contrat, facture le client final | marge non connue de nous |
| Société de portage | emploie Sam, facture Éric | frais de gestion |
| Sam | exécute la mission | **700 €/jour facturés → ~350 €/jour nets** |

**Quatre conséquences.**

1. **Crédit Logement n'est pas un client de l'entité.** Il est le client d'Éric. Sam
   dispose de son accord pour le citer comme référence, mais la relation contractuelle
   n'existe pas. Toute présentation commerciale doit en tenir compte.
2. **Ce revenu est un salaire, pas un chiffre d'affaires.** Il ne consomme aucun des
   deux plafonds de l'entité (§2.4) et n'apparaît pas dans ses recettes.
3. **Le coût d'opportunité réel est de 350 €, pas 800 €** — la moitié de ce que ce
   dossier supposait partout ailleurs avant correction.
4. **Le portage ouvre des droits à l'assurance chômage.** Pour un fondateur solo sans
   revenu récurrent, c'est un élément de solidité financière que ce dossier omettait :
   il existe un filet en cas d'arrêt, ce qui rend le pari produit moins exposé qu'il
   n'y paraît. À confirmer auprès de la société de portage.

**Ce que nous ne savons pas et qu'il faut demander** : la marge prise par Éric entre le
client final et Sam, la durée contractuelle de son engagement, et l'existence d'une
clause d'exclusivité ou de non-concurrence qui interdirait de vendre DEOS au même client
depuis l'entité. **Sam indique une visibilité jusqu'à l'été 2027, voire fin 2027** —
information favorable, mais déclarative et non contractualisée à notre niveau.

---

## 3. Le temps de Sam — la seule ressource véritablement rare

**Correction du 10/08 : le modèle de temps de ce dossier était faux.** Il posait
120 jours par an répartissables entre le conseil et la plateforme, comme si Sam
arbitrait entre les deux. Ce n'est pas ce qui se passe. Sam est **en mission à temps
plein** (environ 21 jours ouvrés par mois) et **Digital·Humans se construit hors temps
de mission** — soirées et week-ends. Il n'y a pas d'arbitrage entre facturer et
développer : les deux se cumulent dans la même journée.

Le coût d'un jour donné au produit a donc **deux régimes**, et non un taux unique :

| Nature du temps | Coût d'opportunité |
| --- | ---: |
| Soirée, week-end, congé | **0 €** — aucun revenu n'y était possible |
| Jour ouvré de mission non facturé | **350 € nets** (700 € facturés, ~50 % après portage et charges) |

**Et c'est le second régime qui se lit dans les chiffres.** Sur un rythme plein
d'environ 21 jours, **juillet n'a compté que 14 jours facturés** — 7 jours perdus, soit
**2 450 € nets**. **Août en compte déjà 4 de perdus**, soit **1 400 €**. Onze jours en
deux mois, **environ 3 850 € nets**, imputés par Sam au développement du produit.

**À rapprocher de la facture technique du dispositif : 690 € sur les deux mêmes mois.**
Le coût réel du projet est donc **environ 5,6 fois sa dépense d'infrastructure**, et
cette part n'apparaissait nulle part au dossier. C'est le chiffre le plus important de
cette revue.

**Ce que cela dit du modèle, et qu'il faut écrire plutôt que lisser** : un temps plein
en mission additionné d'un produit construit le soir produit exactement cette courbe —
des jours facturés qui s'effritent. L'érosion n'est pas un accident de calendrier, c'est
la signature du régime de travail actuel. La question posée à la revue n'est pas
« comment répartir 120 jours » mais **combien de temps ce rythme peut tenir, et ce qui
cède en premier**.

![Répartition des jours consacrés au produit selon les trois scénarios](graphiques/temps_sam_2026-08-10.png)

> **Réserve — ce graphique n'a pas encore été régénéré.** Il repose sur le modèle des
> 120 jours répartissables, invalidé ci-dessus, et sur un jour à 800 €. Les volumes de
> jours par poste restent indicatifs ; leur valorisation est à diviser par deux et leur
> imputation à relire comme du temps hors mission. À reprendre avant diffusion large.

*Lecture : postes chiffrés depuis les plans existants — 30 jours/an de production de
contenu (les 24 000 € de « coût marketing fixe » de l'étude du 09/08), 12 jours/an de
comité et d'arbitrage (`Hypothèse` : un jour par mois), 2 à 30 jours de DEOS selon qu'on
s'arrête au cadrage (8 jours) ou qu'on porte une affaire complète (20 jours, `H2`). Le
solde est ce qui reste disponible pour facturer du conseil.*

### Le creux de septembre — absence planifiée, à ne pas confondre avec l'érosion

Sam est absent **du 7 au 20 septembre**, sans rémunération. Septembre 2026 compte
22 jours ouvrés ; l'absence en couvre **10**.

| | jours ouvrés | revenu net |
| --- | ---: | ---: |
| Mois plein | 22 | 7 700 € |
| Septembre 2026 | 12 | **4 200 €** |
| **Écart** | **−10** | **−3 500 €** |

**Cette absence n'est pas de l'érosion et ne doit pas être additionnée à l'indicateur
n°1.** Juillet et août mesurent un rythme qui cède ; septembre mesure un choix assumé,
décidé à l'avance. Les confondre masquerait le seul signal qui compte.

**Lecture inverse, qui vaut d'être posée** : ces 10 jours ouvrés sont les seuls de
l'année où du temps produit est disponible **à coût d'opportunité nul** — le revenu est
déjà renoncé, la décision est prise. C'est la plus grosse réserve de temps produit de
l'exercice, et elle tombe juste après l'ouverture.

**Ce que la trésorerie ne montre pas, et qu'il faut dire.** Dans le scénario haut, la charge produit
dépasse ce qu'une soirée absorbe : elle déborde sur les jours ouvrés, et chaque
débordement vaut 350 € nets. Le succès de la plateforme ne se paie pas en jours de
conseil arbitrés d'avance — il se paie **en jours de mission manqués, après coup**,
exactement le mécanisme observé en juillet et en août.

**La contradiction de sources est tranchée.** Ce dossier posait 120 jours de capacité
totale, l'étude commerciale du 08/08 posait 120 jours pour la plateforme seule. **Les
deux sont caduques** : la capacité de mission est d'environ 250 jours ouvrés, presque
intégralement engagée, et le temps produit vient s'ajouter en dehors. Ce qu'il faut
mesurer désormais n'est pas une répartition mais **un taux d'érosion** : jours de
mission manqués par mois. Il vaut 7 en juillet, 4 à mi-août.

---

## 4. La trésorerie — trois scénarios, hypothèses déclarées

**Réserve à lire avant les chiffres : je ne projette pas un solde, je projette un
flux.** Le solde bancaire déclaré est de 0 € au 14/07, qualifié de provisoire par Sam
lui-même (compte professionnel en cours d'ouverture), non mis à jour depuis 27 jours.
Le graphique donne donc le flux net cumulé, **à ajouter au solde d'ouverture réel —
inconnu**. Tout chiffre de « mois restants » serait une fausse précision.

![Flux de trésorerie net cumulé sur 12 mois, trois scénarios](graphiques/tresorerie_scenarios_2026-08-10.png)

| | **Bas** | **Médian** | **Haut** |
| --- | ---: | ---: | ---: |
| Recettes 12 mois | 43 680 € | 78 104 € | 148 702 € |
| dont abonnements Pro | 0 € | 37 464 € | 74 462 € |
| Dépenses 12 mois | 4 331 € | 6 317 € | 9 618 € |
| **Flux net cumulé** | **+39 349 €** | **+71 787 €** | **+139 085 €** |
| Recettes en régime de croisière (année pleine) | 43 680 € | 79 179 € | 106 810 € |

> **Réserve de périmètre, ajoutée le 10/08 — à lire avant le tableau.** La ligne
> « Recettes 12 mois » **agrège le conseil et le logiciel**. Or le conseil est perçu en
> portage salarial, hors de l'entité (§2.5). Ces montants décrivent donc **ce que Sam
> perçoit toutes sources confondues**, et non le chiffre d'affaires de l'entité.
> Pour les plafonds fiscaux, seules comptent les lignes d'abonnements et de cadrage :
> environ **0 €** en bas, **45 000 €** en médian, **126 000 €** en haut. Le modèle
> n'a pas été réexécuté ce soir ; ces trois montants sont recomposés à la main depuis
> les lignes existantes et doivent être recalculés avant diffusion.

**Hypothèses communes** : jour de Sam **à 350 € nets** (`H3` corrigée le 10/08 :
700 € facturés via portage, ~50 % après frais de gestion et charges — les projections
ci-dessous n'ont pas encore été réexécutées avec cette valeur et **surestiment le
revenu de conseil d'un facteur proche de 2**) ; taux d'occupation du conseil **60 %**
(`Hypothèse` — caduque : la mission est à temps plein, voir §3) ; dépense API mesurée à 360 $/mois convertie à
1 $ ≈ 0,92 € (`Hypothèse`, reprise du 09/08) ; VPS Hostinger à **30 €/mois**
(`Hypothèse` — montant réel introuvable, demandé depuis le 09/08) ; frais de carte
0,985 × prix − 0,25 €.

- **Bas** — les six blocages ne sont pas levés : aucune inscription, aucun revenu
  logiciel, le cadrage Crédit Logement ne se conclut pas. 91 jours restent disponibles
  pour le conseil, dépense API stable.
- **Médian** — ouverture le 01/10 (un mois après le plan, au vu des six blocages),
  trajectoire nominale du plan marketing (8 / 25 / 50 abonnés à J+30/60/90), **gelée à
  50 faute de trajectoire documentée au-delà** ; cadrage encaissé 8 000 € en novembre ;
  aucune licence DEOS ; dépense API doublant linéairement sur 12 mois.
- **Haut** — ouverture le 01/09 comme prévu, trajectoire ambitieuse (15 / 45 / 90),
  cadrage encaissé en octobre, **une affaire DEOS SaaS signée fin février 2027** (cycle
  grand compte de 180 jours, `H1`), encaissée 43 200 € en avril ; forfait GPU souscrit.

**Les trois fragilités, par ordre d'importance :**

1. **La variable déterminante n'est plus le carnet de commandes, c'est le taux
   d'érosion.** La mission est à temps plein : le conseil n'est pas limité par la
   demande mais par les jours que Sam parvient à honorer. À 350 € nets, **chaque jour
   manqué coûte autant qu'environ sept abonnements Pro mensuels**. Au rythme observé —
   7 jours en juillet, 4 à mi-août — l'érosion représente **~23 000 € nets sur douze
   mois**, davantage que ce que le lancement du Pro rapporte dans le scénario médian.
   **C'est le poste le plus lourd du dossier et il n'était pas compté.**
2. **L'élasticité prix n'est pas mesurée.** La trajectoire d'abonnés a été construite
   pour un prix de 49 € et s'applique ici à 79 €. C'est l'hypothèse la plus optimiste
   du dossier.
3. **Aucune recette logicielle ne peut courir aujourd'hui.** Le parcours de paiement
   tourne en clé de test (`STRIPE-PROD-001` non fait, constat du 09/08 — non revérifié
   ce jour, voir Réserves) et les six blocages interdisent l'ouverture. **Chaque semaine
   de retard décale toute la colonne.**

**Ce que la trésorerie ne montre pas, et qu'il faut dire** : dans les trois scénarios le
flux est positif et le burn dérisoire. **Cette entreprise ne peut pas manquer d'argent
au sens habituel — elle ne peut manquer que de jours de Sam.** C'est pourquoi le §3
précède celui-ci. Et depuis le 10/08 on sait que ces jours ne se perdent pas par
arbitrage mais **par fatigue** : le fondateur déclare lui-même que les onze jours
manqués tiennent au cumul mission plus produit. **Aucune ligne de ce dossier ne couvre
ce risque, et c'est la question la plus utile à poser à la revue.**

---

## 5. Les indicateurs à suivre — et où on en est

Règle appliquée : un indicateur qui ne déclenche aucune décision n'a rien à faire sur un
tableau de bord. Sept suffisent.

| # | Indicateur | Où on en est | Décision qu'il déclenche |
| --- | --- | --- | --- |
| 1 | **Jours de mission manqués / mois** (taux d'érosion — **hors absences planifiées**, cf. §3) | **7 en juillet, 4 à mi-août** | au-delà de 3 j/mois deux mois de suite : réduire la charge produit, le rythme n'est pas tenable |
| 2 | **Recettes de l'entité, année civile** — logiciel + cadrage **hors portage** | **0 €** (inscriptions fermées) | > 30 000 € : instruire la société ; > 37 500 € : préparer la TVA |
| 3 | Solde bancaire déclaré | 0 €, provisoire, 27 j sans mise à jour | sous 50 € : alerte (seuil confirmé par Sam le 03/08) |
| 4 | **Blocages juridiques ouverts** | **6 sur 6** | tant que > 0 : aucune projection de revenu logiciel n'est opposable |
| 5 | Abonnés Pro actifs | 0 (inscriptions fermées) | sous 60 % de la courbe nominale 2 semaines de suite : changer d'angle |
| 6 | Dépense du dispositif | 11,99 $/j, 360 $/mois | au-delà de 500 $/mois : brider les missions ponctuelles |
| 7 | Décisions en attente > 20 jours | 0 (3 en attente, la plus ancienne du 09/08) | une seule : le goulot est l'arbitrage, pas la production |

**Pourquoi ceux-là.** Les métriques classiques du logiciel — revenu récurrent, attrition,
coût d'acquisition, ratio valeur/coût client — sont **inapplicables à zéro client** : les
calculer produirait des ratios sur des dénominateurs nuls, définition d'un tableau de
bord décoratif. Les deux premiers indicateurs ne sont pas des indicateurs de logiciel :
ce sont ceux d'une pratique de conseil qui finance un produit, et c'est ce que cette
entreprise est aujourd'hui. **Les indicateurs 1, 2 et 4 ne sont pas mesurés : c'est le
principal défaut de pilotage de ce dossier, plus grave que n'importe lequel des chiffres
qui précèdent.**

---

## 6. Les risques, hiérarchisés

| # | Risque | Portée | Ce qu'on en fait |
| --- | --- | --- | --- |
| **R1** | **Concentration totale sur une personne** — un porteur, une source de revenu, aucun salarié | perte de 100 % du revenu en cas d'indisponibilité | non couvert. Aucune assurance, aucun second porteur. À poser à la revue |
| **R2** | **Six blocages juridiques gatent 100 % du revenu logiciel** (identifiants clients en clair, cloisonnement non prouvable, pages légales non publiées) | tout le §4 hors conseil | chemin critique. Ne coûte pas d'argent, coûte des jours |
| **R3** | **L'enveloppe fiscale sature** — **déclassé le 10/08** : le conseil étant en portage, les deux plafonds sont intégralement disponibles pour le logiciel | régime, forme juridique | instruire à 30 000 € de recettes **d'entité**, trancher avant 41 250 €. Le motif reste la responsabilité illimitée, pas la fiscalité (§2.4) |
| **R4** | **Le solde bancaire n'est pas suivi** depuis 27 jours (le revenu de conseil, lui, est désormais mesuré : §2.5) | toute décision d'engagement | demande à Sam. Le TJM est connu, le solde ne l'est pas |
| **R9** | **Dépendance à un intermédiaire unique** — 100 % du revenu réel transite par un sous-traitant (Éric), lui-même exposé à un client final unique (Crédit Logement), le tout via une société de portage | perte de la totalité du revenu réel si la chaîne se rompt à n'importe lequel de ses trois maillons | **non couvert.** Aucun second donneur d'ordre. À poser à la revue en priorité |
| **R11** | **Ouverture le 1er septembre, absence du 7 au 20** — les six premiers jours d'exploitation sont suivis de deux semaines sans le fondateur, sur la fenêtre où arrivent les premiers inscrits, les premiers incidents et les premières questions. Les trois échéances réglementaires tombent le même 1er septembre | image de marque au lancement, incidents non traités, conformité non finalisée | **arbitré par Sam le 11/08 : ouverture maintenue au 1er.** Dispositif : Telegram en canal d'urgence, le CEO du comité assure la continuité. Décalage au 21 septembre écarté |
| **R10** | **Soutenabilité du régime de travail** — mission à temps plein plus produit construit le soir ; érosion mesurée à 11 jours sur juillet-août (~3 850 € nets) | la ressource critique du dossier, et la seule non substituable | aucun dispositif. Suivi par l'indicateur n°1 (§5) |
| **R5** | **La marge du Pro dépend d'un arbitrage d'ingénierie non pris** | facteur 25 sur la contribution par abonné (§2.1) | obtenir l'engagement technique **avant** d'ouvrir les inscriptions |
| **R6** | **Le canal Team est indisponible** — chaîne BUILD en échec, exécution 165, échec encore constaté au 10/08 | le palier à 1 490 €/mois, soit 18,9 abonnés Pro par client | exclu des projections du §4. Aucun revenu Team supposé |
| **R7** | **DEOS : zéro référence, zéro installation, connecteur Azure OpenAI inexistant et non chiffré** | la seule offre ouverte aux grands comptes | ne rien promettre en août au-delà de la démonstration et du cadrage |
| **R8** | **« SH Conseil » n'est pas une entité documentée** alors qu'on prévoit de facturer sous ce nom | le cadrage à 8 000 € et le contrat de sous-traitance | à clarifier **avant** la réunion de fin août |

**Ce qui n'est pas dans ce tableau et devrait inquiéter une lectrice extérieure** : il
n'y a aucun risque de marché — non parce qu'il n'y en a pas, mais parce qu'avec zéro
client, **aucune hypothèse de marché n'a encore été confrontée à un acheteur.** Le
premier risque réel de ce dossier est peut-être celui qu'il ne peut pas encore nommer.

---

## 7. Ce qu'on attend de cette revue

**Trois demandes, par ordre de valeur. Ce ne sont pas les mêmes questions.**

1. **La structure — priorité 1.** Une entité pour trois marques, deux plafonds partagés,
   une responsabilité illimitée face à un contrat bancaire. La question n'est pas
   « faut-il une société ? » mais **à quel seuil, sous quelle forme, et quelle marque y
   met-on d'abord ?** Notre proposition — instruire à 30 000 €, trancher avant 41 250 €,
   motif = responsabilité et non fiscalité — mérite d'être attaquée.
2. **La séquence — priorité 2.** L'ordre que nous retenons : (a) lever les six blocages
   juridiques, parce qu'ils ne coûtent pas d'argent et bloquent tout ; (b) DEOS en
   cadrage payant, parce que c'est la meilleure marge par jour, que l'encaissement est
   proche et qu'il ne dépend pas de la chaîne BUILD ; (c) le Pro, seul revenu qui ne
   consomme plus de temps une fois livré, mais dont le seuil est à 38 abonnés ; (d) Team
   en dernier **malgré la meilleure marge unitaire**, parce que le produit est en échec.
   **Est-ce le bon ordre ?** C'est un avis de dirigeante que nous cherchons, pas un
   calcul.
3. **La méthode de projection — priorité 3.** Nous projetons le revenu de conseil par
   « capacité × taux d'occupation », faute de carnet de commandes. Est-ce la bonne façon
   de modéliser une activité mono-personne, ou faut-il exiger un carnet daté avant toute
   projection ? La réponse changerait la construction du §4, pas seulement ses chiffres.

**Ce que nous ne demandons pas, pour ne pas gaspiller son temps :**

- **Pas d'avis sur le financement.** Le burn est de 331 €/mois. Il n'y a rien à lever,
  et une levée répondrait à un problème que nous n'avons pas.
- **Pas d'avis sur le prix du Pro.** Instruit sur quatre hypothèses et arbitré par Sam
  le 10/08 (79 €, lancement à 59 € le premier mois). Le dossier est disponible si elle
  veut le contredire, mais nous ne le rouvrons pas de nous-mêmes.
- **Pas de conseil fiscal ou juridique définitif** — c'est le rôle d'un expert-comptable
  et d'un avocat. Nous cherchons un jugement de dirigeante sur la structure.

---

## Réserves

- **Le revenu de SH Conseil n'est pas mesuré.** C'est le trou le plus important du
  dossier : le seul revenu réel de l'entreprise y figure comme une hypothèse de taux
  d'occupation. Tout le §4 en dépend.
- **Le solde bancaire d'ouverture est inconnu** (0 € déclaré le 14/07, provisoire).
  Aucun « nombre de mois de piste » n'est donné, volontairement.
- **Le montant du VPS Hostinger reste introuvable** malgré une demande du 09/08 ; retenu
  à 30 €/mois en `Hypothèse`. La dépense du §4 est un plancher, pas un total.
- **Le taux de change 1 $ ≈ 0,92 €** vient de la mission du 09/08, pas d'une source
  interne datée.
- **Les 35 jours de Sam de la première affaire DEOS installée sont mon hypothèse**,
  déduite de la projection à 12 mois de l'étude du 08/08. Le chiffre exact n'est pas au
  dossier.
- **La marge de Team n'est pas chiffrée de façon fiable** : le Commercial a signalé le
  09/08 que son coût de jetons n'avait jamais été compté, comme celui du Pro avant
  correction. Aucun revenu Team n'est projeté, ce qui rend le scénario haut **prudent**
  sur ce point précis.
- **Je n'ai pas pu revérifier l'état du parcours de paiement aujourd'hui.** La requête a
  été refusée par le garde-fou d'autonomie (curseur `engager_depense` réglé sur
  « Observe »), déclenché par un mot-clé présent dans la commande. Je rapporte le refus
  au lieu de le contourner. **Le filtre est trop large** : il bloque une lecture de
  configuration comme il bloquerait un paiement — même nature de défaut que celui
  corrigé le 04/08 sur les mots `updated_at`/`deleted`. À signaler au dispositif ; ce
  n'est pas à moi de modifier le garde-fou.
- **Je n'ai pas instruit le fond juridique** des six constats bloquants ni la
  souveraineté du serveur GPU : terrains de la direction juridique. Je ne reprends que
  ce qu'ils déplacent économiquement.

---

## Annexe — méthode et sources

**Dépense mesurée.** `bin/couts.py`, chemin corrigé de `/root/workspace/dh-comite`
(inexistant ici) vers `/workspace` — **le script partagé pointe toujours au mauvais
endroit ; je le signale pour la troisième fois plutôt que de le modifier sans revue.**
Fenêtre de 30 jours au 10/08/2026, fichiers `*/*.json` portant un `total_cost_usd` :
**68 exécutions, 143,83 $, 11,99 $/jour**. Par modèle, imputé au prorata des jetons de
sortie comme dans le script : Sonnet 5 72,7 %, Opus (5 + 4.8) 20,3 %, Fable 5 6,9 %.
Cette mesure couvre les exécutions du comité — **ni le VPS, ni le serveur vidéo, ni
d'éventuels frais bancaires.**

**Marge du Pro.** Formule du Commercial, vérifiée par reconstruction indépendante le
09/08 et rejouée ici à 79 € : `Coût(n) = 25 200 € + n × (variable + 0,10 × prix annuel)`,
variable = 184,28 €/an (bas) ou 901,16 €/an (haut). Contrôle de cohérence : la marge
calculée à 100 abonnés (**44,0 %**) retombe exactement sur celle publiée le 10/08 — la
reconstruction est fidèle.

**Modèle de trésorerie.** 12 mois, septembre 2026 → août 2027. Recettes = (jours
disponibles × 60 % × 800 €)/12 + abonnés × 77,56 € + cadrage + encaissement DEOS.
**Formule caduque au 10/08** : le terme de conseil doit être remplacé par
(jours de mission honorés × 350 € nets), hors chiffre d'affaires de l'entité, et le
taux d'occupation de 60 % n'a plus d'objet (mission à temps plein). Modèle à
réexécuter.
Dépenses = API (331 €/mois, × facteur linéaire 1 → 2 hors scénario bas) + VPS 30 € +
forfait GPU 275 € en scénario haut seulement. Trajectoires d'abonnés : celles du plan de
lancement du 08/08 (nominale 8/25/50, ambitieuse 15/45/90), **gelées à leur dernier
point mesurable** — aucune extrapolation au-delà de J+90.

**Sources internes**, toutes datées, consultées le 10/08 :
`financier/position_2026-08-09.md` · `besoins_et_projections_2026-08-09.md` ·
`long_terme_2026-08-10.md` · `commercial/offre_revue_2026-08-09.md` et son complément ·
`deos_grands_comptes_2026-08-08.md` · `deos_installe_2026-08-09.md` ·
`dossier_demo_credit_logement_2026-08-10.md` · `deos_positionnement.md` ·
`marketing/plan_lancement_2026-08-08.md` §5.3, §5.5, §6 ·
`legal/conformite_donnees_2026-08-08.md` · `identite_legale.md` ·
`pages_legales_2026-08-06.md` §5 · `offre_dh.md` · `sh-conseil/_note_classement.md`.

**Bases interrogées** (`psql "$COMITE_DB_DSN"`, lecture seule) : table `decisions`
(108 lignes — 55 accordées, 41 closes, 5 en exécution, 4 refusées, 3 en attente de Sam ;
34 lignes portant une validation de Sam datée du 10/08) ; `deos_state.cash_suivi` (solde
déclaré 0 € au 14/07, revenu récurrent 0, aucune échéance connue, seuil d'alerte 50 €,
plafond de recharge API 100 $ avec recharge automatique depuis le 02/08).

**Sources publiques**, citées via les études internes : impots.gouv.fr et
bofip.impots.gouv.fr (seuils micro et TVA) · aife.economie.gouv.fr (facturation
électronique) · RH Solutions (tarif journalier d'un profil technique senior) ·
NPI Financial, ERP Research, Kellblog, Centraleyes (économie du logiciel installé).

**Graphiques** : `charte.py` du skill `dh-charte-documents`. Les graphiques 2 et 4 sont
en variante locale de la charte (couleurs et police inchangées) : le gabarit partagé code
le dépassement d'un seuil en vert « favorable », ce qui est faux pour un plafond fiscal —
franchir 77 700 € est une contrainte, pas un succès.
