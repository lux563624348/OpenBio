# BioDeepagents CLI

## PyPI Package

The `BioDeep` package ships the bioinformatics skill bundle so you can manage and distribute skills via PyPI.

Install from PyPI:

```bash
python3 -m pip install BioDeep
```

The package includes:
- The `biodeep` Python package
- Bundled bioinformatics skills under `biodeep/skills`
- A console entry point: `deepagents`

## Skills

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
| [claw-ancestry-pca](skills/claw-ancestry-pca/SKILL.md) | Ancestry decomposition PCA against the Simons Genome Diversity Project. |
| [claw-metagenomics](skills/claw-metagenomics/SKILL.md) | Shotgun metagenomics profiling — taxonomy, resistome, and functional pathways. |
| [claw-semantic-sim](skills/claw-semantic-sim/SKILL.md) | Semantic Similarity Index for disease research literature using PubMedBERT embeddings. |
| [drug-photo](skills/drug-photo/SKILL.md) | Photo of a medication to get pharmacogenomic dosage guidance via a CPIC single-drug lookup. |
| [equity-scorer](skills/equity-scorer/SKILL.md) | Compute HEIM diversity and equity metrics from VCF or ancestry data. Generates heterozygosity, FST, PCA plots, and a composite HEIM Equity Score with markdown reports. |
| [genome-compare](skills/genome-compare/SKILL.md) | Compare your genome to George Church (PGP-1) and estimate ancestry composition. |
| [labstep](skills/labstep/SKILL.md) | Interact with the Labstep electronic lab notebook API using labstepPy. Query experiments, protocols, resources, inventory, and other lab entities. |
| [lit-synthesizer](skills/lit-synthesizer/SKILL.md) | Search PubMed and bioRxiv, summarise papers with LLM, build citation graphs, and generate literature review sections. |
| [nutrigx-advisor](skills/nutrigx_advisor/SKILL.md) | Personalised nutrition report from genetic data (23andMe, AncestryDNA, or VCF). |
| [pharmgx-reporter](skills/pharmgx-reporter/SKILL.md) | Pharmacogenomic report from DTC genetic data (23andMe/AncestryDNA). |
| [repro-enforcer](skills/repro-enforcer/SKILL.md) | Export any bioinformatics analysis as a reproducible bundle with Conda environment, Singularity container definition, and Nextflow pipeline. |
| [scrna-orchestrator](skills/scrna-orchestrator/SKILL.md) | Automate single-cell RNA-seq analysis with Scanpy or Seurat. QC, normalisation, clustering, DE analysis, and visualisation. |
| [seq-wrangler](skills/seq-wrangler/SKILL.md) | Sequence QC, alignment, and BAM processing. Wraps FastQC, BWA/Bowtie2, SAMtools for automated read-to-BAM pipelines. |
| [struct-predictor](skills/struct-predictor/SKILL.md) | Local protein structure prediction with AlphaFold, Boltz, or Chai. Compare predicted structures, compute RMSD, visualise 3D models. |
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
