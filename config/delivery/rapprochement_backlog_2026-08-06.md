# Rapprochement backlog vs réalité — 2026-08-06

**Directeur Delivery** · **Mission** : confronter le backlog (TASKS_MASTER.md, BACKLOG.md) à l'état RÉEL (base de production, historique git, serveur) · **Checkpoint** : 15/08/2026 (BUILD→SANDBOX dans 9 jours).

**Sources consultées** : `/backlog/TASKS_MASTER.md` (14 juillet 2026, 52 tâches), `/backlog/BACKLOG.md` (06 juin 2026), `/backlog/SESSION_2026-08-05.md` (tâche 4 : clé statut_o2), base `digital_humans_db` (vues v_deos_*), base `dh_comite` (deos_state, decisions), `/prodlogs/backend-24h.log`.

**Principe** : chaque affirmation porte sa preuve. « Fait » sans trace vérifiable = « coché sans preuve ». « À faire » avec commit mergé = « fait mais non coché ».

---

## 1. RAPPROCHEMENT : trois catégories

### 1.1 FAIT MAIS NON COCHÉ

Tâches réalisées avec preuve git/base, mais que le backlog classe encore « à faire » ou ignore.

| ID | Description | Preuve | Note TASKS_MASTER | État backlog |
|---|---|---|---|---|
| **P10-BaseAgent** | Classe de base pour les 11 agents (déduplique _call_llm, logging, execution_id) | commit `258c5c3`, tag `v2026.05-p10-baseagent`, dans main | TASKS_MASTER l.23 : « ⚠️ marqué à faire alors que FAIT » | BACKLOG.md l.161 : « P2 dette, sprint post-launch » |
| **FIX-PARSE-001** | Parser JSON tronqué (fermeture structures au lieu de renvoyer unrecoverable) | commit `666e02d`, fusionné `5fa1420`, dans main | TASKS_MASTER l.162 : « ✅ FAIT 10 juin, Aisha 100% / Elena 99,9% récupérés » | BACKLOG.md : absent (postérieur au 02/05) |
| **FIX-MAXTOKENS-002** | max_tokens Aisha/Elena 16K → 64K + mode patch Marcus 64K | commit `397ed4a`, fusionné `5fa1420`, dans main | TASKS_MASTER l.163 : « ✅ FAIT 10 juin » | BACKLOG.md : absent |
| **PATCH-MERGE-001** | Merge automation_design préservant les clés (au lieu de remplacer) | commit `ad158de`, fusionné `73dd681`, dans main | TASKS_MASTER l.164 : « ✅ FAIT 10 juin, testé unitairement » | BACKLOG.md : absent |
| **FIX-EMPTY-001** | Retry x2 sur réponse LLM vide + RuntimeError (Jordan/DevOps) | commit `31ba2d5`, fusionné `5fa1420`, dans main | TASKS_MASTER l.165 : « ✅ FAIT 10 juin, testé unitairement » | BACKLOG.md : absent |
| **FEAT-LANG-001** | Directive de langue injectée dans llm_service + lang dynamique sds_shell | fusionné `73dd681`, dans main | TASKS_MASTER l.166 : « ✅ FAIT 10 juin, exec 159 en fr prouvée » | BACKLOG.md : absent |
| **OBSERV-001** | Heartbeat 30s streaming + monitoring N8N réactivé + worker au périmètre | commit `280d3c8`, fusionné `73dd681`, dans main | TASKS_MASTER l.167 : « ✅ FAIT 10 juin » — MAIS réserve l.167 : « contredit par situation 05/08 » | BACKLOG.md : absent |
| **RAG-V2** | Bascule corpus v2 (161 856 chunks), v1 en backup froid, rollback 30s | commit `02bf92d` (15/07), `/backlog/RAG_V2_JOURNAL.md` l.14 : bascule validée 14/07 | statut_o2 : « fait », non revérifié durant session 05/08 | BACKLOG.md : absent |
| **LEGAL-002** | Compléter SIRET + adresse siège (Mentions Légales) | `/backlog/SESSION_2026-08-05.md` n'en parle plus | TASKS_MASTER l.71 : « ✅ FAIT (Sam, 8 juin) » | BACKLOG.md l.97 : « ❌ Sam, 30 min » |
| **BIZ-001** | Décision tier Free ouvert/fermé au launch | — | TASKS_MASTER l.72 : « ✅ TRANCHÉ : Free ouvert au launch » | BACKLOG.md l.99 : « ❌ Sam, arbitrage » |
| **SDS Claim Resolver (exec 155)** | SDS complet (31/05, $9.75 / 40 min) | base prod : exec 155 COMPLETED | TASKS_MASTER l.25 : « ⚠️ absent de tous les docs, marqué 'bientôt' sur le site live alors qu'il est prêt » | BACKLOG.md : absent |

