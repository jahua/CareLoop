#!/usr/bin/env python3
"""
Prompt & Model Harness Engineering for Big Five (OCEAN) Detection.

Systematic grid search over (model × prompt_set × few_shot_count) to find the
best configuration for personality detection on PANDORA evaluation data.

Features:
  - Multi-model × multi-prompt grid search
  - 8 prompt-set strategies (4 original + 4 new research-informed)
  - Few-shot ablation (0, 5, 10, 20 shots)
  - Per-trait Pearson / Spearman / MAE / bias
  - Bootstrap 95% CI on macro Pearson
  - Automatic winner selection → BEST_CONFIG.json
  - Resume from partial runs

Outputs under results/:
  harness_<run_id>.jsonl        — raw per-sample results
  ANALYSIS_harness_<run_id>.md  — full analysis report
  BEST_CONFIG_<run_id>.json     — winning configuration
  ANALYSIS_LATEST_HARNESS.md    — copy of latest analysis

Usage:
  python3 benchmark_llama33_prompt_tuning.py --limit 50 --pool stable
  python3 benchmark_llama33_prompt_tuning.py --limit 100 --models "meta/llama-3.3-70b-instruct"
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

# ── Constants ──────────────────────────────────────────────────────────────────

TRAITS = ("O", "C", "E", "A", "N")
TRAIT_LABELS = {
    "O": "Openness",
    "C": "Conscientiousness",
    "E": "Extraversion",
    "A": "Agreeableness",
    "N": "Neuroticism",
}

MODEL_POOLS: dict[str, list[str]] = {
    "thesis_final": [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "moonshotai/kimi-k2-instruct",
        "google/gemma-3-12b-it",
    ],
    "stable": [
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "google/gemma-3-27b-it",
    ],
    "broad": [
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.3-70b-instruct",
        "google/gemma-3-27b-it",
        "google/gemma-3-12b-it",
        "qwen/qwen2.5-72b-instruct",
        "qwen/qwen2.5-32b-instruct",
        "deepseek-ai/deepseek-r1",
        "deepseek-ai/deepseek-v3",
        "moonshotai/kimi-k2-instruct",
        "mistralai/mistral-nemo-12b-instruct-2407",
        "mistralai/mixtral-8x7b-instruct-v0.1",
    ],
    "psychometric": [
        "meta/llama-3.3-70b-instruct",
        "meta/llama-3.1-70b-instruct",
        "google/gemma-3-27b-it",
        "qwen/qwen2.5-72b-instruct",
        "deepseek-ai/deepseek-r1",
        "moonshotai/kimi-k2-instruct",
    ],
    "single_llama33": [
        "meta/llama-3.3-70b-instruct",
    ],
    "single_llama31": [
        "meta/llama-3.1-70b-instruct",
    ],
}

FEW_SHOT_COUNTS = [0, 5, 10, 20]

BOOTSTRAP_N = 1000
BOOTSTRAP_SEED = 42

# ── Prompt Library ─────────────────────────────────────────────────────────────


def _workflow_prompt_sets(
    workflow_variants: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """Original 4 prompt sets from the initial benchmark."""

    strict_style = [
        {
            "name": "strict_style",
            "system": (
                "You are a psychometric rater. Infer Big Five O,C,E,A,N from writing style only. "
                "Ignore topic popularity, morality, and factual correctness. "
                "Return only JSON with O,C,E,A,N in [-1,1]."
            ),
        },
        {
            "name": "strict_anti_confound",
            "system": (
                "Avoid confounds: positivity != A, verbosity != O/C, argument confidence != E, "
                "stress topic != N without dysregulated style. Traits independent. Return only JSON."
            ),
        },
        {
            "name": "strict_anchor",
            "system": (
                "Use evidence thresholds: strong(|x|>=0.6), moderate(0.25-0.6), weak(<0.25). "
                "If evidence mixed, move score toward 0. Return JSON only with O,C,E,A,N."
            ),
        },
    ]

    lowA_control = [
        {
            "name": "lowA_control_main",
            "system": (
                "Rate O,C,E,A,N from interpersonal stance and discourse behavior. "
                "Normative/controlling/judgmental tone can reduce Agreeableness even without profanity. "
                "Return JSON only in [-1,1]."
            ),
        },
        {
            "name": "lowA_control_aux",
            "system": (
                "Check A carefully: empathy/cooperation/tact -> +A; contempt/dismissiveness/moralizing -> -A. "
                "Do not boost A from polite wording alone. Return JSON only."
            ),
        },
        {
            "name": "lowA_control_balance",
            "system": (
                "Separate C from A: organized language can coexist with low A. "
                "Separate E from A: assertive style can be low A. Return JSON only."
            ),
        },
    ]

    lowOC_guard = [
        {
            "name": "lowOC_guard_main",
            "system": (
                "Long detailed text is not automatically high O or high C. "
                "Score O from novelty/abstraction, C from consistency/planfulness. Return JSON only."
            ),
        },
        {
            "name": "lowOC_guard_aux",
            "system": (
                "If text repeats points, is rigid, or prescriptive, consider lower O even when long. "
                "If reasoning is selective or impulsive, lower C. Return JSON only."
            ),
        },
        {
            "name": "lowOC_guard_balance",
            "system": (
                "Traits independent. Use weak scores near 0 when uncertain. "
                'Output strict JSON {"O":float,"C":float,"E":float,"A":float,"N":float}.'
            ),
        },
    ]

    return {
        "workflow_current": workflow_variants,
        "strict_style_v1": strict_style,
        "lowA_control_v1": lowA_control,
        "lowOC_guard_v1": lowOC_guard,
    }


def _new_prompt_sets() -> dict[str, list[dict[str, str]]]:
    """4 new research-informed prompt strategies."""

    chain_of_thought = [
        {
            "name": "cot_main",
            "system": (
                "You are an expert psychometric rater. For the given message, think step-by-step:\n"
                "1. What is the INTERPERSONAL STANCE? (cooperative, hostile, neutral, assertive)\n"
                "2. What is the EMOTIONAL REGULATION style? (calm, anxious, reactive, volatile)\n"
                "3. What is the COGNITIVE STYLE? (rigid, curious, structured, chaotic)\n"
                "4. What is the SOCIAL ENERGY? (withdrawn, engaged, dominant, passive)\n"
                "5. What is the CONSCIENTIOUSNESS signal? (planful, impulsive, organized, careless)\n\n"
                "Then map to O,C,E,A,N in [-1,1] based on your analysis.\n"
                "Output your reasoning in 1-2 sentences, then return ONLY the JSON on the last line:\n"
                '{"O": float, "C": float, "E": float, "A": float, "N": float}'
            ),
        },
        {
            "name": "cot_debiased",
            "system": (
                "Before scoring, check for these common biases:\n"
                "- Halo effect: one strong trait spilling into unrelated traits\n"
                "- Length bias: long text ≠ high O or C\n"
                "- Positivity bias: friendly tone ≠ high A if controlling\n"
                "- Confidence bias: assertive argumentation ≠ high E\n"
                "Score each trait INDEPENDENTLY. Return JSON only."
            ),
        },
        {
            "name": "cot_calibrator",
            "system": (
                "Calibrate your scores:\n"
                "- |score| > 0.7: requires STRONG, unambiguous evidence\n"
                "- |score| 0.3-0.7: moderate evidence from multiple cues\n"
                "- |score| < 0.3: weak or mixed evidence — default toward 0\n"
                "Return JSON only with O,C,E,A,N in [-1,1]."
            ),
        },
    ]

    calibrated_rubric = [
        {
            "name": "rubric_main",
            "system": (
                "Rate Big Five traits using this behavioral rubric:\n\n"
                "O (Openness): +1 = exploratory, abstract, novel framing, intellectual curiosity. "
                "-1 = rigid, literal, conventional, closed to new ideas. 0 = neutral.\n\n"
                "C (Conscientiousness): +1 = structured, planful, disciplined, detail-oriented. "
                "-1 = impulsive, disorganized, inconsistent, careless. 0 = neutral.\n\n"
                "E (Extraversion): +1 = socially energized, assertive, enthusiastic, talkative. "
                "-1 = reserved, withdrawn, solitary, quiet. 0 = neutral.\n\n"
                "A (Agreeableness): +1 = empathic, cooperative, warm, trusting. "
                "-1 = hostile, contemptuous, competitive, suspicious. 0 = neutral.\n\n"
                "N (Neuroticism): +1 = anxious, reactive, ruminative, emotionally volatile. "
                "-1 = calm, stable, emotionally regulated, resilient. 0 = neutral.\n\n"
                "Score ONLY from writing style and interpersonal behavior, not content topic.\n"
                'Return JSON: {"O": float, "C": float, "E": float, "A": float, "N": float}'
            ),
        },
        {
            "name": "rubric_anti_confound",
            "system": (
                "Critical checks before scoring:\n"
                "- Discussing stress ≠ high N (look for dysregulated STYLE)\n"
                "- Being polite ≠ high A (look for genuine empathy vs social performance)\n"
                "- Writing a lot ≠ high O/C (look for actual novelty/structure)\n"
                "- Strong opinions ≠ high E (look for social energy, not just confidence)\n"
                "- Organized argument ≠ high C if the reasoning is motivated/selective\n"
                "Return JSON only."
            ),
        },
        {
            "name": "rubric_independence",
            "system": (
                "IMPORTANT: Each trait is independent. Common mistakes:\n"
                "- High C does not imply high A (organized ≠ agreeable)\n"
                "- High E does not imply high A (assertive ≠ cooperative)\n"
                "- High O does not imply low C (creative ≠ disorganized)\n"
                "- Low A does not imply high N (hostile ≠ anxious)\n"
                "Score each trait from its OWN evidence only. Return JSON."
            ),
        },
    ]

    contrastive = [
        {
            "name": "contrastive_main",
            "system": (
                "For each Big Five trait, consider both directions:\n\n"
                "O: Would this person explore novel ideas (high O)? Or stick to convention (low O)?\n"
                "C: Would this person plan carefully (high C)? Or act impulsively (low C)?\n"
                "E: Would this person seek social engagement (high E)? Or prefer solitude (low E)?\n"
                "A: Would this person show genuine warmth (high A)? Or be dismissive/hostile (low A)?\n"
                "N: Does this person show emotional instability (high N)? Or steady resilience (low N)?\n\n"
                "Pick the direction supported by evidence. Use 0 if unclear.\n"
                'Return JSON: {"O": float, "C": float, "E": float, "A": float, "N": float}'
            ),
        },
        {
            "name": "contrastive_evidence",
            "system": (
                "For each trait, list one piece of evidence supporting positive direction and one "
                "supporting negative direction. Score toward whichever has stronger evidence. "
                "If balanced, score near 0. Return JSON only."
            ),
        },
        {
            "name": "contrastive_calibration",
            "system": (
                "Avoid extreme scores (|x| > 0.8) unless evidence is overwhelming. "
                "Most real people cluster in [-0.5, 0.5] for most traits. "
                "Extreme scores should be rare. Return JSON only."
            ),
        },
    ]

    minimal_instruction = [
        {
            "name": "minimal_main",
            "system": (
                "Rate O,C,E,A,N from this message. Each trait in [-1,1].\n"
                "Return JSON only: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
            ),
        },
        {
            "name": "minimal_style",
            "system": (
                "Rate Big Five personality from writing style. "
                "JSON only: {\"O\": float, \"C\": float, \"E\": float, \"A\": float, \"N\": float}"
            ),
        },
        {
            "name": "minimal_no_bias",
            "system": (
                "Big Five O,C,E,A,N from text. Style only, not topic. "
                "Each in [-1,1]. JSON only."
            ),
        },
    ]

    correlation_focus = [
        {
            "name": "corr_focus_main",
            "system": (
                "You are a psychometric rater for O,C,E,A,N in [-1,1]. "
                "Avoid central tendency bias: use 0 only when evidence is weak or mixed. "
                "When evidence is clear, use at least moderate magnitude (|x| >= 0.3). "
                "Infer traits from style and interpersonal behavior, not topic. "
                'Return strict JSON only: {"O": float, "C": float, "E": float, "A": float, "N": float}'
            ),
        },
        {
            "name": "corr_focus_trait_independence",
            "system": (
                "Score each trait independently:\n"
                "O novelty/abstraction vs rigidity;\n"
                "C planfulness vs impulsivity;\n"
                "E social energy/assertiveness vs reserve;\n"
                "A empathy/cooperation vs hostility/contempt;\n"
                "N emotional reactivity vs stability.\n"
                "Do not copy one trait signal into others. Return JSON only."
            ),
        },
        {
            "name": "corr_focus_calibration",
            "system": (
                "Calibration rubric:\n"
                "- strong evidence -> |x| in [0.6, 1.0]\n"
                "- moderate evidence -> |x| in [0.3, 0.6)\n"
                "- weak/mixed evidence -> |x| < 0.3\n"
                "Use the sign supported by evidence; do not default positive. Return JSON only."
            ),
        },
    ]

    return {
        "chain_of_thought_v1": chain_of_thought,
        "calibrated_rubric_v1": calibrated_rubric,
        "contrastive_v1": contrastive,
        "minimal_instruction_v1": minimal_instruction,
        "correlation_focus_v1": correlation_focus,
    }


# ── Parsing & Utils ────────────────────────────────────────────────────────────


def clamp(v: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def parse_ocean(raw: str | None) -> dict[str, float] | None:
    """Extract OCEAN JSON from LLM output, tolerating markdown fences and preamble."""
    if not raw:
        return None
    s = raw.strip()
    # Strip markdown fence
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", s, re.I)
    if fence:
        s = fence.group(1).strip()
    start = s.find("{")
    if start < 0:
        return None
    depth = 0
    end = -1
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        return None
    try:
        obj = json.loads(s[start : end + 1])
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict):
        return None

    out: dict[str, float] = {}
    for t in TRAITS:
        v = obj.get(t)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out[t] = clamp(float(v))
        elif isinstance(v, str) and v.strip():
            try:
                out[t] = clamp(float(v.strip()))
            except ValueError:
                return None
        else:
            return None
    return out


def load_workflow_prompt_and_fewshot(
    workflow_path: Path,
) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
    """Extract prompt variants and few-shots from the n8n workflow JSON."""
    wf = json.loads(workflow_path.read_text(encoding="utf-8"))[0]
    code = None
    for n in wf["nodes"]:
        if n.get("name") == "Zurich Model Detection (EMA)":
            code = n["parameters"]["jsCode"]
            break
    if not code:
        raise RuntimeError("Detection node not found")

    pv_block = code[code.find("const promptVariants = [") : code.find("const fewShot = [")]
    variants = []
    for name, body in re.findall(r'name:"([^"]+)",system:"((?:[^"\\]|\\.)*)"', pv_block):
        variants.append({"name": name, "system": bytes(body, "utf-8").decode("unicode_escape")})

    fs_block = code[code.find("const fewShot = [") : code.find("const parseOcean =")]
    few_shots: list[tuple[str, str]] = []
    for u, a in re.findall(r'\{u:"((?:[^"\\]|\\.)*)",a:\'(\{[^}]+\})\'\}', fs_block):
        few_shots.append((bytes(u, "utf-8").decode("unicode_escape"), a))

    return variants, few_shots


# ── API Calls ──────────────────────────────────────────────────────────────────


def build_messages(
    system: str,
    few_shots: list[tuple[str, str]],
    user_text: str,
    n_shots: int = 20,
    max_chars: int = 600,
) -> list[dict[str, str]]:
    """Build chat messages with system prompt, N few-shot examples, and user text."""
    msgs: list[dict[str, str]] = [{"role": "system", "content": system}]
    selected = few_shots[:n_shots] if n_shots > 0 else []
    for u, a in selected:
        msgs.append({"role": "user", "content": f'Utterance: "{u}"'})
        msgs.append({"role": "assistant", "content": a})
    msgs.append({"role": "user", "content": f'Utterance: "{user_text[:max_chars]}"'})
    return msgs


def call_variant(
    session: requests.Session,
    api_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: int,
    retries: int,
    retry_backoff: float,
) -> tuple[str | None, str | None]:
    """Call the NVIDIA API with retries and exponential backoff."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            r = session.post(
                api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.05,
                    "max_tokens": 200,
                },
                timeout=timeout,
            )
            status = r.status_code
            if status == 404:
                return None, f"404 model_not_found: {model}"
            if status in (429, 500, 502, 503, 504):
                last_err = f"{status} transient"
                if attempt < retries:
                    time.sleep(retry_backoff * (2**attempt))
                    continue
            r.raise_for_status()
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content")
            return (content if isinstance(content, str) else str(content)), None
        except Exception as e:
            last_err = str(e)
            transient = any(
                k in last_err
                for k in ["429", "timeout", "timed out", "503", "502", "500", "connection reset"]
            )
            if transient and attempt < retries:
                time.sleep(retry_backoff * (2**attempt))
                continue
            break
    return None, last_err


