# Les mandats du comité — pourquoi les fiches sont écrites ainsi

**Lot** LOT-07 · **Date** 17 août 2026 · **Périmètre** `.claude/agents/`
**Remplace** des fiches qui décrivaient un périmètre, des outils et des interdits, sans
objectif. Versions d'origine dans l'historique git — voir §5.

> Tous les chemins de ce document sont **relatifs à la racine du dépôt**. Le serveur et
> un clone n'ont pas la même racine ; `/repo`, `/repo-delivery`, `/backlog` et
> `/prodlogs` sont des **points de montage du conteneur**, pas des chemins du dépôt.

---

## 1. Le défaut qu'on corrige

Aucune fiche ne contenait d'objectif. Elles disaient ce que la direction *fait*, avec
quoi, et ce qu'elle ne doit pas faire. Résultat observable : **un comportement de
tâcheron** — l'agent traite ce qu'on lui pose sur le bureau, ne découpe pas, ne signale
pas d'écart, ne propose rien, parce qu'il n'a aucun cap contre lequel mesurer ce qu'il
voit.

Trois symptômes datés, tous dans le journal :

| Date | Symptôme | Ce que l'absence d'objectif explique |
| --- | --- | --- |
| 09/08 | Sam sur le CEO : *« il fait plus le passe-plat »* | il route, il constate — il n'arbitre pas, faute de cap à défendre |
| 12/08 | rapport du CoS impeccable (score 47/100, trois écarts) qui **ne déplace aucune décision** | un rapport était le livrable ; personne n'était noté sur un résultat |
| 08→12/08 | pages légales signalées vides pendant quatre jours, sans que le constat de l'un rencontre l'inaction de l'autre | aucune direction ne portait « produit livrable » comme objectif propre |

Le CEO, lui, **n'avait pas de fiche du tout** : son mandat vivait dans
`ceo/prompt-ceo.md`, injecté par `bin/comite.sh`. Il était la seule fonction du comité
sans mandat écrit au même endroit que les autres.

---

## 2. La chaîne : mission → objectifs → initiatives

Chaque fiche est construite dans cet ordre, et l'ordre est la substance.

```
MISSION       une phrase — ce que la direction existe pour faire
   ▼
OBJECTIFS     exactement 3, datés, mesurés sur une donnée qu'elle n'écrit pas
   ▼
INITIATIVES   le backlog — et il n'a de valeur que s'il sert un objectif
```

**Pourquoi cet ordre, et pas l'inverse.** Une fiche qui commence par les initiatives
produit un exécutant : le backlog devient la fin. Une fiche qui commence par la mission
et les objectifs permet la question qui manquait — *« est-ce que ce que je fais me
rapproche de mon objectif ? »* — et donc le signalement d'écart, le découpage, la
proposition. C'est le seul changement structurel du lot ; le reste en découle.

**Exactement trois objectifs.** Deux laissent un pan du mandat sans cap ; cinq
équivalent à aucun, parce que rien n'est arbitré quand tout est prioritaire. Le nombre
est vérifié mécaniquement — voir §7.

### Les quatre dimensions

Chaque mandat porte quatre dimensions, pas seulement la première :

```
DELIVER      tenir ses objectifs opérationnels
IMPROVE      rendre son domaine plus rapide, moins cher, plus fiable
CHALLENGE    contester ce que l'entreprise tient pour acquis
ANTICIPATE   voir ce que personne ne regarde
```

**Motif :** une organisation qui n'a que la première dimension exécute parfaitement une
stratégie moyenne. Et la règle qui prime sur la hiérarchie : *aucun directeur n'est
uniquement responsable de son département ; tous sont responsables de la réussite de
Digital·Humans.*

### Le garde-fou du challenge, et pourquoi il est mécanique

L'obligation hebdomadaire de challenge tient en deux questions. Elle est refusée si elle
ne produit pas une hypothèse **testable** :

| Élément exigé | Sans lui |
| --- | --- |
| une formulation réfutable | c'est une opinion |
| un coût d'expérimentation | c'est un vœu |
| un critère de réfutation | on ne saura jamais si elle était fausse |

C'est exactement le mécanisme de `next_action` sur un blocage, et pour la même raison :
une obligation qualitative non vérifiable produit de la forme. Sept directions rendant
chaque semaine une hypothèse que personne ne lit coûterait plus que le silence.

---

## 3. Les quatre mandats actifs

