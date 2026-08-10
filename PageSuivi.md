# Page de suivi — Digital·Humans
Générée par le Chief of Staff · ronde du 2026-08-10 + **complément hebdomadaire du 10/08 (10h00Z)** + **temps 4 du 10/08, 15h40Z — session benchmark Fable, 2 clôtures sur preuve, priorités requalifiées, recomptage avec ventilation actions/constats**.

Sources : `psql "$COMITE_DB_DSN"` (table `decisions`) · `git -C /repo show --stat 293adec` (vérifié ce jour 15h59Z) · `git -C /repo log --since=2026-08-02 --until=2026-08-10 -- backend/app/services/pm_orchestrator_service_v2.py` · `deos_state_history` (rapport_commercial du 07/08T07:12:22Z, rapport_legal du 08/08, rapport_cos du 10/08 09h56Z) · fichiers `/workspace/config/contenus/CONT-2026-0804-02/03/04`, `/workspace/config/offre_dh.md` (vérifié non modifié) · `curl -o /dev/null -w '%{http_code}' https://digital-humans.fr/` (15h47Z et 16h03Z, 200, titre Entracte) · `/repo` (commits 03fc6e6, 3bcd757, 293adec vérifiés) · `/workspace/bin/memoire` (opérationnel ce jour) · `find .claude/skills-proposed` · `deos-state get/set priorites_semaine`.

---

## §0 — Le chiffre qui compte : dette d'exécution, avec ventilation actions/constats (nouveau ce jour)

| mesure | date/source | accordées | en_execution | **total ouvert** |
|---|---|---|---|---|
| 1 | 08/08 matin, brief CEO | — | — | **24** |
| 2 | 09/08 matin, brief CEO | 28 | 2 | **30** |
| 3 | 10/08 07h06 (ronde CoS) | 31 | 2 | **33** |
| 4 | 10/08 09h30 (comptage direct de Sam) | 35 | 2 | **37** |
| 5 | 10/08 10h00 (complément CoS, après 2 clôtures + 4 requalifications) | 29 | 6 | **35** |
| 6 | 10/08 ~10h30 (clôture de comité par le CEO, confirmée en base) | 29 | 5 | **34** |
| 7 | **10/08 15h59Z (temps 4, après ~26 décisions de la session Sam + 2 clôtures CoS ce jour)** | 53 | 5 | **58** |

**La hausse 34 → 58 n'est pas une dérive de l'exécution** : elle vient des ~26 décisions créées cet après-midi par la session de Sam (benchmark Fable), dont une grande partie sont des **constats/consignes de session** (corrections d'interprétation sur la composition d'équipe, résultats de test GPU, clarifications de principe) qui n'appellent aucune exécution distincte. D'où la ventilation ci-dessous, demandée pour la première fois ce jour.

### Ventilation demandée : décisions-actions vs constats/consignes

| catégorie | définition | compte |
|---|---|---|
| **Décisions-actions** | nomment un porteur et un livrable/geste encore attendu | **39** |
| **Constats/consignes de session** | corrigent une compréhension, posent une règle, ou documentent un résultat déjà vérifié — rien à exécuter en propre | **19** |

Le bloc `DEC-2026-0810-11` à `-19` cité par le CEO est exactement ce deuxième groupe pour 7 de ses 9 décisions (`-11, -12, -14, -15, -16, -17, -19` — `-13` et `-18` ont été clôturées ce jour, voir point de contrôle ci-dessous). S'y ajoutent 12 autres constats répartis sur la semaine (ex. `DEC-2026-0808-12`/`-09`/`-13` déjà « clos en substance » mais pas formellement, `DEC-2026-0809-06`/`-08`/`-09`, `DEC-2026-0810-05`/`-06`/`-20`/`-21`). Liste complète disponible sur demande — méthode : absence de porteur+livrable distinct nommé, ou texte à dominante rétrospective/déclarative.

**La tendance qui compte est celle des actions : 39.** Comparée au dernier chiffre non ventilé (34 à 10h30), la hausse réelle de dette-actions ce jour est modeste (~+5, portée par des décisions neuves comme `DEC-2026-0810-02/03/04/08/09/10`), la majorité de la hausse brute étant des constats.

### Point de contrôle temps 4 — deux clôtures sur preuve

**DEC-2026-0810-18 (état des lieux aveugle, greenfield) → CLOSE.** Vérifié `git -C /repo show --stat 293adec` : commit réel, message confirme le mode déduit de la présence d'une org (plus du type déclaré à la création), écart journalisé, et **4 projets vérifiés** (105, 107, 108, 109) tous rattachés à une org réelle — 3 étaient déclarés `greenfield` à tort. Conforme à la preuve annoncée. Preuve stockée : commit `293adec9d4f8034bd75c1ae15f2551400a018d0c`.

**DEC-2026-0810-13 (affichage trompeur des étapes sautées) → CLOSE.** Lecture confirmée du texte de `DEC-2026-0810-14`, accordée : « qui remplace le correctif d'interface de DEC-2026-0810-13 ». La matière (agent affiché « en cours » alors qu'il ne fait rien) est désormais traitée à la racine par la composition d'équipe selon le besoin (`-14`), pas par un correctif d'affichage. Preuve stockée : remplacement par `-14`, elle-même accordée.

