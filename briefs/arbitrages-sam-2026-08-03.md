# Arbitrages de Sam — comité du 3 août 2026

Réponses au document *Demandes, arguments, arbitrages*. Une entrée par référence, à router
et à tracer au registre. La partie II ajoute des instructions nouvelles qui ne figuraient pas
au comité.

---

# I. Réponses aux décisions en attente

## Bloc A

**A1 · DEC-2026-0716-04 — Portrait de Sophie → option (b), ACCORDÉE sous condition**
Publication au jalon de réouverture conforme, pas au calendrier. Le fond du texte reste à
valider par Sam le 04/08, ainsi que le choix éditorial du hook propre à la sous-série (repris
ou non sur les dix portraits suivants). Rien ne part avant ce retour.

**A2 · DEC-2026-0716-03 — Seuil d'alerte de trésorerie → 50 €**
Seuil fixé à 50 €, provisoire, ajustable d'un mot.
*Point à confirmer par Sam avant câblage :* la seconde règle énoncée (« si pas de décision à
20, alerte urgente ») est lue comme **20 jours sans réponse sur une décision → alerte
urgente**. Le CoS ne câble pas avant confirmation.

**A3 · DEC-2026-0716-02 — Lecture des leads du concierge → ACCORDÉE, périmètre réduit**
Autorisé. Champs exposés : **un résumé de la conversation et une analyse d'intention**. Pas
de verbatim. Inutile d'aller au-delà de ce que le RGPD exige.
*Réponse à la question de Sam :* les vues `v_deos_*` sont des vues en lecture seule sur la
base de production Digital·Humans, nommées d'après leur lecteur (le comité). Aucun
développement n'est engagé pour un produit DEOS. Nommage renommable si Sam le souhaite.

**A4 · DEC-2026-0802-03 — Travail incrémental du BUILD → ACCORDÉE**
Ordre validé : delta d'abord, reprise sur incident (DEC-2026-0802-02) ensuite.
*Priorité relevée :* ce chantier conditionne désormais la viabilité économique du Pro et du
Team (voir partie II). Ce n'est plus une optimisation, c'est un prérequis de tarification.

## Bloc B

**B1 · DEC-2026-0716-01 — Source de comptes cibles → ACCORDÉE, combinaison**
1. **Réseau de Sam** — Sam fournit l'extract. Le Commercial identifie les comptes
   intéressants. **Chaque cas est discuté avec Sam avant tout contact.** Aucune approche
   directe sans son accord nominatif.
2. **Rebrancher le workflow d'enrichissement + Playwright**, dans le respect strict de la
   légalité (pas de scraping massif, pas de contournement, sources publiques uniquement,
   conservation de l'URL et de la date pour chaque contact).
3. **SIRENE / data.gouv : écarté.**
4. **Ouverture UK/US à instruire** — ratio investissement/revenu jugé favorable, culture de
   l'abonnement plus installée. À croiser avec DEC-2026-0802-05 (mission juridique vente hors
   France).
*Préalable posé par Sam :* finalisation de la page LinkedIn et ouverture d'un compte
commercial, pour travailler l'audience (abonnés, signaux d'intérêt) en amont.

**B2 · DEC-2026-0803-01 — Correctif du bug phase 2 → VALIDÉE**
Correctif ciblé engagé. Instruction complète de Sam, plus large que la décision soumise :
analyser les logs, trouver la cause, corriger, **puis valider le pipeline complet en livrant
le projet CRM Digital·Humans en sandbox**, et **fournir un budget chiffré** pour que Sam
provisionne l'API si nécessaire. L'urgence ne justifie pas de faire n'importe quoi, mais le
budget nécessaire sera mis.

**B3 · DEC-2026-0802-07 — Les quatre actions de l'AI Act → VALIDÉES**
Les quatre sans réserve : pas de réouverture sans mention IA dans le widget, vérification de
l'absence d'accès résiduel, extension aux agents Pro et Team avant septembre, recoupement
EUR-Lex et validation par un avocat.

**B4 · Fiabilisation des logs → ACCORDÉE** (re-arbitrage de DEC-2026-0714-02, refusée le 14/07)
Le contexte a changé et le manque a eu un coût mesurable. Statut du registre à mettre à jour :
la décision de juillet n'est pas rouverte, une nouvelle est créée avec référence à la
précédente.

**B5 · Suivi des 8 chantiers du 31/08 → ACCORDÉE, version minimale**
Clé d'état mise à jour par Sam une fois par semaine. Pas de branchement sur l'API de
facturation.

## Bloc C — cinq missions

