# Mécanismes de challenge et Strategic Yield

> Produit par **LOT-11**. Outil : `bin/challenge.py`. Interrupteur :
> `config/activation.yaml`. Migration : `migrations/2026-08-17-v2-challenge.sql`.
> Contrat : `refonte-v2/SPEC.md` §4bis et `refonte-v2/lots/LOT-11-challenge.md`.
> Dernière mise à jour : 17 août 2026.

**Implémenté et testé, mais essentiellement INACTIF à la livraison.** Principe DEOS :
on prépare et on valide tout, on active selon la situation. L'état exact de chaque
mécanisme se lit dans `config/activation.yaml`, et se rend par
`bin/challenge.py activation`.

---

## 1. Pourquoi ce lot existe

> Une organisation qui n'a que la dimension « livrer » exécute parfaitement une
> stratégie moyenne.

Et la règle commune à toutes les fiches :

> **Aucun directeur n'est uniquement responsable de son département ; tous sont
> responsables de la réussite de Digital·Humans.**

Un mandat a quatre dimensions (SPEC §4bis) : DELIVER, IMPROVE, **CHALLENGE**,
ANTICIPATE. Le comité savait produire la première. La troisième n'avait aucun
support : une hypothèse formulée en ronde vivait dans le texte du compte rendu,
c'est-à-dire nulle part. Rien ne portait son coût, rien ne disait ce qui prouverait
qu'elle est fausse, et personne ne pouvait dire six semaines plus tard si elle avait
été testée.

### Le risque que ce lot crée, et comment il est tenu

Ce lot ajoute de la **production de réflexion** au moment précis où la refonte vient
d'en supprimer. La différence est réelle — un rapport d'état répète le connu, un
challenge produit une hypothèse — mais elle ne se décrète pas. D'où trois
précautions, et elles sont mécaniques :

| Précaution | Où elle vit |
| --- | --- |
| un garde-fou qui refuse une hypothèse non testable | contrainte `challenge_testable`, et `bin/challenge.py` |
| un essai dont les sorties ne comptent nulle part | colonne `activation`, posée à l'écriture |
| un interrupteur | `config/activation.yaml`, lu fail-closed |

---

## 2. Le garde-fou — et pourquoi il existe

> **Un challenge qui ne produit pas une hypothèse TESTABLE n'est pas rendu.**

Trois champs sont exigés. Chacun répond à une façon précise de ne rien dire :

| Élément exigé | Sans quoi |
| --- | --- |
| une formulation réfutable | c'est une opinion |
| un coût d'expérimentation (temps, euros, ou les deux) | c'est un vœu |
| un critère de réfutation | on ne saura jamais si elle était fausse |

**Ce que le garde-fou empêche concrètement.** Sans lui, sept directions produisent
une hypothèse de *forme* chaque semaine : « on sous-exploite le RAG », « le
positionnement mérite d'être retravaillé ». Personne ne peut ni les tester ni les
écarter, elles s'accumulent, et le mécanisme censé créer de la pensée finit par
produire le même stock illisible que le registre avant le tri du 11/08 — 61 entrées
dont 21 inclassables.

**Il est écrit à deux endroits, et ce n'est pas une redite.** La contrainte
`challenge_testable` protège le *fait* : elle vaut pour tous les chemins d'écriture,
y compris un `psql` à la main pendant une ronde, c'est-à-dire exactement le moment où
la discipline cède. Le message de `bin/challenge.py` protège l'*agent* : une erreur
PostgreSQL n'apprend rien à une direction qui vient de passer dix minutes sur son
hypothèse — elle ne saura pas lequel des trois champs manque, ni pourquoi il est
exigé.

C'est le même dispositif que `blocage_avec_suite` sur les tâches (LOT-01) : **une
obligation vérifiable mécaniquement, pas une consigne.** Une règle demande la
coopération de celui qu'elle contraint ; un mécanisme non.

```bash
# refusé — les trois champs sont exigés, et les manquants sont nommés
bin/challenge.py soumettre delivery --hypothese "on sous-exploite le RAG"

# accepté
bin/challenge.py soumettre delivery \
  --hypothese "le RAG est sous-exploité sur les SDS" \
  --cout "2 jours" \
  --refutation "si le rappel ne monte pas de 10 points, elle est fausse"
```

---

## 3. Les trois mécanismes

### 3.1 Obligation de challenge hebdomadaire — **en essai**

