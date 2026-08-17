# La boucle d'exécution

> Produit par **LOT-04**, le lot central de la refonte.
> `bin/executer-file.sh` · `bin/diagnostic-blocage.py`
> Outils appelés : `docs/OUTILS.md` · Registre : `docs/REGISTRE.md`
> Dernière mise à jour : 17 août 2026.

---

## La phrase qui fonde ce lot

> ## « Je suis bloqué » n'est pas une sortie de session.
> ## C'est un événement qui génère du travail.

Tout le reste de ce document n'est que la mise en œuvre de cette phrase.

---

## 1. Ce qui manquait

La version précédente d'`executer-file.sh` avait déjà le bon rythme. Elle prenait une
décision, la faisait traiter, recommençait — exécution plutôt que reporting, ce qui
était le diagnostic juste du 17/08 : *« à deux tâches tous les trois jours contre
quarante en file, il faudrait deux mois. »*

Mais il lui manquait le **mécanisme de persistance**. Le scénario qui ramène à la V1
restait ouvert, et il est banal :

```
tâche → difficulté → « je suis bloqué » → fin de session → rapport
```

Rien ne forçait la difficulté à produire autre chose qu'un constat. L'agent était de
bonne foi : il *disait* son blocage. Simplement, le dire ne créait rien — pas de
tâche, pas de porteur, pas de date. Le lendemain, personne ne reprenait, parce que
rien n'était à reprendre : le blocage vivait dans un journal.

---

## 2. Le cœur du lot : la réconciliation

C'est le seul mécanisme réellement nouveau, et il tient en une idée :

> **La boucle ne croit pas le compte rendu. Elle relit l'état en base.**

Après chaque appel d'agent, la boucle compare ce qu'elle attendait à ce qui existe :

| État lu en base | Interprétation |
| --- | --- |
| `done` / `valide` | l'agent a déclaré, avec preuve. Rien à faire. |
| `blocked` / `failed` | l'agent a déclaré. La contrainte garantit déjà la suite. |
| `a_faire` / `en_cours` | **l'agent n'a rien déclaré** — et c'est ici que tout se joue |

Dans le troisième cas, **la boucle déclare à sa place** : elle diagnostique le compte
rendu, en déduit `next_action` et `next_owner`, et pose l'état.

Un agent ne peut donc plus terminer sur une difficulté sans laisser de suite —
**y compris en ne faisant rien du tout.** C'est la différence entre une règle et un
mécanisme : une règle demande la coopération de celui qu'elle contraint.

Le cas testé le plus parlant : un agent qui ne renvoie **rien**. Le blocage posé est
alors :

```
blocker     : l'agent n'a rien declare
next_action : qualifier le blocage et le reassigner
next_owner  : chief-of-staff
```

Rien n'est perdu, rien n'est inventé, et quelqu'un a la main.

---

## 3. Les états de fin de session

| État | Suite obligatoire |
| --- | --- |
| `DONE` | preuve → `propose_cloture` → tâche suivante. **Seul état qui n'engendre rien.** |
| `BLOCKED` | `blocker` + `next_action` + `next_owner`, déterminés par le diagnostic |
| `FAILED` | `attempt_count++`, budget d'échec, `retry_at` posé |
| `NEEDS_DECISION` | escalade, crée l'entrée `attente_sam` liée |
| `TIMEBOX_EXPIRED` | la tâche retourne dans la file avec son avancement. **Pas un échec.** |

> **Quatre ou cinq ?** Le lot annonce « quatre états » et son tableau en liste
> **cinq** : `SPEC §2` en définit quatre, `TIMEBOX_EXPIRED` n'apparaît que dans
> LOT-04. Les cinq sont implémentés — un dépassement de temps ou de budget n'est ni
> un échec ni un blocage, et le confondre avec l'un des deux fausserait
> `attempt_count`. À corriger dans le texte du lot. *(Même nature que l'écart
> neuf/dix statuts relevé par LOT-01.)*

### Pourquoi `TIMEBOX_EXPIRED` n'est pas un échec

