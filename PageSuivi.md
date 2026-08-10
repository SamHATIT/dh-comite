# Page de suivi — Digital·Humans
Générée par le Chief of Staff · ronde du 2026-08-10 + **complément hebdomadaire du 10/08 — trois points de contrôle instruits avec preuve (10h00Z), puis clôture de comité par le CEO (~10h30Z) avec liste de priorités arbitrée par Sam**.

Sources : `psql "$COMITE_DB_DSN"` (table `decisions`) · `deos_state_history` (rapport_commercial du 07/08T07:12:22Z, rapport_legal du 08/08) · fichiers `/workspace/config/contenus/CONT-2026-0804-02/03/04` · `git log -- bin/rondes.sh` (commits b0d6084, 476ddf1) · `/repo` (commits 03fc6e6, 3bcd757, vérifiés) · `curseurs` (table) · `find .claude/skills-proposed` · `deos-state get priorites_semaine/cash_suivi`.

---

## §0 — Le chiffre qui compte : dette d'exécution, écart expliqué, comité clôturé

| mesure | date/source | accordées | en_execution | **total ouvert** |
|---|---|---|---|---|
| 1 | 08/08 matin, brief CEO | — | — | **24** |
| 2 | 09/08 matin, brief CEO | 28 | 2 | **30** |
| 3 | 10/08 07h06 (ronde CoS) | 31 | 2 | **33** |
| 4 | 10/08 09h30 (comptage direct de Sam) | 35 | 2 | **37** |
| 5 | 10/08 10h00 (complément CoS, après 2 clôtures + 4 requalifications) | 29 | 6 | **35** |
| 6 | **10/08 ~10h30 (clôture de comité par le CEO, confirmée en base)** | 29 | 5 | **34** |

### Point de contrôle (1) — écart 33 → 37 expliqué, avec les 4 identifiants
**Cause : (a) — quatre décisions ont basculé `attente_sam → accordee` entre ma ronde (07h06) et le comptage de Sam (09h30).** Pas une erreur de requête : mon 33 et son 37 étaient tous les deux exacts, à deux instants différents.

Les 4 identifiants exacts, tous `validation_par='sam'`, horodatage `updated_at = 2026-08-10 08:06:27Z` :
- `DEC-2026-0806-08` — audit de sécurité des accès
- `DEC-2026-0806-09` — offre intégrateur
- `DEC-2026-0806-14` — opportunité Crédit Logement
- `DEC-2026-0809-06` — mot de passe du comité régénéré

**Leçon retenue** : horodater explicitement chaque publication du chiffre (« mesuré à HH:MM ») pour qu'un écart de ce type se lise d'emblée comme un décalage temporel et non comme une erreur.

### Mouvement 37 → 35 → 34, entièrement tracé et vérifié
- **10h00 (CoS)** : 2 clôtures avec preuve (DEC-2026-0716-01, DEC-2026-0716-05) + 4 requalifications `accordee → en_execution` (DEC-2026-0803-03/04/05, DEC-2026-0806-12). Détail au §1.
- **~10h30 (CEO, en séance)** : 4 clôtures supplémentaires avec preuve (DEC-2026-0802-08, DEC-2026-0803-02, DEC-2026-0808-05, DEC-2026-0806-01) + 6 décisions créées, dont 3 sont des arbitrages propres du CEO correctement exclus du compteur de Sam (DEC-2026-0810-05 accordée, DEC-2026-0810-07 close, DEC-2026-0810-08 accordée) et 3 des escalades vers Sam (DEC-2026-0810-06, -09, -10, en `attente_sam`).

**Vérification indépendante effectuée par le CoS** (pas une simple confirmation de façade) :
- Les 4 clôtures du CEO portent chacune une preuve exploitable (`preuve` JSON non nul, motif + source + parfois commit).
- Les commits cités (`03fc6e6` FIX-GIT-001, `3bcd757` FIX-TASKENUM-001) **existent réellement sur `/repo`**, message cohérent avec la preuve enregistrée — vérifié par `git log`, pas seulement pris pour argent comptant.
- Les 3 décisions d'arbitrage propre du CEO (`-05`, `-07`, `-08`) ont `validation_par='ceo'` et un statut `accordee`/`clos` — elles ne polluent pas le compteur `attente_sam` de Sam.
- **Compteurs confirmés en base, exacts** : `attente_sam` = **16**, `accordee` = **29**, `en_execution` = **5** → dette d'exécution = **34**.

---

## §1 — Décisions (95 au total : 16 attente_sam · 29 accordée · 5 en_execution · 41 clos · 4 refusée)

### Point de contrôle (2) — le constat du 06/08 sur le livre blanc et 3 autres décisions était erroné pour l'une, incomplet pour les trois autres

