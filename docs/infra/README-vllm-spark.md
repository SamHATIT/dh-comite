# vLLM sur DGX Spark — correctif des appels d'outils

**Etabli et verifie le 22/08/2026.** Conditionne la bascule du comite sur
inference locale : sans appels d'outils, les directions ne peuvent ni lire
ni ecrire en base.

## Le probleme

L'image `nvcr.io/nvidia/vllm:26.07-py3` embarque vLLM 0.24.0 et xgrammar 0.2.0.
Le code de vLLM importe `normalize_tool_choice`, qui n'existe qu'a partir de
xgrammar 0.2.1. Toute requete portant `tools` renvoie une 500 :

    ImportError: cannot import name 'normalize_tool_choice' from 'xgrammar'

Le chat simple fonctionne. Seuls les appels d'outils echouent — donc un test
de qualite superficiel ne le detecte pas.

**Contournement inefficace, verifie :** `--structured-outputs-config.backend
guidance` ne change rien. L'import a lieu avant que le moteur de sortie
structuree ne soit choisi. Ne pas perdre de temps dessus.

## Le correctif

Deux elements, tous deux necessaires :

1. `Dockerfile.vllm-xg` — xgrammar 0.2.4, avec `--no-deps` **obligatoire**
   (la mise a jour normale retrograde `transformers` en v4, que vLLM refuse
   au demarrage).
2. `--tool-call-parser qwen3_xml` et non `hermes`, dans le script de lancement.

## Verifie

| Test | Resultat |
|---|---|
| Appel d'outil, `enable_thinking: false` | OK |
| Appel d'outil, `enable_thinking: true`  | OK |
| Cache KV | 1 867 776 jetons |
| Chargement des poids (Qwen38-NVFP4) | 19,95 Gio, ~120 s |
| Compilation des noyaux, 1er lancement | ~180 s de plus |

Cache KV : environ **57 sequences a 32k de contexte**, ou **14 a 131k**.
Une seule instance peut donc servir le comite et les agents a contexte
profond (Emma, Marcus en E2E).

## Reconstruire

    docker build -t vllm-spark:xg024 -f Dockerfile.vllm-xg .

