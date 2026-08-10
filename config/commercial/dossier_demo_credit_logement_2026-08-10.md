# DossierCommercial — Crédit Logement (démonstration DEOS, dernière semaine d'août)

```json
{
  "type": "DossierCommercial",
  "agent": "commercial",
  "date": "2026-08-10",
  "societe": "Crédit Logement",
  "contact": "DSI — connu personnellement de Sam (réseau SH Conseil)",
  "source": "DEC-2026-0806-14 (origine sam, 06/08/2026) — grand compte entrant, présentation au retour de congés du DSI, dernière semaine d'août",
  "tier_vise": "DEOS (hors offre canonique DH ; segment grands comptes, non tarifé)",
  "score_qualification": {
    "total": 9,
    "besoin": {"points": 3, "sur": 3, "motif": "établissement financier sous supervision ACPR/DORA + précédent sectoriel daté (TD Bank, crédit immobilier garanti, 21/05/2026) + gouvernance d'agents = besoin réel et récurrent, pas hypothétique"},
    "maturite_org": {"points": 2, "sur": 2, "motif": "grand établissement financier, DSI identifié et joignable, organisation dotée d'un contrôle interne existant"},
    "budget": {"points": 1, "sur": 2, "motif": "plausible pour un compte de cette taille (fourchette marché 50k-500k$/an chez les concurrents) mais non confirmé formellement — aucun budget voté connu à ce jour"},
    "sponsor": {"points": 2, "sur": 2, "motif": "DSI connu personnellement de Sam — relation directe, pas un contact froid"},
    "urgence": {"points": 1, "sur": 1, "motif": "date fixée (dernière semaine d'août), Sam part en congés juste après"}
  },
  "verdict": "démo (seuil >=7 largement atteint)",
  "decisions_sources": ["DEC-2026-0806-14", "DEC-2026-0805-01", "DEC-2026-0808-03", "DEC-2026-0808-07", "DEC-2026-0809-08", "DEC-2026-0809-09"],
  "ce_qu_on_vend_le_jour_J": "une démonstration du dispositif de gouvernance + un cadrage payant (8 000 €, 5 à 10 jours, facturé par SH Conseil) — PAS une licence, PAS un prix ferme",
  "montage": "SH Conseil porte la présentation et le cadrage (prestation de jours) ; bascule vers Digital·Humans seulement si un abonnement DEOS se vend ensuite — recommandation du CEO du 08/08, confirmée économiquement (étude du 08/08, §5.4)",
  "verification_produit": {
    "demontrable": ["curseur d'autonomie en base, par direction et par type de tâche (table curseurs, 36 lignes)", "garde-fou technique qui refuse et journalise en moins de 60s (hooks.log)", "registre des décisions horodaté, avec origine et statut", "brief quotidien consolidé"],
    "NON_demontrable": ["tableau de bord de gouvernance côté client (n'existe pas)", "journal d'audit exportable (n'existe pas comme livrable)", "installation dans le SI d'un tiers (jamais faite)", "toute référence client (nous en avons zéro)", "tout déploiement en production (DEC-2026-0808-07, règle absolue)", "tout mode supervision (retiré du périmètre)"],
    "regle": "DH-CRO-004 — rien de la colonne NON_demontrable n'est promis le jour J"
  },
  "prix_si_demande": {
    "regle": "DH-CRO-002 — aucun prix ferme, aucun chiffre validé par Sam à ce jour (DEC-2026-0809-02 toujours en attente)",
    "phrase_a_dire": "Un dispositif de ce type se situe entre 40 et 90 000 € par an selon le nombre de directions gouvernées. Pour référence, les plateformes américaines de gouvernance IA se négocient entre 100 et 500 000 $ par an. Le périmètre exact, c'est ce qu'un cadrage détermine.",
    "proposition_immediate": "cadrage payant à 8 000 € (SH Conseil), livrable = cartographie des décisions à déléguer + réglage des curseurs + périmètre chiffré"
  },
  "prochaine_action": "finaliser le support de démonstration (3 gestes ci-dessous) et le remettre à Sam avant son départ en congés",
  "echeance": "dernière semaine d'août 2026",
  "historique": [
    {"date": "2026-08-06", "evenement": "opportunité signalée par Sam, DEC-2026-0806-14 créée"},
    {"date": "2026-08-07", "evenement": "qualification formelle 9/10, escaladée à Sam"},
    {"date": "2026-08-08", "evenement": "étude de marché et de tarification DEOS livrée (deos_grands_comptes_2026-08-08.md)"},
    {"date": "2026-08-09", "evenement": "concurrent Naaia identifié et positionnement 'pas de la conformité' tranché par Sam"},
    {"date": "2026-08-10", "evenement": "dossier de démonstration consolidé (ce document) — engagement pris le 08/08 pour le 10/08, tenu"}
  ]
}
```

