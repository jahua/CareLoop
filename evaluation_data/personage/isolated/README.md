# Isolated PERSONAGE Benchmark

This directory is a **benchmark-only workspace** for improving PERSONAGE alignment without changing the production Big5Loop workflow.

## Goal

Target: push PERSONAGE full-corpus performance as high as possible, with the aspirational goal of `r >= 0.75` on every trait.

Important note: that target is intentionally ambitious. The purpose of this isolated workspace is to optimize the benchmark setup cleanly and reproducibly before deciding what is realistic to report.

## Why isolated

The production workflow must remain tuned for caregiving conversations. PERSONAGE is a restaurant-domain benchmark with strong style manipulations. Mixing the two in one prompt creates conflicting objectives.

This workspace isolates:

- benchmark-only prompt tuning
- benchmark-only few-shot examples
- dev/test split discipline
- result analysis independent of the app workflow

## Files

- `prompt_bank.py`
  - benchmark-only system prompt
  - fixed few-shot exemplar ids
- `create_splits.py`
  - deterministic stratified split generator
  - forces all benchmark exemplars into the dev split
- `run_isolated_eval.py`
  - direct NVIDIA API evaluation on dev or test split
- `run_ensemble_eval.py`
  - multi-prompt ensemble evaluation for improving Pearson-r alignment
- `analyze_results.py`
  - quick per-trait `r` and MAE analysis
- `data/`
  - generated dev/test splits and split manifest
- `results/`
  - model outputs for each isolated benchmark run

## Protocol

1. Generate splits

```bash
cd evaluation_data/personage/isolated
python3 create_splits.py
```

2. Tune only on dev

```bash
export NVIDIA_API_KEY=...
python3 run_isolated_eval.py --split dev --model llama70b --temperature 0.1
python3 analyze_results.py results/dev_meta_llama-3_3-70b-instruct_t01.jsonl
```

3. Try the ensemble benchmark when single-prompt tuning plateaus

```bash
python3 run_ensemble_eval.py --split dev --model llama70b --temperature 0.1
python3 analyze_results.py results/dev_ensemble_benchmark-trait_first-anti_conflation_meta_llama-3_3-70b-instruct_t01.jsonl
```

4. When prompt/examples are frozen, run test once

```bash
python3 run_isolated_eval.py --split test --model llama70b --temperature 0.1
python3 analyze_results.py results/test_meta_llama-3_3-70b-instruct_t01.jsonl
```

Or, if the ensemble wins on dev:

```bash
python3 run_ensemble_eval.py --split test --model llama70b --temperature 0.1
python3 analyze_results.py results/test_ensemble_benchmark-trait_first-anti_conflation_meta_llama-3_3-70b-instruct_t01.jsonl
```

## Current benchmark strategy

The prompt bank uses 10 balanced examples covering:

- `agree_high`
- `agree_low`
- `consc_high`
- `consc_low`
- `ems_high`
- `ems_low`
- `open_high`
- `open_low`
- `random compare2`
- `random recommend`

This is meant to improve transfer across the full PERSONAGE corpus rather than only the earlier high-performing subset.

## Success criteria

Primary:

- improve mean full-corpus `r`
- improve weakest traits (`O`, `C`, `E`) without collapsing `A` or `N`

Stretch goal:

- `r >= 0.75` for all five traits on the test split

## Suggested next iterations

- vary only one thing at a time:
  - number of examples
  - system prompt wording
  - temperature
  - max tokens
- compare single-prompt vs ensemble runs on the same dev split
- keep the dev/test boundary strict
- log every run in `results/` instead of overwriting

## Important evaluation note

Simple affine trait calibration (`a * x + b`) can improve **MAE**, but it will not materially improve **Pearson r**. Since the benchmark goal here is stronger alignment (`r`), this workspace prioritizes:

- better prompt discrimination
- cleaner benchmark-only examples
- ensemble prompting
