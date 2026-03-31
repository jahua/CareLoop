# Phase 3: Held-Out Test Evaluation and Extraversion Bias Mitigation

## Abstract

This report presents the final, unbiased evaluation of optimized Big Five personality detection on the PERSONAGE corpus held-out test set (n=288). We compare three approaches: the Phase 1 winner (`trait_first`, 11-shot, temp 0.3), an E-improved prompt with rebalanced exemplars, and post-hoc linear calibration. The held-out test reveals a substantial generalization gap: macro Pearson r drops from 0.661 (dev) to 0.466 (test), demonstrating that dev-set optimization inflated performance estimates. The E-improved prompt successfully increases Extraversion detection (r: 0.486 → 0.560, +15%) and halves E bias (+0.296 → +0.144), but at a cost to Openness and Conscientiousness. Post-hoc calibration reduces E bias without affecting correlation. All three approaches exceed the N8N baseline (r = 0.457) on the held-out test, but none reach the r ≥ 0.60 target, which was an artifact of dev-set overfitting.

---

## 1. Introduction

Phase 1 (prompt engineering) and Phase 2 (multi-model benchmark) were conducted on the dev set (n=292, of which 80 were used per configuration). The resulting macro r = 0.661 exceeded the r ≥ 0.60 target. However, these results were obtained on data used for optimization, raising concerns about overfitting.

Phase 3 addresses this by running the frozen winning configuration exactly once on the held-out test set (n=288), providing an unbiased estimate of true performance. Additionally, based on the EDA finding that Extraversion detection suffers from systematic positive bias, we test two mitigation strategies.

### 1.1 Approaches Evaluated

| Approach | Description |
|----------|-------------|
| **v1 (original)** | Phase 1 winner: `trait_first` prompt, 11 original exemplars, temp 0.3 |
| **v2 (E-improved)** | Modified prompt with explicit low-E detection guards + rebalanced exemplars (4 low-E, 3 mid-E, 4 high-E) |
| **v1+cal (calibrated)** | v1 predictions with post-hoc linear E calibration fitted on dev set |

All three use `meta/llama-3.3-70b-instruct` via JuLing API.

---

## 2. E-Improvement Design

### 2.1 Prompt Modifications (v2)

The v2 system prompt adds an "Extraversion calibration" section to the original `trait_first` prompt:

> **Extraversion calibration (critical):**
> - Short, terse, or minimal utterances do NOT indicate high Extraversion — they often indicate LOW Extraversion.
> - Hedging ("I am not sure", "I mean", "you know") signals introversion, not energy.
> - Flat, withdrawn, or reluctant delivery = low E, even if the content is polite.
> - Reserve high E for genuinely energetic, assertive, socially dominant speech.
> - Use the full [−1, +1] range for E. Many speakers are introverted (E < 0).

### 2.2 Exemplar Rebalancing

The original 11 exemplars had a severe E-positive skew: only 2 had negative E (−0.917, −0.750), while the remaining 9 ranged from 0.0 to +1.0.

| E range | v1 (original) | v2 (rebalanced) |
|---------|:---:|:---:|
| E < −0.5 | 2 | 4 |
| −0.5 ≤ E < 0.5 | 3 | 3 |
| E ≥ 0.5 | 6 | 4 |

The rebalanced set replaces high-E exemplars with low-E full-OCEAN examples (E = −0.667, −0.750, −0.750) to anchor the model's understanding of introverted speech.

### 2.3 Post-hoc Calibration

A linear calibration was fitted on v1 dev predictions (n=80):

$$E_{\text{calibrated}} = 0.6521 \times E_{\text{predicted}} + (-0.0172)$$

This compresses the prediction range and shifts the mean downward, correcting for the systematic positive bias observed in Phase 1.

---

## 3. Results

### 3.1 Overall Performance (Test Set, n=288)

