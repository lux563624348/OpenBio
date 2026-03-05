---
name: search-claude-scientific-skills
description: Search a downloaded Claude scientific skills collection and install a selected skill. Use when asked to find, select, or install skills from a local checkout of https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills into /root/.deepagents/agent/skills/, including dependency installation from requirements.txt or pyproject.toml.
---

# Search Claude Scientific Skills

Use this skill to find and install a Claude scientific skill from a local checkout of the GitHub collection.

## Quick Start

1. Download the collection locally (one-time):

```bash
git clone https://github.com/K-Dense-AI/claude-scientific-skills.git /root/.deepagents/agent/claude-scientific-skills
```

2. Run the search-and-install helper:

```bash
python skills/search-claude-scientific-skills/scripts/search_install.py \
  --query "metagenomics" \
  --root /root/.deepagents/agent/claude-scientific-skills/scientific-skills
```

3. Pick a result when prompted.
4. Confirm installation and dependency setup when asked.

## How It Works

- Searches folder names first, then file contents if no folder matches.
- Auto-detects whether the `--root` path contains a nested `scientific-skills/` directory and uses it if present.
- Installs the selected skill into `/root/.deepagents/agent/skills/<skill-name>` (or `--install-root` if provided).
- Installs dependencies from `requirements.txt` and/or `pyproject.toml` inside the selected skill directory.

## Non-Interactive Usage

```bash
python skills/search-claude-scientific-skills/scripts/search_install.py \
  --query "genome" \
  --select "genome-compare" \
  --root /root/.deepagents/agent/claude-scientific-skills/scientific-skills \
  --force
```

## Safety Checks

- Always confirm before overwriting an existing destination skill.
- If dependency installation fails, report the exact command and error.
