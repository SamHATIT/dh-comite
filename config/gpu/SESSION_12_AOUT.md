# Session GPU du 12/08 — protocole

> Préparé le 11/08 au soir. Sam travaille à la maison, sur second écran, Citrix en parallèle.
> **Principe : la machine travaille pendant que Sam est ailleurs. Sam n'intervient que pour arbitrer.**

## Ordre des opérations

1. **Sam** : relouer la machine Packet.ai, noter l'hôte et le port SSH s'ils ont changé.
2. **Sam** : `bash /root/bin-gpu-demarrage.sh` depuis le VPS. Le script vérifie, puis lance le
   téléchargement en tâche de fond et rend la main. **Retour à Citrix.**
3. **Pendant le téléchargement** (~66 Go) : le chantier jeu de données tourne en parallèle,
   voir plus bas. Il ne touche pas au GPU.
4. **Au retour** : relancer le même script. Il détecte le modèle présent, démarre le serveur
   et fait le contrôle de santé.
5. **Arbitrage de Sam** : lecture des résultats.

## Le modèle retenu et pourquoi

**gpt-oss-120b**, ~66 Go en MXFP4. Le point décisif : **c'est son format natif**, pas une
requantification. Sam a soulevé le 11/08 qu'en dessous de Q8 la qualité se dégrade — objection
juste, et qui écarte DeepSeek V4 Flash dont la seule variante tenant en 96 Go est un IQ2
(2 bits) obtenu par double requantification communautaire.

Apache 2.0, réputation solide sur l'appel d'outils et le raisonnement structuré, et il laisse
**30 Go de marge** sur la carte — assez pour du contexte long et pour garder l'audio chargé.

*Suppléant si le premier déçoit sur le code Apex/LWC* : Qwen3-Coder-Next 80B-A3B en Q8
(~80 Go, 3 Md actifs, 262K de contexte, conçu pour l'agentique).

**À vérifier avant lancement** : le nom exact du dépôt Hugging Face, non confirmé le 11/08.
Variable `DEPOT` en tête du script.

## Ce qui se compare

| Point de comparaison | Origine | Ce qu'on en attend |
| --- | --- | --- |
| **Gemma 4 31B** | benchmark du 10/08 | 0 sur 4 familles d'analyse. C'est le plancher |
| **gpt-oss-120b** | session du 12/08 | fait-il mieux, et de combien |
| **Sonnet 5** | rondes en production | référence de qualité, ~2,58 $ par direction |

Entrées gelées identiques pour les trois. **Ne pas comparer sur le style** : ce qui compte
est la production effective des familles d'analyse, pas l'élégance de la rédaction.

## Ce que le GPU ne servira PAS

Les rondes du comité tournent sous `claude -p`, un harnais qui ne parle que le format
Anthropic. Un serveur llama.cpp expose du OpenAI. **Sans passerelle, les rondes ne basculent
pas** — même blocage qu'identifié le 11/08 pour Terra et Luna.

Ce que le GPU peut servir aujourd'hui : le pipeline SDS/BUILD, qui a son propre routage dans
`backend/config/llm_routing.yaml` (profil `test_gpu_complet` déjà en place).

## Chantier parallèle — jeu de données du qualifieur

**Indépendant du GPU. Peut tourner pendant le téléchargement.**

### Ce qui existe au 11/08

- **112 signaux étiquetés à la main par Sam** dans `v_deos_signaux` : score de 6 à 9,
  quatre statuts. Origine : Portfolio 10 ans (37), fichier de prospection (29),
  AppExchange (18), APEC (16), annuaire public (12).
- **Aucun exemple négatif.** Tous les scores sont entre 6 et 9. Un modèle entraîné là-dessus
  apprendrait que tout est bon.
- **Table `signaux_collecte` créée le 11/08** pour la collecte brute, distincte de
  `signaux_publics` où travaille le Commercial.
- **Workflow BOAMP repointé** vers cette table. Reste à l'activer via l'interface n8n —
  la CLI refuse, le workflow n'a jamais eu de version publiée (`triggerCount=0`).

### La règle qui encadre le chantier

**Le jeu d'entraînement ne doit contenir aucune étiquette produite par un modèle de langage.**
Les conditions d'Anthropic excluent l'usage des sorties pour entraîner un modèle concurrent.
Claude Code peut écrire le code d'extraction, de normalisation et d'augmentation.
**Il ne produit pas les jugements.** Les étiquettes viennent de Sam ou de la règle métier.

### Ce qui est demandé

1. Extraire les 112 signaux et leurs étiquettes vers un format d'entraînement
   (paires entrée → verdict + score), sans passer par un modèle.
2. Écrire un script de qualification manuelle en ligne de commande : affiche un signal
   de `signaux_collecte`, Sam tranche, l'étiquette est écrite. Objectif : qualifier
   50 signaux bruts en une heure pour obtenir les négatifs manquants.
3. Documenter les critères de scoring tels qu'ils ressortent des 112 exemples —
   par analyse statistique des champs, pas par interprétation d'un modèle.

**Le bruit du BOAMP est la matière première.** Test du 11/08 : sur cinq avis remontés par
la recherche plein texte, **un seul** concernait un CRM (plateforme GRC d'Issy-les-Moulineaux).
Les quatre autres — consommables de laboratoire, traiteur, nettoyage de bâtiments — sont
exactement les négatifs qui manquent.

## Suite, hors session

- **LFM2.5-2.6B sur le VPS en CPU** (2,7 Go en Q8, 8 cœurs EPYC disponibles) pour alimenter
  les workflows n8n en permanence, sans dépendre du GPU loué à l'heure.
- **Premier candidat à la bascule : Lead Scoring.** Il envoie aujourd'hui des données de
  leads chez Google. Le basculer supprime un sous-traitant de la chaîne plutôt que d'avoir
  à le déclarer avant le 1er septembre. **Argument de conformité avant d'être un gain d'euros.**
