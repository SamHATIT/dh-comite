# Page de suivi — Chief of Staff Digital·Humans

Ronde du **2026-08-17** (lundi), complétée en fin de journée par la **clôture du comité hebdo présidé par le CEO**. Dernière ronde CoS persistée avant celle-ci : **2026-08-14** (le CoS ne tourne pas le week-end, DOW>5 — cf. `bin/rondes.sh`).

**Contexte d'infrastructure du jour, vérifié en direct** : au démarrage de cette ronde (07:00-07:05 UTC), la ronde automatisée `rondes.sh` du jour tournait en parallèle en arrière-plan (`ps aux`) ; les fichiers `rondes/*-2026-08-17.json` de Delivery, Commercial, CS, Marketing, Legal et Chief-of-Staff étaient encore à 0 octet au moment de mon audit, et le Financier a échoué avec une erreur d'infrastructure explicite (« modèle `gemma` inexistant ou inaccessible dans cet environnement »). Cette ronde manuelle constitue donc la restitution de référence du jour.

**Clôture du comité hebdo (fin de journée)** : le CEO a routé DEC-2026-0817-06 vers le CoS avec quatre écritures de statut à effectuer, preuves déjà disponibles. Exécutées et vérifiées ci-dessous (§1.1bis). Les priorités finales de la semaine (§3) remplacent la version du matin.

---

## 0. Score d'exécution — méthode et résultat

Formule du skill appliquée à la lettre, sur la totalité du stock `accordee`/`en_execution`, proxy `updated_at` pour l'« activité » (limite méthodologique assumée : `updated_at` capte toute écriture, y compris une reclassification du CoS, pas nécessairement un travail réel du porteur — voir réserve du 11/08 sur l'auto-mesure du registre).

| Bracket | Définition | Compte (matin) | Compte (après clôture comité) |
|---|---|---|---|
| En retard | accordée/en_execution, aucune écriture depuis 4 à 7 jours | 23 | à recompter à la prochaine ronde (plusieurs statuts viennent de bouger) |
| En risque d'oubli | idem, > 7 jours | 11 | idem |
| Skills proposés non traités > 14j | — | 0 | 0 |
| Priorité de semaine sans activité à mi-semaine | — | 0 | 0 |

**Score du matin : 100 − 184 − 165 = −249 → plancher 0/100 (rouge).** Le score détaillé par bracket n'est pas recalculé ce soir (les quatre écritures de clôture comité ne changent pas la répartition en_retard/en_risque, seulement le total accordee+en_execution) ; il reste **0/100** — le plancher persiste, le stock n'a pas été résorbé par ces quatre écritures ponctuelles.

### 0bis. Dette d'exécution (accordée + en_execution) — évolution

- **Avant cette ronde du matin** (07:02 UTC) : 45 (39 accordée + 6 en_execution), 9 attente_sam, 86 clos, 4 refusée — total 144.
- **Après la ronde du matin** (07:15 UTC) : 46 (40 accordée + 6 en_execution), 7 attente_sam, 89 clos, 4 refusée — total 146.
- **Après clôture du comité hebdo (ce soir, recompté en base)** : **45** (37 accordée + 8 en_execution), **10** attente_sam, **91** clos, 4 refusée — total 148.
- **Delta net dette depuis ce matin : −1.** Composition : DEC-2026-0813-04 et DEC-2026-0813-05 passent accordée→en_execution (mouvement interne, dette inchangée) ; DEC-2026-0802-05 sort de la dette en clôturant (−1) avec preuve vérifiée sur disque (23185 octets, `config/legal/cadrage_international_2026-08-12.md`) ; DEC-2026-0804-01 reste accordée (annotation de rattachement, pas de changement de statut). Le CEO a par ailleurs ouvert deux décisions en comité (DEC-2026-0817-04 legal, DEC-2026-0817-05 arbitrage BUILD) qui restent `attente_sam`/`en_attente d'exécution effective` et n'entrent donc pas dans la dette. DEC-2026-0817-06 (le routage lui-même) est clos avec preuve : les quatre écritures qu'il demandait ont été faites.

### Les trois décisions ouvertes les plus anciennes (âge calendaire depuis création)