Deux questions à chaque direction active, mot pour mot :

1. Quelle hypothèse actuelle penses-tu fausse, fragile ou insuffisamment exploitée ?
2. Quelle opportunité personne n'est actuellement en train de regarder ?

```bash
bin/challenge.py collecter          # qui a rendu, qui est attendu, cette semaine
bin/challenge.py liste              # les challenges rendus
bin/challenge.py statuer CHA-… --statut retenu|ecarte --par ceo --motif "…"
```

**`collecter` nomme, il ne sanctionne pas**, et sort toujours en 0. Pendant l'essai,
aucune sortie du mécanisme ne doit avoir de conséquence — sinon l'essai est déjà une
activation.

**Un challenge n'est jamais jugé par son auteur** (`statuer` est réservé au CEO et à
Sam). Une hypothèse jugée par celui qui l'a rendue ne serait jamais écartée, et le
stock ne décroîtrait pas.

**Qui est challengé.** La liste des directions actives est lue dans
`config/preflight.yaml`, là où elle est déjà déclarée et vérifiée à chaque ronde. On
ne la redéclare pas ici : deux listes de directions divergent, et c'est exactement ce
qui est arrivé au Financier le 14/08 — une fiche qui existait, une direction absente
de toutes les rondes et de la table des curseurs.

### 3.2 Strategic Challenge mensuel — **inactif**

Sept questions du CEO à chaque direction, et une règle qui prime :

> **Une direction doit pouvoir contredire le CEO et Sam.** Une contradiction
> s'accompagne de ses preuves et d'une alternative. Un comité qui confirme les
> intuitions du dirigeant ne sert à rien.

**Les sept questions ne sont pas écrites, et on ne les a pas inventées.** SPEC §4bis
et LOT-11 §2 en donnent le *nombre* et la règle qui prime, jamais le contenu. SPEC §8
impose de signaler plutôt que de combler : la liste
(`questions_strategic_challenge`) est vide dans `config/activation.yaml`, et
`bin/challenge.py strategic` refuse de tourner tant qu'elle l'est, en nommant le
point ouvert. Sept questions écrites ici auraient pris force de spécification au
premier usage.

**Ce qui est spécifié fonctionne dès aujourd'hui : la contradiction.**

```bash
bin/challenge.py contredire delivery --cible ceo \
  --sujet "la priorité donnée au socle avant le lancement" \
  --preuve "trois incidents de production en dix jours sur le même composant" \
  --alternative "geler le socle, livrer le 27, reprendre le 1er novembre"
```

Le garde-fou est le même, appliqué à l'autre forme du challenge : **contester ne
suffit pas, il faut apporter de quoi trancher.** Une contradiction sans alternative
arrête une direction sans rien mettre à la place.

Et la contradiction reste possible quand le Strategic Challenge est inactif. Ce n'est
pas une cérémonie mensuelle, c'est un droit permanent : l'interrupteur coupe les sept
questions, jamais le droit de dire non.

### 3.3 Boucle d'intelligence collective — **inactive**

Une proposition du CEO est challengée par chaque direction **sur son axe propre**,
puis synthétisée, arbitrée par Sam, exécutée, mesurée.

```bash
bin/challenge.py boucle PROP-…                 # l'interrogation, axe par axe
bin/challenge.py avis PROP-… delivery --verdict defavorable \
    --preuve "…" --alternative "…"
bin/challenge.py boucle PROP-… --synthese      # tous les avis, prêts pour Sam
bin/challenge.py repondre PROP-… --par sam --reponse acceptee
```

| Axe (LOT-11 §3) | Direction | |
| --- | --- | --- |
| exécutable | `chief-of-staff` | |
| techniquement réaliste | `delivery` | |
| vendable | `growth` | |
| économiquement viable | `financier` | |
| soutenable | `legal` | **à confirmer** |
| créateur de valeur | `customer-success` | **à confirmer**, en veille |

Les six axes sont ceux du lot, mot pour mot. **Leur rattachement à une direction n'est
écrit nulle part** : il est déduit des mandats, il vit dans `config/activation.yaml`,
et les deux rattachements discutables y sont signalés plutôt que présentés comme
acquis. Une fonction en veille garde son axe (invariant I2) ; la boucle la nomme et
ne la sollicite pas.

**Un avis défavorable exige une alternative** (contrainte
`alternative_si_defavorable`). Arrêter une proposition sans rien mettre à la place est
la version collective du blocage sans suite — l'invariant I4 appliqué à une décision
collective.

