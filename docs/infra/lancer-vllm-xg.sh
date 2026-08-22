#!/bin/bash
# vLLM sur le DGX Spark, image derivee avec xgrammar 0.2.4.
# Memoire UNIFIEE : ce que le systeme garde en cache manque au GPU, d ou le sync.
sync
docker rm -f vllm-test 2>/dev/null
exec docker run --rm --name vllm-test --gpus all --ipc=host \
  -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 -e PYTHONIOENCODING=utf-8 \
  -p 8001:8000 -v ~/modeles:/modeles \
  vllm-spark:xg024 \
  vllm serve /modeles/qwen38-nvfp4 \
    --served-model-name qwen \
    --host 0.0.0.0 --port 8000 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.75 \
    --enable-auto-tool-choice --tool-call-parser qwen3_xml