Archive de secours sur le Spark :
`~/images/vllm-spark-xg024-20260822.tar.gz` (~7 Go compresses, 33 Go d'image)

    gunzip -c vllm-spark-xg024-20260822.tar.gz | docker load

## Points d'attention

**Cohabitation impossible.** `--gpu-memory-utilization 0.75` reserve ~91 Go.
Un llama-server Nemotron actif occupe ~32 Go. Sur 121 Go de memoire unifiee,
les deux ne tiennent pas ensemble. Il faut arreter l'un pour lancer l'autre.

**Le thinking se regle par requete**, jamais au niveau du serveur :
`chat_template_kwargs: {"enable_thinking": false}`. Sa place est donc dans
`llm_routing.yaml`, a cote du modele — meme maille, meme logique.
Repartition retenue : SDS et analyse du comite avec raisonnement ;
BUILD, ecriture en base et chat de decouverte sans.

**Nemotron n'a aucune relance automatique.** S'il est arrete, il reste arrete.
Attention : `~/lancer-nemotron.sh` annonce `--parallel 8 --ctx-size 65536`,
alors que le montage reel du comite est `--parallel 2 --ctx-size 262144` —
deux emplacements a 131k de contexte, choisis pour la profondeur dont Emma et
Marcus ont besoin. Relancer avec le script casse ce reglage sans le dire.

Commande de retour effective :

    export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
    nohup setsid ~/llama.cpp/build/bin/llama-server \
      --model ~/modeles/nemotron/Nemotron-3-Nano-30B-A3B-Q8_0.gguf \
      --alias nemotron --host 0.0.0.0 --port 8080 --gpu-layers all \
      --ctx-size 262144 --parallel 2 -ub 2048 -b 4096 --flash-attn on --jinja \
      > /tmp/nemotron.log 2>&1 &

---

# Nemotron 3.5 Lightning — bascule du 23/08/2026

`lancer-lightning.sh`. Modele : `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4`
dans `~/modeles/lightning-nvfp4`. Brouillon DSpark telecharge dans
`~/modeles/lightning-dspark` (decodage speculatif pas encore branche).

## Pourquoi ce modele plutot que Qwen38

Ronde complete du comite, quatre directions, meme jour, meme base :

| | Sonnet 5 (API) | Qwen38 NVFP4 | Lightning + analyseur |
|---|---|---|---|
| Resultat | 4 fiches | **aucune** apres 46 min | 4 fiches |
| Duree | 4 min | abandonnee | 9 min |
| Tours | 13 a 29 | — | 3 a 25 |
| Debit | — | 32 puis 2 tok/s | 34 a 114 tok/s |
| Cache KV | — | 2 060 994 jetons | **21 000 647 jetons** |
| Cout reel | 2,56 USD | — | electricite |

**Qwen n'a pas echoue sur la qualite, il n'a pas converge.** Chaque direction
accumulait ~71 500 jetons de contexte ; le cout de l'attention croissant avec le
contexte, le debit est tombe de 32 a 2 tok/s sans qu'aucune fiche ne soit rendue.
Ni saturation memoire, ni preemption, ni bridage thermique — le modele tournait
en rond.

Lightning est hybride Mamba-2 + MoE : les couches a espace d'etats ne gardent pas
un cache proportionnel au contexte. D'ou le facteur dix sur le cache KV
(~160 sequences a 131k contre ~15) et l'absence de derive.

Poids : 17,86 Gio (Qwen : 19,95). Chargement ~120 s + ~180 s de compilation,
plus une etape `Warming up Mamba2 SSD Triton kernels` propre a cette architecture.

## Les trois options indispensables, et pourquoi

**`--structured-outputs-config.reasoning_parser nemotron_v3`** — LA plus
importante. Sans elle, la premiere ronde a « reussi » mecaniquement en produisant
**la deliberation brute du modele, en anglais, a la place des fiches** :

    "The bash commands are being blocked by the policy hook... I need to
     understand the constraints better... There seems to be a conflict."

Le modele repondait correctement ; on lisait ses brouillons au lieu de sa copie.
Le gabarit emet `<think>...</think>` ; l'analyseur range ce bloc dans
`reasoning_content`, que le harnais ignore, et ne laisse dans `content` que la
fiche. Attention : le nom d'enregistrement est `nemotron_v3`, PAS
`nemotron_v3_engine` (le nom du fichier dans `vllm/reasoning/`). La liste valide
figure dans le message d'erreur au demarrage.

**`--tool-call-parser qwen3_xml`** — `hermes` ne lit pas le format emis par
Lightning. Le modele formule pourtant l'appel correctement :

    <tool_call><function=deos_tasks_list><parameter=direction>delivery</parameter></function></tool_call>

`hermes` le laisse dans le texte ; `qwen3_xml` le convertit en `tool_calls`.
Il n'existe pas d'analyseur `nemotron` cote outils dans cette image.
Liste : `ls /usr/local/lib/python3.12/dist-packages/vllm/tool_parsers/`.

**`--default-chat-template-kwargs '{"enable_thinking": false}'`** — complementaire
de l'analyseur, pas redondant : il evite que le modele ouvre un bloc `<think>`
pour les tours simples. Les deux ensemble donnent `reasoning_content` vide et un
`content` propre.

## Defauts constates pendant le test, hors modele

- **Le garde-fou classe `deos-tasks list` et `deos-decisions list` comme des
  ecritures** et les refuse. `delivery` a brule 25 tours a contourner ce refus,
  contre 3 pour le CEO. Signale par le comite dans le brief du 22/08.
- **`bin/deos-decisions list --depuis <date>` renvoie 0 ligne** alors que des
  decisions existent a cette date. Filtre casse. Signale par `growth` le 22/08,
  confirme par `chief-of-staff` le 23/08.
- **`--served-model-name qwen`** est conserve pour que `config/cadence.yaml`
  n'ait rien a changer pendant le test. C'est trompeur : le nom dit « qwen »
  alors que Lightning tourne. A renommer si la bascule est definitive.

## Reste a faire

Brancher le decodage speculatif avec le brouillon DSpark
(`~/modeles/lightning-dspark`) — c'est lui qui porte le facteur 4 annonce par
NVIDIA. Les mesures ci-dessus sont celles du modele nu.
