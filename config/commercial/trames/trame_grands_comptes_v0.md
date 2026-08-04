# Trame de qualification et d'approche — segment grands comptes v0 (DRAFT, non envoyable)

Statut : brouillon de structure, produit par le Directeur Commercial le 2026-08-04,
suite aux instructions de packaging/tarification de Sam du 03/08 (briefs/arbitrages-sam-2026-08-03.md,
partie II.1-II.2). Aucun prix nouveau n'est introduit : le tableau de
/workspace/config/offre_dh.md reste la seule grille tarifaire en vigueur pour Free/Pro/Team/
Enterprise. Les deux modes décrits ci-dessous (conseil, supervision) n'ont PAS ENCORE de prix
canonique publié — ce document ne doit servir à aucune proposition chiffrée tant que
offre_dh.md n'a pas été mis à jour et commité en conséquence [DH-CRO-002].

## 1. Positionnement (ce qu'on vend, ce qu'on ne vend pas)
- On ne vend PAS du développement à un grand compte qui a déjà un intégrateur (Accenture,
  Capgemini, etc.) : on ne les remplace pas.
- On vend la maîtrise de l'amont : cahier des charges détaillé, produit en interne, en jours,
  avec la trace de chaque décision — avant que l'intégrateur ne chiffre.
- Argument Team : le prototypage jetable (variantes à quelques euros / deux heures, POC et A/B
  d'architecture) — le studio prototype et jette, l'intégrateur industrialise ce qui a gagné.
- Formule directrice (Sam, 03/08) : « vos partenaires livrent, la partition vous appartient. »

## 2. Qualification — critère supplémentaire spécifique grands comptes
Le scoring standard (skill dh-qualification-commerciale, /10) s'applique intégralement.
S'y ajoute, pour ce segment, un filtre d'entrée AVANT même de lancer le scoring :
- Cible = **une personne dans une BU** (PO CRM, responsable CRM métier), jamais l'entreprise
  en tant que telle.
- Qualification par un **signal daté** obligatoire : offre d'emploi Salesforce publiée, projet
  Agentforce annoncé, nouveau titulaire en poste. Sans signal daté, pas d'entrée pipeline
  [DH-CRO-003] — "une liste d'utilisateurs Salesforce n'est pas une cible" (Sam, 03/08).
- Corollaire prix : à 49€, l'achat Pro passe sous les seuils de procurement — ce qui rend le
  contact direct BU plausible sans validation comité d'achat pour ce tier précis.

## 3. Deux modes de vente (structure, sans prix)
### 3.1 Mode conseil
- Conseil, mise en place, transfert de compétences, support optionnel.
- Existe déjà (SH Conseil) : aucun développement engagé, marge haute, ressource consommée =
  agenda de Sam uniquement.
- Ne relève pas de l'offre produit canonique (Free/Pro/Team/Enterprise) : à documenter
  séparément si Sam souhaite le formaliser en collateral commercial.

### 3.2 Mode supervision à distance — à découper en deux
- **Observer et rendre compte** : agent en lecture seule sur l'org du client, compte rendu
  quotidien, alertes sur les dérives. Peu coûteux, pas d'engagement de service lourd,
  vendable rapidement.
- **Prendre le run** : accès production, engagement de service, astreinte, assurance —
  rouvre la frontière "Team s'arrête avant la production" fixée dans l'offre canonique.
  Relève de l'après-mise en production. **Contrat écrit obligatoire avant toute ligne de
  code** — statut : à cadrer avec le Juridique avant toute proposition, hors périmètre
  Commercial seul.

## 4. Ce qui manque avant usage réel de cette trame
- Prix : aucun chiffre publié pour le mode conseil ni pour les deux variantes de supervision.
  Ne pas escalader une remise ici — il ne s'agit pas d'une remise mais d'une offre non encore
  publiée [DH-CRO-002].
- Plafonds d'usage Team (II.3 du brief Sam) : "à fixer, en attente du coût réel d'un BUILD
  complet" — non disponible tant que la preuve BUILD→SANDBOX (checkpoint 15/08) n'existe pas.
- Prototypage jetable sur scratch org : vérification technique demandée par Sam (Jordan sait-il
  déployer sur scratch org depuis un Dev Hub client ?), à lancer par Delivery après le
  correctif phase 2 — argument commercial non utilisable tant que cette vérification n'a pas
  eu lieu.

## 5. Prochaines étapes
- Ce document reste un brouillon interne, structurel, non envoyable [DH-CRO-001].
- Ne pas l'utiliser en dossier de démo ou proposition tant que offre_dh.md n'inclut pas ce
  segment et que la vérification scratch org n'a pas eu de réponse.
