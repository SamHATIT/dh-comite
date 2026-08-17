# Les rituels du comité — la ronde V2

> Produit par **LOT-08**. `bin/rondes.sh` · `config/cadence.yaml`
> Preflight : `docs/PREFLIGHT.md` (LOT-05) · Mandats : `docs/MANDATS.md` (LOT-07)
> Session d'exécution : `docs/BOUCLE_EXECUTION.md` (LOT-04)
> Dernière mise à jour : 17 août 2026.

---

## 1. Ce qu'était une ronde, et ce qu'elle devient

Une ronde était un **rapport d'état du monde**. Le directeur se réveillait, décrivait
sa situation, s'arrêtait. Les sorties allaient de 500 à 15 000 caractères, et
l'essentiel s'y noyait : l'agent reprenait un contexte déjà connu, produisait des
analyses que personne n'avait demandées, et concluait rarement sur un engagement.

C'était un rythme de **reporting**, et le diagnostic du 17/08 l'avait déjà nommé :
*« à deux tâches tous les trois jours contre quarante en file, il faudrait deux
mois. »*

La ronde V2 tient en cinq questions.

---

## 2. Les cinq questions

```
1. Où suis-je par rapport à mes objectifs ?
2. Qu'est-ce qui a avancé depuis hier ?
3. Qu'est-ce qui est bloqué, et par quoi ?
4. QUELLE ACTION EST-CE QUE J'ENTREPRENDS MAINTENANT ?
5. Quelle décision humaine m'est nécessaire ?
```

### Pourquoi la question 4 change tout

Les questions 1 à 3 sont des **constats**. On peut y répondre honnêtement, avec
précision, et n'avoir rien changé. C'est exactement ce que produisait la V1 : des
rondes justes, documentées, et sans effet.

> **La question 4 transforme la ronde en engagement.**

Et l'engagement n'est pas une phrase : **l'agent la pose comme une tâche.**

```bash
bin/deos-tasks add --decision DEC-X --titre "..." \
                   --critere-fin "<vérifiable par une commande>" --owner <direction>
```

Trois conséquences, et c'est là que le mécanisme se referme :

1. **Elle entre dans la file**, donc la boucle d'exécution la reprendra (LOT-04).
2. **Elle porte un critère de fin vérifiable**, donc « c'est fait » cessera d'être
   une affirmation.
3. **L'agent en rend compte le lendemain** — la question 2 de la ronde suivante lit
   littéralement le résultat de la question 4 de la veille.

C'est ce qui relie le rituel au moteur. Sans la question 4, la ronde et la file sont
deux mondes séparés : on décrit d'un côté, on exécute de l'autre, et rien ne garantit
que ce qu'on décrit soit ce qu'on exécute.

### Les interdits sont explicites

L'invite nomme ce qui est refusé :

- le rapport d'état du monde ;
- la reprise du contexte déjà connu ;
- les analyses non demandées — **si une analyse est utile, elle devient une tâche.**

Ils sont écrits parce que l'implicite n'a pas suffi : la consigne « sois bref » a
produit des rapports de 15 000 caractères. Un plafond chiffré et une liste
d'interdits se vérifient ; une exhortation à la concision, non.

**Plafond : 3 000 caractères**, déclaré dans `config/cadence.yaml`. Un dépassement est
signalé au journal, **jamais** une ronde jetée — le travail a eu lieu, et
FIX-BGWAIT-002 a montré ce que coûte de jeter un travail fait.

---

## 3. L'enchaînement

```
PREFLIGHT ──► NOT_READY : la ronde NE SE TIENT PAS
    │                     alerte posée dans la file, assignée au CoS
    ▼
RONDE       5 questions, plafond de 3 000 caractères
    │
    ▼
SESSION     la file d'exécution — LOT-04
```

### Le Preflight passe avant chaque ronde

**Tranché le 18/08** (`SPEC §8`, table des arbitrages) : avant *chaque* ronde, pas une
fois par jour. Mesure de LOT-05 : 0,8 s pour les quatre directions actives. Une passe
quotidienne laisserait une fenêtre d'une journée pendant laquelle un montage perdu ou
une clé expirée passe inaperçu — **soit la durée exacte des pannes que le dispositif
supprime.**

### Un agent NOT READY ne rentre pas dans la ronde

Et son alerte **ne lui est jamais adressée**. Un agent privé de ses moyens ne peut pas
se les rendre (`SPEC §3.1`). `preflight.py` fournit déjà `next_action` et `next_owner`
pour chaque échec ; `rondes.sh` ne les recalcule pas, il les **pose dans la file**.

| | |
| --- | --- |
| **Décision** créée | `PREFLIGHT <direction> <date> — NOT_READY : <détails>` — la trace |
| **Tâche** créée | `Rétablir la capacité de <direction>`, owner = `next_owner` — l'assignation |
| Critère de fin | `bin/preflight.py <direction> sort en code 0` — vérifiable par une commande |

