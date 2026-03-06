# Implications and Recommendations

- Near-term use
  - Works best in narrow, supportive domains with clear language
  - Keep neutral defaults until confident; avoid overfitting early turns
- Build for practice
  - Add probabilistic/confidence outputs; smooth updates (e.g., exponential smoothing)
  - Safety fallbacks for low confidence or risk cues
  - Human evaluation alongside automated evaluator
- For our thesis
  - Rebuild a lightweight, transparent framework (Python preferred)
  - Reproduce small-scale results; then extend with modest improvements (e.g., confidence scoring, clearer logging)