# ── Evaluation Core ────────────────────────────────────────────────────────────


def eval_single_config(
    sample: dict[str, Any],
    model: str,
    prompt_set_name: str,
    variants: list[dict[str, str]],
    few_shots: list[tuple[str, str]],
    n_shots: int,
    api_url: str,
    api_key: str,
    timeout: int,
    retries: int,
    retry_backoff: float,
) -> dict[str, Any]:
    """Evaluate a single (sample, model, prompt_set, n_shots) combination."""
    session = requests.Session()
    valids: list[dict[str, float]] = []
    details: list[dict[str, Any]] = []
    text = str(sample.get("input") or sample.get("text") or "")

    for v in variants:
        msgs = build_messages(v["system"], few_shots, text, n_shots=n_shots)
        raw, err = call_variant(session, api_url, api_key, model, msgs, timeout, retries, retry_backoff)
        oc = parse_ocean(raw) if raw else None
        details.append({"variant": v["name"], "error": err, "ocean": oc, "raw_excerpt": (raw or "")[:200]})
        if oc:
            valids.append(oc)

    # Ensemble: average valid variants
    pred = None
    if valids:
        pred = {t: clamp(sum(v[t] for v in valids) / len(valids)) for t in TRAITS}

    # Also track best single variant (highest coverage of traits)
    best_single = None
    if valids:
        best_single = valids[0]  # first valid

    return {
        "sample_id": sample.get("sample_id"),
        "model": model,
        "prompt_set": prompt_set_name,
        "n_shots": n_shots,
        "ground_truth_ocean": sample.get("ground_truth_ocean") or {},
        "predicted_ocean": pred,
        "n_valid_variants": len(valids),
        "n_total_variants": len(variants),
        "variant_details": details,
    }


