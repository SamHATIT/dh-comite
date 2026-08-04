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
