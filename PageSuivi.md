# Page de suivi — Digital·Humans
Générée par le Chief of Staff · ronde du 2026-08-10 (manuelle, en parallèle de la ronde cron 07:00Z dont les fichiers `rondes/*-2026-08-10.json` sont encore à 0 octet pour les 5 directions au moment de la rédaction — pas un échec constaté, juste pas encore disponible).

Sources : `psql "$COMITE_DB_DSN"` (table `decisions`, 85 lignes, dont `updated_at` pour dater les mouvements réels) · dernier brief consolidé disponible : **2026-08-09 07:46Z** (`decisions_attendues`, `compteurs_decisions`) · `find .claude/skills-proposed` · `deos-state get priorites_semaine/cash_suivi/rapport_financier`.

---

## §0 — Le chiffre qui compte : la dette d'exécution monte pour la 3e mesure consécutive

| mesure | date/source | accordées | en_execution | **total ouvert** |
|---|---|---|---|---|
| 1 | 08/08 matin, brief CEO | — | — | **24** |
| 2 | 09/08 matin, brief CEO (`compteurs_decisions.accordees_en_attente_execution`) | 28 | 2 | **30** |
| 3 | **10/08, cette ronde (mesure directe `psql decisions GROUP BY statut`)** | 31 | 2 | **33** |

**Alerte, conformément à la consigne du 09/08** : le chiffre monte depuis 3 relevés d'affilée (24 → 30 → 33), ce n'est plus un constat isolé. La hausse du 09/08 au 09/08 était mécanique (7 requalifications + 4 nouveaux routages, 2 clôtures) ; la hausse du 09/08 au 10/08 (+3) vient de 4 décisions accordées le 09/08 en fin de journée (réouverture site, BUILD de validation, hygiène dispositif, routage sécurité données) sans qu'aucune des plus anciennes n'ait été close entre-temps. **Le stock ancien ne se vide pas, il s'empile sous un stock neuf.**

---

## §1 — Décisions (85 au total : 14 attente_sam · 31 accordée · 2 en_execution · 34 clos · 4 refusée)

### 1.1 Les trois plus anciennes décisions accordées jamais exécutées (nommées, avec les 3 questions imposées)

