# Le registre des décisions — V2

> Produit par **LOT-03**. Outil : `bin/deos-decisions`.
> Schéma : `docs/MODELE_DONNEES.md` (LOT-01).
> Dernière mise à jour : 17 août 2026.

---

## 1. Pourquoi `propose_cloture` existe

La règle précédente tenait en une ligne : **seuls `cos`, `ceo` et `sam` changent un
statut.** Elle est juste dans son principe — un agent qui peut se déclarer quitte
n'est plus contrôlé, et le contrôle croisé est la seule chose qui empêche un
indicateur de mesurer une déclaration au lieu d'un fait (I3).

Elle était aussi paralysante. **Le Delivery a corrigé une décision le 15/08. Elle est
restée ouverte six jours.** Pas parce que quelqu'un doutait du travail : parce que
personne n'avait le droit d'enregistrer qu'il était fait. Le registre affichait une
décision en cours alors que le travail était terminé — et toute lecture du stock,
donc tout pilotage, s'en trouvait faussée dans le sens qui décourage.

Le goulot n'était pas le contrôle. **C'était d'avoir placé le contrôle sur le mauvais
geste.**

> **La V2 sépare *proposer* de *valider*.** Une direction peut déclarer son travail
> fini — `propose_cloture`, preuve obligatoire. Elle ne peut toujours pas le valider :
> `clos` reste à `cos`, `ceo`, `sam`. Le contrôle croisé est intact, l'attente
> disparaît.

Ce qui change concrètement : le 15/08, le Delivery aurait posé `propose_cloture` avec
son commit le jour même. La décision aurait été visible comme *finie, en attente de
relecture* — et non comme *en cours*. L'attente de validation reste, mais elle est
nommée, et `SPEC §4.3` la borne : au-delà de 24 h, alerte au CEO ; au-delà de 48 h,
remontée à Sam.

---

## 2. Les dix statuts

```
attente_sam ──► accordee ──► en_execution ──┬──► propose_cloture ──► clos
                                            ├──► blocked
                                            ├──► failed
                                            └──► needs_decision
                    refusee        obsolete
```

| Statut | Signification | Exigence |
| --- | --- | --- |
| `attente_sam` | Question ouverte adressée à Sam. **Jamais** l'enregistrement de ce qui est déjà décidé. | — |
| `accordee` | Arbitrée. Le CoS doit en tirer au moins une tâche sous 24 h. | — |
| `en_execution` | Au moins une tâche est en cours. | — |
| `propose_cloture` | L'agent a terminé et fourni sa preuve. En attente de validation. | `--preuve` |
| `blocked` | Obstacle **externe** : l'action n'a pas pu être tentée. | `--blocker`, `--next-action`, `--next-owner` |
| `failed` | L'action **a été tentée** et a échoué. | idem, plus `--erreur` recommandé |
| `needs_decision` | Attend un arbitrage humain. | `--question` |
| `clos` | Validé, avec preuve et constat de relecture. | `--preuve` |
| `refusee` | Écartée — **c'est un jugement**. | — |
| `obsolete` | N'a plus d'objet — **c'est une péremption**. | `--motif` |

> **Dix, et non neuf.** Le texte de `LOT-03` annonce « les neuf statuts » ;
> l'énumération de `SPEC §1.1` en donne dix. L'énumération fait foi. À corriger dans
> le texte du lot.

---

## 3. La matrice de droits

| Statut visé | Qui peut le poser | Pourquoi |
| --- | --- | --- |
| `propose_cloture` | la direction porteuse, **avec preuve** | elle a fait le travail, elle en atteste |
| `blocked`, `failed` | la direction porteuse | elle seule constate l'obstacle |
| `needs_decision` | la direction porteuse | elle seule sait qu'elle est au bout de son mandat |
| `clos` | `cos`, `ceo` (suppléance), `sam` | **le contrôle croisé** : on ne valide pas son propre travail |
| `obsolete`, `refusee` | `cos`, `ceo`, `sam` | ce sont des arbitrages, pas des constats |
| `accordee`, `attente_sam` | `ceo`, `sam` | ce sont des actes de direction |
| `en_execution` | `cos`, `ceo`, `sam` | **inchangé** — voir §6.2 |

L'outil refuse avant la base, avec un message qui dit *pourquoi* :

```
$ deos-decisions status DEC-X clos --par delivery
REFUS: clos reste reserve a cos/ceo/sam — une direction PROPOSE
       (propose_cloture), elle ne valide pas
```