**Go global.** DEC-2026-0802-08 (Entracte version scène), DEC-2026-0802-01 (démo phare),
DEC-2026-0802-05 (juridique vente hors France), DEC-2026-0802-06 (juridique audit parcours et
RGPD), DEC-2026-0716-05 (cadrage du livre blanc). Séquencement du CEO conservé : Delivery
n'intervient sur l'Entracte qu'après le 15/08.

## Points de vigilance

- **Pause du site : confirmée et voulue.** Le retour en ligne doit être accéléré, mais
  seulement après correction de tous les manques — AI Act, RGPD, consentement.
- **Projet 107 en `BUILD_READY`** : la relance d'hier a échoué, d'où les 26 $ perdus. Ne pas
  relancer avant les correctifs, et vérifier avant de payer un cycle.
- **Fiches des 11 agents** : Sam les relit rapidement. Le Marketing attend son mot avant de
  généraliser la série.
- **Libellé `canal_tickets_v2`** : accepté sur le principe, mais **on attend le BUILD** — ce
  sont les agents qui configureront la solution pour qu'elle soit utilisable.

---

# II. Instructions nouvelles — packaging et tarification

Issues de la session de travail du 03/08. À intégrer au plan avant le 1er septembre.

## II.1 Angle commercial grands comptes

Ce qu'on vend à un grand compte n'est pas du développement — ils ont déjà Accenture ou
Capgemini, et ne veulent pas les remplacer. On vend **la maîtrise de l'amont** : le cahier des
charges détaillé produit en interne, en jours, avec la trace de chaque décision, avant
d'ouvrir le sujet avec l'intégrateur. L'intégrateur chiffre serré parce que le périmètre est
carré. Formule directrice : *vos partenaires livrent, la partition vous appartient.*

Second argument, propre au Team : **le prototypage jetable**. Quand une variante coûte
quelques euros et deux heures, on n'arbitre plus deux options sur des slides, on les regarde
tourner toutes les deux. POC, A/B d'architecture, protos successifs. Le studio prototype et
jette, l'intégrateur industrialise ce qui a gagné — ce qui fait de l'arrêt avant la production
une frontière de modèle, non une limite.

Corollaire : à 49 €, l'achat passe sous les seuils de procurement. La cible n'est pas
l'entreprise mais **une personne dans une BU** (PO CRM, responsable CRM métier), qualifiée par
un **signal daté** — offre d'emploi Salesforce publiée, projet Agentforce annoncé, nouveau
titulaire en poste. Une liste d'utilisateurs Salesforce n'est pas une cible.

## II.2 Deux modes de vente grands comptes

- **Mode conseil** — conseil, mise en place, transfert de compétences, support optionnel.
  Existe déjà (SH Conseil), aucun développement, marge haute. Seule ressource consommée :
  l'agenda de Sam.
