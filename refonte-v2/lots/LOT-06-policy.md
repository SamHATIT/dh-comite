# LOT-06 — Policy Engine minimal

**Vague** A · **Dépend de** rien · **Parallélisable avec** 01, 05, 07 · **Durée** 1,5 j

## Objectif

Remplacer le contrôle par motifs textuels par un contrôle par capacité, sur les
**trois axes où le contrôle actuel est faux**.

## Pourquoi ce lot est P0

Le garde-fou actuel demande « la commande contient-elle UPDATE ? ». Or les deux outils
par lesquels le comité écrit réellement — `deos-decisions` et `deos-state` — ne
contiennent aucun de ces motifs. **Le curseur d'écriture en base n'est donc pas
appliqué.** Il existe sur le papier.

Symétriquement, le même contrôle a produit cinq faux positifs en un matin, dont le
blocage d'un correctif de sécurité validé par Sam.

> **Statut de dette : P0 — dette de sécurité connue, tolérance temporaire
> explicitement acceptée.** Le Policy Engine complet vient après. Cette formulation
> est délibérée : elle empêche qu'un compromis devienne permanent.

## Périmètre du minimal

Trois capacités seulement :

| Capacité | Outils concernés | Politique |
| --- | --- | --- |
| `db.write` | `deos-decisions`, `deos-state`, `deos-tasks`, tout `psql` non `SELECT` | niveau du curseur `ecrire_base` |
| `repo.write` | `git` dans un dépôt monté en écriture | curseur `modifier_dispositif` + branche imposée |
| `external.send` | `curl`/`wget` sortant, `sf-lead`, publication | curseur `envoyer_externe` + canal imposé |

Tout le reste passe par le garde-fou actuel, inchangé.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/policy.py` | créer — le moteur |
| `config/capabilites.yaml` | étendre — outil → capacité |
| `.claude/hooks/pretooluse-guard.sh` | modifier — déléguer les 3 capacités au moteur |
| `docs/POLICY_ENGINE.md` | créer |

## Contrat

1. Le moteur reçoit `{agent, outil, arguments}` et rend `ALLOW` ou `DENY` avec motif.
2. La correspondance outil → capacité est **déclarative**, dans le YAML. Ajouter un
   outil ne demande pas de toucher au code.
3. Le crochet appelle le moteur pour les trois capacités et conserve son
   comportement actuel pour le reste.
4. **Aucune régression** sur les douze cas de test du garde-fou existant.

## Critères d'acceptation

```bash
# 1. deos-decisions est maintenant vu comme une écriture en base
echo '{"tool_name":"Bash","tool_input":{"command":"/workspace/bin/deos-decisions status DEC-X clos --par delivery"}}' \
  | docker exec -i -e DH_DIRECTION=delivery dh-comite /workspace/.claude/hooks/pretooluse-guard.sh
# attendu : DENY — le curseur ecrire_base de delivery est a 2 (Conseille)

# 2. Le CoS, lui, passe
echo '{"tool_name":"Bash","tool_input":{"command":"/workspace/bin/deos-decisions status DEC-X clos --par cos"}}' \
  | docker exec -i -e DH_DIRECTION=chief-of-staff dh-comite /workspace/.claude/hooks/pretooluse-guard.sh
# attendu : ALLOW — son curseur est a 4

# 3. Aucune régression : rejouer les douze cas existants
bash /root/workspace/dh-comite/tests/garde-fou.sh
# attendu : 12/12
```

## Documentation à produire

`docs/POLICY_ENGINE.md` doit expliquer **pourquoi le contrôle syntaxique échoue dans
les deux sens** :

- faux négatif : un outil qui écrit sans contenir de mot-clé SQL passe ;
- faux positif : une lecture est refusée parce qu'un chemin protégé apparaît dans la
  commande — cinq cas en un matin, dans quatre directions.

Et porter la mention de dette P0 telle quelle, avec une date de réexamen.