# ── Metrics ────────────────────────────────────────────────────────────────────


def compute_metrics(rows: list[dict[str, Any]], total_rows: int) -> dict[str, Any]:
    """Compute comprehensive metrics for a set of evaluation results."""
    ok = [r for r in rows if r.get("predicted_ocean")]
    n = len(ok)
    if n == 0:
        return {
            "n": 0,
            "coverage": 0.0,
            "macro_pearson": float("nan"),
            "macro_spearman": float("nan"),
            "macro_mae": float("nan"),
            "per_trait": {},
            "macro_bias": float("nan"),
        }

    trait_metrics: dict[str, dict[str, float]] = {}
    pears, spears, maes, biases = [], [], [], []

    for t in TRAITS:
        gt = pd.Series([float((r["ground_truth_ocean"] or {}).get(t, 0.0)) for r in ok])
        pr = pd.Series([float((r["predicted_ocean"] or {}).get(t, 0.0)) for r in ok])

        pear = float(gt.corr(pr, method="pearson")) if gt.std() > 0 and pr.std() > 0 else 0.0
        spear = (
            float(gt.rank().corr(pr.rank(), method="pearson"))
            if gt.std() > 0 and pr.std() > 0
            else 0.0
        )
        mae = float((pr - gt).abs().mean())
        bias = float((pr - gt).mean())  # mean signed error

        trait_metrics[t] = {
            "pearson": pear,
            "spearman": spear,
            "mae": mae,
            "bias": bias,
            "gt_mean": float(gt.mean()),
            "gt_std": float(gt.std()),
            "pred_mean": float(pr.mean()),
            "pred_std": float(pr.std()),
        }
        pears.append(pear)
        spears.append(spear)
        maes.append(mae)
        biases.append(bias)

    macro_pearson = float(np.mean(pears))

    # Bootstrap 95% CI on macro Pearson
    ci_lo, ci_hi = _bootstrap_ci_macro_pearson(ok)

    # Parse failure rate
    all_variants = sum(r.get("n_total_variants", 0) for r in rows)
    failed_variants = sum(r.get("n_total_variants", 0) - r.get("n_valid_variants", 0) for r in rows)
    parse_fail_rate = failed_variants / all_variants if all_variants > 0 else 0.0

    return {
        "n": n,
        "coverage": float(n / total_rows) if total_rows else 0.0,
        "macro_pearson": macro_pearson,
        "macro_spearman": float(np.mean(spears)),
        "macro_mae": float(np.mean(maes)),
        "macro_bias": float(np.mean(biases)),
        "per_trait": trait_metrics,
        "bootstrap_ci_95": (ci_lo, ci_hi),
        "parse_fail_rate": parse_fail_rate,
    }


