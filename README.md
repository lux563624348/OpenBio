# BioDeepagents CLI

[![PyPI](https://img.shields.io/pypi/v/OpenBio?label=OpenBio&logo=pypi&logoColor=white)](https://pypi.org/project/OpenBio/)

## PyPI Package

The `OpenBio` package ships the bioinformatics skill bundle so you can manage and distribute skills via PyPI.

Install from PyPI:

```bash
python3 -m pip install OpenBio
```

The package includes:
- The `OpenBio` Python package
- Bundled bioinformatics skills under `OpenBio/skills`
- A console entry point: `deepagents`

## Skills

Upstream skill sources and datasets:
- [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills)
- [ClawBio](https://github.com/ClawBio/ClawBio)
- [Indexd Skills Datasets](https://agent.indexd.org/skills-datasets)

Skills are sourced from BioClaw. The following skills are sourced from claude-scientific-skills:
- Bioinformatics & Genomics
- Sequence Analysis: Process DNA/RNA/protein sequences with BioPython and pysam
- Single-Cell Analysis: Analyze 10X Genomics data with Scanpy, identify cell types, infer GRNs with Arboreto
- Variant Annotation: Annotate VCF files with Ensembl VEP, query ClinVar for pathogenicity
- Variant Database Management: Build scalable VCF databases with TileDB-VCF for incremental sample addition, efficient population-scale queries, and compressed storage of genomic variant data
- Gene Discovery: Query NCBI Gene, UniProt, and Ensembl for comprehensive gene information
- Network Analysis: Identify protein-protein interactions via STRING, map to pathways (KEGG, Reactome)

| Skill | Description |
| --- | --- |
| [bio-orchestrator](skills/bio-orchestrator/SKILL.md) | Meta-agent that routes bioinformatics requests to specialised sub-skills. Handles file type detection, analysis planning, report generation, and reproducibility export. |
...
| [vcf-annotator](skills/vcf-annotator/SKILL.md) | Annotate VCF variants with VEP, ClinVar, gnomAD frequencies, and ancestry-aware context. Generates prioritised variant reports. |

This project is basing on [deepagents](https://github.com/langchain-ai/deepagents) CLI, an open source coding assistant that runs in your terminal, similar to Claude Code.

*Key Features:**
- **Built-in Tools**: File operations (read, write, edit, glob, grep), shell commands, web search, and subagent delegation
- **Customizable Skills**: Add domain-specific capabilities through a progressive disclosure skill system
- **Persistent Memory**: Agent remembers your preferences, coding style, and project context across sessions
- **Project-Aware**: Automatically detects project roots and loads project-specific configurations 

<img src="cli-banner.jpg" alt="deep agent" width="100%"/>


## 🐳 Docker

Build the CLI image from the repository root so both the CLI sources and the shared `deepagents` package are available to Docker:

This project is a docker-compose hosted a deepagents-cli, and inside container some other agents(e.g. dsl) were also hosted. 

```bash
docker compose run --rm --service-ports --build flask-app
```

Copy the sample configuration into place and edit the credentials or tracing toggles you need:


```bash
docker run --rm -it -P \
  -v "$(pwd)/workspace/:/workspace/project" \
  --env-file ./.env \
  deepagents-cli
```
Type naturally as you would in a chat interface. The agent will use its built-in tools, skills, and memory to help you with tasks.

> [!WARNING]
> **Human-in-the-Loop (HITL) Approval Required**
>
> Potentially destructive operations require user approval before execution:
> - **File operations**: `write_file`, `edit_file`
> - **Command execution**: `shell`, `execute`
> - **External requests**: `web_search`, `fetch_url`
> - **Delegation**: `task` (subagents)
>
> Each operation will prompt for approval showing the action details. Use `--auto-approve` to skip prompts:
> ```bash
> deepagents --auto-approve
> ``` 
