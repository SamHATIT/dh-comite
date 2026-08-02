# CAPACITÉS DISPONIBLES — ce qui existe déjà chez Digital·Humans
> **Document de référence obligatoire.** Tout directeur qui propose un outil, un workflow ou une capacité DOIT d'abord vérifier ici si l'équivalent existe déjà, même dormant. Une proposition qui recrée l'existant sera refusée par le CEO.
> Établi le 2026-08-02 par inventaire direct du serveur. Tenu à jour par le Directeur Delivery.

## 1. Workflows N8N (18 au total)
N8N est actif sur le VPS. Ces workflows sont DÉJÀ CONSTRUITS : déclencheurs, appels LLM, écritures en base, envois d'emails. Il leur manque le plus souvent une source à jour, un modèle à repointer, ou un rebranchement.

### 1.1 Actifs et fonctionnels
| Workflow | Ce qu'il fait réellement | Utile à |
| --- | --- | --- |
| Blog - Newsletter Hebdo (lundi 9h) | Envoi newsletter, 2 exécutions réussies | Marketing |
| Blog - Veille Hebdo (jeudi 20h) | Collecte de veille hebdo, 2 exécutions réussies | Marketing, Commercial |
| Blog - Topics API | Webhook multi-action : approuver/rejeter/générer un article, écrit en base | Marketing |
| Blog - Topics Dashboard | Gestion des sujets d'articles | Marketing |
| Content Articles - Blog Generator | Webhook -> génération d'article par LLM -> base -> notification | Marketing |
| Lead Capture - Website | Webhook -> lead en base -> email de vérification -> réponse | Commercial |
| Meeting Booking - Calendly | Prise de rendez-vous (credential à vérifier) | Commercial |
| Dashboard Acquisition - Metrics / Web UI | Agrégation de métriques depuis PostgreSQL + rendu | Commercial, Marketing, CEO |

### 1.2 Désactivés le 14/07 — à MODERNISER, PAS à recréer
Désactivés car ils reposaient sur un modèle local abandonné (Mistral Nemo/Ollama) et pouvaient envoyer des emails sans validation. Leur structure reste excellente : il suffit de repointer l'appel LLM et d'ajouter une validation humaine.

| Workflow | Structure existante (nœuds réels) | Réutilisable pour |
| --- | --- | --- |
| Veille Concurrence | Déclencheur quotidien -> lecture RSS (Salesforce Blog, Salesforce Ben...) -> filtre 24h -> analyse LLM -> parsing -> écriture dans veille_reports -> email | Veille marché (Commercial), matière éditoriale (Marketing), veille release (Delivery) |
| LinkedIn Enrichment - Prospects | Webhook prospect -> préparation -> validation -> analyse/enrichissement LLM -> parsing -> écriture dans prospects | Enrichissement et qualification de prospects (Commercial) |
| Lead Scoring | Déclencheur planifié + webhook -> code de scoring -> PostgreSQL | Scoring automatisé (Commercial) |
| Email Outreach | Déclencheur planifié -> conditions -> composition -> envoi email -> suivi en base | Séquences de relance (Commercial), avec validation ajoutée |
| Follow-up Relances | Même structure, orientée relance | Relances (Commercial), avec validation |

POINT CLÉ SOURCING : la chaîne Lead Capture -> LinkedIn Enrichment -> Lead Scoring -> (validation) -> Email Outreach constitue déjà un pipeline de prospection complet. Il ne manque que la SOURCE D'ENTRÉE (le scraping) et la COUCHE DE VALIDATION humaine. Ce n'est pas un outil à construire, c'est un outil à rebrancher.

### 1.3 Archivés
Rapport Quotidien 8h et Bilan Hebdomadaire lundi 9h : remplacés par le daily brief et le comité hebdo.

## 2. Données déjà en base (PostgreSQL production)
Ces tables existent et sont alimentées. AUCUN directeur ne les consultait jusqu'ici.

| Table | Contenu réel au 02/08 | Pour qui |
| --- | --- | --- |
| leads | 7 leads (email, nom, société, source, vérifié) — aujourd'hui des tests, mais le tuyau fonctionne | Commercial |
| blog_topics | 33 sujets d'articles : 21 en attente, 5 approuvés, 7 générés (ex. « Automating Salesforce Release Management with Salesforce DX ») | Marketing |
| blog_articles | Vide, prête à recevoir les articles générés | Marketing |
| prospects | Vide, schéma prêt (alimentée par LinkedIn Enrichment) | Commercial |
| veille_reports | Vide (workflow désactivé) — se remplit dès réactivation | Commercial, Marketing, Delivery |
| projects / executions / agent_deliverables / build_phase_executions | 78 projets, 165 exécutions — matière pour cas d'usage, références, baselines | Tous, via les vues v_deos_* |

