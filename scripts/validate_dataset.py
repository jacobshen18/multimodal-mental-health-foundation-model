from __future__ import annotations

import argparse
from pathlib import Path

from mhfm.dataset import validate_dataset, write_issues_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate JSONL dataset records before training.")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    issues = validate_dataset(args.dataset)

    if args.output:
        write_issues_json(args.output, issues)

    if issues:
        for issue in issues:
            print(f"{issue.record_id}: {issue.field}: {issue.message}")
        raise SystemExit(1)

    print(f"{args.dataset} passed validation")


if __name__ == "__main__":
    main()
