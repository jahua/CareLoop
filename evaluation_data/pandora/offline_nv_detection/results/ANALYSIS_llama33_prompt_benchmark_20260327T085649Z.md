# Llama-3.3 Prompt Tuning Benchmark

- Run ID: `20260327T085649Z`
- Model: `meta/llama-3.3-70b-instruct`
- Samples: 20
- Prompt sets: workflow_current, strict_style_v1, lowA_control_v1, lowOC_guard_v1
- Results file: `llama33_prompt_benchmark_20260327T085649Z.jsonl`

## Metrics by prompt set

| Prompt set | n | coverage | macro r | macro rho | macro MAE | composite |
|------------|---|----------|---------|-----------|-----------|-----------|
| `workflow_current` | 1 | 5.00% | 0.0000 | 0.0000 | 0.8520 | 0.0150 |
| `strict_style_v1` | 1 | 5.00% | 0.0000 | 0.0000 | 0.8220 | 0.0150 |
| `lowOC_guard_v1` | 2 | 10.00% | -0.2000 | -0.2000 | 0.7220 | -0.1100 |
| `lowA_control_v1` | 3 | 15.00% | -0.5122 | -0.4732 | 0.6140 | -0.3135 |

## Conclusion

- Best prompt set: `workflow_current`
- Coverage: 5.00%
- Macro Pearson: 0.0000
- Macro MAE: 0.8520
