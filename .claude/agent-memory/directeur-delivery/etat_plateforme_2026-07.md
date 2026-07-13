---
name: etat-plateforme-2026-07
description: Contexte observé sur la nature du jeu de données prod (nombreux projets de test) et l'inactivité de juillet 2026, pour ne pas sur-interpréter le silence comme un incident
metadata:
  type: project
---

Ronde du 2026-07-13 (première ronde, MEMORY.md vide au départ) : constat via
`v_deos_executions` ($DEOS_RO_DSN) — aucune exécution n'a démarré depuis le
2026-06-13 (dernière : id 160, COMPLETED). Aucune exécution RUNNING/IN_PROGRESS
au 2026-07-13. 9 exécutions en WAITING_BR_VALIDATION, dont 5 en attente
> 7 jours (jusqu'à 152 jours pour l'id 140 depuis 2026-02-10).

Beaucoup d'entrées historiques portent des noms explicitement liés à des tests
("Agent Tester Sandbox", "TEST_FLOW_*", "test avec Emma", "Test PM+BA
Isolation", "sales cloud test pour pipeline") avec `duration_seconds`/`cost`
souvent à 0 — probablement un environnement mêlant vrais leads clients et
essais internes de la plateforme.

**Pourquoi c'est important** : ne pas confondre un mois d'inactivité
d'exécution avec une panne — le health check et les logs backend restent
normaux (cf. ronde 2026-07-13 : health healthy, RAG 91841 chunks OK, 1 seule
ligne ERROR sur 24h et sans lien avec une exécution). L'absence de nouvelles
exécutions est un signal commercial/pipeline (hors périmètre technique
delivery), pas un signal d'incident — à vérifier auprès de Sam/CSM plutôt que
traité comme une alerte delivery.

**Comment appliquer** : lors des prochaines rondes, comparer le nombre
d'exécutions démarrées dans les dernières 24h à ce repère (zéro depuis un
mois au 2026-07-13) pour distinguer une vraie reprise d'activité d'un bruit de
test. Voir aussi [[baselines-duree-phases]].

**Confirmé par Sam le 2026-07-13** : les 9 exécutions en WAITING_BR_VALIDATION
(85, 86, 120, 140, 149, 150, 151, 152, 158) sont TOUTES des projets de test
internes — il n'y a AUCUN client réel sur la plateforme avant le lancement
payant de la rentrée (septembre 2026). Ne plus proposer de « relance client »
sur ces exécutions ; les traiter comme jeu de données de test. Les alertes
d'attente BR sur ces ids ne sont pas des signaux business.
