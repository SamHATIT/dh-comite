# AUDIT DE FONCTIONNALITÉ DES CAPACITÉS EXISTANTES — 2026-08-02
Rôle : DSI (mission spéciale, hors ronde standard des 5 directeurs). Auteur : agent DSI (Claude).
Périmètre audité : /workspace/config/outils_disponibles.md (établi 2026-08-02 par le Directeur Delivery, commit `d90ac90`).
Besoins référencés : /workspace/rondes/plans-consolides.md (cos, commercial, cs, marketing) + /workspace/rondes/directeur-delivery-2026-08-02-plan.json (plan Delivery, finalisé 14:04, **postérieur** à `plans-consolides.md` figé à 13:31 — absent de ce fichier, lu séparément) + /workspace/briefs/proposition-consolidee-2026-08-02.md (CEO).

## Note de méthode — ce que j'ai pu vérifier moi-même vs. ce qui reste hypothèse

Mon accès réel dans cette session : `$DEOS_RO_DSN` (rôle `deos_ro`), `$COMITE_DB_DSN`, `/prodlogs/backend-24h.log`, le dépôt git `/workspace`, `/workspace/bin`. **Aucun accès** : N8N (pas d'URL/API key en environnement), Salesforce (aucun credential dans le repo, par conception — `config/salesforce_crm_org.md`), Ghost CMS, Docker/systemctl (interdits par les règles du comité), filesystem du VPS hors `/workspace` et `/prodlogs`, serveur MCP Playwright (non chargé dans mes outils de session — recherché via ToolSearch, absent).

Conséquence directe : **pour les 18 workflows N8N et les 8 capacités Salesforce, je ne peux rien vérifier de première main.** Je reprends la source datée du Directeur Delivery (02/08) sans la recréer ni la contredire, et je le marque explicitement à chaque fiche. Ce que j'ai vérifié moi-même ce jour, en direct :

- **Permissions tables prod** : `SELECT count(*)` sur `leads`, `blog_topics`, `blog_articles`, `prospects`, `veille_reports`, `projects`, `executions`, `agent_deliverables`, `build_phase_executions` → **`ERROR: permission denied`** pour les 9, malgré leur visibilité dans `\dt` (schéma visible ≠ droit `SELECT`). Confirme exactement le constat du Commercial (4e tentative, permission denied) et du CS.
- **Vues `v_deos_*`** : 4 vues actives et fonctionnelles — `v_deos_projects` (78 lignes), `v_deos_executions` (128 lignes, id 30→165), `v_deos_build_phases` (3 lignes, toutes `failed`/`raj`/`data_model`, 0 `elena_verdict`), `v_deos_sections`.
- **Écart chiffré non expliqué** : l'inventaire (§2) et le rapport Commercial du jour citent **165 exécutions** ; ma requête directe sur `v_deos_executions` (la seule source lisible) renvoie **128 lignes** (id min 30, id max 165 — donc au moins 37 id absents de la vue dans cette plage). Je ne sais pas trancher si la vue filtre (jointure `INNER JOIN projects`, possible exclusion d'exécutions orphelines) ou si le chiffre de l'inventaire vient d'ailleurs. **Point à clarifier avec Delivery**, pas une invention de ma part.
- **`decisions`** (13 lignes) et **`deos_state`** (13 clés) : lus intégralement, statuts confirmés (6 décisions toujours `attente_sam` : 0716-01/02/03/04/05/07 ; 2 `en_execution` : 0714-01, 0716-06 ; `DEC-2026-0714-02` — fiabilisation des logs — **`refusee`**, pertinent pour la capacité logs ci-dessous).
- **`/prodlogs/backend-24h.log`** : non vide (48 Ko, 109 lignes, écrit à 15:00) — mais son contenu couvre seulement **13:55:48 → 13:57:08 (≈80 secondes)**, pas une fenêtre 24h. Le rapport Delivery de 14:04 le décrivait à 0 octet ; il s'est donc rempli depuis, mais la couverture réelle reste quasi nulle. Ni un « 0% » figé ni un « restauré » — un fichier qui grossit par à-coups sans couverture de fond, cohérent avec `DEC-2026-0714-02` refusée (pas de fiabilisation de fenêtre glissante décidée).
- **`/workspace/bin`** : `deos-decisions`, `deos-state`, `rondes.sh`, `comite.sh`, `daily.sh`, `ab-daily.sh` présents et exécutables. Lu `rondes.sh` intégralement : la logique d'alerte Telegram post-rondes (lecture `TELEGRAM_BOT_TOKEN`/`CHAT_ID` dans `.env`, `curl` vers l'API Telegram si une ronde échoue) est réelle et correspond au commit `16431d9`. Je n'ai pas pu vérifier la réception effective du message (pas d'accès Telegram) — c'est exactement le test que le CoS a demandé en S0.
- **`/workspace/web/app.py`** : lu intégralement (94 lignes). Code FastAPI réel, lecture seule, interroge `COMITE_DB_DSN` et `DEOS_RO_DSN` via les vues `v_deos_*` — cohérent avec les commits `a0bbb23`/`bb1c3d1` (fix liens `/admin/`, panneau exploitation).
- **`.claude/skills/`** : `dh-fr-copywriting` présent (fichier réel). **`.claude/skills-proposed/`** : vide (0 fichier) — confirme le constat du CoS (0 skill en file).
- **`regen_covers.py`** : recherché sur tout `/workspace` (`find -iname`) → **0 résultat**. Ne prouve pas son inexistence (le VPS héberge probablement des scripts hors du repo comité, comme N8N/Ghost), mais je ne peux pas confirmer sa présence non plus. Marqué hypothèse non vérifiable.

---

## JSON — `audit_capacites`

