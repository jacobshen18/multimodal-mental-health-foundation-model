from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from mhfm.multimodal_schema import (
    MultimodalRecord,
    MultimodalValidationIssue,
    validate_multimodal_record,
)


def load_multimodal_jsonl(path: Path) -> list[MultimodalRecord]:
    records: list[MultimodalRecord] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(MultimodalRecord.model_validate_json(stripped))
            except ValidationError as error:
                raise ValueError(f"{path}:{line_number} invalid multimodal record: {error}") from error
    return records


def validate_multimodal_manifest(
    path: Path,
    root: Path | None = None,
    require_existing_files: bool = False,
) -> list[MultimodalValidationIssue]:
    issues: list[MultimodalValidationIssue] = []
    for record in load_multimodal_jsonl(path):
        issues.extend(
            validate_multimodal_record(
                record,
                root=root,
                require_existing_files=require_existing_files,
            )
        )
    return issues
