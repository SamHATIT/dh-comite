FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates postgresql-client jq ripgrep openssh-client \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*
RUN npm install -g @anthropic-ai/claude-code
WORKDIR /workspace
# Generation des dossiers illustres (graphiques + docx)
RUN apt-get update -qq && apt-get install -y -qq python3-matplotlib python3-pip fonts-dejavu \
    && pip3 install --break-system-packages --quiet python-docx \
    && rm -rf /var/lib/apt/lists/*
# python3-yaml : dependance du moteur de politique (bin/policy.py, LOT-06 du
# 17/08). Paquet apt et non pip, pour que la construction reste reproductible.
# Sans lui le moteur rend ERREUR et le controle retombe sur les regles
# textuelles — celles-la memes que le lot remplace. La suite tests/policy.sh
# echoue alors, ce qui est le comportement voulu : la dependance manquante se
# voit a la construction, pas pendant une ronde.
RUN apt-get update -qq && apt-get install -y -qq python3-yaml \
    && rm -rf /var/lib/apt/lists/*
