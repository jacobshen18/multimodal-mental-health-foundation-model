# Contributing

Thanks for helping build this responsibly.

## Before Contributing

- Do not submit private, identifiable, scraped, or non-consensual mental health data.
- Do not present model outputs as medical advice.
- Prefer design proposals before large changes.
- Include evaluation and safety notes for model, dataset, or prompt changes.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull Requests

Every PR should include:

- What changed.
- Why it matters.
- How it was tested.
- Any safety, privacy, or governance impact.
