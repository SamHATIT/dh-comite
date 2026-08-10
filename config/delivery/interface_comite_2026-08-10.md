# Conception complète de l'interface du comité — 10/08/2026

## Statut
**Proposition du Directeur Delivery (rôle DSI), soumise à l'arbitrage de Sam.**
Conformément à DH-CRO-002 : je conçois, Sam tranche — lot par lot, pas en bloc.
Rien ci-dessous n'est engagé ; c'est la base d'un arbitrage au comité.

## Ce qu'il faut retenir

1. **Le socle existant ne se refait pas.** Six écrans tournent déjà sous `/comite/`
   dans une charte cohérente (fond sombre, laiton, JetBrains Mono) : le tableau
   de bord, le poste de pilotage, la gouvernance du curseur, l'arbitrage mobile
   (livré ce soir), les rapports par direction, les briefs quotidiens. On étend,
   on ne recommence pas.
2. **Le renversement demandé — document consulté → question posée — se fait en
   trois lots indépendants**, chacun livrable seul : graphiques (lot 1),
   questions-réponses écrites (lot 2), voix (lot 3, dépend du lot 2). Aucun des
   trois n'attend un autre pour apporter de la valeur.
3. **Deux prérequis bloquent une partie du projet, pas tout.** La mémoire du
   comité (`bin/memoire`) est cassée dans cet environnement — vérifié aujourd'hui,
   voir Réserves. La faille B2 (identifiants clients en clair) doit être close
   avant toute version orientée client DEOS — elle est en cours (DEC-2026-0810-20).
   Ni l'un ni l'autre n'empêche les lots 1 et 2 pour Sam.
4. **Ce qui est vendable à un client DEOS n'est pas ce qui sert Sam aujourd'hui.**
   Le moteur de questions-réponses (lot 2) est le même pour les deux usages ; la
   gouvernance des agents IA, le curseur d'autonomie et l'arbitrage des décisions
   sont propres à notre dispositif interne et ne se vendent pas.
5. **Le coût qui compte est le temps de Sam, pas les heures de développement.**
   Les lots 1 et 2 lui coûtent quelques minutes d'arbitrage sur des maquettes déjà
   posées ; le lot 3 (voix) lui demandera un test personnel du aller-retour réel,
   qu'aucune télémétrie ne remplace.

---

## 1. Ce qui déclenche cette conception

Sam, ce soir : six fois il a fallu qu'on lui lise un rapport qu'il aurait dû
pouvoir consulter seul. Sa demande a deux volets distincts, à ne pas confondre :
- des **indicateurs en graphique** plutôt que des tableaux à dix colonnes ;
- du **contenu en réponse à une question**, à l'oral ou à l'écran, plutôt qu'un
  cahier de cinquante pages qu'il faut qu'on lui commente.

Le document de cinquante pages ne disparaît pas : il devient une **source qu'on
interroge**, pas un livrable qu'on lit en entier (section 5).

## 2. La carte des besoins — qui a besoin de quoi

### 2.1 Sam, aujourd'hui — le besoin qui commande tout le reste

| Besoin | Aujourd'hui | Ce qui manque |
| --- | --- | --- |
| Savoir ce qui l'attend en ouvrant l'écran | `/pilotage` existe et le fait | Rien — déjà couvert |
| Arbitrer une décision en attente | `/arbitrer` existe, livré ce soir | Rien — déjà couvert |
| Situer un chiffre par rapport à un seuil (dette, cash, score) | Tableaux et texte | **Graphique** — lot 1 |
| Poser une question précise et obtenir la réponse | Aucun canal — il demande en conversation ou lit un rapport | **Q/R écrite** — lot 2 |
| Obtenir cette réponse à l'oral, en déplacement | Aucun canal | **Voix** — lot 3 |
| Échanger avec une direction en particulier | Lecture de son rapport brut (`/rapport/delivery/...`) | **Chat par direction** — lot 2b |

### 2.2 Ce qui est propre à notre usage (ne se vend pas)

Le curseur d'autonomie (`/gouvernance`), l'arbitrage des décisions du comité IA
(`/arbitrer`), la gouvernance des cinq/six directions, la dette d'exécution.
Un client DEOS n'a pas de comité de direction IA à arbitrer — il a un projet à
suivre. Ces écrans restent internes, point final.

### 2.3 Ce qui serait vendable — le même moteur, un périmètre différent

Un client DEOS pose les mêmes catégories de questions sur SON dispositif :
« où en est mon projet », « combien ça a coûté ce mois-ci », « qu'est-ce qui
bloque la livraison », « qui attend quoi de mon côté ». Le **moteur de
questions-réponses du lot 2** (catalogue de questions → requête déterministe →
réponse sourcée et datée) est directement réutilisable, scopé à son propre
périmètre de données (`v_deos_*` filtré par son `project_id`).

