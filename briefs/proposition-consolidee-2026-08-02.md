# PROPOSITION CONSOLIDÉE — 2026-08-02

```json
{
  "type": "proposition_consolidee",
  "date": "2026-08-02",
  "auteur": "ceo",
  "sante": {
    "score": 60,
    "statut": "ambre (plafonné)",
    "tendance": "baisse vs 73 le 16/07 — dernier point comparable avant la panne",
    "calcul": "Delivery 88×0,30 + Commercial 33×0,25 + Marketing 40×0,15 + Exécution/CoS 70×0,10 = 47,65 ; CS sans score calculable (0 compte client réel, mode dégradé confirmé par Sam) → recalcul sur poids restants Σ=0,80 : 47,65/0,80 = 59,6 ≈ 60 [DH-CEO-003]. Statut plafonné à ambre (un domaine sans score exploitable). Sources : rapport_delivery#2026-08-02T07:04Z (88), rapport_commercial#2026-08-02T13:25Z (33), rapport_marketing#2026-08-02T13:21Z (40), rapport_cos#2026-08-02T13:22Z (70), rapport_cs#2026-08-02T13:20Z (non calculable)."
  },
  "domaines_manquants": [],
  "plans_recus": ["cos", "commercial", "cs", "marketing"],
  "plans_manquants": [
    {"domaine": "delivery", "constat": "aucun fichier directeur-delivery-2026-08-02-plan.json dans /workspace/rondes/ (vérifié 2026-08-02) ; seul le RapportDirecteur quotidien de 07:04 existe. Le plan Delivery n'a jamais été lancé ou a échoué sans trace.", "gravite": "haute"}
  ],
  "incident_gouvernance": {
    "periode": "2026-07-16 → 2026-08-01",
    "cause": "crédits API épuisés — 'Credit balance is too low' sur toutes les tentatives de rondes (fichiers /workspace/rondes/*-2026-07-{17..31}.json)",
    "impact": "4 domaines sur 5 aveugles pendant 17 jours ; 0 relance de décision émise ; 6 décisions gelées à 17-19 jours",
    "remediation": "commit 16431d9 (alerte Telegram post-rondes indépendante de l'API + règle CEO >48h + escalade 2 domaines) — en place, jamais éprouvée en conditions réelles",
    "residuel": "la cause racine (solde de crédits API) reste invisible au comité (rapport_cos 2026-08-02)"
  },
  "alertes": [
    {"gravite": "haute", "texte": "Aucun plan de département Delivery : l'OKR O2 (produit prêt au 31/08 — 6 bugs clos, RAG v2, Stripe prod, Postmark) n'est porté par aucun plan à J-29 du jalon. Personne ne mentionne Stripe prod dans les 4 plans reçus.", "source": "okr_h2#O2 ; /workspace/rondes/ 2026-08-02 ; lecture des 4 plans"},
    {"gravite": "haute", "texte": "Échec systémique BUILD phase 1 (data_model/raj, 3/3, 0 succès historique) non diagnostiqué depuis 17j ; bloque la preuve du tier Team dont dépendent 3 plans (commercial, marketing, CS). Diagnostic bloqué par DEC-2026-0716-07 (attente_sam, 17j).", "source": "rapport_delivery#2026-08-02 ; deos-decisions list#2026-08-02"},
    {"gravite": "haute", "texte": "Pipeline commercial vide (0 entrée, 7 stades) à J-30 du régime B, verrouillé par DEC-2026-0716-01/02 (19j sans arbitrage).", "source": "rapport_commercial#2026-08-02 ; pipeline_commercial (inchangé depuis le 14/07)"},
    {"gravite": "moyenne", "texte": "Échéance marketing rang 3 (portrait Sophie) : cible 04/08, J-2, décision DEC-2026-0716-04 toujours attente_sam (17-18j). Chaque semaine de blocage décale mécaniquement les rangs 4-13.", "source": "rapport_marketing#2026-08-02 ; calendrier_editorial"},
    {"gravite": "moyenne", "texte": "cash_suivi : seuil_alerte_solde null et echeances_connues vides depuis 19j (DEC-2026-0716-03) ; aucune alerte cash déclenchable, et le solde de crédits API — cause de l'incident — n'est suivi nulle part.", "source": "deos-state get cash_suivi#2026-08-02 ; rapport_cos#2026-08-02"}
  ],
  "decisions_attendues_sam": [
    {"rang": 1, "id": "DEC-2026-0716-07 + 06", "objet": "Débloquer le diagnostic BUILD (accès lecture logs worker + RapportIncident)", "echeance_externe": "démo Team 15/08"},
    {"rang": 2, "id": "NOUVELLE", "objet": "Commander au Directeur Delivery son plan de département + un statut O2 complet (6 bugs, RAG v2, Stripe prod, Postmark) sous 48h"},
    {"rang": 3, "id": "DEC-2026-0716-01 + 02", "objet": "Source de comptes cibles + branchement lecture concierge Sophie ; valider l'ICP proposé"},
    {"rang": 4, "id": "NOUVELLE", "objet": "Position tier Team si BUILD non prouvé au 15/08 (vendre en mode dégradé documenté / retarder l'onboarding Team)"},
    {"rang": 5, "id": "DEC-2026-0716-04 + 05", "objet": "Valider portrait Sophie (échéance 04/08) + cadrage livre blanc"},
    {"rang": 6, "id": "DEC-2026-0716-03 étendue", "objet": "Seuil d'alerte cash + mise sous surveillance du solde de crédits API", "porte": "SMTP-PROD-001 : fixer aussi une date (canal tickets CS)"},
    {"rang": 7, "id": "NOUVELLE (paquet gouvernance)", "objet": "Amendements d'objectifs proposés par les directeurs + mandat priorites_semaine + espaces fichiers par domaine + clôture DEC-2026-0714-01"}
  ]
}
```

