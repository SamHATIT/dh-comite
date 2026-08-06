# Liste de réouverture — site digital-humans.fr
> **Date :** 2026-08-06  
> **Directeur Juridique Digital·Humans**  
> **Statut :** Livrable opérationnel — chaque affirmation porte sa source officielle

---

## Cadre réglementaire applicable

**Texte :** Règlement (UE) 2024/1689 (AI Act), article 50 — Obligations de transparence.  
**Source officielle :** [EUR-Lex — Règlement 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)  
**Date d'application :** **2 août 2026** (aucune période de grâce).  
**Sanctions (art. 99(4)(g)) :** jusqu'à **15 000 000 EUR** ou **3 % du chiffre d'affaires mondial annuel**, le montant le plus élevé étant retenu.  
**Source :** [AI Act Service Desk — Article 99](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99)

**Lignes directrices :** [Guidelines on transparency obligations](https://digital-strategy.ec.europa.eu/en/policies/guidelines-transparency-ai-generated-content) (Commission européenne, mai 2026)  
**Code de pratique :** [Code of Practice on Transparency of AI-generated Content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) (juin 2026)

---

## 1. LISTE DE RÉOUVERTURE — Actions par ordre de priorité

### 1.1 BLOQUANT — Mention IA dans le widget Sophie

**Obligation :** Article 50(1) du règlement (UE) 2024/1689 :
> « Les fournisseurs veillent à ce que les systèmes d'IA destinés à interagir directement avec des personnes physiques soient conçus et développés de manière à ce que les personnes physiques concernées soient informées qu'elles interagissent avec un système d'IA, sauf si cela est évident du point de vue d'une personne physique normalement informée et raisonnablement attentive et avisée, compte tenu des circonstances et du contexte d'utilisation. »

**Interprétation des lignes directrices (mai 2026) :**
- L'obligation s'applique aux chatbots dès la première interaction
- Un nom humain (« Sophie ») n'est PAS un indicateur évident d'IA — au contraire, il peut induire en erreur
- L'information doit être « claire et distincte » et fournie « au plus tard au moment de la première interaction »
- Source : [FAQ Article 50](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)

**Verdict :** NON CONFORME — le widget Sophie ne comporte aucune mention visible indiquant une interaction avec une IA.

**Action requise :** Afficher une mention explicite AVANT ou DÈS le premier message. Voir section 2 pour le libellé exact.

**Statut :** BLOQUANT pour la réouverture.

---

### 1.2 BLOQUANT — Vérifier l'absence d'accès résiduel pendant l'entracte

**Contexte :** Le site affiche une page d'entracte depuis le 02/08. L'arbitrage du 03/08 (DEC-2026-0802-07) exigeait de « confirmer l'absence d'accès résiduel au widget pendant la pause ».

**Action requise :** Vérification technique que le widget Sophie n'est pas accessible via une route directe, un cache, ou un état de session antérieur.

**Responsable :** Delivery (vérification technique).

**Statut :** BLOQUANT — l'exposition d'un chatbot non conforme, même résiduelle, constitue une violation de l'article 50(1).

---

### 1.3 À TRAITER AVANT SEPTEMBRE — Agents Pro et Team

**Obligation :** Article 50(1) s'applique à tous les systèmes d'IA interagissant directement avec des personnes physiques. Les agents du tier Pro (Olivia, Elena, Marcus, Jordan, Lucas) et du tier Team sont des systèmes d'IA au sens du règlement.

**Verdict :** À VÉRIFIER — ces agents sont accessibles après inscription. L'information doit être fournie :
- Soit dans le parcours d'inscription (information générale sur la nature IA de l'équipe)
- Soit au premier message de chaque agent (mention individuelle)

**Action requise :** 
1. Décider du point d'information (inscription OU premier message de chaque agent)
2. Rédiger les mentions correspondantes
3. Implémenter avant le lancement payant du 1er septembre

**Statut :** NON BLOQUANT pour la réouverture du site (ces agents ne sont pas accessibles au public), BLOQUANT pour le lancement du tier Pro.

---

### 1.4 À DOCUMENTER — Contenus générés et exemption de contrôle éditorial

**Obligation :** Article 50(4), alinéa 2 du règlement :
> « Les déployeurs d'un système d'IA qui génère ou manipule du texte publié dans le but d'informer le public sur des questions d'intérêt public veillent à ce que le contenu généré ou manipulé artificiellement soit identifié. Cette obligation ne s'applique pas lorsque [...] le contenu généré par l'IA a fait l'objet d'un processus de révision humaine ou de contrôle éditorial et qu'une personne physique ou morale assume la responsabilité éditoriale de la publication du contenu. »

