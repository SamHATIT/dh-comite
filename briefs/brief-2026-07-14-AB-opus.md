```json
{
  "date": "2026-07-14",
  "agent": "ceo",
  "edition": "second daily du jour — 5/5 rapports directeurs reçus",
  "hier": {
    "delivery": [
      {"texte": "Backend en bonne santé : /health répond 200 'healthy' au moment de la ronde. 0 exécution RUNNING, 9 WAITING_BR_VALIDATION inchangées et confirmées par Sam (13/07) comme tests internes — aucune relance client.", "source": "rapport_delivery 2026-07-14 — http:172.19.0.1:8002/health#2026-07-14T10:49:35Z ; postgres:v_deos_executions#85,86,120,140,149,150,151,152,158"},
      {"texte": "Fin de 30 jours d'inactivité : 2 exécutions du projet test 'LogiFleet G3 (v2 corpus)' le 13/07 — 161 CANCELLED après 10 min (0 ERROR), 162 COMPLETED en 43min28, 8,86$, coût/durée dans la plage historique. Aucune dérive.", "source": "rapport_delivery 2026-07-14 — postgres:v_deos_executions#161,162"},
      {"texte": "0 ERROR/WARNING mais fenêtre de logs limitée à 1h28 (13/07 18:10→19:38 UTC), calée sur un redémarrage backend : ~15h de silence log avant la ronde, sans preuve d'activité ni d'erreur.", "source": "rapport_delivery 2026-07-14 — logs:2026-07-13T18:10:15Z→19:38:22Z ; stat backend-24h.log#mtime 2026-07-14T10:45:02Z"}
    ],
    "commercial": [
      {"texte": "Première ronde commerciale. Pipeline vide (0 lead, 0 prospect), aucun objectif hebdomadaire jamais fixé par Sam (clé objectifs_commerciaux absente) → domain_score non calculable.", "source": "rapport_commercial 2026-07-14 — deos-state:list#2026-07-14T11:32Z"},
      {"texte": "Source de leads concierge (table 'leads' prod) inaccessible au comité : permission denied (attendu, phase 2 non branchée). Aucune tentative de contournement. Seule alimentation possible aujourd'hui : saisie manuelle sourcée — non survenue.", "source": "rapport_commercial 2026-07-14 — psql $DEOS_RO_DSN 'leads'#2026-07-14T11:33Z → permission denied"},
      {"texte": "Schéma de stockage pipeline_commercial mis en conformité (legacy {maj,leads:[]} → schéma cible par stades), sans ajout/modif/suppression de donnée (0 lead avant/après). Signalé pour validation a posteriori (curseur maj_pipeline = agit_sous_validation).", "source": "rapport_commercial 2026-07-14 — deos-state pipeline_commercial#2026-07-14T11:34Z ; config/agent_autonomy_map.yaml"}
    ],
    "marketing": [
      {"texte": "Première ronde marketing. Séquence de lancement proposée : 13 contenus datés du 2026-07-21 au 2026-10-13 (About, post pivot, 11 portraits d'agents), ordre = chronologie du pipeline — hypothèse déclarée, à valider par Sam.", "source": "rapport_marketing 2026-07-14 — calendrier_delta.sequence_proposee_resume"},
      {"texte": "2 BrouillonContenu produits (CONT-2026-0714-01 refonte About, CONT-2026-0714-02 post pivot), opérationnalisant pour la première fois en public le positionnement tech×luxe / argument DEOS déjà acté. Discipline 'un contenu à la fois' appliquée.", "source": "rapport_marketing 2026-07-14 — faits ; .claude/agents/directeur-marketing.md"},
      {"texte": "domain_score non calculable ce jour (calendrier vide à l'ouverture de la ronde) ; la formule s'appliquera dès la prochaine ronde. Aucune donnée de performance n'existe (aucune publication antérieure).", "source": "rapport_marketing 2026-07-14 — calcul_score ; deos-state:list#2026-07-14"}
    ],
    "cs": [
      {"texte": "Première ronde CS, mode dégradé assumé : 0 compte client réel (clé comptes_clients absente), 0 canal de tickets. État attendu avant le lancement client de septembre 2026 (confirmé Sam 13/07), pas un incident — mais rendu visible pour ne pas être confondu avec une santé calculée.", "source": "rapport_cs 2026-07-14 — deos-state:list#2026-07-14T11:16Z"},
      {"texte": "4 identifiants techniques historiques (user_id 2,4,5,6), tous des tests internes, aucun mapping vers une société possible depuis la prod. Seul user_id 2 actif <30j (dernière exéc. 13/07) : 114 exéc. sur 8 mois, 29% FAILED / 23% CANCELLED — donnée de calibration baseline, pas un signal de churn.", "source": "rapport_cs 2026-07-14 — postgres:v_deos_projects×v_deos_executions#2026-07-14T11:34Z"},
      {"texte": "Schéma comptes_clients + parcours d'onboarding type proposés (non écrits en base, curseur agit_sous_validation) — soumis à validation de Sam avant initialisation.", "source": "rapport_cs 2026-07-14 — structure_proposee"}
    ],
    "cos": [
      {"texte": "Table decisions : 1 close avec preuve (DEC-2026-0713-01), décisions ouvertes sans retard (âge max 0j), aucun skill proposé en file. Score exécution 100 (vert).", "source": "rapport_cos 2026-07-14 — deos-decisions:list#2026-07-14 ; calcul_score"},
      {"texte": "Écart brief↔table corrigé dans la ronde : les 3 decisions_attendues du brief (DA-2026-0714-01/02/03) n'étaient pas tracées → création de DEC-2026-0714-02/03/04 (statut attente_sam), action dans le scope CoS.", "source": "rapport_cos 2026-07-14 — execution_delta.ecarts_brief_table"},
      {"texte": "Surveillance cash INACTIVE (clé cash_suivi jamais alimentée, aucun seuil déclaré) et priorites_semaine absente : une surveillance inactive doit se voir — aucune projection produite d'initiative.", "source": "rapport_cos 2026-07-14 — deos-state:list#2026-07-14"}
    ]
  },
  "kpis": [
    {"nom": "service_backend_up", "domaine": "delivery", "statut": "vert", "valeur": "1/1", "source": "rapport_delivery — http:/health#2026-07-14T10:49:35Z"},
    {"nom": "executions_bloquees_techniquement", "domaine": "delivery", "statut": "vert", "valeur": "0/9", "source": "rapport_delivery — postgres:v_deos_executions"},
    {"nom": "erreurs_logs_fenetre_disponible", "domaine": "delivery", "statut": "vert", "valeur": "0 (fenêtre réduite à 1h28)", "source": "rapport_delivery — logs:2026-07-13T18:10:15Z→19:38:22Z"},
    {"nom": "leads_qualifies", "domaine": "commercial", "statut": "ambre", "valeur": "0/0 (pipeline vide, aucun objectif)", "source": "rapport_commercial — deos-state:list#2026-07-14T11:32Z"},
    {"nom": "objectifs_hebdo_commerciaux_definis", "domaine": "commercial", "statut": "ambre", "valeur": "0 (clé absente)", "source": "rapport_commercial — deos-state get objectifs_commerciaux#2026-07-14T11:32Z"},
    {"nom": "contenus_sequence_produits", "domaine": "marketing", "statut": "ambre", "valeur": "2/13 (en attente validation Sam)", "source": "rapport_marketing — CONT-2026-0714-01/02"},
    {"nom": "contenus_valides", "domaine": "marketing", "statut": "ambre", "valeur": "0/2", "source": "rapport_marketing — aucune validation Sam à ce jour"},
    {"nom": "comptes_clients_enregistres", "domaine": "cs", "statut": "info", "valeur": "0 (mode dégradé confirmé Sam)", "source": "rapport_cs — deos-state:list#2026-07-14T11:16Z"},
    {"nom": "incident_delivery_touchant_un_client", "domaine": "cs", "statut": "vert", "valeur": "0", "source": "rapport_cs — deos-state get rapport_delivery#2026-07-14"},
    {"nom": "decisions_en_retard", "domaine": "execution", "statut": "vert", "valeur": "0/4", "source": "rapport_cos — deos-decisions:list#2026-07-14"},
    {"nom": "cash_suivi_alimente", "domaine": "execution", "statut": "ambre", "valeur": "0 (surveillance inactive)", "source": "rapport_cos — deos-state:list#2026-07-14"},
    {"nom": "couverture_comite", "domaine": "gouvernance", "statut": "ambre", "valeur": "5/5 rapports produits, mais 3/5 domain_score non calculables", "source": "contexte daily 2026-07-14 — B1"}
  ],
  "sante": {
    "score": 100,
    "statut": "ambre",
    "tendance": "stable → (100 ambre au brief du matin ; couverture passée de 1/5 à 5/5 rapports, mais 3 domaines restent non calculables)",
    "calcul": "Delivery 100×0,30 + Exécution(CoS) 100×0,10 = 40. Commercial, CS et Marketing ont rapporté ce jour mais leur domain_score est non calculable (inputs fondateurs manquants côté Sam : objectifs commerciaux, schéma comptes_clients, calendrier éditorial validé) → recalcul sur les poids disponibles : 40 / (0,30+0,10) = 100. Statut plafonné à AMBRE : 3 domaines sur 5 sans score exploitable [DH-CEO-003].",
    "domain_scores": {"delivery": 100, "execution": 100, "commercial": null, "cs": null, "marketing": null},
    "domaines_manquants": ["commercial (rapporté mais non calculable — objectifs absents)", "cs (rapporté mais non calculable — 0 compte réel)", "marketing (rapporté mais non calculable — calendrier vide à l'ouverture)"]
  },
  "priorites_jour": [
    {"rang": 1, "texte": "Assurer le suivi de DEC-2026-0714-01 (interface web globale de suivi du comité), accordée par Sam — confirmer qui exécute et le jalon attendu.", "source": "B2 — deos-decisions#DEC-2026-0714-01 (statut accordee)", "origine": "décision de Sam en cours"},
    {"rang": 2, "texte": "Faire valider par Sam la séquence éditoriale (13 contenus) + les 2 brouillons (About, post pivot) : seule production du comité avec une échéance externe (séquence jusqu'à fin oct. 2026) et des livrables concrets prêts — rien ne se publie sans validation [DH-CMO-001].", "source": "rapport_marketing 2026-07-14 — calendrier_delta", "origine": "décision demandée à fort impact"},
    {"rang": 3, "texte": "Obtenir de Sam les objectifs hebdo commerciaux : c'est le domaine le plus lourdement pondéré (0,25) et le plus simple à débloquer ; son absence est la première cause du plafond ambre.", "source": "rapport_commercial 2026-07-14 — decisions_demandees ; B4 sante_ponderations", "origine": "décision demandée à fort impact"},
    {"rang": 4, "texte": "Fiabiliser l'export des logs backend (fenêtre glissante 24h réelle, aujourd'hui tronquée au dernier restart) — DA-2026-0714-01 / DEC-2026-0714-02, à confier à l'équipe technique avant le lancement client.", "source": "rapport_delivery 2026-07-14 — opportunites ; brief matin DA-01", "origine": "décision demandée à fort impact"},
    {"rang": 5, "texte": "Trancher la cadence/le calendrier officiels des rondes des 5 directeurs (DEC-2026-0714-03, attente_sam) et décider de l'activation de la surveillance cash + des priorités de semaine (clés deos_state absentes).", "source": "rapport_cos 2026-07-14 — execution_delta ; B2 DEC-2026-0714-03", "origine": "gouvernance / décision demandée"}
  ],
  "decisions_attendues": [
    {"id": "DA-2026-0714-04", "texte": "[MARKETING] Valider (ou corriger) la séquence des 13 contenus + les 2 BrouillonContenu (CONT-...-01 About, CONT-...-02 post pivot) avant toute programmation [DH-CMO-001]. Impact : débloque la chaîne hebdomadaire de contenu vers le lancement de septembre ; seule échéance externe du comité.", "source": "rapport_marketing 2026-07-14 — calendrier_delta.decision_demandee", "destinataire": "sam"},
    {"id": "DA-2026-0714-05", "texte": "[COMMERCIAL] Fixer les objectifs hebdo commerciaux (leads qualifiés visés, dossiers à produire, relances). Impact : rend le domain_score commercial (poids 0,25) calculable et lève la plus lourde part du plafond ambre.", "source": "rapport_commercial 2026-07-14 — decisions_demandees", "destinataire": "sam"},
    {"id": "DA-2026-0714-06", "texte": "[CS] Valider le schéma comptes_clients + le parcours d'onboarding type et fixer une date cible d'initialisation avant septembre 2026. Impact : formule de santé CS opérationnelle dès le premier compte réel plutôt que construite dans l'urgence.", "source": "rapport_cs 2026-07-14 — structure_proposee ; decisions_demandees", "destinataire": "sam"},
    {"id": "DEC-2026-0714-02", "texte": "[DELIVERY] Fiabilisation de l'export de logs (fenêtre 24h réelle) : décider qui exécute — production en lecture seule pour le comité, correctif = équipe technique (curseur delivery.correctifs = agit_sous_validation).", "source": "rapport_delivery 2026-07-14 — opportunites ; brief matin DA-01", "destinataire": "sam"},
    {"id": "DEC-2026-0714-03", "texte": "[GOUVERNANCE] Acter la cadence et le calendrier officiels des rondes des 5 directeurs, et décider d'activer (ou non) la surveillance cash et les priorités de semaine. Impact : cadre récurrent du comité + surveillance financière visible.", "source": "rapport_cos 2026-07-14 — execution_delta ; B2 DEC-2026-0714-03 (attente_sam)", "destinataire": "sam"}
  ],
  "alertes": [
    {"texte": "Score plafonné ambre : 3 des 5 domaines (commercial 0,25 + CS 0,20 + marketing 0,15 = 60% des pondérations) ont rapporté mais restent non calculables faute d'inputs fondateurs de Sam (objectifs, schéma comptes, calendrier validé). Le 100 ne repose que sur delivery + exécution (40% des poids). La couverture a progressé (1/5→5/5) mais le score n'est pas encore un vrai reflet de santé.", "source": "B1 (5 rapports) ; B4 sante_ponderations", "gravite": "moyenne"},
    {"texte": "Surveillance cash INACTIVE : aucune donnée, aucun seuil déclaré par Sam (clé cash_suivi jamais alimentée). Le CoS ne produit aucune projection d'initiative — l'angle mort financier doit rester visible.", "source": "rapport_cos 2026-07-14 — deos-state:list#2026-07-14", "gravite": "moyenne"},
    {"texte": "Source de leads concierge (Sophie) inaccessible au comité (permission denied, phase 2 non branchée) : aucune alimentation automatisée du pipeline commercial n'est possible avant ce branchement — à planifier ou à confirmer hors périmètre avant septembre 2026.", "source": "rapport_commercial 2026-07-14 — psql permission denied#2026-07-14T11:33Z", "gravite": "moyenne"},
    {"texte": "Incohérence de comptage à réconcilier : le KPI CoS déclare 4 décisions ouvertes (DEC-02/03/04 créées ce jour) alors que la liste B2 des décisions en cours n'en affiche que 2 (DEC-01 accordee, DEC-03 attente_sam). Probable décalage de snapshot ; présenté côte à côte, à vérifier au prochain passage. Aucune donnée masquée.", "source": "rapport_cos 2026-07-14 (execution_delta, kpi decisions_ouvertes 4/5) vs B2 deos-decisions:list#2026-07-14", "gravite": "basse"},
    {"texte": "Fenêtre de logs réellement disponible limitée à 1h28, calée sur le dernier redémarrage backend : ~15h de silence log avant la ronde. Profondeur de vérification réduite en cas d'incident antérieur au restart (sans conséquence aujourd'hui — 0 client réel).", "source": "rapport_delivery 2026-07-14 — logs:2026-07-13T18:10:15Z ; stat backend-24h.log#mtime", "gravite": "basse"},
    {"texte": "Écart de schéma pipeline_commercial corrigé sans validation préalable (curseur maj_pipeline = agit_sous_validation) : 0 donnée touchée (0 lead avant/après), seule la structure a changé — validation a posteriori demandée par le directeur commercial par prudence.", "source": "rapport_commercial 2026-07-14 — alertes ; config/agent_autonomy_map.yaml", "gravite": "basse"},
    {"texte": "Rôle de l'agent Lucas non documenté dans le repo : le portrait rang 13 (échéance 2026-10-13) ne pourra être rédigé sans complément d'information — à demander à Sam ou au directeur delivery avant cette date. Pas d'urgence (3 mois).", "source": "rapport_marketing 2026-07-14 — alertes", "gravite": "basse"}
  ],
  "opportunites": [
    {"texte": "Constituer une bibliothèque de cas d'usage anonymisés à partir des 76 projets internes (v_deos_projects) pour équiper les futurs dossiers de démo — sous réserve stricte 'cas de test interne, pas de référence client' et de la limite 'pas de déploiement production' de l'offre canonique.", "source": "rapport_commercial + rapport_marketing 2026-07-14 — v_deos_projects#2026-07-14T11:33Z ; config/offre_dh.md"},
    {"texte": "Exploiter les 8 mois d'historique d'exécutions (user_id 2 notamment) pour calibrer une première baseline 'usage' (40 pts de la formule santé CS) avant l'arrivée des premiers comptes réels en septembre 2026, et activer le canal de tickets (clé deos_state 'tickets') pour ne pas démarrer en mode dégradé.", "source": "rapport_cs 2026-07-14 — opportunites"},
    {"texte": "Constituer un backlog PropositionEvolution formel et tracé en deos_state (clé backlog_evolutions_delivery, absente) pour fiabiliser le critère 'évolutions P1 en retard' du domain_score delivery — aujourd'hui supposé à 0 faute de traçabilité, pas par preuve. Ouvert depuis le 13/07.", "source": "rapport_delivery 2026-07-14 — opportunites"}
  ],
  "escalades": [],
  "recommandation": {
    "texte": "Consacrer une courte session cette semaine à valider la séquence éditoriale de lancement (13 contenus) et les 2 brouillons prêts (About, post pivot) — puis, dans la foulée, fixer les objectifs hebdo commerciaux.",
    "argument": "Le comité est désormais complet (5/5 rapports), mais presque tout est en attente d'inputs fondateurs de ta part — et une seule production a une échéance externe ET des livrables concrets déjà rédigés : la séquence marketing (elle court jusqu'à fin octobre 2026, en amont du lancement payant de septembre, et rien ne se publie sans ta validation [DH-CMO-001]). C'est le seul geste qui, aujourd'hui, transforme du travail préparé en résultat public et amorce une cadence hebdomadaire. Immédiatement derrière : les objectifs commerciaux, l'input le plus lourdement pondéré (0,25) et le plus simple à donner, qui à lui seul lève la plus grosse part du plafond ambre. Les autres domaines (CS, logs, cadence) préparent septembre 2026 sans urgence propre et figurent dans les décisions attendues.",
    "source": "rapport_marketing 2026-07-14 (calendrier_delta, 2 BrouillonContenu prêts) ; rapport_commercial 2026-07-14 (objectifs_commerciaux absent, poids 0,25) ; B4 sante_ponderations"
  },
  "fraicheur_rapports": {
    "delivery": "2026-07-14T10:52:58Z",
    "commercial": "2026-07-14T11:34Z",
    "marketing": "2026-07-14 (première ronde)",
    "cs": "2026-07-14T11:34Z",
    "cos": "2026-07-14T11:16Z"
  }
}
```

