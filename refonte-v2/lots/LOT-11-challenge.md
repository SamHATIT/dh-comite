# LOT-11 — Mécanismes de challenge

**Vague** D · **Dépend de** 02, 07 · **Durée** 1 j

> **Implémenté et testé, mais INACTIF à la livraison.** Principe DEOS : on prépare et
> on valide tout, on active selon la situation.

## Objectif

Trois mécanismes qui empêchent le comité de devenir une machine à exécuter une
stratégie moyenne : l'obligation de challenge hebdomadaire, le Strategic Challenge
mensuel, et la boucle d'intelligence collective.

## Pourquoi ce lot est séparé

Il ajoute de la production de réflexion, alors que la refonte vient d'en supprimer.
La différence est réelle — un rapport d'état répète le connu, un challenge produit une
hypothèse — mais le risque de dérive l'est aussi. D'où trois précautions : un garde-fou
mécanique, un essai limité, et un interrupteur.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/challenge.py` | créer |
| `config/activation.yaml` | créer — l'interrupteur de chaque mécanisme |
| `docs/CHALLENGE.md` | créer |

## Contrat

### 1. Obligation de challenge hebdomadaire

Deux questions à chaque direction active :

1. Quelle hypothèse actuelle penses-tu fausse, fragile ou insuffisamment exploitée ?
2. Quelle opportunité personne n'est en train de regarder ?

**Garde-fou — refus mécanique.** La réponse n'est acceptée que si elle porte les trois
champs :

```json
{"hypothese": "...",           // formulation réfutable
 "cout_experimentation": "...", // en temps, en euros, ou les deux
 "critere_refutation": "..."}   // ce qui prouverait qu'elle est fausse
```

Si un champ manque, le challenge est **refusé** et redemandé. Sans cela, sept
directions produiraient une hypothèse de forme chaque semaine.

### 2. Strategic Challenge mensuel

Sept questions posées par le CEO à chaque direction. Et une règle qui prime :

> **Une direction doit pouvoir contredire le CEO et Sam.** Une contradiction
> s'accompagne de ses preuves et d'une alternative. Un comité qui confirme les
> intuitions du dirigeant ne sert à rien.

### 3. Boucle d'intelligence collective

Une proposition du CEO est challengée par chaque direction sur son axe propre —
exécutable, techniquement réaliste, vendable, économiquement viable, soutenable,
créateur de valeur — puis synthétisée, arbitrée par Sam, exécutée, mesurée.

### 4. Strategic Yield et seuil de rappel

Chaque proposition stratégique est suivie sur quatre étapes : acceptée, expérimentée,
résultat, impact. **Le CEO n'est pas mesuré au volume de propositions.**

**Sam juge de l'acceptation.** Ce sont des propositions d'amélioration, pas des points
bloquants : rien n'attend derrière, et Sam y consacre le temps que leur valeur
justifie.

**Mais une proposition sans réponse n'est pas un refus.** Sans cette règle,
l'indicateur mesurerait la disponibilité de Sam plutôt que la qualité des propositions.

```
14 jours sans réponse  ──►  le CEO rappelle UNE FOIS
au-delà                ──►  veille : ni perdue, ni comptée comme refusée
                             sort du calcul du Strategic Yield
```

À implémenter : un champ `rappele_le` et un statut `en_veille` sur la proposition.
Une proposition en veille reste consultable et reprenable.

## L'interrupteur

```yaml
# config/activation.yaml
challenge_hebdomadaire:   essai     # actif | essai | inactif
strategic_challenge:      inactif
boucle_collective:        inactif
innovation_budget:        inactif
budget_innovation_pct:    12
```

`essai` : le mécanisme tourne mais ses sorties ne comptent dans aucun indicateur. Il
sert à vérifier que le dispositif fonctionne avant de lui donner du poids.

## Critères d'acceptation

```bash
# 1. Un challenge sans critère de réfutation est refusé
docker exec dh-comite /workspace/bin/challenge.py soumettre delivery \
  --hypothese "on sous-exploite le RAG"
# attendu : refus, les trois champs sont exigés

# 2. Un challenge complet est accepté
docker exec dh-comite /workspace/bin/challenge.py soumettre delivery \
  --hypothese "..." --cout "2 jours" --refutation "si X alors fausse"
# attendu : accepté

# 3. L'interrupteur coupe bien le mécanisme
sed -i 's/challenge_hebdomadaire: .*/challenge_hebdomadaire: inactif/' config/activation.yaml
docker exec dh-comite /workspace/bin/challenge.py collecter
# attendu : rien, sortie 0

# 4. Le Strategic Yield suit une proposition sur ses quatre étapes

# 5. Une proposition sans réponse depuis 14 jours déclenche UN rappel, puis la veille
docker exec dh-comite /workspace/bin/challenge.py yield --audit
# attendu : les propositions en veille sont exclues du calcul, ni bonus ni malus
```

## Documentation à produire

`docs/CHALLENGE.md` : les trois mécanismes, **le garde-fou et pourquoi il existe**, et
le tableau d'activation. Porter la phrase qui fonde le lot :

> Une organisation qui n'a que la dimension « livrer » exécute parfaitement une
> stratégie moyenne.

Et la règle commune : *aucun directeur n'est uniquement responsable de son
département ; tous sont responsables de la réussite de Digital·Humans.*