```json
{
  "audit_capacites": {
    "date": "2026-08-02",
    "auteur": "dsi",
    "sources": [
      "/workspace/config/outils_disponibles.md (02/08, Directeur Delivery)",
      "/workspace/rondes/plans-consolides.md (cos, commercial, cs, marketing, 13:31)",
      "/workspace/rondes/directeur-delivery-2026-08-02-plan.json (14:04, absent de plans-consolides.md)",
      "/workspace/briefs/proposition-consolidee-2026-08-02.md (ceo)",
      "vérifications directes psql $DEOS_RO_DSN / $COMITE_DB_DSN / /prodlogs / /workspace 2026-08-02"
    ],
    "capacites": [
      {
        "id": "N8N-01", "nom": "Blog - Newsletter Hebdo (lundi 9h)",
        "etat_reel": "HYPOTHÈSE (source Delivery 02/08, non vérifiable — pas d'accès N8N) : actif, 2 exécutions réussies. Table de sortie probable (newsletter_sends) : accès direct refusé par moi ce jour (permission denied).",
        "sert": "Marketing — calendrier éditorial",
        "taches": [
          {"description": "Créer une vue v_deos_newsletter (compteurs d'envoi, dates) pour donner au comité marketing une lecture réelle sans passer par N8N", "effort": "S", "risque": "faible", "dependance": "aucune technique, juste l'arbitrage d'exposer la table", "qui": "Delivery (SQL) + Sam (accord)"},
          {"description": "Confirmer avec Sam que le déclencheur lundi 9h est toujours actif (dernière preuve datée)", "effort": "S", "risque": "faible", "dependance": "accès N8N (hors comité)", "qui": "Sam"}
        ],
        "verdict": "REBRANCHER"
      },
      {
        "id": "N8N-02", "nom": "Blog - Veille Hebdo (jeudi 20h)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : actif, 2 exécutions réussies. Distinct de 'Veille Concurrence' (désactivé, N8N-09) — à ne pas confondre.",
        "sert": "Marketing, Commercial",
        "taches": [
          {"description": "Clarifier avec Delivery quelle table ce workflow alimente réellement (blog_topics ? une table dédiée ?) avant de créer une vue", "effort": "S", "risque": "faible — confusion possible avec N8N-09", "dependance": "réponse Delivery", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER"
      },
      {
        "id": "N8N-03", "nom": "Blog - Topics API",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : webhook actif, écrit dans blog_topics (33 sujets selon l'inventaire : 21 attente, 5 approuvés, 7 générés). Accès direct à blog_topics refusé ce jour (permission denied), confirmé par moi.",
        "sert": "Marketing",
        "taches": [
          {"description": "Vue v_deos_blog_topics (comptage par statut, titres) pour lecture comité", "effort": "S", "risque": "faible", "dependance": "aucune", "qui": "Delivery"},
          {"description": "Si le comité doit un jour agir sur ce webhook (approuver/rejeter), cadrer d'abord le périmètre de validation humaine (agent_autonomy_map : programmation_contenu_valide = agit_sous_validation)", "effort": "M", "risque": "moyen — action engageante sur du contenu publié", "dependance": "arbitrage Sam sur le périmètre", "qui": "Sam"}
        ],
        "verdict": "REBRANCHER"
      },
      {
        "id": "N8N-04", "nom": "Blog - Topics Dashboard",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : gestion des sujets d'articles, non vérifiable depuis mon accès.",
        "sert": "Marketing",
        "taches": [
          {"description": "Vérifier si ce dashboard a une URL propre accessible à Sam, sinon ajouter un lien depuis /comite/ (sur le modèle du lien admin déjà ajouté en bb1c3d1)", "effort": "S", "risque": "faible", "dependance": "URL du dashboard (Sam/Delivery)", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER"
      },
      {
        "id": "N8N-05", "nom": "Content Articles - Blog Generator",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : webhook -> génération LLM -> base -> notification. blog_articles vide et verrouillée (permission denied confirmé). Non classé par le doc parmi les 5 workflows pointant Ollama — donc a priori déjà sur une API valide, à confirmer.",
        "sert": "Marketing",
        "taches": [
          {"description": "Confirmer que le nœud LLM ne pointe PAS sur Ollama local (127.0.0.1:11434) avant toute activation", "effort": "S", "risque": "moyen si non confirmé — reproduirait le problème des 5 workflows désactivés le 14/07", "dependance": "accès N8N", "qui": "Sam/Delivery"},
          {"description": "Premier essai supervisé (1 article) avant autonomie, cohérent avec la validation humaine déjà pratiquée par le marketing (discipline 'un contenu à la fois')", "effort": "S", "risque": "faible", "dependance": "confirmation ci-dessus", "qui": "Marketing + Sam"}
        ],
        "verdict": "REBRANCHER, sous réserve de confirmation du repointage LLM"
      },
      {
        "id": "N8N-06", "nom": "Lead Capture - Website",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : webhook -> leads -> email de vérification -> réponse. Table leads confirmée verrouillée par moi ce jour (permission denied), 4e constat identique au Commercial.",
        "sert": "Commercial",
        "taches": [
          {"description": "Créer une vue v_deos_leads en lecture seule (champs minimaux : email masqué/nom/société/source/statut vérifié, PAS de données personnelles brutes au-delà du nécessaire) — c'est précisément l'objet de DEC-2026-0716-02, en attente_sam depuis 19 jours, coût technique nul", "effort": "S", "risque": "RGPD — nécessite le périmètre de champs validé par Sam (toujours_validation: donnees_personnelles_rgpd)", "dependance": "arbitrage Sam sur le périmètre de champs exposés", "qui": "Sam (décision) + Delivery (SQL)"}
        ],
        "verdict": "REBRANCHER — la tuyauterie tourne déjà (7 leads test), il ne manque qu'une vue SQL et un arbitrage RGPD, pas un développement"
      },
      {
        "id": "N8N-07", "nom": "Meeting Booking - Calendly",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : le document lui-même signale 'credential à vérifier' — incertitude assumée à la source.",
        "sert": "Commercial",
        "taches": [
          {"description": "Tester la validité du credential Calendly (RDV test réel)", "effort": "S", "risque": "faible", "dependance": "accès N8N/Calendly", "qui": "Sam"},
          {"description": "Si valide : brancher une notification comité (deos_state ou vue) sur les RDV pris", "effort": "S", "risque": "faible", "dependance": "credential validé", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER — la pièce manquante (le credential) est nommée par la source elle-même"
      },
      {
        "id": "N8N-08", "nom": "Dashboard Acquisition - Metrics / Web UI",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : agrégation de métriques PostgreSQL. Risque de dépendance aux mêmes tables verrouillées (leads, blog_topics) — non confirmé.",
        "sert": "Commercial, Marketing, CEO",
        "taches": [
          {"description": "Vérifier si ses métriques dépendent des tables verrouillées ; si oui, bloqué par le même verrou que N8N-06/N8N-03", "effort": "S (vérification)", "risque": "faible", "dependance": "réponse Delivery", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER, sous réserve de la vérification ci-dessus"
      },
      {
        "id": "N8N-09", "nom": "Veille Concurrence (désactivé 14/07)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : structure complète (RSS -> filtre 24h -> LLM -> veille_reports -> email), désactivée car pointait Ollama local. veille_reports vide et verrouillée, confirmé par moi.",
        "sert": "Commercial (veille marché), Marketing (matière éditoriale), Delivery (veille release)",
        "taches": [
          {"description": "Repointer le nœud LLM vers une API de modèle ouvert (MiniMax/GLM/Qwen) — changement d'URL et de clé, pas une reconstruction", "effort": "S", "risque": "faible techniquement ; implique un coût récurrent (même faible) donc arbitrage budget", "dependance": "clé API + budget", "qui": "Sam (credential/budget) + Delivery (config N8N)"},
          {"description": "Ajouter une validation humaine avant l'envoi d'email automatique (le doc signale que ces workflows 'pouvaient envoyer des emails sans validation')", "effort": "S", "risque": "moyen si omis — envoi non contrôlé", "dependance": "aucune", "qui": "Delivery"},
          {"description": "Vue v_deos_veille pour lecture comité une fois la table alimentée", "effort": "S", "risque": "faible", "dependance": "réactivation ci-dessus", "qui": "Delivery"}
        ],
        "verdict": "MODERNISER"
      },
      {
        "id": "N8N-10", "nom": "LinkedIn Enrichment - Prospects (désactivé 14/07)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : structure complète, pointait Ollama. prospects vide, schéma prêt, verrouillée (permission denied confirmé).",
        "sert": "Commercial",
        "taches": [
          {"description": "Repointage LLM identique à N8N-09", "effort": "S", "risque": "faible", "dependance": "clé API + budget", "qui": "Sam + Delivery"},
          {"description": "Ajouter validation humaine avant écriture/action externe", "effort": "S", "risque": "faible", "dependance": "aucune", "qui": "Delivery"},
          {"description": "Vue v_deos_prospects", "effort": "S", "risque": "faible", "dependance": "réactivation", "qui": "Delivery"}
        ],
        "verdict": "MODERNISER — mais n'a d'utilité qu'une fois DEC-2026-0716-01 tranchée (source de comptes cibles) ; sinon rien à enrichir"
      },
      {
        "id": "N8N-11", "nom": "Lead Scoring (désactivé 14/07)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : déclencheur planifié + webhook -> code de scoring -> PostgreSQL. Le doc ne précise pas si le scoring lui-même est un appel LLM (donc concerné par Ollama) ou du code pur — point à vérifier avant toute action.",
        "sert": "Commercial",
        "taches": [
          {"description": "Clarifier si le nœud de scoring est du code pur (pas de repointage nécessaire) ou un appel LLM (repointage nécessaire)", "effort": "S", "risque": "faible", "dependance": "accès N8N (Sam/Delivery)", "qui": "Sam/Delivery"},
          {"description": "Vérifier la cohérence de la grille codée avec la grille /10 de la skill dh-qualification-commerciale (méthodologie déjà validée par le Commercial ce jour)", "effort": "M", "risque": "moyen — grille incohérente fausserait tout le pipeline dès son démarrage", "dependance": "accès au code du nœud", "qui": "Commercial + Delivery"}
        ],
        "verdict": "MODERNISER"
      },
      {
        "id": "N8N-12", "nom": "Email Outreach (désactivé 14/07)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : déclencheur planifié -> conditions -> composition -> envoi -> suivi base. Pointait Ollama. Envoi externe engageant = catégorie 'toujours_validation' de l'agent_autonomy_map.",
        "sert": "Commercial (séquences de relance)",
        "taches": [
          {"description": "Repointage LLM", "effort": "S", "risque": "faible", "dependance": "clé API", "qui": "Sam + Delivery"},
          {"description": "AJOUT OBLIGATOIRE d'une passerelle de validation humaine avant tout envoi réel (aucun envoi sans validation explicite, cf. agent_autonomy_map: envoi_externe_engageant = toujours_validation)", "effort": "M", "risque": "élevé si omis — envoi non désiré = risque réputationnel en régime A (zéro contact sortant)", "dependance": "arbitrage Sam sur le mécanisme de validation (qui clique, où)", "qui": "Sam (arbitrage) + Delivery (implémentation)"},
          {"description": "Condition d'envoi réel Postmark/SMTP-PROD-001 (item 6 des manques listés) — sans lui, aucun envoi ne peut de toute façon partir", "effort": "indéterminé (dépend de Sam/infra)", "risque": "haute — bloque aussi le canal tickets CS (dépendance croisée)", "dependance": "SMTP-PROD-001", "qui": "Sam"}
        ],
        "verdict": "MODERNISER — mais NE PAS réactiver avant la fin du régime A (zéro contact sortant jusqu'au 31/08, DEC-2026-0714-05) et avant la validation humaine"
      },
      {
        "id": "N8N-13", "nom": "Follow-up Relances (désactivé 14/07)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : même structure qu'Email Outreach, orientée relance.",
        "sert": "Commercial",
        "taches": [
          {"description": "Mêmes tâches que N8N-12 (repointage, validation humaine, condition SMTP-PROD-001)", "effort": "S/M", "risque": "élevé si validation omise", "dependance": "identique à N8N-12", "qui": "Sam + Delivery"}
        ],
        "verdict": "MODERNISER — mêmes réserves que N8N-12 (régime A, validation humaine)"
      },
      {
        "id": "N8N-14", "nom": "Rapport Quotidien 8h (archivé)",
        "etat_reel": "VÉRIFIÉ indirectement : remplacé par bin/daily.sh, présent et exécutable dans /workspace/bin (confirmé ce jour).",
        "sert": "Tous (remplacé par le daily brief)",
        "taches": [],
        "verdict": "ABANDONNER — confirmé, le remplaçant existe et tourne déjà, ne pas reconstruire l'ancien"
      },
      {
        "id": "N8N-15", "nom": "Bilan Hebdomadaire lundi 9h (archivé)",
        "etat_reel": "VÉRIFIÉ indirectement : remplacé par bin/comite.sh (comité hebdo), présent et exécutable (confirmé ce jour).",
        "sert": "Tous",
        "taches": [],
        "verdict": "ABANDONNER — confirmé"
      },
      {
        "id": "N8N-ECART", "nom": "Écart de comptage 15 workflows nommés vs '18 au total'",
        "etat_reel": "CONSTAT : le document liste explicitement 8 (actifs) + 5 (désactivés) + 2 (archivés) = 15 workflows nommés, mais son titre annonce '18 au total'. Non vérifiable de mon côté (pas d'accès N8N pour un décompte indépendant).",
        "sert": "Tous — fiabilité de l'inventaire lui-même",
        "taches": [
          {"description": "Demander à Delivery de lister nommément les 3 workflows manquants (ou de corriger le chiffre '18')", "effort": "S", "risque": "faible en soi, mais un inventaire de référence obligatoire (§0 du document) qui se trompe sur son propre total mine la confiance qu'on peut lui accorder", "dependance": "aucune", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER (clarification documentaire, pas un chantier technique)"
      },
      {
        "id": "TAB-01", "nom": "Table leads",
        "etat_reel": "VÉRIFIÉ ce jour : SELECT refusé (permission denied) pour le rôle deos_ro. 7 lignes de test selon l'inventaire (non vérifiable par moi directement).",
        "sert": "Commercial (DEC-2026-0716-02)",
        "taches": [
          {"description": "Voir N8N-06 — même chantier, une seule vue à créer", "effort": "S", "risque": "RGPD", "dependance": "arbitrage Sam", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "TAB-02", "nom": "Table blog_topics",
        "etat_reel": "VÉRIFIÉ ce jour : SELECT refusé. 33 sujets selon l'inventaire (non vérifiable directement).",
        "sert": "Marketing",
        "taches": [
          {"description": "Voir N8N-03 — vue v_deos_blog_topics", "effort": "S", "risque": "faible", "dependance": "aucune", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "TAB-03", "nom": "Table blog_articles",
        "etat_reel": "VÉRIFIÉ ce jour : SELECT refusé. Vide selon l'inventaire.",
        "sert": "Marketing",
        "taches": [
          {"description": "Vue v_deos_blog_articles, utile seulement une fois N8N-05 confirmé et activé", "effort": "S", "risque": "faible", "dependance": "N8N-05", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "TAB-04", "nom": "Table prospects",
        "etat_reel": "VÉRIFIÉ ce jour : SELECT refusé. Vide, schéma prêt selon l'inventaire.",
        "sert": "Commercial",
        "taches": [
          {"description": "Vue v_deos_prospects, utile seulement une fois N8N-10 réactivé", "effort": "S", "risque": "faible", "dependance": "N8N-10", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "TAB-05", "nom": "Table veille_reports",
        "etat_reel": "VÉRIFIÉ ce jour : SELECT refusé. Vide selon l'inventaire.",
        "sert": "Commercial, Marketing, Delivery",
        "taches": [
          {"description": "Vue v_deos_veille, utile seulement une fois N8N-09 réactivé", "effort": "S", "risque": "faible", "dependance": "N8N-09", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "TAB-06", "nom": "projects / executions / agent_deliverables / build_phase_executions",
        "etat_reel": "VÉRIFIÉ ce jour : les 4 tables brutes sont verrouillées (permission denied), MAIS 4 vues existent déjà et sont fonctionnelles : v_deos_projects (78 lignes), v_deos_executions (128 lignes, id 30-165), v_deos_build_phases (3 lignes, toutes failed/raj), v_deos_sections. Écart non expliqué : l'inventaire cite 165 exécutions, la vue en montre 128 — à clarifier avec Delivery.",
        "sert": "Tous, via les vues v_deos_*",
        "taches": [
          {"description": "Clarifier l'écart 128 vs 165 exécutions (filtre de jointure ? source différente ?)", "effort": "S", "risque": "faible mais touche la fiabilité de toutes les métriques dérivées (score commercial, cas d'usage)", "dependance": "aucune", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER — déjà fait et fonctionnel, seul l'écart de comptage mérite une vérification"
      },
      {
        "id": "SF-01", "nom": "Sales Cloud (Leads, Opportunités, Comptes)",
        "etat_reel": "NON VÉRIFIABLE — aucun credential Salesforce dans ce sandbox (par conception, cf. config/salesforce_crm_org.md : 'Credentials : JAMAIS dans ce repo'). Org Dev Edition confirmée exister par le fichier de config, pas par un accès direct.",
        "sert": "Commercial (remplacerait le pipeline en base de données)",
        "taches": [
          {"description": "Authentification SFDX par Sam dans son Studio (hors comité, comme un projet client)", "effort": "M", "risque": "faible technique, mais action que seul Sam peut faire", "dependance": "aucune", "qui": "Sam"},
          {"description": "Créer l'utilisateur API lecture seule + permission set 'Comite_RO' (mentionné 'prévu au brief' mais non fait à ce jour — aucune trace de vue ou de credential Salesforce dans cet environnement)", "effort": "S une fois SFDX authentifié", "risque": "faible", "dependance": "tâche précédente", "qui": "Sam"},
          {"description": "Exposer une vue v_deos_salesforce_pipeline au comité", "effort": "M", "risque": "faible", "dependance": "2 tâches précédentes", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER — verrou racine : SF-02 à SF-05 et SF-07 en dépendent tous"
      },
      {
        "id": "SF-02", "nom": "Reports & Dashboards natifs Salesforce",
        "etat_reel": "NON VÉRIFIABLE — dépend entièrement de SF-01 et SF-06 (authentification + licence non faites à ce jour).",
        "sert": "Commercial, Marketing, CEO (dataviz commerciale)",
        "taches": [
          {"description": "Aucune action propre avant SF-01/SF-06", "effort": "-", "risque": "-", "dependance": "SF-01, SF-06", "qui": "-"}
        ],
        "verdict": "COMPLÉTER"
      },
      {
        "id": "SF-03", "nom": "Service Cloud + Cases (Email-to-Case natif)",
        "etat_reel": "NON VÉRIFIABLE. POINT DE VIGILANCE : le CS a déjà validé avec Sam le 14/07 une architecture différente pour le canal tickets (Postmark inbound -> webhook N8N -> deos_state.tickets, cf. plan CS). Utiliser Service Cloud Cases serait un SECOND chemin concurrent, pas complémentaire.",
        "sert": "Customer Success (canal de tickets)",
        "taches": [
          {"description": "Arbitrage Sam : lequel des deux canaux privilégier — Postmark->N8N (déjà validé 14/07, dépend de SMTP-PROD-001) ou Service Cloud Cases natif (dépend de SF-01/SF-06) — avant d'investir dans l'un ou l'autre, pour éviter un double effort", "effort": "décision seule, coût nul", "risque": "moyen si non tranché — risque de construire les deux en parallèle", "dependance": "aucune", "qui": "Sam"}
        ],
        "verdict": "COMPLÉTER — arbitrage avant toute construction"
      },
      {
        "id": "SF-04", "nom": "Campaigns (licence Marketing User)",
        "etat_reel": "NON VÉRIFIABLE. Dépend de SF-01 + d'un pipeline commercial rempli (actuellement à 0 entrée).",
        "sert": "Marketing (attribution contenu -> lead)",
        "taches": [
          {"description": "Différer : utilité nulle tant que le pipeline est vide (DEC-2026-0716-01/02 non tranchées)", "effort": "-", "risque": "faible priorité", "dependance": "SF-01, pipeline rempli", "qui": "-"}
        ],
        "verdict": "COMPLÉTER, priorité basse"
      },
      {
        "id": "SF-05", "nom": "Knowledge (base de connaissances Salesforce)",
        "etat_reel": "NON VÉRIFIABLE. POINT DE VIGILANCE : le plan CS du jour prévoit déjà de construire une 'base_connaissances_v1' en fichiers plats (config/ ou deos_state), sans mention de Salesforce Knowledge — même risque de double construction que SF-03.",
        "sert": "Customer Success (base de connaissances support)",
        "taches": [
          {"description": "Arbitrage Sam : Salesforce Knowledge natif vs base de connaissances fichiers déjà planifiée par le CS (échéance 29/08)", "effort": "décision seule", "risque": "moyen si non tranché avant le 29/08 (échéance CS)", "dependance": "SF-01", "qui": "Sam"}
        ],
        "verdict": "COMPLÉTER — arbitrage avant l'échéance CS du 29/08"
      },
      {
        "id": "SF-06", "nom": "Licence Salesforce Integration (Comite_RO)",
        "etat_reel": "NON VÉRIFIABLE. Décrite comme 'disponible, gratuite' par l'inventaire — non activée à ce jour (aucune trace d'utilisateur API dans ce sandbox).",
        "sert": "Le comité lui-même (accès API lecture seule)",
        "taches": [
          {"description": "Activer la licence pour le futur user API RO — prérequis de TOUTES les capacités Salesforce (SF-01 à SF-08)", "effort": "S", "risque": "faible, gratuit", "dependance": "aucune", "qui": "Sam"}
        ],
        "verdict": "COMPLÉTER — c'est le verrou racine de toute la section Salesforce"
      },
      {
        "id": "SF-07", "nom": "450 000 appels API/mois",
        "etat_reel": "NON VÉRIFIABLE. Capacité de volume, pas une tâche en soi.",
        "sert": "Tous usages Salesforce futurs",
        "taches": [],
        "verdict": "REBRANCHER — aucune action au-delà de SF-01/SF-06, s'active automatiquement avec l'org"
      },
      {
        "id": "SF-08", "nom": "Agentforce (201 + 10 000 licences)",
        "etat_reel": "NON VÉRIFIABLE. Le document lui-même le classe 'hors périmètre immédiat' — je respecte cette qualification.",
        "sert": "Sujet stratégique, non urgent",
        "taches": [],
        "verdict": "ABANDONNER pour la période pré-lancement (pas un abandon définitif — à réexaminer après le 01/09, aucune tâche avant)"
      },
      {
        "id": "SCR-01", "nom": "Script regen_covers.py",
        "etat_reel": "NON VÉRIFIÉ — recherché sur tout /workspace (find -iname), 0 résultat. Ne prouve pas l'inexistence (le VPS héberge probablement des scripts hors du repo comité, comme N8N/Ghost), mais je ne peux pas non plus confirmer sa présence.",
        "sert": "Marketing (images de couverture d'articles)",
        "taches": [
          {"description": "Sam confirme l'emplacement réel du script (chemin sur le VPS, hors du repo comité)", "effort": "S", "risque": "faible", "dependance": "aucune", "qui": "Sam"},
          {"description": "Si confirmé, exposer sa sortie (les images) au Directeur Marketing sans lui donner l'exécution — juste la lecture du résultat", "effort": "S", "risque": "faible", "dependance": "tâche précédente", "qui": "Delivery"}
        ],
        "verdict": "COMPLÉTER — localisation à confirmer avant tout jugement de fonctionnalité"
      },
      {
        "id": "AUT-01", "nom": "Ghost CMS (blog, Docker)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : actif, API Admin disponible. Non vérifiable — Docker interdit d'accès par les règles du comité elles-mêmes.",
        "sert": "Marketing",
        "taches": [
          {"description": "Confirmer que les credentials API Admin Ghost sont bien ceux utilisés par N8N-05 (Content Articles - Blog Generator)", "effort": "S", "risque": "faible", "dependance": "accès Sam/Delivery", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER (hypothèse)"
      },
      {
        "id": "AUT-02", "nom": "Concierge Sophie (/api/public/concierge/talk)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : actif sur le site, capte des conversations visiteurs, non exposé au comité. C'est la source amont de la table leads.",
        "sert": "Commercial",
        "taches": [
          {"description": "Doublon exact de TAB-01/N8N-06 (DEC-2026-0716-02) — un seul chantier, pas deux", "effort": "-", "risque": "-", "dependance": "voir TAB-01", "qui": "-"}
        ],
        "verdict": "COMPLÉTER — même chantier que TAB-01, ne pas dupliquer l'effort"
      },
      {
        "id": "AUT-03", "nom": "Skill dh-fr-copywriting",
        "etat_reel": "VÉRIFIÉ ce jour : présent dans /workspace/.claude/skills/dh-fr-copywriting.",
        "sert": "Marketing et tout contenu client",
        "taches": [],
        "verdict": "REBRANCHER — déjà fonctionnel, aucune tâche"
      },
      {
        "id": "AUT-04", "nom": "Watchdog services (15 min)",
        "etat_reel": "HYPOTHÈSE (Delivery 02/08) : actif, alerte Telegram si backend/postgres/nginx/n8n tombe. Non vérifiable — accès process/Docker interdit par les règles du comité.",
        "sert": "Delivery",
        "taches": [
          {"description": "Demander à Sam une preuve récente d'alerte reçue (ou simulation contrôlée) — déjà demandé par le CoS en S0 pour le dispositif Telegram voisin", "effort": "S", "risque": "faible", "dependance": "Sam", "qui": "Sam"}
        ],
        "verdict": "REBRANCHER (hypothèse, preuve d'usage réel à obtenir)"
      },
      {
        "id": "AUT-05", "nom": "Bot Telegram @dh_comite_bot",
        "etat_reel": "VÉRIFIÉ ce jour (code source) : /workspace/bin/rondes.sh contient la logique réelle (lecture TELEGRAM_BOT_TOKEN/CHAT_ID, curl vers l'API Telegram si une ronde échoue), cohérente avec le commit 16431d9. Réception effective du message NON vérifiée (pas d'accès Telegram).",
        "sert": "Tous, via le CEO",
        "taches": [
          {"description": "Test réel du dispositif (déjà demandé par le CoS pour S0) : provoquer un échec contrôlé ou attendre le prochain et confirmer la réception par Sam", "effort": "S", "risque": "faible", "dependance": "Sam confirme la réception", "qui": "Sam + CoS"}
        ],
        "verdict": "REBRANCHER — code vérifié fonctionnel, preuve d'usage réel restant à obtenir"
      },
      {
        "id": "AUT-06", "nom": "Tableau de bord /comite/",
        "etat_reel": "VÉRIFIÉ ce jour (code source) : /workspace/web/app.py (94 lignes), FastAPI, lecture seule via COMITE_DB_DSN et DEOS_RO_DSN/v_deos_*, cohérent avec les commits a0bbb23 et bb1c3d1.",
        "sert": "Sam",
        "taches": [],
        "verdict": "REBRANCHER — actif et vérifié directement, aucune tâche"
      },
      {
        "id": "AUT-07", "nom": "Vues v_deos_* (lecture seule)",
        "etat_reel": "VÉRIFIÉ ce jour : 4 vues actives (v_deos_projects, v_deos_executions, v_deos_build_phases, v_deos_sections). Périmètre limité à ces 4 tables sur les ~9 tables listées comme 'à brancher' dans cet audit (TAB-01 à TAB-05).",
        "sert": "Delivery, CS, Commercial",
        "taches": [
          {"description": "Étendre le même mécanisme de vue aux 5 tables verrouillées (leads, blog_topics, blog_articles, prospects, veille_reports) — c'est LE chantier technique commun à presque tous les verdicts COMPLÉTER de cet audit, et il est mécaniquement identique à ce qui existe déjà 4 fois", "effort": "S par vue (S total si fait en un seul lot par Delivery)", "risque": "faible technique, RGPD sur leads uniquement", "dependance": "arbitrage Sam sur leads (RGPD)", "qui": "Delivery"}
        ],
        "verdict": "REBRANCHER (le mécanisme existe et fonctionne, il ne reste qu'à le répliquer)"
      },
      {
        "id": "AUT-08", "nom": "Playwright MCP",
        "etat_reel": "NON VÉRIFIABLE comme actif pour moi : recherché dans mes outils de session (ToolSearch), absent. Le document affirme un 'serveur MCP disponible sur le VPS' — possible, mais non connecté à cette session d'agent.",
        "sert": "Scraping et automatisation navigateur (évoqué pour le sourcing commercial, DEC-2026-0716-01)",
        "taches": [
          {"description": "Si Sam envisage ce canal pour le sourcing (LinkedIn, annuaires), confirmer d'abord son branchement réel à une session d'agent avant de le compter comme une capacité disponible", "effort": "S (vérification)", "risque": "faible", "dependance": "Sam/Delivery", "qui": "Sam"}
        ],
        "verdict": "COMPLÉTER — statut de branchement à confirmer avant de le considérer comme acquis"
      }
    ],
    "sequence_recommandee": [
      {"rang": 1, "action": "SF-06 (licence Comite_RO) + AUT-07 étendue aux 5 tables verrouillées (TAB-01 à TAB-05)", "justification": "Coût nul à quasi nul, mécanisme déjà prouvé 4 fois (vues v_deos_* existantes), débloque en une seule passe la visibilité comité sur Commercial (leads, prospects), Marketing (blog_topics, blog_articles) et Commercial/Marketing/Delivery (veille_reports). C'est l'effort le plus faible pour le déblocage le plus large — exactement la logique demandée."},
      {"rang": 2, "action": "N8N-06 (Lead Capture, vue leads) puis N8N-09/N8N-10 (repointage LLM Veille Concurrence + LinkedIn Enrichment)", "justification": "Complète en cascade le pipeline de sourcing commercial déjà identifié par le CEO comme 'à rebrancher, pas à reconstruire' — mais seulement utile une fois DEC-2026-0716-01 tranchée (sinon rien à enrichir ni à scorer)."},
      {"rang": 3, "action": "SF-03 et SF-05 (arbitrages Salesforce Service Cloud / Knowledge vs plan CS déjà validé)", "justification": "Coût nul (ce sont des arbitrages, pas des constructions) mais urgent avant que le CS n'investisse dans son propre chantier (kit onboarding, base de connaissances, échéances 15/08 et 29/08) sans savoir si Salesforce doit s'y substituer."},
      {"rang": 4, "action": "N8N-12/N8N-13 (Email Outreach, Follow-up) avec validation humaine obligatoire", "justification": "Volontairement en dernier : ces workflows ne doivent PAS tourner avant la fin du régime A (zéro contact sortant, 31/08) — les rebrancher plus tôt créerait un risque sans bénéfice avant septembre."},
      {"rang": 5, "action": "SF-01/SF-02/SF-04 (Sales Cloud complet) et SF-08 (Agentforce)", "justification": "Nécessite l'authentification SFDX de Sam (effort M, seul Sam peut le faire) et n'a d'utilité qu'une fois le pipeline commercial réellement alimenté — pas avant."}
    ],
    "quick_wins": [
      {"id": "AUT-07-ext", "delai_estime": "< 2h par vue (Delivery, une fois l'arbitrage RGPD tranché sur leads)", "note": "4 des 5 vues (blog_topics, blog_articles, prospects, veille_reports) n'ont AUCUNE contrainte RGPD — peuvent être créées immédiatement, sans attendre Sam. Seule v_deos_leads dépend d'un arbitrage préalable."},
      {"id": "SF-06", "delai_estime": "< 15 min (licence gratuite déjà disponible)", "note": "Un simple clic côté Sam dans l'org Salesforce."},
      {"id": "N8N-07", "delai_estime": "< 30 min", "note": "Tester un credential Calendly n'est pas un développement."},
      {"id": "SCR-01", "delai_estime": "< 10 min", "note": "Une seule question à poser à Sam (emplacement du script) débloque le jugement de cette capacité."},
      {"id": "AUT-05", "delai_estime": "< 30 min", "note": "Provoquer un échec contrôlé d'une ronde (ou attendre la prochaine) pour obtenir la preuve Telegram déjà demandée par le CoS."}
    ],
    "decisions_sam": [
      "Activer la licence Salesforce Integration (Comite_RO) + créer l'utilisateur API lecture seule (SF-06) — gratuit, prérequis de toute la section Salesforce",
      "Trancher le périmètre de champs RGPD exposables sur une future v_deos_leads (condition de DEC-2026-0716-02, déjà en file depuis 19j — cet audit ne fait que confirmer que c'est un chantier SQL de quelques lignes, pas un développement)",
      "Arbitrer Service Cloud Cases vs Postmark->N8N pour le canal de tickets CS (SF-03) — éviter que le CS construise en double avant le 15/08",
      "Arbitrer Salesforce Knowledge vs base de connaissances fichiers déjà planifiée par le CS (SF-05) — avant l'échéance CS du 29/08",
      "Budget/clé API pour un modèle ouvert (MiniMax/GLM/Qwen) sur les workflows désactivés (N8N-09 à N8N-13) — coût récurrent faible mais réel, à valider explicitement",
      "Confirmer l'emplacement réel de regen_covers.py (SCR-01) et du serveur MCP Playwright (AUT-08) — deux capacités citées par l'inventaire que je ne peux ni confirmer ni infirmer depuis mon accès",
      "Clarifier avec Delivery l'écart '18 workflows' (titre) vs 15 nommés dans le document, et l'écart 165 vs 128 exécutions (TAB-06) — deux incohérences chiffrées dans le document de référence obligatoire du comité"
    ],
    "impact_plan_dsi_et_okr_o2": {
      "constat": "Cet audit ne modifie aucune tâche de l'OKR O2 tel que porté par Delivery (les 6 bugs, RAG v2, Stripe prod, Postmark restent des chantiers de code, hors de mon accès, non affectés par ce que j'ai vérifié ici). Mais il change la lecture de la charge de travail globale pré-lancement : la quasi-totalité des 'capacités manquantes' listées indépendamment par les 4 plans de département (Commercial : source prospects, Marketing : SEO/veille, CS : ticketing/knowledge) ne sont PAS des demandes de développement neuf — ce sont des demandes de RACCORDEMENT (vues SQL, arbitrages, credentials) que cet audit chiffre à un effort cumulé très faible (majoritairement S, quelques M) comparé aux 8 chantiers O2 qui, eux, dépendent uniquement du temps de code de Sam, seul développeur.",
      "consequence_priorisation": "Le temps de développement de Sam (ressource la plus rare, confirmée par tous les plans) doit rester concentré sur O2 (diagnostic BUILD en premier, cf. DEC-2026-0716-07 déjà identifiée comme priorité n°1 par Delivery et par le CEO). Les tâches de raccordement identifiées ici (vues v_deos_*, licence Salesforce, arbitrages) ne nécessitent PAS de temps de code de Sam — seulement des arbitrages courts (décisions) et du travail Delivery déjà outillé (SQL sur un mécanisme existant). Ce découplage doit être explicite dans le prochain arbitrage de Sam pour éviter qu'un raccordement à faible coût attende derrière un vrai chantier de développement.",
      "risque_a_signaler": "Deux incohérences chiffrées trouvées dans le document de référence obligatoire du comité (18 vs 15 workflows nommés ; 165 vs 128 exécutions) fragilisent la confiance qu'on peut accorder aux futurs inventaires s'ils ne sont pas corrigés — à traiter comme une dette de fiabilité documentaire, pas seulement un détail.",
      "proposition": "Si un rôle DSI ou équivalent devait porter un plan de département à la prochaine ronde, sa priorité unique serait : obtenir la licence Comite_RO (SF-06) + l'arbitrage RGPD sur leads, pour livrer en moins d'une semaine les 5 vues manquantes (TAB-01 à TAB-05) sans consommer une minute du temps de code de Sam — un déblocage transverse à 3 directeurs pour un coût d'arbitrage quasi nul."
    }
  }
}
```

---

## Narratif

**Ce que j'ai pu vérifier vs. ce que je reprends tel quel.** Sur les 18 (ou 15, voir plus bas) workflows N8N et les 8 capacités Salesforce, je n'ai aucun accès direct — pas d'API N8N dans mon environnement, pas de credential Salesforce dans ce repo (par conception explicite du fichier `config/salesforce_crm_org.md`), et les règles du comité interdisent tout accès Docker/systemctl qui m'aurait permis de sonder les conteneurs. Je reprends donc l'inventaire du Directeur Delivery daté du 02/08 sans le recréer, en le marquant explicitement comme hypothèse à chaque fiche. En revanche, j'ai vérifié moi-même, en direct, ce qui est vérifiable depuis mon accès réel (`$DEOS_RO_DSN`, `$COMITE_DB_DSN`, `/prodlogs`, le dépôt git) : les permissions de 9 tables (toutes verrouillées, confirmant les 4 constats répétés du Commercial), les 4 vues `v_deos_*` (actives, avec un écart de comptage non expliqué sur les exécutions), les 13 décisions et 13 clés `deos_state`, le contenu réel de `/prodlogs/backend-24h.log` (non vide mais couvrant 80 secondes, pas 24h), le code source de `bin/rondes.sh` (alerte Telegram réelle) et de `web/app.py` (dashboard réel), et l'absence de `regen_covers.py` et du serveur MCP Playwright dans mon périmètre.