## 3. Salesforce — Developer Edition connectée
Org digital-humans-dev authentifiée (API 67.0, Summer '26), workspace SFDX sous git, projet CRM spécifié. Licences disponibles et INUTILISÉES :

| Capacité | Statut | Ce qu'elle remplace |
| --- | --- | --- |
| Sales Cloud (Leads, Opportunités, Comptes) | Disponible | Le pipeline commercial en base — CRM complet sans développement |
| Reports & Dashboards natifs | Disponible | Toute dataviz commerciale à construire |
| Service Cloud + Cases | Disponible | Le canal de tickets du CS (Email-to-Case natif : SLA, files, historique) |
| Campaigns (licence Marketing User) | Disponible | L'attribution contenu -> lead du Marketing |
| Knowledge | Disponible | La base de connaissances support du CS |
| Licence Salesforce Integration (1 dispo) | Disponible | L'utilisateur API lecture seule du comité (Comite_RO), gratuit |
| 450 000 appels API/mois | Disponible | Aucune contrainte de volume |
| Agentforce (201 + 10 000 licences) | Disponible | Sujet stratégique, hors périmètre immédiat |

## 4. Modèles LLM et routage par tâche
RÈGLE : le modèle se choisit par la nature de la tâche. Un modèle cher sur une tâche simple est un gaspillage ; un modèle faible sur un arbitrage est un risque.

| Tâche | Modèle | Pourquoi |
| --- | --- | --- |
| Comité hebdo, analyse croisée, arbitrages | Fable 5 | Raisonnement long, détection d'incohérences inter-domaines |
| Brief quotidien, consolidation | Opus (semaine) | Bon rapport qualité/prix sur la synthèse |
| Rondes des directeurs, diagnostics, rédaction | Sonnet | Suffisant et économique pour l'exécution outillée |
| Résumé, extraction, classement, reformatage | Haiku | Tâches mécaniques : ~10x moins cher, qualité équivalente |
| Génération de masse en arrière-plan (veille, brouillons d'articles, enrichissement) | Modèle ouvert en API (MiniMax, GLM, Qwen) | ~5x moins cher que Sonnet, qualité suffisante hors arbitrage — cas d'usage exact des workflows N8N |
| Ollama local sur le VPS | À ÉVITER | Le VPS n'a PAS de GPU : un 26B en CPU ne produit pas un token en 3 minutes. Installé mais inexploitable en temps réel |

CONSÉQUENCE N8N : les cinq workflows désactivés pointaient sur Ollama local (127.0.0.1:11434). Il faut repointer leur nœud LLM vers une API de modèle ouvert — changement d'URL et de clé, pas une reconstruction.

## 5. Autres capacités existantes
| Capacité | État | Pour qui |
| --- | --- | --- |
| Ghost CMS (blog, Docker) | Actif — API Admin pour lecture des stats et dépôt de brouillons | Marketing |
| Concierge Sophie (/api/public/concierge/talk) | Actif sur le site — capte des conversations visiteurs, NON exposé au comité | Commercial |
| Script regen_covers.py | Existant — génération d'images de couverture | Marketing |
| Skill dh-fr-copywriting | Installé dans le comité | Marketing et tout contenu client |
| Watchdog services (15 min) | Actif — alerte Telegram si backend/postgres/nginx/n8n tombe | Delivery |
| Bot Telegram @dh_comite_bot | Actif — brief, CR de comité, alertes | Tous, via le CEO |
| Tableau de bord /comite/ | Actif — vue globale, drill-down, rapports détaillés | Sam |
| Vues v_deos_* (lecture seule) | Actives — exécutions, sections, projets, phases BUILD | Delivery, CS, Commercial |
| Playwright MCP | Serveur MCP disponible sur le VPS | Scraping et automatisation navigateur (à évaluer) |

## 6. Ce qui manque réellement (après inventaire)
1. Une SOURCE de sourcing de prospects en entrée du pipeline existant (scraping — décision de Sam : sourcing externe, pas son réseau). Le reste de la chaîne existe.
2. Une COUCHE DE VALIDATION humaine avant tout envoi externe (workflows Email Outreach et Follow-up).
3. L'ACCÈS du comité aux données déjà en base : leads, blog_topics, prospects, veille_reports (vues à créer).
4. Le REPOINTAGE LLM des cinq workflows désactivés vers une API de modèle ouvert.
5. Les ACCÈS du Delivery : logs du worker BUILD, source de suivi des chantiers O2.
6. Postmark / SMTP-PROD-001 : condition d'envoi réel.

Tout le reste — CRM, dashboards, base de connaissances, tickets, veille, génération d'articles, capture de leads, enrichissement, scoring — EXISTE DÉJÀ sous une forme ou une autre.
