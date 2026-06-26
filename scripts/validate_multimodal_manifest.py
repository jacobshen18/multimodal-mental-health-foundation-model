from __future__ import annotations

import argparse
from pathlib import Path

from mhfm.multimodal_dataset import validate_multimodal_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a multimodal JSONL dataset manifest.")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--require-existing-files", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    issues = validate_multimodal_manifest(
        args.manifest,
        root=args.root,
        require_existing_files=args.require_existing_files,
    )

    if issues:
        for issue in issues:
            print(f"{issue.record_id}: {issue.field}: {issue.message}")
        raise SystemExit(1)

    print(f"{args.manifest} passed validation")


if __name__ == "__main__":
    main()
