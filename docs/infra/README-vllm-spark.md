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