Une tâche interrompue par la fin du temps imparti **n'a pas échoué** : elle n'a pas
fini. La compter comme un échec incrémenterait `attempt_count`, déclencherait le
budget d'échec, et enverrait au Chief of Staff une tâche parfaitement saine dont le
seul tort est d'être longue. La boucle la laisse donc en `en_cours`, sans compteur,
et elle sera la plus ancienne due au tour suivant.

---

## 4. Le diagnostic de blocage — routage

`bin/diagnostic-blocage.py` tient la table de `SPEC §2.1` :

| Nature | `next_action` | `next_owner` |
| --- | --- | --- |
| technique | créer la tâche corrective | la direction elle-même |
| permission / accès | vérifier le Preflight, ouvrir le droit | `chief-of-staff` |
| information manquante | recherche assignée | la direction elle-même |
| décision nécessaire | escalade | `ceo`, puis `sam` |
| dépendance d'un autre agent | tâche assignée | l'autre direction |
| *indéterminé* | qualifier le blocage et le réassigner | `chief-of-staff` |

### L'ordre des tests n'est pas alphabétique

On cherche **d'abord ce que l'agent ne peut pas résoudre seul** — permission,
arbitrage, dépendance — et seulement ensuite ce qui lui revient.

Tester « technique » en premier attraperait presque tout : un refus de droit produit
lui aussi une erreur, un message d'échec, parfois une trace. On classerait alors en
technique un blocage que la direction ne peut pas lever, et on lui renverrait le
travail — **le défaut exact que le routage doit empêcher.**

Vérifié : `erreur : permission denied lors du git push` est classé **permission**, pas
technique.

C'est `SPEC §3.1`, le paradoxe du Preflight, appliqué à chaque blocage : sans ce
routage on produit « tu n'as pas les droits pour travailler → voici une tâche →
obtiens les droits ».

### Ce que le diagnostic n'est pas

Ce n'est **pas un juge**. Il ne dit pas si le blocage est légitime, il ne note
personne. Il lit un compte rendu et en déduit un **acheminement**. En cas de doute il
ne devine pas : il route vers le Chief of Staff, dont c'est précisément le mandat.

Les indices textuels sont volontairement larges. Rater un blocage de permission coûte
plus cher qu'en sur-détecter un : un faux positif envoie la suite au CoS, qui
requalifie ; un faux négatif renvoie à l'agent un travail qu'il ne peut pas faire, et
la tâche tourne.

---

## 5. Deux tables de routage, à ne pas confondre

C'est l'erreur que la première version de cette boucle a commise, et elle est
instructive.

| | Table | Ce qui détermine la suite |
| --- | --- | --- |
| **Blocage** | `SPEC §2.1` | la **nature** de l'obstacle |
| **Échec** | `SPEC §2.2` | le **rang de la tentative** |

La boucle passait le résultat du diagnostic à `deos-tasks fail`, qui écrasait le
budget d'échec. Une 2ᵉ tentative se voyait donc poser « créer la tâche corrective » au
lieu de « changer d'approche, cause à nommer » — et l'opérateur ne pouvait plus
comprendre pourquoi la tâche avait cessé de revenir.

**Correction :** sur le chemin `FAILED`, la boucle ne passe ni `--next-action` ni
`--next-owner`. `deos-tasks` tient `§2.2` ; on le laisse faire.

### Le budget d'échec, vu depuis la boucle

