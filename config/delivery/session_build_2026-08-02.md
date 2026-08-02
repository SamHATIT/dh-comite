# Session BUILD du 2026-08-02 — compte rendu pour le Directeur Delivery
> À lire avant le comité hebdomadaire du 03/08. Rédigé par Claude avec Sam, sur accès complet
> à la production (logs worker, code, base). Tous les faits ci-dessous sont vérifiés.

## 1. Le BUILD n'était pas cassé — corrige ton diagnostic

Ton rapport concluait à une panne systémique (« phase 1 data_model, 3/3, 0 succès historique »).
Cette conclusion était rigoureuse au vu de tes données, mais tes données étaient incomplètes :
la vue `v_deos_build_phases` n'exposait pas `last_error`. Elle l'expose désormais (avec
`attempt_count`, `started_at`, `completed_at`).

Les trois échecs avaient TROIS causes distinctes :
- exécution 131 (février) : « No batches generated » — ancienne, antérieure à des dizaines de correctifs
- exécution 147 (mai) : « Deploy failed: SF Admin service not initialized » — l'org n'était pas
  connectée ; résolu depuis le 14/07
- exécution 165 (15/07) : « run interrompu » — interruption volontaire de Sam pendant l'application
  de correctifs. Ce n'était pas un échec technique.

## 2. Cause racine du blocage réel : le clip d'Elena

`salesforce_qa_tester.py` remettait à Elena `code_content[:80000]`. Le plan agrégé de Raj fait
~168 000 caractères. Elena lisait donc une moitié de fichier et rejetait « JSON tronqué » —
sur un livrable complet. Trois semaines de blocage pour cette ligne.
Correctif `FIX-REVIEW-CLIP-001` : limite portée à 600 000 caractères + avertissement journalisé
si le clip s'applique quand même.

## 3. Le worker ARQ était arrêté depuis le 15/07

`digital-humans-worker.service` en état `failed (timeout)` depuis 2 semaines et 4 jours, malgré
`Restart=always`. Les 40 tâches de l'exécution 165 attendaient en PENDING. C'est cela, « le BUILD
en pause ». **À surveiller désormais dans ta ronde** : l'état du worker, pas seulement le backend.

## 4. Le routage des tâches envoyait n'importe quoi à Raj — la découverte majeure

`group_tasks_by_phase` ne connaissait pas les agents `devops`, `trainer` et `qa` : ces tâches
tombaient sur `else: phase = 1`, donc chez Raj. Et Raj, agent du modèle de données, les modélisait
consciencieusement en objets Salesforce :

| Tâche WBS | Objet inventé par Raj |
| --- | --- |
| Configurer le dépôt Git et la stratégie de branches | `Depot_Git__c`, `Strategie_Branche__c`, `Regle_Protection_Branche__c` |
| Rédiger la documentation de l'Integration User | `Documentation_Integration_User__c` |
| Préparer le package de déploiement | `Checklist_Preparation_Package__c` |
| Élaborer le plan de test et les scénarios UAT | `Scenario_UAT__c`, `Execution_Test_UAT__c` |
| Exécuter le déploiement en production | `JournalErreurDeploiementProd__c` |

Le WBS de Marcus était excellent (champs `Source_DH__c`, `Score_Qualification__c`, `Tier_Vise__c`,
`OpportunityTrigger`, batch de relances, permission set `Comite_RO`, application Lightning,
rapports). C'est le routage qui était fautif, pas la conception.

Correctifs : `FIX-ROUTING-001` (devops/trainer → phase 6, qa → phase 2, défaut → phase 6 avec
avertissement) et `FIX-SCOPE-001` (garde-fou dans le prompt de Raj : retour `out_of_scope` motivé
au lieu d'inventer un objet).

## 5. Les 7 autres correctifs de la session
`FIX-BUILDV2-MAXTOKENS-2` (Raj 16k→64k, Elena 16k→32k) · `FIX-TASKVIS-001` (passerelle phases
BUILD ↔ tâches WBS + préfixe « Phase N » à la création) · `FIX-BATCHPROG-001` (publication de
l'avancement lot par lot) · `llm_interactions.task_id` varchar(50)→255 · `sf_org_id` renseigné sur
les projets 106/107 · `git_repo_url` renseigné (dépôt `dh-crm-salesforce` créé) · vue
`v_deos_build_phases` enrichie.
Commits : 1003baa, da7b1d6, c2a0166, d65d13f, 2bf8def.

## 6. L'économie unitaire — ton sujet n°1

Exécution 165 : **26,13 $ et 2,57 M de jetons sans franchir la phase 1** sur six.
Deux causes mesurées :
- **contexte inter-lots quadratique** : chaque lot produit est réinjecté dans le contexte du
  suivant (`register_batch_output`), donc le 12e porte les 11 précédents. Entrées d'Elena :
  35 953 → 37 128 → 37 331 → 58 799 jetons.
- **régénération intégrale** : 12 lots refaits quand 3 étaient rejetés.

Correction d'une erreur d'analyse : Elena n'est PAS verbeuse. Sa réponse fait 6 577 caractères
pour 58 799 jetons d'entrée. Le compteur `tokens_output` de `llm_interactions` sur ses lignes est
un agrégat de la tentative, pas sa production. Ce qui coûte, c'est ce qu'on lui envoie.

## 7. Ce que Sam attend de toi (décisions au registre)

- **DEC-2026-0802-03 — travail incrémental (delta), PRIORITÉ 1.** Cadrage de Sam : « comme on écrit
  en base, on ne renvoie que les modifications demandées et éventuellement les éléments impactés ».
  Concrètement : ne régénérer que les lots rejetés par Elena et leurs dépendances ; ne transmettre
  au lot suivant que les références nécessaires (noms d'objets et de champs déjà créés), pas les
  définitions entières.
- **DEC-2026-0802-02 — reprise sur incident.** Sauter les phases déjà `completed` au lieu de
  repartir de la phase 1.
- **DEC-2026-0802-04 — rationalisation Salesforce.** Tout sur Salesforce : tickets en Email-to-Case
  natif, base de connaissances en Knowledge. Seule exception : le mailing de masse passera par un
  outil dédié, pour ne pas exposer la réputation d'expéditeur de l'org.

À traiter à froid, avec test dédié, et dans cet ordre. Le travail est désormais sain : Raj ne
recevra plus que du vrai modèle de données.

## 8. État à l'instant
Worker arrêté volontairement, exécution 165 en CANCELLED, dépense stoppée. Le dépôt
`dh-crm-salesforce` est en place et l'org connectée : la prochaine relance peut aller au bout.