**Le constat central de cet audit** : la quasi-totalité des « capacités manquantes » que les quatre directeurs ont listées indépendamment aujourd'hui (source de prospects pour le Commercial, veille et SEO pour le Marketing, canal de tickets et base de connaissances pour le CS) ne sont pas des trous à combler par du développement — ce sont des tuyaux déjà posés, coupés au dernier mètre par une vue SQL absente ou un arbitrage non tranché. Le mécanisme technique existe déjà et fonctionne : 4 vues `v_deos_*` tournent, exposent 78 projets et une centaine d'exécutions en lecture seule au comité. Il suffit de le répliquer sur 5 tables de plus (`leads`, `blog_topics`, `blog_articles`, `prospects`, `veille_reports`) — un chantier que je chiffre à moins de 2 heures de travail Delivery pour 4 des 5 (aucune contrainte RGPD), la cinquième (`leads`) ne dépendant plus que d'un arbitrage de périmètre de champs, pas d'un développement.

**Deux points de vigilance croisée que je signale sans les trancher.** Le Salesforce Developer Edition (Service Cloud Cases, Knowledge) offre des capacités qui recoupent directement des chantiers déjà planifiés indépendamment par le CS (canal Postmark->N8N validé le 14/07, base de connaissances fichiers prévue au 29/08). Sans arbitrage explicite de Sam, le risque est que le CS construise en double une architecture que Salesforce pourrait fournir nativement — ou l'inverse. Ce n'est pas mon rôle de trancher à sa place, mais mon audit doit le nommer avant que l'effort ne soit engagé dans les deux directions à la fois.

