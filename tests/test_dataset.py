import json

import pytest

from mhfm.dataset import load_jsonl, validate_dataset
from mhfm.schema import DatasetRecord, validate_record


def test_load_jsonl_reads_dataset_record(tmp_path) -> None:
    dataset = tmp_path / "train.jsonl"
    dataset.write_text(
        json.dumps(
            {
                "id": "sample-1",
                "text": "A short supportive example.",
                "source": "synthetic",
                "license": "CC0",
                "consent": "synthetic",
                "risk_tags": ["supportive-dialogue"],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    records = load_jsonl(dataset)

    assert records[0].id == "sample-1"
    assert records[0].consent == "synthetic"


def test_invalid_record_raises(tmp_path) -> None:
    dataset = tmp_path / "train.jsonl"
    dataset.write_text(json.dumps({"id": "sample-1"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid dataset record"):
        load_jsonl(dataset)


def test_diagnosis_tag_requires_review() -> None:
    record = DatasetRecord(
        id="sample-2",
        text="Example text",
        source="synthetic",
        license="CC0",
        consent="synthetic",
        risk_tags=["diagnosis"],
    )

    issues = validate_record(record)

    assert issues
    assert issues[0].field == "risk_tags"


def test_private_data_marker_is_flagged(tmp_path) -> None:
    dataset = tmp_path / "train.jsonl"
    dataset.write_text(
        json.dumps(
            {
                "id": "sample-3",
                "text": "This line includes a phone number marker.",
                "source": "synthetic",
                "license": "CC0",
                "consent": "synthetic",
                "risk_tags": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    issues = validate_dataset(dataset)

    assert any(issue.field == "text" for issue in issues)