**La boucle ne duplique pas le cycle de vie d'une proposition, elle s'y branche** :
synthèse → arbitrage de Sam (`repondre`) → exécution et mesure (`etape`). Une seconde
table d'arbitrage aurait fabriqué deux vérités sur le même objet.

---

## 4. Strategic Yield

```
proposition ──► acceptée ──► expérimentée ──► résultat ──► impact
```

**Le CEO n'est pas mesuré au volume de propositions.** Ce sont les taux de passage
d'une étape à la suivante qui font l'indicateur. Un CEO mesuré au volume produit du
volume.

```bash
bin/challenge.py proposer --texte "…" [--hors-backlog]
bin/challenge.py repondre PROP-… --par sam --reponse acceptee|refusee
bin/challenge.py etape PROP-… --etape experimentee --evidence-type commit --evidence-ref abc1234
bin/challenge.py etape PROP-… --etape resultat --texte "…"
bin/challenge.py etape PROP-… --etape impact   --texte "…"
bin/challenge.py yield [--audit] [--json]
```

### Ce qui protège l'indicateur

| Règle | Mécanisme |
| --- | --- |
| **Sam juge l'acceptation** (arbitrage du 17/08) | contrainte `reponse_de_sam` : `repondue_par` ne peut valoir que `sam` |
| une étape est un **fait**, pas une déclaration | contrainte `etape_prouvee` : preuve obligatoire à partir de « expérimentée » |
| l'ordre des étapes est imposé | `etape` refuse un impact sans résultat — un passage sauté fabriquerait un taux supérieur à 1 |
| on n'efface pas ce qui gêne | déclencheurs append-only sur les trois tables |

Les trois premières lignes sont l'invariant I3 : *aucun indicateur ne se calcule sur
une donnée que la partie évaluée peut écrire elle-même*. Le Strategic Yield mesure le
CEO ; si le CEO pouvait écrire l'acceptation, il mesurerait la déclaration. La
quatrième est le même invariant par l'autre bout : il suffirait d'effacer trois
propositions refusées pour améliorer un taux d'acceptation.

### Le seuil de rappel — une proposition sans réponse n'est pas un refus

```
14 jours sans réponse  ──►  le CEO rappelle UNE FOIS
au-delà                ──►  veille : ni perdue, ni comptée comme refusée
                             sort du calcul du Strategic Yield
```

Sans cette règle, l'indicateur mesurerait **la disponibilité de Sam** plutôt que la
qualité des propositions — et le CEO serait pénalisé pour un silence qui n'est pas le
sien. Ce sont des propositions d'amélioration, pas des points bloquants : rien
n'attend derrière, et Sam y consacre le temps que leur valeur justifie.

