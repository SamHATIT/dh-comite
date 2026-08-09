J'ai lu les sources directement plutôt que de m'en tenir à la matière fournie — pour une raison que je dois signaler d'abord.

---

# Boucle d'évolution des skills — semaine du 02/08 au 09/08/2026

## Avertissement sur la matière fournie

La matière transmise par `bin/evolution.sh` était **vide pour les 38 rondes de la semaine** : sous chaque titre de ronde, rien. J'ai vérifié la cause avant de conclure quoi que ce soit.

Le script extrait les clés `faits`, `alertes`, `escalades`, `donnees_manquantes`, `besoin_interface` **à la racine** du JSON de ronde (`bin/evolution.sh`, boucle `find rondes`). Or un fichier `rondes/*.json` est une enveloppe de résultat Claude Code : ces clés n'existent pas à la racine, elles vivent en texte libre dans le champ `.result`. Le `except` avale l'erreur et n'imprime rien. La seule ligne non vide de tout le contexte — `illisible`, sous `directeur-commercial-revision` — n'est pas un rapport illisible : c'est un fichier réellement corrompu (l'enveloppe en ligne 1, puis le plan de l'agent appendé à partir de la ligne 2).

**Conséquence** : l'analyse aurait porté sur les seules décisions, soit un tiers de la matière. J'ai donc relu moi-même les 38 rondes via `jq -r '.result'`, les 8 briefs, le JOURNAL, la note de Sam du 06/08 et les 22 skills. Ce qui suit s'appuie sur ces lectures.

*Correctif d'une ligne, hors des cinq propositions : lire `.result` et le passer au modèle tel quel, plutôt que de chercher des clés qui n'existent pas.*

---

## 1. Résumer — où ça a coincé

### Delivery

- **Six rondes consécutives à 88/100 « vert »** (04, 05, 06, 07, 08, 09/08) pendant que la chaîne exec 165/166 était bloquée depuis le 02/08 et que la couverture des logs tombait à **~1 seconde sur 86 400** (ronde du 06/08). Le directeur l'écrit lui-même le 06/08 : *« La dégradation des logs n'est pas déduite mécaniquement (elle ne correspond à aucune catégorie formelle de la formule). »* La formule du skill ne sait pas dire qu'un domaine est aveugle.
- **Contradiction décision/base escaladée en gravité haute deux jours de suite** (07/08 puis 08/08, INC-2026-0808-01) : DEC-2026-0806-23 et DEC-2026-0807-02 affirmaient un correctif appliqué et un BUILD lancé, `v_deos_build_phases` ne montrait rien.
- **Le 09/08, le raisonnement s'avère faux** : la phase 1 avait réellement réussi le 08/08 à 09:05:10Z, et c'est **l'écriture de la trace** qui était cassée (`TASK-001` textuel dans une colonne entière, transaction avortée). Le CEO se corrige dans le brief du 09/08 : *« Mon raisonnement — pas de trace, donc pas d'activité — était faux ici. »*
- **Diagnostic faux publié puis rétracté** (DEC-2026-0808-06) : accusation portée contre Marcus sur la foi d'une requête `LIKE '%Lead__c%'`, où `_` est un joker. Zéro occurrence réelle après re-vérification par `position()`.
- `/backlog/TASKS_MASTER.md` en retard de trois semaines, signalé le 07/08 puis le 09/08, sans effet.

### Commercial

- **Huit constats identiques de `permission denied`** rapportés comme KPI du 14/07 au 06/08 (« 5ᵉ constat » le 03/08, « 6ᵉ » le 04/08, « 7ᵉ » le 05/08, « 8 constats » le 06/08). Le directeur re-testait à chaque fois la **table** `leads` — interdite par conception — jamais `\dv`. Le 06/08 il lance enfin `\dv` : **les vues existaient déjà**, avec le périmètre RGPD attendu.
- **Chiffre inventé puis corrigé** : le rapport du 03/08 annonce 11/15 fiches de cas d'usage ; l'audit fichiers + git du 04/08 en trouve 5. Le chiffre venait du rapport de la veille, pas d'un comptage.
- **Score 100 / statut ambre** le 07/08, contradiction que le directeur assume à la main : *« ce chiffre mesure un rythme de processus, pas la santé réelle du pipeline »*. La formule du skill ne prévoit pas ce cas.
- Refus de scope sur `deos-state set plan_commercial_revise` (révision du 02/08) — refus respecté, non contourné, mais le plan n'a survécu qu'en fichier.