| Tentative | Comportement | Trace au journal |
| --- | --- | --- |
| 1re | reprise directe à +10 min | `1 essai(s), suite chez delivery : reprise directe` |
| 2e | **reprise suspendue** tant que la cause n'est pas nommée | `changer d'approche — cause a nommer` + `reprise SUSPENDUE` |
| 3e | passe au `chief-of-staff`, plus de reprise automatique | `suite chez chief-of-staff : arbitrage du CoS` |

La boucle **dit explicitement** quand la reprise est suspendue, avec la commande qui
la relance. Sans cela, la tâche disparaîtrait de la file sans que personne sache
pourquoi — un silence de plus, là où on en supprime un.

---

## 6. La file se traite par ancienneté

```sql
ORDER BY cree_le, id LIMIT 1
```

**La plus ancienne due, pas la plus facile.** Sinon la file se trie toute seule par
confort et les dossiers lourds ne bougent jamais. C'est le mécanisme qui produit les
« quarante décisions accordées de plus de trois jours » — chacune évitée pour une
bonne raison, quarante fois de suite.

Est « due » une tâche qui est :

- `a_faire` ou `en_cours` (y compris reprise d'une session interrompue) ;
- `failed` dont `retry_at` est dépassé — **la reprise, `SPEC §2.3`** ;
- `blocked` dont le `next_owner` est cette direction : la suite lui a été assignée.

Une tâche déjà vue dans la session courante est exclue, sans quoi une tâche qu'on
vient de bloquer serait reprise indéfiniment.

### La reprise est ce qui fait un moteur

> Une tâche `failed` dont `retry_at` est dépassé revient **d'elle-même**.

Sans cela, une tâche bloquée en premier est oubliée pendant que les suivantes
s'exécutent. C'est ce qui distingue un moteur d'exécution d'un ordonnanceur, et c'est
ce que la V1 n'avait pas.

---

## 7. Le budget de session

Budget de session = **somme des budgets des tâches traitées**. Tolérance 10 %.
Au-delà, la session s'arrête en `TIMEBOX_EXPIRED` **et produit une escalade**.

L'escalade n'est pas une ligne de journal. Elle est **posée dans la file** : la tâche
suivante est bloquée avec `next_owner = ceo` et le motif chiffré.

```
budget de session depasse : 0.6000 USD pour 0.5000 budgetes (tolerance 10 %)
  ESCALADE -> ceo : budget de session depasse (0.6000 USD pour 0.5000)
=== TIMEBOX_EXPIRED — 1 tache(s), 0.6000 USD pour 0.5000 budgetes ===
```

Une escalade tracée seulement dans un journal n'est pas une escalade : c'est une
note. Posée dans la file, elle apparaît au CEO comme du travail qui lui revient.

> **Une escalade n'est pas un refus. C'est une demande d'arbitrage à qui peut
> engager davantage.** Voir `docs/OUTILS.md §2` pour la récursion complète.

---

## 8. Trois défauts trouvés en validation

Ils méritent d'être écrits : les trois sont des cas où le mécanisme censé protéger
échouait précisément dans la situation qu'il devait couvrir.

### 8.1 Le diagnostic se bloquait sur le silence

`diagnostic-blocage.py` testait la *vérité* de la chaîne : `--texte ""` retombait donc
sur `stdin`, qui n'est pas redirigé quand la boucle l'appelle. Le processus attendait
indéfiniment.

Or **un compte rendu vide est exactement le cas que ce module existe pour
rattraper** : l'agent qui s'arrête sans rien dire. Le mécanisme censé attraper le
silence se bloquait dessus. Un `--texte` vide n'est pas un `--texte` absent.

### 8.2 Une base injoignable se lisait comme une file vide

Toutes les requêtes renvoyaient du vide, la boucle ne trouvait aucune tâche due, et
concluait `TERMINEE — 0 tâche`. **Une panne se lisait comme une fin de session
normale** — le pire des rapports : faux, rassurant, indistinguable du vrai.

La boucle vérifie désormais que la base répond avant de conclure quoi que ce soit, et
sort en code 1 sinon.

*Une file vide et une panne ne se ressemblent que si personne ne vérifie laquelle des
deux c'est.*

### 8.3 Les deux tables de routage confondues

Voir §5.

---

## 9. Pourquoi le script n'utilise pas `set -e`

Une erreur ne doit pas interrompre la boucle. Avec `set -e`, la première commande qui
échoue termine la session — **le défaut corrigé ici, reproduit au niveau du shell.**
Chaque étape gère son échec et on continue. C'est délibéré, et c'est la seule raison.

---

## 10. Ce qui reste ouvert

| Point | État |
| --- | --- |
| `SPEC §8.2` — ce qu'un commit doit modifier pour valoir preuve | **non tranché.** La boucle accepte `done --evidence-type commit` sans vérifier que le commit change quoi que ce soit. Un commit vide passerait. C'est le lot qui rencontre ce point de plein fouet : il valide des preuves à chaque tour. Signalé, pas décidé. |
| L'avancement d'une tâche `TIMEBOX_EXPIRED` | aucune colonne ne porte un avancement partiel. Il vit dans le journal de session. La tâche revient entière au tour suivant. |
| `SPEC §8.3` — concurrence entre agents sur un même périmètre | ouvert. Deux sessions lancées sur la même direction prendraient la même tâche : aucun verrou n'est posé. |
| `SPEC §8.4` — fréquence du Preflight | ouvert. La boucle ne l'appelle pas ; c'est le périmètre de LOT-05 et LOT-08. |

---

## 11. Vérification

```bash
# 1. Une difficulte n'arrete pas la session
bin/executer-file.sh delivery 3 20
# attendu : les 3 traitees, la 1re en failed avec next_action

