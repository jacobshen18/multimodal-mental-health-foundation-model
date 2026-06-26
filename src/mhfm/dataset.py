from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from mhfm.schema import DatasetRecord, ValidationIssue, validate_record


def load_jsonl(path: Path) -> list[DatasetRecord]:
    records: list[DatasetRecord] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(DatasetRecord.model_validate_json(stripped))
            except ValidationError as error:
                raise ValueError(f"{path}:{line_number} invalid dataset record: {error}") from error
    return records


def validate_dataset(path: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for record in load_jsonl(path):
        issues.extend(validate_record(record))
        if _looks_like_private_data(record.text):
            issues.append(
                ValidationIssue(
                    record_id=record.id,
                    field="text",
                    message="Text may contain private data and needs manual privacy review.",
                )
            )
    return issues


def write_issues_json(path: Path, issues: list[ValidationIssue]) -> None:
    payload = [issue.__dict__ for issue in issues]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _looks_like_private_data(text: str) -> bool:
    lowered = text.lower()
    private_markers = ["ssn", "social security", "phone number", "home address", "patient id"]
    return any(marker in lowered for marker in private_markers)