J'ai ouvert et vérifié sur disque les 4 fichiers cités par le Marketing. Verdict, dossier par dossier :

| décision | fichier de preuve | ce qu'il contient réellement | verdict |
|---|---|---|---|
| **DEC-2026-0716-05** (cadrage livre blanc) | `CONT-2026-0804-04_cadrage-livre-blanc.md` (déposé 04/08 07:07) | Sujet, plan en 5 parties, jalons, responsables — **exactement** le mandat de la décision. | Mandat rempli. **Clôturée** avec preuve citée (`--par cos`). |
| **DEC-2026-0803-04** (page LinkedIn) | `CONT-2026-0804-02_page-linkedin.json` (déposé 04/08 07:07) | Accroche + résumé livrés (réemploi validé le 14/07). Bannière **explicitement différée**. | 2/3 de l'objet produit, mandat pas rempli en entier. Requalifiée `en_execution`. |
| **DEC-2026-0803-03** (portraits N&B) | `CONT-2026-0804-03_concept-visuel-portraits-identite.json` (déposé 04/08 07:07) | Un **concept d'orientation** — le document dit lui-même : « rien n'est produit ni engagé sur les 10 portraits avant la mesure du traitement Sophie ». | Cadrage réel, production non commencée, en attente de validation Sam. Requalifiée `en_execution`. |
| **DEC-2026-0803-05** (identité directeurs) | même fichier | Idem : principe défini, rien produit ni mis en ligne. | Même verdict. Requalifiée `en_execution`. |

**Ce que ça change** : ces 4 dossiers sortent de la case « personne n'a travaillé ». Seul 0716-05 remplit intégralement son mandat ; les trois autres attendent une **validation d'orientation de Sam**, restée sans réponse depuis 6 jours — une dette de validation, pas une dette d'exécution du Marketing.

### Point de contrôle (3) — deux clôtures instruites par le CoS, deux autres confirmées par le CEO en séance

**DEC-2026-0716-01 (source de comptes cibles) → clôturée.** Preuve vérifiée indépendamment : `deos_state_history.rapport_commercial` du **2026-08-07T07:12:22Z**, 10 sociétés dont les `signal_source` correspondent exactement aux ids cités (`v_deos_signaux #48,59,62,63,65,66,67,68,69,73`), croisées avec une fiche ICP sur 78 projets réels. Réserve conservée dans la preuve : aucun compte demo-ready, aucun saisi en pipeline.

**DEC-2026-0806-12 (chemin critique réouverture du site) → non clôturée, requalifiée `en_execution`.** Le sous-objet (FIX-LEGAL-001) est prouvé (commit `b0d6084`) mais l'objet réel (réouverture du site) reste bloqué — `rapport_legal` du 08/08 défavorable, 5 bloquants B1-B5. **Rang 1 des priorités de la semaine désormais** (voir §3) — le CEO l'a escaladée en `DEC-2026-0810-06` : « il n'y a personne pour exécuter ».

**Confirmées par le CEO en séance, avec preuve, indépendamment vérifiées par le CoS :**
- `DEC-2026-0802-08` + `DEC-2026-0803-02` (mission Entracte) → **closes**, arbitrage `DEC-2026-0810-07` : mission suspendue, le concept déjà en ligne (`ENTR-2026-0803-01`) est réemployé, le volet Delivery jamais engagé n'a rien coûté.
- `DEC-2026-0808-05` (FIX-GIT-001) → **close**, commit `03fc6e6` (10/08 09:07:57Z), vérifié sur `/repo`. Elle traînait en `attente_sam` alors que le problème technique était déjà résolu en code — Sam n'avait plus rien à y trancher.
- `DEC-2026-0806-01` (statut démo phare) → **close**, réponse du Delivery : la démo n'est pas en retard, elle est derrière une porte que la décision elle-même a posée (après le 15/08, preuve d'un BUILD de bout en bout).

### 1.1 Les trois plus anciennes décisions accordées/en_execution jamais exécutées

| id | quoi | âge | encore pertinente ? | bloquée par quoi | depuis quand / par qui |
|---|---|---|---|---|---|
| **DEC-2026-0714-01** | Interface web globale de suivi du comité | **27j** | Oui. | Consolidation DSI attendue depuis le 05/08 (5j). | Collectif/DSI, porteur nommé Delivery. |
| **DEC-2026-0802-07** | AI Act art. 50 — mise en conformité | **8j** | Oui, urgente. | Rien de bloquant : `en_execution` réel — libellés IA livrés. Reste : intégration technique widget (Delivery). | Activité continue, Legal + Delivery. |
| **DEC-2026-0802-05** | Mission juridique — vente hors France | **8j** | Oui — DEC-2026-0809-12 montre que Sam raisonne déjà hors France. | Le Légal reconnaît lui-même (rapport du 10/08) : « reconnu en retard, pas livré » — priorisation implicite non signalée. Livraison engagée pour le **13/08**. | 8j sans livrable, statut et date propres depuis aujourd'hui — Legal. |

