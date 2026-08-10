# Comité de direction — lundi 10 août 2026

**Ce qui se joue cette semaine, en une phrase :** six tâches sont accordées, non contestées, chiffrées à zéro ou presque — et aucune n'avance, parce qu'il n'y a personne pour les faire.

Ce n'est pas un défaut de discipline des directions. Chacune a rapporté son blocage, nommément, en refusant de contourner son curseur. Le dispositif fonctionne exactement comme il a été conçu. C'est la conception qui a un trou : nous avons construit six observateurs et aucun exécutant. Le réflexe de contrôle serait de relancer plus fort ; le bon réflexe est de regarder ce qui manque — ici, un droit d'agir, pas une volonté. C'est l'objet de la décision 1 ci-dessous, et elle explique à elle seule la majeure partie de la dette.

**La bonne nouvelle du jour, et elle est réelle :** à 09:07Z, FIX-GIT-001 a été corrigé — l'intégration git de la plateforme, jamais fonctionnelle depuis l'origine, fonctionne (commit `03fc6e6`, dépôt cloné, contenu présent). À 09:19Z, une tâche de phase 2 `business_logic` a réussi pour la première fois depuis le crash du 2 août. Le BUILD n'est pas prouvé de bout en bout, mais il a bougé pour la première fois en huit jours.

---

## 1. Position par rapport au plan

| Courbe du plan | Cible | Réel au 10/08 | Écart |
|---|---|---|---|
| **O1 — Revenu** (MRR ≥ 4 800 € au 31/12, 11 clients) | pipeline alimenté | **MRR 0 €, pipeline 0/0 sur 7 stades**, inchangé depuis le 14/07 (27 j) | 1 opportunité qualifiée hors pipeline (Crédit Logement, 9/10) |
| **O2 — Lancement** (produit prêt 31/08, payant septembre) | 8 chantiers clos | 7/8 « fait », bascule paiement en production non faite ; source datée du 05/08 | 21 jours restants |
| **O3 — Visibilité** (13 contenus avant fin octobre) | rangs 3-13 publiés | **rangs 3-13 bloqués depuis 3 semaines** : le site est en entracte | réouverture au 10/08 ⇒ rang 13 vers le 14/10, marge 17 j |

**Fait, pas opinion :** le pipeline est vide à J-22 du lancement payant. Les référentiels `okr_h2` et `objectifs_commerciaux` datent du 14/07 (27 jours) — ils n'ont pas été révisés depuis, je les cite tels quels.

**Santé globale : 58/100 — ambre.** Calcul : Delivery 68 × 0,30 + Commercial 100 × 0,25 + Marketing 5 × 0,15 + Exécution 0 × 0,10, rapporté aux poids restants (0,80). **Domaine manquant : Customer Success**, dont le score est non calculable — 0 client réel, la formule est sans objet, c'est normal et non une défaillance. Score plafonné à l'ambre en conséquence.

Deux lectures à ne pas faire : le 100 du Commercial mesure le respect d'un rythme de processus, pas la santé d'un pipeline — son auteur le dit lui-même, aucun des 10 comptes qualifiés n'est prêt pour une démo. Le 5 du Marketing vient d'un malus de −40 pour quatre contenus en attente de validation depuis 6 jours : il mesure **ta** file de validation, pas sa production.

---

## 2. Alignements actés

