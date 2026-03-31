# 🔬 Prompt & Model Harness Engineering Report

- **Run ID**: `20260327T103447Z`
- **Samples**: 100
- **Models**: `meta/llama-3.3-70b-instruct`
- **Prompt sets**: `workflow_current`, `minimal_instruction_v1`
- **Few-shot counts**: [0, 5, 10, 20]
- **Total configs**: 4
- **Retries**: 3, backoff: 1.5s

## 🏆 Leaderboard (Top 20)

| Rank | Model | Prompt Set | Shots | n | Coverage | Macro r | 95% CI | Macro ρ | Macro MAE | Composite |
|------|-------|------------|-------|---|----------|---------|--------|---------|-----------|-----------|
| 1 | `meta/llama-3.3-70b-instruct` | `workflow_current` | 20 | 28 | 28% | 0.0542 | [-0.106, 0.227] | 0.0652 | 0.5682 | 0.1974 |
| 2 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 20 | 23 | 23% | -0.0191 | [-0.203, 0.186] | 0.0219 | 0.6183 | 0.1358 |
| 3 | `meta/llama-3.3-70b-instruct` | `workflow_current` | 5 | 25 | 25% | -0.0323 | [-0.197, 0.130] | -0.0116 | 0.6178 | 0.1353 |
| 4 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 5 | 21 | 21% | -0.1041 | [-0.328, 0.135] | -0.1268 | 0.6485 | 0.0813 |

## 📊 Per-Trait Analysis (Top 5 Configs)

### #1: `meta/llama-3.3-70b-instruct` / `workflow_current` / 20-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | -0.1727 | -0.2352 | 0.6020 | +0.1563 | 0.01±0.56 | 0.16±0.34 |
| **C** (Conscientiousness) | -0.0591 | -0.0350 | 0.5713 | -0.2865 | 0.38±0.44 | 0.09±0.37 |
| **E** (Extraversion) | 0.1059 | 0.1123 | 0.6032 | +0.3761 | -0.19±0.60 | 0.18±0.23 |
| **A** (Agreeableness) | 0.2311 | 0.2197 | 0.5588 | +0.1319 | -0.13±0.66 | -0.00±0.46 |
| **N** (Neuroticism) | 0.1655 | 0.2644 | 0.5056 | -0.0349 | 0.16±0.58 | 0.12±0.37 |

### #2: `meta/llama-3.3-70b-instruct` / `minimal_instruction_v1` / 20-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | -0.0575 | -0.0317 | 0.7248 | +0.1300 | 0.02±0.73 | 0.15±0.39 |
| **C** (Conscientiousness) | 0.1380 | 0.1502 | 0.5104 | -0.0426 | 0.14±0.54 | 0.10±0.41 |
| **E** (Extraversion) | -0.2250 | -0.1152 | 0.6817 | +0.1757 | -0.02±0.66 | 0.15±0.30 |
| **A** (Agreeableness) | 0.0104 | 0.0862 | 0.6330 | +0.2157 | -0.29±0.63 | -0.07±0.40 |
| **N** (Neuroticism) | 0.0383 | 0.0202 | 0.5413 | -0.0109 | 0.09±0.60 | 0.08±0.33 |

### #3: `meta/llama-3.3-70b-instruct` / `workflow_current` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.1144 | 0.1218 | 0.6676 | +0.2823 | -0.10±0.69 | 0.18±0.36 |
| **C** (Conscientiousness) | -0.1449 | -0.1317 | 0.6017 | -0.1783 | 0.31±0.49 | 0.13±0.42 |
| **E** (Extraversion) | -0.0676 | -0.0244 | 0.6656 | +0.2192 | -0.03±0.66 | 0.19±0.38 |
| **A** (Agreeableness) | 0.0899 | 0.0414 | 0.6243 | +0.1987 | -0.05±0.65 | 0.15±0.50 |
| **N** (Neuroticism) | -0.1531 | -0.0649 | 0.5299 | +0.0189 | 0.20±0.58 | 0.22±0.35 |

### #4: `meta/llama-3.3-70b-instruct` / `minimal_instruction_v1` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | -0.1740 | -0.2031 | 0.6721 | +0.2873 | -0.34±0.62 | -0.05±0.32 |
| **C** (Conscientiousness) | -0.1476 | -0.2203 | 0.6156 | -0.1806 | 0.07±0.53 | -0.11±0.41 |
| **E** (Extraversion) | -0.1173 | -0.1168 | 0.6698 | +0.2356 | -0.18±0.58 | 0.06±0.43 |
| **A** (Agreeableness) | 0.1000 | 0.1031 | 0.6460 | +0.1883 | -0.11±0.61 | 0.08±0.61 |
| **N** (Neuroticism) | -0.1815 | -0.1967 | 0.6390 | +0.2333 | 0.18±0.50 | 0.41±0.43 |

## 🤖 Model Comparison (avg composite across all prompt sets)

| Model | Avg Composite | Best Composite | # Configs |
|-------|--------------|----------------|-----------|
| `meta/llama-3.3-70b-instruct` | 0.1374 | 0.1974 | 4 |

## 📝 Prompt Set Comparison (avg composite across all models)

| Prompt Set | Avg Composite | Best Composite | # Configs |
|------------|--------------|----------------|-----------|
| `workflow_current` | 0.1664 | 0.1974 | 2 |
| `minimal_instruction_v1` | 0.1085 | 0.1358 | 2 |

## 🎯 Few-Shot Ablation

| # Shots | Avg Composite | Avg Macro r | # Configs |
|---------|--------------|-------------|-----------|
| 5 | 0.1083 | -0.0682 | 2 |
| 20 | 0.1666 | 0.0175 | 2 |

## ⚠️ Parse Failure Rates

| Config | Parse Fail Rate |
|--------|----------------|
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|5` | 91.7% |
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|20` | 91.3% |
| `meta/llama-3.3-70b-instruct|workflow_current|20` | 89.0% |
| `meta/llama-3.3-70b-instruct|workflow_current|5` | 88.0% |

## 🏅 Winner

- **Model**: `meta/llama-3.3-70b-instruct`
- **Prompt set**: `workflow_current`
- **Few-shot count**: 20
- **Coverage**: 28%
- **Macro Pearson**: 0.0542 (95% CI: [-0.106, 0.227])
- **Macro Spearman**: 0.0652
- **Macro MAE**: 0.5682
- **Macro Bias**: +0.0686
- **Composite Score**: 0.1974

