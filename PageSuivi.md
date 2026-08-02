# Page de suivi — Digital·Humans

Ronde Chief of Staff du 2026-08-02 (source : `deos-decisions:list` + psql
direct sur `decisions`, `deos-state get brief|okr_h2|cash_suivi|priorites_semaine`,
`find .claude/skills-proposed`, `git log`, `rondes/*.json`,
`briefs/daily-*.meta.json`, `briefs/comite-*.meta.json`). Ronde précédente :
**2026-07-16T07:02Z** — écart de **17 jours** dû à un incident de
gouvernance détaillé ci-dessous.

## Incident de gouvernance — silence du comité (17/07 → 01/08)

**Ne pas minimiser : ce n'est pas seulement commercial/marketing/CS qui ont
manqué à l'appel — le comité entier (les 5 agents + la composition du brief
CEO) a été à l'arrêt pendant 16 jours calendaires.**

- **Durée** : 2026-07-17 → 2026-08-01 inclus (16 jours). Dernier rapport CoS
  exploitable avant la coupure : 2026-07-16T07:02Z. Reprise : 2026-08-02
  (delivery et CoS).
- **Cause** : erreur API systématique `Credit balance is too low`
  (`api_error_status: 400`) sur chaque tentative de ronde, tous agents
  confondus — vérifié sur 100% des fichiers `rondes/*-2026-07-{17..31}.json`,
  `rondes/*-2026-08-01.json` et `briefs/daily-2026-07-{17..31}.meta.json`,
  `briefs/comite-2026-07-{20,27}.meta.json`.
- **Directeurs/agents concernés** : delivery (cadence 7j/7, 16 échecs
  consécutifs), commercial / marketing / customer-success / chief-of-staff
  (cadence lun-ven, 11 échecs chacun : 17,20,21,22,23,24,27,28,29,30,31/07),
  et le brief CEO quotidien (mêmes dates).
- **État à ce jour (2026-08-02)** : reprise **partielle**. Delivery a produit
  un rapport frais (07:02:24Z) et le brief CEO a pu être composé (07:33Z).
  Le CoS reprend sa ronde aujourd'hui via ce document. **Commercial,
  marketing et CS restent silencieux ce jour même** (dernier rapport connu :
  2026-07-16, ~408h) — l'incident n'est donc pas clos pour ces 3 domaines,
  il dure depuis **17 jours** et se poursuit. Aucun fichier de ronde non
  vide ne prouve leur reprise aujourd'hui (seuls des artefacts `*-plan.json`
  à 0 octet existent, sans valeur probante).
- **Remédiation déjà engagée** : commit `16431d9` (2026-08-02 13:17:21Z)
  ajoute une alerte Telegram sur échec de ronde et fait traiter par le CEO
  tout rapport absent >48h comme alerte haute, avec escalade si 2 domaines
  muets — correctif tiré explicitement de « la leçon du silence 16/07-01/08 ».