| Trait | v1 r | v2 r | v1+cal r | v1 bias | v2 bias | v1+cal bias |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Openness | **0.354** | 0.294 | 0.354 | +0.101 | +0.151 | +0.101 |
| Conscientiousness | **0.426** | 0.367 | 0.426 | +0.210 | +0.148 | +0.210 |
| **Extraversion** | 0.486 | **0.560** | 0.486 | +0.296 | **+0.144** | **+0.098** |
| Agreeableness | 0.552 | **0.564** | 0.552 | +0.057 | +0.089 | +0.057 |
| Neuroticism | **0.514** | 0.499 | 0.514 | +0.107 | +0.099 | +0.107 |
| **Macro** | **0.466** | 0.457 | **0.466** | +0.154 | +0.126 | +0.115 |

**Bootstrap 95% CIs (macro r, n=2000):**
- v1: 0.465 [0.392, 0.531]
- v2: 0.455 [0.379, 0.526]
- v1+cal: 0.465 [0.392, 0.531]

### 3.2 Generalization Gap

| Metric | Dev (Phase 1) | Test (Phase 3) | Gap |
|--------|:---:|:---:|:---:|
| Macro r | 0.661 | 0.466 | −0.195 (−29.5%) |
| r_O | 0.563 | 0.354 | −0.209 |
| r_C | 0.655 | 0.426 | −0.229 |
| r_E | 0.461 | 0.486 | +0.025 |
| r_A | 0.824 | 0.552 | −0.272 |
| r_N | 0.801 | 0.514 | −0.287 |

The dev-to-test drop is −0.195 in macro r (−29.5%). Interestingly, Extraversion is the only trait that **improves** on the test set (+0.025), while Agreeableness and Neuroticism show the largest drops (−0.27 to −0.29). This suggests that A and N were most over-fitted during prompt optimization on the dev set.

### 3.3 Extraversion Bias Analysis (Test Set)

| GT Bin | v1 bias | v2 bias | v1+cal bias | v1 MAE | v2 MAE | v1+cal MAE | n |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [−1.0, −0.5) | +0.666 | **+0.360** | +0.640 | 0.714 | **0.496** | 0.641 | 37 |
| [−0.5, 0.0) | +0.591 | **+0.281** | +0.441 | 0.684 | **0.553** | 0.487 | 69 |
| [0.0, +0.5) | +0.331 | **+0.140** | **+0.114** | 0.424 | 0.513 | **0.224** | 103 |
| [+0.5, +1.0] | −0.010 | −0.002 | −0.266 | **0.159** | 0.297 | 0.270 | 113 |

**v2 (E-improved prompt)** dramatically reduces bias for introverted text:
- Low-E bias: +0.666 → +0.360 (−46%)
- Mid-low-E bias: +0.591 → +0.281 (−52%)

**v1+cal (calibration)** is most effective in the mid-range (0.0 to 0.5: bias +0.331 → +0.114) but over-corrects on high-E samples (bias −0.010 → −0.266).

### 3.4 v2 Trade-off Analysis

| Trait | Δr (v2 − v1) | Assessment |
|-------|:---:|------------|
| Openness | −0.060 | Degraded — lost O-focused exemplars |
| Conscientiousness | −0.059 | Degraded — lost C-focused exemplars |
| **Extraversion** | **+0.074** | **Improved** — E prompt guards + low-E exemplars |
| Agreeableness | +0.012 | Marginal gain |
| Neuroticism | −0.015 | Marginal loss |

The v2 exemplar rebalancing removed `agree_low` and `consc_low` exemplars (which were also high-E), replacing them with low-E exemplars. This improved E detection at the expense of O and C anchoring. The net macro r is flat (0.466 → 0.457, within CI overlap).

---

## 4. Discussion

### 4.1 The Generalization Gap Problem

The 29.5% drop from dev to test is the most important finding of Phase 3. This gap arises because:

1. **Prompt selection bias**: The best of 48 configurations was chosen based on dev performance. With 80 samples per configuration, sampling variance means the "winner" likely benefited from favorable noise.