---

## 1. Où nous en sommes réellement

**Le comité a été muet du 16/07 au 01/08 — 16 jours. C'est un incident de gouvernance, et je l'assume.** Toutes les rondes ont échoué sur épuisement des crédits API (« Credit balance is too low », tracé fichier par fichier dans `/workspace/rondes/`, 11 à 15 tentatives par directeur). Pendant que le comité était aveugle, le calendrier a continué de tourner : les 6 décisions ouvertes le 16/07 ont vieilli jusqu'à 17-19 jours sans une seule relance, deux jalons commerciaux sont arrivés à J-13 avec 0 % d'avancement, et l'échéance du portrait Sophie est maintenant à J-2. Le dispositif de détection n'existait pas ; il existe depuis hier (commit `16431d9` : alerte Telegram indépendante de l'API, règle CEO >48h, escalade à 2 domaines muets) mais **n'a jamais été éprouvé en réel**, et la cause racine — le solde de crédits API — reste invisible au comité (constat CoS du jour).

**Aujourd'hui, les cinq directeurs ont reporté** (première couverture complète depuis le 16/07). Santé globale : **60/100, ambre plafonné**, en baisse contre 73 le 16/07. Détail : Delivery 88 (vert), Exécution/CoS 70 (ambre), Marketing 40 (rouge), Commercial 33 (rouge), CS non calculable (0 client réel — état attendu, confirmé par Sam). Lecture honnête de ces chiffres : le 88 du Delivery mesure la stabilité de la plateforme, pas la readiness du lancement — l'incident BUILD systémique y vaut -12 points seulement alors qu'il conditionne le tier Team ; à l'inverse, les rouges Commercial et Marketing traduisent surtout des blocages d'arbitrage, pas une mauvaise exécution.

**Quatre plans de département sur cinq ont été produits — pas cinq.** Le plan Delivery n'existe nulle part (aucun fichier `directeur-delivery-2026-08-02-plan.json`, vérifié ce jour) ; seul son rapport quotidien de 07:04 est disponible. Je ne comble pas ce silence : la section Delivery ci-dessous est reconstituée depuis son rapport du jour et je demande le plan manquant sous 48h. C'est d'autant plus grave que **l'OKR O2 — « produit prêt au 31/08 : 6 bugs clos, RAG v2, Stripe prod, Postmark » — n'est porté par aucun des 4 plans reçus**. Personne ne mentionne Stripe. À J-29 du jalon, c'est le plus gros trou de la consolidation.

---

## 2. La proposition d'ensemble : d'ici au lancement du 01/09

Une phrase : **août sert à transformer un produit instable sur son haut de gamme et un entonnoir commercial vide en un lancement crédible — en prouvant avant de promettre, et en ne dépensant rien qui ne soit débloqué par une décision déjà nécessaire.**

Quatre lignes de force, dans l'ordre :

1. **Prouver le produit (03-15/08).** Diagnostiquer l'échec BUILD (la seule chose qui sépare le tier Team à 1 490 €/mois d'une promesse invérifiable), obtenir le statut O2 complet du Delivery, et poser un **checkpoint go/no-go le 15/08** : si le SANDBOX n'est pas prouvé à cette date, toute la communication et l'offre de septembre basculent sur le périmètre SDS prouvé (tier Pro), sans surpromesse — les trois directeurs concernés ont déjà, indépendamment, prévu ce repli.
2. **Remplir l'amont commercial (dès déblocage DEC-01/02).** Réseau de Sam d'abord (coût nul), concierge Sophie en lecture, ICP validé, trames de proposition et de démo livrées au 15/08, bibliothèque de cas d'usage à 15/15 au 31/08.
3. **Construire la vitrine et l'accueil (tout août, indépendant des blocages).** Marketing : dérouler les portraits SDS (rangs 3-6) et cadrer le livre blanc sur ce qui est prouvé. CS : kit d'onboarding, base de connaissances, schéma tickets — testés à blanc en S4.
4. **Blinder la gouvernance (S1).** Preuve réelle du dispositif Telegram, auto-diagnostic en début de ronde CoS, surveillance du solde de crédits API, seuil cash. Le comité ne doit plus jamais mettre 16 jours à savoir qu'il est en panne.