| id | âge | encore pertinente ? | bloquée par | porteur |
|---|---|---|---|---|
| DEC-2026-0802-01 | 14j | Oui, mais dépendante d'un prérequis BUILD non tenu (checkpoint 15/08 raté deux fois) | Concept déposé (04/08) mais production jamais engagée ; en attente de validation d'orientation par Sam | delivery / sam |
| DEC-2026-0802-02 | 14j | Oui, et de plus en plus urgente : exec165/166 illustrent exactement le symptôme (BUILD relance depuis la phase 1, pas de reprise incrémentale) | Jamais écrit en code — 0 commit — 5e cycle de relance sans effet ; **le CEO a donné un GO périmètre étroit ce soir (DEC-2026-0817-05, échéance 19/08)** | delivery |
| DEC-2026-0802-03 | 14j | Oui, même constat que ci-dessus (mécanisme delta jamais implémenté) | Jamais écrit en code — 0 commit — 5e cycle de relance sans effet | delivery |

**Constat sur ces trois** : DEC-2026-0802-02 vient de recevoir un GO explicite du CEO ce soir (rang 3 des priorités, §3) — à vérifier lors de la prochaine ronde qu'un commit apparaît sous 48h (échéance 19/08). Les deux autres restent des correctifs d'architecture BUILD jamais commencés en code après 14 jours et 5 cycles de relance, sans arbitrage nouveau ce jour.

---

## 1. Décisions

### 1.1 Accordées / en exécution (dette, triées par âge calendaire décroissant)