| Fonction | Mission | Les trois objectifs, en un mot |
| --- | --- | --- |
| **CEO** (`ceo.md`, créé) | Tenir le cap et proposer les choix qui créent un avantage durable | contrôle exécutif · intelligence stratégique · différenciation |
| **Chief of Staff** (réécrit) | Faire que les décisions deviennent des résultats, vite et avec preuves | spécification sous 24 h · 95 % d'états terminaux · dette en baisse |
| **Delivery** (réécrit) | Construire vite une plateforme fiable, différenciante et évolutive | livrable au 27/09 · zéro critique > 24 h · vélocité d'ingénierie |
| **Growth** (`directeur-growth.md`, créé) | Transformer une plateforme intéressante en offre désirée et achetée | positionnement · pipeline qualifié · apprentissage marché |

### Ce qui est particulier au CEO

- **Strategic Yield** : il n'est pas mesuré au nombre de propositions mais à leur devenir
  — acceptée → expérimentée → résultat → impact. **C'est Sam qui juge de l'acceptation**
  (arbitré le 17/08). Une proposition sans réponse **n'est pas un refus** : rappel unique
  à 14 jours, puis mise en veille — ni perdue, ni comptée comme refusée, elle sort du
  calcul. Sans cette règle, le silence de Sam dégraderait mécaniquement le score du CEO.
- **Droit de sortir du backlog** : droit de **proposition**, pas d'initiative (arbitré le
  17/08). Il soumet, Sam valide. Précaution de départ, réexaminable.
- **Suppléance du CoS** : si le CoS est NOT READY ou indisponible, le CEO prend sa place
  momentanément et **alerte Sam**. Suppléance tracée, qui prend fin au retour du CoS.
  Motif : la validation des clôtures et l'assignation sous 24 h sont des fonctions
  critiques ; sans suppléant nommé, elles s'arrêtent sans que personne ne le décide.

### Ce qui est particulier au Chief of Staff

Il est la seule fonction qui **écrit au registre** et il est noté sur **l'état de ce
registre** : il compte un stock qu'il alimente. Faiblesse relevée en revue externe le
11/08, et conservée telle quelle dans la fiche, avec ses deux contreparties : le calcul
de ses objectifs est fait par `bin/health.py` (LOT-10) **sur les tables**, jamais repris
d'un chiffre qu'il déclare ; et il signale lui-même tout écart entre ce qu'il compte et
ce que les directions rapportent.

C'est aussi lui qui reçoit **toute alerte Preflight**, automatiquement. Sans cette règle
on obtient l'absurdité : *« tu n'as pas les moyens de travailler → voici une tâche →
travaille pour obtenir les moyens »*. Un agent bloqué par un accès manquant ne peut pas
se débloquer seul.

### Ce qui est particulier à Growth

**La fusion est temporaire, et c'est une fusion de cadence, pas de fichiers.**
`directeur-commercial.md` et `directeur-marketing.md` restent **intacts** (invariant I2) :
seule leur cadence s'arrête. Le jour de la re-séparation, il n'y a rien à reconstruire.

Le risque propre à la fusion est nommé dans la fiche : que le commercial mange le
marketing, ou l'inverse. Les objectifs O2 (pipeline) et O3 (contenus publiés) sont là
pour le rendre visible — si l'un décroche deux semaines de suite, c'est un signal de
re-séparation à remonter, pas un retard à rattraper en silence.

### Les trois mandats dormants

Écrits, **pas activés**. Cadence à zéro, condition de réveil inscrite dans la fiche.

| Fonction | Mission | Condition de réveil |
| --- | --- | --- |
| Financier | Donner la visibilité économique nécessaire pour investir intelligemment | bascule sur matériel dédié ; régime cible : à la demande + passe hebdomadaire |
| Juridique | Aller vite sans créer de dette juridique qui bloquera la croissance | à la demande |
| Customer Success | Faire de chaque client une preuve que le produit crée une valeur mesurable | **au premier client** |

Leur corps d'origine est **conservé intégralement** sous le titre « Le texte d'origine » :
il porte des règles acquises et datées qui restent valables. Seul un en-tête V2 (mission,
objectifs, challenge suspendu, activation) a été ajouté au-dessus.

**La Finance garde un droit permanent de challenger la tarification**, même en veille.
C'est la seule exception : un prix faux ne se voit nulle part ailleurs avant plusieurs
mois.

*Principe DEOS : on prépare et on valide tout, on active selon la situation.* Le motif
est d'éviter tout effet de bord avant le lancement, tout en ayant la certitude que le
mécanisme fonctionne le jour où on l'active.

---

## 4. Droits sur un objectif — et pourquoi un agent ne peut jamais en modifier un