Une alerte qui ne vit que dans un journal n'est pas une alerte, c'est une note.

**La règle du paradoxe tient jusqu'au CoS lui-même** : quand c'est le Chief of Staff
qui est NOT READY, son alerte part au `ceo` (suppléance, `SPEC §4.2`). Vérifié.

**Idempotence** : une seule alerte par direction et par jour. Sans cela une panne
durable produirait une décision par ronde, et le registre deviendrait illisible au
moment précis où il doit servir.

---

## 4. La cadence

| Direction | Cadence |
| --- | --- |
| `ceo`, `chief-of-staff`, `delivery`, `growth` | **quotidienne** |
| `legal`, `financier`, `customer-success` | aucune — à la demande |

### Les fonctions en veille gardent tout

> **On prépare et on valide tout. On active selon la situation.** (`SPEC §5`)

Une fonction en veille garde sa **fiche**, son **mandat**, ses **droits** et son
**Preflight**. Seule sa cadence s'arrête. C'est l'invariant **I2**, et son motif est la
réversibilité : `growth` est une fusion *temporaire* du Commercial et du Marketing, et
leurs deux fiches sont intactes.

`rondes.sh --simulation` les affiche explicitement, pour qu'une fonction dormante ne
devienne jamais une fonction oubliée :

```
--- simulation : rondes qui se tiendraient le 2026-08-17 ---
  ceo  ->  ceo
  chief-of-staff  ->  chief-of-staff
  delivery  ->  directeur-delivery
  growth  ->  directeur-growth
--- fonctions sans cadence (fiches conservees, invocables a la demande) ---
  legal (veille, a_la_demande)
  financier (veille, a_la_demande)
  customer-success (veille, au_premier_client)
```

---

## 5. Où vit la cadence — et pourquoi pas dans `cadence.yaml`

**C'est la décision de conception de ce lot, et elle s'écarte de la lettre du
contrat.**

Le contrat de LOT-08 demandait de créer la cadence dans `config/cadence.yaml`, pour la
sortir du code. L'intention était juste, et l'historique de `rondes.sh` dit pourquoi :
le Juridique n'a figuré dans **aucune** ronde pendant quatre jours (FIX-LEGAL-001), le
Financier pendant douze (FIX-FINANCIER-001) — chaque fois parce qu'une fiche existait
sans que personne ait pensé à ajouter la ligne de `if` correspondante.

> Une fonction absente d'un fichier de configuration se voit.
> Une fonction absente d'un `if` ne se voit pas.

Mais **LOT-05 a été livré entre-temps**, et `config/preflight.yaml` déclare déjà `etat`
et `cadence` pour chaque direction. `preflight.py --lister` les expose. **L'intention du
lot est donc déjà tenue.**

Redéclarer la cadence dans `cadence.yaml` en ferait une **seconde vérité**. Deux
fichiers portant le même fait divergent — c'est précisément ce qui est arrivé à
`config/capabilites.yaml`, écrit par deux lots avec des structures incompatibles, et
séparé le 18/08 pour cette raison. Recréer le problème une semaine plus tard, sur le
fichier voisin, serait difficile à défendre.

**`config/cadence.yaml` existe donc**, et porte deux choses :

1. ce qui appartient vraiment aux rondes — plafond de sortie, plafond d'attente des
   subagents, modèle, outils supplémentaires ;
2. `source_cadence: config/preflight.yaml`, pour que **celui qui cherche la cadence la
   trouve au lieu d'en créer un doublon.**

*Écart signalé, pas silencieux. Si l'arbitrage doit être l'inverse — la cadence dans
`cadence.yaml`, et `preflight.py` qui l'y lit — c'est une modification de LOT-05, pas
de LOT-08.*

---

## 6. Trois défauts trouvés en validation

### 6.1 « Toutes les rondes ont produit un rapport » — après zéro ronde

Quatre rondes refusées par le Preflight, et le journal se terminait sur une ligne
rassurante : `controle-rondes.py` compare les rapports produits à ceux attendus, et
après zéro ronde il ne trouve rien à redire. Vrai au sens strict. **Parfaitement
trompeur.**

Le contrôle n'est plus lancé quand aucune ronde ne s'est tenue. À la place :

```
COMITE MUET aujourd'hui : aucune ronde tenue. 4 alerte(s) en file.
Le controle des rapports n'est pas lance — il n'y a rien a controler.
```

### 6.2 Un rapport d'hier présenté comme celui d'aujourd'hui

La passe de contrôle parcourait **toutes les directions actives** et lisait leur
fichier de sortie. Après une exécution où aucune ronde ne s'était tenue, elle relisait
les fichiers du tour précédent et rapportait `ceo : ronde de 4501 caracteres`.

**Un fichier qui existe ne prouve pas qu'un travail vient d'avoir lieu.** La passe ne
parcourt plus que les rondes réellement tenues dans l'exécution en cours.

### 6.3 Le contrôle de longueur criait au loup

