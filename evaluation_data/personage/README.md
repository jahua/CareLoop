# PERSONAGE Evaluation

**Best for evaluation**: PERSONAGE has human ratings for **all 5 OCEAN traits** per utterance (unlike BIG5-CHAT, which annotates only one trait per sample).

**Detection is weak on PERSONAGE?** See [IMPROVEMENTS.md](./IMPROVEMENTS.md) for why and how to improve (style-aware prompt, heuristic cues, re-run eval).

## Schema

- **avg.extra, avg.ems, avg.agree, avg.consc, avg.open**: Human ratings 1–7
- **realization**: Utterance text (restaurant recommendations)

**Scale transformation (1–7 → [-1, 1]):**
- `(x - 4) / 3` for O, C, E, A. Neutral (4) → 0. Matches Big5Loop T in [-1,1]^5.
- Neuroticism: `N = -scale(EMS)` (high emotional stability → low N)

## Workflow

```bash
# 1. Preprocess (from evaluation_data/)
python scripts/preprocess_personage.py [--limit N]

# 2. Run evaluation (Big5Loop + N8N must be running)
python scripts/run_personage_eval.py [--limit N]

# 3. Visualize
python scripts/visualize_personage.py

# Demo (synthetic detected OCEAN when Big5Loop not running)
python scripts/visualize_personage.py --demo
```

## Outputs

- `personage/processed/personage_eval.jsonl` — preprocessed input
- `personage/processed/personage_eval_results.jsonl` — detected + ground truth OCEAN
- `personage/processed/personage_detected_vs_ground_truth.png` — scatter per trait
- `personage/processed/personage_metrics.png` — Pearson r, MAE per trait
- `personage/processed/personage_summary.csv` — per-sample comparison