**Réserve qui prime sur l'enthousiasme commercial** : ouvrir une interrogation
libre sur les données d'un client suppose une isolation par tenant plus solide
que celle qui existe aujourd'hui. Ma ronde de ce matin (mission sécurité
DEC-2026-0809-05, finding B2) a établi qu'il n'existe **aucune garantie serveur**
de cloisonnement entre clients — seulement un paramètre `project_id` transmis
par l'appelant, sans filtre imposé côté base. Tant que ce chantier n'est pas
clos (accordé ce jour sous DEC-2026-0810-20, non encore vérifié exécuté), une
version client de l'interface de questions-réponses **agrandit la surface
d'exposition** au lieu de la réduire. Ne pas scoper de lot client avant preuve
de clôture de B2.

## 3. Les écrans, avec leur priorité

### Ce qui existe déjà — ne pas refaire

| Écran | Rôle | Depuis |
| --- | --- | --- |
| `/` | Tableau de bord global (poinçon de santé, loges par domaine) | 14/07 |
| `/pilotage` | Poste de pilotage (N0) : ce qui attend, décisions, cash | Récent |
| `/gouvernance` | Curseur d'autonomie : réglé vs vécu (refus tracés) | 06/08 |
| `/arbitrer` | Décisions en attente, une carte, trois boutons, mobile | Ce soir |
| `/rapports` + `/rapport/{direction}/{nom}` | Lecture des rapports markdown, rendus lisibles | — |
| `/brief/{jour}` | Brief quotidien en HTML, présentable à un client | — |

### Ce qui manque, par ordre de déploiement

**Lot 1 — Indicateurs en graphique.** Étend `/pilotage` (pas un nouvel écran) :
remplacer les nombres nus par de petits graphiques quand une valeur doit être
*comparée ou située par rapport à un seuil* — score par direction dans le temps,
dette d'exécution en jours, trésorerie vs seuil d'alerte, coûts API du mois.
Rendu serveur en image (même gabarit `charte.py` que les docx, pas de
bibliothèque JS à ajouter), un graphique à la fois sur mobile, jamais une grille
de dix vignettes. Aucun besoin de Sam au-delà d'un go sur le choix des quatre
graphiques.

**Lot 2 — Poser une question (écrit).** Un écran unique : un champ de saisie,
une réponse sourcée et datée. Détail du principe en section 4. C'est le cœur du
renversement demandé. Réutilise les API existantes (`/api/etat`,
`/api/pilotage`, `/api/gouvernance`, `/api/brief_complet`) — pas de nouvelle
source de données, un nouveau routeur par-dessus celles qui existent.

**Lot 2b — Échanger avec une direction.** Variante du lot 2, scopée à un
directeur : la question porte sur son dernier rapport (`deos_state`) et, si
`bin/memoire` est réparé (Réserve), sur son historique indexé. Dépend
techniquement du lot 2 — même moteur, périmètre restreint.

**Lot 3 — Voix dans les deux sens.** Ajoute un micro et une lecture à voix haute
sur les écrans des lots 2 et 2b, pour l'usage mobile en déplacement. Ne se
justifie pas comme écran séparé : c'est une entrée/sortie alternative sur le
moteur de questions-réponses déjà construit.

**Souhaitable, plus tard** — hors urgence de lancement : export vendable pour
client DEOS (dépend de la clôture B2, section 2.3) ; drill-down complet par
domaine au-delà des rapports bruts actuels ; historique long du `domain_score`
au-delà de 30 jours.

## 4. Le principe de réponse aux questions

### Comment ça marche, concrètement

Un **catalogue fermé de questions canoniques**, chacune reliée à une requête
déjà existante — pas un moteur qui invente une réponse. La question posée est
rapprochée d'une entrée du catalogue (correspondance simple, pas de modèle pour
cette étape) ; si elle correspond, la requête déterministe s'exécute et un
modèle économique (Haiku) met la réponse en phrase — il formate, il ne calcule
jamais le chiffre. Si aucune entrée ne correspond, la réponse est : « je ne sais
pas répondre à ça pour l'instant, voici les rapports bruts » avec un lien vers
`/rapports`. Jamais de réponse non sourcée : la règle DH-DEL-006 (aucune
affirmation sans preuve datée) s'applique à une réponse orale exactement comme
à un rapport écrit.

### Les questions que Sam pose réellement

Relevées dans les briefs et journaux des dernières semaines — ce sont les
premières entrées du catalogue, toutes déjà calculables avec les sources
existantes :

| Question posée | Source déjà en place | Nouveau ? |
| --- | --- | --- |
| Où en est le BUILD (exécution X) ? | `v_deos_executions`, `v_deos_build_phases` | Non |
| Combien ça a coûté ce mois ? | `cash_suivi` (`deos_state`), `bin/couts.py` | Non |
| Qu'est-ce qui bloque le lancement ? | décisions `attente_sam` + alertes delivery | Non |
| Qui attend quoi ? | `/api/pilotage` (décisions par direction) | Non |
| A-t-on avancé depuis le X ? | `git log` sur `/repo` (leçon du 08/08) | Non |
| Le curseur de [direction] est réglé comment ? | `/api/gouvernance` | Non |
| Une décision a-t-elle été prise sur X ? | table `decisions` + `bin/memoire` | Partiel — dépend de la mémoire (Réserve) |