### Marketing

- **Barème inventé cinq rondes de suite** sur le critère « cadence » (50 points) : 20/50 le 02/08, 15/50 le 03/08, 25/50 les 05 et 07/08. Le directeur le déclare deux fois explicitement : *« le skill ne fixe pas de barème fin pour la pondération du critère cadence ; la répartition est une appréciation documentée pour audit, pas une mesure automatique. »*
- **Travail refait** le 07/08 : *« `deos_state` ne conserve qu'une valeur par clé (pas d'historique) — le bloc `besoin_interface` détaillé du 05/08 n'était plus récupérable ; reconstruit intégralement. »*
- Publication réelle des rangs 1-2 non vérifiable, signalée comme angle mort structurel dans **cinq rondes** (02, 03, 04, 05, 07/08) sans que le skill dise quoi faire d'un critère non mesurable.

### Customer Success

- **Neuf rondes consécutives** avec `domain_score` « non calculable » (le directeur les compte lui-même le 07/08). La formule du skill (usage 40 / tickets 30 / −15 / −20) suppose des comptes qui n'existent pas avant septembre.
- Bloc `besoin_interface` « reconduit sans modification » les 06 et 07/08 — même cause que le marketing : `deos_state` écrase.
- Le 07/08, découverte que le permission set `Comite_RO` **ne couvre pas l'objet `Case`** — donc le canal tickets restera invisible même une fois câblé.

### Chief of Staff

- **Deux rondes perdues** (04/08 et 06/08) : le fichier ne contient qu'un accusé de lancement, *« je te restitue dès qu'il termine »*. Aucun rapport. Le 09/08, aucune ronde du tout — le CEO fait le ménage du registre *« à défaut de CoS »*.
- **L'étape 0 d'auto-diagnostic demandée par le CoS lui-même**, classée `[HAUTE]` dans son plan du 02/08 (*« défense en profondeur si le CEO échoue en même temps que moi — déjà arrivé »*), redemandée dans sa révision, **jamais écrite**. Elle n'est toujours pas dans `dh-suivi-execution`.
- **La file `.claude/skills-proposed/` constatée vide** aux rondes des 02/08, 03/08, 05/08, et par l'audit DSI du 02/08. Elle est vide depuis sa création le 13/07.
- Le 07/08, un « fait » de décision contredit par la base (DEC-2026-0806-23), escaladé à Sam sans délai — légitime sur la méthode, mais la conclusion reposait sur la même inférence que celle qui s'est révélée fausse le 09/08.

### Juridique et CEO

- Six jours sans être dans aucune ronde (FIX-LEGAL-001), aucun périmètre d'écriture (FIX-LEGAL-002) — rapports refusés en silence. Corrigé le 08/08.
- **Défaut de routage assumé par le CEO** (DEC-2026-0809-05) : B2 et B3 du rapport juridique du 08/08, classés critique et bloquant, non routés pendant 24 h.
- Le brief du 06/08 annonçait 25 décisions en attente alors que 2 seulement attendaient Sam — troisième cas de la semaine d'un chiffre publié sans être recompté.

---

## 2. Agréger — ce qui se répète