**Interprétation des lignes directrices :**
- « Révision humaine » = examen délibéré du fond du contenu par une ou plusieurs personnes possédant les connaissances et le jugement professionnel pertinents
- NE COMPTE PAS : corrections orthographiques/grammaticales, vérifications superficielles
- « Responsabilité éditoriale » = une personne assume la responsabilité juridique ultime de la publication
- Source : [FAQ Article 50](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)

**Position de Digital·Humans :**
- Les SDS (livrables du tier Pro) sont validés par le client avant usage — le client assume la responsabilité éditoriale
- Les contenus marketing (posts LinkedIn, articles de blog) font l'objet d'une validation par Sam Hatit avant publication — Sam assume la responsabilité éditoriale
- Le comité de direction interne n'est pas exposé au public — hors périmètre article 50(4)

**Verdict :** POTENTIELLEMENT CONFORME sous réserve de :
1. Documenter le processus de validation humaine (qui valide, quels critères, quelle traçabilité)
2. Identifier explicitement la personne assumant la responsabilité éditoriale
3. Faire valider cette position par un avocat

**Statut :** NON BLOQUANT pour la réouverture (le site n'expose pas de contenus générés non validés), À DOCUMENTER avant le lancement du tier Pro.

---

### 1.5 NON REQUIS POUR LA RÉOUVERTURE — Marquage machine (article 50(2))

**Obligation :** Article 50(2) — marquage des contenus synthétiques (audio, image, vidéo, texte) dans un format lisible par machine.

**Délai de transition :** Selon les FAQ officielles, les systèmes commercialisés avant le 2 août 2026 bénéficient d'un délai jusqu'au **2 décembre 2026** pour la détectabilité du contenu généré.

**Verdict :** Le site peut rouvrir sans marquage machine des contenus. L'obligation s'applique au 2 décembre 2026.

**Statut :** NON BLOQUANT pour la réouverture.

---

## 2. MENTION IA DU CONCIERGE SOPHIE — Texte exact

### Position et moment d'apparition

**Position :** DANS le widget de chat, visible AVANT que l'utilisateur ne puisse envoyer son premier message.

**Forme :** Texte statique affiché en haut du widget OU premier message système avant toute interaction utilisateur.

**Justification :** Les lignes directrices exigent une information « claire et distincte » « au plus tard au moment de la première interaction ». Une mention dans les CGU ou les mentions légales ne suffit PAS — elle doit être visible au point d'interaction.

### Libellé proposé

**Version française :**
```
Sophie est une assistante virtuelle alimentée par l'intelligence artificielle.
```

**Version anglaise :**
```
Sophie is a virtual assistant powered by artificial intelligence.
```

**Alternative plus directe (si espace réduit) :**
- FR : `Assistant IA`
- EN : `AI Assistant`

### Placement recommandé

**Option A (préférée) — Mention permanente :**
Afficher le libellé en permanence sous le nom « Sophie » dans l'en-tête du widget.

**Option B — Message système initial :**
Premier message affiché automatiquement dès l'ouverture du widget :
> « Bonjour, je suis Sophie, une assistante virtuelle alimentée par l'intelligence artificielle. Comment puis-je vous aider ? »

L'option A est préférable car elle reste visible pendant toute la conversation. L'option B est conforme mais l'information peut disparaître du champ visuel en scrollant.

---

## 3. PARCOURS D'ESSAI — Prérequis réglementaires

Le moteur Pro suppose une inscription autonome. Voici ce qui est requis avant qu'une personne puisse s'inscrire et essayer.

### 3.1 Information sur le traitement des données (RGPD)

**Base légale :** Article 13 du RGPD — information au moment de la collecte.

**Ce qui doit être affiché ou accessible au moment de l'inscription :**
- Identité du responsable de traitement (Digital·Humans / SH Conseil)
- Finalités du traitement (fourniture du service, mémoire conversationnelle, facturation)
- Base légale (exécution du contrat)
- Destinataires (fournisseur de modèle IA — à nommer)
- Durée de conservation
- Droits de la personne (accès, rectification, suppression, portabilité)
- Contact pour exercer ces droits

**Statut actuel :** À VÉRIFIER — la politique de confidentialité existe-t-elle ? Est-elle accessible depuis le formulaire d'inscription ?

### 3.2 Consentement explicite pour certains traitements

**Upload de documents :** Si le tier Pro permet l'upload de documents, un consentement explicite est requis pour le traitement de ces documents par un fournisseur tiers (transfert de données).

**Mémoire conversationnelle :** Si la mémoire persiste au-delà de la session, l'information doit le mentionner.

### 3.3 Mentions obligatoires du formulaire d'inscription

- Case à cocher « J'ai lu et j'accepte les CGV » (obligatoire, non pré-cochée)
- Case à cocher « J'ai lu la politique de confidentialité » (obligatoire, non pré-cochée)
- OU lien cliquable vers ces documents avec mention « En vous inscrivant, vous acceptez... »

### 3.4 Vérification d'e-mail

**Raison :** Éviter le renouvellement infini du tier gratuit. Mentionné explicitement par Sam dans les arbitrages du 03/08.

### Ce qui manque aujourd'hui (à vérifier)

| Élément | Statut | Action |
|---------|--------|--------|
| Politique de confidentialité en ligne | À VÉRIFIER | Vérifier l'URL |
| Lien vers la politique dans le formulaire | À VÉRIFIER | Intégrer si absent |
| CGV accessibles | À VÉRIFIER | Vérifier l'URL |
| Lien vers les CGV dans le formulaire | À VÉRIFIER | Intégrer si absent |
| Double opt-in e-mail | À VÉRIFIER | Implémenter si absent |
| Mention IA dans le parcours | MANQUANT | Ajouter |

**Note :** Le site est actuellement en pause totale (toutes routes → Entracte). Je n'ai pas pu vérifier l'état réel des pages légales ni du formulaire d'inscription.

---

## 4. ÉTAT DES DEUX MISSIONS DU 02/08

### 4.1 Mission DEC-2026-0802-06 — Audit de conformité du parcours RGPD

**Statut :** NON DÉMARRÉE.

**Raison :** Cette mission n'a jamais été invoquée. Je n'ai été créé que le 06/08, lors de cette session.

**Ce que je peux produire maintenant :** Une trame d'audit par étape (inscription, concierge, upload, traitement IA, Salesforce client, etc.) — mais elle reste théorique tant que je n'ai pas accès :
- Au contenu réel des pages de confidentialité/CGV (site en pause)
- Au schéma de données réel (quelles données sont collectées où)
- Aux contrats avec les sous-traitants (fournisseur de modèle IA)

**Blocage :** Site en pause → pages légales inaccessibles. Besoin des schémas de données et des contrats sous-traitants.

**Prochaine action :** Récupérer les brouillons des pages légales (mentions, CGV, confidentialité) et la liste des sous-traitants avec leurs DPA.

### 4.2 Mission DEC-2026-0802-05 — Vente hors France (cadrage juridique)

**Statut :** NON DÉMARRÉE.

**Raison :** Même cause — mission jamais invoquée.

**Ce que je peux produire :** Un cadrage préliminaire des questions à traiter (TVA, transferts de données, droit applicable, DPA client). Mais la recherche documentée sur les seuils de nexus économique par État américain, les clauses contractuelles types, et le cadre transatlantique exige du temps de recherche web que je peux engager.

**Prochaine action :** Si Sam le confirme, je peux produire un premier cadrage d'ici la prochaine ronde (lundi 10/08).

---

## 5. SYNTHÈSE — Ce qui bloque la réouverture

| Action | Bloquant ? | Responsable | Effort |
|--------|------------|-------------|--------|
| Mention IA dans le widget Sophie | **OUI** | Delivery (intégration) | ~1h dev |
| Vérifier l'absence d'accès résiduel | **OUI** | Delivery | ~30 min |
| Vérifier les pages légales accessibles | OUI | Delivery + Legal | ~2h |
| Agents Pro/Team — mention IA | Non (avant 01/09) | Delivery | ~2h dev |
| Marquage machine contenus | Non (avant 02/12) | — | — |

### Actions immédiates pour Sam

1. **Valider le libellé de la mention Sophie** (section 2)
2. **Instruire Delivery** pour l'intégration dans le widget
3. **Confirmer l'accès aux brouillons des pages légales** pour que je puisse les auditer

### Ce qui peut attendre

- Audit RGPD complet du parcours → dès que j'ai accès aux documents
- Cadrage vente hors France → prochaine ronde (lundi 10/08)
- Marquage machine → 2 décembre 2026

---

## 6. AVERTISSEMENT — Limites de ce livrable

Ce document prépare un travail de mise en conformité. Il ne constitue pas un conseil juridique.

**Recommandations :**
- Faire valider la mention Sophie et la position sur l'exemption de contrôle éditorial par un avocat avant mise en ligne
- Le DPA avec le fournisseur de modèle IA (chaîne de sous-traitance pour les données Salesforce client) doit être revu par un avocat
- Toute clause de responsabilité dans les CGV doit être validée par un avocat

---

## Sources officielles citées

- [Règlement (UE) 2024/1689 — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- [Article 50 — AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50)
- [Article 99 (sanctions) — AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99)
- [FAQ Article 50 — Commission européenne](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act)
- [Lignes directrices transparence — Commission européenne](https://digital-strategy.ec.europa.eu/en/policies/guidelines-transparency-ai-generated-content)
- [Code de pratique sur le marquage — Commission européenne](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)

---

*Rapport produit le 2026-08-06 par le Directeur Juridique Digital·Humans. Stocké via :*
```bash
echo '<json>' | /workspace/bin/deos-state set rapport_legal --par legal
```