- **La réouverture du site n'est pas bloquée juridiquement.** Le Juridique l'a tranché en séance : en vitrine stricte (pas d'inscription, pas de paiement), seules les mentions légales restent obligatoires (LCEN art. 6-III-1). Il manque trois lignes — OpenAI dans les sous-traitants, le téléphone de l'hébergeur, l'entité du prestataire de paiement — **livrées ce soir**. Les CGV ne sont pas exigibles sans transaction. Son avis défavorable ne porte que sur **l'ouverture des inscriptions**, pas sur la vitrine.
- **Le livre blanc n'était pas en retard de 25 jours.** Le Chief of Staff le comptait comme « aucun cadrage produit » ; le Marketing a montré le fichier. Le CoS a vérifié sur disque et a clos la décision. Il a aussi établi que trois autres décisions (portraits, LinkedIn, identité) ne sont couvertes qu'à moitié — le concept existe, la production non : requalifiées en exécution, pas closes. **Le Marketing avait raison sur une, le CoS sur trois.**
- **Le compteur de dette n'était pas faux.** L'écart 33 (07h) → 37 (09h30) vient de quatre décisions passées en « accordée » à 08:06Z. Les deux chiffres étaient justes, à deux instants.
- **La démo phare n'est pas en retard** : elle est derrière une porte que la décision elle-même a fermée (après le 15/08, conditionnée à la preuve BUILD). Trois relances pour un blocage qui n'existait pas — c'est ma faute de lecture, pas celle du Delivery.
- **Le correctif de sécurité B2 est petit.** L'infrastructure de chiffrement existe et fonctionne ; elle est contournée dans un seul fichier (`projects.py`, 6 sites). 5 à 15 USD d'API.

**Un incident de dispositif à signaler, il n'est pas anodin :** la ronde Commercial a bien tourné ce matin et produit deux livrables réels sur disque — mais son rapport n'a jamais atteint la base, par sur-prudence face au curseur. Pendant 74 h, le comité a cru la direction commerciale silencieuse alors qu'elle travaillait. Corrigé à 09:44Z. Le mode de défaillance — un travail fait qui n'arrive jamais au registre — mérite d'être surveillé. Par ailleurs, le Directeur Financier n'a pas pu tourner sur son modèle local (GPU hors service) ; j'ai appliqué le repli documenté. `/workspace/bin/memoire` est cassé pour trois directions (chemin absent, `chromadb` manquant).

---

## 3. Arbitrages

### Ce que j'ai tranché et tracé — sans toi

**Mission Entracte version scène : suspendue** (DEC-2026-0810-07, clôt 0802-08 et 0803-02). Investir dans une plus belle page d'entracte quand on cherche à en sortir n'a plus de sens. Vérifié avant de trancher : rien d'engagé n'est perdu (le volet Delivery était séquencé après le 15/08), le livrable existant reste en ligne, et deux éléments sont conservés pour la vitrine. Coût : 0 €. Porte à double sens — se rouvre d'un mot si la réouverture se bloquait au-delà du 20/08.

**Support visuel Crédit Logement : le Marketing le porte** (DEC-2026-0810-08). Le Commercial a livré le dossier complet aujourd'hui et déclaré le support visuel hors de son périmètre : personne ne le portait, à 15 jours de l'échéance. Marketing livre le 12/08 (4-6 pages, données réelles, aucune dépendance au BUILD) ; le Commercial fournit trois prérequis sous 48 h. **Limite que je pose : l'objection Naaia n'y figure pas sans ton accord distinct** — nommer un concurrent dans un document projeté relève de la publicité comparative, et le Juridique n'a pas vérifié les articles applicables.

**Discipline du comité : −35 à 45 USD/mois** (DEC-2026-0810-05). Le Financier a mesuré que ce comité a réinterrogé six directions ayant déjà rapporté le matin même, dont j'avais les rapports sous les yeux : ~11 USD de doublon. Dès le 17/08, je lis les rondes fraîches et n'invoque que le Financier, les directions où une friction exige une position, et le Juridique si un sujet est ouvert. Je m'applique la règle avant de demander quoi que ce soit.

**Quatre décisions closes avec preuve**, dont **FIX-GIT-001** — elle occupait ton compteur d'arbitrage alors que le problème avait été résolu à 09:07Z. Tu n'avais plus rien à y trancher.

### Ce qui te revient — 5 décisions

**1 · ESCALADE — PERSONNE POUR EXÉCUTER** (DEC-2026-0810-06). Six tâches accordées, aucune ne peut être faite par une direction du comité : réouverture du site (le site affiche toujours *Entracte*, vérifié à 09h30, HTTP 200) · fiabilisation des logs (blackout de 20 h ce matin, résorbé par hasard au redémarrage) · Email-to-Case (3 h de configuration, licence déjà payée) · mention IA du widget Sophie (~1 h ; l'AI Act art. 50 s'applique depuis le 02/08, l'exposition est continue) · relecture Elena · SMTP N8N.
**Options :** (a) **SAM** — tu gardes ces gestes, on te réserve 4 h et on cesse de les compter comme dette des directions ; (b) **CURSEUR** — tu élèves le curseur du Delivery sur un périmètre borné et journalisé ; (c) **TIERS** — un exécutant externe.
**Ma recommandation : (a) cette semaine, (b) à instruire pour septembre.** Élever un droit sur la production est une porte à sens unique — tu as toi-même posé la règle absolue du 08/08 (aucun déploiement en production). On ne franchit pas cette porte sous la pression d'une dette de gouvernance.

**2 · GO SUR LE CORRECTIF B2** (DEC-2026-0810-09). Coût : 5-15 USD, 2-4 h d'agents BUILD. Sans lui, l'avis juridique reste défavorable, donc les inscriptions n'ouvrent pas, donc septembre n'a pas de revenu. **Argument contraire honnête :** migrer les valeurs déjà en clair exige un accès en écriture sur la production, que personne ici n'a — porte à sens unique.
**Options :** (a) **GO** correctif de code cette semaine, migration instruite séparément ; (b) **GO COMPLET** ; (c) **ATTENDRE** le verdict T1-T4 de demain. **Recommandation : (a).**

**3 · PRIX DU PRO** — décisions existantes DEC-2026-0809-13 (79 € avec lancement à 59 €) et DEC-2026-0809-12 (« 79 €, c'est déjà haut en Europe continentale »), qui se contredisent partiellement. **Neuf livrables portent aujourd'hui un prix obsolète** : les 8 fiches de cas d'usage et le plan de lancement (16 occurrences). Les deux directions refusent à raison de les reprendre avant que tu tranches, pour éviter une double reprise. Le Financier confirme les seuils : **73 abonnés à 49 €, 56 à 59 €, 38 à 79 €** ; le plafond micro-entreprise n'est une contrainte à aucun de ces prix. **Recommandation : trancher en un mot cette semaine** — reprise ensuite en moins d'une heure, 0 €.

**4 · CRÉDIT LOGEMENT — DEC-2026-0809-02**, en attente depuis le 09/08, plus une question posée le 07/08 restée sans réponse : **qui porte la relation, SH Conseil ou Digital·Humans ?** Présentation dernière semaine d'août, tu pars en congés juste après. Le dossier est prêt, le support arrive le 12/08 ; il manque ta grille de prix et ce montage.

**5 · DEUX CHIFFRES QUE PERSONNE NE CONNAÎT** (DEC-2026-0810-10). Le solde de trésorerie réel est inconnu depuis 27 jours : le seuil d'alerte de 50 € existe mais ne peut se déclencher sur une donnée périmée — **la surveillance cash est décorative** (2 minutes de ta part). Et le plafond API est dépassé de 2,4× (357 USD/mois projetés contre 150). **Les cinq questions ont été posées avant toute demande d'argent :** ~85 USD/mois d'économies identifiées, dont 35-45 déjà actées aujourd'hui, et le retour du Juridique en cadence hebdomadaire après B2. Reste ~270 USD/mois. **Recommandation : (c) mesurer d'abord le gisement du brief quotidien** — premier poste de dépense, 25 % du total, gisement jamais chiffré ; demander une rallonge sans l'avoir regardé serait exactement ce que tu as interdit. Je ne masque pas la conclusion probable : à dispositif constant, 150 USD/mois ne couvre pas le fonctionnement réel.

---

## 4. La dette d'exécution

| | 08/08 | 09/08 | 10/08 (07h) | **10/08 (clôture)** |
|---|---|---|---|---|
| **Accordées, en attente d'exécution** | 24 | 30 | 33 | **34** |
| **En attente de ton arbitrage** | — | — | 13 | **16** |

**La tendance s'est inversée dans la séance, pas dans les chiffres.** Le stock brut monte encore (+1), mais il a d'abord baissé de 37 à 32 pendant le comité : sept décisions closes avec preuve, dont **deux des trois plus anciennes du dispositif**. Il remonte à 34 uniquement parce que j'ai ajouté mes propres arbitrages du jour. La dette ancienne, elle, se résorbe pour la première fois.

**Les trois plus anciennes qui restent :** DEC-2026-0714-01 — interface web de suivi, **27 jours**, bloquée par la consolidation attendue depuis le 05/08 ; DEC-2026-0802-07 — **AI Act art. 50, 8 jours**, seule décision en exécution, sur un règlement applicable depuis le 02/08, exposition continue de Sophie sans mention ; DEC-2026-0802-05 — vente hors France, **8 jours, 0 % produit**.

**Ce que je te dois en retour.** Le Juridique a reconnu sans détour que DEC-2026-0802-05 n'a pas avancé par une priorisation implicite qu'il n'avait jamais annoncée, et s'engage sur le **13/08** — une date, pas une intention. C'est la bonne attitude. La mienne l'est moins : j'ai relancé trois fois la démo phare pour un blocage qui n'existait pas, et le Commercial a posé une question au comité le 07/08 qui est restée trois jours sans identifiant, donc sans compteur, donc invisible. Le CoS l'a transformée en décision aujourd'hui. **Une question sans identifiant est un angle mort du dispositif** — nous n'en avions pas la mesure.

---

## 5. Priorités de la semaine

| Rang | Priorité | Responsable | OKR |
|---|---|---|---|
| 1 | **Réouverture du site** — mentions légales ce soir, mention IA du widget, geste sur Hostinger | **Sam** (appui Legal, Delivery, Marketing) | O3, O2 |
| 2 | **Correctif de sécurité B2** — condition d'ouverture des inscriptions de septembre | directeur-delivery | O4 |
| 3 | **BUILD de validation jusqu'au SANDBOX avant le 15/08** — débloque le jalon commercial et la démo phare | directeur-delivery | O2 |
| 4 | **Support visuel Crédit Logement** — relecture le 12/08 | directeur-marketing (appui commercial) | O1 |
| 5 | **Canal de support minimal au 01/09** — stopgap à coût nul | directeur-customer-success | O1, O4 |

Transmises au Chief of Staff pour stockage (`deos-state set priorites_semaine --par cos`) et mise à jour de la PageSuivi.

---

## Ma recommandation

**Réserve 4 heures cette semaine et prends les six gestes toi-même — puis instruis l'élévation de curseur pour septembre, à froid.**

Nous sommes en temps de guerre : zéro revenu, échéance au 1er septembre, un fondateur seul qui tient un autre emploi. Le régime de décision qui va avec, c'est d'accélérer les portes à double sens et de ne surtout pas précipiter celles à sens unique. Les six tâches bloquées coûtent presque rien et deux d'entre elles conditionnent le revenu de septembre : elles ne méritent pas d'attendre une refonte des droits. Mais élever le curseur d'une direction sur la production pour les débloquer plus vite serait franchir, dans l'urgence, la porte que tu as toi-même verrouillée le 08/08.

Le vrai coût n'est pas en euros — il est dans tes heures, et c'est la ressource rare. C'est précisément pour ça que le choix mérite d'être fait une fois, calmement, plutôt que subi chaque lundi.

---

<details>
<summary>Annexe — données du comité</summary>

**Contrôles croisés effectués (C1-C5).** C1 incohérences factuelles : 5 relevées, 5 résolues en séance (compteur de dette, livre blanc, démo phare, statut O2, BUILD de validation déjà accordé). C2 collisions de plan : 2 (Entracte vs réouverture — arbitrée ; charge de Sam — matière de la décision 1). C3 synergies manquées : 2 (support Crédit Logement — fermée ; succès BUILD non relié au jalon commercial du 15/08 — porté en priorité 3). C4 décisions orphelines : 6, objet de la décision 1. C5 dette d'exécution : relance nominative effectuée auprès des 6 directions.

**Décisions créées ce jour par le CEO :** DEC-2026-0810-05 (discipline du comité, accordée), -06 (escalade porteur, attente_sam), -07 (suspension Entracte, close), -08 (routage support Crédit Logement, accordée), -09 (escalade go B2, attente_sam), -10 (escalade trésorerie et plafond API, attente_sam).

**Décisions closes ce jour par le CEO :** DEC-2026-0802-08, DEC-2026-0803-02, DEC-2026-0806-01, DEC-2026-0808-05. Par le Chief of Staff : DEC-2026-0716-01, DEC-2026-0716-05.

**Fraîcheur des rapports :** Delivery 10/08 07:05Z · Marketing 10/08 07:11Z · CS 10/08 07:03Z · CoS 10/08 07:06Z · Commercial 10/08 09:44Z (stocké pendant le comité, après 74 h de silence apparent) · Legal 10/08 09:52Z · Financier 09/08 22:03Z (cadence hebdomadaire, pas de retard).

**Vérifications faites par le CEO lui-même :** `curl https://digital-humans.fr` → HTTP 200, titre « Entracte — Digital·Humans » à 09h30 · `git log` sur `/repo` → commits `03fc6e6` (09:07:57Z) et `3bcd757` (09:18:45Z) · comptages `decisions` en base à 09h30 et à la clôture.

**Compteurs à la clôture :** clos 41 · accordée 29 · attente_sam 16 · en exécution 5 · refusée 4.

**Score de santé :** (68 × 0,30 + 100 × 0,25 + 5 × 0,15 + 0 × 0,10) ÷ 0,80 = 57,7 → **58/100, ambre**. Domaine manquant : Customer Success (non calculable, 0 client réel).
</details>
