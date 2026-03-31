# Five-Trait OCEAN Detectors

Five specialized LLM agents (one per Big Five trait: **O**penness, **C**onscientiousness, **E**xtraversion, **A**greeableness, **N**euroticism) evaluate Reddit posts from the PANDORA dataset. Each agent uses a trait-specific system prompt and few-shot examples to predict a score on a 1–5 scale.

## Directory layout

```
five_trait_detectors/
├── llama31_five_trait_detect.py   # Main script (default: meta/llama-3.1-70b-instruct)
├── llama33_five_trait_detect.py   # Variant using meta/llama-3.3-70b-instruct
├── merge_results.py               # Merge + deduplicate runs, compute correlation/MAE
├── Five-Trait-Analysis.ipynb       # Jupyter notebook for visualization & metrics
├── README.md                       # This file
└── results/
    ├── five_trait_ocean_<timestamp>.jsonl          # Individual run outputs
    ├── merged_five_trait_ocean_<timestamp>.jsonl   # Merged deduplicated runs
    ├── merged_five_trait_analysis_<timestamp>.json # Per-run analysis JSON
    └── merged_five_trait_metrics_<timestamp>.csv   # Trait-level metrics CSV
```

## Quick start

```bash
cd five_trait_detectors
python llama31_five_trait_detect.py --limit 500

# Merge all runs and compute metrics
python merge_results.py

# Then open Five-Trait-Analysis.ipynb
```

## Key flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `meta/llama-3.1-70b-instruct` | NVIDIA NIM model ID |
| `--limit` | `500` | Number of PANDORA samples to evaluate |
| `--n-shots` | `5` | Few-shot examples per agent |
| `--temperature` | `0.3` | Sampling temperature |
| `--timeout` | `45` | API timeout in seconds |
| `--input` | `pandora_eval_results_v4_20260327-1.jsonl` | Input PANDORA dataset |
| `--workflow` | `big5loop-pandora-eval-v4.json` | n8n prompt bundle |

## Output format (JSONL)

Each line is a JSON object:

```json
{
  "sample_id": "abc123",
  "model": "meta/llama-3.1-70b-instruct",
  "method": "multi_agent",
  "ground_truth_ocean": {"O": 3.2, "C": 4.1, "E": 2.8, "A": 3.5, "N": 2.0},
  "predicted_ocean": {"O": 3.0, "C": 4.0, "E": 3.0, "A": 3.5, "N": 2.5},
  "success": true,
  "agent_details": { ... },
  "timestamp": "2026-03-28T23:27:34Z"
}
```

- `success: true` = all 5 agents returned valid scores
- `method: "multi_agent"` = live API call

## Analysis notebook

`Five-Trait-Analysis.ipynb` loads the merged JSONL and computes:
- Per-trait Pearson r and MAE
- Scatter plots (predicted vs ground truth) per trait