---

## §1 — Décisions (115 au total : 10 attente_sam · 53 accordée · 5 en_execution · 43 clos · 4 refusée)

### 1.1 Les trois plus anciennes décisions-actions accordées/en_execution jamais exécutées
**Corrigé ce jour** : le classement précédent citait `DEC-2026-0802-07` et `DEC-2026-0802-05` comme 2ᵉ/3ᵉ plus anciennes — elles sont en réalité 6ᵉ et 7ᵉ dans l'ordre chronologique exact des décisions-actions du 02/08 (`-01` 15h33, `-02` 16h57, `-03` 17h24, `-04` 17h33, avant `-05` 20h46 et `-06`/`-07` 20h48-20h52). Corrigé par tri direct sur `date`.

| id | quoi | âge | encore pertinente ? | bloquée par quoi | par qui |
|---|---|---|---|---|---|
| **DEC-2026-0714-01** | Interface web globale de suivi du comité | **27j** | Oui, **active** — 10 gabarits de graphiques livrés et intégrés ce jour (commits `5f06c15`→`7f12845`), arbitrage prévu au comité du 10/08 (aujourd'hui). | Rien de bloquant identifié : activité du jour même, pas un cas de silence malgré l'âge nominal. | Collectif/DSI, porteur nommé Delivery. |
| **DEC-2026-0802-01** | Démo phare (boucle fermée Agentforce → DH → sandbox) | **8j** | Oui — c'est exactement R3 des priorités de la semaine. | Le pipeline BUILD tracé jusqu'au sandbox n'est pas encore complet (0 ligne `v_deos_build_phases` pour l'exécution du jour). Explicitement gatée après le 15/08 par `DEC-2026-0806-01` (close) : ce n'est pas un oubli, c'est une porte posée en connaissance de cause. | Directeur Delivery. |
| **DEC-2026-0802-02** | Evolution BUILD — reprise sur incident (BUILD v2 recommence à la phase 1 à chaque relance) | **8j** | Oui, correctif jamais confirmé. Vérifié : `git -C /repo log --since=2026-08-02 --until=2026-08-10 -- backend/.../pm_orchestrator_service_v2.py` ne montre **aucun commit dédié** à cette reprise entre le 02/08 et le 10/08 (seuls trouvés dans la fenêtre : le bug NoneType phase2 `120635d` et le fix greenfield `293adec`, sujets différents). Un mécanisme `last_completed_phase` existe en code mais date de février (`86aa448`), avant l'incident signalé — non re-vérifié depuis. | Absence de preuve de correctif post-02/08 ; à confirmer par le Delivery. | Directeur Delivery — **candidat à relance nommée au prochain cycle**. |

**Franchissement du seuil de 7j** : `DEC-2026-0802-01` et `DEC-2026-0802-02` sont à 8 jours — en risque d'oubli au sens strict, mais la première est gatée explicitement (pas un oubli), la seconde n'a pas de preuve de traitement et doit être relancée.

### 1.2 — Historique de la ronde 10h00-10h30 (rappel, inchangé depuis le complément hebdomadaire)
- CoS (10h00) : `DEC-2026-0716-01`, `DEC-2026-0716-05` → clos · `DEC-2026-0803-03/04/05`, `DEC-2026-0806-12` → en_execution · `DEC-2026-0810-04` créée (curseur ecrire_base).
- CEO (~10h30) : `DEC-2026-0802-08`, `DEC-2026-0803-02`, `DEC-2026-0808-05`, `DEC-2026-0806-01` → clos · `DEC-2026-0810-05` (accordée) · `DEC-2026-0810-06/09/10` (attente_sam, escalades) · `DEC-2026-0810-07` (close) · `DEC-2026-0810-08` (accordée).
- **Temps 4 (15h40-16h00, ce jour)** : session Sam/benchmark Fable, ~26 décisions créées (`DEC-2026-0810-11` à `-30`) · CoS : `DEC-2026-0810-13`, `DEC-2026-0810-18` → clos (voir §0).

---

## §2 — Skills proposés par les directeurs
Toujours vide : `find /workspace/.claude/skills-proposed -mindepth 1` → 0 résultat, vérifié à nouveau ce jour (16h00Z). Aucun skill en attente de validation de Sam.

---

## §3 — Priorités / OKR de la semaine du 10 au 16/08 — requalifiées ce jour (temps 4), remplacent la version de 10h14Z

`priorites_semaine` mise à jour via `deos-state set priorites_semaine --par cos` à 16h00Z environ. Deux requalifications factuelles (R2, R3) et une intégration (R4), sur constat du rapport Delivery de l'après-midi.