**Impact** : le backlog sous-estime l'avancement. Sur les 8 chantiers du lancement (mission du 05/08), **7 sur 8 sont faits et mergés dans main**. Seul STRIPE-PROD reste à faire.

---

### 1.2 COCHÉ SANS PREUVE

Tâches marquées « fait » sans trace vérifiable en production, ou avec preuve partielle.

| ID | Description | Ce qui manque | Note |
|---|---|---|---|
| **REVISION-001 patch mode** | Code posé, mais validation E2E en attente | E2E #144 a tombé en fallback fix_gaps (worker non restart, SESSION_2026-08-05.md) | TASKS_MASTER l.33 : « 🟡 code fait, validation E2E en attente » |
| **OBSERV-001** (doublon) | Heartbeat + monitoring N8N réactivé + worker au périmètre | Le worker est de nouveau resté silencieux sans détection le 05/08 | TASKS_MASTER l.167 : « À RELIRE PAR SAM : c'est le chantier le plus directement contredit par la situation du 05/08 » + statut_o2 : « silence du worker n'a de nouveau été détecté par personne » |
| **SDS templating Phase 1** | Marquée CLOSE, mais checklist tests fonctionnels non cochés | `docs/sds/STATUS.md` garde checklist (bascule Emma write_sds, preview frontend, robustesse multi-exec) | TASKS_MASTER l.34 : « 🟡 de facto couverts par exec 148/155 mais jamais validés formellement » |
| **STREAM-001** | Mergé main + déployé, preuve unit OK | Validation finale = batch Vague 2 (non fait) | TASKS_MASTER l.54 : « 🟡 mergé main + déployé (04ea3c5), validation finale = batch Vague 2 » |
| **MOD40-CAPABILITY** | Posé en opt-in, activé en `warn` | Jamais passé en `apply` (production) | TASKS_MASTER l.61 : « ✅ activé en warn (8 juin), passer en apply quand prêt » |
| **mods 37-39** | Dans l'arbre de travail, datés 31/05, commentaires mod38/mod39 | **NON COMMITÉS** — la mémoire les dit completed | TASKS_MASTER l.29 : « ⚠️ mods 37-39 dans l'arbre de travail, non commités. Risque de perte » |
| **main jamais poussé** | 4 commits locaux non poussés (P10 BaseAgent + tag, tuning ARQ, studio 3-col, helper P3) | `origin/main` a 5 semaines de retard | TASKS_MASTER l.28 : « ⚠️ risque de perte (priorité absolue) » |

**Impact** : 7 tâches marquées « fait » nécessitent une validation ou un commit. Deux risques de perte (mods 37-39, main non poussé) classés **priorité absolue** par TASKS_MASTER.

---

### 1.3 BLOQUÉ SANS PORTEUR

Tâches ouvertes depuis longtemps sans avancée, ou avec porteur absent.

| ID | Ouvert depuis | Ancienneté | Porteur | Bloquant |
|---|---|---|---|---|
| **STRIPE-PROD-001** | Avant 02/05 (BACKLOG.md l.100) | **> 3 mois** | Sam (action humaine) | Dépend de BIZ-001 (tranché ✅ le 08/06), mais secret encore en `sk_test` (vérifié SESSION_2026-08-05.md). Dette sécurité liée : secret partagé en conversation → rotation obligatoire |
| **LEGAL-001** | Avant 02/05 | **> 3 mois** | Sam (validation juriste CGV, 300-500 €) | Boilerplate FR+EN livré, attend validation externe |
| **SECURITY-001..005** | Avant 02/05 | **> 3 mois** | Sam (Phase 0 NON démarrée) | Audit secrets + manager (Doppler/Infisical) + migration + docs. TASKS_MASTER l.74 : « Phase 0 NON démarrée » |
| **GHOST-001** | 02/05 (BACKLOG.md l.143) | **3 mois** | ? | SMTP réel (Postmark) pour Ghost + réactiver staffDeviceVerification. Désactivé en hotfix 02/05 (`b728a69`) — mail Direct ne livre pas à Gmail |
| **BUNDLE-001** | Avant 02/05 | **> 3 mois** | ? | Bundle marketing 16 MB, split lazy-load. Perf Lighthouse 25/100. TASKS_MASTER l.101 : dette technique P2 |
| **STUDIO-RIM-AGENTS** | Avant 02/05 | **> 3 mois** | ? | Sidebar agents rim-only, accent par acte. TASKS_MASTER l.84 : ❌ |
| **MARKETING-EX3-001** | 02/05 (BACKLOG.md l.112) | **3 mois** | ? | SDS Télécom — exec 144 est pre-refonte, inutilisable. Nouvelle exec post-refonte requise. TASKS_MASTER l.86 : « dépend de STREAM-001 + BR-FOOTGUN » (les deux ✅) |
| **MARKETING-EX4-001** | 02/05 | **3 mois** | ? | SDS Retail — pas lancé. TASKS_MASTER l.87 : ❌ |
| **GIT-CLEANUP-001** | 08/06 (TASKS_MASTER l.114) | **2 mois** | Sam (script `--apply` prêt, Sam doit lancer) | 58 branches, 4 mergées = suppression sûre, 53 non mergées = arbitrage Sam (risque de perte) |