Le budget est serré et Sam est seul : cette proposition ne demande **aucune dépense nouvelle avant le 15/08** (tout est coût nul ou déjà engagé), et concentre l'effort de Sam sur **une passe d'arbitrage de ~30 minutes** en début de semaine.

---

## 3. Le plan par domaine, condensé

**Delivery** *(source : rapport du jour uniquement — plan manquant)* — La plateforme est saine (health 200, 0 exécution bloquée) mais inactive depuis 18 jours, et l'échec BUILD phase 1 (data_model/raj) est à 3/3 sans jamais un succès, non diagnostiqué faute d'accès aux logs du worker (DEC-07) et sans RapportIncident (DEC-06, `en_execution` sans livrable depuis 17j). Couverture des logs backend : 0 % de la fenêtre 24h, en régression. **En tant que CEO : je ne retiens rien — il n'y a rien à retenir, c'est le problème.** Je demande le plan de département et le statut O2 (6 bugs, RAG v2, Stripe prod, Postmark) sous 48h, et je fais du diagnostic BUILD la priorité produit unique jusqu'au 15/08.

**Commercial** *(score 33, rouge)* — Propose : trames proposition + démo pour le 15/08 (priorité immédiate, 0 % à J-13), bibliothèque 15/15 au 31/08 (8/15 ce jour, rythme 3/sem tenable), ICP complet + fichier de prospects RGPD prêt à peupler, remplacement du KPI « comptes cibles 5/sem » (à 0 depuis 19j faute de source) par un objectif de préparation, et un sous-objectif d'entrée d'entonnoir pour le régime B. **Je retiens tout, avec un amendement : la volumétrie « 40-60 comptes qualifiés en stock au 01/09 » est irréaliste** — elle suppose une source validée immédiatement plus un outil de recherche web qui n'existe pas ; avec le réseau de Sam seul, 20-30 est l'hypothèse honnête. Le plan lui-même marque d'ailleurs ses taux de conversion comme non vérifiés.

**Marketing** *(score 40, rouge)* — Propose : débloquer et publier le rang 3 (portrait Sophie) dès validation, puis rangs 4-6 (Olivia, Emma, Marcus — le pipeline SDS prouvé) à cadence hebdo, cadrage livre blanc au 15/08 ancré sur le SDS, setup SEO minimal (pas de cible chiffrée sans baseline), et **conditionner les portraits BUILD (rangs 7-10) à une preuve SANDBOX réelle**. Ne touche pas à O3. **Je retiens tout, y compris et surtout la conditionnalité BUILD — c'est la bonne discipline.** J'ajoute : la confirmation de publication réelle des rangs 1-2 (état inconnu, le comité ne lit pas LinkedIn) passe par le rituel hebdo proposé avec Sam, pas par un outil.

**Customer Success** *(mode dégradé attendu, 0 client)* — Propose : kit d'onboarding outillé (22/08), base de connaissances ≥12 entrées dont un script BUILD (29/08), schéma du canal tickets prêt à câbler (15/08) indépendamment de SMTP-PROD-001, calibration provisoire des seuils de santé sur les données de test, test à blanc complet en S4 et revue go/no-go avec Sam avant le 01/09, plus un « score de préparation CS » pour rendre la phase mesurable. **Je retiens tout — c'est le plan le plus frugal et le mieux séquencé des quatre.** Sa demande unique (une date pour SMTP-PROD-001) est légitime : sans elle, le premier client n'a aucun canal de support au jour 1 et 30 points de la formule de santé sont invérifiables.

