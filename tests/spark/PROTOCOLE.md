# Protocole de mesure — DGX Spark

> **Principe : on mesure les tâches réelles, pas des bancs d'essai publics.**
> Aucun banc ne teste Apex, ni les métadonnées Salesforce, ni le français de
> Sophie. Ce sont pourtant les trois choses qui décident.

## Ce qu'on cherche à savoir

La matrice « local ou externe » se remplit avec quatre chiffres, pas avec une opinion.

| # | Mesure | Ce qu'elle décide |
| --- | --- | --- |
| 1 | Vitesse sur un prompt long | si le pipeline SDS peut tourner en local |
| 2 | Conversations simultanées | si le palier gratuit tient — **c'est la mesure qui compte** |
| 3 | Qualité en français | si Sophie peut accueillir les visiteurs |
| 4 | Qualité sur Apex | si Diego et Zara peuvent produire du code |

## Ce qui est comparé

| Variante | Format | Taille | Exécuteur |
| --- | --- | --- | --- |
| Qwen 3.8 27B Q8_0 | 8 bits, llama.cpp | 28 Go | llama.cpp |
| Qwen 3.8 27B NVFP4 | 4 bits natif Blackwell | ~15 Go | vLLM |

**Le NVFP4 est exécuté nativement par Blackwell**, sans conversion. C'est ce qui le
distingue des formats 4 bits habituels — et ce qui justifie de le mesurer plutôt que
de supposer qu'un format plus court est forcément moins bon.

## Mesure 1 — vitesse

Un prompt représentatif d'un appel de Marcus : contexte long, sortie structurée.

```
Repère du 16/08 sur le GPU loué (RTX PRO 6000, Q8, llama.cpp) :
  46 jetons/s en génération courte
  27 jetons/s sur une sortie longue
  SDS complet : 51 minutes
```

À relever : jetons par seconde en entrée, en sortie, et délai avant le premier jeton.

## Mesure 2 — conversations simultanées

**La mesure décisive pour le palier gratuit.**

Le 16/08, avec llama.cpp réglé sur un seul flux, une requête d'essai est restée en
attente derrière le SDS pendant toute sa durée. Ce n'est pas un défaut de qualité,
c'est une file.

Protocole : 1, 2, 5, 10 puis 20 conversations lancées ensemble, chacune de longueur
comparable à un échange d'accueil. À relever pour chaque palier : le temps de réponse
du dernier servi, et le débit agrégé.

**Seuil d'acceptabilité à fixer avec Sam** — au-delà de quelques secondes d'attente,
un visiteur du site s'en va.

## Mesure 3 — qualité en français

Le prompt réel de Sophie, avec la question d'un DSI sceptique. Ce qu'on regarde :

- la langue est-elle naturelle, ou traduite ?
- respecte-t-elle les règles de confidentialité de sa fiche (ne jamais nommer un
  modèle, un fournisseur, un outil interne) ?
- la réponse est-elle utile, ou seulement polie ?

**Ce test n'a jamais pu être fait** : le 16/08 la requête est restée coincée derrière
le SDS.

## Mesure 4 — qualité sur Apex

Trois tâches réelles, tirées du projet Volta Réseaux :

1. un trigger handler bulkifié, sans requête en boucle ;
2. une règle de validation avec sa formule ;
3. un lot de champs personnalisés en métadonnées.

Repère : le 16/08, gpt-oss produisait du code correct ; Qwen en Q8 aussi, mais
seulement après désactivation de la réflexion — sans quoi il consommait tout son
budget de jetons sans jamais répondre.

## Ce qu'il ne faut pas oublier

- **Vider le cache système avant de lancer vLLM.** NVIDIA le documente pour le Spark :
  la mémoire est unifiée, donc ce que le système garde en cache manque au GPU.
  `sync && echo 3 > /proc/sys/vm/drop_caches`
- **Vérifier le contexte réellement chargé**, pas celui annoncé. Le 16/08, le fichier
  déclarait 32 768 alors que le modèle en annonçait huit fois plus, et Marcus a été
  tronqué en plein WBS.
- **Ne pas conclure sur une seule exécution.** La première charge un modèle froid.
