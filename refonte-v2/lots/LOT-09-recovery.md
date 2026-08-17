# LOT-09 — Recovery Sprint

**Vague** C · **Dépend de** 03 · **Parallélisable avec** 04 · **Durée** 1 j

## Objectif

Trier les quarante décisions accordées et repartir d'une file propre.

## Pourquoi

Quarante décisions ouvertes, la plus ancienne a treize jours. Une partie est obsolète,
une autre déjà faite sans que rien ne le prouve, une troisième réellement en attente.
Traîner ce passif fausse tout signal — y compris le nouveau tableau de bord.

## Fichiers

| Chemin | Action |
| --- | --- |
| `bin/recovery.py` | créer |
| `docs/RECOVERY_2026-08.md` | créer — la trace du tri |

## Contrat

Pour chaque décision accordée, six questions dans cet ordre :

| Question | Action si oui |
| --- | --- |
| Plus nécessaire ? | `obsolete` avec motif |
| Déjà réalisée ? | demander la preuve, puis `propose_cloture` |
| Partiellement réalisée ? | créer les **tâches restantes** |
| Bloquée ? | nommer le `blocker`, poser `next_action` et `next_owner` |
| Mal définie ? | reformuler, ou renvoyer en `attente_sam` |
| Encore pertinente ? | créer au moins une tâche avec porteur et échéance |

### Deux étages, comme pour la détection de preuves

1. **Mécanique** : le script propose un classement, à partir des empreintes
   disponibles — commit citant la décision, clé métier en base.
2. **Relecture** : le Chief of Staff tranche. **Il ne clôt jamais sur la seule
   empreinte.**

Leçon du 17/08 : sur neuf décisions que la détection croyait faites, la relecture n'en
a validé qu'**une seule**. Les autres étaient partielles — un commit qui prépare mais
ne déploie pas, deux volets demandés dont un seul traité.

### Attention aux fausses preuves

Tout document qui **parle** des décisions ressemble à une preuve : rapports, briefs,
calendriers de suivi, fiches d'agents. La première version de la détection en trouvait
trente-cinq au lieu de six. **Seul le commit porte un travail daté et signé.**

### Interdits

- Ne jamais clore dans le doute. Une décision close sort du radar et personne n'y
  revient. Laisser traîner est moins grave que fermer à tort.
- Ne jamais marquer `refusee` ce qui est `obsolete` : ce n'est pas un jugement.

## Critères d'acceptation

```bash
# 1. Chaque décision de départ a reçu un traitement
docker exec dh-comite /workspace/bin/recovery.py --rapport
# attendu : 40 traitées, 0 sans décision

# 2. Aucune décision restée accordée sans tâche
docker exec dh-comite bash -c 'psql "$COMITE_DB_DSN" -tAc "
  SELECT count(*) FROM decisions d WHERE d.statut = :s
    AND NOT EXISTS (SELECT 1 FROM tasks t WHERE t.decision_id = d.id);" -v s="accordee"'
# attendu : 0

# 3. La file finale est de 10 à 15 décisions actives
```

## Documentation à produire

`docs/RECOVERY_2026-08.md` : **la trace décision par décision** — ce qu'elle est
devenue et pourquoi. C'est un document d'archive : dans trois mois, personne ne se
souviendra pourquoi telle décision de début août a été marquée obsolète.
