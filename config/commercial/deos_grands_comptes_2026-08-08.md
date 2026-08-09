# DEOS — Étude de marché, de positionnement et de tarification GRANDS COMPTES
> Directeur Commercial · 08/08/2026 · Commandée par Sam (DEC-2026-0805-01, arbitrée le 08/08 ;
> routée par le CEO en DEC-2026-0808-03). Échéance proposée : 13/08. Présentation Crédit Logement :
> dernière semaine d'août.
> **Statut : proposition. Aucun prix ci-dessous n'existe dans l'offre canonique. DH-CRO-002 s'applique —
> Sam tranche, je propose.**

```json
{
  "type": "EtudePricing",
  "agent": "commercial",
  "date": "2026-08-08",
  "objet": "DEOS grands comptes — marché, positionnement, tarification",
  "decisions_sources": ["DEC-2026-0805-01", "DEC-2026-0808-03", "DEC-2026-0806-14"],
  "fait_majeur_du_jour": {
    "constat": "Le prérequis bloquant de DEC-2026-0806-14 est LEVÉ",
    "detail": "Le curseur d'autonomie n'est plus du texte dans des prompts : table `curseurs` en base (36 lignes = 6 directions × 6 types de tâche), lue par le hook PreToolUse toutes les 60 s, refus journalisés dans hooks.log (427 lignes, dernier refus tracé le 08/08 à 07:26:34).",
    "consequence": "La démonstration devant un DSI devient possible. C'est le seul actif produit réellement démontrable fin août."
  },
  "positionnement_retenu": {
    "concurrent_percu": "Plateforme de gouvernance IA américaine (Credo AI, Holistic AI, IBM watsonx.governance) — PAS une prestation de conseil",
    "raison": "Le concurrent perçu détermine le prix acceptable. Contre le conseil, DEOS vaut des jours-homme. Contre une plateforme, il vaut un abonnement annuel.",
    "plancher_marche_concurrent": "50 000 $/an (OneTrust, IBM OpenPages)",
    "plafond_marche_concurrent": "500 000 $/an (IBM, Credo AI, ModelOp)"
  },
  "approches_tarification": [
    {
      "id": "A",
      "nom": "Abonnement au périmètre gouverné",
      "unite": "direction gouvernée × mois",
      "niveau_propose": "1 200 €/direction/mois, minimum 3 directions",
      "fourchette_an": [43200, 86400],
      "recommandee_comme": "grille affichée"
    },
    {
      "id": "B",
      "nom": "Socle + revue de gouvernance",
      "unite": "forfait annuel + prestation trimestrielle + installation",
      "niveau_propose": "30 000 €/an socle + 24 000 €/an revue + 25 000 € installation",
      "fourchette_an1": [54000, 79000],
      "recommandee_comme": "montage de la première affaire (encaisse plus tôt)"
    }
  ],
  "seuils_calcules": {
    "plancher_destruction_valeur_DEOS": "31 800 €/compte/an — en dessous, Sam gagne plus en facturant ses jours chez SH Conseil",
    "parite_avec_le_canal_Team": "79 400 €/compte/an — au-dessus, un compte DEOS rapporte mieux qu'un client Team au temps de Sam égal",
    "seuil_de_rentabilite_du_Pro": "≈150 abonnés payants (LTV/CAC 4,70x, payback 8,7 mois). En dessous de 120, le Pro échoue au seuil."
  },
  "articulation_DH_DEOS": {
    "cannibalisation_chiffre": "non — segments disjoints, facteur 5 sur le prix",
    "cannibalisation_reelle": "le TEMPS de Sam — 120 j/an disponibles, 20 j par affaire DEOS",
    "sens_de_la_porte": "DEOS → DH oui ; DH → DEOS non"
  },
  "credit_logement": {
    "ce_qu_on_vend_fin_aout": "une démonstration du dispositif + un cadrage payant, pas une licence",
    "prix_si_demande": "fourchette de cadrage 40–90 k€/an, jamais un prix ferme",
    "cadrage_paye_propose": "8 000 € (5 à 10 jours SH Conseil)",
    "montage_recommande": "SH Conseil — confirmé économiquement (voir §5.4)"
  },
  "verification_produit": {
    "demontrable_fin_aout": ["curseur en base par direction et par type de tâche", "garde-fou technique qui refuse et journalise", "registre des décisions horodaté", "brief quotidien consolidé"],
    "NON_demontrable": ["tableau de bord de gouvernance côté client", "journal d'audit exportable", "installation dans le SI d'un client", "toute référence client — nous en avons zéro"],
    "regle": "DH-CRO-004 — rien de la colonne NON_demontrable ne doit être promis le jour J"
  },
  "escalades": ["montage Crédit Logement (déjà ouvert, DEC-2026-0806-14)", "validation des deux grilles — DH-CRO-002", "AI Act : report de l'annexe III à confirmer par le Juridique", "mode supervision : incompatible avec DEC-2026-0808-07"],
  "demandes_d_arbitrage_nouvelles": 2
}
```

---

## 0. Méthode, et ce que je sais contre ce que je suppose

Cette étude s'appuie sur trois sources et je les distingue partout dans le texte.

**Ce que j'ai vérifié moi-même, en base ou sur le disque** — c'est un fait, il porte sa requête.
**Ce que j'ai trouvé publiquement, daté et sourcé** — c'est un fait de marché, il porte son URL.
**Ce que je pose comme hypothèse** — c'est écrit `Hypothèse`, avec ce qui la fonderait ou la démentirait.

Deux outils neufs installés ce jour ont servi : `pricing-strategist` et `channel-economics`. Leurs
scripts sont déterministes ; j'ai gardé leurs sorties telles quelles, y compris quand elles me
contredisent (§3.4 et §4.2 en sont les deux exemples).

**Ce que je n'ai pas et qu'il faut savoir avant de lire :** nous n'avons **aucune donnée de
consentement à payer**. Zéro répondant. J'ai passé le script `wtp_analyzer.py` avec 5 répondants
fictifs uniquement pour vérifier son garde-fou : il rend
`« Sample size N=5 is below 30. PSM results are directional only »`. Je n'ai donc **pas** construit
le prix par l'analyse de sensibilité au prix. Je l'ai construit par le coût chargé et par la
comparaison concurrentielle, qui sont les deux seules bases dont je dispose honnêtement.

---