**Deux incohérences chiffrées dans le document de référence lui-même**, que je ne peux résoudre depuis mon accès : le titre annonce 18 workflows N8N, mais seuls 15 sont nommément listés ; l'inventaire et le rapport Commercial citent 165 exécutions dans la base pendant que ma requête directe sur l'unique vue accessible (`v_deos_executions`) en montre 128. Ce ne sont pas des détails cosmétiques : ce document sert de référence obligatoire pour éviter que les directeurs ne proposent de recréer l'existant — s'il se trompe sur son propre décompte, sa fiabilité globale en pâtit. Je les signale à Delivery plutôt que de trancher dans un sens ou dans l'autre.

**A. Séquence recommandée** : (1) licence Salesforce Comite_RO + extension des vues `v_deos_*` aux 5 tables verrouillées — coût quasi nul, déblocage transverse Commercial/Marketing en une seule passe ; (2) réactivation en cascade du pipeline de sourcing commercial (Lead Capture, Veille Concurrence, LinkedIn Enrichment) une fois DEC-2026-0716-01 tranchée ; (3) arbitrages Salesforce Service Cloud/Knowledge vs plans CS déjà engagés, avant que le CS n'avance seul vers ses échéances du 15/08 et 29/08 ; (4) Email Outreach/Follow-up Relances, délibérément en dernier — ils ne doivent tourner qu'après la fin du régime A (31/08) ; (5) Sales Cloud complet et Agentforce, qui nécessitent le temps rare de Sam (auth SFDX) et n'ont d'utilité qu'une fois le pipeline réellement alimenté.

