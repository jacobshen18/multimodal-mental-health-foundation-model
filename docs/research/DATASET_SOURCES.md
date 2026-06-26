# Open Data Sources

This file tracks candidate public datasets for responsible mental-health-adjacent model research.

Do not download, train on, redistribute, or mirror any dataset until its license, provenance, consent basis, privacy risk, and intended use have been reviewed.

## Recommended Starting Points

| Dataset | Use | Why It Matters | License / Access Notes | Source |
| --- | --- | --- | --- | --- |
| Cactus | Training/evaluation candidate | Synthetic multi-turn CBT-style counseling dialogues; paper reports 31,577 dialogues and about 1M utterances. | Publicly available per paper; verify repository/license before use. Synthetic data still needs safety review. | https://arxiv.org/abs/2407.03103 |
| KokoroChat | Research/evaluation candidate | Japanese counseling dialogue dataset collected through role-play by trained counselors; includes 6,589 long-form dialogues and feedback labels. | CC BY-NC-ND 4.0, so do not modify, redistribute derivatives, or use commercially. Good candidate for research evaluation, not open-ended commercial training. | https://github.com/UEC-InabaLab/KokoroChat |
| EmpatheticDialogues | Empathy pretraining/evaluation candidate | 25k conversations grounded in emotional situations; not clinical, but useful for empathy and supportive-response baselines. | CC BY-NC 4.0. Non-commercial only. | https://github.com/facebookresearch/EmpatheticDialogues |
| GoEmotions | Emotion classifier/evaluation candidate | 58k Reddit comments labeled for 27 emotions plus neutral; useful for auxiliary emotion recognition, not therapy behavior. | Google Research repo is Apache-2.0; Reddit-origin data still needs privacy and terms review. | https://github.com/google-research/google-research/tree/master/goemotions |

## Use With Extra Caution

| Dataset | Use | Main Concern | Source |
| --- | --- | --- | --- |
| MentaLLaMA / IMHI | Mental-health classification benchmark candidate | Built from social-media mental-health sources and model-generated explanations. Treat as classification/eval data first; review original raw-data licenses and consent carefully. | https://arxiv.org/abs/2309.13567 |
| Dreaddit | Stress-detection benchmark candidate | Reddit-origin stress data. Useful for stress classification research, but not a consented counseling corpus. | https://arxiv.org/abs/1911.00133 |
| OnCoCo 1.0 | Counseling message classification candidate | Public dataset from online counseling conversations; verify access terms and privacy constraints before use. | https://arxiv.org/abs/2512.09804 |
| Psy-Insight | Counseling analysis candidate | Face-to-face counseling dialogues with bilingual annotations; verify release status, consent model, and license before use. | https://arxiv.org/abs/2503.03607 |
| OpenNeuro | Multimodal/neuroscience research candidate | CC0 neuroimaging repository, not a language-model counseling dataset. Useful only for broader mental-health research with specialized governance. | https://openneuro.org |

## Exclusion Rules

Reject a dataset if any of the following are true:

- It contains private therapy records without explicit release consent.
- It is scraped from vulnerable communities without clear redistribution rights.
- It lacks a license or terms compatible with the intended use.
- It includes identifiable personal data that cannot be removed.
- It is marketed as enabling diagnosis or crisis intervention without clinical validation.

## First Data Plan

1. Start with synthetic or role-played datasets for pipeline development.
2. Use empathy and emotion datasets as auxiliary evaluation, not as proof of clinical safety.
3. Keep Reddit/social-media mental-health datasets out of generative training until governance review.
4. Write a dataset card for every approved source before ingestion.
5. Publish only scripts and metadata in this repository, not third-party dataset copies.