## 1. LE MARCHÉ — qui achète un dispositif de gouvernance d'agents, et pourquoi

### 1.1 Le marché existe, il est jeune, et il est en train de basculer

Gartner situe les dépenses mondiales en modèles et plateformes d'IA à **64 milliards de dollars en
2026, soit +63,4 % sur un an**, et considère que la bataille de 2026 se joue précisément sur la
gouvernance ([La Revue Tech, 2026](https://larevuetech.fr/gartner-prevoit-63-pour-les-modeles-et-plateformes-dia-en-2026-la-bataille-se-joue-sur-la-gouvernance/)).
Le cadre de référence porte un nom chez Gartner : **AI TRiSM** (AI Trust, Risk and Security
Management), et une catégorie neuve y est apparue, les *guardian agents* — définis comme le mélange
de gouvernance IA et de contrôles à l'exécution qui rend l'action d'un agent autonome fiable et
sécurisée ([Gartner Market Guide for Guardian Agents, via OpsIn Security](https://www.opsinsecurity.com/blog/gartner-market-guide-guardian-agents)).

C'est exactement la description de ce que fait notre hook PreToolUse. Le vocabulaire de la catégorie
existe déjà ; nous n'avons pas à en créer un.

Le chiffre qui compte le plus pour nous n'est pas la taille du marché mais **l'état d'avancement des
acheteurs**. Enquête Gartner auprès des DSI, juin 2026 : **17 % des DSI interrogés ont déjà déployé
des agents IA, 42 % prévoient de le faire dans l'année**
([même source](https://larevuetech.fr/gartner-prevoit-63-pour-les-modeles-et-plateformes-dia-en-2026-la-bataille-se-joue-sur-la-gouvernance/)).

Lecture commerciale : le segment adressable *maintenant* n'est pas « les entreprises qui veulent des
agents ». C'est **les 17 % qui en ont déjà déployé et qui découvrent qu'ils ne savent pas les
encadrer**. C'est un segment étroit, mais c'est un segment où le besoin est déjà formulé par
l'acheteur — pas un besoin qu'il faut lui faire admettre. Les 42 % suivants sont un marché de
2027, pas de 2026.

### 1.2 Les segments, nommés, et le motif d'achat de chacun

| Segment | Motif d'achat | Solidité |
|---|---|---|
| **Établissements financiers sous supervision ACPR** | Obligation réglementaire. DORA impose la **traçabilité exhaustive des décisions**, chaque délibération enregistrée, archivée, revue périodiquement ; l'article 8 impose une cartographie complète des actifs TIC supportant les fonctions critiques ([Haas Avocats, DORA 2026](https://www.haas-avocats.com/cybersecurite/dora-2026-cybersecurite-et-gouvernance-bancaire/)). L'ACPR devrait par ailleurs être désignée autorité de surveillance des systèmes d'IA à haut risque du secteur bancaire (même source). | **Fait sourcé.** C'est le segment le plus dur et le plus solide. |
| **Grandes entreprises ayant déjà déployé des agents** (les 17 %) | Le contrôle a posteriori : « qui a décidé quoi, avec quelle autorisation ». Motif opérationnel avant d'être réglementaire. | **Fait sourcé** (enquête Gartner juin 2026). |
| **Entreprises soumises à l'AI Act hors haut risque** | Transparence et littératie IA, applicables depuis le 2 août 2026 sans seuil de taille ([SmartForge](https://www.smartforge.fr/blog/ai-act-2-aout-2026-entreprise)). | **Fait, mais moins urgent qu'il n'y paraît — voir §1.3.** |
| **ETI et scale-up déployant des agents métier** | Ni obligation ni contrôle : la peur de l'incident. | `Hypothèse.` Je n'ai aucune preuve datée de budget sur ce segment. |

### 1.3 Le point qui affaiblit l'argument réglementaire — et qu'il faut dire avant de le découvrir en réunion

Un accord politique provisoire entre le Parlement et le Conseil, conclu le **7 mai 2026** dans le
cadre du paquet « Digital Omnibus », **a repoussé l'application des obligations « haut risque » de
l'annexe III du 2 août 2026 au 2 décembre 2027**
([mdp-data](https://mdp-data.com/ai-act-systemes-ia-haut-risque-aout-2026/)).

Conséquence directe sur notre discours : **on ne peut pas vendre DEOS en agitant une échéance AI Act
imminente sur le haut risque.** Elle a bougé de seize mois. Ce qui s'applique bien au 2 août 2026,
c'est la transparence sur les contenus générés, la littératie, et l'activation des pouvoirs de
sanction nationaux ([SmartForge](https://www.smartforge.fr/blog/ai-act-2-aout-2026-entreprise)) —
utile, mais pas de quoi déclencher un budget à six chiffres.

**Le vrai moteur réglementaire pour Crédit Logement n'est donc pas l'AI Act, c'est DORA**, applicable
et supervisé par l'ACPR ([ACPR](https://acpr.banque-france.fr/fr/reglementation/focus-sur-la-reglementation/transverse/digital-operational-resilience-act-dora)).
C'est un déplacement d'argumentaire, pas un affaiblissement : DORA est plus contraignant, plus
ancien, et parle le langage d'un DSI de banque.

> **Escalade au Juridique.** Le report de l'annexe III est un résultat de recherche web, pas une
> source officielle lue. Il modifie l'argumentaire de vente d'une offre. Je demande au Directeur
> Juridique de le confirmer sur EUR-Lex avant la présentation de fin août — il dispose du serveur
> MCP openlaw pour le faire. C'est une vérification, pas un arbitrage de Sam.

### 1.4 Le signal sectoriel le plus utile du dossier

**TD Bank a annoncé le 21 mai 2026 le lancement de son premier modèle d'IA agentique appliqué au
crédit immobilier garanti**, présenté comme la première étape d'une transformation complète de cette
activité par l'IA agentique
([TD, communiqué du 21/05/2026](https://td.fr.mediaroom.com/2026-05-21-La-TD-lance-lIA-agentique-pour-transformer-completement-le-credit-garanti-par-des-biens-immobiliers)).

C'est le métier exact de Crédit Logement, et c'est daté de moins de trois mois. Un pair international
a déjà franchi le pas sur leur cœur d'activité. C'est l'accroche la plus forte du dossier : elle ne
parle pas de nous, elle parle d'eux.

### 1.5 Ce que notre veille interne apporte — et ce qu'elle n'apporte pas

`v_deos_veille` contient **5 rapports, tous datés du 06/08/2026, tous construits sur les mêmes
2 articles**. Ils portent sur l'écosystème Salesforce (vagues de licenciements, coupes Trailhead,
« leadership émergent ») et concluent tous à la même opportunité : positionner Digital·Humans en
« faire plus avec moins ».

Utile pour DH. **Sans valeur pour DEOS** : la veille est branchée sur des flux Salesforce
(Salesforce Blog, Salesforce Ben), pas sur le marché de la gouvernance IA. Je le signale sans
demander d'outil : c'est un changement de flux RSS dans un workflow N8N qui existe déjà
(Veille Concurrence, DEC-2026-0806-18), pas une construction.

---

## 2. LE POSITIONNEMENT — contre quoi DEOS est-il comparé, et ce que ça coûte de se tromper

C'est le cœur de l'étude, parce que **le concurrent perçu détermine le prix acceptable**. Trois
comparaisons sont possibles dans la tête d'un DSI, et elles ne mènent pas au même ordre de grandeur.

### 2.1 Comparaison n° 1 — une prestation de conseil

C'est la comparaison par défaut si Sam se présente comme consultant, ce qu'il est.

Le marché français est mesurable. TJM médian d'un consultant Salesforce freelance à Paris en 2026 :
**730 €/jour**, contre 680 € en moyenne nationale
([TJMetre.fr](https://tjmetre.fr/tjm/consultant-salesforce/paris)). Par profil : **650 € pour un
fonctionnel confirmé, 800 € pour un technique senior, au-delà de 1 000 € pour un architecte
certifié** sur les modules de niche ; 15 à 25 % de moins via une ESN
([RH Solutions, étude TJM freelances IT 2026](https://www.rh-solutions.com/le-grand-guide-du-portage/tjm-freelance-tech/)).

Si DEOS est perçu comme du conseil, **son prix plafonne au nombre de jours qu'on peut y mettre**.
Un dispositif à 86 400 €/an devient « 108 jours de consultant », ce qu'aucun DSI ne signera pour un
outil. C'est la comparaison qui tue le prix.

### 2.2 Comparaison n° 2 — une plateforme de gouvernance IA

C'est la comparaison qu'il faut installer.

Ordres de grandeur publics, tous en tarification sur devis, aucun prix affiché :

| Éditeur | Fourchette annuelle | Source |
|---|---|---|
| IBM watsonx.governance, Credo AI, ModelOp | **100 000 – 500 000 $/an** | [Difinity.ai](https://difinity.ai/blog/best-ai-governance-platforms) |
| OneTrust, IBM OpenPages | **50 000 – 200 000 $/an** | [Difinity.ai](https://difinity.ai/blog/best-ai-governance-platforms) |
| Fourchette générale du segment | **25 000 – 200 000 $+/an** selon périmètre | [CloudZero](https://www.cloudzero.com/blog/ai-governance-tools/) |
| Plateformes d'entreprise en général | engagement annuel à six chiffres, prestation d'implémentation incluse | [Modulos](https://www.modulos.ai/best-ai-governance-platforms/) |

Sur le modèle de facturation, la tendance 2026 est nette et elle nous arrange : le marché s'éloigne
du siège pour aller vers l'agent, l'usage, la tâche accomplie ; **le modèle hybride — socle
prévisible plus part variable — est le choix le plus courant en entreprise en 2026**
([Kosmoy](https://www.kosmoy.com/resources/blog/best-ai-agent-governance-platforms-2026/)).

Dans cette comparaison, **une offre à 43–86 k€/an se situe sous le plancher du marché**. C'est
défendable comme « l'alternative accessible et européenne ». C'est aussi un risque de signal :
trop bas, on ne ressemble plus à la catégorie.

### 2.3 Comparaison n° 3 — un logiciel de pilotage interne

Un DSI peut aussi ranger DEOS à côté d'un outil de GRC ou d'un portail de suivi. C'est la
comparaison la plus dangereuse : elle mène à « on a déjà ça », et elle est fausse — aucun outil de
GRC ne règle le niveau d'autonomie d'un agent avant l'appel d'outil. Il faut la désamorcer tôt, en
montrant le refus journalisé plutôt qu'en l'expliquant.

### 2.4 Le positionnement que je recommande

> **DEOS est un dispositif de gouvernance d'agents, comparable aux plateformes d'AI TRiSM, opéré en
> Europe, sur un périmètre de direction plutôt que sur un parc de modèles.**

Trois raisons.

**Un.** C'est la comparaison qui autorise le prix le plus élevé et c'est la seule des trois où nous
sommes moins chers que la référence — donc la seule où le prix est un argument et non un obstacle.

**Deux.** La différenciation est réelle et tient en une phrase : les plateformes américaines
gouvernent des **modèles** (inventaire, dérive, biais) ; DEOS gouverne des **décisions et des
actions** (qui a le droit de faire quoi, à quel cran, avec quelle trace du refus). Un DSI de banque
comprend la différence immédiatement, parce que c'est celle entre un modèle et une délégation de
pouvoir.

**Trois.** C'est le positionnement qui rend le prix *indépendant du temps de Sam*. Tant que DEOS est
du conseil, la croissance est plafonnée par un homme seul. C'est le seul chemin qui ne l'est pas.

**Ce qui nous manque pour le tenir, et qu'il faut regarder en face :** aucune référence client, aucun
rapport d'analyste, aucun audit tiers. Face à un acheteur qui compare à IBM, notre seul actif est la
démonstration elle-même. D'où l'importance du §5.

---

## 3. LES DEUX APPROCHES DE TARIFICATION

### 3.1 Ce que le choix de modèle donne, avant de choisir un niveau

`pricing_model_picker.py`, profil `enterprise-software`, sur le contexte DEOS
(adoption descendante, valeur portée par la traçabilité et le contrôle, concurrents en devis) :

| Rang | Modèle | Score |
|---|---|---:|
| 1 | **Hybride** | **80/100** |
| 2 | Valeur | 60/100 |
| 3 | Abonnement au siège | 55/100 |
| 4 | À l'usage | 50/100 |
| 5 | Freemium | 10/100 |

Deux remarques du script méritent d'être citées telles quelles, parce qu'elles sont des mises en
garde et non des encouragements :

> *« Value signal present but no measurable driver — collapses to bad usage pricing. »*
> *« Top-down sale — freemium dilutes positioning without unlocking pipeline. »*

La première est la plus importante. **Nous ne pouvons pas vendre à la valeur, parce que nous ne
mesurons aucune valeur chez un client.** Nous n'avons pas de client. Facturer « à la valeur » sans
instrumentation, c'est facturer au doigt mouillé, et le canon du domaine le dit sans détour
(Campbell / ProfitWell, cité par le skill). Les deux approches ci-dessous facturent donc sur un
périmètre observable, pas sur un bénéfice affirmé.

La seconde condamne l'idée d'un « DEOS gratuit pour essayer ». Vente descendante à un DSI : le
gratuit abîme le positionnement sans ouvrir de pipeline.

### 3.2 Approche A — Abonnement au périmètre gouverné *(grille affichée recommandée)*

**Sur quoi on facture :** la **direction gouvernée**. Une direction, c'est un domaine dont on règle
le cran d'autonomie, dont on trace les décisions, et dont les refus sont journalisés. Chez nous il y
en a six. Chez un client, il en aura deux, quatre ou dix.

**Niveau proposé : 1 200 € par direction et par mois, minimum trois directions.**

| Périmètre | Mensuel | Annuel |
|---|---:|---:|
| 3 directions (socle minimum) | 3 600 € | **43 200 €** |
| 4 directions | 4 800 € | 57 600 € |
| 6 directions (périmètre DEOS complet) | 7 200 € | **86 400 €** |

**Ce qui la rend défendable.**

*L'unité de facturation est l'unité de gouvernance.* On facture ce qu'on règle. C'est vérifiable par
le client dans le produit — il compte ses lignes de curseur. La règle de Ramanujam (*Monetizing
Innovation*, erreur n° 1) est respectée : facturer au siège un produit dont la valeur ne dépend pas
du nombre d'utilisateurs plafonne le potentiel à environ 20 % du consentement à payer. Une
gouvernance ne se consomme pas par utilisateur.

*Le comparatif tient dans les deux sens.* Face à IBM ou Credo AI (100–500 k$/an), on est cinq à dix
fois moins cher : c'est un argument. Face au conseil, 86 400 € = 108 jours à 800 € : le DSI voit
qu'il achète l'équivalent d'un mi-temps senior permanent, pour une mission qu'aucun mi-temps ne peut
tenir la nuit et le week-end.

*Elle grandit avec le client sans renégociation.* Une direction de plus, c'est une ligne de plus.

**Ce qui la fragilise.** Le client peut réduire son périmètre déclaré pour payer moins et gouverner
quand même le reste « à la main ». Parade : le garde-fou technique ne s'applique qu'aux directions
sous contrat, et c'est visible.

### 3.3 Approche B — Socle + revue de gouvernance *(montage recommandé pour la première affaire)*

**Sur quoi on facture :** un forfait de dispositif, une prestation récurrente de revue, et une
installation.

| Ligne | Montant | Nature |
|---|---:|---|
| Socle DEOS (6 directions, curseurs, garde-fou, registre) | 30 000 €/an | récurrent |
| Revue trimestrielle de gouvernance animée par Sam (4 × 6 000 €) | 24 000 €/an | récurrent, prestation |
| Installation dans le SI du client (VPC ou sur site) | 25 000 € | une fois |
| **Année 1** | **79 000 €** | |
| **Année 2 et suivantes** | **54 000 €** | |

**Ce qui la rend défendable.** C'est le montage qui ressemble le plus à ce que Sam sait déjà vendre
et facturer. La revue trimestrielle est du conseil assumé, à un tarif cohérent avec le marché
(6 000 € pour environ 7 jours à ~850 €). Et l'installation **encaisse tôt** — ce qui, avec une
trésorerie déclarée à 0 € depuis le 14/07 (`deos_state.cash_suivi`), n'est pas un détail de forme.

**Ce qui la fragilise, et c'est sérieux.** Sur 79 000 € d'année 1, **49 000 € sont du temps de Sam**
(revue + installation). C'est un modèle de cabinet, pas d'éditeur : il ne se valorise pas, il ne se
délègue pas, et il ramène le §2.1 par la fenêtre. À terme, il replafonne DEOS au nombre de jours
disponibles.

### 3.4 Ce que la mise en paliers a révélé — et pourquoi je ne propose pas de Good/Better/Best

J'ai fait tourner `packaging_designer.py` sur dix fonctionnalités DEOS, profil `enterprise`, puis
une seconde fois en retirant les lignes de prestation lourde pour voir si l'équilibre changeait.

**Les deux fois, le même résultat** : les fonctions de gouvernance — curseur réglable, garde-fou,
journal d'audit, cloisonnement — se rangent toutes dans le palier haut. Le palier intermédiaire ne
retient qu'un tableau de bord. Et le script lève le même défaut les deux fois :

> *« No clear upgrade trigger Good → Better: Better-tier features have lower avg importance than
> Good. Why would a Good customer ever upgrade? »*

**Je ne vais pas contre ce résultat, je le prends comme un enseignement : DEOS ne se découpe pas.**
Il n'existe pas de « DEOS allégé » qu'un acheteur paierait puis quitterait pour monter en gamme,
parce que retirer le curseur gouverné ne laisse qu'un outil de reporting sans intérêt. Un palier bas
artificiel produirait exactement l'anti-modèle que le skill décrit : 70 % des clients prennent le
moins cher et n'en bougent jamais.

**Conséquence pratique** : une offre unique, un axe de périmètre (approche A), et deux options
facturées à part — l'installation dans le SI, et la revue trimestrielle. C'est plus simple à
défendre et plus honnête.

### 3.5 Projections à 6 et 12 mois

**Hypothèses, toutes déclarées, toutes discutables.**

- `H1` — Cycle de vente grand compte : **180 jours** depuis la présentation. C'est le chiffre que
  j'ai retenu au vu du segment ; je n'ai aucune mesure interne, notre pipeline n'a jamais rien
  signé. Présentation fin août 2026 → signature réaliste fin février 2027.
- `H2` — **Capacité de Sam : 120 jours par an** sur Digital·Humans et DEOS réunis. Le reste va à
  SH Conseil et au produit. Une affaire DEOS consomme **20 jours** (relation, sécurité, juridique,
  DPA, démonstration, comité).
- `H3` — **Coût d'un jour de Sam : 800 €**, retenu comme coût d'opportunité et non comme dépense —
  c'est ce qu'il ne facture pas ailleurs pendant qu'il vend. Référence marché : technique senior
  800 €/jour ([RH Solutions](https://www.rh-solutions.com/le-grand-guide-du-portage/tjm-freelance-tech/)).
- `H4` — Deux affaires DEOS closables sur 12 mois : Crédit Logement, plus une du réseau de Sam.
  Au-delà, la capacité `H2` sature.

**Approche A — 6 directions à 86 400 €/an**

| Horizon | Signatures | ARR | Encaissé | Jours de Sam |
|---|---:|---:|---:|---:|
| 6 mois (fin fév. 2027) | 0 à 1 | 0 – 86 400 € | 0 – 43 200 € | 25 |
| 12 mois (août 2027) | 2 | **172 800 €** | ~130 000 € | 40 à 55 |

**Approche B — 79 000 € en année 1**

| Horizon | Signatures | ARR récurrent | Encaissé | Jours de Sam |
|---|---:|---:|---:|---:|
| 6 mois (fin fév. 2027) | 0 à 1 | 0 – 54 000 € | 0 – 55 000 € | 30 |
| 12 mois (août 2027) | 2 | **108 000 €** | ~158 000 € | 65 à 80 |

**La lecture croisée, qui est le vrai résultat.** L'approche A produit **60 % d'ARR récurrent en
plus**. L'approche B produit **20 % d'encaissement en plus la première année**, et consomme
**25 jours de Sam de plus** — soit, au coût d'opportunité de `H3`, 20 000 € de conseil non facturé
ailleurs. B encaisse mieux tout de suite et coûte plus cher en réalité.

**Mise en perspective sur l'OKR O1** (`deos_state.okr_h2` : 11 clients signés au 31/12 dont 3 Team,
MRR ≥ 4 800 €) : **un seul client DEOS à 86 400 €/an représente 7 200 € de MRR, soit 150 % de la
cible MRR de l'OKR à lui seul.** Un client DEOS pèse 4,8 clients Team. Ce n'est pas une raison de
tout miser dessus — c'en est une de ne pas le traiter comme un dossier secondaire.

---

## 4. L'ARTICULATION AVEC DIGITAL·HUMANS — franchement

### 4.1 La cannibalisation du chiffre d'affaires n'existe pas

Les segments ne se recouvrent pas. Digital·Humans est **gaté par Salesforce** et vendu à l'ETI par
un décideur unique, à 1 490 €/mois. DEOS n'est pas gaté et vendu au DSI d'un établissement supervisé,
à 43–86 k€/an. **Facteur cinq sur le prix, acheteurs différents, cycles différents.** Un client Team
ne « monte » pas vers DEOS et un prospect DEOS ne se rabat pas sur Team.

### 4.2 La cannibalisation réelle porte sur le temps de Sam — et elle est mesurable

J'ai chargé les trois canaux dans `cost_to_serve_calculator.py`, avec une méthode d'imputation
**identique pour les trois** (10 % de frais généraux, coût du jour de Sam à 800 €) — la constance
d'imputation étant, d'après le skill, la condition sans laquelle toute comparaison entre canaux est
contaminée (Horngren, *Cost Accounting*).

| Canal | Volume 12 mois | Revenu | Coût chargé | Coût par affaire | **Marge brute réelle** |
|---|---:|---:|---:|---:|---:|
| Pro en libre-service (49 €/mois) | 60 abonnés | 35 280 € | 31 728 € | 529 € | **10,1 %** |
| Team en direct (1 490 €/mois) | 6 clients | 107 280 € | 49 128 € | 8 188 € | **54,2 %** |
| DEOS grands comptes (86 400 €/an) | 2 clients | 172 800 € | 74 480 € | 37 240 € | **56,9 %** |

Puis `channel_roi_analyzer.py` sur les mêmes chiffres :

| Canal | ROI cash an 1 | ROI à vie | Verdict du script |
|---|---:|---:|---|
| Pro (60 abonnés) | 1,11x | 3,89x | **MAINTAIN** |
| Team | 2,18x | 7,64x | **DOUBLE-DOWN** |
| DEOS à 30 k€/compte | 0,95x | 4,75x | MAINTAIN |
| DEOS à 50 k€/compte | 1,49x | 7,44x | DOUBLE-DOWN |
| **DEOS à 80 k€/compte** | **2,19x** | **10,93x** | **DOUBLE-DOWN** |
| DEOS à 120 k€/compte | 2,96x | 14,78x | DOUBLE-DOWN |

**Deux seuils tombent, et ils se confirment par deux méthodes indépendantes.**

**31 800 €/compte/an — le plancher.** En dessous, le canal DEOS détruit de la valeur : Sam gagnerait
davantage à facturer les mêmes jours chez SH Conseil. Calculé par la marge (57 200 € de coûts
directs / 0,9), confirmé par le ROI (0,95x à 30 k€).

**79 400 €/compte/an — la parité avec le canal Team.** C'est le niveau auquel un compte DEOS rapporte
autant qu'un client Team pour un jour de Sam équivalent. Calculé par la marge (57 200 / 0,36),
confirmé par le ROI (2,19x à 80 k€, contre 2,18x pour Team).

**C'est ce qui fonde le niveau de 1 200 €/direction/mois de l'approche A** : à six directions, elle
tombe à 86 400 €, juste au-dessus du seuil de parité. Le prix n'est pas choisi, il est déduit.

### 4.3 Ce que le résultat sur le Pro oblige à dire

Le canal Pro affiche **10,1 % de marge et échoue au seuil LTV/CAC (0,38x, retour sur investissement
en 107 mois)** — à 60 abonnés. La raison n'est pas le prix de 49 €, c'est que la production de
contenu (30 jours de Sam par an, 24 000 €) est un **coût fixe** que 60 abonnés ne couvrent pas.

J'ai fait varier le nombre d'abonnés :

| Abonnés payants | Marge | Coût d'acquisition | Retour | LTV/CAC | Seuil |
|---:|---:|---:|---:|---:|---|
| 60 | 10,1 % | 529 € | 107 mois | 0,38x | **ÉCHEC** |
| 100 | 42,0 % | 341 € | 16,5 mois | 2,47x | **ÉCHEC** |
| **150** | **58,0 %** | **247 €** | **8,7 mois** | **4,70x** | **PASSE** |
| 300 | 74,0 % | 153 € | 4,2 mois | 9,68x | PASSE |
| 500 | 80,4 % | 115 € | 2,9 mois | 13,95x | PASSE |

**La position arbitrée — « le Pro est le moteur de trésorerie » — tient, et je ne la renverse pas.
Mais elle a un seuil, et il vaut environ 150 abonnés payants.** En dessous de 120, le Pro consomme
la trésorerie qu'il est censé produire. Ce n'est pas un désaccord, c'est un chiffre à ajouter à la
décision : le moteur de trésorerie devient un moteur au troisième mois après le lancement, pas au
premier.

### 4.4 L'optimiseur de mix dit 100 % DEOS. Je ne le recommande pas, et voici pourquoi

`channel_mix_optimizer.py` recommande **100 % DEOS, 0 % Team, 0 % Pro**, et le maintient dans les
trois scénarios de sensibilité (coût d'acquisition +20 %, remise partenaire +5 pts, rétention
−3 pts).

Je rapporte le résultat, je ne le suis pas. L'optimiseur maximise le LTV/CAC pondéré et **ne porte
trois choses qu'aucune formule ne connaît** :

1. **Le calendrier de trésorerie.** Cycle DEOS à 180 jours, trésorerie déclarée à 0 € depuis le
   14/07. Un mix 100 % DEOS, c'est six mois sans encaissement.
2. **La capacité.** 120 jours par an. Trois affaires DEOS en consomment 60 : le modèle n'a pas de
   contrainte de ressource, Sam si.
3. **Le risque produit.** DEOS a zéro client, zéro référence, zéro installation chez un tiers. Le
   modèle traite un canal prouvé et un canal hypothétique de la même façon.

**Le mix que je recommande** : Team reste le canal de trésorerie court (payback 10 mois, verdict
DOUBLE-DOWN, produit qui existe), Pro reste le canal de volume à monter jusqu'à son seuil de 150,
DEOS est traité comme **une affaire à la fois, avec un plafond de 40 jours de Sam par an** — soit
deux affaires. Au-delà, il faut un second porteur, et c'est une autre décision.

### 4.5 Le sens de la porte

**DEOS → DH : oui.** Un client DEOS qui utilise Salesforce est un client Team naturel — le dispositif
est déjà installé, les curseurs sont déjà réglés, il ne reste qu'à brancher la chaîne de delivery.
C'est la seule séquence d'expansion crédible que je voie.

**DH → DEOS : non.** L'acheteur Team est un dirigeant de PME ou d'ETI. Il n'a pas de comité de
direction à gouverner ni de contrôle ACPR à passer. Lui vendre DEOS n'a pas de sens.

**Ce que je ne sais pas et qui conditionne tout ça pour Crédit Logement : sont-ils sur Salesforce ?**
Ils ne figurent ni dans les 29 utilisateurs Salesforce identifiés de `v_deos_signaux`, ni dans les
37 comptes du portefeuille historique de Sam. **Sans Salesforce, DEOS ne rouvre aucune porte vers
Digital·Humans chez eux** — c'est une vente autonome, à traiter comme telle. Sam sait la réponse, je
ne l'ai pas : c'est une question de deux minutes, pas un arbitrage.

### 4.6 Sur le mode supervision — il ne faut pas le vendre, et DEOS n'en a pas besoin

La demande initiale (DEC-2026-0805-01) prévoyait un « mode supervision » grands comptes, dont le CEO
a noté qu'il rouvrirait la frontière « Team s'arrête avant la production ».

**Cette frontière a été refermée à clé le 08/08 : DEC-2026-0808-07, « RÈGLE ABSOLUE — AUCUN
DÉPLOIEMENT EN PRODUCTION », posée par Sam ce jour même.** Le mode supervision tel qu'il était
esquissé le 05/08 est donc incompatible avec une règle postérieure de trois jours.

**La bonne nouvelle, et elle est structurelle : DEOS n'a pas besoin de cette frontière.** DEOS
gouverne des décisions et des délégations, il ne déploie rien chez le client. Le point d'escalade que
j'avais ouvert au Juridique le 07/08 sur ce sujet devient sans objet pour DEOS — il reste ouvert pour
Digital·Humans, où il porte sur autre chose.

Je retire donc le mode supervision du périmètre de cette étude, et je le dis explicitement pour que
personne ne le reprenne dans un document commercial.

---

## 5. CE QUE ÇA IMPLIQUE POUR CRÉDIT LOGEMENT

### 5.1 Le fait qui change la nature de la présentation

`DEC-2026-0806-14` posait un prérequis bloquant, daté du 06/08 :

> *« le curseur d'autonomie — cœur du concept DEOS — n'existe aujourd'hui que comme TEXTE dans les
> prompts des directions. Aucune valeur en base, aucune colonne, rien dans le tableau de bord, et pas
> de réglage par type de tâche contrairement au principe fondateur. […] indémontrable devant un DSI. »*

**Ce prérequis est levé.** Vérifié ce jour, en base et sur le disque :

- **Table `curseurs` : 36 lignes**, soit six directions × six types de tâche (`observer`,
  `ecrire_base`, `agir_production`, `envoyer_externe`, `engager_depense`, `modifier_dispositif`).
  Chaque ligne porte son niveau, sa justification, son code de règle, son auteur, sa date, et pour
  certaines un canal imposé et une évolution prévue.
  *(`psql "$COMITE_DB_DSN" -c "SELECT * FROM curseurs"`, 08/08/2026.)*
- **Le réglage par type de tâche existe** — c'était précisément ce que la décision signalait comme
  manquant. Le Chief of Staff est à 4 sur `ecrire_base` mais à 1 sur `agir_production` ; le
  Commercial est à 4 sur `observer` et à 2 sur `envoyer_externe`. Ce n'est pas un niveau global par
  agent, c'est une matrice.
- **Le Directeur Juridique a bien ses six curseurs** — la décision notait qu'il n'en avait aucun.
- **Le garde-fou lit la base, pas le script.** `.claude/hooks/pretooluse-guard.sh` recharge les
  curseurs depuis PostgreSQL toutes les 60 secondes : *« Avant : les règles étaient FIGÉES dans ce
  script »*. Un changement de curseur prend effet en moins d'une minute, sans redéploiement.
- **Les refus sont journalisés.** `hooks.log`, 427 lignes. Dernier refus tracé le **08/08 à
  07:26:34** : `CURSEUR-DENY [Bash] marketing/engager_depense regle=2 requis=3`, avec la commande
  refusée en clair.
- **Le défaut est restrictif** : une direction sans curseur déclaré tombe au niveau 1, le plus
  fermé. C'est un choix de conception, commenté dans le code, et c'est exactement ce qu'un auditeur
  vient chercher.

**Ce qui se démontre fin août n'est donc plus un concept, c'est un dispositif qui refuse et qui
laisse une trace.** C'est notre seul actif produit face à IBM, et il est meilleur que ce que la
décision du 06/08 laissait croire.

> **À rapporter tel quel :** je ne peux pas mettre à jour `DEC-2026-0806-14` — mon curseur
> `ecrire_base` est réglé sur 2, et seuls le CoS, le CEO ou Sam changent un statut. Je demande au
> **Chief of Staff** de porter la levée de ce prérequis au registre, avec pour preuve les six
> vérifications ci-dessus. Ce n'est pas un arbitrage de Sam.

### 5.2 Ce qu'on vend le jour J — et ce qu'on ne vend pas

**On vend une démonstration et un cadrage. Pas une licence.**

Nous avons zéro client, zéro référence, zéro installation chez un tiers. Vendre une licence à un DSI
de banque dans ces conditions, c'est perdre la réunion suivante. Ce qu'on peut tenir, en revanche,
c'est ceci :

**La démonstration, en trois gestes, dans cet ordre.**

1. **Le registre.** Une décision, son origine, sa date, son statut, sa preuve de clôture. Le langage
   d'un contrôle interne.
2. **Le curseur.** La matrice à 36 lignes, à l'écran. On change un cran devant eux.
3. **Le refus.** On demande à une direction de faire ce que son curseur interdit. Le dispositif
   refuse, et la ligne apparaît dans le journal, horodatée. **C'est le moment de la démonstration.**
   Tout le reste est du contexte.

**L'accroche qui ouvre la réunion** n'est pas notre produit, c'est leur métier : TD Bank a lancé le
21 mai 2026 son premier modèle d'IA agentique sur le crédit immobilier garanti, en annonçant vouloir
transformer complètement cette activité
([communiqué TD](https://td.fr.mediaroom.com/2026-05-21-La-TD-lance-lIA-agentique-pour-transformer-completement-le-credit-garanti-par-des-biens-immobiliers)).
Puis la question : *quand vos agents commenceront à décider, qu'est-ce qui les arrête, et qu'est-ce
qui le prouve ?*

**Le cadre réglementaire qu'on invoque** est DORA, pas l'AI Act — traçabilité exhaustive des
décisions, cartographie des actifs TIC critiques (art. 8), supervision ACPR
([Haas Avocats](https://www.haas-avocats.com/cybersecurite/dora-2026-cybersecurite-et-gouvernance-bancaire/) ·
[ACPR](https://acpr.banque-france.fr/fr/reglementation/focus-sur-la-reglementation/transverse/digital-operational-resilience-act-dora)).
Si un interlocuteur mentionne l'échéance AI Act du 2 août 2026, ne pas surenchérir : l'annexe III
« haut risque » a été repoussée à décembre 2027 (§1.3), et se faire reprendre sur ce point devant un
DSI de banque coûterait plus cher que le point ne rapporte.

**Ce qu'on ne promet à aucun moment** — DH-CRO-004, liste fermée : tableau de bord de gouvernance
côté client (n'existe pas), journal d'audit exportable (n'existe pas comme livrable), installation
dans un SI tiers (jamais faite), toute référence client (nous n'en avons aucune), tout SLA, tout
déploiement en production (DEC-2026-0808-07), tout mode supervision (§4.6).

### 5.3 Le prix, si la question tombe — et elle tombera

**Ne pas donner de prix ferme.** Aucun des niveaux de cette étude n'est validé (DH-CRO-002) et un
prix lâché sans périmètre devient le plafond de toute la négociation.

**Donner une fourchette de cadrage, et une seule phrase :**

> « Un dispositif de ce type se situe entre 40 et 90 000 € par an selon le nombre de directions
> gouvernées. Pour référence, les plateformes américaines de gouvernance IA se négocient entre 100
> et 500 000 $ par an. Le périmètre exact, c'est ce qu'un cadrage détermine. »

Cette phrase fait trois choses : elle ancre sur la bonne catégorie (§2.2), elle annonce l'ordre de
grandeur sans l'engager, et elle enchaîne naturellement sur ce qui suit.

**Puis proposer le cadrage payant : 8 000 €, cinq à dix jours, facturé par SH Conseil.**

Livrable : la cartographie des décisions et actions qu'ils envisagent de déléguer à des agents, le
réglage des curseurs qui en découle, et le périmètre chiffré du dispositif. C'est ce qui transforme
une présentation en affaire : ça encaisse tout de suite, ça engage sans contrat cadre, ça produit
le périmètre dont l'approche A a besoin — et ça donne **notre premier point de mesure du
consentement à payer**, celui qui nous manque depuis le début de cette étude (§0).

C'est aussi la seule proposition compatible avec le fait que **Sam part en congés après la
présentation**. Un cadrage se cale à son retour ; une négociation de licence qui s'ouvre la veille
d'un départ meurt pendant l'absence.

### 5.4 Le montage — l'économie confirme la recommandation du CEO

Le CEO recommande dans le brief du 08/08 : *SH Conseil pour la présentation, Digital·Humans pour la
suite si elle se concrétise.* L'analyse de canal le confirme, pour une raison qui lui est propre :

**le cadrage payant est une prestation de jours, et une prestation de jours se facture par
SH Conseil.** La passer par Digital·Humans engagerait la marque produit sur un revenu de conseil, ce
qui est précisément le positionnement à éviter (§2.1). Le basculement vers Digital·Humans se fait au
moment où l'on vend un abonnement — c'est-à-dire quand on vend le produit.

Le seul actif réel de ce dossier est que le DSI connaît Sam personnellement. Cet actif appartient à
SH Conseil.

---

## 6. CE QUE JE FAIS ENSUITE, SANS ATTENDRE PERSONNE

1. **Le dossier de démonstration Crédit Logement**, sur l'ossature déjà produite le 07/08, avec le
   déroulé en trois gestes du §5.2, l'accroche TD Bank, le bloc `verification_produit`, et une page
   de réponses aux objections prévisibles (« on a déjà une gouvernance », « pourquoi pas IBM »,
   « qui vous audite »). Prêt lundi 10/08.
2. **Une note d'une page pour la phrase de prix** (§5.3), à valider par Sam avant le jour J — c'est
   la seule ligne de la présentation qui touche DH-CRO-002.
3. **Le brouillon de proposition de cadrage à 8 000 €**, prêt à partir le lendemain de la
   présentation. Je ne l'envoie pas : mon curseur `envoyer_externe` est à 2.
4. **La question du Salesforce chez Crédit Logement** (§4.5), posée à Sam en une ligne dans mon
   prochain rapport — pas en demande d'arbitrage.

---

## 7. LES DEUX SEULES CHOSES QUE JE DEMANDE À SAM

Tout le reste de ce document est produit, pas demandé.

**1. Valider ou corriger la grille de l'approche A** — 1 200 €/direction/mois, minimum trois
directions, fourchette 43–86 k€/an — et la phrase de cadrage du §5.3.
*Pourquoi c'est bloquant :* DH-CRO-002. Aucun prix hors offre canonique ne sort de ma bouche sans son
arbitrage, et la question du prix tombera en réunion. *Coût :* 15 minutes. *Coût de l'inaction :* la
meilleure opportunité du portefeuille (9/10) se présente sans réponse à la seule question qui compte.

**2. Confirmer le plafond de 40 jours de Sam par an sur le canal DEOS** (§4.4).
*Pourquoi c'est bloquant :* c'est l'hypothèse `H2`, elle porte toutes les projections du §3.5, et
elle décide de ce que le Commercial prépare — deux affaires ou une file. Sam est le seul à savoir
combien de jours il peut réellement y mettre. *Coût :* 5 minutes.

**Ce que je ne demande pas** : ni source de prospects (elle existe), ni outil (la veille se rebranche
sur d'autres flux RSS dans un workflow qui tourne déjà), ni décision sur le montage Crédit Logement
(déjà ouverte en DEC-2026-0806-14, la recommandation du CEO est bonne et je la confirme), ni le
mode supervision (retiré du périmètre, §4.6).

**Deux escalades qui ne vont pas à Sam** : au **Juridique**, la confirmation du report de l'annexe III
de l'AI Act sur source officielle (§1.3) ; au **Chief of Staff**, l'inscription au registre de la
levée du prérequis de DEC-2026-0806-14 (§5.1).

---

## Sources

**Vérifications internes du 08/08/2026** — `curseurs` (36 lignes, `$COMITE_DB_DSN`) ·
`decisions` (DEC-2026-0805-01, 0806-09, 0806-14, 0808-03, 0808-07) · `deos_state`
(`okr_h2`, `objectifs_commerciaux`, `cash_suivi`, `pipeline_commercial`) · `v_deos_signaux`
(112 signaux, dont 37 du portefeuille historique de Sam et 29 utilisateurs Salesforce identifiés) ·
`v_deos_veille` (5 rapports, 06/08) · `v_deos_projects` (79 projets : 54 Sales Cloud, 19 Service
Cloud) · `.claude/hooks/pretooluse-guard.sh` · `hooks.log` (427 lignes) ·
`config/offre_dh.md` · `config/commercial/strategie_approche.md` · `config/outils_disponibles.md`.

**Outils** — `pricing-strategist` (`pricing_model_picker.py`, `packaging_designer.py`,
`wtp_analyzer.py`) et `channel-economics` (`cost_to_serve_calculator.py`,
`channel_roi_analyzer.py`, `channel_mix_optimizer.py`), installés le 08/08. Jeux d'entrée conservés
dans `/workspace/tmp/`.

**Sources publiques**
- [La Revue Tech — Gartner : +63 % pour les modèles et plateformes d'IA en 2026, la bataille se joue sur la gouvernance](https://larevuetech.fr/gartner-prevoit-63-pour-les-modeles-et-plateformes-dia-en-2026-la-bataille-se-joue-sur-la-gouvernance/)
- [OpsIn Security — Gartner Market Guide for Guardian Agents](https://www.opsinsecurity.com/blog/gartner-market-guide-guardian-agents)
- [Difinity.ai — Best AI Governance Platforms in 2026: An Enterprise Buyer's Guide](https://difinity.ai/blog/best-ai-governance-platforms)
- [CloudZero — Best AI Governance Tools In 2026: Compliance, Security, and Cost](https://www.cloudzero.com/blog/ai-governance-tools/)
- [Modulos — AI governance tools: the 2026 enterprise buyer's guide](https://www.modulos.ai/best-ai-governance-platforms/)
- [Kosmoy — Best AI Agent Governance Platforms in 2026](https://www.kosmoy.com/resources/blog/best-ai-agent-governance-platforms-2026/)
- [TJMetre.fr — TJM Consultant Salesforce à Paris](https://tjmetre.fr/tjm/consultant-salesforce/paris)
- [RH Solutions — TJM des freelances IT & Tech : étude 2026](https://www.rh-solutions.com/le-grand-guide-du-portage/tjm-freelance-tech/)
- [SmartForge — AI Act au 2 août 2026 : ce qui s'applique vraiment à votre entreprise](https://www.smartforge.fr/blog/ai-act-2-aout-2026-entreprise)
- [mdp-data — AI Act 2026 : obligations des systèmes IA à haut risque](https://mdp-data.com/ai-act-systemes-ia-haut-risque-aout-2026/)
- [ACPR — Digital Operational Resilience Act (DORA)](https://acpr.banque-france.fr/fr/reglementation/focus-sur-la-reglementation/transverse/digital-operational-resilience-act-dora)
- [Haas Avocats — DORA 2026 : cybersécurité et gouvernance bancaire](https://www.haas-avocats.com/cybersecurite/dora-2026-cybersecurite-et-gouvernance-bancaire/)
- [TD — La TD lance l'IA agentique pour transformer complètement le crédit garanti par des biens immobiliers (21/05/2026)](https://td.fr.mediaroom.com/2026-05-21-La-TD-lance-lIA-agentique-pour-transformer-completement-le-credit-garanti-par-des-biens-immobiliers)
- [Crédit Logement — Rapport annuel 2025](https://www.creditlogement.fr/entreprise/rapport-annuel-2025/) (plus de 365 000 prêts garantis en 2025)
