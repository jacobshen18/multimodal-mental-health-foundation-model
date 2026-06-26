"""Responsible training scaffolding for mental-health-adjacent foundation models."""

from mhfm.schema import DatasetRecord, ValidationIssue, validate_record
from mhfm.multimodal_schema import (
    MultimodalRecord,
    MultimodalValidationIssue,
    validate_multimodal_record,
)

__all__ = [
    "DatasetRecord",
    "ValidationIssue",
    "validate_record",
    "MultimodalRecord",
    "MultimodalValidationIssue",
    "validate_multimodal_record",
]
