# LOT-10 — Executive Health Score

**Vague** D · **Dépend de** 01, 02 · **Durée** 1 j

## Objectif

Une vue d'entreprise, pas une accumulation de rapports.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/health.py` | créer |
| `docs/KPI.md` | créer |

## Contrat

| Composante | Poids | Source — **doit être hors de portée de l'évalué (I3)** |
| --- | --- | --- |
| Exécution | 30 % | tâches terminées / créées, dette en évolution, âge moyen |
| Objectifs | 25 % | avancement mesuré sur des faits, pas une auto-évaluation |
| Produit | 20 % | incidents ouverts, état de la chaîne, livrabilité |
| Trésorerie | 10 % | relevé consolidé des coûts |
| Pipeline | 10 % | comptes qualifiés en base Salesforce |
| Risques | 5 % | risques ouverts non traités |

### La règle qui prime

> **No self-attested KPI.** Un agent ne peut jamais être à la fois producteur et
> source de vérité de son propre indicateur.

C'est la raison pour laquelle l'évaluateur actuel a été gelé : toutes ses métriques
lisaient des champs de statut que la partie évaluée pouvait écrire.

Chaque composante doit citer sa source, et cette source doit être **une trace**
(commit, ligne écrite par un autre acteur, facture) et non une déclaration.

## Critères d'acceptation

```bash
# 1. Le score se calcule et affiche ses sources
docker exec dh-comite /workspace/bin/health.py
# attendu : score global + 6 composantes + source de chacune

# 2. Aucune composante ne lit un champ auto-déclaré
docker exec dh-comite /workspace/bin/health.py --audit-sources
# attendu : chaque source nommée, avec qui l'écrit

# 3. Le score par direction est cohérent avec le global
```

## Documentation à produire

`docs/KPI.md` : les six composantes, leurs sources exactes, et **le principe
« No self-attested KPI » énoncé comme règle générale DEOS**, pas comme précaution
locale. Citer le cas de l'évaluateur gelé.
