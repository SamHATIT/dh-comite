# Trame de dossier de démonstration Digital·Humans — v0 (DRAFT, non envoyable)

Statut : brouillon de structure, jalon régime A pré-lancement (échéance 2026-08-15).
Produit par le Directeur Commercial le 2026-08-03.

## 1. Ouverture — le problème type
- Point de douleur générique (pas de client nommé) illustré par 1 fiche de la
  bibliothèque de cas d'usage anonymisés.

## 2. Démonstration du parcours
- Palier Pro (SDS) : peut être illustré dès aujourd'hui avec preuve réelle
  (11 fiches disponibles au 2026-08-03, cf. bibliothèque cas_usage, toutes
  arrêtées à sds_complete, conformes à l'offre Pro).
- Palier Team (BUILD → SANDBOX) : NE PEUT PAS être illustré avec une preuve
  d'exécution réelle bout-en-bout en l'état [DH-CRO-004]. Motif corrigé le 03/08
  (source : /workspace/config/delivery/session_build_2026-08-02.md ; rapport_delivery
  2026-08-03) — CE N'EST PAS une panne systémique : les 3 échecs historiques
  (exécutions 131, 147, 165-phase1) avaient 3 causes distinctes désormais
  documentées et corrigées, et la phase 1 de l'exécution 165 a obtenu un PASS de
  la revue qualité Elena le 02/08 (chaîne validée jusqu'à cette étape, arrêt
  ensuite volontaire pour maîtrise des coûts, pas un échec technique). L'obstacle
  ACTUEL est distinct : un nouveau bug bloquant en phase 2 (business_logic,
  apparu le 02/08T17:55:43Z, "'NoneType' object has no attribute 'lower'"),
  décision de correctif en attente côté Delivery — c'est la première fois que
  cette phase est atteinte dans l'historique de la plateforme. Motif de blocage
  de cette section : « pas encore de preuve d'exécution BUILD→SANDBOX de bout en
  bout », pas « échec/panne systémique ». Blocage à lever avant de finaliser
  cette section ; utiliser en attendant une description de périmètre sans preuve
  d'exécution, explicitement présentée comme telle.
- Démo phare "boucle fermée Agentforce → DH → sandbox" (DEC-2026-0802-01, concept
  validé par Sam) : prérequis bloquant identique — preuve BUILD attendue après le
  checkpoint du 15/08. Ne pas anticiper cette section avant que Delivery ait produit
  la preuve.

## 3. Preuve technique consolidée
- Renvoi vers la bibliothèque de cas d'usage (11/15 au 2026-08-03), avec disclaimer
  systématique "projet de test interne, aucun client réel avant septembre 2026".

## 4. Ce que Digital·Humans NE fait PAS (à énoncer explicitement, anti-survente)
- Pas de déploiement production en Team (choix de sécurité, offre canonique).
- Pas de mémoire/upload en Free.
- Aucun engagement de délai ferme tant que le succès BUILD n'est pas démontré.

## 5. Prochaines étapes
- Ce dossier reste un brouillon interne ; aucune diffusion externe sans validation
  Sam [DH-CRO-001].