| Acteur | Droit |
| --- | --- |
| Sam | crée, modifie, supprime |
| CEO | propose, avec motif |
| Chief of Staff | **aucun** |
| Direction | propose, avec motif et impact chiffré |
| Agent d'exécution | **jamais** |

**Le motif, et il est plus fort qu'une question de hiérarchie.**

Un agent noté sur un indicateur et capable de modifier cet indicateur a deux moyens
d'améliorer son score : améliorer le fait, ou réécrire la mesure. Le second est
systématiquement moins coûteux. Une organisation qui laisse cette porte ouverte
n'obtient pas de la triche délibérée — elle obtient une **dérive silencieuse** des
définitions : le seuil de qualification qui s'abaisse d'un point, l'incident « critique »
qui devient « haut », l'échéance qui glisse d'une semaine. Chaque pas est défendable, et
au bout de deux mois l'indicateur ne mesure plus rien.

C'est pour ça que le droit se répartit ainsi et pas autrement :

- **le CoS n'a aucun droit**, alors qu'il séquence tout le reste : il est la fonction
  notée sur l'état du registre qu'il alimente. C'est précisément celle qu'il ne faut pas
  laisser toucher aux objectifs.
- **une direction propose avec impact chiffré** : elle a l'information de terrain, donc
  le droit de dire qu'un objectif est faux — mais avec le coût de son changement.
- **le CEO propose avec motif**, y compris hors backlog, mais Sam valide.
- **l'agent d'exécution, jamais** : il est le plus près de la mesure et le plus loin de
  l'intention.

Corollaire, écrit dans chaque fiche : un indicateur ne se mesure jamais sur une donnée
que la partie évaluée peut écrire elle-même (invariant I3). Exemples posés par ce lot :
Delivery est noté sur les vues `v_deos_*` et les logs, qu'il lit sans les écrire ; Growth
sur Salesforce et sur des URL publiées ; le CEO sur le jugement de Sam ; le CoS sur un
calcul fait par un autre programme, directement sur les tables.

---

## 5. Ce que ça remplace — et ce qui a été retiré

Les fiches réécrites ont perdu de la matière. Détail, pour qu'un lecteur qui arrive dans
trois mois sache si une absence est un oubli ou une décision.

### Conservé, avec son incident d'origine

Toutes les règles acquises et datées ont été gardées, condensées, chacune avec la phrase
qui dit pourquoi elle existe :

- la règle anti-fausse-alerte du Delivery [DH-DEL-003] ;
- « avant de conclure que rien n'a bougé, regarde l'historique » — 32 commits invisibles
  le 08/08 ;
- « tu ne rends jamais la main avant d'avoir le résultat » — deux rondes perdues, CoS le
  06/08 et Delivery le 14/08 ;
- « vérifie dans les deux bases avant d'affirmer qu'une source n'existe pas » —
  l'accusation fausse du 10/08 ;
- les deux compteurs jamais additionnés du CEO — la faute de reporting du 06/08 ;
- la règle de la ronde suivante du CoS — les pages légales vides du 12/08 ;
- « avant de demander, produis » et « toute proposition porte son coût » ;
- la réserve du CoS sur sa propre mesure — revue externe du 11/08 ;
- les trois natures d'entrée au registre — le tri de 61 → 35 du 11/08 ;
- Salesforce fait foi, avec les six valeurs exactes de `Source_DH__c` — 10/08.

### Retiré délibérément

| Retiré | Motif |
| --- | --- |
| « MISSION DU 05/08 : ton besoin pour l'interface » (4 fiches) | mission ponctuelle, échue et livrée. Une consigne datée qui reste dans une fiche est relue chaque jour comme si elle était en cours. |
| « MISSION DU 05/08 : consolidation interface (rôle DSI) » (Delivery) | idem, livrée dans `config/delivery/`. |
| Le bloc « capacités existantes » répété **cinq fois** à l'identique | condensé en un paragraphe par fiche. Cinq copies divergent dès la première correction. |
| Les listes de skills financiers du CoS, en trois paragraphes | ramenées à deux lignes utiles. Le skill porte sa propre documentation. |
| Le tableau des quatre décisions attendant Delivery sur sa branche | c'est de l'état, pas du mandat. L'état vit dans le registre ; une fiche qui porte de l'état devient fausse en trois jours. |

**Rien n'est perdu, et voici où chercher.** L'état d'avant le lot est le commit
`a3fd171` :

```bash
git show a3fd171:.claude/agents/chief-of-staff.md      # version d'origine, integrale
git diff a3fd171 -- .claude/agents/                    # tout ce que le lot change
```

