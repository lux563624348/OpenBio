FROM python:3.12-slim

ARG BIODEEP_DIR=/workspace/biodeep
ENV PYTHONUNBUFFERED=1
ENV BIODEEP_DIR=${BIODEEP_DIR}

# Install utilities for debugging and Git for repo initialization.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git htop ripgrep vim \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /workspace/cli/.venv \
    && /workspace/cli/.venv/bin/pip install --no-cache-dir --upgrade pip \
    && /workspace/cli/.venv/bin/pip install --no-cache-dir deepagents deepagents-cli \
    && rm -rf /root/.cache/pip

## Copy customized skills/ config
COPY AGENTS_BIODEEP.md /root/.deepagents/agent/AGENTS.md
COPY config.toml /root/.deepagents/config.toml
COPY skills/ /root/.deepagents/agent/skills/
## potential skills

COPY cli_cp/ /workspace/cli/
COPY .gitignore /workspace/cli/deepagents_cli/.gitignore

RUN /workspace/cli/.venv/bin/python -c "from pathlib import Path;import shutil;import deepagents_cli;pkg=Path(deepagents_cli.__file__).parent;src=Path('/workspace/cli/deepagents_cli'); \
    shutil.copytree(src, pkg, dirs_exist_ok=True)" 

RUN CONFIG_PATH=$(/workspace/cli/.venv/bin/python -c "import deepagents_cli;from pathlib import Path;print(Path(deepagents_cli.__file__).parent / 'config.py')") \
    && curl -fsSL https://raw.githubusercontent.com/langchain-ai/deepagents/refs/heads/main/libs/cli/deepagents_cli/config.py -o "$CONFIG_PATH" \
    && /workspace/cli/.venv/bin/python -c "from pathlib import Path;import re;import deepagents_cli;bs=Path('/workspace/cli/deepagents_cli/ASCII_Banner.py').read_text();m=re.search(r'_UNICODE_BANNER\\s*=\\s*f?\"\"\"[\\s\\S]*?\"\"\"',bs); \
        (m is None) and (_ for _ in ()).throw(SystemExit('_UNICODE_BANNER not found')); \
        cp=Path(deepagents_cli.__file__).parent / 'config.py';ct=cp.read_text();u,c=re.subn(r'_UNICODE_BANNER\\s*=\\s*f?\"\"\"[\\s\\S]*?\"\"\"',m.group(0),ct,1); \
        (c!=1) and (_ for _ in ()).throw(SystemExit('_UNICODE_BANNER block not replaced'));cp.write_text(u)"

EXPOSE 8888
COPY scripts/start_services.sh /workspace/start_services.sh
RUN chmod +x /workspace/start_services.sh

WORKDIR ${BIODEEP_DIR}
ENTRYPOINT ["/workspace/start_services.sh"]
