# Llama-3.3 Prompt Tuning Benchmark

- Run ID: `20260327T090257Z`
- Model: `meta/llama-3.3-70b-instruct`
- Samples: 20
- Prompt sets: workflow_current, strict_style_v1, lowA_control_v1, lowOC_guard_v1
- Results file: `llama33_prompt_benchmark_20260327T090257Z.jsonl`

## Metrics by prompt set

| Prompt set | n | coverage | macro r | macro rho | macro MAE | composite |
|------------|---|----------|---------|-----------|-----------|-----------|
| `lowOC_guard_v1` | 2 | 10.00% | 0.4000 | 0.4000 | 0.8170 | 0.3100 |
| `workflow_current` | 3 | 15.00% | -0.0718 | -0.0732 | 0.9080 | -0.0053 |
| `strict_style_v1` | 6 | 30.00% | -0.1653 | -0.1395 | 0.6787 | -0.0257 |
| `lowA_control_v1` | 5 | 25.00% | -0.2157 | -0.2015 | 0.6312 | -0.0760 |

## Conclusion

- Best prompt set: `lowOC_guard_v1`
- Coverage: 10.00%
- Macro Pearson: 0.4000
- Macro MAE: 0.8170