def _bootstrap_ci_macro_pearson(
    ok: list[dict[str, Any]],
    n_boot: int = BOOTSTRAP_N,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, float]:
    """Bootstrap 95% CI on macro Pearson r."""
    if len(ok) < 5:
        return (float("nan"), float("nan"))

    rng = np.random.RandomState(seed)
    boot_rs: list[float] = []

    for _ in range(n_boot):
        idx = rng.choice(len(ok), size=len(ok), replace=True)
        sample = [ok[i] for i in idx]
        pears = []
        for t in TRAITS:
            gt = pd.Series([float((r["ground_truth_ocean"] or {}).get(t, 0.0)) for r in sample])
            pr = pd.Series([float((r["predicted_ocean"] or {}).get(t, 0.0)) for r in sample])
            pear = float(gt.corr(pr, method="pearson")) if gt.std() > 0 and pr.std() > 0 else 0.0
            pears.append(pear)
        boot_rs.append(float(np.mean(pears)))

    return (float(np.percentile(boot_rs, 2.5)), float(np.percentile(boot_rs, 97.5)))


def composite_score(m: dict[str, Any]) -> float:
    """Composite ranking: 0.5*pearson + 0.3*coverage + 0.2*(1-mae)."""
    if m["n"] == 0:
        return float("-inf")
    pearson = m["macro_pearson"] if not np.isnan(m["macro_pearson"]) else 0.0
    coverage = m["coverage"]
    mae = m["macro_mae"] if not np.isnan(m["macro_mae"]) else 1.0
    return 0.5 * pearson + 0.3 * coverage + 0.2 * (1.0 - mae)