2. **Exemplar leakage**: The 11 few-shot exemplars are drawn from the dev set. The model has literally seen these examples during both optimization and evaluation. On the test set, no such advantage exists.

3. **Small-sample instability**: With n=80 per configuration in Phase 1, per-trait Pearson r has a standard error of approximately ±0.10, meaning the "true" performance of any configuration is substantially uncertain.

This finding has direct implications for the thesis: **reported dev-set results should always be accompanied by held-out test estimates**, and the gap should be explicitly discussed.

### 4.2 Extraversion Improvement: Prompt vs Calibration

Two orthogonal strategies for improving E detection were tested:

**Prompt-level (v2)**: Modifies the model's internal reasoning about E by adding explicit calibration instructions and rebalanced exemplars. This reduces bias across all GT bins but introduces noise in other traits due to exemplar changes. The improvement is visible in correlation (+0.074 in r), meaning the model produces fundamentally better-ranked predictions.

**Post-hoc calibration**: Applies a linear transform to predictions after inference. This cannot improve correlation (Pearson r is invariant to linear transforms) but can reduce bias and MAE. It is most effective in the mid-range but over-corrects at extremes.

**Optimal strategy**: A combined approach — v2 prompt for better E ranking, followed by a light calibration fitted on v2 dev predictions — would likely yield the best overall E performance.

### 4.3 Implications for Big5Loop Production System

The test-set macro r of 0.466 (95% CI: [0.392, 0.531]) represents the honest performance estimate for the current detection pipeline on PERSONAGE-style text. Key implications:

1. **The r ≥ 0.60 target is not met** on held-out data. The dev-set result of 0.661 was an over-estimate.
2. **Agreeableness (r = 0.552) and Neuroticism (r = 0.514) are the strongest traits** on the test set, suggesting that linguistic markers of warmth/rudeness and anxiety/calm are most reliably detected.
3. **Openness (r = 0.354) is the weakest trait**, below the r ≥ 0.40 per-trait target.
4. **Extraversion benefits most from targeted intervention** — the v2 prompt achieves r = 0.560, demonstrating that trait-specific prompt engineering is effective.

---

## 5. Conclusions

1. **The held-out test set reveals a generalization gap of −0.195** (macro r: 0.661 → 0.466). Dev-set optimization inflated performance by ~30%. This underscores the critical importance of Phase 3 evaluation.

2. **The E-improved prompt (v2) successfully increases Extraversion detection** from r = 0.486 to r = 0.560 (+15%) and halves E bias (+0.296 → +0.144), validating the EDA hypothesis that exemplar imbalance and missing calibration instructions were key factors.

3. **The v2 trade-off**: E/A gains come at the cost of O/C accuracy (−0.06 each) due to exemplar rebalancing. A future v3 could retain O/C exemplars while adding low-E exemplars (expanding to 13–15 shots).

4. **Post-hoc calibration** is complementary to prompt improvements: it reduces bias and MAE without affecting correlation, and can be applied at zero inference cost.

5. **Honest performance estimate**: The Big5Loop PERSONAGE detection achieves macro r ≈ 0.466 [0.392, 0.531] on held-out data, with Agreeableness and Neuroticism as the strongest traits and Openness as the weakest.

---

## Appendix: File Inventory

```
phase3/
├── prompt_bank_v2.py           ← E-improved prompt + rebalanced exemplars
├── run_phase3.py               ← Test evaluation script (v1 + v2)
├── calibrate_e.py              ← Post-hoc E calibration utility
├── results/
│   ├── phase3_v1_test_*.jsonl  ← 288 test predictions (original)
│   ├── phase3_v2_test_*.jsonl  ← 288 test predictions (E-improved)
│   └── phase3_v2_dev_*.jsonl   ← 80 dev predictions (E-improved, validation)
└── Phase3-Analysis.ipynb       ← Visualization notebook
```
