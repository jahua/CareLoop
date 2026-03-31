# Llama-3.3 Prompt Tuning Benchmark

- Run ID: `20260327T093145Z`
- Model: `meta/llama-3.3-70b-instruct`
- Samples: 10
- Retries: 2, backoff: 1.2s
- Prompt sets: workflow_current, strict_style_v1, lowA_control_v1, lowOC_guard_v1
- Results file: `llama33_prompt_benchmark_20260327T093145Z.jsonl`

## Metrics by prompt set

| Prompt set | n | coverage | macro r | macro rho | macro MAE | composite |
|------------|---|----------|---------|-----------|-----------|-----------|
| `workflow_current` | 1 | 10.00% | 0.0000 | 0.0000 | 0.8220 | 0.0300 |
| `lowA_control_v1` | 1 | 10.00% | 0.0000 | 0.0000 | 0.7920 | 0.0300 |
| `strict_style_v1` | 0 | 0.00% | nan | nan | nan | nan |
| `lowOC_guard_v1` | 0 | 0.00% | nan | nan | nan | nan |

## Conclusion

- Best prompt set: `workflow_current`
- Coverage: 10.00%
- Macro Pearson: 0.0000
- Macro MAE: 0.8220
