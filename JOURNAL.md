# Journal — dh-comite

> Genere automatiquement depuis les messages de commit.
> Derniere mise a jour : 06/08/2026 14:30 UTC

## 2026-08-06
- Strategie d'approche : trois moteurs (Team personnalise milieu de gamme, Pro entrant par contenu, Partenaires differe) `b71d5fe`
- Inventaire teste des sources de signaux publics : APEC operationnel (16 signaux), BOAMP trop rare, France Travail et HelloWork a construire. LinkedIn ecarte avec justification. Constat strategique : 9 signaux sur 16 sont des ESN, canal partenariat. `e424382`
- Cartographie des capacites du 06/08 transmise aux six directions + correction de l'inventaire (N8N tourne en systemd, pas en Docker) `76861a2`
- Journal automatique du depot (hook post-commit) — genere depuis les messages de commit, sans modele de langage `c0e637e`
- Journal automatique du depot active (hook post-commit) `ab68f3a`
- securite : mot de passe Postgres sorti du docker-compose vers .env (ignore) avant la mise sur GitHub `83e6117`
- Note de Sam au comite du 06/08 : 14 arbitrages, 4 demandes de statut, 3 corrections de fonctionnement `4c2e61e`
- FIX-BGWAIT-001 : plafond d'attente des rondes porte a 20 min + consigne de restitution complete au CoS (sa ronde du 06/08 perdue : main rendue en 14s, travail tue a 600s en arriere-plan) `4533eec`
- Sourcing de prospects : methode et pistes transmises au Commercial (jamais livrees jusqu'ici — faute de transmission cote Claude). DEC-2026-0716-01 requalifiee en accordee `6ce2b5e`
- CoS : escalade d'une inexecution vers le CEO et le directeur porteur, plus vers Sam (constat de Sam du 06/08 : il etait la mauvaise cible) `1198a5d`
- CEO : deux compteurs distincts (arbitrage attendu vs execution attendue) — le brief du 06/08 annoncait 25 decisions en attente alors que 2 seulement attendaient Sam `fdfce29`
- Regle 'avant de demander, produis' posee dans les six fiches de direction (reproche de Sam du 06/08 : trop de demandes, trop peu de production) `4117c33`

## 2026-08-05
- FIX-ARGLIST-001 : le prompt du brief et du comite transite par l'entree standard (depassait la limite d'arguments des que les 5 directions rapportent — brief perdu le 05/08) + FIX-ALERTE-BRIEF : un brief absent ou perime declenche desormais une alerte Telegram `7bc1ab9`

## 2026-08-04
- Mission collective interface web globale : besoin exprime par chaque direction en ronde du 05/08, consolidation DSI dans la journee, arbitrage au comite du 10/08 sur document instruit `16c98e2`
- FIX-GUARD-001 : limites de mot dans les regex du garde-fou (updated_at / deleted declenchaient le blocage a tort — 5 rondes perdues le 04/08). Batterie verifiee : 3 legitimes passent, 6 dangereuses bloquees `75bc927`
- Archives des dossiers dans l'interface (menu + telechargement) ; le CEO instruit chaque decision (argument, contre-argument, options, recommandation) et le generateur la rend en section dediee `e2d1dc0`
- Dossier illustre comme format de reference : generateur bin/dossier.py (4 graphiques + tableaux depuis deos_state), cable dans daily.sh et comite.sh, telechargeable via /comite/dossier/, Telegram reduit a une notification courte avec lien `fa88c1c`

## 2026-08-02
- Regle budget : la rallonge n'est jamais la premiere option — cinq questions d'optimisation avant toute demande d'augmentation (Sam, 02/08) `0d3b4ff`
- Mission transverse Entracte v2 (marketing pilote, delivery realise, juridique relit) — premier projet inter-directions, banc d'essai de la coordination `2892e64`
- URGENT AI Act art. 50 applicable depuis le 02/08/2026 : mission prioritaire du Directeur Juridique (concierge Sophie en ligne = exposition immediate) `57d24ea`
- Directeur Juridique : mission d'audit de conformite du parcours complet (10 etapes, chaine responsable/sous-traitant, RGPD) `0339604`
- Directeur Juridique : perimetre international (UE hors France, UK, US) — mission de cadrage tracee au registre `1f273eb`
- Comite hebdo 03/08 : le CEO lit le compte rendu BUILD avant son analyse croisee `1001476`
- Compte rendu session BUILD 02/08 pour le Directeur Delivery + mise a jour de sa memoire (avant comite hebdo du 03/08) `483e044`
- Directeur Juridique (6e directeur, régime à la demande) : validation forme+complétude des pages légales sur sources officielles, extension contrats/DPA en septembre ; curseurs et CEO mis à jour `62b9c11`
- Inventaire des capacités existantes (18 workflows N8N, licences Salesforce, tables alimentées, routage LLM par tâche) + injection obligatoire dans le contexte des 5 directeurs et du CEO `d90ac90`
- Plans de département des 5 directeurs + proposition consolidée CEO (2026-08-02) : reprise après 16j de silence, trou noir O2 identifié, 19 décisions préparées pour arbitrage Sam `41399d1`
- Robustesse comité : alerte Telegram si une ronde échoue (post-rondes) + le CEO traite un rapport absent >48h comme alerte haute et escalade si 2 domaines muets (leçon du silence 16/07-01/08, crédits API épuisés) `16431d9`