- **Décisions/échéances qui auraient dû être suivies pendant le trou** :
  - **DEC-2026-0714-01** (interface web comité, `en_execution` depuis le
    14/07) : dernière preuve d'activité le 2026-07-14T17:12:48Z (commits
    `c7067b0`/`bb1c3d1`/`a0bbb23`). Le seuil de relance (3j) était atteint le
    **17/07 — premier jour du silence** — et n'a donc **jamais été signalé**.
    Elle est aujourd'hui à **19 jours** sans preuve : première relance émise
    par la présente ronde.
  - **DEC-2026-0716-06** (routage delivery : produire un RapportIncident sur
    l'échec systémique BUILD data_model, `en_execution` depuis le 16/07,
    créée juste avant la coupure) : 17 jours sans aucun livrable, jamais
    relancée pendant le silence. Première relance émise ce jour.
  - **6 décisions `attente_sam`** (DEC-2026-0716-01/02/03/04/05/07, créées le
    16/07 juste avant la coupure) : 17 jours sans arbitrage de Sam, dont deux
    à échéance proche (dossier démo Team 15/08, régime commercial B et
    lancement payant 01/09). Le CEO les a re-signalées en escalade dans le
    brief de ce jour faute d'arbitrage pendant la coupure.
  - **OKR H2** : O1 Revenu (pipeline commercial gelé, 0/5 comptes cibles non
    rafraîchi), O3 Visibilité (calendrier éditorial et livre blanc sans
    mouvement traçable, échéance de publication du 21/07 de statut inconnu),
    O5 Gouvernance (« 0 décision oubliée, brief à l'heure ≥95% ») — cette
    cible est objectivement dépassée sur la période (11 rondes ratées sur
    les jours ouvrés du 17 au 31/07).

## §1 Décisions

| id | quoi (≤60c) | origine | statut | âge | preuve | prochaine action |
|---|---|---|---|---|---|---|
| DEC-2026-0713-01 | Test étape 1 : validation du socle | sam | clos | 20j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-01 | Interface web comité : tableaux de bord par domaine | sam | en_execution | 19j (19j sans activité) | non | **relance émise ce jour** — en risque d'oubli (>7j), aucune relance n'avait jamais pu être émise (silence 17/07-01/08) |
| DEC-2026-0714-02 | DA-2026-0714-01 : fiabilisation export logs | ceo | refusée | 19j | oui | aucune — refusée par Sam avec preuve |
| DEC-2026-0714-03 | DA-2026-0714-02 : activation calendrier rapports directeurs | ceo | clos | 19j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-04 | DA-2026-0714-03 : confirmer hypothèse déploiement + test fumée | ceo | clos | 19j | oui | aucune — clôturée avec preuve |
| DEC-2026-0714-05 | Session validation 14/07 : OKR H2, objectifs, calendrier, comptes, Postmark, fiches agents, cash_suivi | sam | clos | 19j | oui | aucune — clôturée avec preuve |
| DEC-2026-0716-01 | DA-2026-0715-01 : source de comptes cibles régime A | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — bloque le régime B (01/09) ; escaladé par le CEO ce jour |
| DEC-2026-0716-02 | DA-2026-0715-02 : branchement lecture source concierge Sophie | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — signalé sans décision dès le 14/07 ; escaladé par le CEO ce jour |
| DEC-2026-0716-03 | DA-2026-0715-03 : fixer le seuil d'alerte cash (seuil_alerte_solde) | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — condition d'activation de la surveillance cash |
| DEC-2026-0716-04 | DA-2026-0715-04 : valider portrait Sophie CONT-2026-0715-01 + format hook | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — bloque la publication [DH-CMO-001] |
| DEC-2026-0716-05 | DA-2026-0715-05 : cadrer le livre blanc v1 | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — échéance 30/11, 0 avancement, OKR O3 à risque |
| DEC-2026-0716-06 | ROUTAGE delivery : produire un RapportIncident sur l'échec BUILD data_model | ceo | en_execution | 17j (17j sans activité) | non | **relance émise ce jour** — en risque d'oubli (>7j), aucun livrable depuis la création |
| DEC-2026-0716-07 | Autoriser l'accès EN LECTURE aux logs du worker BUILD | ceo | attente_sam | 17j | non | obtenir arbitrage Sam — seul chemin de diagnostic du signal produit de gravité HAUTE ; échéance démo Team 15/08 ; escaladé par le CEO ce jour |

**Décisions ouvertes (non terminales) : 8/13** — 2 `en_execution` (toutes
deux en risque d'oubli, >7j sans preuve) + 6 `attente_sam` (toutes à 17
jours sans arbitrage). **Aucune décision n'a pu être suivie pendant les 17
jours d'interruption du CoS** : c'est l'écart de traçabilité central de
cette ronde, documenté ci-dessus plutôt que corrigé rétroactivement (aucune
preuve n'existe pour ces jours, donc rien n'est comblé [DH-COS-002]).

**Écart brief↔table** : aucun — les décisions référencées dans le brief du
2026-08-02 (escalades + priorités du jour) correspondent toutes à des
décisions déjà en table depuis le 16/07 (DEC-2026-0716-01 à 07).

## §2 Skills proposés

Aucun skill proposé à ce jour — `.claude/skills-proposed/` reste vide
(aucun sous-dossier directeur). Source : `find
/workspace/.claude/skills-proposed -mindepth 1` (2026-08-02, 0 résultat).
Inchangé depuis la création du dossier (14/07), y compris pendant le
silence du comité.

## §3 Priorités / OKR de la semaine

**Toujours absent** (`priorites_semaine` jamais alimentée dans `deos_state`,
sur les 4 rondes CoS ayant pu vérifier cette clé : 14/07, 15/07, 16/07,
02/08). Signalé à nouveau à Sam ; aucune estimation ne sera produite par le
CoS à sa place.

Cadre semestriel disponible (`okr_h2`, scénario NOMINAL, validé par Sam le
14/07) : O1 Revenu (11 clients signés au 31/12 dont 3 Team, MRR ≥ 4 800 €),
O2 Lancement (produit prêt 31/08, lancement payant septembre), O3
Visibilité (13 contenus avant fin octobre, livre blanc v1 au 30/11), O4
Qualité (0 incident visible client, exécutions réussies ≥ 95 %), O5
Gouvernance (0 décision oubliée, brief à l'heure ≥ 95 %).

**O5 est aujourd'hui objectivement en risque** : le silence de 16-17 jours
du comité (11 rondes CoS/commercial/marketing/cs ratées sur les jours
ouvrés du 17 au 31/07) place le taux de « brief à l'heure » très en dessous
de 95 % sur la période, et 2 décisions en_execution sont passées en risque
d'oubli sans relance possible pendant la coupure.

Priorités du jour du brief 2026-08-02 (CEO, ordre décroissant de gravité) :
(1) débloquer l'échec systémique BUILD (DEC-2026-0716-06/07, échéance démo
Team 15/08) ; (2) rétablir la remontée d'information des 4 directeurs
silencieux ; (3) débloquer l'amont commercial (DEC-2026-0716-01/02,
échéance régime B 01/09) ; (4) fixer le seuil d'alerte cash
(DEC-2026-0716-03) ; (5) statuer sur les livrables marketing
(DEC-2026-0716-04/05).