**Chief of Staff** *(score 70, ambre)* — Propose : Étape 0 d'auto-diagnostic en début de ronde (le CoS vérifie sa propre fraîcheur et celle de tous les agents — coût nul, répond directement à l'angle mort révélé par l'incident), outil bash de fraîcheur multi-agents, preuve réelle du dispositif Telegram en S0, priorites_semaine alimentée 4 semaines (sous réserve de mandat), 2 sous-KPI de résilience ajoutés à O5, rapport de readiness gouvernance à J-1 du lancement. **Je retiens tout.** J'appuie particulièrement la correction d'O5 : l'incident a donné un délai de détection réel de 16 jours pour une tolérance implicite de 2 — l'OKR doit porter cette leçon. Sa demande de visibilité sur le solde de crédits API est la seule vraie prévention de récidive ; je la porte en décision 6.

---

## 4. Arbitrages et conflits — mes contrôles croisés

**a) Le trou Delivery (incohérence majeure).** Quatre plans dépendent du Delivery (preuve BUILD pour le commercial, rangs 7-10 pour le marketing, onboarding Team et SMTP-PROD-001 pour le CS, poids 0,30 du score pour le CoS) — et c'est précisément le domaine sans plan. Par ailleurs O2 liste des chantiers (Stripe prod, Postmark, RAG v2, 6 bugs) qu'**aucun document du jour ne mentionne ni ne planifie**. Sans Stripe en production, il n'y a pas de lancement payant le 01/09, quel que soit l'état du reste. C'est mon arbitrage n°1 : plan + statut O2 sous 48h, avant toute autre allocation d'effort Delivery.

**b) Convergence de 3 plans sur un même point de défaillance unique.** Trame démo Team (commercial, 15/08), portraits BUILD (marketing, septembre) et discours d'onboarding Team (CS) dépendent tous du même incident BUILD — lui-même bloqué par une décision en attente_sam depuis 17j (DEC-07, coût nul). Les trois directeurs ont chacun prévu un repli « SDS seul » : je les aligne sur **un seul checkpoint, le 15/08**, avec une seule décision de posture tier Team (décision 4) au lieu de trois replis improvisés séparément.

**c) Doublon d'effort : trois demandes d'espaces de fichiers.** Commercial (config/commercial/), CS (base de connaissances), et le précédent du marketing (config/contenus/) : même besoin, trois formulations. Je fusionne en une décision unique — arborescence `config/<domaine>/` versionnée, commit par ronde (décision 7). Motif réel et documenté : le détail des 3 fiches commerciales du 15/07 est déjà perdu, écrasé dans deos_state.

**d) Doublon commercial interne.** « Outil de recherche web RGPD » et « connecteur SIRENE/data.gouv » sont deux réponses au même problème (pas de source de prospects). Tant que DEC-01 n'est pas tranchée, aucun des deux n'est justifié : si le réseau de Sam fournit les premiers comptes, l'outil peut attendre septembre. Je déclasse les deux en « plus tard » (section 6).

**e) Sur-ambition au regard de Sam seul.** Les quatre plans réunis demandent à Sam **une quinzaine de validations distinctes** cette semaine (6 côté commercial, 4 marketing, 3 CS, 6 CoS, avec recouvrements). Sam est seul et a déjà laissé 6 décisions en attente 17 jours — leur en présenter 15 garantit une nouvelle pile morte. Je les ai compressées à 7, groupées, classées par impact (section 5). C'est le contrat : si Sam traite ces 7, les directeurs ont tous leur déblocage prioritaire.

**f) Sur-ambitions ponctuelles, nommées.** Commercial : stock 40-60 comptes au 01/09 → ramené à 20-30 (voir §3). Marketing : la cadence rangs 4-6 (11, 18, 25/08) ne tient que si DEC-04 est tranchée cette semaine — sinon la cascade est mécanique et O3 devra être révisé, ce que le CMO admet. CS : « ≥12 entrées de base de connaissances » suppose l'espace fichiers de la décision 7 — dépendance non déclarée dans son plan, je la trace ici. CoS : « ≥95 % de rondes réussies en août » ne dépend pas de lui mais du crédit API — le KPI est bon, mais il mesure Sam autant que le CoS ; sans visibilité solde (décision 6), il est en partie hors de contrôle.

