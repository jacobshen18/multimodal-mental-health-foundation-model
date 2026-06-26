from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field


ConsentType = Literal["explicit", "public-domain", "synthetic", "not-applicable"]


class DatasetRecord(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    source: str = Field(min_length=1)
    license: str = Field(min_length=1)
    consent: ConsentType
    risk_tags: list[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ValidationIssue:
    record_id: str
    field: str
    message: str


def validate_record(record: DatasetRecord) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if record.consent not in {"explicit", "public-domain", "synthetic", "not-applicable"}:
        issues.append(
            ValidationIssue(
                record_id=record.id,
                field="consent",
                message="Consent must be explicit, public-domain, synthetic, or not-applicable.",
            )
        )

    if "diagnosis" in {tag.lower() for tag in record.risk_tags}:
        issues.append(
            ValidationIssue(
                record_id=record.id,
                field="risk_tags",
                message="Diagnosis-related data requires maintainer review before training use.",
            )
        )

    return issues
