from __future__ import annotations

import argparse
from pathlib import Path

from openbioskill.installer import (
    MODEL_DIRS,
    detect_target_dir,
    install_skills,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="openbio",
        description="OpenBio CLI for managing bundled skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser(
        "install", help="Install bundled skills to ~/.{model_name}/skills."
    )
    install_parser.add_argument(
        "--model-name",
        choices=sorted(MODEL_DIRS),
        help="Target model folder name. If omitted, auto-detect is used.",
    )
    install_parser.add_argument(
        "--target-dir",
        type=Path,
        help="Explicit destination path. Overrides --model-name when set.",
    )
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in the destination.",
    )
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without writing files.",
    )

    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if args.command != "install":
        raise SystemExit(2)

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
