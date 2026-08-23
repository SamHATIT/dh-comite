#!/bin/bash
# Nemotron 3.5 Lightning 30B-A3B NVFP4 sur DGX Spark.
# Image derivee vllm-spark:xg024 (xgrammar 0.2.4) — voir Dockerfile.vllm-xg.
#
# Chaque option ci-dessous a ete rendue necessaire par un echec observe.
# Voir README-vllm-spark.md, section "Nemotron 3.5 Lightning".
sync
docker rm -f vllm-test 2>/dev/null
exec docker run --rm --name vllm-test --gpus all --ipc=host \
  -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e PYTHONIOENCODING=utf-8 \
  -p 8001:8000 -v ~/modeles:/modeles \
  vllm-spark:xg024 \
  vllm serve /modeles/lightning-nvfp4 \
    --served-model-name qwen \
    --host 0.0.0.0 --port 8000 \
    --max-model-len 131072 \
    --gpu-memory-utilization 0.75 \
    --default-chat-template-kwargs '{"enable_thinking": false}' \
    --structured-outputs-config.reasoning_parser nemotron_v3 \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml
