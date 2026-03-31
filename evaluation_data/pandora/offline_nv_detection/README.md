# Offline NVIDIA detection (no N8N)

Runs the **same** three system prompts and **20 few-shots** as `workflows/n8n/big5loop-pandora-eval-v4.json` (`Zurich Model Detection (EMA)`), calls the **NVIDIA Chat Completions** API directly, and averages the three variants’ JSON outputs (same ensemble idea as the workflow).

## Requirements

- `NVIDIA_API_KEY` (required; loaded from shell env, fallback to repo `.env`)
- `NVIDIA_API_URL` (optional; default `https://integrate.api.nvidia.com/v1/chat/completions`)
- Python packages: `requests`, `pandas` (same as `evaluation_data/requirements-eval.txt`)

## Run (20 samples, stable pool)

From Big5Loop repo root:

```bash
cd evaluation_data/pandora/offline_nv_detection
export NVIDIA_API_KEY="your-key"
python3 run_offline_detection.py --limit 20
```

Pool presets:

```bash
# Stable (fewer 404 surprises)
python3 run_offline_detection.py --limit 20 --pool stable

# Broader pool (Google/Qwen/DeepSeek/Moonshot candidates included)
python3 run_offline_detection.py --limit 20 --pool broad --max-workers 2

# Psychometric-focused candidates
python3 run_offline_detection.py --limit 20 --pool psychometric --max-workers 2
```

Custom models (comma-separated NVIDIA route names; overrides pool):

```bash
python3 run_offline_detection.py --limit 20 \
  --models "meta/llama-3.3-70b-instruct,mistralai/mistral-nemo-12b-instruct-2407"
```

Run multiple models simultaneously:

```bash
python3 run_offline_detection.py --limit 20 --max-workers 6 \
  --models "meta/llama-3.3-70b-instruct,meta/llama-3.1-70b-instruct,meta/llama-3.1-8b-instruct,mistralai/mistral-nemo-12b-instruct-2407"
```

For model route names and availability, check [NVIDIA model catalog](https://build.nvidia.com/models).

Notes:
- Some models may return `404 model_not_found` depending on your NVIDIA account access.
- Higher parallelism can cause `429 rate_limit`; reduce `--max-workers` for fair comparison.

## Outputs (under `results/`)

- `offline_detection_<UTC-timestamp>.jsonl` — one line per `(sample_id, model)` with `predicted_ocean`, `ground_truth_ocean`, and per-variant raw output.
- `ANALYSIS_<UTC-timestamp>.md` — macro Pearson / Spearman / MAE per model.
- `ANALYSIS_LATEST.md` — copy of the last analysis for quick viewing.

`results/` may contain API outputs; keep local or gitignore as you prefer.

## Note

This does **not** run the full Big5Loop N8N pipeline (routing, EMA from DB, generation). It isolates **detection only** for model comparison.
