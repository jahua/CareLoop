# 🔬 Prompt & Model Harness Engineering Report

- **Run ID**: `20260327T105404Z`
- **Samples**: 20
- **Models**: `meta/llama-3.1-70b-instruct`, `meta/llama-3.3-70b-instruct`
- **Prompt sets**: `workflow_current`, `minimal_instruction_v1`
- **Few-shot counts**: [0, 5, 10, 20]
- **Total configs**: 8
- **Retries**: 3, backoff: 1.5s

## 🏆 Leaderboard (Top 20)

| Rank | Model | Prompt Set | Shots | n | Coverage | Macro r | 95% CI | Macro ρ | Macro MAE | Composite |
|------|-------|------------|-------|---|----------|---------|--------|---------|-----------|-----------|
| 1 | `meta/llama-3.1-70b-instruct` | `workflow_current` | 5 | 20 | 100% | 0.1563 | [-0.029, 0.356] | 0.1868 | 0.6101 | 0.4561 |
| 2 | `meta/llama-3.1-70b-instruct` | `minimal_instruction_v1` | 20 | 19 | 95% | 0.1573 | [-0.051, 0.374] | 0.1455 | 0.5690 | 0.4498 |
| 3 | `meta/llama-3.1-70b-instruct` | `minimal_instruction_v1` | 5 | 20 | 100% | 0.1167 | [-0.111, 0.356] | 0.1328 | 0.5945 | 0.4395 |
| 4 | `meta/llama-3.1-70b-instruct` | `workflow_current` | 20 | 20 | 100% | 0.0558 | [-0.121, 0.240] | 0.1181 | 0.6012 | 0.4076 |
| 5 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 5 | 4 | 20% | 0.4451 | — | 0.3359 | 0.4720 | 0.3882 |
| 6 | `meta/llama-3.3-70b-instruct` | `workflow_current` | 5 | 4 | 20% | 0.0587 | — | -0.0094 | 0.6340 | 0.1625 |
| 7 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 20 | 1 | 5% | 0.0000 | — | 0.0000 | 0.3440 | 0.1462 |
| 8 | `meta/llama-3.3-70b-instruct` | `workflow_current` | 20 | 2 | 10% | 0.2000 | — | 0.2000 | 0.9420 | 0.1416 |

## 📊 Per-Trait Analysis (Top 5 Configs)

### #1: `meta/llama-3.1-70b-instruct` / `workflow_current` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.3245 | 0.5227 | 0.5273 | +0.3400 | -0.29±0.58 | 0.04±0.26 |
| **C** (Conscientiousness) | 0.1989 | 0.2376 | 0.5247 | -0.2007 | 0.26±0.54 | 0.06±0.33 |
| **E** (Extraversion) | 0.1541 | 0.0637 | 0.7133 | +0.6000 | -0.28±0.53 | 0.31±0.36 |
| **A** (Agreeableness) | 0.0922 | 0.1206 | 0.6780 | -0.1273 | -0.03±0.68 | -0.15±0.50 |
| **N** (Neuroticism) | 0.0119 | -0.0106 | 0.6073 | +0.0473 | 0.22±0.68 | 0.26±0.34 |

### #2: `meta/llama-3.1-70b-instruct` / `minimal_instruction_v1` / 20-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.0998 | 0.2050 | 0.6028 | +0.3818 | -0.26±0.58 | 0.12±0.33 |
| **C** (Conscientiousness) | 0.4328 | 0.3153 | 0.4889 | -0.3465 | 0.32±0.49 | -0.03±0.26 |
| **E** (Extraversion) | 0.1002 | -0.0205 | 0.5875 | +0.3935 | -0.26±0.54 | 0.13±0.34 |
| **A** (Agreeableness) | 0.3530 | 0.3283 | 0.5314 | -0.0809 | 0.02±0.66 | -0.06±0.43 |
| **N** (Neuroticism) | -0.1994 | -0.1007 | 0.6341 | -0.1139 | 0.18±0.68 | 0.07±0.25 |

