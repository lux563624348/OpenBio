---
name: hubmap-rag
description: RAG over HuBMAP-related PDFs using local file-based retrieval (no FAISS) with the opendataloader-pdf parser. Use for questions that mention HuBMAP docs, policies, or data, and ground answers in parsed documents under `skills/hubmap-rag/parsed`.
---

# HuBMAP RAG

## Overview

Search HuBMAP PDFs with lightweight local retrieval to support RAG-style answers, grounded in parsed content under `skills/hubmap-rag/parsed`.

## Workflow

1. Confirm prerequisites. Source PDFs are in `skills/hubmap-rag/pdfs`, parsed files are in `skills/hubmap-rag/parsed`, and the parser from https://github.com/opendataloader-project/opendataloader-pdf is installed and available.
2. Refresh parsed files only when PDFs changed:
   - Run `opendataloader-pdf skills/hubmap-rag/pdfs -o skills/hubmap-rag/parsed -f json,text,markdown`.
3. Build query terms from the user question. Include synonyms and key entities (for example: "data access", "DUA", "consent", "tissue", "metadata").
4. Retrieve candidate passages from parsed files (no vector index):
   - Use fast local search (for example `rg -n`) across `skills/hubmap-rag/parsed/*.txt` or `*.md`.
   - Pull the best matching snippets and nearby context windows.
5. Rank and filter snippets for relevance. Prefer passages that match multiple key terms and explicit policy/process language.
6. Respond with RAG-style output. Cite the original PDF filename and page number when available. If retrieval is weak or empty, ask for a narrower query or suggest specific document names.

## Retrieval Notes

- No FAISS index is required for this skill.
- Default source PDF path: `skills/hubmap-rag/pdfs`.
- Default retrieval path: `skills/hubmap-rag/parsed`.
- Default parser: https://github.com/opendataloader-project/opendataloader-pdf
- Prefer reproducible local retrieval (parse -> search -> cite) so answers stay auditable.

## Example Triggers

- "Search the HuBMAP policy documents for data retention rules."
- "What do the HuBMAP docs say about tissue data formats?"
- "Find passages about HuBMAP data access policy."