## §4 Cash

**Surveillance cash alimentée mais toujours sans seuil d'alerte — inchangé
depuis le 14/07 (19 jours sans mise à jour, y compris pendant le silence).**
Déclaré par Sam le 14/07 : solde 0 €, MRR réel 0 €, compte professionnel en
cours d'ouverture (source : `deos-state get cash_suivi`, maj_par sam,
2026-07-14T12:59:27Z). `seuil_alerte_solde` est `null` et
`echeances_connues` est vide : **aucune alerte ne peut être déclenchée par
le CoS.** Tracé par DEC-2026-0716-03 (`attente_sam`, 17 jours).

## §5 Relances émises

**2 relances émises cette ronde** — la première pour chacune des 2
décisions `en_execution`, aucune n'ayant jamais reçu de relance
auparavant (DH-COS-004 respecté : une par cycle, pas de harcèlement) :

1. **DEC-2026-0714-01** (interface web comité) — 19 jours sans preuve
   d'activité. Le seuil de 3 jours était franchi le 17/07, mais la coupure
   du comité a empêché toute relance jusqu'à ce jour.
2. **DEC-2026-0716-06** (RapportIncident BUILD, routage delivery) — 17 jours
   sans livrable depuis la création.

Les 6 décisions `attente_sam` (DEC-2026-0716-01/02/03/04/05/07) ne relèvent
pas du mécanisme de relance (réservé aux décisions accordées/en_execution)
mais sont escaladées vers Sam ci-dessous compte tenu de leur âge (17j) et
de la proximité d'échéances produit/commerciales.

## Escalades de cette ronde

1. **Incident de gouvernance** : silence total du comité du 17/07 au 01/08
   (16 jours, crédit API épuisé), et silence **toujours en cours** pour
   commercial/marketing/CS ce jour (17e jour).
2. **6 décisions attente_sam bloquées 17 jours** (DEC-2026-0716-01 à 07) :
   demande d'arbitrage explicite à Sam, notamment sur l'accès aux logs du
   worker BUILD (échéance démo Team 15/08) et l'amont commercial (échéance
   régime B 01/09).

## Score d'exécution

**70/100 — ambre.** Calcul : base 100 − 8×0 (décisions en retard 3-7j :
0/2 éligibles — les 2 `en_execution` dépassent déjà 7j) − 15×2 (décisions
en risque d'oubli >7j : DEC-2026-0714-01, DEC-2026-0716-06) − 5×0 (skills
proposés en attente >14j : file vide) − 10×0 (priorité de semaine sans
activité à mi-semaine : non applicable, `priorites_semaine` jamais
définie) = **70**.

Ce score ne capture pas directement le coût du silence de 16-17 jours
(impossibilité de relancer à temps) : c'est documenté séparément
ci-dessus, en alerte de premier plan, et ne doit pas être lu comme
« inchangé » ou anodin par rapport au score 100/vert de la dernière ronde
exploitable (16/07) — la situation s'est réellement dégradée pendant la
coupure, elle n'a simplement pas pu être mesurée en continu.