La passe est déclenchée par `yield --audit`, elle est **idempotente** (le rappel n'est
émis qu'une fois), et `--simuler` la montre sans rien écrire. Une proposition en
veille **reste consultable et reprenable** : y répondre la fait ressortir de la veille
et la remet dans le calcul. La veille n'est pas un cimetière, c'est une file d'attente
sans échéance.

Et l'on ne met pas en veille ce qu'on n'a pas rappelé : la contrainte
`veille_apres_rappel` l'interdit en base. Sans elle, « sans réponse » deviendrait
silencieusement « sortie du calcul ».

### « — » n'est pas « 0 % »

Un taux dont le dénominateur est nul s'affiche `—`, jamais `0 %`. Un taux d'impact à
« 0 % » alors qu'aucune proposition n'a encore de résultat se lit comme un échec du
CEO ; c'est une étape que personne n'a atteinte. Même piège que sur les gabarits de
graphiques du 10/08 : **une valeur absente ne se dessine pas comme un zéro.**

---

## 5. L'interrupteur

```yaml
# config/activation.yaml
challenge_hebdomadaire:   essai     # actif | essai | inactif
strategic_challenge:      inactif
boucle_collective:        inactif
innovation_budget:        inactif
budget_innovation_pct:    12
```

| État | Effet |
| --- | --- |
| `actif` | le mécanisme tourne, ses sorties comptent dans les indicateurs |
| `essai` | le mécanisme tourne, ses sorties **ne comptent dans aucun indicateur** |
| `inactif` | le mécanisme ne tourne pas — sortie 0, rien n'est écrit |

**`essai` sert à vérifier que le dispositif fonctionne avant de lui donner du poids.**
Le régime est enregistré **sur chaque ligne au moment où elle est écrite**, et jamais
recalculé : basculer l'interrupteur en `actif` ne transforme pas rétroactivement un
essai en note. Sans cette garantie, personne n'oserait se servir de l'essai.

**Lecture fail-closed.** Une clé absente ou une valeur non reconnue vaut `inactif`, et
l'outil le signale (`bin/challenge.py activation`). Un interrupteur qu'on ne sait pas
lire vaut éteint : l'inverse allumerait un mécanisme par accident de configuration.

**Le Strategic Yield n'a pas d'interrupteur**, délibérément : une proposition
stratégique relève du mandat du CEO, pas d'un mécanisme optionnel. Ce que
l'interrupteur gouverne, c'est la *boucle* qui la challenge.

`innovation_budget` est déclaré ici et **n'est consommé par aucun code de ce lot** :
la réserve de capacité se pilote dans le tableau de bord (LOT-10). L'interrupteur
existe pour que la décision d'activation se prenne à un seul endroit ; il ne fait pas
croire que le mécanisme est branché.

---

## 6. Où vivent les données

Trois tables, créées par `migrations/2026-08-17-v2-challenge.sql`.

| Table | Contenu |
| --- | --- |
| `challenges` | hypothèses hebdomadaires **et** contradictions — deux natures, un même principe |
| `propositions` | propositions stratégiques et leurs quatre étapes |
| `avis` | un avis par direction et par proposition, sur son axe |

**Pourquoi pas dans `decisions`.** Deux raisons, aucune n'est de goût.

1. Une proposition n'est **pas un point bloquant**. La ranger en `attente_sam` la
   ferait entrer dans la file d'arbitrage. Le 10/08, huit fausses entrées
   `attente_sam` ont été reclassées pour ce motif exact : une file d'arbitrage qui se
   remplit de non-bloquants cesse d'être lue, et les vraies questions se perdent avec.
2. Le vocabulaire de `decisions.statut` appartient au LOT-03. Y ajouter `en_veille`
   modifierait un objet partagé pour un besoin qui n'est pas le sien.

**Ces tables sont un ajout au contrat du lot**, qui ne listait que trois fichiers.
Motif : le lot exige `rappele_le`, `en_veille` et un suivi sur quatorze jours — rien
de cela ne survit à la fin d'un processus. Sans table, le garde-fou redevient une
consigne et le Strategic Yield un calcul sur rien.

---

## 7. Vérification

```bash
# les garde-fous qui se vérifient sans base
bin/challenge.py --autotest

# la suite d'acceptation complète, sur une base JETABLE
createdb challenge_test
CHALLENGE_TEST_DSN=postgresql:///challenge_test tests/challenge.sh
```

`tests/challenge.sh` **refuse de tourner sur la base du comité**. Une suite qui
écrirait là fabriquerait des propositions et des challenges qui compteraient dans le
Strategic Yield : un indicateur alimenté par ses propres tests mesure ses tests.

Couverture : les cinq critères du lot, dans l'ordre du lot, plus ce que le lot exige
sans en faire un critère — le garde-fou **en base**, l'ordre des quatre étapes, la
reprise d'une proposition en veille, l'append-only, et l'axe lu depuis la
configuration. **40 cas, 40 passent** (17/08/2026).

---

## 8. Ce qui reste à trancher — signalé, pas comblé

| Point | État |
| --- | --- |
| **Délai de veille après le rappel.** SPEC §4bis écrit « au-delà → veille » sans dire au-delà de quoi. Pris au pied de la lettre, la veille tomberait le jour même du rappel, et le rappel ne servirait à rien. | `delai_veille_jours: 7` dans `config/activation.yaml` — valeur posée pour que le mécanisme soit exécutable, **à trancher par Sam**. |
| **Les sept questions du Strategic Challenge.** Leur nombre et la règle qui prime sont spécifiés, leur contenu non. | Liste vide ; `challenge.py strategic` refuse de tourner et nomme le point. |
| **Rattachement des axes `soutenable` et `créateur de valeur`.** Déduit des mandats, pas spécifié. | Déclaré et marqué « à confirmer » dans `config/activation.yaml`. |
| **Condition de bascule de l'essai vers l'actif.** Le lot dit « validation après quelques tours », sans seuil. | Non chiffré ici — l'inventer ferait passer une convenance pour une règle. |