### Ce que l'outil refuse aussi

| Refus | Motif |
| --- | --- |
| `propose_cloture` sans preuve | proposer sans preuve, c'est **déplacer** l'attente, pas la lever |
| `obsolete` sans motif | sinon `obsolete` devient la sortie commode de ce qu'on ne veut pas arbitrer |
| `blocked`/`failed` sans les trois champs | I4 — un blocage sans suite est invisible, il ne repart jamais |
| `needs_decision` sans question | une escalade sans question formulée n'est pas une escalade |
| décision inconnue | voir §6.4 |
| statut inconnu | la base le refuserait ; l'outil le dit mieux |

---

## 4. `needs_decision` crée l'entrée liée

Poser `needs_decision` ne suffit pas : la question doit **arriver à Sam**. L'outil crée
donc automatiquement une décision `attente_sam` :

```bash
$ deos-decisions status DEC-Z needs_decision --par delivery \
    --question "faut-il du materiel dedie ou rester en variable ?"
OK: DEC-Z → needs_decision (par delivery) — question posee a Sam : DEC-2026-0817-01
```

L'entrée créée porte `origine = delivery`, `porte_sur = DEC-Z`, et un texte qui
**contient l'identifiant source** — de sorte que le lien se retrouve aussi bien par la
colonne que par une recherche textuelle.

**Les deux écritures sont une seule transaction.** Une décision qui attend un arbitrage
sans que la question soit posée serait une attente que personne ne voit — exactement
ce que le statut sert à éviter. Si l'insertion échoue, le changement de statut est
annulé avec elle.

---

## 5. `refusee` et `obsolete` ne sont pas la même chose

| `refusee` | `obsolete` |
| --- | --- |
| **Un jugement.** Quelqu'un a examiné et écarté. | **Une péremption.** Le contexte a changé. |
| Dit quelque chose sur la proposition. | Ne dit rien sur la proposition. |

**Ce que coûterait la confusion.** Sur la quarantaine de décisions ouvertes, une part
n'a plus d'objet — le report du lancement au 1er octobre en périme mécaniquement
plusieurs. Les marquer `refusee` **salirait le signal** : on lirait ensuite un taux de
refus élevé et on en conclurait quelque chose de faux sur la qualité de ce qui est
proposé, alors que rien n'a été jugé. Le Recovery Sprint (LOT-09) a besoin des deux
sorties, distinctes.

Symétriquement, `obsolete` ne doit pas devenir la porte de sortie de ce qu'on ne veut
pas arbitrer. D'où le `--motif` obligatoire.

---

## 6. Décisions d'implémentation, et ce qui reste ouvert

### 6.1 « La direction porteuse » n'est pas définie — avis, pas refus

`SPEC` et `LOT-03` disent « la direction porteuse » sans dire ce qui la désigne. Trois
lectures possibles : l'`origine` de la décision, le propriétaire d'une de ses tâches,
ou toute direction. Elles divergent dans un cas banal — une décision **ouverte par le
CEO et exécutée par le Delivery**.

**Non tranché ici.** L'outil accepte toute direction reconnue et **signale** l'écart
quand `--par` n'est ni l'origine ni le porteur d'une tâche de la décision :

```
AVIS: legal n'est ni l'origine de DEC-Y ni le porteur d'une de ses taches
```

Refuser aurait recréé le goulot que le lot supprime, sur une règle que personne n'a
écrite. Le durcir plus tard est trivial ; débloquer un refus injustifié coûte des
jours — c'est la leçon du 15/08.

### 6.2 `en_execution` est absent de la matrice — laissé inchangé

La matrice de `LOT-03` couvre neuf statuts et **ne dit rien de `en_execution`**. Le
comportement précédent est donc conservé tel quel : `cos`, `ceo`, `sam`. Aucune
invention.

À noter pour LOT-04 : si la boucle d'exécution doit faire passer une décision en
`en_execution` quand une direction démarre une tâche, il faudra ouvrir ce droit. **À
trancher à ce moment-là.**

### 6.3 Le motif d'`obsolete` va dans `porte_sur` — dette assumée

Il n'existe pas de colonne `motif`. Le motif d'un refus est déjà rangé dans
`porte_sur` par l'outil existant ; `obsolete` suit la même convention pour ne pas
créer une seconde façon de faire la même chose. **Une colonne `motif` serait plus
juste** — c'est une dette, pas un choix de conception. Elle n'a pas été créée ici :
LOT-03 n'a pas de budget DDL et LOT-01 est clos.