Une copie locale `<fiche>.md.pre-v2` est produite au passage, par convention du dépôt.
**Elle n'est pas versionnée** : `.gitignore` exclut `*.pre-*` depuis le 14/08, avec ce
motif écrit dans le fichier — *« git assure déjà cette fonction, les versionner double le
bruit »*. Ne compte donc pas sur ces copies pour restaurer depuis un autre clone : elles
n'existent que sur la machine où le lot a tourné. C'est l'historique git qui fait foi.

Aucune fiche n'a été supprimée (invariant I2) — le dépôt en compte neuf là où il en
comptait sept.

---

## 6. Ce que ce lot signale et ne tranche pas

Quatre écarts rencontrés en écrivant les fiches. Ils y sont **inscrits comme écarts**,
avec leur destinataire. Aucun n'a été corrigé ici.

1. **Deux sources de vérité pour le CEO.** `ceo/prompt-ceo.md` (15 400 caractères,
   injecté par `bin/comite.sh`) et désormais `.claude/agents/ceo.md`. Le lot demandait la
   fiche ; il ne dit pas laquelle fait foi. Tant que les deux existent, elles peuvent
   diverger — c'est le défaut que la duplication du bloc « capacités » a déjà produit
   cinq fois. **À trancher au LOT-08** (rondes), qui touche `bin/comite.sh` et
   `bin/rondes.sh` : soit le script lit la fiche, soit le prompt devient un simple
   préambule d'exécution.
2. **Aucune ligne `ceo` ni `growth` dans la table des curseurs.** `bin/rondes.sh` déduit
   le nom de la direction du nom de l'agent (`${AGENT#directeur-}`) : il demandera
   `growth`, puis `ceo`, et n'obtiendra rien. Le repli en place — OBSERVE sur tout — est
   le bon comportement, et il rend la fonction NOT READY. C'est un défaut à corriger **en
   base**, hors périmètre de ce lot. Le même oubli a déjà coûté quatre jours au Juridique
   (06/08) et deux décisions non vues au Financier (14/08) : cette fois il est signalé
   avant. **Sam pose les deux ensemble le 17/08 — une seule correction en base.** Les
   fiches `ceo.md` et `directeur-growth.md` portent chacune l'état constaté.
   *À vérifier au même moment* : la sauvegarde des curseurs du 11/08 ne porte pas non plus
   de ligne `financier`, et le commentaire FIX-FINANCIER-001 de `bin/rondes.sh` le
   confirmait au 14/08. Non vérifiable depuis une session sans accès à la base — donc
   signalé, pas affirmé.
3. **Trois cadences en écart avec la cible de SPEC §5** : Juridique et Customer Success
   tournent tous les jours ouvrés alors que la cible les veut en veille ; le Financier
   tourne deux fois par semaine pour une passe hebdomadaire cible. Chaque écart est
   inscrit dans la fiche concernée, avec sa date et son motif d'origine. **Relève du
   LOT-08.**
4. **Point ouvert n° 2 — ce qu'un commit doit modifier pour valoir preuve.** Non tranché :
   en l'état, **un commit vide passerait**. Les fiches du CoS et du Delivery portent la
   consigne de citer ce que le commit change (`git show <sha> --stat`) et d'ouvrir l'écart
   en `attente_sam` en citant ce point — **sans fabriquer de critère**.
5. **Une contradiction entre le lot et le contrat global, résolue en faveur du contrat.**
   `lots/LOT-07-fiches.md` présente la limite du droit du CEO à sortir du backlog comme un
   « point ouvert n° 8 » ; `SPEC.md §8` indique que ce point **a été tranché le 17/08** —
   c'est un droit de proposition soumis à Sam. La SPEC étant le contrat global, c'est cette
   version qui est écrite dans `ceo.md`. Signalé parce qu'un lecteur qui n'ouvre que le lot
   croirait la question encore ouverte.

Et trois points ouverts de SPEC §8 sont inscrits nommément dans les fiches concernées,
avec l'interdiction de les combler : **n° 1** coût cible du comité (Financier), **n° 5**
obligations réglementaires datées pendant la veille (Juridique), **n° 6 et n° 7** canal
imposé et re-séparation de Growth.

---

## 6bis. Trois arbitrages de Sam, rendus le 17/08 et intégrés ici

Ils sont **tranchés**, à la différence de ce qui précède. Chacun est inscrit dans les
fiches concernées, pas seulement dans ce document.

**1. Le curseur du CEO se pose avec celui de Growth.** Deux lignes manquantes, **une
seule correction en base**. Voir §6 point 2 : les deux fiches portent l'état constaté et
la consigne de ne pas contourner le repli OBSERVE en attendant.