- **Mode supervision à distance** — à découper en deux : **observer et rendre compte** (agent
  en lecture seule sur l'org du client, compte rendu quotidien, alertes sur les dérives), peu
  coûteux, sans engagement de service lourd, vendable rapidement ; et **prendre le run**
  (accès production, engagement de service, astreinte, assurance), qui rouvre la frontière
  fermée par le choix « Team s'arrête avant la production » et relève de l'après-MEP, avec
  contrat écrit avant toute ligne de code.

## II.3 Plafonds d'usage — à câbler avant le 1/09

| Tier | Plafond | Livrables |
|---|---|---|
| Gratuit | ~10 à 20 échanges/mois (borne réelle en jetons), un seul sujet, **pas de mémoire** | **aucun** |
| Pro 49 € | **3 SDS/mois**, mémoire, upload | SDS |
| Team 1 490 € | à fixer — **en attente du coût réel** d'un BUILD complet | pipeline jusqu'à sandbox |
| Enterprise | sur demande | — |

Au-delà du plafond : packs supplémentaires à l'unité.
Le compteur se déclenche en fin d'échange, jamais au milieu. Le message de passage est de la
copie de marque, à écrire par le Marketing avec le skill de transcréation : le besoin est
cadré ; le cahier des charges complet, la mémoire et les documents, c'est le Pro.
Garde-fou : vérification d'e-mail à l'inscription, sinon le gratuit se renouvelle à l'infini.

## II.4 Cible de coût unitaire du SDS : 10 € maximum

Référence mesurée : exécution #144, 6,49 $ pour 847 737 jetons (~5,60 €) — déjà sous la
cible. Le problème est la **variance**, pas la moyenne : rien ne borne aujourd'hui la
longueur des sorties.

Leviers, dans l'ordre :
1. **Borner la longueur de sortie de Marcus.** Il consomme ~56 % du coût d'un SDS.
2. **Mise en cache des invites** sur les orchestrateurs, qui répètent le contexte plateforme
   et RAG à chaque appel.
3. **Travail incrémental** (A4), qui évite de repayer une régénération complète pour trois
   lots rejetés.

**Arbitrage de Sam sur Marcus : on ne change rien — Marcus reste sur Opus.** Bascule sur
Sonnet envisagée uniquement si un test montre un niveau de qualité identique ou quasi. Test
demandé, protocole en II.6, restitution courte.

## II.5 Compteur d'usage et traçage des coûts — chantier bloquant

Le compteur existant **hallucine** : il estime au lieu de mesurer. À partir du 1/09 c'est lui
qui décide de ce qu'un client peut consommer et de ce qu'on lui facture en plus — il doit être
**déterministe**. Les jetons sont retournés par l'API à chaque appel : la seule opération
légitime est de les additionner en base. Toute évaluation par un modèle est à retirer.

Prérequis, prioritaire : **combler le trou de traçage des coûts sur 29 exécutions**
(déc. 2025 → fév. 2026). Tant qu'il subsiste, on fixe des prix sur des chiffres non
prouvables.

Le mécanisme est le même pour les trois tiers — mesurer, afficher le reste, bloquer
proprement, proposer le pack. À inscrire au plan avec **test bloquant** avant le 1/09.

## II.6 Test comparatif Marcus — Opus vs Sonnet (court)

Économie du test : les sorties Opus **existent déjà en base** (exécutions #144, #159, #160).
On ne rejoue que la variante Sonnet. Coût estimé : quelques euros.

- **Protocole** : rejouer 3 SDS déjà exécutés, tout identique, Marcus seul routé sur Sonnet 5.
- **Mesures automatiques** : jetons et coût de la section architecture, longueur de sortie,
  délai.
- **Qualité** : lecture en aveugle par Sam des deux sections architecture d'un même projet
  (versions non étiquetées), sur cinq critères — complétude du modèle de données,
  justification des choix standard vs custom, traitement de la sécurité, cohérence avec les
  cas d'usage d'Olivia, absence d'erreur factuelle Salesforce.
- **Restitution** : un tableau, une page maximum. Pas de rapport.
- **Réserve honnête** : une notation automatique de la qualité de design ne vaut rien ici. La
  lecture en aveugle de Sam est le seul juge crédible — vingt minutes.

## II.7 Prix HT et facturation

Prix affichés **hors taxes** (vente B2B), avec le TTC mentionné à côté : des indépendants
achèteront à titre personnel, et l'affichage TTC est requis vis-à-vis d'un consommateur. SIRET
et numéro de TVA intracommunautaire collectés et validés à la commande.

**Échéance réglementaire ajoutée au plan : 1er septembre 2026.** Obligation de réception des
factures électroniques pour toutes les entreprises assujetties à la TVA, sans distinction de
taille — donc pour Digital·Humans le jour même du lancement. Sanction en cas d'absence de
plateforme agréée : 500 € dès le 1/09, puis 1 000 € tous les trois mois. L'obligation
d'émission ne s'applique aux TPE, PME, micro et indépendants qu'au 1er septembre 2027. Action
portée par Sam avant fin août.

## II.8 Vérification à instruire — scratch orgs

L'argument « autant de variantes que d'hypothèses » suppose des orgs isolées et jetables,
c'est-à-dire des **scratch orgs**, pas des sandboxes (délais de rafraîchissement, non
multipliables à volonté). À vérifier : Jordan sait-il déployer sur scratch org depuis un Dev
Hub client ? Une heure de vérification sur l'org de dev. **À lancer après le correctif phase
2**, pour ne pas disperser le Delivery.

## II.9 Canaux — cadrage pour le Marketing

Écartés : Instagram, TikTok, Product Hunt — mauvaise audience, coût de contenu permanent.
Retenus, par ordre de rendement estimé :
1. **Consultants Salesforce indépendants et anciens collègues** — apport d'affaires ou marque
   blanche. Ils ont déjà l'accès et la confiance ; il leur manque la vitesse de cadrage.
2. **Écosystème Salesforce physique** — groupes Trailblazer FR, meetups admins/développeurs
   Paris, Salesforce Saturday. On y arrive en praticien, pas en vendeur.
3. **Salesforce Ben** — un article de fond sur la traçabilité et la confiance comme premier
   frein d'adoption. Un week-end d'écriture, audience exactement ciblée.
4. **LinkedIn** — socle de crédibilité, pas mégaphone. La série des 11 portraits est ce qui
   valide tout le reste quand quelqu'un vérifie qui on est.
