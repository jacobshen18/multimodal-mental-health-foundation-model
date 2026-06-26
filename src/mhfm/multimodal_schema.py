from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator


ConsentType = Literal["explicit", "approved-research-use", "public-domain", "synthetic", "not-applicable"]


class MultimodalRecord(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source: str = Field(min_length=1)
    license: str = Field(min_length=1)
    consent: ConsentType
    image_path: str | None = None
    frame_paths: list[str] = Field(default_factory=list)
    audio_path: str | None = None
    risk_tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_visual_modality(self) -> "MultimodalRecord":
        if not self.image_path and not self.frame_paths:
            raise ValueError("A multimodal record must include image_path or frame_paths.")
        return self


@dataclass(frozen=True)
class MultimodalValidationIssue:
    record_id: str
    field: str
    message: str


def validate_multimodal_record(
    record: MultimodalRecord,
    root: Path | None = None,
    require_existing_files: bool = False,
) -> list[MultimodalValidationIssue]:
    issues: list[MultimodalValidationIssue] = []
    lowered_tags = {tag.lower() for tag in record.risk_tags}

    if record.consent not in {"explicit", "approved-research-use", "public-domain", "synthetic", "not-applicable"}:
        issues.append(
            MultimodalValidationIssue(
                record_id=record.id,
                field="consent",
                message="Consent must be explicit, approved-research-use, public-domain, synthetic, or not-applicable.",
            )
        )

    if {"diagnosis", "crisis", "private-media"} & lowered_tags:
        issues.append(
            MultimodalValidationIssue(
                record_id=record.id,
                field="risk_tags",
                message="High-risk multimodal data requires maintainer and privacy review before training.",
            )
        )

    if require_existing_files:
        issues.extend(_validate_paths_exist(record, root or Path(".")))

    return issues


def _validate_paths_exist(record: MultimodalRecord, root: Path) -> list[MultimodalValidationIssue]:
    issues: list[MultimodalValidationIssue] = []
    paths: list[tuple[str, str]] = []

    if record.image_path:
        paths.append(("image_path", record.image_path))
    paths.extend(("frame_paths", path) for path in record.frame_paths)
    if record.audio_path:
        paths.append(("audio_path", record.audio_path))

    for field, path in paths:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = root / candidate
        if not candidate.exists():
            issues.append(
                MultimodalValidationIssue(
                    record_id=record.id,
                    field=field,
                    message=f"Referenced file does not exist: {path}",
                )
            )

    return issues