| rang | titre | responsable | appui | OKR | statut / échéance |
|---|---|---|---|---|---|
| 1 | **Réouverture du site** | Sam | Legal · Delivery (mention IA widget Sophie) · Marketing | O2, O3 | **Vérifié en Entracte à 15h47Z** (`curl` 200, titre « Entracte — Digital·Humans »), revérifié 16h03Z, inchangé. `DEC-2026-0809-01`/`DEC-2026-0810-06`. |
| 2 | **B2 volet CODE — correctif `projects.py`** *(requalifiée)* | Delivery | — | O4 | Identifiants chiffrés (`DEC-2026-0810-20`) MAIS `projects.py` n'a **aucun commit** — 6 sites actifs, régression immédiate sur Test Salesforce/Git Connection (projets 84/106) et réintroduction de clair à la prochaine écriture via le modal Settings (source : rapport_delivery, complément temps3 CEO 15h54Z). Pattern déjà validé (`03fc6e6`), go déjà donné (`DEC-2026-0810-09`), 5-15 USD. Verdict T1-T4 dû le 11/08. |
| 3 | **BUILD tracé jusqu'au sandbox avant le 15/08** *(requalifiée)* | Delivery | — | O2 | Preuve du jour (10 composants déployés + versionnés, commit `99dd9d8`) réelle mais **hors pipeline tracé** (0 ligne `v_deos_build_phases`) — il faut une exécution complète dans le flux orchestré. Fourchette delivery 12-14/08, plafond 20 EUR (`DEC-2026-0809-03`). |
| 4 | **Support visuel Crédit Logement** *(complétée)* | Marketing | Commercial | O1 | Relecture Sam le 12/08 (`DEC-2026-0810-08`) + intégration démonstration locale avec ses limites (`DEC-2026-0810-30`) : coût réel 2,35 USD (exec 167), écart qualité Emma (`DEC-2026-0810-12`), limite Naaia maintenue. |
| 5 | **Canal de support minimal au 01/09** | Customer Success | — | O1, O4 | Inchangée. Stopgap coût nul. |

**Points de suivi hors priorités** :
- Créneau Sam (`DEC-2026-0810-06` option a) désormais élargi à la saisie des 11 Leads Salesforce (`DEC-2026-0810-29`, 20-30 min) et au solde de trésorerie (`DEC-2026-0810-10`, 2 min).
- `pipeline_commercial` saisi ce jour (11 entrées, `DEC-2026-0810-04` exécutée).

---

## §4 — Cash (DH-COS-003 : lecture/alerte, jamais d'estimation de ma part)
- **Solde de trésorerie : 0 EUR, déclaré par Sam le 2026-07-14 — inchangé depuis 27 jours.** `cash_suivi` non alimenté depuis le 02/08 (`maj: 2026-08-02` en base, vérifié `deos-state get cash_suivi`) — surveillance toujours inactive, signalé sans estimation.
- **Seuil d'alerte : 50 EUR** (Sam, 03/08, `DEC-2026-0716-03`, clos). Solde déclaré sous ce seuil, mais périmé.
- **Point de suivi hors priorités ajouté ce jour** : le créneau Sam désormais élargi couvre la saisie du solde de trésorerie (`DEC-2026-0810-10`, 2 min) — c'est le geste minimal qui réactiverait la surveillance ; non fait à ce jour.
- **Budget API** : dépassement chiffré signalé par le Financier (`DEC-2026-0810-10`, attente_sam) — relayé sourcé, pas de projection de mon initiative.

---

## §5 — Relances émises ce jour (temps 4)
| destinataire | décision(s) | objet | pourquoi |
|---|---|---|---|
| Directeur Delivery | DEC-2026-0802-02 | Reprise sur incident BUILD v2 — aucun commit dédié trouvé dans la fenêtre 02/08-10/08 | 8j, franchit le seuil de risque d'oubli, pas de preuve de traitement |
| Directeur Delivery | R2 (correctif `projects.py`, 6 sites) | Verdict T1-T4 dû le 11/08 | Échéance à J+1, régression de sécurité active |
| Directeur Delivery | R3 (BUILD tracé jusqu'au sandbox) | Fourchette delivery 12-14/08 | Preuve du jour hors pipeline tracé, à corriger avant le 15/08 |
| Sam (info, via CEO) | DEC-2026-0810-06/09/10 | Réouverture, GO sécurité B2, visibilité cash/budget | Escaladées par le CEO, relayées sans sollicitation directe |
| Sam (info) | — | Dette totale 34 → 58 (dont 39 actions / 19 constats) | Premier recomptage avec ventilation — le chiffre brut ne doit plus être lu seul |

---

## §6 — Complément hebdomadaire (rappel, produit à 10h00Z ce jour — inchangé)
Voir version précédente : tendances_7j, plan_semaine, besoin_arbitrage (`DEC-2026-0810-04`, curseur `ecrire_base`, toujours en attente_sam), point mort Commercial corrigé (`DEC-2026-0810-04` créée).

---

## §7 — Score d'exécution
Score du matin : 0/100 (plancher), calcul détaillé dans `rapport_cos` du 2026-08-10T07:08:43Z. Stock ouvert : 33 → 37 → 35 → 34 → **58 (dont 39 actions, 19 constats)** après la session de l'après-midi. Recalcul formel du score à la prochaine ronde quotidienne, sur la base ventilée actions/constats introduite ce jour.