**g) Incohérences de données mineures, déclarées.** Le rapport marketing cite l'échec BUILD « inchangé depuis le 15/07 » sur la base d'une lecture du rapport delivery de la veille au soir — le rapport delivery du jour (07:04) confirme le même état, pas de conflit de fond. Le décompte projets (78, corrigé de 76 par le commercial) est cohérent avec les 78 lignes vues par le CS. Rien à arbitrer.

---

## 5. Ce que Sam doit décider (7 décisions, par impact décroissant)

1. **Débloquer le diagnostic BUILD — DEC-2026-0716-07 (+ faire aboutir DEC-06).** Options : (a) autoriser l'accès en lecture aux logs du worker BUILD (ARQ/raj-diego-zara-aisha) ; (b) refuser et accepter que le tier Team reste invérifiable au 15/08. **Ma recommandation : (a)** — coût nul, lecture seule, 17 jours de retard, et c'est le seul chemin vers une preuve Team avant la démo du 15/08 (sources : rapport_delivery 02/08 ; DEC-07 attente_sam).
2. **Exiger le plan Delivery + statut O2 sous 48h.** Options : (a) instruction immédiate au Directeur Delivery (dans son cran, je route dès validation) ; (b) attendre la prochaine ronde spontanée. **Recommandation : (a)** — O2 échoit le 31/08 et personne ne porte Stripe/Postmark/RAG v2/6 bugs aujourd'hui (source : okr_h2 ; absence constatée dans les 4 plans).
3. **Débloquer l'amont commercial — DEC-2026-0716-01 + 02 + validation ICP.** Options pour 01 : liste du réseau de Sam (coût nul, recommandé) / budget outil de recherche / suspension formelle du KPI. Pour 02 : vue `v_deos_*` en lecture sur la table leads. **Recommandation : réseau de Sam + branchement concierge**, et validation de la méthodologie ICP proposée ce jour — le pipeline est à zéro à J-30 (sources : rapport_commercial 02/08 ; pipeline_commercial 14/07).
4. **Posture tier Team si le BUILD n'est pas prouvé au 15/08.** Options : (a) vendre Team avec mode dégradé documenté (« SANDBOX en cours de fiabilisation ») ; (b) lancer septembre sur Pro seul et ouvrir Team dès preuve ; (c) retarder tout le lancement. **Recommandation : décider le 15/08 au checkpoint, avec (b) comme défaut** — les trois domaines concernés ont déjà leur repli SDS, et (c) est disproportionné tant qu'O2 hors BUILD tient (source : convergence des 3 plans, §4b).
5. **Débloquer le marketing — DEC-2026-0716-04 (portrait Sophie, échéance 04/08, J-2) + DEC-05 (cadrage livre blanc).** Options : valider / amender / refuser le portrait. **Recommandation : valider 04 immédiatement** (10 rangs en dépendent, dernière échéance tenable) et recevoir la note de cadrage livre blanc le 10/08 plutôt que cadrer à froid (sources : rapport_marketing 02/08 ; calendrier_editorial).
6. **Boucher les angles morts financiers — DEC-2026-0716-03 étendue + date SMTP-PROD-001.** Fixer `seuil_alerte_solde`, renseigner `echeances_connues`, et **ajouter le solde de crédits API au suivi cash** — c'est la cause racine des 16 jours de silence et elle reste invisible aujourd'hui. Dans le même geste : donner une date (même approximative) pour SMTP-PROD-001, condition du canal tickets CS au 01/09. **Recommandation : tout fixer lundi, 10 minutes** (sources : cash_suivi null depuis 19j ; rapport_cos ; plan CS).
7. **Paquet gouvernance (une validation groupée).** (i) Amendements d'objectifs proposés par les directeurs : KPI « comptes cibles » remplacé par un objectif de préparation tant que DEC-01 n'est pas tranchée ; sous-objectif « prospects sourcés bruts/sem » en régime B ; 2 sous-KPI de résilience sur O5 ; score de préparation CS avant le 01/09. (ii) Mandat priorites_semaine (proposition CoS à valider chaque lundi). (iii) Espaces fichiers versionnés `config/<domaine>/`. (iv) Clôture de DEC-2026-0714-01 (interface web : V1 et V1.1 livrées, commits c7067b0/bb1c3d1) et principe de clôture par le CoS sur preuve en table. **Recommandation : valider le paquet tel quel** — quatre corrections nées de faits vécus, zéro coût (sources : plans cos/commercial/cs 02/08 ; git log).

---

## 6. Capacités manquantes — consolidation priorisée

