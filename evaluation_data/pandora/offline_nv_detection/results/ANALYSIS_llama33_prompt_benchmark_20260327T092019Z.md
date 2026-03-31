# Llama-3.3 Prompt Tuning Benchmark

- Run ID: `20260327T092019Z`
- Model: `meta/llama-3.3-70b-instruct`
- Samples: 20
- Retries: 3, backoff: 1.5s
- Prompt sets: workflow_current, strict_style_v1, lowA_control_v1, lowOC_guard_v1
- Results file: `llama33_prompt_benchmark_20260327T092019Z.jsonl`

## Metrics by prompt set

| Prompt set | n | coverage | macro r | macro rho | macro MAE | composite |
|------------|---|----------|---------|-----------|-----------|-----------|
| `strict_style_v1` | 12 | 60.00% | 0.2485 | 0.2603 | 0.5700 | 0.3540 |
| `workflow_current` | 17 | 85.00% | 0.0968 | 0.0864 | 0.6362 | 0.3228 |
| `lowOC_guard_v1` | 15 | 75.00% | 0.1363 | 0.1452 | 0.5782 | 0.3204 |
| `lowA_control_v1` | 16 | 80.00% | 0.0822 | 0.1614 | 0.6139 | 0.2976 |

## Conclusion

- Best prompt set: `strict_style_v1`
- Coverage: 60.00%
- Macro Pearson: 0.2485
- Macro MAE: 0.5700
