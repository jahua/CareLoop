# Supplementary Materials

**Paper**: Personality-Adaptive Conversational AI for Mental Health Support: A Simulation Study Using Big Five Detection and Zurich Model-Aligned Regulation (V8.3.1)

---

## Folder Structure

```
supplementary/
├── docs/                            # S1–S3 — System prompts, regulation templates, evaluator
│   ├── S1_detection_prompts.md              # Big Five trait detection prompts (enhanced)
│   ├── S1_detection_prompts_fixed.md        # Fixed/production detection prompts
│   ├── S2_regulation_zurich_algorithm.md    # Zurich Model regulation algorithm
│   ├── S2_regulation_zurich_model_application.md  # Full Zurich Model application doc
│   ├── S3_evaluator_system_prompt.md        # Evaluator GPT integration & scoring matrix
│   ├── S3_evaluator_workflow_guide.md       # Evaluator workflow guide
│   ├── technical_specifications_v1.2.md     # Full system technical specification
│   └── workflow_gpt4_production.json        # Production n8n workflow (GPT-4, Sep 2024)
│
├── data/
│   ├── raw/                         # S5 — Simulation transcripts & evaluation data
│   │   ├── A-1.csv … A-5.csv        # Type A profile evaluation sheets (5 conversations)
│   │   ├── B-1.csv … B-5.csv        # Type B profile evaluation sheets (5 conversations)
│   │   ├── RESULTS.csv              # Aggregated evaluation results
│   │   └── Evaluation-Simulated-Conversations.xlsx  # Master evaluation workbook
│   └── processed/                   # S5 — Merged & cleaned data for analysis
│       ├── baseline.csv             # Baseline condition (merged, scored)
│       └── regulated.csv            # Regulated condition (merged, scored)
│
├── code/                            # S6 — Statistical analysis code
│   ├── statistical_analysis.ipynb   # Jupyter notebook (full analysis with outputs)
│   └── enhanced_statistical_analysis.py  # Python script (effect sizes, tests, plots)
│
└── figures/                         # Supplementary Figures SF1–SF3
    ├── SF1_missingness_comparison.png   # SF1: <5% missing data across conditions
    ├── SF2_personality_needs_by_conversation.png  # SF2: YES-rate per conversation pair
    └── SF3_rating_distribution.png     # SF3: YES/NOT SURE/NO distribution (100% stacked)
```

---

## Supplementary File Index

| Label | Description | Location |
|-------|-------------|----------|
| S1 | Big Five personality trait **detection system prompts** (enhanced + production-fixed) | `docs/S1_detection_prompts.md`, `docs/S1_detection_prompts_fixed.md` |
| S2 | **Regulation templates** — Zurich Model algorithm implementation and full application doc | `docs/S2_regulation_zurich_algorithm.md`, `docs/S2_regulation_zurich_model_application.md` |
| S3 | **Evaluator GPT** system prompt, scoring matrix and workflow guide | `docs/S3_evaluator_system_prompt.md`, `docs/S3_evaluator_workflow_guide.md` |
| — | Full PROMISE **technical specification** (v1.2) | `docs/technical_specifications_v1.2.md` |
| — | Production **n8n workflow JSON** (importable; GPT-4, Sep 2024 study run) | `docs/workflow_gpt4_production.json` |
| S5 | Complete simulation transcripts — 20 conversations (10 regulated, 10 baseline), 120 dialogue turns total, evaluation scores per turn | `data/raw/` |
| S6 | Statistical analysis code — Python/Jupyter for effect sizes, paired tests, weighted scoring, bootstrap CI, and visualisations | `code/` |
| SF1 | Missingness comparison plot — horizontal bars showing <5% missing data across conditions | `figures/SF1_missingness_comparison.png` |
| SF2 | Personality needs YES-rate by conversation — paired lines connecting baseline and regulated across all 10 conversation pairs | `figures/SF2_personality_needs_by_conversation.png` |
| SF3 | Rating distribution raw counts — YES/NOT SURE/NO composition per metric and condition | `figures/SF3_rating_distribution.png` |

> **Note**: Supplementary File S4 (author qualitative review protocol) and S7–S12 (qualitative examples, cultural analysis, RCT protocol, robustness analysis, visualisation documentation, interpretations guide) are available from the corresponding author upon request.

---

## Data Description

- **Type A profiles**: All Big Five traits set to +1 (boundary-condition high)
- **Type B profiles**: All Big Five traits set to −1 (boundary-condition low)
- **Scoring scale**: Yes = 2, Not Sure = 1, No = 0 (trinary)
- **Metrics per regulated turn**: Detection Accuracy, Regulation Effectiveness, Emotional Tone, Relevance & Coherence, Personality Needs Addressed (5 criteria)
- **Metrics per baseline turn**: Emotional Tone, Relevance & Coherence, Personality Needs Addressed (3 criteria)

## Requirements (for code)

```bash
pip install pandas numpy scipy matplotlib seaborn jupyter
```