**Vraiment nécessaire maintenant (avant le 15/08, tout à coût nul ou quasi) :**
1. **Accès lecture logs worker BUILD** (= décision 1) — sans lui, aucun diagnostic possible ; demandé par Delivery, conditionne Commercial, Marketing, CS.
2. **Visibilité sur le solde de crédits API + seuil d'alerte** (= décision 6) — la seule prévention réelle d'une récidive du silence ; demandé par le CoS.
3. **Étape 0 auto-diagnostic dans la ronde CoS + outil bash de fraîcheur multi-agents** — défense en profondeur si le CEO tombe en même temps que les directeurs (c'est arrivé) ; à déposer en `.claude/skills-proposed/cos/`, promotion par Sam.
4. **Espaces fichiers versionnés par domaine** (= décision 7iii) — perte de livrables déjà constatée (fiches du 15/07).
5. **Extension de l'export de logs au worker BUILD + fiabilisation de la fenêtre 24h** (couverture 0 % ce jour, en régression) — côté Sam/infra, hors périmètre comité, mais sans elle la supervision Delivery reste borgne.

**Utile mais différable (après le 15/08 ou après arbitrage) :** outil de recherche web RGPD et connecteur SIRENE (seulement si le réseau de Sam ne suffit pas — attendre DEC-01) ; skill `dh-sourcing-prospects` (après validation ICP) ; outil de calcul automatique du score de santé CS (dès les premiers comptes réels, fin août) ; setup Search Console (avant le 31/08, faible effort) ; alerte Telegram à sévérité croissante ; gabarit de cadrage livre blanc.

**Plus tard (post-lancement) :** sandbox de test du webhook Postmark→N8N ; accès en lecture aux futures tables tickets ; vigie légère 7j/7 (à valider quand de vrais clients existent) ; mécanisme de scoring semi-automatisé du pipeline.

**Ce que je refuse de porter maintenant :** tout outil payant avant que les décisions gratuites soient prises. Le principe « minimum viable, preuve avant investissement » s'applique d'abord à nous-mêmes.

---

## 7. La semaine qui vient (03-09/08), si Sam valide

**Lundi 03/08 — Sam (~30 min) :** passe d'arbitrage sur les décisions 1, 2, 3, 5 et 6 (les décisions 4 et 7 peuvent attendre le milieu de semaine). Test réel du canal Telegram avec le CoS (preuve reçue, tracée).

**Delivery :** livrer plan de département + statut O2 complet sous 48h (mercredi au plus tard). Si décision 1 validée : premier diagnostic des logs worker et RapportIncident BUILD (clôture de DEC-06) avant vendredi.

**Commercial :** trame_proposition v0 + 3 fiches de cas d'usage (cible 11/15) + fiche ICP et schéma fichier_prospects finalisés. Si décision 3 validée : premiers comptes du réseau de Sam intégrés au fichier.

**Marketing :** publication du rang 3 (portrait Sophie) dès validation de la décision 5, avec preuve de publication ; production du rang 4 (Olivia) lancée ; confirmation par Sam de l'état réel des rangs 1-2 sur LinkedIn (premier rituel hebdo).

**CS :** kit_onboarding_v0 (4 templates) + schema_tickets_v1.json ; note de dépendance SMTP-PROD-001 mise à jour avec la date fixée en décision 6.

**CoS :** Étape 0 auto-diagnostic déposée en skills-proposed ; premier jet priorites_semaine (si mandat, décision 7) ; proposition de clôture sourcée de DEC-2026-0714-01 ; relances actives sur toute décision restant ouverte.

**CEO (moi) :** routage tracé de chaque instruction ci-dessus via deos-decisions dès validation de Sam, dans le respect des curseurs ; pose du checkpoint go/no-go tier Team au 15/08 ; brief quotidien rétabli chaque matin — et si un seul domaine manque à l'appel plus de 48h, c'est une alerte haute, plus jamais une note de bas de page.

---

*Sources : rapports des 5 directeurs du 2026-08-02 (deos_state : rapport_delivery 07:04Z, rapport_cs 13:20Z, rapport_marketing 13:21Z, rapport_cos 13:22Z, rapport_commercial 13:25Z) ; plans de département (rondes/plans-consolides.md, 4/5 — delivery manquant, constaté 02/08) ; okr_h2, objectifs_commerciaux, cash_suivi (deos_state, 14/07, validés Sam) ; deos-decisions list 02/08 (13 décisions) ; brief-2026-08-02.md ; git log (16431d9, c7067b0, bb1c3d1). Toute hypothèse est marquée comme telle dans les plans sources.*