---

# Brief quotidien — 2026-07-14 (second daily, 5/5 rapports)

*Comité complet pour la première fois : les 5 directeurs ont rapporté. Le brief du matin ne reposait que sur delivery.*

## 1. Santé globale — **100/100 · AMBRE · stable →**

Le score reste plafonné **ambre**. Il ne reflète en réalité que 40 % des pondérations.

> **Calcul** — Delivery 100 × 0,30 + Exécution (CoS) 100 × 0,10 = **40**.
> Commercial, CS et Marketing **ont rapporté ce jour**, mais leur `domain_score` est **non calculable** (inputs fondateurs manquants côté Sam : objectifs commerciaux, schéma comptes_clients, calendrier éditorial validé).
> Recalcul sur les poids disponibles : 40 / (0,30 + 0,10) = **100**.
> Statut **plafonné ambre** : 3 domaines sur 5 sans score exploitable [DH-CEO-003].

**Tendance :** stable. Le score était déjà à 100/ambre ce matin. Ce qui a changé, ce n'est pas le score mais la **couverture** : de 1/5 à 5/5 rapports. Le comité est désormais opérationnel ; il attend maintenant tes inputs pour que le score devienne un vrai reflet de santé.

## 2. Hier — par domaine

**Delivery** *(inchangé depuis le brief du matin, même fraîcheur 10:52 UTC)*
- Backend `/health` 200 « healthy ». 0 exécution RUNNING, 9 WAITING_BR_VALIDATION inchangées — tests internes confirmés par Sam, aucune relance client.
- Fin de 30 j d'inactivité : test *LogiFleet G3 (v2 corpus)* — **161** CANCELLED à 10 min (0 ERROR), **162** COMPLETED en 43 min 28, 8,86 $, dans la plage historique.
- 0 ERROR/WARNING mais fenêtre de logs de **1h28 seulement**, calée sur un redémarrage backend : ~15 h de silence log avant la ronde.

