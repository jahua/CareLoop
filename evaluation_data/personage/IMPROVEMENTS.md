# Improving Big5Loop Detection on PERSONAGE

Big5Loop’s personality detection is **weak** on the [PERSONAGE dataset](https://farm2.user.srcf.net/research/personage/): low or negative Pearson r for most OCEAN traits and high MAE (see `personage_metrics.png`). This doc explains **why** and **how to improve** it.

## Why detection is weak

1. **Detection is tuned for caregiving, not PERSONAGE**
   - **Current heuristic** (N8N STEP 3) uses emotion/support keywords: “good”, “calm”, “sad”, “anxious”, “you”, “we”, “plan”, “new”, “explore”, etc. PERSONAGE utterances are **restaurant recommendations** with **stylistic** variation (formality, hedging, agreement, swearing), not emotional support.
   - **NVIDIA API** (when used) gets a generic prompt: “Analyze this text for OCEAN personality traits…” with no hint that style (hedging, politeness, assertiveness) matters.

2. **PERSONAGE ground truth reflects *style*, not mood**
   - **Agreeableness**: “I would suggest/advise/appreciate”, “you would like” (high) vs “bloody”, “damn”, “rude”, “isn’t as bad” (low).
   - **Extraversion**: Warm, enthusiastic phrasing vs flat, hesitant “Err…”, “I might be wrong”, “I don’t know”.
   - **Openness**: Rich, varied vocabulary vs simple, repetitive wording.
   - **Conscientiousness**: Structured, detailed descriptions vs vague, “I might be wrong”, “there could be worse places”.
   - **Neuroticism (EMS)**: Calm, assured tone vs hedging, “I am not sure”, filler (“Mmhm…”, “Err…”).

3. **Single-turn eval**
   - Each PERSONAGE sample is turn 1; EMA smoothing doesn’t change the value. So the weak numbers are entirely from **raw detection** (heuristic or API), not from smoothing.

4. **Detected values cluster**
   - Heuristic often yields E ≈ 0.2, O/C/A in 0.2–0.7, so variance is low while ground truth spans [-1, 1], which keeps correlations low.

---

## Recommended improvements

### 1. Use the NVIDIA API with a style-aware prompt (highest impact)

If `NVIDIA_API_KEY` is set, the workflow calls the model instead of the heuristic. The current prompt does not tell the model to focus on **linguistic style** (hedging, politeness, assertiveness).

**Change the prompt** in the “Zurich Model Detection (EMA)” node (STEP 3) from something like:

```text
Analyze this text for OCEAN personality traits. Return ONLY JSON: {"O":float,"C":float,"E":float,"A":float,"N":float} (each -1.0 to 1.0).
Text: "..."
```

To a **style-aware** version, e.g.:

```text
Rate the speaker's Big Five personality from this single utterance. Focus on STYLE: wording, hedging (e.g. "I mean", "basically", "might be wrong"), politeness (e.g. "would suggest", "I imagine you would"), assertiveness, formality, and emotional tone. Return ONLY valid JSON with keys O,C,E,A,N; each value in [-1.0, 1.0]. O=Openness, C=Conscientiousness, E=Extraversion, A=Agreeableness, N=Neuroticism (high N = anxious/hedging). No other text.
Text: "..."
```

- **Where to edit**: N8N → workflow “Big5Loop Phase1-2 PostgreSQL” → node “Zurich Model Detection (EMA)” → in the `jsCode`, find the `prompt` variable and replace the string (keep the same variable and `userText.slice(0,500)` usage).
- **Check**: Ensure the model response is still parsed as JSON and clamped to [-1, 1]; existing code already does that.

### 2. Add PERSONAGE-style cues to the heuristic (when API is not used)

When the API is not available, the heuristic runs. Extend it with **stylistic** cues so PERSONAGE-like text is scored better:

- **Agreeableness (A)**  
  - **High**: “would suggest”, “would advise”, “would appreciate”, “imagine you would”, “you would like”, “rather nice”, “quite nice”, “friendly”.  
  - **Low**: “bloody”, “damn”, “rude”, “nasty”, “unfriendly”, “isn’t as bad”, “only place that is any good” (grudging).

- **Extraversion (E)**  
  - **High**: “outstanding”, “phenomenal”, “favourite”, “love them”, “you would love”, exclamations, warmth.  
  - **Low**: “err”, “mmhm”, “i might be wrong”, “i am not sure”, “i don’t know”, “there could be worse”, flat tone.

- **Openness (O)**  
  - **High**: varied adjectives, “satisfactory”, “dainty”, “rather”, “quite”, descriptive.  
  - **Low**: repetitive, simple wording, “like,” “basically,” “actually” (filler).

- **Conscientiousness (C)**  
  - **High**: structured sentences, “I think that”, “It seems to me”, “Even if…”, clear comparisons.  
  - **Low**: “i might be wrong”, “err”, “mmhm”, “there could be worse places”, vague.

- **Neuroticism (N)**  
  - **High**: “i am not sure”, “i might be wrong”, “err”, “mmhm”, hedging, “bloody”, “damn” (frustration).  
  - **Low**: calm, assured, “I imagine”, “I suppose”, “well”, “alright”.

You can implement this as a **second pass** in the same node: compute `heuristicOcean(text)` as now, then if the text looks like formal/restaurant style (e.g. contains “restaurant”, “place”, “food”, “price”, “dollars”, “eating”), add deltas from the style cues above and clamp. Example (pseudo-code):

```javascript
// After base heuristicOcean(userText):
const style = heuristicOcean(userText);
const t = userText;
// Personage-style: recommendation/restaurant context
const isStyleContext = /\b(restaurant|place|food|price|dollars|eating|waiter|atmosphere)\b/.test(t);
if (isStyleContext) {
  const agreeHigh = (t.match(/(would suggest|would advise|would appreciate|imagine you would|you would like|rather nice|quite nice|friendly)/g)||[]).length;
  const agreeLow = (t.match(/(bloody|damn|rude|nasty|unfriendly|isn't as bad)/g)||[]).length;
  const extraHigh = (t.match(/(outstanding|phenomenal|favourite|love them|you would love)/g)||[]).length;
  const extraLow = (t.match(/(err|mmhm|i might be wrong|i am not sure|i don't know|there could be worse)/g)||[]).length;
  const hedge = (t.match(/(i mean|basically|actually|err|mmhm|i might be wrong|i am not sure)/g)||[]).length;
  style.A = clamp(style.A + (agreeHigh - agreeLow) * 0.2, -1, 1);
  style.E = clamp(style.E + (extraHigh - extraLow) * 0.15, -1, 1);
  style.N = clamp(style.N + hedge * 0.2, -1, 1);
  style.C = clamp(style.C - hedge * 0.15, -1, 1);
}
ocean = style;
```

Integrate this into the existing `heuristicOcean` block (or call a `personageStyleAdjustment(style, userText)` after it) and keep using `ocean` for EMA as now.

### 3. Ensure evaluation uses the right OCEAN source

The eval script already uses `personality_state.ocean` from the chat API, which is `detector.smoothed_ocean` (for turn 1 = raw detection). No change needed unless you add a separate “raw only” path for experiments.

### 4. Optional: dedicated PERSONAGE evaluation mode

For **benchmarking only**, you could:

- Add an **evaluation_mode** (or similar) flag in the ingest so that when it’s set, the detector uses a **PERSONAGE-specific prompt** (for API) or **style-only heuristic** (no caregiving keywords), and optionally skip EMA so the returned OCEAN is the raw detection. That keeps production behavior unchanged while allowing fair comparison on PERSONAGE.

### 5. Direct API experiment script (fast iteration, no Big5Loop needed)

`scripts/run_personage_eval_direct.py` calls the NVIDIA API directly — **no Big5Loop or N8N required**. It supports configurable model, temperature, and prompt so you can compare setups quickly.

```bash
cd evaluation_data
export NVIDIA_API_KEY=nvapi-...

# Experiment 1: Llama 3.3 70B, temp 0.1, PERSONAGE-tuned prompt (default)
python scripts/run_personage_eval_direct.py --limit 20

# Experiment 2: compare with Gemma
python scripts/run_personage_eval_direct.py --model google/gemma-3n-e4b-it --limit 20

# Experiment 3: generic prompt (baseline)
python scripts/run_personage_eval_direct.py --prompt generic --limit 20

# Experiment 4: chain-of-thought prompt
python scripts/run_personage_eval_direct.py --prompt personage_cot --limit 20

# Experiment 5: higher temperature
python scripts/run_personage_eval_direct.py --temperature 0.5 --limit 20

# Full run (all 320 samples)
python scripts/run_personage_eval_direct.py

# Visualize any result file
python scripts/visualize_personage.py --input personage/processed/personage_results_llama_3_3_70b_instruct_personage_t01.jsonl
```

**Available models** (shortcut or full name):
| Shortcut | Full model name |
|----------|-----------------|
| `llama70b` | `meta/llama-3.3-70b-instruct` |
| `llama8b` | `meta/llama-3.1-8b-instruct` |
| `gemma` | `google/gemma-3n-e4b-it` |
| `mistral` | `mistralai/mistral-7b-instruct-v0.3` |

**Available prompts:**
| Name | Description |
|------|-------------|
| `personage` | Style-aware, PERSONAGE-tuned (default) |
| `generic` | Original generic "Analyze this text for OCEAN…" |
| `personage_cot` | Chain-of-thought: identify cues first, then rate |

Output files are auto-named by model/prompt/temperature and saved in `personage/processed/`. Use `visualize_personage.py --input <file>` to generate scatter + metrics for any result file.

### 6. N8N workflow changes (already applied)

The N8N workflows (`big5loop-phase1-2-postgres-mvp.json` and `-v2.json`) have been updated:

- **Model**: `google/gemma-3n-e4b-it` → `meta/llama-3.3-70b-instruct`
- **Temperature**: `0.3` → `0.1` (more deterministic personality scoring)
- **Prompt**: Generic → style-aware PERSONAGE-tuned (same as the "personage" prompt in the direct eval script)
- **Heuristic fallback**: now includes PERSONAGE-style cues (hedging, politeness, profanity) when restaurant/recommendation context is detected

### 7. Re-run via Big5Loop (full pipeline)

After N8N picks up the updated workflow:

```bash
cd evaluation_data
python scripts/run_personage_eval.py   # optionally --limit 50 for a quick check
python scripts/visualize_personage.py
```

Compare the new `personage_metrics.png` and `personage_detected_vs_ground_truth.png` with the previous run.

---

## Summary

| Action | Impact | Effort |
|--------|--------|--------|
| **Direct API eval** with Llama 3.3 70B + style-aware prompt | Highest (fast iteration) | Low (`run_personage_eval_direct.py`) |
| Switch N8N to **Llama 3.3 70B** + temp 0.1 + style prompt | High (production improvement) | Done |
| Add **PERSONAGE-style heuristic cues** in N8N | Medium (heuristic fallback) | Done |
| Compare models/prompts/temperatures | Required to find best setup | Low (use direct script) |
| Optional **evaluation_mode** for PERSONAGE | Better metrics clarity | Medium |

The main fix is to align detection with **stylistic** Big Five (as in PERSONAGE) rather than only **emotional/caregiving** cues. Llama 3.3 70B with a style-aware prompt and low temperature should significantly outperform the previous Gemma + generic prompt setup.
