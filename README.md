# Mental Health Foundation Model

An open-source research project for training and evaluating foundation models that can support mental-health-adjacent workflows responsibly.

This project is not a medical device, therapist, diagnostic system, crisis service, or substitute for professional care. The goal is to build transparent tooling, datasets, training recipes, and safety evaluations for research and assistive use cases.

## Goals

- Build reproducible training and adaptation recipes for mental-health-supportive language models.
- Establish data governance practices for consent, privacy, de-identification, provenance, and licensing.
- Create evaluation suites for safety, empathy, clinical-boundary adherence, crisis handling, and hallucination risk.
- Publish model, data, and evaluation cards with each release.
- Encourage interdisciplinary review from clinicians, researchers, people with lived experience, and safety experts.

## Non-Goals

- Diagnosing mental health conditions.
- Replacing licensed clinicians or crisis services.
- Training on private, scraped, or non-consensual therapy records.
- Releasing models without safety evaluation and usage guidance.

## Repository Layout

```text
configs/                 Training and evaluation configs
data/cards/              Dataset card templates and governance docs
docs/guidelines/         Safety, contribution, and release guidance
docs/research/           Research notes and design proposals
scripts/                 Command-line entry points
src/mhfm/                Python package
tests/                   Unit tests
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,train]"
python scripts/validate_dataset.py --dataset examples/synthetic_dataset.jsonl
pytest
```

## Dataset Format

Training and evaluation examples should be JSONL records:

```json
{"id":"example-001","text":"...","source":"...","license":"...","consent":"explicit","risk_tags":["supportive-dialogue"]}
```

Do not commit sensitive data, private clinical notes, identifiable personal information, or scraped therapy conversations.

## Safety Principles

- Prefer lower-risk assistive use cases first: journaling support, psychoeducation drafts, clinician workflow support, and resource navigation.
- Always maintain clear boundaries: no diagnosis, no treatment plans, no medication advice, no claims of professional relationship.
- Route crisis or imminent-harm content toward local emergency resources and qualified human support.
- Measure model behavior before release, and document known limitations.

## Status

Early scaffold. The project is ready for issues, design proposals, governance work, and first training experiments.

## License

Code is licensed under Apache-2.0. Dataset contributions must include explicit license and provenance metadata.
