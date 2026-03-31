# 🔬 Prompt & Model Harness Engineering Report

- **Run ID**: `20260327T102025Z`
- **Samples**: 3
- **Models**: `meta/llama-3.3-70b-instruct`
- **Prompt sets**: `minimal_instruction_v1`
- **Few-shot counts**: [0, 5, 10, 20]
- **Total configs**: 2
- **Retries**: 3, backoff: 1.5s

## 🏆 Leaderboard (Top 20)

| Rank | Model | Prompt Set | Shots | n | Coverage | Macro r | 95% CI | Macro ρ | Macro MAE | Composite |
|------|-------|------------|-------|---|----------|---------|--------|---------|-----------|-----------|
| 1 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 5 | 3 | 100% | 0.5113 | — | 0.2000 | 0.4124 | 0.6732 |
| 2 | `meta/llama-3.3-70b-instruct` | `minimal_instruction_v1` | 0 | 3 | 100% | 0.0296 | — | 0.0268 | 0.4924 | 0.4163 |

## 📊 Per-Trait Analysis (Top 5 Configs)

### #1: `meta/llama-3.3-70b-instruct` / `minimal_instruction_v1` / 5-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | 0.9966 | 0.5000 | 0.5622 | +0.5622 | -0.54±0.55 | 0.02±0.36 |
| **C** (Conscientiousness) | 0.0000 | 0.0000 | 0.4556 | -0.0778 | -0.10±0.10 | -0.18±0.56 |
| **E** (Extraversion) | 0.5731 | 0.5000 | 0.6444 | +0.6444 | -0.47±0.22 | 0.18±0.37 |
| **A** (Agreeableness) | 0.9821 | 0.5000 | 0.1911 | -0.1911 | 0.41±0.78 | 0.22±0.77 |
| **N** (Neuroticism) | 0.0048 | -0.5000 | 0.2089 | -0.2089 | 0.69±0.21 | 0.48±0.23 |

### #2: `meta/llama-3.3-70b-instruct` / `minimal_instruction_v1` / 0-shot

| Trait | Pearson | Spearman | MAE | Bias | GT μ±σ | Pred μ±σ |
|-------|---------|----------|-----|------|--------|----------|
| **O** (Openness) | -0.8160 | -0.8660 | 0.7400 | +0.7400 | -0.54±0.55 | 0.20±0.00 |
| **C** (Conscientiousness) | 0.2638 | 0.5000 | 0.2111 | +0.2111 | -0.10±0.10 | 0.11±0.38 |
| **E** (Extraversion) | 0.3392 | 0.5000 | 0.5333 | +0.5333 | -0.47±0.22 | 0.07±0.32 |
| **A** (Agreeableness) | 0.9548 | 0.5000 | 0.2689 | +0.0644 | 0.41±0.78 | 0.48±0.42 |
| **N** (Neuroticism) | -0.5937 | -0.5000 | 0.7089 | -0.7089 | 0.69±0.21 | -0.02±0.17 |

## 🤖 Model Comparison (avg composite across all prompt sets)

| Model | Avg Composite | Best Composite | # Configs |
|-------|--------------|----------------|-----------|
| `meta/llama-3.3-70b-instruct` | 0.5448 | 0.6732 | 2 |

## 📝 Prompt Set Comparison (avg composite across all models)

| Prompt Set | Avg Composite | Best Composite | # Configs |
|------------|--------------|----------------|-----------|
| `minimal_instruction_v1` | 0.5448 | 0.6732 | 2 |

## 🎯 Few-Shot Ablation

| # Shots | Avg Composite | Avg Macro r | # Configs |
|---------|--------------|-------------|-----------|
| 0 | 0.4163 | 0.0296 | 1 |
| 5 | 0.6732 | 0.5113 | 1 |

## ⚠️ Parse Failure Rates

| Config | Parse Fail Rate |
|--------|----------------|
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|5` | 22.2% |
| `meta/llama-3.3-70b-instruct|minimal_instruction_v1|0` | 11.1% |

## 🏅 Winner

- **Model**: `meta/llama-3.3-70b-instruct`
- **Prompt set**: `minimal_instruction_v1`
- **Few-shot count**: 5
- **Coverage**: 100%
- **Macro Pearson**: 0.5113 (95% CI: —)
- **Macro Spearman**: 0.2000
- **Macro MAE**: 0.4124
- **Macro Bias**: +0.1458
- **Composite Score**: 0.6732