### #3: `meta/llama-3.1-70b-instruct` / `minimal_instruction_v1` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.1000 | 0.2887 | 0.5632 | +0.3492 | -0.29±0.58 | 0.05±0.23 |
| **C** (Conscientiousness) | 0.2708 | 0.2431 | 0.5605 | -0.3498 | 0.26±0.54 | -0.09±0.31 |
| **E** (Extraversion) | 0.0232 | -0.0328 | 0.6193 | +0.3567 | -0.28±0.53 | 0.07±0.36 |
| **A** (Agreeableness) | 0.3785 | 0.2913 | 0.5438 | +0.1218 | -0.03±0.68 | 0.10±0.50 |
| **N** (Neuroticism) | -0.1888 | -0.1262 | 0.6857 | +0.1373 | 0.22±0.68 | 0.35±0.38 |

### #4: `meta/llama-3.1-70b-instruct` / `workflow_current` / 20-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.2804 | 0.4669 | 0.5813 | +0.4067 | -0.29±0.58 | 0.11±0.31 |
| **C** (Conscientiousness) | 0.1344 | 0.1306 | 0.5472 | -0.2498 | 0.26±0.54 | 0.01±0.31 |
| **E** (Extraversion) | -0.0891 | -0.0080 | 0.6077 | +0.4417 | -0.28±0.53 | 0.16±0.26 |
| **A** (Agreeableness) | 0.1008 | 0.0975 | 0.6323 | -0.1123 | -0.03±0.68 | -0.14±0.44 |
| **N** (Neuroticism) | -0.1477 | -0.0964 | 0.6373 | -0.1060 | 0.22±0.68 | 0.11±0.27 |

### #5: `meta/llama-3.3-70b-instruct` / `minimal_instruction_v1` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.1439 | 0.2000 | 0.6800 | +0.2700 | -0.07±0.72 | 0.20±0.44 |
| **C** (Conscientiousness) | 0.0033 | -0.4000 | 0.5400 | -0.1100 | 0.21±0.41 | 0.10±0.50 |
| **E** (Extraversion) | 0.5528 | 0.4472 | 0.3750 | +0.3750 | -0.48±0.24 | -0.10±0.12 |
| **A** (Agreeableness) | 0.7442 | 0.8000 | 0.3400 | -0.0100 | 0.16±0.57 | 0.15±0.70 |
| **N** (Neuroticism) | 0.7813 | 0.6325 | 0.4250 | -0.2050 | 0.33±0.73 | 0.12±0.37 |

## 🤖 Model Comparison (avg composite across all prompt sets)

| Model | Avg Composite | Best Composite | # Configs |
|-------|--------------|----------------|-----------|
| `meta/llama-3.1-70b-instruct` | 0.4383 | 0.4561 | 4 |
| `meta/llama-3.3-70b-instruct` | 0.2096 | 0.3882 | 4 |

## 📝 Prompt Set Comparison (avg composite across all models)

| Prompt Set | Avg Composite | Best Composite | # Configs |
|------------|--------------|----------------|-----------|
| `minimal_instruction_v1` | 0.3559 | 0.4498 | 4 |
| `workflow_current` | 0.2920 | 0.4561 | 4 |

## 🎯 Few-Shot Ablation

| # Shots | Avg Composite | Avg Macro r | # Configs |
|---------|--------------|-------------|-----------|
| 5 | 0.3616 | 0.1942 | 4 |
| 20 | 0.2863 | 0.1033 | 4 |

## ⚠️ Parse Failure Rates

| Config | Parse Fail Rate |
|--------|----------------|
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|20` | 98.3% |
| `meta/llama-3.3-70b-instruct|workflow_current|20` | 96.7% |
| `meta/llama-3.3-70b-instruct|workflow_current|5` | 93.3% |
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|5` | 93.3% |
| `meta/llama-3.1-70b-instruct|minimal_instruction_v1|20` | 40.0% |
| `meta/llama-3.1-70b-instruct|minimal_instruction_v1|5` | 11.7% |
| `meta/llama-3.1-70b-instruct|workflow_current|20` | 1.7% |
| `meta/llama-3.1-70b-instruct|workflow_current|5` | 0.0% |

## 🏅 Winner

- **Model**: `meta/llama-3.1-70b-instruct`
- **Prompt set**: `workflow_current`
- **Few-shot count**: 5
- **Coverage**: 100%
- **Macro Pearson**: 0.1563 (95% CI: [-0.029, 0.356])
- **Macro Spearman**: 0.1868
- **Macro MAE**: 0.6101
- **Macro Bias**: +0.1319
- **Composite Score**: 0.4561