**Impact** : 9 tâches bloquées **> 2 mois**, dont 3 sur **> 3 mois**. Aucune n'a avancé depuis le dernier backlog (02/05 ou 08/06).

**Cas particulier — BUILD : bloqué sans porteur depuis février 2026** :
- **4 phases BUILD enregistrées en base, toutes FAILED** (v_deos_build_phases)
- Exec 165 (14/07) : phase 1 arrêtée volontairement (coûts), phase 2 crashée immédiatement (`'NoneType' object has no attribute 'lower'`)
- Bug phase 2 **corrigé le 05/08** (SESSION_2026-08-05.md tâche 1 : `task_type` NULL → fix persistance), **MAIS worker pas redémarré** → correctif inactif
- **Aucune exécution BUILD complète jamais réussie** depuis février 2026 (exec 131)
- **Ancienneté** : **6 mois**, aucun porteur identifié dans les backlogs

---

## 2. LES 8 CHANTIERS DU LANCEMENT — vérification croisée

Source : clé `statut_o2` (base `dh_comite`, créée session 05/08), croissement TASKS_MASTER.md, git.

| Chantier | État | Preuve git | Date | Dans main | Réserve |
|---|---|---|---|---|---|
| **FIX-PARSE-001** | ✅ fait | `666e02d`, fusionné `5fa1420` | 10/06 | ✅ | — |
| **FIX-MAXTOKENS-002** | ✅ fait | `397ed4a`, fusionné `5fa1420` | 10/06 | ✅ | Autres max_tokens=16000 laissés tels quels (hors périmètre minimal) |
| **PATCH-MERGE-001** | ✅ fait | `ad158de`, fusionné `73dd681` | 10/06 | ✅ | — |
| **FIX-EMPTY-001** | ✅ fait | `31ba2d5`, fusionné `5fa1420` | 10/06 | ✅ | — |
| **FEAT-LANG-001** | ✅ fait | fusionné `73dd681` | 10/06 | ✅ | — |
| **OBSERV-001** | ✅ fait | `280d3c8`, fusionné `73dd681` | 10/06 | ✅ | **Contredit par situation 05/08** : worker silencieux non détecté |
| **RAG-V2** | ✅ fait | `02bf92d` | 15/07 | ✅ | Bascule validée 14/07, non revérifié durant session 05/08 |
| **STRIPE-PROD** | ❌ a_faire | aucun commit | — | — | Secret encore en `sk_test` (vérifié 05/08). Dépend de BIZ-001 (tranché ✅ 08/06) |

**Synthèse** : **7 fait / 1 à faire**. STRIPE-PROD est le seul des 8 à ne pas être engagé.

**Limite de la preuve** (inscrite dans statut_o2) : « Un état 'fait' signifie ici : correctif commité, fusionné dans main, et déclaré prouvé par le registre du dépôt au moment où il a été posé. Il ne signifie PAS revérifié de bout en bout en production durant cette session. »

**Point d'attention** : OBSERV-001 est le chantier **le plus directement contredit par la situation observée**. Le monitoring N8N aurait dû détecter le silence du worker le 05/08 — ce ne fut pas le cas.

---

## 3. CE QUI COMPTE POUR LE 15/08 — checkpoint BUILD→SANDBOX

**Échéance** : 15 août 2026 (dans **9 jours**). **Objectif** : preuve BUILD→SANDBOX (première exécution BUILD complète aboutie + déploiement sandbox fonctionnel).

