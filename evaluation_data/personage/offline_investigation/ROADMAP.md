# PERSONAGE Offline Investigation — Roadmap

**Objective:** Systematically optimize Big5Loop OCEAN detection on PERSONAGE (machine-generated restaurant utterances with human personality ratings), then benchmark the best strategy across multiple base models.

**Current baseline (Phase 4):** Mean Pearson r = 0.457 (Llama 3.3 70B, 7-shot, via N8N workflow).

**Target:** Mean Pearson r ≥ 0.60, with all traits r ≥ 0.40.

---

## Architecture

```
offline_investigation/
├── ROADMAP.md              ← this file
├── data/
│   ├── personage_dev.jsonl       ← 292 samples (tuning; 160 full OCEAN + 132 E-only)
│   └── personage_test.jsonl      ← 288 samples (held-out; 160 full OCEAN + 128 E-only)
├── scripts/
│   ├── prepare_data.py           ← copy splits from isolated/, verify
│   ├── prompt_bank.py            ← all prompt strategies (expanded)
│   ├── harness_personage.py      ← Phase 1: prompt × shot × temp grid
│   ├── benchmark_models.py       ← Phase 2: best prompt × multiple models
│   └── calibration.py            ← optional post-hoc calibration
├── results/
│   ├── harness_*.jsonl           ← per-sample predictions per config
│   └── benchmark_*.jsonl         ← multi-model benchmark outputs
└── analysis/
    ├── Harness-Analysis.ipynb    ← Phase 1 analysis notebook
    └── Benchmark-Analysis.ipynb  ← Phase 2 multi-model analysis
```

---

## Phase 1: Prompt Harness (find optimal prompt strategy)

**Goal:** Determine best prompt × few-shot × temperature on dev set using a single model.

**Grid:**
- Model: `meta/llama-3.3-70b-instruct` (fixed)
- Prompts: 6+ strategies from prompt_bank.py
  - `strict_style` — minimal, style-only instruction (Pandora winner)
  - `benchmark` — detailed trait rubric (existing)
  - `trait_first` — step-by-step per-trait (existing)
  - `anti_conflation` — explicit topic-independence (existing)
  - `minimal` — bare minimum instruction
  - `contrastive` — high/low pole descriptions per trait
- Few-shots: 0, 3, 5, 10, 11 (all exemplars)
- Temperature: 0.1, 0.3
- Data: dev split (292 samples: 160 full OCEAN, 132 E-only)

**Metrics:** Per-trait Pearson r, macro r, MAE, coverage, composite.

**Output:** `results/harness_<run_id>.jsonl`, analysis in `analysis/Harness-Analysis.ipynb`.

**Success criteria:** Identify one prompt config with macro r ≥ 0.50.

---

## Phase 2: Multi-Model Benchmark (compare base models)

**Goal:** Run the Phase 1 winning prompt config across multiple models.

**Models (via JuLing API):**
- `meta/llama-3.3-70b-instruct`
- `meta/llama-3.1-70b-instruct`
- `moonshotai/kimi-k2-instruct`
- `google/gemma-3-12b-it`
- (others as available on the API)

**Fixed config:** Winning prompt + shots + temp from Phase 1.

**Data:** dev split first, then test split (single final run per model).

**Output:** `results/benchmark_<run_id>.jsonl`, analysis in `analysis/Benchmark-Analysis.ipynb`.

**Success criteria:** Identify best single model AND whether model ensemble improves over best single.

---

## Phase 3: Final Test Evaluation

**Goal:** Run best config(s) on held-out test split exactly once.

**Protocol:**
1. Freeze prompt, shots, temp from Phase 1.
2. Run each Phase 2 model on test (160 samples).
3. Report final per-trait r, MAE, bias with bootstrap 95% CIs.
4. Compare to Phase 4 baseline (r=0.457) and document delta.

---

## Key Differences from Pandora Investigation

| Aspect | Pandora | PERSONAGE |
|--------|---------|-----------|
| Text source | Real Reddit posts | Machine-generated (NLG) |
| GT source | Self-report BFI | Human raters judging text |
| GT–text alignment | Weak (ceiling r≈0.10) | Strong (achievable r≈0.50+) |
| Optimization potential | Low (bottleneck is data, not prompt) | High (prompt engineering matters) |
| Few-shot domain | Mismatched (Reddit posts ≠ restaurant reviews) | Matched (same domain) |

---

## Dependencies

- JuLing API key (env: `JULING_API_KEY`, `JULING_API_URL`)
- Python 3.10+, `requests`
- Data: `personage_dev.jsonl` (292), `personage_test.jsonl` (288) — 580 total from `processed/personage_eval.jsonl`
