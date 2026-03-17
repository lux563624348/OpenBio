![OpenBio](src/images/OpenBio.png)
# BioDeepagents CLI

[![PyPI](https://img.shields.io/pypi/v/openbioskill?label=openbioskill&logo=pypi&logoColor=white)](https://pypi.org/project/openbioskill/)

## PyPI Package

The `openbioskill` package ships the bioinformatics skill bundle so you can manage and distribute skills via PyPI.

Install from PyPI:

```bash
python3 -m pip install openbioskill
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

## Verified K-Dense Skills (146 total)
- `iso-13485-certification` (author: K-Dense Inc.) – comprehensive ISO 13485:2016 QMS guidance with gap analysis tooling, clause-by-clause references, and templates for Quality Manuals, procedures, and Medical Device Files so teams can assess readiness and build compliant documentation.

| Skills Source | Verified # | Total # | Verification Methods |
| --- | --- | --- | --- |
| `claude-scientific-skills` (K-Dense Inc.) | 146 | 147 (total skills in `skills/`) | Metadata-driven audit: only `SKILL.md` files with `skill-author: K-Dense Inc.` are promoted from `skills_unverified/claude-scientific-skills/` into `skills/`, ensuring each verified skill is explicitly claimed by the author. |

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