| id | quoi | origine | statut | âge | preuve | prochaine action |
|---|---|---|---|---|---|---|
| DEC-2026-0802-01 | Démo phare Agentforce→DH→sandbox | sam | accordee | 14j | non | Attend prérequis BUILD ; statut à demander à Delivery |
| DEC-2026-0802-03 | BUILD travail incrémental (delta, pas 12 lots complets) | sam | accordee | 14j | non | 5e relance sans effet — statut CEO à Delivery |
| DEC-2026-0802-04 | Rationalisation outillage — tout sur Salesforce | sam | accordee | 14j | oui | Migration Email-to-Case jamais commencée — 4e cycle |
| DEC-2026-0802-06 | Mission juridique — audit conformité parcours complet | sam | accordee | 14j | non | Audit Legal attendu |
| DEC-2026-0802-07 | AI Act art.50 — obligations transparence Sophie | sam | en_execution | 14j | non | mentions_ia.md non retouché depuis le 06/08 (11j) — 3e+ cycle, en risque d'oubli confirmé ; **suite ouverte ce soir en attente_sam : DEC-2026-0817-03** |
| DEC-2026-0803-03 | Portraits — traitement visuel (concept livré, prod non engagée) | sam | en_execution | 13j | oui | Attente validation d'orientation Sam |
| DEC-2026-0803-04 | Page LinkedIn — retravail (2/3 livré) | sam | en_execution | 13j | oui | Attente validation Sam + dépend de 0803-03/05 |
| DEC-2026-0803-05 | Identité visuelle directeurs | sam | en_execution | 13j | oui | Attente arbitrage illustré vs photoréaliste |
| DEC-2026-0804-01 | Fiabilisation export logs backend | sam | accordee | 13j | non | **Annoté ce soir (DEC-2026-0817-06)** : le correctif de journalisation uvicorn (commit c3e534c) se rattache ici, et non à DEC-2026-0811-01 (erreur de traçabilité corrigée) |
| DEC-2026-0804-02 | Suivi 8 chantiers O2 | sam | accordee | 13j | non | MAJ hebdo par Sam lui-même (modalité fixée) |
| DEC-2026-0804-05 | Mission collective — interface web globale | sam | accordee | 12j | non | Statut du DSI / planning consolidé à vérifier |
| DEC-2026-0805-01 | Offre canonique — grands comptes + plafonds Bloc II | sam | accordee | 12j | oui | En risque d'oubli (8j sans activité) |
| DEC-2026-0806-08 | Audit sécurité des accès | sam | accordee | 10j | oui | GO donné 10/08 — statut à demander à Delivery |
| DEC-2026-0806-09 | Offre intégrateur à concevoir | sam | accordee | 10j | oui | Commercial pilote — pas encore de production client de référence |
| DEC-2026-0806-12 | Chemin critique — réouverture du site | sam | en_execution | 10j | oui | Regroupé dans la session technique unique de Sam, rang 1 des priorités (§3) |
| DEC-2026-0806-14 | Opportunité DEOS — Crédit Logement DSI | sam | accordee | 10j | oui | Sam pilote personnellement, présentation dernière semaine d'août |
| DEC-2026-0808-01 | Audit des 2 sites jamais audités | sam | accordee | 8j | non | Audit Legal attendu |
| DEC-2026-0808-08 | Angle mort de relecture (Elena / XML) | sam | accordee | 8j | non | Extension à tout ce qui part chez le client — statut Delivery |
| DEC-2026-0808-10 | Clé de sauvegarde à mettre à l'abri | sam | accordee | 6j | oui | Solution immédiate proposée, à confirmer faite |
| DEC-2026-0809-01 | Réouverture du site — GO conditionnel partiel | ceo | accordee | 7j | oui | Regroupé rang 1 des priorités (§3) |
| DEC-2026-0809-04 | Hygiène du dispositif — 2 corrections à 0€ | ceo | accordee | 7j | oui | Fiche de surveillance CoS pas encore amendée |
| DEC-2026-0809-05 | Routage CEO → Delivery, sécurité données (B2/B3) | ceo | accordee | 7j | oui | B2 clos 16/08 ; B3 = DEC-2026-0812-01, encore ouvert, rang 2 des priorités |
| DEC-2026-0809-07 | GPU et souveraineté | sam | accordee | 6j | oui | Suivi Hostinger RTX 6000 en Europe |
| DEC-2026-0809-08 | Concurrent identifié — Naaia | sam | accordee | 6j | oui | Veille concurrentielle, pas d'action bloquante |
| DEC-2026-0809-10 | Carte bancaire à l'inscription, y compris gratuit | sam | accordee | 6j | oui | À intégrer au parcours d'inscription (dépend réouverture) |
| DEC-2026-0810-02 | Créer un compte d'organisation Digital-Humans | sam | accordee | 6j | oui | Tâche pour Sam |
| DEC-2026-0810-05 | Discipline du comité hebdo — économie 35-45 USD/mois | ceo | accordee | 6j | non | Preuve de clôture attendue : coût du 17/08 < coût du 10/08 |
| DEC-2026-0810-08 | Support visuel Crédit Logement | ceo | accordee | 6j | non | Complétée selon priorites_semaine du 10/08 |
| DEC-2026-0810-11 | Déploiement entièrement local chez le client | sam | accordee | 6j | oui | Démonstration en cours, matière pour Crédit Logement |
| DEC-2026-0810-22 | Notification des décisions en attente | sam | accordee | 6j | oui | Pas de canal de notification créé |
| DEC-2026-0810-23 | Tableau de bord périmé après exécution manuelle | sam | accordee | 6j | oui | Cause identifiée, correctif à vérifier |
| DEC-2026-0810-30 | Intégrer démo locale au support Crédit Logement | ceo | en_execution | 6j | oui | Cf. 0810-08 |
| DEC-2026-0811-01 | Écart traçabilité — uvicorn.access WARNING→INFO | cos | accordee | 6j | oui | Arbitrage Sam demandé depuis le 05/08, jamais rendu ; **le commit c3e534c ne s'y rattache plus (voir 0804-01)** |
| DEC-2026-0811-02 | Garde-fou du comité — 2 faux négatifs | ceo | accordee | 5j | oui | GO de correction attendu de Sam ; conditionne rang 2 des priorités (§3) |
| DEC-2026-0811-04 | Préciser ce que chaque axe du curseur tient | ceo | accordee | 5j | oui | Dépend de la réponse à 0811-02 |
| DEC-2026-0811-05 | Supervision N8N hors service | delivery | accordee | 5j | oui | Bloquée par infra conteneur (port injoignable), pas par Delivery |
| DEC-2026-0811-10 | Récupérer documents Trust Center Hostinger | sam | accordee | 5j | oui | Butoir 22/08 — tâche exclusive à Sam |
| DEC-2026-0812-01 | Chiffrage B3 — cloisonnement RAG | delivery | accordee | 5j | oui | Rang 2 des priorités (§3) — GO du 13/08, 4 jours d'inexécution |
| DEC-2026-0813-02 | Rétention conversations Sophie — écart 90j/12 mois | legal | accordee | 4j | oui | Legal a tranché ce soir (DEC-2026-0817-04) — Delivery doit implémenter |
| DEC-2026-0813-03 | Pages légales absentes sur les 3 sites | cos | accordee | 4j | non | Bloquée par la bascule du site (0813-06), regroupé rang 1 |
| DEC-2026-0813-04 | Architecture LLM — proposition conjointe Financier+Delivery | financier | **en_execution** | 3j | **oui** | **Passé en_execution ce soir (DEC-2026-0817-06)** — preuve : chiffrages livrés le 14/08 par le Financier, `rondes/directeur-financier-2026-08-14.json` |
| DEC-2026-0813-05 | Complément — forfait MiniMax à chiffrer en scénario complet | financier | **en_execution** | 3j | **oui** | **Passé en_execution ce soir (DEC-2026-0817-06)** — même preuve que 0813-04 |
| DEC-2026-0814-02 | Pipeline publication Marketing — clé Ghost manquante | marketing | accordee | 2j | oui | Regroupé rang 1 des priorités (dépôt clé Ghost par Sam) |
| DEC-2026-0815-02 | 3 compteurs faux à l'écran d'exécution | delivery | accordee | 1j | non | Sous curseur correctifs de Delivery |