def rank_value(m: dict[str, Any], objective: str, min_coverage: float) -> float:
    """Ranking value with optional coverage floor."""
    if m["n"] == 0 or m.get("coverage", 0.0) < min_coverage:
        return float("-inf")
    if objective == "pearson":
        pearson = m.get("macro_pearson", float("nan"))
        return pearson if not np.isnan(pearson) else float("-inf")
    return composite_score(m)


def config_eligible(
    m: dict[str, Any], objective: str, min_coverage: float
) -> bool:
    """True if this config should appear in leaderboard / winner selection."""
    return rank_value(m, objective, min_coverage) > float("-inf")


# ── Report Generation ──────────────────────────────────────────────────────────


def generate_report(
    all_metrics: dict[str, dict[str, Any]],
    run_id: str,
    models: list[str],
    prompt_sets: dict[str, list[dict[str, str]]],
    n_samples: int,
    n_shots_list: list[int],
    args: argparse.Namespace,
) -> str:
    """Generate the full markdown analysis report."""
    lines: list[str] = []
    lines.append("# 🔬 Prompt & Model Harness Engineering Report")
    lines.append("")
    lines.append(f"- **Run ID**: `{run_id}`")
    lines.append(f"- **Samples**: {n_samples}")
    lines.append(f"- **Models**: {', '.join(f'`{m}`' for m in models)}")
    lines.append(f"- **Prompt sets**: {', '.join(f'`{k}`' for k in prompt_sets)}")
    lines.append(f"- **Few-shot counts (this run)**: {n_shots_list}")
    lines.append(f"- **Total configs**: {len(all_metrics)}")
    lines.append(f"- **Retries**: {args.retries}, backoff: {args.retry_backoff}s")
    lines.append(f"- **Ranking objective**: `{args.objective}` (min coverage {args.min_coverage:.0%})")
    lines.append("")

    # ── Leaderboard ──
    ranked = sorted(
        all_metrics.items(),
        key=lambda x: rank_value(x[1], args.objective, args.min_coverage),
        reverse=True,
    )

    ranked_eligible = [
        (k, m)
        for k, m in ranked
        if config_eligible(m, args.objective, args.min_coverage)
    ]
    no_pred = [k for k, m in all_metrics.items() if m["n"] == 0]
    low_cov = [
        k
        for k, m in all_metrics.items()
        if m["n"] > 0 and m.get("coverage", 0.0) < args.min_coverage
    ]

    lines.append("## 🏆 Leaderboard (Top 20)")
    lines.append("")
    lines.append(
        "Configs with **no predictions** or **coverage below the floor** are **skipped** "
        "(not ranked). Same rule applies to model/prompt/few-shot aggregations below."
    )
    lines.append("")
    lines.append(
        "| Rank | Model | Prompt Set | Shots | n | Coverage | Macro r | 95% CI | Macro ρ | Macro MAE | Composite |"
    )
    lines.append(
        "|------|-------|------------|-------|---|----------|---------|--------|---------|-----------|-----------|"
    )
    if not ranked_eligible:
        lines.append("| — | *none* | *no eligible configs* | — | 0 | — | — | — | — | — | — |")
    for rank_idx, (key, m) in enumerate(ranked_eligible[:20], start=1):
        ci = m.get("bootstrap_ci_95", (float("nan"), float("nan")))
        ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if not np.isnan(ci[0]) else "—"
        model, ps, ns = key.split("|")
        comp = composite_score(m)
        lines.append(
            f"| {rank_idx} | `{model}` | `{ps}` | {ns} | {m['n']} | {m['coverage']:.0%} "
            f"| {m['macro_pearson']:.4f} | {ci_str} | {m['macro_spearman']:.4f} "
            f"| {m['macro_mae']:.4f} | {comp:.4f} |"
        )

    lines.append("")
    lines.append("## ⏭️ Skipped configs (not ranked)")
    lines.append("")
    if no_pred:
        lines.append(f"- **No predictions** (`n=0`): {len(no_pred)} config(s)")
        for k in sorted(no_pred)[:30]:
            lines.append(f"  - `{k}`")
        if len(no_pred) > 30:
            lines.append(f"  - … and {len(no_pred) - 30} more")
    if low_cov:
        lines.append(
            f"- **Below coverage floor** (below {args.min_coverage:.0%}): {len(low_cov)} config(s)"
        )
        for k in sorted(low_cov)[:30]:
            lines.append(f"  - `{k}`")
        if len(low_cov) > 30:
            lines.append(f"  - … and {len(low_cov) - 30} more")
    if not no_pred and not low_cov:
        lines.append("- *None* (all configs met the floor and had predictions).")
    lines.append("")

    # ── Per-Trait Analysis for Top 5 ──
    lines.append("## 📊 Per-Trait Analysis (Top 5 eligible configs)")
    lines.append("")

    if not ranked_eligible:
        lines.append("*No eligible configs — section skipped.*")
        lines.append("")
    for rank_idx, (key, m) in enumerate(ranked_eligible[:5], start=1):
        model, ps, ns = key.split("|")
        lines.append(f"### #{rank_idx}: `{model}` / `{ps}` / {ns}-shot")
        lines.append("")
        lines.append("| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |")
        lines.append("|-------|---------|----------|-----|------|--------|----------|")

        per_trait = m.get("per_trait", {})
        for t in TRAITS:
            tm = per_trait.get(t, {})
            if not tm:
                continue
            lines.append(
                f"| **{t}** ({TRAIT_LABELS[t]}) "
                f"| {tm['pearson']:.4f} | {tm['spearman']:.4f} "
                f"| {tm['mae']:.4f} | {tm['bias']:+.4f} "
                f"| {tm['gt_mean']:.2f}±{tm['gt_std']:.2f} "
                f"| {tm['pred_mean']:.2f}±{tm['pred_std']:.2f} |"
            )
        lines.append("")

    # ── Model Comparison (aggregated across prompt sets) ──
    model_agg: dict[str, list[float]] = {}
    for key, m in all_metrics.items():
        if not config_eligible(m, args.objective, args.min_coverage):
            continue
        model_name = key.split("|")[0]
        model_agg.setdefault(model_name, []).append(composite_score(m))

    if model_agg:
        lines.append("## 🤖 Model Comparison (avg composite across all prompt sets)")
        lines.append("")
        lines.append("| Model | Avg Composite | Best Composite | # Configs |")
        lines.append("|-------|--------------|----------------|-----------|")
        for model_name in sorted(model_agg, key=lambda x: np.mean(model_agg[x]), reverse=True):
            scores = model_agg[model_name]
            lines.append(
                f"| `{model_name}` | {np.mean(scores):.4f} | {max(scores):.4f} | {len(scores)} |"
            )
        lines.append("")

    # ── Prompt Set Comparison (aggregated across models) ──
    ps_agg: dict[str, list[float]] = {}
    for key, m in all_metrics.items():
        if not config_eligible(m, args.objective, args.min_coverage):
            continue
        ps_name = key.split("|")[1]
        ps_agg.setdefault(ps_name, []).append(composite_score(m))

    if ps_agg:
        lines.append("## 📝 Prompt Set Comparison (avg composite across all models)")
        lines.append("")
        lines.append("| Prompt Set | Avg Composite | Best Composite | # Configs |")
        lines.append("|------------|--------------|----------------|-----------|")
        for ps_name in sorted(ps_agg, key=lambda x: np.mean(ps_agg[x]), reverse=True):
            scores = ps_agg[ps_name]
            lines.append(
                f"| `{ps_name}` | {np.mean(scores):.4f} | {max(scores):.4f} | {len(scores)} |"
            )
        lines.append("")

    # ── Few-Shot Ablation ──
    fs_agg: dict[int, list[float]] = {}
    for key, m in all_metrics.items():
        if not config_eligible(m, args.objective, args.min_coverage):
            continue
        ns = int(key.split("|")[2])
        fs_agg.setdefault(ns, []).append(composite_score(m))

    if fs_agg:
        lines.append("## 🎯 Few-Shot Ablation")
        lines.append("")
        lines.append("| # Shots | Avg Composite | Avg Macro r | # Configs |")
        lines.append("|---------|--------------|-------------|-----------|")
        for ns in sorted(fs_agg):
            cs = fs_agg[ns]
            # Get avg pearson too
            rs = [
                all_metrics[k]["macro_pearson"]
                for k in all_metrics
                if int(k.split("|")[2]) == ns
                and config_eligible(all_metrics[k], args.objective, args.min_coverage)
                and not np.isnan(all_metrics[k]["macro_pearson"])
            ]
            avg_r = np.mean(rs) if rs else float("nan")
            lines.append(
                f"| {ns} | {np.mean(cs):.4f} | {avg_r:.4f} | {len(cs)} |"
            )
        lines.append("")

    # ── Parse Failure Analysis ──
    lines.append("## ⚠️ Parse Failure Rates")
    lines.append("")
    lines.append("| Config | Parse Fail Rate |")
    lines.append("|--------|----------------|")
    fail_items = [(k, m["parse_fail_rate"]) for k, m in all_metrics.items() if m["n"] > 0]
    fail_items.sort(key=lambda x: x[1], reverse=True)
    for k, fr in fail_items[:10]:
        lines.append(f"| `{k}` | {fr:.1%} |")
    lines.append("")

    # ── Winner ──
    lines.append("## 🏅 Winner")
    lines.append("")
    if ranked_eligible:
        winner_key, winner_m = ranked_eligible[0]
        w_model, w_ps, w_ns = winner_key.split("|")
        ci = winner_m.get("bootstrap_ci_95", (float("nan"), float("nan")))
        ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if not np.isnan(ci[0]) else "—"
        lines.append(f"- **Model**: `{w_model}`")
        lines.append(f"- **Prompt set**: `{w_ps}`")
        lines.append(f"- **Few-shot count**: {w_ns}")
        lines.append(f"- **Coverage**: {winner_m['coverage']:.0%}")
        lines.append(f"- **Macro Pearson**: {winner_m['macro_pearson']:.4f} (95% CI: {ci_str})")
        lines.append(f"- **Macro Spearman**: {winner_m['macro_spearman']:.4f}")
        lines.append(f"- **Macro MAE**: {winner_m['macro_mae']:.4f}")
        lines.append(f"- **Macro Bias**: {winner_m['macro_bias']:+.4f}")
        lines.append(f"- **Composite Score**: {composite_score(winner_m):.4f}")
    else:
        lines.append(
            "*No winner — all configs were skipped* (no predictions and/or below min coverage)."
        )
    lines.append("")

    return "\n".join(lines) + "\n"