# 2. Aucune tache bloquee sans suite
psql "$COMITE_DB_DSN" -tAc "SELECT count(*) FROM tasks
  WHERE statut IN ('blocked','failed')
    AND (blocker IS NULL OR next_action IS NULL OR next_owner IS NULL);"
# attendu : 0, toujours

# 3. La reprise fonctionne
psql "$COMITE_DB_DSN" -c "UPDATE tasks SET retry_at = now() - interval '5 min' WHERE id='TASK-X';"
bin/executer-file.sh delivery 3 20        # attendu : « reprise : 1 tache(s) »

# 4. Le depassement de budget escalade au lieu de continuer
# attendu : TIMEBOX_EXPIRED + tache suivante bloquee vers le ceo
```

La boucle exécute elle-même le contrôle 2 en fin de session, et alerte si l'invariant
est violé — *un invariant qu'on n'observe jamais est un invariant qu'on croit tenu.*

### Résultat — 17 août 2026

Instance PostgreSQL locale jetable, migrations LOT-01 et LOT-02 appliquées. Les appels
d'agent sont simulés par un `claude` de substitution qui reproduit chaque comportement
— déclarer une fin, se taire, échouer techniquement, buter sur un droit, demander un
arbitrage. **Le modèle n'est pas appelé : c'est la boucle qui est testée, pas l'agent.**

| Contrôle | Résultat |
| --- | --- |
| **1.** Difficulté non déclarée → session continue | 3 tâches traitées sur 3 |
| **1.** La tâche en difficulté porte une suite | `failed`, `next_action` posé |
| **2.** Tâches bloquées sans suite | **0** |
| **3.** Reprise d'une tâche `failed` échue | `reprise : 1 tache(s)`, reprise effective |
| **4.** Dépassement de budget | `TIMEBOX_EXPIRED` + escalade posée vers le `ceo` |
| Budget dans la tolérance | session poursuivie |
| Diagnostic — permission | → `chief-of-staff` |
| Diagnostic — décision | → `ceo` **+ entrée `attente_sam` liée créée** |
| Diagnostic — agent totalement muet | → `chief-of-staff`, sans blocage du script |
| Diagnostic — permission masquée par une erreur | classé `permission` |
| Budget d'échec sur 3 tours via la boucle | 1re reprise, 2e suspendue, 3e au CoS |
| `propose_cloture` quand toutes les tâches sont finies | posé, avec preuves agrégées |
| `propose_cloture` si une tâche reste ouverte | **non posé** |
| Base injoignable | arrêt bruyant, code 1 |
| `bash -n`, `python3 -m py_compile` | sans erreur |

> **Non appliqué en production.** Le script et le diagnostic sont produits et vérifiés
> ici ; leur mise en service suppose les migrations LOT-01 et LOT-02 appliquées.