### 6.4 Trois défauts corrigés en passant

Ils touchent des lignes que ce lot modifiait, et deux d'entre eux sont des
conséquences directes de ce qu'il ajoute.

**Un identifiant erroné passait pour un succès.** `UPDATE ... WHERE id='DEC-TYPO'` ne
touche aucune ligne et ne produit aucune erreur : l'outil affichait `OK`. Une faute de
frappe ressemblait à un changement de statut. L'existence de la décision est
désormais vérifiée d'abord.

**La validation effaçait le proposeur.** `propose_cloture` inscrit `propose_par` dans
la preuve — aucune colonne ne porte cette information. Mais `clos` écrivait
`preuve = <nouvelle valeur>`, ce qui écrasait la trace : la chaîne
proposition → validation perdait son premier maillon au moment même où elle se
refermait. La preuve est maintenant **fusionnée**, et `clos` y ajoute `valide_par` et
`valide_le`. Une décision close porte donc son histoire complète :

```json
{
  "commit":      "abc1234",
  "propose_par": "delivery",
  "propose_le":  "2026-08-17T12:39:30+00:00",
  "constat":     "file vide, verifie le 17/08",
  "valide_par":  "cos",
  "valide_le":   "2026-08-17T12:39:30+00:00"
}
```

**Un blocage résolu restait affiché.** Une décision passée de `failed` à
`propose_cloture` continuait de porter `blocker: api muette` : un blocage fantôme,
qu'un lecteur croit actif. Sortir de `blocked`/`failed` efface donc `blocker`,
`next_action` et `next_owner`. `attempt_count` et `last_error` sont **conservés** : ce
sont des faits passés, pas un état courant — et le nombre de tentatives est
précisément ce qu'on veut encore savoir après coup.

### 6.5 Toujours ouvert

| Point | État |
| --- | --- |
| Preuve obligatoire sur `propose_cloture` **en base** | l'outil l'exige ; la contrainte `clos_avec_preuve` ne couvre que `clos`. L'étendre modifierait une contrainte hors du périmètre de ce lot. |
| `SPEC §8.2` — ce qu'un commit doit modifier pour valoir preuve | **non tranché.** Un commit vide passerait aujourd'hui, à `propose_cloture` comme à `clos`. Signalé, pas décidé. |

---

## 7. Vérification

```bash
# 1. Une direction peut proposer une cloture
deos-decisions status DEC-X propose_cloture --par delivery --preuve '{"commit":"abc1234"}'
# attendu : OK

# 2. Elle ne peut pas clore
deos-decisions status DEC-X clos --par delivery
# attendu : refus, code 2

# 3. Une proposition sans preuve est refusee
deos-decisions status DEC-Y propose_cloture --par delivery
# attendu : refus, code 2

# 4. needs_decision cree bien l'entree liee
deos-decisions status DEC-Z needs_decision --par delivery --question "faut-il X ou Y ?"
psql "$COMITE_DB_DSN" -tAc "SELECT count(*) FROM decisions
  WHERE statut='attente_sam' AND texte ILIKE '%DEC-Z%';"
# attendu : 1
```

### Résultat — 17 août 2026

Instance PostgreSQL locale jetable, schéma `db/init/01_schema.sql` + dérive (`demo`,
`mode_demo`) + migration LOT-01.

| Contrôle | Résultat |
| --- | --- |
| Les 4 critères officiels du lot | **passés** |
| Matrice : `cos` ne pose pas `accordee`, `ceo` oui | conforme |
| Matrice : `delivery` ne pose pas `obsolete` | refusé |
| `obsolete` sans motif / `blocked` sans les 3 champs | refusés |
| `failed` incrémente `attempt_count`, garde `last_error` | conforme |
| Décision inconnue / statut inconnu / `--par` manquant | refusés |
| AVIS quand `--par` n'est pas porteuse | émis, non bloquant |
| Chaîne `failed → propose_cloture → clos` | preuve complète conservée |
| Non-régression `add` (action, acquis, acquis sans preuve) | conforme |
| Non-régression `list` | conforme |
| `bash -n` | sans erreur |

> **Non appliqué en production.** L'outil est écrit et vérifié sur instance locale.
> Il suppose la migration LOT-01 appliquée : sans les colonnes `blocker`,
> `next_action`, `next_owner` sur `decisions`, `blocked` et `failed` échoueraient.