def generate_best_config(
    all_metrics: dict[str, dict[str, Any]],
    prompt_sets: dict[str, list[dict[str, str]]],
    few_shots: list[tuple[str, str]],
    run_id: str,
    objective: str,
    min_coverage: float,
) -> dict[str, Any]:
    """Generate the BEST_CONFIG.json for deployment."""
    ranked = sorted(
        all_metrics.items(),
        key=lambda x: rank_value(x[1], objective, min_coverage),
        reverse=True,
    )
    winner: tuple[str, dict[str, Any]] | None = None
    for k, m in ranked:
        if config_eligible(m, objective, min_coverage):
            winner = (k, m)
            break

    n_with_preds = sum(1 for m in all_metrics.values() if m["n"] > 0)
    if winner is None:
        return {
            "skipped": True,
            "reason": "No config meets eligibility (predictions + coverage floor + valid objective score).",
            "run_id": run_id,
            "selected_at": datetime.now(timezone.utc).isoformat(),
            "selection": {"objective": objective, "min_coverage": min_coverage},
            "configs_total": len(all_metrics),
            "configs_with_predictions": n_with_preds,
        }

    winner_key, winner_m = winner
    w_model, w_ps, w_ns = winner_key.split("|")
    n_shots = int(w_ns)

    variants = prompt_sets.get(w_ps, [])

    return {
        "run_id": run_id,
        "selected_at": datetime.now(timezone.utc).isoformat(),
        "model": w_model,
        "prompt_set": w_ps,
        "n_shots": n_shots,
        "composite_score": composite_score(winner_m),
        "ranking_value": rank_value(winner_m, objective, min_coverage),
        "metrics": {
            "macro_pearson": winner_m["macro_pearson"],
            "macro_spearman": winner_m["macro_spearman"],
            "macro_mae": winner_m["macro_mae"],
            "macro_bias": winner_m["macro_bias"],
            "coverage": winner_m["coverage"],
            "bootstrap_ci_95": winner_m.get("bootstrap_ci_95"),
            "per_trait": winner_m.get("per_trait", {}),
        },
        "selection": {
            "objective": objective,
            "min_coverage": min_coverage,
        },
        "prompt_variants": variants,
        "few_shots": [{"user": u, "assistant": a} for u, a in few_shots[:n_shots]],
        "deployment_config": {
            "temperature": 0.05,
            "max_tokens": 200,
            "api_endpoint": "https://integrate.api.nvidia.com/v1/chat/completions",
        },
    }