| Famille de friction | Occurrences | Où |
|---|---|---|
| **A. Un fait affirmé, ou nié, sans preuve recomptée** | **~24** | Delivery 04→09/08 (6), CS 04→07/08 (4), Commercial 05, 06/08 (2), CoS 07/08 (1), CEO briefs 08 et 09/08 (2), DEC-2026-0808-06, DEC-2026-0809-05, Commercial 11/15→5/15, brief 25→2, 8 constats `permission denied` sur le mauvais objet |
| **B. Le `domain_score` ne dit pas ce que le domaine vit** | **12** | Delivery 88/vert ×6, Marketing barème inventé ×5, Commercial 100/ambre ×1 |
| **C. `deos_state` écrase — un livrable long disparaît** | **7** | Marketing 07/08 (retravail réel), CS 06 et 07/08, Commercial 02 et 03/08, Delivery 05/08, CoS révision |
| **D. Le dispositif tombe et personne ne le déclare** | **5** | CoS 04/08 et 06/08 (rondes perdues), CoS 09/08 (absente), demande d'étape 0 du 02/08, redemande en révision |
| **E. La file des skills proposés est morte** | **4 constats + 16 contournements** | CoS 02, 03, 05/08 ; audit DSI 02/08 ; 16 des 22 skills posés en direct les 08 et 09/08 |

### Recouvrements entre skills — signalés, pas encore proposés

**Seize des vingt-deux skills ont été installés dans les 48 dernières heures** (11 le 08/08, 5 le 09/08). Aucune ronde de la semaine ne les a chargés : les collisions ci-dessous sont **structurelles et lisibles dans les descriptions**, mais **zéro ronde n'en a encore souffert**. La règle « une seule occurrence n'est pas une proposition » s'applique — je les signale pour l'arbitrage, je n'en fais pas une proposition cette semaine.