| id | quoi | âge | encore pertinente ? | bloquée par quoi | depuis quand / par qui |
|---|---|---|---|---|---|
| **DEC-2026-0714-01** | Interface web globale de suivi du comité (tableaux de bord par domaine) | **27j** | Oui — objet de la Mission collective DEC-2026-0804-05 et d'un arbitrage collectif annoncé pour **aujourd'hui 10/08** par le CEO le 09/08. | La consolidation DSI attendue depuis le **05/08** (5j) n'est toujours pas produite — c'est elle qui bloque, pas une absence de volonté. | Bloquée depuis le 05/08 par le **collectif/DSI** (porteur nommé : Delivery, en tant qu'agrégateur). |
| **DEC-2026-0716-01** | Source de comptes cibles régime A (sourcing prospection) | **25j** | Oui, et **en exécution réelle** : le Commercial l'exploite depuis le 07/08 (10 comptes qualifiés cités dans le brief CEO du 09/08, sur la base des 112 signaux `v_deos_signaux`). | Rien de bloquant. Le retard est un **défaut de clôture formelle** (DH-COS-002) : personne n'a encore cité la liste des 10 comptes comme preuve pour clore. Rappel : Sam a explicitement refusé une nouvelle sollicitation le 06/08 (« j'ai déjà donné... proposez »). | Activité réelle depuis le 07/08 (3j), porteur = **Commercial**. Action : demander au Commercial de citer sa liste en preuve, pas une relance de fond. |
| **DEC-2026-0716-05** | Cadrer le livre blanc v1 (sujet, plan, responsable, jalons) | **25j** | Oui — échéance 30/11/2026 toujours valable, mais le cadrage lui-même n'a pas commencé formellement. | Aucun cadrage écrit produit. Le CEO notait le 09/08 « toujours au stade cadrage » ; relance prévue **aujourd'hui 10/08** avec la méthode qui a marché ailleurs (instruction écrite, bornée, contrainte de réutilisation de l'existant). | Aucune activité constatée depuis la création (25j), porteur = **Marketing**. |

### 1.2 Reste du stock ouvert (30 décisions, par tranche d'âge)

| tranche d'âge | nombre | ids | porteur(s) principal(aux) | commentaire |
|---|---|---|---|---|
| 8j (>7j, en risque d'oubli) | 8 | DEC-2026-0802-01,02,03,04,05,06,07,08 | delivery, legal, sam/collectif | Hétérogène : 0802-04 a une note explicite (« arbitrage de principe donné, exécution non prouvée »), 0802-06 est « largement livré » (41 Ko le 08/08) mais pas formellement clos, 0802-05 (juridique vente hors France) est à **0 % produit** — absent du dernier rapport Légal (08/08). 0802-07 progresse réellement (pages légales, mentions IA). |
| 7j | 6 | DEC-2026-0803-01,02,03,04,05,06 | delivery, marketing | 0803-01 (correctif BUILD) avance concrètement (13/14 correctifs livrés le 08/08, GO de validation donné le 09/08, plafond 20 EUR). 0803-03/04/05 (portraits, LinkedIn, identité) sans trace de production confirmée. |
| 6j | 3 | DEC-2026-0804-01,02,05 | delivery/sam, collectif | 0804-01 (fiabilisation logs) : proposition chiffrée prête depuis le 05/08, choix toujours entre les mains de Sam. |
| 5j | 1 | DEC-2026-0805-01 | commercial/sam | Étude livrée, offre canonique pas encore mise à jour — attend la validation de la grille (DEC-2026-0809-02). |
| 4j | 2 | DEC-2026-0806-01,12 | delivery/marketing, sam | 0806-12 vient d'obtenir une réponse partielle de Sam le 09/08 (DEC-2026-0809-01, GO vitrine conditionnel). |
| 2j | 6 | DEC-2026-0808-01,08,09,11,12,13 | marketing, legal, sam, delivery | Trop récentes pour un jugement de retard ; à revoir demain si toujours ouvertes. |
| 1j | 4 | DEC-2026-0809-01,03,04,05 | sam, delivery | Fraîches (arbitrées hier soir) — aucune action aujourd'hui. |

### 1.3 attente_sam (14 — arbitrage de Sam attendu, hors dette d'exécution)
Toutes datées du 09/08 (1 jour), sous le seuil de relance (3j). Liste : DEC-2026-0806-08/09 (calendrier), DEC-2026-0806-14 + DEC-2026-0809-02 (Crédit Logement), DEC-2026-0808-05 (jeton GitHub), DEC-2026-0808-10 (clé de sauvegarde), DEC-2026-0809-06/07/08/09/10/11/12/13 (mot de passe, GPU/souveraineté, concurrent Naaia, positionnement, carte bancaire x2, prix x2). Aucune action de ma part aujourd'hui sauf listing.

### 1.4 Clôturées avec preuve depuis la dernière ronde CoS (07/08 → aujourd'hui)
**22 décisions closes avec preuve**, mouvement réel confirmé par `updated_at` : DEC-2026-0806-02/03/04/05/07/10/11/13/18/19/20/21/22/23, DEC-2026-0807-01/02, DEC-2026-0802-02/03 (routage), DEC-2026-0808-02/03/04/06/07/14. C'est un vrai signal positif de purge — mais il porte sur le stock **récent** (5-8 août), pas sur le stock **ancien** (§1.1), qui lui reste immobile.

---

## §2 — Skills proposés par les directeurs
**File toujours vide** : `find /workspace/.claude/skills-proposed -mindepth 1` → 0 résultat, vérifié ce jour. Aucun skill en attente de validation de Sam.

---

## §3 — Priorités / OKR de la semaine (source : `deos-state get priorites_semaine`, alimenté par cos le **2026-08-03** — 7 jours, jamais rafraîchi depuis)

**Constat de process à signaler** : nous sommes lundi, une semaine complète s'est écoulée depuis la dernière fixation de priorités et aucune n'a été reposée pour la semaine du 10-16/08. Rétrospective de la semaine écoulée :

| rang | titre | responsable | bilan de la semaine écoulée |
|---|---|---|---|
| 1 | BUILD checkpoint 15/08 | delivery | Actif : 13/14 correctifs livrés (08/08), GO de validation donné par Sam (09/08, plafond 20 EUR). |
| 2 | Purger le lot d'arbitrage prioritaire | chief-of-staff | Actif : 22 décisions closes avec preuve, 7 requalifiées avec porteur nommé. |
| 3 | Jalons commerciaux 15/08 (bibliothèque 15/15, trames) | commercial | **Stagnant** : bibliothèque 8/15 et trames 3/3 inchangées depuis le 03-05/08 (source : rapport_commercial du 07/08, lui-même non renouvelé depuis 3 jours). Échéance dans **5 jours**. |
| 4 | Conformité AI Act art. 50 | legal | Actif : B1 corrigé, mentions IA posées, pages légales prêtes (08/08). |
| 5 | Séquence éditoriale | marketing | Débloquée : DEC-2026-0716-04 (arbitrage carte 4) est désormais **clos** ; dépend maintenant de la réouverture du site (DEC-2026-0809-01, GO vitrine partiel du 09/08). |

**Pénalité appliquée au score** : rang 3 est resté sans mouvement constaté toute la semaine sur un jalon à échéance proche et sans rapport Commercial depuis 3 jours — traité comme priorité sans activité à mi-semaine (voir §6). Pas de relance émise pour autant (DH-COS-004) : j'attends le rapport Commercial du jour avant de qualifier un blocage.

---

## §4 — Cash (mandat DH-COS-003 : lecture/alerte uniquement, jamais d'estimation de ma part)

- **Solde de trésorerie : 0 EUR, déclaré par Sam le 2026-07-14 — inchangé depuis 27 jours.** Surveillance toujours largement inactive, signalé conformément au mandat, sans estimation de ma part.
- **Seuil d'alerte : 50 EUR**, confirmé par Sam le 2026-08-03 (DEC-2026-0716-03, clos avec preuve). Le solde déclaré (0 EUR) est sous ce seuil — mais la donnée elle-même est périmée depuis 27 jours, donc l'alerte ne peut pas se déclencher utilement sur une base fiable.
- **Budget API (distinct de la trésorerie)** : rythme de consommation **11,92 USD/jour**, projection médiane à 30j = **358 USD**, contre un plafond mensuel de 150 USD — chiffré par le **Directeur Financier le 09/08** (`rapport_financier`, document `config/financier/position_2026-08-09.md`), confirmé indépendamment par `bin/couts.py` le même jour. Ce n'est pas une découverte de ma part, déjà traité par Sam le 09/08 (missions ponctuelles passées sur Sonnet par défaut) — je le rappelle car il reste sourcé et daté, pas pour redemander un arbitrage.
- Aucune échéance de trésorerie connue déclarée.

---

## §5 — Relances émises cette ronde (2026-08-10)

| destinataire | décision(s) | objet | pourquoi maintenant |
|---|---|---|---|
| **CEO** (le CEO relance nommément, cf. règle du 09/08) | DEC-2026-0714-01 | Interface web globale, 27j, bloquée par l'absence de consolidation DSI attendue depuis le 05/08 — à réclamer en tête de l'arbitrage collectif prévu aujourd'hui. | Doyenne du stock, échéance d'arbitrage tombant précisément aujourd'hui. |
| **CEO** | DEC-2026-0716-05 | Livre blanc v1, 25j, aucun cadrage écrit — relance avec la méthode qui a fonctionné ailleurs (instruction bornée). | Deuxième plus ancienne, porteur Marketing nommé. |
| **CEO** | DEC-2026-0802-05 | Mission juridique vente hors France, 8j, **0 % produit**, absente du rapport Légal du 08/08 alors que la mission jumelle (0802-06) a été largement livrée. Un seul cycle de relance CEO fait à ce jour (06/08, DEC-2026-0806-02) — 2e demande nécessaire avant d'envisager Sam. | Franchit le seuil des 7j sans aucun livrable, porteur Legal nommé. |
| **Sam** (info, pas d'arbitrage demandé) | — | Score d'exécution à 0/100 (plancher) pour la première fois depuis la mise en place du calcul — dette d'exécution en hausse 3 mesures d'affilée (24→30→33). Pas une nouvelle question : un signal, conformément au mandat. | Seuil de gravité franchi. |
| — (aucune relance, à surveiller) | rang 3 priorités semaine (jalons commerciaux) | Bibliothèque et trames inchangées depuis 5-7 jours, échéance dans 5 jours, rapport Commercial vieux de 3 jours. | DH-COS-004 : j'attends le rapport du jour avant de qualifier un blocage et d'escalader. |

---

## §6 — Score d'exécution du jour

**Score = 0/100 — ROUGE (plancher)**

Calcul (formule visible), base 100 :
− 8 × 23 décisions en retard (accordée/en_execution, âge >3j) = **−184**
− 15 × 11 décisions en risque d'oubli (âge >7j) : DEC-2026-0714-01, 0716-01, 0716-05, 0802-01/02/03/04/05/06/07/08 = **−165**
− 5 × 0 skill proposé sans traitement >14j (file vide) = **0**
− 10 × 1 priorité de semaine sans activité à mi-semaine (rang 3, jalons commerciaux) = **−10**
= 100 − 184 − 165 − 0 − 10 = **−259, plancher 0**

**Lecture** : ce n'est pas une dégradation soudaine de l'activité — 22 décisions ont été closes avec preuve depuis la dernière ronde CoS (07/08), un vrai signal positif. C'est un changement de **résolution de la mesure** : cette ronde applique pour la première fois la consigne du 09/08 (compter la dette d'exécution tous les jours, pas seulement au comité hebdomadaire) sur l'intégralité du stock ouvert plutôt que sur la seule vague la plus récente. Le stock ancien (0714-01, 0716-01, 0716-05, la vague du 02/08) ne bouge pas pendant que le stock récent se renouvelle. Le score à 0 est le signal exact que le dispositif est censé produire : la dette ne se résorbe pas, elle s'accumule sous un flux qui, lui, tourne bien.