## 2026-07-14
- Fix liens Delivery/CS : /admin/ avec slash (sans slash, nginx retombait sur l'app client) — corrigé à chaud, zéro redémarrage `a0bbb23`
- Interface V1.1 : panneau Delivery = bloc Exploitation temps réel (utilisateurs actifs 30j, exécutions 7j/30j, en cours, charge/RAM/disque serveur) + lien unique vers le dashboard admin interne (retrait de la vue client /projects) `bb1c3d1`
- Interface web V1 (DEC-01) : tableau de bord drill-down 3 niveaux (poinçon santé + 5 loges domaines -> rapport détaillé -> liens outils SF/plateforme), FastAPI RO + page charte DH, nginx /comite/ auth basique `c7067b0`
- Org CRM : username admin corrigé (shatit.1f62a5011548@agentforce.com) `7e6773b`
- POCs Odoo + Camunda arrêtés (volumes conservés jusqu'au 28/07) ; org Salesforce Dev Edition CRM référencée `da7a1fa`
- Telegram : envoi brief (daily) + CR (comité) via sendMessage direct ; watchdog host 15min remplace le Monitoring N8N en échec (6 workflows désactivés, backup pris) `e6d869b`
- Comité hebdo : prompt d'analyse croisée C1-C4 (4 temps), comite.sh (contexte hebdo + Fable 5), daily.sh saute le lundi, cron lundi 08h00 — premier comité : lundi 20/07 `60ebf9f`
- Session de validation Sam 14/07 : OKR nominal, objectifs commerciaux 2 régimes, séquence éditoriale + 2 contenus validés (retouche pricing), schéma comptes CS + canal Postmark, fiches 11 agents (Lucas=Formateur), cash_suivi initialisé, cadence actée + cron rituels posé `9f87d1f`
- Répartition CEO validée par Sam : Opus 4.8 en semaine, Fable 5 le lundi (comité hebdo) `6908a5d`
- Étape 7d — rondes CRO/CSM/CMO réussies (5/5 rapports) + A/B CEO Fable 2,26$ vs Opus 0,87$ sur contexte identique ; composeur : les décisions refusées/closes <48h restent visibles au contexte `a53cf0b`
- Étape 7c — CRO, CSM, CMO : définitions subagents (fiches Gate 3), skills (qualification, santé comptes, calendrier éditorial), offre_dh.md canonique, dh-fr-copywriting copié intégral (8744o) `61adb8a`
- Étape 7b — première ronde CoS : écart brief↔table détecté et corrigé (DEC-02/03/04 créées), PageSuivi.md générée, cash déclaré inactif, score exécution calculé — coût 0,64$ `d5f75fe`
- Étape 7a — Chief of Staff : définition subagent (fiche Gate 3), skill dh-suivi-execution (audit décisions, rapprochement brief↔table, file skills, PageSuivi) `f3603cb`
- Étape 6b — premier daily complet : brief conforme Gate 1 (score plafonné ambre, 4 domaines dégradés déclarés, calcul visible, 100% sourcé), coût mesuré 1,43$ (Fable 5) `59bd35d`
- Étape 6a — CEO digital : prompt (fiche Gate 1), agent_autonomy_map.yaml (curseurs + pondérations santé), composeur daily.sh (blocs B1-B6, fraîcheur, mode dégradé) `2215bb9`
- Étape 5c — ronde 3 (J+1) validée : mémoire inter-sessions OK, détection des exécutions 161/162 et du restart backend ; correction mémoire : export logs fidèle au journal (silence réel, pas troncature) `2b2c997`

## 2026-07-13
- Mémoire delivery : les 9 WAITING_BR_VALIDATION sont des tests internes (confirmé par Sam) — pas de relance client à proposer `8ae230d`
- Étape 5b — ronde 1 réelle OK (score 100 vert, 14 faits sourcés, 0 refus hook, rapport stocké) ; clarification skill : execution_id vs id de ligne dans v_deos_build_phases `dddde7f`
- Étape 5a — Directeur Delivery : définition subagent (fiche Gate 2), skill dh-supervision-delivery (ronde P1 outillée), CLAUDE.md `eb845fc`
- Étape 5 — Directeur Delivery en Observe : agent + skill dh-supervision-delivery + CLAUDE.md ; ronde 1 réelle OK (score 100 auditable, 9 WAITING_BR dont 5 >7j remontés en opportunité, baselines initialisées en mémoire) — coût 0,73$ / 4min26 `93f68ab`
- Étape 4 — garde-fous exécutables : deos-state/deos-decisions (scopes par agent, clôture sur preuve), hook PreToolUse (DH-DEL/CRO/CMO/CSM/COS + R14), settings.json — batterie 8 interdits bloqués / 3 autorisés passants `cd78b95`
- Étape 2+3 — accès prod lecture seule : vues v_deos_* (sans contenu client), rôle deos_ro (SELECT only, pg_hba réseau comité), export logs journald -> /prodlogs:ro (cron 15min) `1c40eea`
- Étape 1 — socle comité : compose (comite+comite-db), schéma dh_comite (deos_state, decisions append-only, contrainte clos_avec_preuve), Dockerfile Claude Code `ac2623f`