`controle-rondes.py` signalait en dessous de **800 caractères** : sous cette longueur,
un rapport V1 n'était qu'un accusé de réception, et le signaler a rendu service — c'est
ce contrôle qui a rattrapé FIX-BGWAIT-002.

Mais une ronde V2 correcte fait 370 caractères. Elle était donc signalée « trop
court », avec pour remède suggéré de **relever le plafond d'attente des subagents** —
l'inverse de ce qu'il faut faire.

> Un contrôle calibré sur un format disparu ne mesure plus rien : il apprend seulement
> à ignorer ses alertes.

Seuil ramené à **120 caractères** — pas à zéro : une sortie plus courte ne peut pas
contenir cinq réponses, et c'est exactement ce que FIX-BGWAIT-002 a produit.

---

## 7. Un défaut corrigé hors périmètre

`bin/couts.py` levait une `ValueError` sur `--help` : il lisait `argv[1]` comme un
nombre de jours. Le Preflight de LOT-05 contrôle que chaque outil déclaré répond à
`--help`, et **cette exception rendait le CEO NOT READY en permanence** — donc aucune
ronde du CEO ne pouvait se tenir.

Corrigé ici : `--help` rend l'aide, un argument non numérique rend un usage et le code
2. *Hors des fichiers déclarés de LOT-08, signalé comme tel.* Le laisser aurait livré
un lot dont le chemin nominal ne s'exécute jamais.

**C'est le Preflight qui l'a trouvé**, deux jours après sa mise en service, sur un
script vieux de plusieurs semaines. Un outil qui ne sait pas dire ce qu'il fait est
indistinguable d'un outil cassé.

---

## 8. Ce qui reste ouvert

| Point | État |
| --- | --- |
| `SPEC §8.4` — obligations réglementaires datées du Juridique pendant sa veille | ouvert. Une obligation à date fixe ne s'accommode pas d'un régime « à la demande ». La cadence `aucune` est appliquée telle que le lot la définit. |
| `SPEC §8.5` — canal imposé de Growth | ouvert. Growth cumule Salesforce et Ghost. |
| `SPEC §8.6` — date ou condition de re-séparation de Growth | ouvert. Les fiches `directeur-commercial` et `directeur-marketing` sont conservées, ce qui rend la re-séparation possible à tout moment (I2). |
| Cadence du Financier | **écart signalé.** `SPEC §5` lui donne « à la demande **+ passe hebdomadaire** » ; le contrat de LOT-08 lui donne « aucune ». C'est le lot qui est appliqué, sans inventer la passe. Rappel : FIX-FINANCIER-001 — deux décisions assignées le 13/08 avec échéance au 15/08, qu'il n'aurait jamais vues faute de cadence. |
| Nommage `customer-success` / `cs` | divergence entre `preflight.yaml` et les scopes de `bin/deos-state`. Signalée, non corrigée ici. |

---

## 9. Vérification

```bash
# 1. Seules quatre directions tournent
bin/rondes.sh --simulation
# attendu : ceo, chief-of-staff, delivery, growth

# 2. Un agent NOT READY ne tient pas sa ronde
bin/rondes.sh
# attendu : ronde non tenue, alerte creee avec next_owner=chief-of-staff

# 3. Les rapports sont courts
jq -r '.result' rondes/ceo-$(date -u +%F).json | wc -c
# attendu : < 3000
```

### Résultat — 17 août 2026

Instance PostgreSQL locale jetable, migrations LOT-01 et LOT-02 appliquées, table
`curseurs` peuplée pour le CEO. Les appels d'agent sont simulés : **c'est
l'enchaînement qui est testé, pas le modèle.**

| Contrôle | Résultat |
| --- | --- |
| **1.** Directions quotidiennes | `ceo`, `chief-of-staff`, `delivery`, `growth` — exactement |
| **1.** Fonctions en veille affichées, fiches conservées | les 3, avec leur état |
| **2.** NOT READY → ronde non tenue | 4 sur 4 refusées |
| **2.** Alerte créée, décision + tâche | 4 alertes, tâches assignées |
| **2.** Règle du paradoxe — alerte du CoS | partie au `ceo`, pas à lui-même |
| **2.** Idempotence, seconde exécution le même jour | aucun doublon |
| **3.** Ronde tenue par une direction READY | `ceo`, 8 contrôles passés |
| **3.** Longueur du rapport | **370 caractères** (plafond 3 000) |
| Ronde au-delà du plafond | signalée, **non jetée** |
| Aucune ronde tenue | `COMITE MUET`, contrôle non lancé |
| Rapport du tour précédent | n'est plus attribué au tour courant |
| Configuration illisible | arrêt en code 1, jamais « rien à faire » |
| `bash -n` | sans erreur |

> **Non appliqué en production.** Le script est produit et vérifié ici. Sa mise en
> service suppose les migrations LOT-01 et LOT-02 appliquées, et les montages réels du
> conteneur — sans eux, les quatre directions restent NOT READY, ce qui est le
> comportement voulu.
