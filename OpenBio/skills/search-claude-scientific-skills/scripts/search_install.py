#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def resolve_skills_root(root: Path) -> Path:
    nested = root / "scientific-skills"
    return nested if nested.is_dir() else root


def list_skill_dirs(skills_root: Path) -> list[Path]:
    if not skills_root.exists():
        return []
    return sorted([p for p in skills_root.iterdir() if p.is_dir()])


def tokenize(query: str) -> list[str]:
    return [t for t in query.lower().split() if t.strip()]


def name_match_candidates(skills: list[Path], query: str) -> list[Path]:
    tokens = tokenize(query)
    if not tokens:
        return []
    scored = []
    for p in skills:
        name = p.name.lower()
        score = sum(1 for t in tokens if t in name)
        if score > 0:
            scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], x[1].name))
    return [p for _, p in scored]


def rg_available() -> bool:
    return shutil.which("rg") is not None


def rg_search(skills_root: Path, query: str) -> list[Path]:
    if not rg_available():
        return []
    try:
        result = subprocess.run(
            ["rg", "-l", query, str(skills_root)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return []
    files = [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]
    roots = set()
    for f in files:
        try:
            rel = f.relative_to(skills_root)
        except ValueError:
            continue
        parts = rel.parts
        if parts:
            roots.add(skills_root / parts[0])
    return sorted(roots)


def fallback_content_search(skills_root: Path, query: str) -> list[Path]:
    hits = set()
    for skill_dir in list_skill_dirs(skills_root):
        for root, _, files in os.walk(skill_dir):
            for fname in files:
                path = Path(root) / fname
                try:
                    text = path.read_text(errors="ignore")
                except Exception:
                    continue
                if query.lower() in text.lower():
                    hits.add(skill_dir)
                    break
            if skill_dir in hits:
                break
    return sorted(hits)


def choose_candidate(candidates: list[Path], select: str | None) -> Path | None:
    if not candidates:
        return None
    if select:
        for c in candidates:
            if c.name == select:
                return c
        return None
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c.name}")
    try:
        choice = input("Select a skill number (or press Enter to cancel): ").strip()
    except EOFError:
        return None
    if not choice:
        return None
    if not choice.isdigit():
        return None
    idx = int(choice)
    if idx < 1 or idx > len(candidates):
        return None
    return candidates[idx - 1]


def confirm(prompt: str, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    try:
        resp = input(f"{prompt} [y/N]: ").strip().lower()
    except EOFError:
        return False
    return resp in {"y", "yes"}


def install_dependencies(skill_dir: Path) -> list[str]:
    commands = []
    req = skill_dir / "requirements.txt"
    pyproject = skill_dir / "pyproject.toml"
    if req.exists():
        commands.append([sys.executable, "-m", "pip", "install", "-r", str(req)])
    if pyproject.exists():
        commands.append([sys.executable, "-m", "pip", "install", str(skill_dir)])
    return commands


def run_commands(commands: list[list[str]]) -> bool:
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}: {' '.join(cmd)}")
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Search and install Claude scientific skills.")
    parser.add_argument("--query", required=True, help="Search query.")
    parser.add_argument(
        "--root",
        default="/root/.deepagents/agent/scientific-skills",
        help="Root directory containing scientific skills.",
    )
    parser.add_argument(
        "--install-root",
        default="/root/.deepagents/agent/skills",
        help="Destination skills directory.",
    )
    parser.add_argument("--select", help="Exact skill folder name to install.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing destination.")
    parser.add_argument("--yes", action="store_true", help="Assume yes to prompts.")
    args = parser.parse_args()

    root = resolve_skills_root(Path(args.root))
    if not root.exists():
        print(f"Skills root not found: {root}")
        return 1

    skills = list_skill_dirs(root)
    name_matches = name_match_candidates(skills, args.query)
    if name_matches:
        candidates = name_matches
        print("Found matches by folder name:")
    else:
        print("No folder matches. Searching file contents...")
        candidates = rg_search(root, args.query)
        if not candidates:
            candidates = fallback_content_search(root, args.query)
        if not candidates:
            print("No matches found.")
            return 1

    selection = choose_candidate(candidates, args.select)
    if not selection:
        print("No selection made.")
        return 1

    dest_root = Path(args.install_root)
    dest = dest_root / selection.name
    if dest.exists():
        if not args.force and not confirm(f"Destination exists at {dest}. Overwrite?", args.yes):
            print("Install cancelled.")
            return 1
        shutil.rmtree(dest)

    print(f"Installing {selection.name} to {dest}")
    dest_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(selection, dest)

    commands = install_dependencies(dest)
    if commands:
        if confirm("Install dependencies now?", args.yes):
            if not run_commands(commands):
                return 1
    else:
        print("No dependencies found to install.")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