### 3.1 État réel BUILD (06/08/2026)

**Base de production** (v_deos_build_phases) :

```
 id  | execution_id | phase_number | phase_name     | status | total_batches | completed_batches | last_error
-----+--------------+--------------+----------------+--------+---------------+-------------------+--------------------------------------------
 101 |          165 |            2 | business_logic | failed |             0 |                 0 | 'NoneType' object has no attribute 'lower'
  30 |          165 |            1 | data_model     | failed |            12 |                 2 | Arret volontaire (maitrise des couts) […]
  24 |          147 |            1 | data_model     | failed |             0 |                 0 | Deploy failed: SF Admin service not init
   1 |          131 |            1 | data_model     | failed |             0 |                 0 | No batches generated
```

**Constat** :
- **4 tentatives BUILD**, toutes FAILED
- **Aucune exécution BUILD complète jamais réussie** (ancienneté : 6 mois, depuis février 2026)
- Dernière tentative (exec 165, 14-15/07) :
  - Phase 1 (data_model, Raj) : 12 lots, 2 complétés, arrêt volontaire coûts le 02/08
  - Phase 2 (business_logic, Diego) : crash immédiat `'NoneType' object has no attribute 'lower'`

**Bug phase 2** : corrigé le 05/08 (SESSION_2026-08-05.md tâche 1). Cause racine : `task_type` présent dans le WBS de Marcus (40 tâches) mais **jamais recopié** dans `TaskExecution` → colonne NULL (413/476 lignes en base) → crash ligne 452 `phased_build_executor.py` : `if "test" in task_type.lower()`. Correctif : persistance du champ + idiome défensif `or ""` en second rideau.

**MAIS** : le correctif est **inactif** — le worker tourne encore avec l'ancien code (pas de redémarrage depuis le 05/08, règle 7 de la session : ne pas redémarrer pendant la mission).

### 3.2 Bloquants pour le checkpoint du 15/08

| Bloquant | Type | Impact | Résolution |
|---|---|---|---|
| **Worker pas redémarré** | Déploiement | Correctif phase 2 inactif, toute tentative BUILD recrashe | Redémarrer `digital-humans-worker.service` (+ backend pour cohérence) |
| **Aucune validation E2E des 6 fixes du 10 juin** | Validation | FIX-PARSE-001, FIX-MAXTOKENS-002, PATCH-MERGE-001, FIX-EMPTY-001, FEAT-LANG-001, OBSERV-001 jamais testés en condition réelle BUILD | Lancer exec BUILD complète (coût : exec 165 phase 1 partielle = $X, phase 2 = $0 car crash immédiat) |
| **Phase 1 incomplète (exec 165)** | Coût | 2/12 lots complétés, arrêt volontaire | Reprendre phase 1 OU lancer nouvelle exec (décision Sam : budget disponible ?) |
| **Monitoring défaillant** | Observabilité | OBSERV-001 ✅ fait mais contredit par les faits (worker silencieux 05/08 non détecté) | Vérifier N8N workflow `digital-humans-worker` actif + test déclenchement |
| **STRIPE-PROD non fait** | Bloquant métier ? | Seul des 8 chantiers à ne pas être engagé | Arbitrage Sam : bloquant checkpoint 15/08 ou différé ? |