**Commercial** *(1ʳᵉ ronde)*
- Pipeline **vide** (0 lead), **aucun objectif hebdo** jamais fixé → `domain_score` non calculable.
- Source de leads concierge (table `leads`) **inaccessible** (permission denied, attendu — phase 2 non branchée). Aucun contournement.
- Schéma `pipeline_commercial` mis en conformité (structure only, **0 donnée touchée**) — signalé pour validation a posteriori (curseur agit_sous_validation).

**Marketing** *(1ʳᵉ ronde)*
- Séquence de lancement proposée : **13 contenus** datés 2026-07-21 → 2026-10-13 (About, post pivot, 11 portraits) — ordre = chronologie du pipeline, **hypothèse à valider**.
- **2 brouillons rédigés** (About, post pivot) opérationnalisant pour la première fois en public le positionnement tech × luxe / argument DEOS déjà acté.
- `domain_score` non calculable (calendrier vide à l'ouverture) ; aucune donnée de performance n'existe.

**Customer Success** *(1ʳᵉ ronde — mode dégradé assumé)*
- **0 compte client réel**, 0 canal de tickets. État **attendu** avant septembre 2026 (confirmé Sam 13/07), pas un incident — rendu visible pour ne pas être confondu avec une santé calculée.
- 4 identifiants techniques historiques, tous des tests. Seul user_id 2 actif <30 j (114 exéc./8 mois, 29 % FAILED) → donnée de calibration baseline, **pas** un signal de churn.
- Schéma comptes_clients + onboarding proposés (non écrits en base) → validation Sam.

**Exécution (CoS)** *(1ʳᵉ ronde — score 100 vert)*
- Décisions sans retard (âge max 0 j), 1 close avec preuve, 0 skill en file.
- Écart brief↔table corrigé dans la ronde : DA-01/02/03 non tracées → création de DEC-2026-0714-02/03/04 (attente_sam).
- **Surveillance cash inactive** et priorités de semaine absentes : signalé, aucune projection d'initiative.

## 3. KPIs

| Domaine | KPI | Valeur | Statut |
|---|---|---|---|
| Delivery | Backend up | 1/1 | 🟢 |
| Delivery | Exécutions bloquées techniquement | 0/9 | 🟢 |
| Delivery | Erreurs logs (fenêtre dispo) | 0 (fenêtre 1h28) | 🟢 |
| Commercial | Leads qualifiés | 0/0 (pipeline vide) | 🟠 |
| Commercial | Objectifs hebdo définis | 0 (absent) | 🟠 |
| Marketing | Contenus séquence produits | 2/13 (en attente validation) | 🟠 |
| Marketing | Contenus validés | 0/2 | 🟠 |
| CS | Comptes clients enregistrés | 0 (mode dégradé) | ⚪ info |
| CS | Incident delivery touchant un client | 0 | 🟢 |
| Exécution | Décisions en retard | 0/4 | 🟢 |
| Exécution | Surveillance cash | inactive | 🟠 |
| Gouvernance | Couverture comité | 5/5 rapports, 3/5 scores non calculables | 🟠 |

## 4. Priorités du jour

1. **Suivi de DEC-2026-0714-01** (interface web de suivi du comité), accordée par toi — confirmer qui exécute et le jalon attendu.
2. **Valider la séquence éditoriale + les 2 brouillons** (marketing) — seule production du comité avec échéance externe (fin oct. 2026) et livrables prêts ; rien ne se publie sans validation [DH-CMO-001].
3. **Fixer les objectifs hebdo commerciaux** — domaine le plus lourdement pondéré (0,25), le plus simple à débloquer ; première cause du plafond ambre.
4. **Fiabiliser l'export des logs backend** (fenêtre 24 h réelle) — DA-01 / DEC-02, à confier à l'équipe technique avant le lancement client.
5. **Trancher la cadence des rondes des 5 directeurs** (DEC-03, attente_sam) et décider d'activer surveillance cash + priorités de semaine.

## 5. Décisions attendues

1. **[MARKETING] DA-2026-0714-04** — Valider/corriger la séquence des 13 contenus + les 2 brouillons (About, post pivot) avant programmation [DH-CMO-001]. *Débloque la chaîne hebdo vers septembre ; seule échéance externe.*
2. **[COMMERCIAL] DA-2026-0714-05** — Fixer les objectifs hebdo commerciaux. *Rend le score commercial (poids 0,25) calculable ; lève la plus lourde part du plafond ambre.*
3. **[CS] DA-2026-0714-06** — Valider le schéma comptes_clients + parcours d'onboarding et fixer une date d'initialisation avant sept. 2026. *Formule de santé CS prête dès le premier compte réel.*
4. **[DELIVERY] DEC-2026-0714-02** — Fiabilisation de l'export de logs : décider qui exécute (correctif = équipe technique, prod en lecture seule pour le comité).
5. **[GOUVERNANCE] DEC-2026-0714-03** — Acter cadence/calendrier des rondes des 5 directeurs + décider d'activer surveillance cash et priorités de semaine.

*Aucune escalade ce jour : aucune décision >5 j, aucun conflit non arbitrable, aucune alerte haute touchant un client (0 client réel).*

## 6. Alertes

- 🟠 **Score plafonné ambre — 60 % des pondérations non calculables.** Commercial (0,25), CS (0,20), marketing (0,15) ont rapporté mais restent sans score faute d'inputs fondateurs (objectifs, schéma comptes, calendrier validé). Le 100 ne repose que sur delivery + exécution. La couverture a progressé (1/5→5/5) mais le score n'est pas encore un vrai reflet de santé.
- 🟠 **Surveillance cash inactive** — aucune donnée, aucun seuil déclaré. Le CoS ne produit aucune projection d'initiative ; l'angle mort financier reste visible.
- 🟠 **Source de leads concierge inaccessible** (permission denied, phase 2 non branchée) — aucune alimentation automatisée du pipeline avant branchement ; à planifier ou confirmer hors périmètre avant sept. 2026.
- 🔵 **Incohérence de comptage à réconcilier** — le KPI CoS déclare **4 décisions ouvertes** (DEC-02/03/04 créées ce jour) alors que la liste B2 n'en affiche que **2** (DEC-01 accordee, DEC-03 attente_sam). Probable décalage de snapshot ; présenté côte à côte, à vérifier au prochain passage. Rien n'est masqué.
- 🔵 **Fenêtre de logs 1h28** calée sur le dernier restart (~15 h de silence) — profondeur de vérif. réduite en cas d'incident antérieur au restart. Sans conséquence aujourd'hui (0 client).
- 🔵 **Schéma pipeline_commercial corrigé sans validation préalable** (curseur agit_sous_validation) — 0 donnée touchée, structure seule ; validation a posteriori demandée.
- 🔵 **Rôle de Lucas non documenté** — bloque le portrait rang 13 (échéance 2026-10-13). Pas d'urgence.

## 7. Opportunités

- **Bibliothèque de cas d'usage anonymisés** à partir des 76 projets internes pour équiper les futurs dossiers de démo — sous réserve stricte « cas de test interne, pas de référence client » et de la limite « pas de déploiement production » de l'offre.
- **Calibrer la baseline « usage » CS** sur 8 mois d'historique avant les premiers comptes réels, et activer le canal de tickets pour ne pas démarrer en mode dégradé.
- **Backlog PropositionEvolution tracé** (deos_state) pour fiabiliser le critère « évolutions P1 en retard » du score delivery — aujourd'hui supposé à 0 faute de traçabilité. Ouvert depuis le 13/07.

## 8. Ma recommandation

**Consacrer une courte session cette semaine à valider la séquence éditoriale de lancement (13 contenus) et les 2 brouillons prêts (About, post pivot) — puis, dans la foulée, fixer les objectifs hebdo commerciaux.**

Le comité est désormais complet (5/5 rapports), mais presque tout attend un input fondateur de ta part. Une seule production a à la fois une **échéance externe** et des **livrables concrets déjà rédigés** : la séquence marketing (elle court jusqu'à fin octobre 2026, en amont du lancement payant de septembre, et rien ne se publie sans ta validation [DH-CMO-001]). C'est le seul geste qui transforme aujourd'hui du travail préparé en résultat public et amorce une cadence hebdomadaire. Immédiatement derrière : les **objectifs commerciaux**, l'input le plus lourdement pondéré (0,25) et le plus simple à donner, qui à lui seul lève la plus grosse part du plafond ambre. Les autres chantiers (CS, logs, cadence des rondes) préparent septembre 2026 sans urgence propre — ils figurent dans les décisions attendues.

*Sources : rapport_marketing 2026-07-14 (2 BrouillonContenu prêts, séquence datée) ; rapport_commercial 2026-07-14 (objectifs_commerciaux absent, poids 0,25) ; B4 sante_ponderations.*
