# Offline NVIDIA detection — analysis

- Run ID: `20260328T165906Z`
- Samples: 9 (multi-model × samples in batch)
- Results: `offline_detection_20260328T165906Z.jsonl`
- Mode: `five_trait_agents` (per-trait agents; rows include `five_agent_all_traits_ok`)

## Per-model metrics (Pearson on [-1,1], macro-averaged over traits)

| Model | n | macro Pearson (approx) |
|-------|---|------------------------|
| `meta/llama-3.1-70b-instruct` | 9 | 0.15 |
| `google/gemma-3-12b-it` | 8 | 0.04 |
| `meta/llama-3.3-70b-instruct` | 9 | -0.03 |
| `moonshotai/kimi-k2-instruct` | 9 | -0.06 |

Recompute exact Spearman / MAE in `OFFLINE-Detection-Analysis.ipynb` (offline section).

## Note on stale pins

If `ANALYSIS_LATEST.md` referenced an older failed run (e.g. all `predicted_ocean: null` from 429), the notebook used to **force** that file and show `n=0`. The notebook now keeps the **newest** `offline_detection_*.jsonl` by filename when the markdown run is older.