**Sortie de la dette ce soir** : DEC-2026-0802-05 (mission juridique vente hors France) — **clos** avec preuve `config/legal/cadrage_international_2026-08-12.md` (23185 octets, vérifiés sur disque).

### 1.1bis Les quatre écritures du routage CEO (DEC-2026-0817-06) — exécutées et vérifiées

| id | avant | après | preuve citée |
|---|---|---|---|
| DEC-2026-0813-04 | accordee | en_execution | `rondes/directeur-financier-2026-08-14.json` (11996 octets, 14/08) |
| DEC-2026-0813-05 | accordee | en_execution | idem |
| DEC-2026-0802-05 | accordee | **clos** | `config/legal/cadrage_international_2026-08-12.md` (23185 octets, 12/08) |
| DEC-2026-0804-01 | accordee (inchangé) | accordee, `porte_sur` annoté | rattachement du commit c3e534c corrigé (était erronément associé à DEC-2026-0811-01) |

Vérifié par `psql` après écriture : `SELECT id, statut, porte_sur FROM decisions WHERE id IN (...)` — les quatre lignes reflètent l'état ci-dessus. DEC-2026-0817-06 lui-même est **clos** par le CoS ce soir, preuve = l'exécution des quatre écritures listées.

### 1.2 Attente_sam (questions réellement ouvertes pour Sam / le comité) — 10 au total

| id | quoi | âge | note |
|---|---|---|---|
| DEC-2026-0813-06 | Site vitrine jamais basculé — qui a la main sur le geste hébergeur ? | 4j | Regroupé dans la session technique unique de Sam, rang 1 des priorités |
| DEC-2026-0813-07 | Chat multi-agents au niveau du tableau de bord | 4j | Préalable de cloisonnement (0812-01) recommandé avant tout développement |
| DEC-2026-0813-09 | Validation conjointe Legal+Delivery — cloisonnement RAG | 4j | Legal a produit sa moitié le 14/08 ; Delivery reste à faire (rang 2 des priorités) |
| DEC-2026-0813-10 | DEOS ne peut imposer de fournisseur de modèle | 4j | Principe déjà tranché par Sam (sortir du harnais) ; chiffrage encore attendu, lié à 0816-01 |
| DEC-2026-0816-01 | vLLM expose une entrée Anthropic native — le chantier lourd de 0813-10 pourrait s'annuler | 1j | À trancher par Sam avant le 20/08 (rang 5 des priorités) |
| DEC-2026-0817-01 | Escalade 3e occurrence — push SSH repo-delivery bloqué | 0j | Ouverte hier par le CoS ; regroupée dans la session technique unique, rang 1 |
| DEC-2026-0817-02 | Pricing.tsx affiche Pro à 49€ avec BUILD inclus, contraire à l'offre canonique (79€, sans BUILD) | 0j | Ouverte hier par le CoS ; regroupée rang 1 |
| DEC-2026-0817-03 | AI Act art.50 — implémentation code de la mention IA non tracée | 0j | **Ouverte ce soir par Legal** ; regroupée rang 1 des priorités |
| DEC-2026-0817-04 | Suite DEC-2026-0813-02 — Legal tranche la durée, Delivery doit implémenter | 0j | **Ouverte ce soir par Legal** |
| DEC-2026-0817-05 | Arbitrage CEO comité 17/08 — GO périmètre étroit sur DEC-2026-0802-02 (BUILD phase 1) | 0j | **GO donné ce soir par le CEO**, échéance 19/08 — rang 3 des priorités |

### 1.3 Clôtures ce soir (comité hebdo)

| id | motif |
|---|---|
| DEC-2026-0802-05 | Cadrage juridique international livré et vérifié sur disque (23185 octets, 12/08) |
| DEC-2026-0817-06 | Routage CEO exécuté intégralement (les 4 écritures ci-dessus) — clos par le CoS avec preuve |

---

## 2. Skills proposés

`.claude/skills-proposed/` est **vide** (vérifié par `find`, 2026-08-17). Aucun skill en attente de traitement.

---