---

## Ce qu'il faut retenir

1. **C'est toujours la meilleure opportunité du portefeuille** (score 9/10) et rien n'a bougé
   depuis le 07/08 sur le fond : sponsor connu, date fixée, besoin sourcé.
2. **Le dossier de démonstration est prêt** — c'est l'engagement pris dans l'étude du 08/08,
   tenu aujourd'hui. Il ne manque qu'un support visuel (écrans du comité) que Sam pourra
   projeter lui-même.
3. **Le prix reste bloqué en attente de Sam** (DEC-2026-0809-02, posée le 09/08, toujours sans
   réponse) : la phrase de cadrage ci-dessus permet de tenir la réunion sans lui, mais elle
   n'a pas été formellement validée.
4. **Le déroulé ne repose pas sur le BUILD** : contrairement au dossier démo du moteur Team
   (bloqué par l'exécution 165, en échec depuis le 02/08), cette démonstration s'appuie sur le
   curseur d'autonomie et le registre des décisions — tous deux vérifiés en base ce jour et
   fonctionnels. Aucune dépendance technique non résolue sur ce dossier précis.

## Le déroulé en trois gestes (reprend l'étude du 08/08, §5.2)

1. **Le registre** — une décision, son origine, sa date, son statut, sa preuve de clôture.
2. **Le curseur** — la matrice à 36 lignes, à l'écran. On change un cran devant eux.
3. **Le refus** — on demande à une direction de faire ce que son curseur interdit. Le dispositif
   refuse, la ligne apparaît dans le journal, horodatée. **C'est le moment de la démonstration.**

**Accroche d'ouverture** : TD Bank a lancé le 21/05/2026 son premier modèle d'IA agentique sur
le crédit immobilier garanti — le métier exact de Crédit Logement, daté de moins de trois mois.
Puis la question : *quand vos agents commenceront à décider, qu'est-ce qui les arrête, et
qu'est-ce qui le prouve ?*

**Cadre réglementaire à invoquer** : DORA (traçabilité exhaustive, art. 8, supervision ACPR) —
pas l'AI Act (l'annexe III « haut risque » a été repoussée à décembre 2027, ne pas s'appuyer
dessus, voir escalade Juridique déjà ouverte le 08/08).

## Réponses aux objections prévisibles

| Objection | Réponse |
|---|---|
| « On a déjà une gouvernance interne » | Un outil de GRC ou de contrôle interne classique règle des process, pas le cran d'autonomie d'un agent avant l'appel d'outil. Montrer le refus journalisé plutôt que l'expliquer. |
| « Pourquoi pas IBM / Credo AI ? » | Ces plateformes gouvernent des modèles (inventaire, dérive, biais). DEOS gouverne des décisions et des délégations (qui a le droit de faire quoi, à quel cran). Cinq à dix fois moins cher, à périmètre de direction plutôt que de parc de modèles. |
| « Et Naaia, qui est français et fait de la gouvernance IA ? » | Naaia documente la conformité (registre, ISO 42001) — un référentiel pour l'auditeur. DEOS gouverne l'action en temps réel — il refuse et journalise avant l'incident. Deux outils différents, pas concurrents frontaux. |
| « Qui vous audite, vous ? » | Personne à ce jour — zéro référence client, zéro audit tiers, on ne le cache pas. C'est pour cela qu'on ne vend rien de fermé aujourd'hui, seulement une démonstration et un cadrage. |
| « Quel est le prix ? » | Fourchette de cadrage 40 à 90 k€/an selon le nombre de directions gouvernées (référence marché américain : 100 à 500 k$/an). Le chiffre exact vient d'un cadrage, proposé à 8 000 €. |

## Ce que je ne demande pas ici

Rien de nouveau : les deux demandes à Sam sur ce dossier (validation du prix, plafond de jours
DEOS) sont déjà posées en DEC-2026-0809-02 depuis le 09/08 et ne sont pas répétées.
