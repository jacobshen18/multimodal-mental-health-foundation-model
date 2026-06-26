import json

import pytest

from mhfm.multimodal_dataset import load_multimodal_jsonl, validate_multimodal_manifest
from mhfm.multimodal_schema import MultimodalRecord, validate_multimodal_record


def test_load_multimodal_manifest_reads_image_record(tmp_path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(
        json.dumps(
            {
                "id": "sample-1",
                "text": "A synthetic example.",
                "image_path": "image.jpg",
                "source": "synthetic",
                "license": "CC0",
                "consent": "synthetic",
                "risk_tags": ["demo"],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    records = load_multimodal_jsonl(manifest)

    assert records[0].id == "sample-1"
    assert records[0].image_path == "image.jpg"


def test_multimodal_record_requires_visual_modality() -> None:
    with pytest.raises(ValueError, match="image_path or frame_paths"):
        MultimodalRecord(
            id="bad",
            text="No visual data.",
            source="synthetic",
            license="CC0",
            consent="synthetic",
        )


def test_high_risk_tags_are_flagged() -> None:
    record = MultimodalRecord(
        id="sample-2",
        text="Example text.",
        image_path="image.jpg",
        source="synthetic",
        license="CC0",
        consent="synthetic",
        risk_tags=["private-media"],
    )

    issues = validate_multimodal_record(record)

    assert issues
    assert issues[0].field == "risk_tags"


def test_missing_file_is_flagged_when_required(tmp_path) -> None:
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(
        json.dumps(
            {
                "id": "sample-3",
                "text": "A synthetic example.",
                "image_path": "missing.jpg",
                "source": "synthetic",
                "license": "CC0",
                "consent": "synthetic",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    issues = validate_multimodal_manifest(manifest, root=tmp_path, require_existing_files=True)

    assert issues
    assert issues[0].field == "image_path"