## 3. Priorités de la semaine / OKR — VERSION FINALE, clôture comité hebdo du 17/08

Remplace la version du 17/08 matin (mêmes rangs 1-3 consolidés, ajout du rang BUILD et du rang Commercial décidés en comité). Détail complet stocké dans `deos_state.priorites_semaine` (clé `cos`), relu et vérifié après écriture (`deos-state get priorites_semaine --par cos`).

| Rang | Titre | Responsable | Décisions | OKR |
|---|---|---|---|---|
| 1 | Session technique unique de Sam (~2h) regroupant TOUS les gestes hôte : bascule site + correction Pricing.tsx, mentions IA, clé API Ghost, deploy key SSH + récupération commits 62674ed/c3e534c/7af590b, correction `model: gemma` de directeur-financier.md, redémarrage backend | sam | 0813-06, 0806-12, 0817-02, 0817-03, 0814-02, 0817-01 | O2/O3/O4 |
| 2 | Cloisonnement RAG — Sam débloque (routage garde-fou 0811-02 corrigé ou dérogation tracée), Delivery applique et livre sa moitié de la validation conjointe | sam (déblocage), directeur-delivery (application) | 0812-01, 0811-02, 0813-09 | O4 |
| 3 | BUILD phase 1 — correctif de journalisation sous 48h, GO CEO donné en comité ce soir, échéance 19/08, moyens demandés à Sam (migration schéma build_phase_executions + vue RO v_deos_llm_interactions) | directeur-delivery | 0817-05 | O2 |
| 4 | Production commerciale — clients finaux des 5 offres ESN APEC, recherche de signaux ICP, 4 fiches de cas d'usage manquantes (jalon 15/15 au 31/08) | directeur-commercial | — | O1 (5 comptes cibles/semaine — 0/5 la semaine passée) |
| 5 | Fournisseur de modèle — Sam tranche DEC-2026-0816-01 (piste vLLM) avant le 20/08 (arrivée DGX Spark), puis Delivery teste l'appel d'outils réel | sam puis directeur-delivery | 0816-01 | O5 + coûts (poste comité ~196 USD/mois) |

---

## 4. Cash

**Dernière donnée déclarée par Sam le 2026-08-13** (`maj_par=sam`), non rafraîchie depuis **4 jours** :
- Budget mensuel : 500 EUR (CFO externe), crédité le 1er de chaque mois.
- Consommé au 13/08 : 253,38 USD (Anthropic, relevé exact) + 10 USD GPU consommé = 263,38 USD ≈ 242 EUR.
- Solde déclaré (13/08) : 258 EUR.
- Projection (13/08, par Sam) : ≈ 350 USD toutes sources si la tendance tient — **je ne recalcule pas cette projection, je la cite telle que déclarée**, conformément à DH-COS-003.
- Aucun seuil fixé par Sam n'est signalé franchi.

**Signal de vigilance, pas une alarme** : cette clé n'a pas été rafraîchie depuis 4 jours. Ce n'est pas une surveillance inactive au sens strict (Sam l'a lui-même alimentée avec un cycle mensuel, pas quotidien), mais je le signale pour que l'écart entre fraîcheur affichée et fraîcheur réelle soit visible.

---

## 5. Relances émises ce jour

| id | âge | motif | porteur | cycle |
|---|---|---|---|---|
| DEC-2026-0802-02 | 14j | Reprise sur incident BUILD jamais écrite en code | delivery | 5e — **GO périmètre étroit donné ce soir par le CEO (0817-05), échéance 19/08** |
| DEC-2026-0802-03 | 14j | Mécanisme delta BUILD jamais écrit | delivery | 5e (recommandation : demande de statut nominative par le CEO) |
| DEC-2026-0802-04 | 14j | Migration Email-to-Case Salesforce jamais commencée | delivery | 4e |
| DEC-2026-0802-07 | 14j | AI Act art.50 — mentions_ia.md non retouché depuis 11 jours | legal | 3e+ — passe en risque d'oubli confirmé ; suite ouverte ce soir (0817-03) |
| DEC-2026-0817-01 | — | Push SSH bloqué 3 jours consécutifs (15,16,17/08) sans effet | sam (accès conteneur) | Escaladé directement (règle des 3 occurrences), regroupé rang 1 |

---

*Généré par le Chief of Staff, ronde du 2026-08-17 (matin) complétée par la clôture du comité hebdo (soir). Sources citées dans le corps ci-dessus, dans le RapportDirecteur JSON stocké via `deos-state set rapport_cos --par cos`, et dans `deos_state.priorites_semaine` (clé `cos`).*
