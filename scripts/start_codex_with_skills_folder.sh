#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_SOURCE_DIR="${SKILL_SOURCE_DIR:-$REPO_ROOT/skills_folder_test}"
LAUNCH_CODEX_HOME="${LAUNCH_CODEX_HOME:-$REPO_ROOT/.codex-skills-folder-home}"
BASE_CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <skills_dir> [codex args...]" >&2
  exit 1
fi

INPUT_SKILLS_DIR="$1"
shift

if [[ ! -d "$INPUT_SKILLS_DIR" ]]; then
  echo "Error: skills_dir must be a directory: $INPUT_SKILLS_DIR" >&2
  exit 1
fi

mkdir -p "$LAUNCH_CODEX_HOME"
mkdir -p "$SKILL_SOURCE_DIR"

if ! find "$INPUT_SKILLS_DIR" -name "SKILL.md" -type f | grep -q .; then
  echo "Error: no SKILL.md files found under: $INPUT_SKILLS_DIR" >&2
  exit 1
fi

# Replace previous test skills with the provided folder contents.
find "$SKILL_SOURCE_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -a "$INPUT_SKILLS_DIR/." "$SKILL_SOURCE_DIR/"

# Reuse existing Codex settings and auth when available.
for filename in config.toml auth.json; do
  if [[ -f "$BASE_CODEX_HOME/$filename" ]]; then
    cp -f "$BASE_CODEX_HOME/$filename" "$LAUNCH_CODEX_HOME/$filename"
  fi
done

rm -rf "$LAUNCH_CODEX_HOME/skills"
ln -s "$SKILL_SOURCE_DIR" "$LAUNCH_CODEX_HOME/skills"

exec env CODEX_HOME="$LAUNCH_CODEX_HOME" codex "$@"