**2. `couts.py` est une tâche du Delivery, pas un lot.** `bin/couts.py` et
`bin/couts-consolides.py` sont des scripts, donc du périmètre Delivery ; le Financier en
est l'**utilisateur**, pas le mainteneur. Inscrit dans les deux fiches — chez le Delivery
comme une initiative, chez le Financier comme une limite de périmètre.
*Pourquoi la distinction compte.* `couts-consolides.py` existe parce que le 11/08 une
estimation annonçait ~4 USD pour les rondes du matin quand le réel était 21 — facteur
cinq, de cause structurelle : chaque source a son compteur, et on en citait un seul en
croyant citer le tout. Le script **affiche ce qu'il ne mesure pas**. C'est sa propriété la
plus importante, et la fiche du Delivery porte la consigne de la préserver : un chiffre
incomplet présenté comme complet est pire qu'une absence de chiffre. Confier l'outil de
mesure à celui qui est mesuré rouvrirait exactement le trou que I3 ferme.

**3. Point ouvert n° 4 — fréquence du Preflight : CLOS. Avant chaque ronde.**
La mesure a réglé la question : **0,8 seconde pour quatre directions**. Le compromis
envisagé — un passage par jour — n'achetait donc rien et coûtait la fraîcheur du contrôle :
un accès qui tombe à 9 h 10 resterait invisible jusqu'au lendemain, alors que c'est
précisément le genre de panne qui a produit six arrêts en douze jours. Les quatre fiches
actives portent désormais la cadence dans leur section RONDE, avec sa conséquence : NOT
READY → la direction n'entre pas dans la ronde, et l'alerte part automatiquement au Chief
of Staff, **avant** que le budget de la session soit consommé.

Il reste donc **six** points ouverts sur les sept numérotés de SPEC §8 : n° 1 (coût
cible), n° 2 (ce qu'un commit doit modifier), n° 3 (concurrence sur un même périmètre),
n° 5 (obligations datées du Juridique), n° 6 (canal imposé de Growth) et n° 7 (re-séparation
de Growth). La mise à jour de `refonte-v2/SPEC.md §8` n'appartient pas à ce lot : elle est
signalée, pas faite.

---

## 7. Vérification

Commandes exécutables depuis la racine du dépôt. Aucune affirmation de ce document ne
demande d'être crue.

```bash
# 1. Les quatre fiches actives portent exactement 3 objectifs et 1 obligation de challenge
for f in ceo chief-of-staff directeur-delivery directeur-growth; do
  printf "%-24s objectifs=%s challenge=%s\n" "$f" \
    "$(grep -cE '^- O[123] :' .claude/agents/$f.md)" \
    "$(grep -c 'OBLIGATION DE CHALLENGE' .claude/agents/$f.md)"
done
# attendu : objectifs=3 challenge=1 partout

# 2. Aucune fiche supprimee (I2) : 7 anciennes + ceo + growth
ls .claude/agents/*.md | grep -vc "\.pre-"
# attendu : 9

# 3. Les trois fiches dormantes portent leur condition de reveil
for f in directeur-financier directeur-legal directeur-customer-success; do
  printf "%-32s ACTIVATION=%s\n" "$f" "$(grep -c 'ACTIVATION' .claude/agents/$f.md)"
done
# attendu : 1 partout

# 4. Commercial et Marketing intacts
git diff --stat HEAD -- .claude/agents/directeur-commercial.md \
                        .claude/agents/directeur-marketing.md
# attendu : aucune sortie

# 5. Aucun chemin absolu du depot dans les fiches
grep -rn "/workspace\|/root/workspace" .claude/agents/*.md
# attendu : aucune sortie (/repo, /backlog, /prodlogs sont des montages du conteneur)
```

**Le troisième critère du lot — « aucun objectif auto-déclaré » — est une revue
manuelle.** Elle est consignée au §4 ci-dessus : pour chacun des douze objectifs des
quatre fonctions actives, la fiche nomme la source de mesure et pourquoi la partie
évaluée ne peut pas l'écrire. Le cas le plus fragile est celui du CoS, et il est traité
explicitement plutôt que masqué.

## 8. Ce que ce lot ne fait pas

Il n'a touché **ni la base, ni le registre** : aucune sauvegarde n'était donc requise au
titre de l'invariant I6. Il ne touche **pas la plateforme** (I1). Il ne modifie **aucun
script** : les cadences, l'invocation du CEO et la création de la ligne de curseur
`growth` sont des travaux d'autres lots, listés au §6.
