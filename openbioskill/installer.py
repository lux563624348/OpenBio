from __future__ import annotations

import argparse
import shutil
from importlib import resources
from pathlib import Path

DEFAULT_MODEL_NAME = "claude"
MODEL_DIRS = {
    "cursor": ".cursor",
    "claude": ".claude",
    "codex": ".codex",
    "gemini": ".gemini",
    "deepagents": ".deepagents",
    "deepagents-cli": ".deepagents",
}
AUTO_DETECT_ORDER = ("cursor", "claude", "codex", "gemini", "deepagents")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install bundled OpenBio skills into ~/.{model_name}/skills."
    )
    parser.add_argument(
        "--model-name",
        choices=sorted(MODEL_DIRS),
        help="Target model folder name. If omitted, auto-detect is used.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        help="Explicit destination path. Overrides --model-name when set.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the destination.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files.",
    )
    return parser.parse_args()


def model_name_to_target_dir(model_name: str, home: Path | None = None) -> Path:
    base = home or Path.home()
    model_root = MODEL_DIRS.get(model_name, f".{model_name}")
    return base / model_root / "skills"


def detect_target_dir(
    model_name: str | None = None, *, home: Path | None = None
) -> tuple[str, Path, bool]:
    base = home or Path.home()

    if model_name:
        return model_name, model_name_to_target_dir(model_name, base), False

    for candidate in AUTO_DETECT_ORDER:
        root_dir = base / MODEL_DIRS[candidate]
        skills_dir = root_dir / "skills"
        if root_dir.exists() or skills_dir.exists():
            return candidate, skills_dir, True

    return (
        DEFAULT_MODEL_NAME,
        model_name_to_target_dir(DEFAULT_MODEL_NAME, base),
        True,
    )


def _iter_skill_files(skills_root: Path):
    for src_path in skills_root.rglob("*"):
        if not src_path.is_file():
            continue
        rel_path = src_path.relative_to(skills_root)
        if "__pycache__" in rel_path.parts:
            continue
        if rel_path == Path("__init__.py"):
            continue
        if src_path.suffix in {".pyc", ".pyo"}:
            continue
        yield src_path, rel_path


def install_skills(
    target_dir: Path, *, force: bool = False, dry_run: bool = False
) -> tuple[int, int]:
    copied = 0
    skipped = 0
    skills_tree = resources.files("skills")

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    with resources.as_file(skills_tree) as source_dir:
        for src_path, rel_path in _iter_skill_files(Path(source_dir)):
            dst_path = target_dir / rel_path
            if dst_path.exists() and not force:
                skipped += 1
                continue
            if not dry_run:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
            copied += 1
    return copied, skipped


def main() -> int:
    args = _parse_args()
    if args.target_dir:
        target_dir = args.target_dir
        selected_model = "custom"
        auto_detected = False
    else:
        selected_model, target_dir, auto_detected = detect_target_dir(args.model_name)

    copied, skipped = install_skills(
        target_dir=target_dir,
        force=args.force,
        dry_run=args.dry_run,
    )

    mode = "dry-run" if args.dry_run else "installed"
    detect_note = "auto-detected" if auto_detected else "selected"
    print(
        f"{mode}: copied={copied} skipped={skipped} "
        f"model={selected_model} ({detect_note}) target={target_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