Le catalogue démarre à ces sept entrées et s'étend à l'usage : chaque question
posée hors catalogue et jugée légitime devient la huitième entrée, pas un
prétexte à laisser un modèle deviner.

## 5. Ce qui reste du document

Le cahier de cinquante pages garde sa valeur là où l'interrogation ne la
remplace pas :
- **La preuve et la traçabilité** — un audit, une décision juridique, un rapport
  opposable à un tiers ou à une autorité. Une réponse orale ne se archive pas.
- **Le narratif complet** — la démonstration d'un raisonnement (pourquoi ce
  score, pourquoi cette recommandation), qu'une réponse courte compresse
  forcément.
- **Le document client** — un dossier commercial ou un audit de conformité reste
  un livrable, pas une conversation.

Ce qui devient interrogeable : toute question de statut, de chiffre ou de
blocage déjà couverte par `deos_state`, les vues `v_deos_*` ou la table
`decisions` — c'est-à-dire l'essentiel de ce qui motivait les six demandes de
lecture de ce soir.

## 6. La voix — quand oui, quand non

Faisabilité technique acquise (testée ce jour sur le serveur GPU : Whisper
chargé en 5 secondes, 2 Go ; Piper fonctionnel). Reste à borner l'usage, pas la
technique :

- **Oui** : en déplacement, mains occupées, entre deux rendez-vous — l'usage que
  Sam décrit lui-même pour l'arbitrage mobile.
- **Non** : au bureau, pour toute réponse qui se rend mieux en tableau ou en
  graphique qu'en phrase — un graphique du lot 1 ne se dicte pas à voix haute.
  Toute réponse du lot 3 doit donc rester un **résumé court à l'oral avec un
  lien vers l'écran** pour le détail, jamais un remplacement complet de l'écran.

## 7. Planning en lots — valeur, effort, temps de Sam

| Lot | Contenu | Effort | Renvoi ou développement ? | Temps de Sam requis | Avant le 01/09 ? |
| --- | --- | --- | --- | --- | --- |
| 1 | Graphiques sur `/pilotage` | S | Développement (rendu serveur, gabarit déjà existant) | Un go sur 4 graphiques | **Oui** — valeur immédiate, risque quasi nul |
| 2 | Questions-réponses écrites, catalogue de 7 | M | Développement (routeur) + renvoi (requêtes existantes) | Valider le catalogue de questions | **Oui** — répond directement au symptôme de ce soir |
| 2b | Échange par direction | M | Développement, bloqué par la mémoire cassée (Réserve) | Aucun avant réparation | Non — après le 01/09 |
| 3 | Voix (micro + lecture) | M/L | Développement, dépend du lot 2 | **Test personnel du aller-retour réel** — irremplaçable | Non — après la démo de fin août, sauf test concluant avant |
| Client DEOS | Version scopée client du lot 2 | L | Développement, bloqué par la clôture de B2 | Arbitrage sur le go commercial | Non — attend la preuve de clôture B2 |

## Réserves

- **`bin/memoire` est cassé dans cet environnement**, vérifié en tentant une
  requête pendant cette conception : `chromadb` n'est pas installé et le script
  pointe vers un chemin de dépôt absent (`/root/workspace/digital-humans-production/backend`).
  Le lot 2b (échange par direction) et une partie de la septième question du
  catalogue en dépendent. À corriger avant d'engager le lot 2b — pas un
  bloquant pour les lots 1 et 2.
- **Le round-trip voix complet n'est pas mesuré.** Ce qui est vérifié, c'est le
  chargement des modèles (Whisper 5 s, Piper fonctionnel) — pas la latence
  cumulée capture → transcription → routage → réponse → synthèse → lecture. Ne
  pas promettre le lot 3 « instantané » avant ce test bout en bout.
- **La faille B2** (identifiants clients en clair, DEC-2026-0809-05) est
  accordée pour correction (DEC-2026-0810-20) mais pas encore vérifiée exécutée
  à l'heure de cette conception. Toute version orientée client de l'interface
  attend cette preuve, pas seulement l'accord.
- **Le catalogue de questions (section 4) est un point de départ, pas une
  liste fermée.** Il s'enrichira à l'usage ; le risque à surveiller est
  l'inverse — qu'on élargisse la correspondance question→réponse au point de
  laisser un modèle répondre hors catalogue sans source. La règle « je ne sais
  pas répondre à ça » doit rester l'option par défaut, pas une exception.

## Annexe — inventaire technique du service `/comite/`

Dix-neuf routes actives dans `web/app.py`, une seule en écriture (`POST
/api/arbitrer`, livrée ce soir avec ses trois garde-fous : verdict à trois
valeurs, refus si la décision n'est plus en attente, traçabilité de l'origine).
Charte visuelle commune : fond `#0E0E10`/`#0A0A0B`, accent laiton `#C8A97E`,
police JetBrains Mono pour les écrans (Georgia pour les titres), viewport
mobile posé sur toutes les pages depuis ce soir. Les lots 1 et 2 s'insèrent
dans ce même gabarit — aucune nouvelle charte à définir.