# ── Main ───────────────────────────────────────────────────────────────────────


def main() -> None:
    root = Path(__file__).resolve().parent
    eval_data = root.parent.parent
    big5loop = eval_data.parent

    ap = argparse.ArgumentParser(
        description="Prompt & Model Harness Engineering for OCEAN Detection"
    )
    ap.add_argument(
        "--workflow",
        default=str(big5loop / "workflows" / "n8n" / "big5loop-pandora-eval-v4.json"),
    )
    ap.add_argument(
        "--input",
        default=str(eval_data / "pandora" / "processed" / "pandora_eval_test.jsonl"),
    )
    ap.add_argument("--limit", type=int, default=50, help="Number of samples to evaluate")
    ap.add_argument("--max-workers", type=int, default=2, help="Parallel API workers")
    ap.add_argument("--timeout", type=int, default=45, help="API timeout in seconds")
    ap.add_argument("--retries", type=int, default=3, help="Max retries per API call")
    ap.add_argument("--retry-backoff", type=float, default=1.5, help="Base seconds for backoff")
    ap.add_argument("--delay", type=float, default=0.1, help="Delay between job completions")
    ap.add_argument(
        "--models",
        default=None,
        help="Comma-separated model names (overrides --pool)",
    )
    ap.add_argument(
        "--pool",
        default="single_llama31",
        choices=sorted(MODEL_POOLS.keys()),
        help="Predefined model pool",
    )
    ap.add_argument(
        "--prompt-sets",
        default=None,
        help="Comma-separated prompt set names to test (default: all 8)",
    )
    ap.add_argument(
        "--n-shots",
        default=None,
        help="Comma-separated few-shot counts (default: 0,5,10,20)",
    )
    ap.add_argument(
        "--objective",
        default="pearson",
        choices=["pearson", "composite"],
        help="Ranking objective for leaderboard/winner",
    )
    ap.add_argument(
        "--min-coverage",
        type=float,
        default=0.9,
        help="Minimum coverage required for ranking/winner",
    )
    ap.add_argument(
        "--resume",
        action="store_true",
        help="Resume from existing JSONL (skip already-evaluated combos)",
    )
    ap.add_argument(
        "--api-url",
        default=os.environ.get(
            "NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"
        ),
    )
    args = ap.parse_args()

    # ── API key ──
    api_key = os.environ.get("NVIDIA_API_KEY", "")
    if not api_key:
        envf = big5loop / ".env"
        if envf.exists():
            for line in envf.read_text(encoding="utf-8").splitlines():
                if line.startswith("NVIDIA_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    if not api_key or len(api_key) < 10:
        raise SystemExit("NVIDIA_API_KEY is required")

    # ── Models ──
    if args.models:
        models = [m.strip() for m in args.models.split(",") if m.strip()]
    else:
        models = list(MODEL_POOLS[args.pool])
    models = list(dict.fromkeys(models))

    # ── Few-shot counts ──
    if args.n_shots:
        n_shots_list = [int(x.strip()) for x in args.n_shots.split(",")]
    else:
        n_shots_list = list(FEW_SHOT_COUNTS)

    # ── Prompts ──
    wf_variants, few_shots = load_workflow_prompt_and_fewshot(Path(args.workflow))
    all_prompt_sets: dict[str, list[dict[str, str]]] = {}
    all_prompt_sets.update(_workflow_prompt_sets(wf_variants))
    all_prompt_sets.update(_new_prompt_sets())

    if args.prompt_sets:
        selected = [s.strip() for s in args.prompt_sets.split(",")]
        all_prompt_sets = {k: v for k, v in all_prompt_sets.items() if k in selected}
        if not all_prompt_sets:
            raise SystemExit(f"No matching prompt sets. Available: {list(all_prompt_sets.keys())}")

    # ── Load samples ──
    samples: list[dict[str, Any]] = []
    with open(args.input, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= args.limit:
                break
            samples.append(json.loads(line))

    print(f"\n{'='*70}")
    print(f"  Harness Engineering Benchmark")
    print(f"  Models:      {len(models)} ({', '.join(models)})")
    print(f"  Prompt sets: {len(all_prompt_sets)} ({', '.join(all_prompt_sets.keys())})")
    print(f"  Few-shots:   {n_shots_list}")
    print(f"  Samples:     {len(samples)}")
    total_configs = len(models) * len(all_prompt_sets) * len(n_shots_list)
    total_evals = total_configs * len(samples)
    print(f"  Total configs: {total_configs}")
    print(f"  Total evals:   {total_evals}")
    print(f"{'='*70}\n")

    # ── Output setup ──
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = root / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jsonl = out_dir / f"harness_{run_id}.jsonl"

    # ── Resume support ──
    done_keys: set[str] = set()
    if args.resume:
        # Find latest harness JSONL
        existing = sorted(out_dir.glob("harness_*.jsonl"), reverse=True)
        if existing:
            resume_file = existing[0]
            print(f"Resuming from {resume_file.name}")
            out_jsonl = resume_file  # append to existing
            with open(resume_file, encoding="utf-8") as f:
                for line in f:
                    r = json.loads(line)
                    k = f"{r['sample_id']}|{r['model']}|{r['prompt_set']}|{r['n_shots']}"
                    done_keys.add(k)
            print(f"  Already completed: {len(done_keys)} evaluations")

    # ── Build job list ──
    jobs_args: list[tuple] = []
    skipped_models: set[str] = set()
    for s in samples:
        sid = s.get("sample_id")
        for model in models:
            for ps_name, variants in all_prompt_sets.items():
                for n_shots in n_shots_list:
                    key = f"{sid}|{model}|{ps_name}|{n_shots}"
                    if key in done_keys:
                        continue
                    jobs_args.append((s, model, ps_name, variants, n_shots))

    print(f"Jobs to run: {len(jobs_args)} (skipped {len(done_keys)} already done)")

    # ── Execute ──
    completed = 0
    total_jobs = len(jobs_args)

    with ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as ex:
        futures = {}
        for s, model, ps_name, variants, n_shots in jobs_args:
            fut = ex.submit(
                eval_single_config,
                s,
                model,
                ps_name,
                variants,
                few_shots,
                n_shots,
                args.api_url,
                api_key,
                args.timeout,
                args.retries,
                args.retry_backoff,
            )
            futures[fut] = (s.get("sample_id"), model, ps_name, n_shots)

        for fut in as_completed(futures):
            rec = fut.result()
            sid, model, ps_name, n_shots = futures[fut]

            # Track 404 models to skip future jobs (handled gracefully)
            if rec.get("variant_details"):
                first_err = rec["variant_details"][0].get("error", "")
                if "404 model_not_found" in str(first_err):
                    if model not in skipped_models:
                        skipped_models.add(model)
                        print(f"  ⚠ {model}: 404 — will continue other models")

            with open(out_jsonl, "a", encoding="utf-8") as w:
                w.write(json.dumps(rec, ensure_ascii=False) + "\n")

            completed += 1
            job_status = "ok" if rec.get("predicted_ocean") else "failed"
            print(
                f"  [{completed}/{total_jobs}] status={job_status} {sid} | {model.split('/')[-1]} "
                f"| {ps_name} | {n_shots}-shot"
            )

            if args.delay > 0:
                time.sleep(args.delay)

    # ── Aggregate & Analyze ──
    print("\nAggregating metrics...")

    all_results: dict[str, list[dict[str, Any]]] = {}
    with open(out_jsonl, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            key = f"{r['model']}|{r['prompt_set']}|{r['n_shots']}"
            all_results.setdefault(key, []).append(r)

    all_metrics: dict[str, dict[str, Any]] = {}
    for key, rows in all_results.items():
        all_metrics[key] = compute_metrics(rows, len(samples))

    # ── Generate report ──
    report = generate_report(
        all_metrics, run_id, models, all_prompt_sets, len(samples), n_shots_list, args
    )
    out_md = out_dir / f"ANALYSIS_harness_{run_id}.md"
    out_md.write_text(report, encoding="utf-8")
    latest_md = out_dir / "ANALYSIS_LATEST_HARNESS.md"
    latest_md.write_text(report, encoding="utf-8")

    # ── Generate best config ──
    best = generate_best_config(
        all_metrics,
        all_prompt_sets,
        few_shots,
        run_id,
        objective=args.objective,
        min_coverage=args.min_coverage,
    )
    best_json = out_dir / f"BEST_CONFIG_{run_id}.json"
    best_json.write_text(json.dumps(best, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    latest_best = out_dir / "BEST_CONFIG_LATEST.json"
    latest_best.write_text(best_json.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"\n{'='*70}")
    print(f"  DONE — {completed} evaluations")
    print(f"  Results: {out_jsonl}")
    print(f"  Analysis: {out_md}")
    print(f"  Best config: {best_json}")
    if best.get("skipped"):
        print(f"\n  ⏭ No eligible winner — all configs skipped: {best.get('reason', '')}")
        print(
            f"     With predictions: {best.get('configs_with_predictions', 0)} / {best.get('configs_total', 0)} configs"
        )
    elif best.get("model"):
        print(f"\n  🏅 Winner: {best['model']} / {best['prompt_set']} / {best['n_shots']}-shot")
        print(f"     Composite: {best['composite_score']:.4f}")
        bm = best.get("metrics", {})
        print(f"     Macro r: {bm.get('macro_pearson', 0):.4f}, MAE: {bm.get('macro_mae', 0):.4f}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
