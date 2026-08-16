J'ai lu les sources directement : la matière transmise était de nouveau vide. Voici l'analyse.

---

# Boucle d'évolution des skills — semaine du 09/08 au 16/08/2026

## Avertissement — deux constats préalables qui conditionnent la lecture

**1. La matière fournie était vide pour les 33 rondes de la semaine**, exactement comme le 09/08. La cause est identique et vérifiée : `bin/evolution.sh` ligne 46 cherche toujours les clés `faits`, `alertes`, `escalades`, `donnees_manquantes`, `besoin_interface` **à la racine** du JSON, alors qu'un fichier `rondes/*.json` est une enveloppe Claude Code où ces clés vivent en texte libre dans `.result`. Le correctif d'une ligne signalé le 09/08 n'a pas été appliqué. J'ai donc relu moi-même les 33 rondes via `jq -r '.result'`, les décisions, `hooks.log` et les 24 skills.

**2. Aucune des cinq propositions du 09/08 n'a été appliquée.** Vérifié : aucun répertoire de `.claude/skills/` n'a été modifié depuis le 09/08 (`dh-supervision-delivery` date du 13/07, les quatre autres skills de ronde du 14/07) ; `dh-methode-de-preuve` n'existe pas ; `.claude/skills-proposed/` est toujours vide.

Cela change ce que je remonte. Deux des familles de friction ci-dessous sont des **récidives** : je ne les réécris pas à l'identique, je donne leur compteur réactualisé et j'amende le texte proposé quand la semaine a produit un symptôme nouveau. Sam a déjà cinq propositions sur son bureau ; je n'en ajoute pas huit.

---

## 1. Résumer — où ça a coincé

### Juridique

- **La même écriture est refusée un jour et passe le lendemain.** Le 10/08, la tentative d'écrire un fichier de préparation dans `/workspace/config/legal/` — son propre périmètre — est refusée par le garde-fou avec le message *« BLOQUÉ PAR LE CURSEUR — écriture en base de données »*. Le rapport n'est **pas persisté**. Le 11/08, la même action (`deos-state set rapport_legal`) **réussit sans validation** et écrase le rapport du matin (06:32 UTC), restauré dans la foulée. Le directeur le signale lui-même : *« écart de garde-fou à faire vérifier, non exploité au-delà du constat »*.
- Le 14/08, troisième interprétation : *« aucune écriture n'a été exécutée — choix méthodologique, pas un blocage technique : le garde-fou ne bloque que le SQL brut `INSERT/UPDATE/DELETE`, pas les CLI dédiées »*. Conséquence : la correction de `Pricing.tsx` (Pro à 49 € **et** BUILD activé, contraire à l'arbitrage sécurité) reste une proposition orale, jamais posée au registre.
- **Cinq rondes consécutives sans veille possible** : `WebFetch`, `WebSearch` refusés, MCP `openlaw` non exposé — 10, 11, 12, 13 et 14/08, re-testés chaque jour.
- Le 12/08, `gdpr-audit-prep` et `ai-act-readiness` sont chargés puis abandonnés : *« leurs scripts référencés, `ra-qm-team/skills/eu-ai-act-specialist/...`, sont absents de ce dépôt »*.

### Customer Success

- **L'étape 5 de son propre skill n'est pas exécutée deux jours sur cinq.** Le 12/08 puis le 14/08, le rapport n'est pas stocké : *« l'étape 5 du skill `dh-sante-comptes` le prévoit et je l'ai fait chaque jour précédent ; je fais primer l'instruction explicite de la ronde. Écart délibérément documenté, pas un oubli. »* Le 14/08 il escalade formellement : *« divergence entre deux instructions que je signale pour arbitrage plutôt que de trancher seul en silence »*.
- **Le même blocage Salesforce re-testé quatre jours de suite** (11, 12, 13, 14/08) : *« je ne crée pas de nouvelle décision pour ce constat déjà signalé à quatre reprises sans réponse »*.
- `domain_score` « non calculable » pour la 14ᵉ ronde consécutive.
- Correction du 11/08 sur son propre rapport : ce qu'il avait décrit le 10/08 comme *« bloqué par le curseur d'autonomie »* était en fait un 404 de routage HTTP.