**Franchissement du seuil de 7j** : DEC-2026-0802-05 passe en « risque d'oubli », mais avec statut et date auto-déclarés le jour même — pas de silence, pas d'escalade à Sam.

### 1.2 — Mouvements du jour, tous tracés (`validation_par`/`preuve` en base)
- CoS : `DEC-2026-0716-01`, `DEC-2026-0716-05` → clos · `DEC-2026-0803-03/04/05`, `DEC-2026-0806-12` → en_execution · `DEC-2026-0810-04` créée (curseur ecrire_base).
- CEO : `DEC-2026-0802-08`, `DEC-2026-0803-02`, `DEC-2026-0808-05`, `DEC-2026-0806-01` → clos · `DEC-2026-0810-05` (accordée, arbitrage propre) · `DEC-2026-0810-06` (attente_sam, escalade réouverture) · `DEC-2026-0810-07` (close, arbitrage propre Entracte) · `DEC-2026-0810-08` (accordée, routage Marketing Crédit Logement) · `DEC-2026-0810-09` (attente_sam, escalade GO sécurité B2) · `DEC-2026-0810-10` (attente_sam, escalade cash/budget — non nommée dans le message de clôture mais présente et correctement comptée).

---

## §2 — Skills proposés par les directeurs
File toujours vide : `find /workspace/.claude/skills-proposed -mindepth 1` → 0 résultat. Aucun skill en attente de validation de Sam.

---

## §3 — Priorités / OKR de la semaine du 10 au 16/08 — arbitrées par Sam, stockées ce jour
`priorites_semaine` mise à jour via `deos-state set priorites_semaine --par cos` (précédente version du 03/08, désormais périmée).

| rang | titre | responsable | appui | OKR | échéance / condition |
|---|---|---|---|---|---|
| 1 | **Réouverture du site** | Sam (geste VPS Hostinger) | Legal (mentions légales, livrées ce soir) · Delivery (mention IA widget Sophie, ~1h) · Marketing (contenu prêt depuis le 03/08) | O2, O3 | Accordée depuis le 09/08, non exécutée à J+1, non bloquée juridiquement — escaladée en `DEC-2026-0810-06`. |
| 2 | **Correctif de sécurité B2** (identifiants Salesforce clients en clair) | Delivery | — | O4 | 5-15 USD API, 2-4h agents BUILD. Condition de l'ouverture des inscriptions de septembre. GO demandé à Sam (`DEC-2026-0810-09`), verdict T1-T4 dû le 11/08. |
| 3 | **BUILD de validation jusqu'au sandbox** | Delivery | — | O2 | Plafond 20 EUR déjà accordé (09/08, `DEC-2026-0809-03`), 3,77 EUR consommés. Débloque le jalon commercial du 15/08 et la démo phare (`DEC-2026-0802-01`, après le 15/08). |
| 4 | **Support visuel Crédit Logement** | Marketing | Commercial (3 prérequis sous 48h) | O1 | Relecture Sam le 12/08 ; présentation DSI dernière semaine d'août, avant les congés de Sam (`DEC-2026-0810-08`). |
| 5 | **Canal de support minimal au 01/09** | Customer Success | — | O1, O4 | Stopgap à coût nul (adresse relevée manuellement + réponse-type carte bancaire validée par Sam + journal des demandes). Indépendant du câblage Email-to-Case, resté sans porteur. |

**Points de suivi hors priorités (à ne pas traiter comme rangs)** : les 4 clôtures et les 3 arbitrages propres du CEO (§0/§1.2) — intégrés au suivi, pas promus en priorité.

---

## §4 — Cash (DH-COS-003 : lecture/alerte, jamais d'estimation de ma part)
- **Solde de trésorerie : 0 EUR, déclaré par Sam le 2026-07-14 — inchangé depuis 27 jours.** Surveillance toujours inactive, signalé sans estimation de ma part.
- **Seuil d'alerte : 50 EUR** (Sam, 03/08, DEC-2026-0716-03, clos). Solde déclaré sous ce seuil, mais périmé depuis 27 jours — l'alerte ne peut pas se déclencher utilement.
- **Budget API** : le CEO a escaladé ce jour (`DEC-2026-0810-10`) un dépassement chiffré par le Financier — 11,90 USD/jour, 357 USD projetés/mois contre un plafond informel de 150 USD, soit 2,4x. Les cinq questions d'optimisation ont été posées avant toute demande de rallonge (économies déjà actées ~35-45 USD/mois, cf. `DEC-2026-0810-05`). Ce n'est pas une découverte du CoS ; je le relaie sourcé, en attente_sam.
- `cash_suivi` (mon périmètre propre) non alimenté depuis le 06/08 (4 jours) — surveillance à réactiver, signalé.

