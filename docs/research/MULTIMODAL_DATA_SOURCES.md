# Multimodal Data Sources

This file tracks candidate image, video, audio, and text datasets for multimodal mental-health-adjacent research.

Do not download, train on, redistribute, or mirror any dataset until its license, consent basis, provenance, privacy risk, and intended use have been reviewed. Many mental-health video datasets are access-controlled for good reasons.

## Mental-Health-Relevant Video and Audio

| Dataset | Modalities | Use | Access Notes | Source |
| --- | --- | --- | --- | --- |
| DAIC-WOZ / Extended DAIC | Video, audio, transcripts, questionnaire responses, facial features | Depression, anxiety, PTSD research; good candidate for evaluation and carefully governed training | Access-controlled. USC notes distribution is limited by consent constraints to academics and non-profit researchers. | https://dcapswoz.ict.usc.edu/ |
| AVEC 2019 State-of-Mind / Depression Challenge | Audio, visual, language features | Benchmarking multimodal state-of-mind and depression assessment models | Uses challenge datasets under controlled conditions; verify challenge terms before use. | https://arxiv.org/abs/1907.11510 |

## Auxiliary Multimodal Affect Data

These are not clinical mental-health datasets, but they can be useful for representation learning, affective pretraining, or evaluation of multimodal perception.

| Dataset | Modalities | Use | Access Notes | Source |
| --- | --- | --- | --- | --- |
| MELD | Video, audio, text | Emotion recognition in conversations; useful for multimodal emotion baselines | Based on TV dialogue; not clinical. Verify dataset license and redistribution terms. | https://arxiv.org/abs/1810.02508 |
| AffectNet | Images | Facial expression, valence, and arousal representation learning | Academic-use restrictions are common; verify license before use. | https://arxiv.org/abs/1708.03985 |
| CMU-MOSEI | Video, audio, text | Multimodal sentiment and emotion modeling | General-domain sentiment/emotion data; not clinical. Verify current access terms. | https://arxiv.org/abs/2505.06110 |

## Recommended Data Strategy

1. Use synthetic examples to test pipelines.
2. Use general affect datasets only for auxiliary representation learning and evaluation.
3. Use DAIC-WOZ or Extended DAIC only after formal access approval and dataset-card review.
4. Store only manifests, code, and metadata in this repository.
5. Keep raw videos, images, audio, and derived face crops outside git.
6. Never train on private, scraped, identifiable, or non-consensual mental-health media.

## Manifest Policy

Every multimodal dataset should be represented as JSONL manifests with explicit fields:

- `id`
- `text`
- `image_path` or `frame_paths`
- `source`
- `license`
- `consent`
- `risk_tags`

The manifest makes experiments reproducible without copying restricted media into the repository.