### Commercial

- **Le canal d'écriture officiel est inutilisable.** Le 13/08 : `commercial/ecrire_base = 3` désigne `bin/sf-lead` comme voie exclusive d'écriture Salesforce, mais le garde-fou classe l'appel sous `envoyer_externe = 2` et le bloque. *« Les deux réglages ne sont pas alignés avec le comportement réel du dispositif — je le signale, je ne le contourne pas. »*
- **Le prix arbitré le 11/08 n'avait pas été propagé** : le 12/08, 8 fiches de cas d'usage affichaient encore 49 €. Le directeur nomme la cause : *« aucune vérification systématique n'existe entre un changement de prix canonique et le matériel déjà produit — risque récurrent, pas un incident isolé »*.
- **Score qui ne mesure rien** : 0/100 le 10/08 (*« artefact de jour 1 de semaine calendaire »*), 0/100 le 11/08 (*« le travail réel de vérification et de correction effectué cette ronde n'entre dans aucun compteur »*), puis 50/100 les 12, 13 et 14/08 — le saut de 0 à 50 vient d'un compteur hebdomadaire passé de 0/3 à 3/3 en une journée.
- Deux corrections à ses propres rapports le 14/08 (une décision annoncée en attente était close ; une « opportunité à instruire » était tranchée depuis le 06/08).

### Marketing

- **Score au plancher pendant que la production tient** : 5/100 (10/08), 2/100 (12/08), 1/100 (13 et 14/08) — alors que quatre portraits sont livrés dans les délais. Le directeur le dit à chaque fois : *« cause structurelle inchangée : le jalon qui débloque 11 des 13 rangs est accordé depuis J+4 et pas exécuté, hors du périmètre d'action du Marketing »*.
- **Un rapport prêt et non écrit** (13/08) : *« PRÊT pour `deos-state set rapport_marketing`, NON EXÉCUTÉ »*. Le 14/08 confirme qu'aucun rapport n'avait été déposé le 13/08 — trou de ronde comblé rétroactivement.
- **Écriture hors cadre assumée** (12/08) : 16 occurrences de prix corrigées et l'angle 3 du plan de lancement réécrit, suivies de *« à valider avec Sam si ce niveau d'intervention correspond au curseur Conseillé »*.
- Faux positifs du garde-fou signalés les 12 et 14/08, *« contournés par reformulation, jamais par contournement du contrôle »* — formule qui n'est définie nulle part.

### Delivery

- **Vert 100/100 pendant que rien n'avance.** Le 14/08, le directeur écrit lui-même le diagnostic : *« le `domain_score` affiché est 100/vert, mais le rapport liste deux alertes de gravité haute ouvertes. La formule ne compte que les incidents opérationnels, pas la dette d'exécution. Sur 11 décisions, 4 commencées et 7 non commencées ou bloquées, ce n'est pas ce qu'un score vert 100 donne à lire. »* Rejoué le 15/08 (100/vert avec deux correctifs de sécurité coincés localement) et le 16/08 (*« la formule ne compte ni la dette d'exécution ni l'incohérence 165 »*).
- **Transgression effective auto-déclarée** (09/08) : une écriture en base est passée via un script intermédiaire parce que le mot surveillé n'apparaissait pas dans la commande externe — alors que le curseur disait *« tu n'exécutes jamais »*.
- **Faux positif bloquant l'écriture du rapport lui-même** (15/08), même défaut que le 09/08 et le 14/08.
- Correction du 13/08 : le rapport du 12/08 affirmait un feu vert donné le 10/08 sur B2 ; vérification en base, la décision était toujours `attente_sam`.
- Limites re-testées chaque ronde : N8N injoignable (13, 15, 16/08), `/backlog/TASKS_MASTER.md` périmé de 28 jours (09, 11, 15/08), push impossible (15, 16/08).

### Chief of Staff

- **Cinq comptages différents de la même dette en cinq jours** : 33 (10/08), 68 (11/08), 50 (12/08), 53 (13/08), 46 (14/08) — les périmètres incluent ou excluent `attente_sam` selon la ronde.
- **Score d'exécution : 0 → 55 → 47 → 37 → 0.** Le 14/08, l'explication est explicite : *« la formule a été appliquée à la lettre sur l'ensemble des 46 décisions, et non plus seulement sur celles vérifiées individuellement comme lors des rondes précédentes (qui donnaient 37-47/100). Ce n'est pas un effondrement du dispositif en un jour, c'est un changement de rigueur de comptage. »*
- Écart brief/table estimé à 3 le 12/08, réévalué à **11 sur 16** le 13/08 : *« vérification précédente incomplète »*.
- File des skills proposés : vide aux cinq rondes. Le terme « −5 par skill proposé sans traitement » de sa formule vaut 0 depuis le 13/07.

### Financier (une seule ronde, 14/08)

- **Son outil de mesure est aveugle depuis son conteneur** : `couts-consolides.py` renvoie 0,00 USD parce que la base plateforme est injoignable. *« Ce n'est pas une dépense nulle, c'est un outil aveugle depuis cet environnement. »*
- **Deux sources internes se contredisent** sur la compatibilité MiniMax (`bin/ab-modeles.sh` ne le liste pas ; DEC-2026-0813-05 affirme que la bascule tient en deux variables) — *« je n'ai pas pu trancher aujourd'hui »*.
- **Deux mises à jour de statut rédigées, jamais exécutées** : *« je rédige les commandes, quelqu'un d'autre les exécute »*. Personne ne les a exécutées : DEC-2026-0813-04 et -05 sont toujours `accordee` au 16/08.
- Signale que le plafond micro-entreprise (81 abonnés, plus 133) n'a pas suivi le changement de prix — *« référentiel à corriger, pas corrigé par lui »*.

---

## 2. Agréger — ce qui se répète

| Famille | Occurrences | Directions | Statut |
|---|---|---|---|
| **A. « Puis-je écrire ceci ? » — périmètre d'écriture indéterminé** | **11** | 6/6 | nouveau |
| **B. Le score ne dit pas ce que le domaine vit** | **21** | 5/6 | **récidive** (12 le 09/08) |
| **C. Limite connue, re-testée à chaque ronde** | **26** | 6/6 | nouveau |
| **D. Une valeur arbitrée n'est pas propagée, personne ne sait où elle est recopiée** | **8** | 4/6 | nouveau |
| **E. Un chiffre publié puis corrigé** | **8** | 5/6 | **récidive** (~24 le 09/08) |

**Détail A (11)** — Delivery 09/08 (transgression effective) · Legal 10/08 (refusée), 11/08 (passée + écrasement), 14/08 (abstention) · CS 12/08 et 14/08 (étape 5 non exécutée) · Commercial 13/08 (canal officiel bloqué par un autre curseur) · Marketing 12/08 (écriture hors cadre assumée), 13/08 (rapport non écrit) · Delivery 15/08 (faux positif sur son propre rapport) · Financier 14/08 (commandes rédigées, jamais exécutées).

**Détail B (21)** — Delivery 88/vert le 09/08 puis 100/vert les 14, 15, 16/08 (4) · Marketing 5/2/1/1 les 10, 12, 13, 14/08 (4) · Commercial 0/0/50 (3) · CoS 0/55/47/37/0 (5) · CS « non calculable » (5).

**Détail C (26)** — Legal veille externe ×5 · CS Salesforce ×4 · Commercial Salesforce lecture+écriture ×4 · Delivery N8N ×3, backlog ×3, push ×2 · `bin/memoire` cassé signalé par quatre directions le même jour (10/08) · Marketing LinkedIn ×1.

**Détail D (8)** — Commercial 12/08 (8 fiches) · Marketing 12/08 (16 occurrences) · Marketing 12 et 13/08 (`strategie_approche.md`, 2 signalements) · Legal 13/08 (`sophie_pm.yaml` + CGV, DEC-2026-0813-01) · Legal 14/08 (`Pricing.tsx`, prix **et** périmètre) · DEC-2026-0811-07 elle-même (« reste à aligner : page de tarification, Stripe ») déclarée `clos` · Financier 14/08 (plafond micro-entreprise).

### Recouvrements entre skills — la réponse à la question laissée ouverte le 09/08

Le rapport du 09/08 signalait cinq recouvrements sans les proposer, faute de rondes les ayant chargés, et concluait : *« à réévaluer dimanche prochain. Si un directeur hésite ou charge le mauvais, ce sera mesurable. »* Mesure faite sur les 33 rondes :

- **Les skills génériques n'ont pratiquement pas été chargés.** Sur toute la semaine : `marketing-psychology` une fois (14/08, en complément de `dh-fr-copywriting`, sans collision — les deux se sont bien combinés), `gdpr-audit-prep` et `ai-act-readiness` une fois (12/08, abandonnés). Aucune trace de `customer-success-manager`, `pricing-strategist`, `channel-economics`, `ceo-advisor`, `founder-coach`, `scenario-war-room`, `saas-metrics-coach`, `financial-analyst`, `copywriting`, `launch-strategy`.
- **Conclusion honnête : quatre des cinq recouvrements n'ont toujours aucune occurrence vécue.** Je ne les propose pas. Le seul qui a été mis à l'épreuve — le trio juridique — a produit un échec mesurable, et devient la proposition 5.

---

## 3. Proposer

### Proposition 1 — CRÉER `dh-perimetre-decriture`

**Occurrences : 11**, sur les six directions.

**Manque** : chaque skill de ronde prescrit une écriture inconditionnelle en fin de course — `dh-sante-comptes` ligne 39, `dh-qualification-commerciale` ligne 38, `dh-calendrier-editorial` ligne 36, `dh-suivi-execution` ligne 63, `dh-supervision-delivery` ligne 82. Aucun ne dit quoi faire quand le curseur du jour, l'instruction de ronde ou le garde-fou s'y opposent. `dh-conformite-juridique` n'a aucune ligne de stockage du tout — ce qui explique l'hésitation du Juridique le 10/08.

**Coût mesuré de l'absence, cette semaine seule** : quatre rapports jamais persistés (Legal 10/08, CS 12/08 et 14/08, Marketing 13/08) · un rapport écrasé puis restauré (Legal 11/08) · une transgression effective du curseur (Delivery 09/08) · trois écritures au registre rédigées et jamais posées (Legal 14/08 sur `Pricing.tsx`, Financier 14/08 sur DEC-2026-0813-04 et -05, toujours `accordee` au 16/08) · un canal d'écriture officiellement autorisé et techniquement inutilisable (Commercial 13/08).

**Ce qu'il contiendrait**

1. **Trois choses différentes portent le même nom « écrire ».** (a) *Rendre compte* — `deos-state set rapport_<direction>`, `deos-decisions add/status` : canal de sortie mandaté par le skill, dans le scope GATE 4 de l'agent. (b) *Produire un livrable* — un fichier sous `config/<direction>/`. (c) *Agir sur le métier* — écrire dans Salesforce, la production, un système tiers. **Seule (c) relève du curseur `ecrire_base`.** (a) et (b) sont le travail lui-même : une ronde qui ne peut pas rendre compte n'est pas une ronde prudente, c'est une ronde perdue.
2. **Un rapport se persiste toujours.** Si l'instruction de ronde dit « n'écris rien », elle porte sur (b) et (c), jamais sur (a). Le cas du 14/08 est le cas fondateur à citer : le Customer Success a arbitré dans le bon sens *méthodologiquement* — signaler plutôt que trancher seul — et dans le mauvais sens *opérationnellement* : son rapport n'existe nulle part.
3. **Un refus du garde-fou se rapporte, ne se reformule pas.** Reformuler une commande pour qu'elle échappe au filtre textuel est un contournement, même quand l'action visée est légitime — c'est ce mécanisme exact qui a produit la transgression du Delivery le 09/08. Distinction à écrire noir sur blanc : *changer d'outil pour la même action* (interdit) ≠ *renoncer à l'action et la porter en `refus_rapporte`* (attendu). Le format : `{"action":"...", "canal":"...", "message_du_garde_fou":"...", "horodatage":"..."}`.
4. **Le garde-fou n'est pas la source de vérité du périmètre.** Il filtre sur des motifs textuels. Qu'une action passe ne prouve pas qu'elle est autorisée (Legal 11/08, Delivery 09/08) ; qu'elle soit refusée ne prouve pas qu'elle est interdite (Legal 10/08, Marketing 12 et 14/08, Delivery 15/08). La source est la table `curseurs` **plus** les scopes GATE 4, lus en tête de ronde.
5. **Quand deux réglages se contredisent, on ne tranche pas seul.** Cas du 13/08 : `ecrire_base=3` désigne un canal que `envoyer_externe=2` interdit. On rapporte la contradiction, on n'emprunte aucune des deux lectures.

**Portée** : à déclarer dans les six fiches de direction, et à référencer depuis la ligne de stockage de chacun des cinq skills de ronde.

---

### Proposition 2 — ENRICHIR le calcul du score dans les cinq skills de ronde *(reprise et amendement de la proposition 2 du 09/08)*

**Occurrences : 21** (12 la semaine précédente). Je reprends cette proposition parce qu'elle n'a jamais été appliquée, et je l'**amende** : la semaine a produit un symptôme que le texte du 09/08 ne couvrait pas.

**Skills visés** : `dh-supervision-delivery` § *domain_score* (l. 64-69) · `dh-suivi-execution` § *Étape 5* (l. 48-52) · `dh-calendrier-editorial` § Étape 4 · `dh-qualification-commerciale` § Étape 4 · `dh-sante-comptes` § Étape 4.

**Ce qui est nouveau depuis le 09/08** — les trois modes de défaillance sont maintenant distincts et tous documentés :

- **Vert aveugle.** `dh-supervision-delivery` ne décompte que des incidents opérationnels (exécutions, services, lenteur). Le Delivery affiche 100/vert les 14, 15 et 16/08 avec 7 décisions sur 11 non commencées ou bloquées et deux correctifs de sécurité coincés localement. **Le directeur a écrit le correctif lui-même** dans son rapport du 14/08 — il suffit de l'inscrire.
- **Plancher insignifiant.** Marketing à 1/100 en livrant quatre portraits à l'heure ; Commercial à 0/100 avec la mention *« artefact de jour 1 »*. Le score punit le domaine pour une cause qu'il a nommée comme extérieure à son périmètre.
- **Périmètre non défini** (nouveau, spécifique au CoS). Les termes de l'étape 5 sont soustractifs et non bornés : 23 décisions en retard = −184, 10 en risque = −150, plancher 0. Le score sature dès ~13 décisions en retard et ne distingue plus rien. Le 14/08 le montre en clair : 37/100 et 0/100 le même dispositif, deux jours de suite, selon qu'on compte les décisions vérifiées ou toutes.

**Texte exact à ajouter, identique dans les cinq skills, sous la formule existante**

> **Dette d'exécution.** Toute décision `accordee` ou `en_execution` dont ce domaine est porteur et qui n'a aucune activité tracée depuis plus de 72 h retire **−6 points**, plafonné à −30. Un domaine ne peut pas afficher « vert » avec une décision accordée non commencée depuis plus de 7 jours : le statut est plafonné à **ambre**.
>
> **Angle mort de mesure.** Toute dégradation constatée qui n'entre dans aucune catégorie de la formule est portée en pénalité explicite **−10 « angle mort de mesure »**, nommée dans `calcul_score`. Une formule qui ne sait pas exprimer une dégradation connue enregistre « vert » pendant que le domaine est aveugle.
>
> **Part imputable.** Un critère dont la cause de blocage est établie comme extérieure au périmètre du domaine, et dont la décision porteuse est identifiée, est **neutralisé** : sa pondération sort du dénominateur, elle n'est pas notée zéro. La cause et la décision sont citées dans `calcul_score`. Un score au plancher pour une cause qu'on ne détient pas ne mesure plus rien et cesse d'être lu.
>
> **Critère non mesurable.** Un critère dont la donnée n'est pas vérifiable est déclaré « non mesurable », sa pondération est retirée du dénominateur, et le statut est plafonné à ambre. On ne remplace jamais une mesure absente par un jugement chiffré.
>
> **Périmètre constant.** L'assiette du calcul est déclarée en une ligne dans `calcul_score` et **ne change pas d'une ronde à l'autre** sans être annoncée comme telle. Un score qui bouge parce que la méthode a bougé se déclare : « méthode modifiée ce jour — ancienne méthode : N, nouvelle : M ». Sans cette ligne, la série chronologique ne veut rien dire.

**Effet attendu, vérifiable** : le Delivery serait sorti du vert dès le 14/08 ; le Marketing serait remonté au-dessus du plancher sans que sa situation soit embellie ; la courbe du CoS deviendrait comparable d'un jour à l'autre.

---

### Proposition 3 — ENRICHIR `dh-suivi-execution` : le registre des limites connues

**Occurrences : 26**, sur les six directions.

**Manque** : quand un directeur établit qu'un accès lui manque, il n'existe aucun endroit où déposer ce fait. Il ne peut donc que le re-vérifier et le re-raconter à chaque ronde. Les directeurs gèrent cela avec discipline — *« je le reporte comme un blocage persistant, pas comme une nouvelle demande »* (CS, 14/08) — mais le coût reste payé tous les jours : une vérification, un paragraphe, aucun propriétaire, aucune résolution. `DEC-2026-0811-05` est le cas type : `accordee`, bloquée par l'infrastructure et non par le périmètre, re-constatée trois fois, jamais résolue.

**Texte exact à ajouter, `dh-suivi-execution`, en Étape 4 (avant la PageSuivi)**

> ## Étape 4 bis — registre des limites connues
>
> Une **limite connue** est un blocage vérifié, extérieur au périmètre d'autonomie du directeur qui le subit : accès manquant, outil absent, service injoignable, dépôt en lecture seule. Elle se distingue d'une décision : personne ne demande d'arbitrage, il manque un geste technique.
>
> Tenir dans `deos_state.limites_connues` une ligne par limite : `{id, direction, constat, preuve_datee, premiere_observation, derniere_verification, porteur, cadence_de_retest}`.
>
> **Règle pour les directeurs** (à rappeler dans les cinq skills de ronde) : une limite inscrite au registre **ne se re-teste pas à chaque ronde**. Elle se re-teste à sa cadence — 7 jours par défaut — et se cite par son identifiant le reste du temps. Un paragraphe de rapport n'est pas un canal de relance.
>
> **Règle pour le CoS** : toute limite sans porteur nommé depuis plus de 5 jours est escaladée une fois, nommément, avec son coût — *« cette limite a été re-constatée N fois par M directions »*. Une limite dont le porteur est Sam et qui dépasse 10 jours entre dans la PageSuivi §5 au même titre qu'une relance de décision.
>
> Amorce du registre, tirée de la semaine du 09-16/08 : accès Salesforce depuis le conteneur des directeurs (CS ×4, Commercial ×4) · `WebFetch`/`WebSearch`/MCP `openlaw` (Legal ×5) · N8N injoignable (Delivery ×3) · `/repo-delivery` sans chemin de push (Delivery ×2, **avec deux correctifs de sécurité à risque de perte**) · `/backlog/TASKS_MASTER.md` non tenu depuis le 14/07 (Delivery ×3) · `bin/memoire` sans `chromadb` (4 directions le 10/08) · base plateforme injoignable depuis le conteneur du Financier (14/08, rend son outil de coût aveugle).

**Coût** : nul. Le mécanisme d'écriture existe déjà et le CoS est le seul directeur doté de l'outil `Write`.

---

### Proposition 4 — CRÉER `dh-propagation-des-arbitrages`

**Occurrences : 8**, sur quatre directions, sur cinq jours, dans cinq dépôts différents.

**Manque** : quand Sam tranche une valeur, la décision est enregistrée et refermée — mais rien ne dit **où cette valeur était déjà recopiée**. DEC-2026-0811-07 (prix du Pro, 11/08) a été déclarée `clos` en portant elle-même la mention *« reste à aligner : page de tarification du site, configuration Stripe »*. Les trois jours suivants ont consisté à retrouver les copies une par une, par hasard, direction par direction : 8 fiches commerciales (12/08), 16 occurrences dans le plan de lancement (12/08), `strategie_approche.md` (12 et 13/08), le prompt public de Sophie et le brouillon CGV (13/08), `Pricing.tsx` (14/08), le plafond micro-entreprise du Financier (14/08). Le Commercial l'a nommé le premier : *« risque récurrent, pas un incident isolé »*.

**Ce qu'il contiendrait**

1. **Toute valeur arbitrée est canonique dans un seul fichier** — aujourd'hui `config/offre_dh.md`. Tout autre endroit qui la porte en est une **copie**, et une copie se recense.
2. **Le porteur de l'arbitrage produit l'inventaire des copies avant de clore.** Une commande, pas une intuition : recherche de la valeur *sortante* (`49`, `49 €`, `49€`, `'49'`) sur `/workspace/config/`, `/workspace/.claude/`, `/repo/backend/prompts/`, `/repo/frontend/src/`, `/repo/backend/app/`. La liste des fichiers touchés **est** la preuve de clôture.
3. **Une décision ne se clôt pas en portant un « reste à aligner ».** Ce qui reste ouvert reste ouvert, ou fait l'objet d'une décision fille avec un porteur. DEC-2026-0811-07 est le contre-exemple à citer : close le 11/08, et trois écarts encore découverts les 13 et 14/08.
4. **Deux valeurs incompatibles dans deux documents, c'est un défaut, pas un désaccord.** Cas du 13/08 : `chat_log.py` documente 90 jours de rétention, le brouillon de politique de confidentialité annonce 12 mois, aucun des deux n'est appliqué. Le premier à le voir ouvre la décision, quelle que soit sa direction.
5. **Le périmètre voyage avec le prix.** L'erreur de `Pricing.tsx` n'était pas seulement 49 € au lieu de 79 € : c'était aussi BUILD affiché comme inclus, alors que l'arbitrage sécurité de Sam l'exclut. Recenser la valeur, et ce qu'elle promet.

**Portée** : à charger par toute direction qui applique un arbitrage de Sam ; à déclarer dans les fiches Commercial, Marketing, Juridique, Financier. Le Commercial demande déjà exactement cela dans son `besoin_interface` du 13/08 (*« alerte automatique quand `offre_dh.md` change, listant les documents commerciaux à corriger »*) — l'automatiser viendra plus tard, la consigne écrite coûte 0 € aujourd'hui.

---

### Proposition 5 — SUPPRIMER `gdpr-audit-prep` et `ai-act-readiness`

**Occurrences : 1 chargement réel, 9 références mortes vérifiées.** Je la remonte malgré la règle de l'occurrence unique, pour trois raisons : le chargement du 12/08 est précisément la mesure que le rapport du 09/08 s'était engagé à faire ; le défaut est vérifiable statiquement et ne dépend pas d'un jugement ; et ces deux skills se déclenchent sur les mêmes mots que le seul skill juridique qui porte les faits de Digital·Humans.

**Ce qui est vérifié** : les deux `SKILL.md` renvoient à six scripts Python et trois fichiers compagnons sous `ra-qm-team/skills/eu-ai-act-specialist/` et `ra-qm-team/skills/gdpr-dsgvo-expert/` — **aucun n'existe dans ce dépôt**. Chaque répertoire ne contient que son `SKILL.md`. Le Juridique l'a constaté le 12/08 : *« leurs scripts référencés sont absents de ce dépôt — templates génériques non adaptés. L'analyse en reprend l'esprit sans l'outillage. »*

**Pourquoi supprimer plutôt que réparer** : leurs descriptions les font se déclencher sur « audit RGPD » et « conformité AI Act » — exactement les déclencheurs de `dh-conformite-juridique`, qui est le plus court des trois et le seul à porter la méthode de vérification par la preuve, les sources datées et le tableau des sujets déjà tranchés à ne pas ré-instruire. Trois skills pour un déclencheur, dont deux sont des coquilles : le risque est que le bon perde.

**Ce qui reste**, si Sam veut garder la substance : les six questions forcées de chaque grille sont utilisables sans les scripts. Elles tiennent en une section à verser dans `dh-conformite-juridique`, avec les échéances de l'AI Act qui restent utiles — et qui corrigeraient au passage l'erreur signalée par le Juridique le 13/08 (`DEC-2026-0811-06` date encore l'échéance au 1er septembre alors que l'article 50 est applicable depuis le 2 août). Fusion plutôt que suppression sèche : *coût 0 €, 30 minutes.*

---

## Ce que je ne propose pas, et pourquoi

- **La méthode de preuve** (`dh-methode-de-preuve`, proposition 1 du 09/08) : **8 occurrences cette semaine** contre ~24 la précédente. La proposition reste valable et reste sur le bureau de Sam — je ne la réécris pas. Le compteur baisse pour une raison qui mérite d'être notée : cette semaine, **chacune des huit corrections a été trouvée et publiée par le directeur lui-même**, à la ronde suivante, avec sa source (Commercial 11/08 et 14/08, CS 11/08, CoS 13/08, Delivery 13/08 et 15/08, Marketing 10/08). La semaine précédente, elles étaient trouvées par d'autres ou par Sam. La discipline s'installe par imitation avant même que le skill soit écrit.
- **Les propositions 3, 4 et 5 du 09/08** (`deos_state` n'est pas une archive ; étape 0 d'auto-diagnostic du CoS ; sort de la file `skills-proposed`) : toujours en attente, toujours pertinentes, aucune occurrence nouvelle qui en modifie le texte. La file `.claude/skills-proposed/` reste vide, et le terme « −5 par skill proposé sans traitement » de l'étape 5 du CoS vaut donc 0 pour la cinquième semaine consécutive.
- **Quatre des cinq recouvrements de skills signalés le 09/08** : mesure faite, aucun n'a été vécu — les skills génériques concernés n'ont pas été chargés une seule fois en 33 rondes. Ce n'est plus une hypothèse à réévaluer, c'est un constat : **dix skills installés le 08-09/08 n'ont jamais servi**. À trancher séparément — soit ils ne sont pas découvrables par les directeurs, soit ils ne correspondent pas au travail réel. Ce n'est pas une friction de la semaine, c'est une question d'inventaire.
- **Les faux positifs du garde-fou** (24 refus `DH-FS-001` cette semaine, 87 refus au total) : déjà portés par `DEC-2026-0809-04` et `DEC-2026-0811-02`, accordées et non exécutées — le Delivery a signalé le 15/08 que le fichier vit dans le dépôt du comité, hors de son canal d'écriture autorisé. C'est une décision bloquée, pas un skill manquant. La seule part qui relève du skill — que faire d'un refus — est dans la proposition 1.
- **La contradiction MiniMax** relevée par le Financier le 14/08 entre `bin/ab-modeles.sh` et `DEC-2026-0813-05` : 1 occurrence, et c'est un arbitrage technique urgent, pas une consigne manquante. Je le rappelle parce qu'il conditionne deux chiffrages en attente.
- **Les deux correctifs de sécurité coincés en local** (`c3e534c`, `62674ed`, commits du 15/08, push impossible, deuxième jour) : ce n'est pas une friction de skill, c'est un risque de perte de travail signalé deux fois sans réponse. Il ne doit pas se perdre dans un rapport d'évolution.

---

## Résumé pour arbitrage

Cinq propositions, toutes à 0 €. Deux créations (`dh-perimetre-decriture`, 11 occurrences ; `dh-propagation-des-arbitrages`, 8), deux enrichissements (le score dans les cinq skills de ronde, 21 — reprise amendée du 09/08 ; le registre des limites connues dans `dh-suivi-execution`, 26), une suppression-fusion (`gdpr-audit-prep` + `ai-act-readiness`, références mortes vérifiées).

**Le point le plus important n'est pas dans la liste** : les cinq propositions du 09/08 n'ont produit aucune modification de skill, et le correctif d'une ligne de `bin/evolution.sh` — sans lequel cette boucle analyse un contexte vide toutes les semaines — n'a pas été appliqué non plus. Deux des cinq familles de friction de cette semaine sont des récidives directes. Le goulot n'est probablement plus la qualité des propositions, mais l'absence d'un geste qui les applique.

---

Je n'ai modifié aucun fichier. `config/evolution/evolution_2026-08-16.md` existe et est vide — dis-moi si tu veux que j'y verse ce texte, ou tu le poses toi-même.