**B. Quick wins (< 2h)** : les 4 vues sans contrainte RGPD (`blog_topics`, `blog_articles`, `prospects`, `veille_reports`), l'activation de la licence Salesforce Comite_RO, un test du credential Calendly, une question à Sam sur l'emplacement de `regen_covers.py`, et la provocation d'un échec contrôlé de ronde pour obtenir la preuve Telegram déjà réclamée par le CoS.

**C. Ce qui exige une décision de Sam** : le périmètre RGPD de `v_deos_leads` ; l'arbitrage Service Cloud vs Postmark pour les tickets CS ; l'arbitrage Knowledge vs base de connaissances fichiers ; un budget pour une clé API de modèle ouvert sur les 5 workflows désactivés ; la confirmation d'emplacement de `regen_covers.py` et de connexion du MCP Playplaywright ; et la clarification des deux incohérences chiffrées du document de référence.

**D. Impact sur mon propre plan et sur l'OKR O2** : cet audit ne touche à aucun des 8 chantiers de code d'O2 (hors de mon accès, non affectés par mes vérifications). Ce qu'il change, c'est la priorisation du temps de Sam : la quasi-totalité des demandes de « capacités manquantes » des quatre directeurs ne consomment pas de temps de développement — seulement des arbitrages courts et du travail Delivery sur un mécanisme déjà prouvé. Le temps de code de Sam, ressource la plus rare confirmée par tous les plans, doit rester concentré sur le diagnostic BUILD (DEC-2026-0716-07, déjà identifié comme priorité n°1 par Delivery et le CEO) plutôt que d'être dilué sur des raccordements qui ne le nécessitent pas. Si un rôle DSI devait porter un plan de département à la prochaine ronde, sa priorité unique serait la licence Comite_RO + l'arbitrage RGPD sur `leads` : un déblocage transverse à 3 directeurs pour un coût d'arbitrage proche de zéro.