---

## §5 — Relances émises ce jour
| destinataire | décision(s) | objet | pourquoi |
|---|---|---|---|
| CEO | DEC-2026-0714-01 | Interface web, 27j, bloquée par consolidation DSI absente depuis le 05/08. | Doyenne du stock. |
| CEO | DEC-2026-0802-05 | Mission juridique vente hors France — statut et date (13/08) auto-déclarés ce jour, à vérifier au prochain cycle. | Franchit 7j, mais le Légal rend compte. |
| Sam (via CEO, attente_sam) | DEC-2026-0810-06, -09, -10 | Réouverture du site, GO sécurité B2, visibilité cash/budget. | Escaladées par le CEO en séance, non par moi — je les relaie. |
| Sam (info) | — | Dette : 33 → 37 → 35 → **34** (mouvement complet tracé en §0). | Le chiffre bouge dans les deux sens — signe que le suivi fonctionne. |

---

## §6 — Complément hebdomadaire (demande du CEO, 10/08)

### tendances_7j
1. **Dette d'exécution en dents de scie, pas en hausse continue** : 24 → 30 → 33 → 37 → 35 → **34**, purge du stock ancien amorcée pour la première fois (pas seulement le stock récent).
2. **Le Directeur Légal, passé de « 0 rapport jamais reçu » à un rapport quotidien fiable** (FIX-LEGAL-001/002), mais son avis sur la réouverture du site reste défavorable — devenu le rang 1 des priorités de la semaine.
3. **Des livrables Marketing du 04/08 étaient invisibles dans mon comptage** jusqu'à vérification sur disque ce jour — la vérification directe des fichiers doit précéder toute qualification « sans activité ».

### plan_semaine (10-16/08, relié à O5)
| # | intention | coût € | temps de Sam | coût de l'inaction |
|---|---|---|---|---|
| 1 | Horodater chaque publication du chiffre de dette. | 0 € | 0 | Sam recompte lui-même chaque jour. |
| 2 | Router toute question inter-directions sans réponse en 48h vers une DEC- (fait pour `ecrire_base`, `DEC-2026-0810-04`). | 0 € | ~2 min | Angles morts répétés, découverts seulement quand remontés manuellement. |
| 3 | Vérifier sur disque avant de qualifier une décision de « sans activité ». | 0 € | 0 | Constats erronés corrigés a posteriori par les directeurs. |
| 4 | Suivre les 3 échéances fraîches (11/08 verdict T1-T4, 12/08 relecture visuel, 13/08 mission Légal hors France). | 0 € | 0 (déjà engagé) | Échéances à 24-72h qui glissent sans qu'on le note. |
| 5 | Relance nommée (une fois) au Légal sur DEC-2026-0802-05 au prochain cycle. | 0 € | 0 | La date auto-déclarée du 13/08 peut glisser sans suivi. |

### besoin_arbitrage
`DEC-2026-0810-04` (curseur `ecrire_base` du Commercial) reste le seul point que je ne peux pas trancher moi-même — en attente_sam, non résolu par ce comité.

### Point mort signalé par le Commercial (07/08) — confirmé et corrigé
Confirmé dans `deos_state_history.rapport_commercial` (10/08 09:44Z) : question posée au CoS le 07/08, restée sans réponse ni DEC- pendant 3 jours, absente de mon propre rapport du 07/08. Corrigé : `DEC-2026-0810-04` créée. Recherche d'autres cas limitée par l'indisponibilité de `/workspace/bin/memoire` (module `chromadb` absent) — aucun autre cas confirmé dans le temps disponible ; règle structurelle proposée (action 2 du plan) plutôt qu'un balayage manuel répété.

### priorites_semaine
**Stockée ce jour** (§3), arbitrée par Sam, transmise par le CEO en clôture de comité.

---

## §7 — Score d'exécution
Score du matin : 0/100 (plancher), calcul détaillé dans `rapport_cos` du 2026-08-10T07:08:43Z. Stock ouvert : 33 → 37 → 35 → **34** après le comité complet (2 clôtures CoS + 4 clôtures CEO, 4 requalifications, 6 créations dont 3 hors compteur Sam). Recalcul formel du score à la prochaine ronde quotidienne, sur base stabilisée.