- **Customer Success** — `dh-sante-comptes` (formule 40/30/−15/−20, récitée dans 9 rondes) contre `customer-success-manager` (modèle de scoring pondéré + CLI Python). **Deux formules de santé différentes pour le même score.** C'est le recouvrement le plus dur, parce qu'il porte sur un calcul, pas sur un thème.
- **Marketing** — `dh-fr-copywriting` (« DÈS QUE l'on retravaille… du contenu français ») et `copywriting` (« when the user wants to write, rewrite, or improve marketing copy »). Déclencheurs identiques, doctrines différentes.
- **Juridique** — `dh-conformite-juridique`, `gdpr-audit-prep`, `ai-act-readiness` se déclenchent tous trois sur « audit RGPD » et « conformité AI Act ». Le seul qui porte les faits propres à DH — la règle « on n'affirme jamais une mesure qu'on ne peut pas prouver » et le tableau des **7 sujets déjà tranchés à ne pas ré-instruire** — est aussi le plus court. C'est celui qui risque de perdre.
- **CEO** — `dh-conseil-ceo`, `ceo-advisor`, `founder-coach`, `scenario-war-room` : quatre skills pour un arbitrage.
- **Commercial** — `dh-qualification-commerciale`, `pricing-strategist`, `channel-economics`.

**À réévaluer dimanche prochain avec des rondes qui les auront réellement chargés.** Si un directeur hésite ou charge le mauvais, ce sera mesurable.

---

## 3. Proposer

### Proposition 1 — CRÉER `dh-methode-de-preuve`

**Manque** : chaque direction sait qu'il faut une source datée (règle du repo). Aucune ne sait **comment établir qu'une chose n'a pas eu lieu**. C'est la friction la plus coûteuse de la semaine.

**Occurrences : ~24**, réparties sur les six porteurs (détail famille A ci-dessus).

**Coût de l'absence, mesuré** : deux briefs de contestation erronée du CEO (08 et 09/08), un diagnostic public à retirer (DEC-2026-0808-06), huit rondes commerciales à reconduire un blocage déjà levé, une escalade CoS à Sam sur une contradiction qui n'en était pas une (07/08). La règle existe déjà — mais **pour le seul Juridique**, dans `dh-conformite-juridique` (« la règle qui prime sur tout »). Il faut la généraliser aux cinq autres.

**Ce qu'il contiendrait**

1. **L'absence de trace n'est pas la preuve d'une absence.** Avant de conclure « ça n'a pas eu lieu », vérifier que le mécanisme d'écriture de la trace fonctionne. Cas fondateur du 09/08 : `v_deos_build_phases` à 0 ligne pendant que 482 417 jetons et 3,19 $ étaient réellement consommés — la transaction d'écriture du statut était avortée par un bug de type.
2. **Deux sources de nature différente.** Une contradiction entre une décision et une table ne se tranche pas avec cette seule table. Croiser : compteurs de coût et de jetons, historique git, journaux, taille de fichier. Le CEO a tranché le 09/08 par les jetons, pas par la table.
3. **Le piège du joker.** `LIKE '%Lead__c%'` fait de `_` un joker : `Lead__c` y signifie « Lead + deux caractères quelconques + c ». Pour une chaîne littérale : `position('Lead__c' in colonne) > 0`. Source : DEC-2026-0808-06.
4. **Tester le bon objet.** Un refus sur une table ne dit rien de l'existence d'une vue. Avant de reconduire un constat de blocage : `\dv` et `\dt`, jamais la seule requête de la veille. Source : 8 constats commerciaux du 14/07 au 06/08.
5. **Ne jamais recopier un chiffre.** Tout nombre publié dans un rapport est recompté à la source du jour. Trois cas : 11/15 → 5/15 (Commercial, 04/08), « 25 décisions en attente » → 2 (brief du 06/08), « 7 mentions fautives » → 0 (DEC-2026-0808-06).
6. **Formuler l'incertitude, pas la conclusion.** « Aucune trace au *[date, heure, requête]* — je ne peux pas trancher entre X et Y sans *[la source qui manque]* » plutôt que « ça n'a pas eu lieu ». Le Delivery l'a fait correctement le 08/08 dans INC-2026-0808-01 ; c'est ce modèle qu'il faut écrire.

**Portée** : à déclarer dans les six fiches de direction et dans le prompt du CEO.

---

### Proposition 2 — ENRICHIR le calcul du `domain_score` dans trois skills de ronde

**Skills visés** : `dh-supervision-delivery` (§ *domain_score*), `dh-calendrier-editorial` (§ *Étape 4*), `dh-qualification-commerciale` (§ *Étape 4*).

**Occurrences : 12** (famille B).

**Manque** : les formules produisent un chiffre qui contredit l'état du domaine, et aucune ne dit quoi faire d'un critère non mesurable.

**Texte exact à ajouter, identique dans les trois skills, sous la formule existante**

> **Plafond de statut.** Tant qu'une alerte de gravité haute est ouverte depuis plus de 72 h, le statut ne peut pas dépasser **ambre**, quel que soit le score. Un score et un statut qui divergent s'expliquent en une ligne dans `calcul_score`.
>
> **Angle mort de mesure.** Toute dégradation constatée qui n'entre dans aucune catégorie de la formule est portée en pénalité explicite **−10 « angle mort de mesure »**, nommée dans `calcul_score`. Une formule qui ne sait pas exprimer une dégradation connue enregistre « vert » pendant que le domaine est aveugle.
>
> **Critère non mesurable.** Un critère dont la donnée n'est pas vérifiable ne reçoit pas une note d'appréciation : il est déclaré « non mesurable », sa pondération est retirée du dénominateur, et le statut est plafonné à ambre. On ne remplace jamais une mesure absente par un jugement chiffré.

**Texte supplémentaire, `dh-calendrier-editorial` seulement**, en remplacement de « cadence tenue vs calendrier (50) » :

> **Cadence (50 pts)** = 50 × (contenus dont la publication est **confirmée par une source lue** ÷ contenus dont la date cible est passée). Sans accès en lecture au canal de publication, ce critère est **non mesurable** : le déclarer, retirer les 50 points du dénominateur, plafonner le statut à ambre. Ne pas produire de note d'appréciation.

**Effet attendu** : le Delivery serait sorti du vert dès le 05/08 au lieu du 09/08 ; le Marketing aurait cessé de produire cinq notes successives sans barème.

---

### Proposition 3 — ENRICHIR les quatre skills de ronde : `deos_state` n'est pas une archive

**Skills visés** : `dh-supervision-delivery`, `dh-qualification-commerciale`, `dh-sante-comptes`, `dh-calendrier-editorial` — section « sorties / stockage » de chacun.

**Occurrences : 7** (famille C), dont **un retravail intégral mesuré** : Marketing, ronde du 07/08.

**Texte exact à ajouter**

> **`deos_state` ne conserve qu'une valeur par clé.** Écrire y écrase l'écriture précédente, sans historique : ce que tu y as mis avant-hier n'est plus relisible. Tout livrable long — bloc `besoin_interface`, note de cadrage, étude, rapport d'incident, proposition d'évolution — est d'abord écrit dans `/workspace/config/<direction>/<AAAA-MM-JJ>_<sujet>.md`. `deos_state` ne porte que le rapport du jour et le **chemin du fichier**. Avant de reconstruire un bloc « reconduit depuis une ronde précédente », chercher le fichier : il existe probablement.

**Coût** : nul. Le Commercial applique déjà cette discipline de lui-même (`/workspace/config/commercial/` versionné, alerte basse du 03/08 : *« deos_state.rapport_commercial reste écrasé à chaque mise à jour ; le dossier versionné fait foi »*). Il s'agit de généraliser une pratique qui existe et fonctionne.

---

### Proposition 4 — ENRICHIR `dh-suivi-execution` : Étape 0, auto-diagnostic du dispositif

**Occurrences : 5** (famille D). Demandée par le CoS lui-même le 02/08 en priorité **HAUTE**, redemandée dans sa révision, jamais écrite.

**Manque** : le CoS audite l'exécution des autres sans jamais déclarer si son propre dispositif de reporting a tourné. Deux de ses rondes de la semaine n'ont produit aucun rapport (04/08, 06/08) sans que personne le signale ; la troisième (09/08) n'a pas eu lieu et c'est le CEO qui a fait le ménage du registre à sa place.

**Texte exact à ajouter, en tête du skill, avant l'Étape 1 actuelle**

> ## Étape 0 — auto-diagnostic (avant tout le reste)
>
> ```bash
> ls -la /workspace/rondes/*-$(date -u +%F).json          # rondes du jour : taille 0 = ronde perdue
> ls -la /workspace/rondes/ | tail -20                     # ma propre ronde d'hier a-t-elle produit un rapport ?
> /workspace/bin/deos-state get brief | head -5            # le brief du jour existe-t-il ?
> ```
>
> Déclarer en tête de rapport, avant tout audit de décision :
> - ma ronde de la veille a-t-elle produit un rapport, ou un fichier vide/tronqué ?
> - quelles directions n'ont pas de rapport frais (> 24 h) ?
> - le brief du jour existe-t-il et de quand date-t-il ?
>
> **Trois absences ou plus = alerte haute, escalade immédiate au CEO et à Sam.** Un fichier de ronde de 0 octet, ou contenant un simple accusé de lancement (« je te restitue dès qu'il termine »), est une **ronde perdue** : la compter comme telle, jamais comme une ronde silencieuse.
>
> Ne jamais commencer l'audit des décisions sans avoir déclaré l'état du dispositif de reporting lui-même — c'est ce dispositif qui fournit toutes les autres données. Défense en profondeur : si le CEO tombe en même temps que moi, plus rien ne détecte le silence (cas vécu du 17/07 au 01/08, 16 jours).

---

### Proposition 5 — SUPPRIMER l'Étape 3 de `dh-suivi-execution`, ou réparer le mécanisme

**Occurrences : 4 constats + 16 contournements.** `.claude/skills-proposed/` est vide depuis sa création le 13/07 et l'a été constaté aux rondes CoS des 02, 03 et 05/08 et par l'audit DSI du 02/08. Dans le même temps, **16 des 22 skills du dispositif ont été installés en 48 heures**, tous en écriture directe dans `.claude/skills/`.

**Ce que cela signifie** : la règle non négociable de `CLAUDE.md` — *« proposition en `.claude/skills-proposed/<agent>/`, jamais d'écriture directe dans `.claude/skills/` »* — est contournée à 100 %, et l'Étape 3 du skill CoS audite chaque jour une file qui ne recevra jamais rien.

**Cause racine, vérifiée** : cinq des six directeurs (`directeur-commercial`, `-marketing`, `-customer-success`, `-delivery`, `-legal`) n'ont **pas l'outil `Write`** dans leur définition (`.claude/agents/*.md`, ligne `tools:`). Seul le `chief-of-staff` l'a. Les directeurs ne peuvent physiquement pas déposer une fiche dans la file qu'ils sont censés alimenter. Preuve corroborante : la seule demande de skill formulée cette semaine — l'étape 0 du CoS, classée HAUTE le 02/08 — n'y a jamais été déposée et n'existe toujours pas.

**Deux branches, à trancher par Sam**

- **A — Supprimer.** Retirer l'Étape 3 de `dh-suivi-execution` et la mention de `skills-proposed` dans `CLAUDE.md`. Les skills se posent par cette boucle hebdomadaire et par arbitrage direct. Assumer que la file n'a jamais servi. *Coût : 0 €, 5 minutes.*
- **B — Réparer sans donner de nouvel outil (recommandé).** Les directeurs écrivent déjà dans `deos_state`. Ajouter au schéma `RapportDirecteur` un champ facultatif `proposition_skill` `{titre, manque_constate, occurrences, texte_propose}`, et une consigne à l'Étape 3 du CoS : *« relever les champs `proposition_skill` des rapports de la journée et les matérialiser dans `.claude/skills-proposed/<agent>/` — le CoS est le seul directeur doté de l'outil d'écriture »*. Aucun curseur d'autonomie n'est touché, aucune permission élargie. *Coût : 0 €, 20 minutes.*

**Pourquoi cela mérite un arbitrage plutôt qu'un correctif silencieux** : c'est la seule règle non négociable du repo qui soit intégralement contournée, et elle porte précisément sur l'objet de cette boucle.

---

## Ce que je ne propose pas, et pourquoi

- **Les cinq recouvrements de skills** (§2) : structurels et réels, mais **zéro ronde ne les a encore chargés** — les 16 skills concernés datent de 48 heures. Une collision non vécue est une hypothèse, pas une friction. À réévaluer dimanche prochain, avec le recouvrement Customer Success en tête de liste : deux formules de santé différentes pour le même score, c'est le seul qui porte sur un calcul et non sur un thème.
- **`/backlog/TASKS_MASTER.md` périmé de trois semaines** (signalé les 07 et 09/08) : 2 occurrences, mais ce n'est pas un manque de consigne — c'est un registre que personne ne tient. Relève d'une décision, pas d'un skill.
- **L'écriture d'un agent dans `rondes/directeur-commercial-revision.json`**, qui a corrompu le fichier : 1 occurrence réelle, plus un évitement explicite côté CoS (*« ce fichier semble alimenté par un pipeline automatisé séparé »*). Anecdote pour l'instant. Si un second fichier de ronde est corrompu, cela devient une consigne de propriété des fichiers à écrire.
- **Le plafond statutaire micro-entreprise** découvert par le Marketing le 08/08 (77 700 €/an, franchise de TVA perdue avant le premier Pro) et le seuil de rentabilité Pro calculé par le Commercial le même jour (~150 abonnés, échec sous 120) : deux chiffres qui n'ont jamais été mis face à face, comme le note le brief du 09/08. C'est un arbitrage commercial urgent, pas un skill manquant — je le rappelle ici parce qu'il ne doit pas se perdre entre deux directions.

---

**Résumé pour arbitrage** : cinq propositions, toutes à 0 €. Une création (`dh-methode-de-preuve`, 24 occurrences), trois enrichissements de skills existants (score, persistance, auto-diagnostic), une suppression ou réparation à trancher. Plus un correctif d'une ligne dans `bin/evolution.sh`, sans quoi la boucle de dimanche prochain analysera de nouveau un contexte vide.
