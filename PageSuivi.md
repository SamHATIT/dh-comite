# Page de suivi — Digital·Humans

Dernière ronde : 2026-08-14 07:15 UTC (Chief of Staff)
Précédente ronde de référence : 2026-08-13 07:14 UTC

## 0. Score exécution — 0/100 (rouge), lecture stricte de la formule

**Ce chiffre demande une explication avant d'être lu comme une alerte.**

Formule du skill appliquée littéralement à l'ensemble des 46 décisions
`accordee`/`en_execution` (pas seulement aux quelques décisions vérifiées
une à une comme les rondes précédentes) :
- 23 décisions sans signe d'activité tracé depuis 4 à 7 jours → −8 × 23 = −184
- 10 décisions sans signe d'activité tracé depuis plus de 7 jours (« en risque d'oubli ») → −15 × 10 = −150
- 0 skill proposé en attente >14j → 0
- Priorité de semaine rang 2 (B2 code, 6 sites) toujours à 0 avancement en jour 5/7 → −10
- Total théorique −344, plancher appliqué → **0/100**

**Pourquoi ce chiffre change aussi brutalement vs hier (37/100) : ce n'est pas
une dégradation réelle du dispositif, c'est un changement de règle de compte
de ma part.** Les rondes du 12 et 13/08 ne comptaient dans le malus que les
décisions individuellement vérifiées (1 à 4 items), pas l'ensemble du stock.
En appliquant la formule à la lettre — comme le mandat du 12/08 ("compter ne
suffit pas") l'exige — le vrai stock de décisions dormantes apparaît : sur
les 46 `accordee`/`en_execution`, 33 n'ont aucune trace d'activité récente en
base (`updated_at` comme proxy, faute de mieux — limite assumée ci-dessous).
Je choisis de le montrer plutôt que de continuer à compter comme avant.

**Contrepoint factuel, vérifié ce jour, qui nuance le chiffre brut** : la
journée du 13/08 a été une des plus actives depuis longtemps —
- Sam a débloqué de vive voix les 3 « GO orphelins » signalés depuis le
  10-12/08 (DEC-2026-0809-03 → clos, DEC-2026-0810-10 → clos,
  DEC-2026-0810-09 → accordée confirmée), tous avec preuve datée 13/08.
- La chaîne BUILD a connu sa **première tentative en 11 jours** :
  exécution 166, phase `data_model`, agent Raj, lancée le 13/08 à 13h03Z,
  échouée 4 secondes plus tard (`No batches generated`) — vérifié directement
  dans `v_deos_build_phases` via `$DEOS_RO_DSN`. Aucune nouvelle tentative
  depuis (18h).
- Le prix obsolète de Sophie (DEC-2026-0813-01) est **corrigé dans le
  fichier** `backend/prompts/agents/sophie_pm.yaml` (diff vérifié dans
  `/repo`, working tree) — mais **non commité** (aucun commit depuis
  293adec du 10/08). Travail réel, non versionné : fragile.
- `cash_suivi` a été **réactivé par Sam lui-même** le 13/08 (voir §4).

**Limite méthodologique assumée** : `updated_at` sur la table `decisions`
n'est pas toujours un signe d'activité du porteur — pour une partie des 33
décisions (celles touchées en bloc le 10/08 lors du tri, ou le 13/08 lors
des confirmations de Sam), c'est une trace de bureaucratie interne, pas une
preuve de travail. Je n'ai vérifié individuellement (git, curl, base prod)
que les décisions citées avec preuve dans ce document ; pour les autres, je
m'appuie sur l'absence de toute preuve contraire trouvée en base ou en repo.

## 1. Décisions — dette d'exécution

**46 décisions `accordee`/`en_execution`** (40 + 6), en hausse de +11 vs hier
(35). Hausse expliquée : +5 décisions nouvelles créées et accordées le 13/08
(légal ×2, financier ×2, CoS ×1) + Sam a fait passer plusieurs décisions
d'`attente_sam` à `accordee`/`clos` dans l'après-midi du 13/08 en résolvant
l'escalade des 3 GO orphelins. Ce n'est pas une aggravation de l'inexécution :
c'est le stock d'arbitrage qui s'est vidé dans le stock d'exécution, ce qui
est le sens normal du flux.

**5 décisions `attente_sam`** (en forte baisse vs 18 hier matin, grâce à
l'arbitrage de Sam) :

| id | objet (résumé) | âge | destination |
|---|---|---|---|
| DEC-2026-0813-06 | Site jamais basculé de la page Entracte vers le vrai site (`/var/www/dh-preview` prêt, jamais mis en prod) — cause racine des 3 pages légales vides | 1j | **Sam directement** (geste hébergeur, risque juridique — site marchand sans mentions légales) |
| DEC-2026-0813-07 | Chat agents au niveau tableau de bord — bloqué par le même défaut RAG que 0813-09 | 1j | Sam (arbitrage produit) |
| DEC-2026-0813-08 | Relance CoS à Delivery : 11 lignes de statut attendues à la ronde d'aujourd'hui | 1j | réponse attendue de Delivery aujourd'hui — non encore vérifiable (Delivery n'a pas encore posté son rapport du 14/08 au moment de cette ronde, 07h15Z) |
| DEC-2026-0813-09 | Validation conjointe Legal+Delivery sur le périmètre réel du correctif de cloisonnement RAG | 1j | Sam (arbitrage) |
| DEC-2026-0813-10 | Sortir du harnais claude -p, router les LLM par fournisseur | 1j | Sam (arbitrage d'architecture) |

Aucune de ces 5 n'a encore dépassé le délai normal de réponse (toutes datées
du 13/08). Pas de nouvelle escalade « 2 relances sans réponse » aujourd'hui.

### Les trois plus anciennes décisions accordées (12 jours, porteur Delivery)

| id | objet | pertinente ? | bloquée par | porteur |
|---|---|---|---|---|
| DEC-2026-0802-01 | Démo phare Agentforce → DH → sandbox | Oui, échéance de preuve BUILD au 15/08 (demain) | le même défaut technique que ci-dessous : la chaîne BUILD a tenté un redémarrage le 13/08 et a échoué (`No batches generated`) | delivery |
| DEC-2026-0802-02 | BUILD — reprise sur incident : ne pas repartir en phase 1 à chaque relance | À reconfirmer — l'échec du 13/08 est un nouveau mode de panne, ce correctif visait l'ancien symptôme | rien d'externe : correctif jamais écrit, 0 commit en 12 jours | delivery |
| DEC-2026-0802-03 | BUILD — travail incrémental (delta), ne renvoyer que les lots rejetés | Idem 0802-02 | rien d'externe, jamais engagé | delivery |

Sur ce même lot du 02/08, 4 autres décisions ferment le même âge (12 jours) :
DEC-2026-0802-04 (Email-to-Case Salesforce jamais migré — preuve au dossier
confirme explicitement « exécution non prouvée, pas de clôture »),
DEC-2026-0802-05/06 (missions juridiques hors France / audit conformité —
aucune trace de livrable), DEC-2026-0802-07 (AI Act art. 50 — **bascule en
risque d'oubli aujourd'hui**, dernier geste vérifiable le 06/08 sur
`config/legal/mentions_ia.md`, 8 jours sans retouche).

### Les 10 décisions en risque d'oubli (>7j sans activité tracée)

DEC-2026-0802-01, 02, 03, 04, 05, 06, 07 (7 décisions du 02/08, 11-12j) +
DEC-2026-0804-01, 02, 05 (3 décisions du 04/08, 10j — suivi des chantiers O2,
ré-arbitrage export logs, interface web globale). Toutes portées par
Delivery, sauf les deux missions juridiques (0802-05/06) dont le porteur
Legal formel reste à confirmer.

### Relances émises ce jour (une par décision, pas de nouvelle depuis leur dernier cycle)

- DEC-2026-0802-02 / 0802-03 — Delivery, 5e cycle, aucun changement.
- DEC-2026-0802-04 — Delivery, migration Email-to-Case jamais commencée, 4e cycle.
- DEC-2026-0802-07 — Legal, bascule en risque d'oubli ce jour, 3e cycle.

## 2. Skills proposés

`.claude/skills-proposed/` est **vide** (vérifié : `ls -la`, aucun sous-dossier).
Rien à instruire, rien à relancer.

## 3. Priorités de la semaine (10-16/08, jour 5/7)

Version en base datée du 10/08 (non rafraîchie depuis 4 jours — à mettre à
jour par le CoS, pas une action pour Sam) :

| rang | titre | état vérifié ce jour |
|---|---|---|
| 1 | Réouverture du site | Toujours « Entracte » sur les 7 URL testées (accueil + 6 pages), curl direct 14/08 07h. Cause racine désormais nommée (DEC-2026-0813-06) : bascule hébergeur jamais faite, `/var/www/dh-preview` prêt et non déployé. |
| 2 | B2 code — correctif 6 sites `projects.py` | GO reconfirmé par Sam le 13/08 (DEC-2026-0810-09). 0/6 sites corrigés — vérifié : aucun commit ni modification de fichier depuis. **Malus mi-semaine appliqué.** |
| 3 | BUILD tracé avant le 15/08 (demain) | Tentative réelle le 13/08 13h03Z (exec166, phase data_model), échec technique en 4 secondes (`No batches generated`). Checkpoint à J-1. |
| 4 | Support visuel Crédit Logement | Marqué complet le 10/08. |
| 5 | Canal support minimal CS au 01/09 | Confirmé normal par Sam (rapport CS du 13/08), pas d'alerte. |

## 4. Cash — surveillance RÉACTIVÉE par Sam

Contrairement à hier (signalée inactive 7 jours), `cash_suivi` a été mis à
jour **par Sam lui-même** le 13/08 à 10h22 UTC (vérifié : `maj_par='sam'` en
base). Chiffres, tous attribués :

- Budget mensuel **500 EUR**, crédité le 1er de chaque mois, validé par le
  CFO externe — remplace le plafond de 150 USD (déclaré caduc par Sam).
- Consommé du 1er au 13/08 : **242 EUR** (253,38 USD Anthropic, relevé
  console exact + 10 USD GPU consommés sur 50 USD déjà achetés).
- Solde restant déclaré : **258 EUR**.
- Tendance : 57 USD le 10/08 (pic tests GPU) → 10 USD le 13/08, division par
  trois en deux jours suite à la bascule Sonnet et au plafond de tours du
  11/08.
- Projection fin août : ~350 USD toutes sources si la tendance tient — **sous
  le budget de 500 EUR**, aucun seuil franchi.

**Note de vigilance, pas une alerte** : le champ `solde_declare` de
`cash_suivi` a changé de nature. Il désignait jusqu'ici la trésorerie de
l'entreprise (0 EUR déclaré le 14/07, jamais actualisé). Il désigne
maintenant le reste du budget API/infra mensuel (258 EUR sur 500). Sam a
clos DEC-2026-0810-10 sur cette base — je le signale pour que la distinction
soit explicite au comité, sans rouvrir une question qu'il a tranchée.

## 5. Écart brief/table

Le dernier brief généré (13/08 07h35) ne référence pas les 5 décisions
`attente_sam` créées après cet horaire (0813-06 à 10). Ce n'est pas un défaut
de traçabilité : elles n'existaient pas encore au moment de la génération. Le
brief du jour (14/08), pas encore généré au moment de cette ronde, devra les
inclure.