**Chemin critique pour le 15/08** (dans l'ordre) :

1. **Redémarrer worker + backend** (5 min, à faire hors exec en cours)
2. **Vérifier monitoring N8N** (10 min : `systemctl status n8n`, workflow actif, test heartbeat)
3. **Décision budget** : reprendre exec 165 OU lancer nouvelle exec (Sam)
4. **Lancer BUILD complet** :
   - Si reprise 165 : phase 1 lots 3 à 12 (10 lots) + phase 2 + phase 3 + phase 4
   - Si nouvelle exec : phases 1-4 complètes
5. **Déploiement sandbox** (prévu dans phase 4, jamais atteint)
6. **Validation fonctionnelle** (smoke test sandbox)

**Estimation effort** (hors décision Sam) :
- Redémarrage + vérif monitoring : **30 min**
- Exec BUILD complète (si budget ok) : **durée inconnue** (aucune jamais terminée), coût estimé : **à chiffrer depuis exec 165 phase 1 partielle**
- Déploiement sandbox : **inclus phase 4** (jamais testé)
- Validation : **1-2 h**

**Total hors exécution** : ~2-3 h. **Total avec exécution** : impossible à estimer sans référence.

### 3.3 Ce qui peut attendre après le 15/08

**Non bloquant checkpoint** (différable sans impact BUILD→SANDBOX) :

- STRIPE-PROD (si Sam confirme)
- LEGAL-001 (validation juriste CGV)
- SECURITY-001..005 (secrets manager)
- GHOST-001 (SMTP Ghost)
- BUNDLE-001 (perf marketing)
- STUDIO-RIM-AGENTS (UI plateforme)
- MARKETING-EX3-001, MARKETING-EX4-001 (galerie SDS)
- GIT-CLEANUP-001 (branches stale)
- UI-002/003/004 (cosmétique)
- Mods 37-39 non commités (**SAUF si** ils touchent le BUILD — à vérifier)
- main non poussé (**SAUF** risque de perte si serveur crashe)

**Risque de perte à traiter AVANT le 15/08** (priorité absolue TASKS_MASTER) :

- **Mods 37-39 non commités** (budget_service.py, llm_router_service.py, llm_service.py, llm_routing.yaml datés 31/05) → **commiter MAINTENANT**
- **main non poussé** (4 commits locaux, origin/main 5 semaines de retard) → **pusher MAINTENANT**

---

## 4. PROPOSITION D'ORDRE DE TRAITEMENT

**Principe** : priorité au checkpoint du 15/08, puis dette bloquée > 3 mois.

### Lot 0 — URGENCE (avant toute autre action, risque de perte)

| ID | Action | Effort | Qui | Pourquoi |
|---|---|---|---|---|
| **Commit mods 37-39** | `git add` + `git commit` des 4 fichiers datés 31/05 | **5 min** | Delivery OU Sam | Travail non sauvegardé, risque de perte si reboot/crash serveur |
| **Push main** | `git push origin main` (4 commits locaux) | **2 min** | Delivery OU Sam | `origin/main` 5 semaines de retard, risque de perte |

**Total Lot 0** : **7 min**. **Bloquant** : aucun. **À faire** : **IMMÉDIATEMENT**.

### Lot 1 — CHECKPOINT 15/08 (chemin critique)

| ID | Action | Effort | Qui | Débloque |
|---|---|---|---|---|
| **1.1 Redémarrage** | `systemctl restart digital-humans-worker digital-humans-backend` | **5 min** | Sam OU Delivery (curseur ?) | Active correctif phase 2 (bug task_type) |
| **1.2 Vérif monitoring** | N8N workflow `digital-humans-worker` actif + test heartbeat | **10 min** | Delivery | Détection panne worker (OBSERV-001 validation) |
| **1.3 Décision budget** | Reprendre exec 165 OU nouvelle exec (chiffrage coût) | **Arbitrage** | Sam | Autorise lancement BUILD |
| **1.4 Lancement BUILD** | Reprendre exec 165 phase 1 lot 3-12 + phases 2-4 OU nouvelle exec | **durée inconnue** | Sam (lance via UI) | Preuve BUILD→SANDBOX |
| **1.5 Validation** | Smoke test sandbox (déploiement fonctionnel, API répond, logs présents) | **1-2 h** | Delivery | Checkpoint 15/08 ✅ |

**Total Lot 1** : **~3 h hors exécution** (exécution : durée inconnue, jamais terminée). **Bloquant** : décision budget Sam (1.3). **Échéance** : **15/08 (9 jours)**.

### Lot 2 — DETTE > 3 MOIS (post-checkpoint, bloquants métier)

| ID | Action | Effort | Qui | Pourquoi |
|---|---|---|---|---|
| **STRIPE-PROD-001** | Rotation `sk_test` → `sk_live`, recréation produits Pro/Team | **1 h** + checklist | Sam | Bloquant ouverture payante (dépend BIZ-001 tranché ✅ 08/06). Dette sécu : secret partagé en conversation |
| **LEGAL-001** | Validation juriste CGV (300-500 €, 1-2 h) | **externe** | Sam | Bloquant ouverture (boilerplate livré, attend validation) |
| **SECURITY-001..005** | Audit secrets + Doppler/Infisical + migration + docs | **4-6 h** | Sam OU Delivery | Phase 0 non démarrée, ancienneté > 3 mois |

**Total Lot 2** : **5-7 h + externe**. **Bloquant** : budget/décision Sam. **Échéance** : avant ouverture publique (non datée).

### Lot 3 — DETTE TECHNIQUE (post-checkpoint, qualité)

| ID | Action | Effort | Qui | Débloque |
|---|---|---|---|---|
| **GIT-CLEANUP-001** | Lancer script `--apply` (4 branches mergées sûres) + arbitrage 53 non mergées | **30 min** + arbitrage | Sam | Hygiène repo |
| **BUNDLE-001** | Split lazy-load bundle marketing (16 MB → perf Lighthouse 25 → 75+) | **2-3 sessions** | ? | UX site marketing |
| **GHOST-001** | SMTP Postmark + réactiver staffDeviceVerification | **1-2 h** | ? | Reset password Owner |
| **STUDIO-RIM-AGENTS** | Sidebar agents rim-only, accent par acte | **1 session** | ? | UX plateforme (cohérence STUDIO-S4.1 ✅) |

**Total Lot 3** : **1-2 jours**. **Bloquant** : aucun. **Échéance** : aucune.

### Lot 4 — GALERIE SDS (post-checkpoint, marketing)

| ID | Action | Effort | Qui | Débloque |
|---|---|---|---|---|
| **MARKETING-EX2-001** | Intégrer SDS Pharma (exec 148) sur site | **1-2 h** | ? | Galerie 2/4 exemples |
| **MARKETING-EX3-001** | Générer SDS Télécom post-refonte (exec 144 inutilisable) | **4-6 h** | ? | Galerie 3/4 exemples |
| **MARKETING-EX4-001** | Générer SDS Retail | **4-6 h** | ? | Galerie 4/4 exemples (recommandation O4 pour lancement) |

**Total Lot 4** : **1-2 jours**. **Bloquant** : aucun (STREAM-001 + BR-FOOTGUN ✅). **Échéance** : avant lancement public.

---

## 5. SYNTHÈSE POUR SAM

**Rapprochement backlog vs réalité** (06/08/2026) :

- **FAIT MAIS NON COCHÉ** : 11 tâches réalisées (dont 7/8 chantiers lancement) que le backlog ignore
- **COCHÉ SANS PREUVE** : 7 tâches marquées « fait » nécessitant validation (dont 2 risques de perte **priorité absolue**)
- **BLOQUÉ SANS PORTEUR** : 9 tâches bloquées > 2 mois (dont 3 > 3 mois), aucune avancée depuis 02/05

**Les 8 chantiers du lancement** : **7 fait / 1 à faire** (seul STRIPE-PROD reste). OBSERV-001 marqué fait mais **contredit par les faits** (worker silencieux 05/08 non détecté).

**Checkpoint 15/08 (BUILD→SANDBOX)** : **non atteignable en l'état** sans :
1. Redémarrage worker (correctif phase 2 inactif)
2. Décision budget (reprendre exec 165 OU nouvelle exec)
3. Exécution BUILD complète (jamais réussie en 6 mois)

**Urgence immédiate** (risque de perte, **7 min**) :
- Commiter mods 37-39 (4 fichiers non suivis depuis 31/05)
- Pusher main (4 commits locaux, origin/main 5 semaines de retard)

**Chemin critique 15/08** (~3 h hors exécution) :
- Redémarrage worker + backend (5 min)
- Vérif monitoring N8N (10 min)
- **Décision budget Sam** (arbitrage)
- Lancement BUILD complet (durée inconnue, jamais terminée)
- Validation sandbox (1-2 h)

**Arbitrages attendus** :
1. **Budget BUILD** : reprendre exec 165 (10 lots restants phase 1 + phases 2-4) OU nouvelle exec ? Coût à chiffrer.
2. **STRIPE-PROD** : bloquant checkpoint 15/08 ou différé ?
3. **Porteurs** : 9 tâches bloquées > 2 mois sans porteur (GHOST-001, BUNDLE-001, STUDIO-RIM-AGENTS, MARKETING-EX3/4, GIT-CLEANUP, SECURITY).

**Limite de ce rapprochement** : les états « fait » reposent sur l'historique git et le registre du dépôt (TASKS_MASTER.md, statut_o2), **pas sur un test rejoué en production**. Les 7 chantiers marqués « fait » (dont les 6 fixes du 10 juin) n'ont **jamais été validés en condition réelle BUILD**.

---

**Directeur Delivery** · 06/08/2026 · Sources : `/backlog/TASKS_MASTER.md` (14/07), `/backlog/BACKLOG.md` (06/06), `/backlog/SESSION_2026-08-05.md`, base `digital_humans_db` (v_deos_*), base `dh_comite` (deos_state), `/prodlogs/backend-24h.log`.
