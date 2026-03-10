# Big5Loop Evaluation Data

This folder contains personality-related datasets used as **ground truth** for simulated evaluation of Big5Loop's personality-aware dialogue system (OCEAN detection, EMA regulation, and style adaptation).

**Datasource description**: See [DATASOURCE-DESCRIPTION.md](./DATASOURCE-DESCRIPTION.md) for provenance, schema, and citations.

## Datasets Overview

| Dataset | Status | Format | Use Case |
|---------|--------|--------|----------|
| **BFI2** | ✅ Present | CSV | Ground-truth personality profiles (60 items → 5 domains) |
| **BIG5-CHAT** | ✅ Present | CSV | Dialogue pairs with (trait, level) for response-style evaluation |
| **PERSONAGE** | ✅ Present | TAB/XML | Utterances with human Big Five ratings (1–7 scale) |
| **NEO-PI-R** | ✅ Partial | SAV/CSV | Validated personality instrument; alternative gold profiles |
| **BFI-2-R** | ❌ Restricted | — | IEEE DataPort; requires subscription |

---

## Using These Datasets as Ground Truth for Big5Loop Simulated Evaluation

### 1. BFI2 (`raw/bfi2_dataset.csv`)

- **Source**: ShinyItemAnalysis R package
- **Content**: 1,733 respondents, 60 items (5-point Likert), domains: E, A, C, N, O
- **Use for Big5Loop**:
  - Sample rows to derive **target OCEAN profiles** (e.g., high-N, high-C, mixed)
  - Simulate users with known personality; run Big5Loop detection → compare inferred OCEAN to ground truth
  - Build regression test suites: golden conversations for high-N, high-C, mixed profiles (per Technical Spec §13)

### 2. BIG5-CHAT (`raw/big5_chat_dataset.csv`)

- **Source**: Hugging Face `wenkai-li/big5_chat`
- **Content**: 100,000 dialogues with `trait`, `level` (low/high), `train_input`, `train_output`
- **Use for Big5Loop**:
  - Use `train_input` as user message; run Big5Loop; compare output style to `train_output` (or use LLM-as-judge for personality consistency)
  - Evaluate whether Big5Loop adapts responses to match target trait/level (e.g., low openness vs high openness)
  - Benchmark policy Q/A packs with personality-styled delivery (per Technical Spec §13)

### 3. PERSONAGE (`raw/predefinedParams.tab`, `raw/randomParams.tab`) — **Best for evaluation**

- **Source**: PERSONAGE project (Mairesse & Walker, 2006–2008)
- **Content**: 580 utterances with human ratings (1–7) for **all 5 OCEAN traits** per sample
- **Use for Big5Loop**:
  - **Full OCEAN comparison**: each utterance has ground truth O, C, E, A, N (unlike BIG5-CHAT’s single-trait annotation)
  - Feed `realization` to Big5Loop; compare detected OCEAN with `avg.extra`, `avg.agree`, `avg.consc`, `avg.open`, `avg.ems`
  - See [personage/README.md](./personage/README.md) for workflow

### 4. NEO-PI-R (Pitt D-Scholarship)

- **Source**: D-Scholarship@Pitt, https://d-scholarship.pitt.edu/35840/
- **Content**: Validity NEO participant data (`.sav`), codebook
- **Use for Big5Loop**:
  - Alternative gold profiles for validation
  - Cross-check BFI2-derived profiles with NEO-PI-R structure

### 5. BFI-2-R (IEEE DataPort) — Restricted

- **Source**: https://ieee-dataport.org/documents/bfi-2-r
- **Access**: Requires IEEE account + IEEE DataPort subscription
- **Use for Big5Loop**: Supplementary Rasch-validated Italian BFI-2 data if needed

---

## Download Instructions

### BFI2 (ShinyItemAnalysis)

```r
# In R
install.packages("ShinyItemAnalysis")
library(ShinyItemAnalysis)
data(BFI2)
write.csv(BFI2, "evaluation_data/raw/bfi2_dataset.csv", row.names = FALSE)
```

### BIG5-CHAT (Hugging Face)

```bash
# Using Hugging Face datasets
pip install datasets
```

```python
from datasets import load_dataset
ds = load_dataset("wenkai-li/big5_chat", split="train")
ds.to_csv("evaluation_data/raw/big5_chat_dataset.csv", index=False)
```

Or download from: https://huggingface.co/datasets/wenkai-li/big5_chat

### PERSONAGE

- **URL**: https://farm2.user.srcf.net/research/personage/README.html
- **Files**: `predefinedParams.xml`, `randomParams.xml`, `predefinedParams.tab`, `randomParams.tab`
- **Direct links** (if available):
  - `predefinedParams.xml`: https://farm2.user.srcf.net/research/personage/predefinedParams.xml
  - `randomParams.xml`: https://farm2.user.srcf.net/research/personage/randomParams.xml

### NEO-PI-R (Pitt D-Scholarship)

- **URL**: https://d-scholarship.pitt.edu/35840/
- **License**: CC BY-ND
- **Files**: `35840_Validity_NEO-Participant_NEW_FINAL.sav`, `35840_Validity_NEO_codebook.docx`
- Download manually from the repository page.

### BFI-2-R (IEEE DataPort) — Restricted

1. Create/login at https://ieee-dataport.org
2. Subscribe to IEEE DataPort (individual or institutional)
3. Go to https://ieee-dataport.org/documents/bfi-2-r
4. Click “Login to access dataset files”

---

## Directory Structure

```
evaluation_data/
├── raw/                    # Original datasets (do not edit)
│   ├── big5_chat_dataset.csv
│   ├── bfi2_dataset.csv
│   ├── predefinedParams.*, randomParams.*  (PERSONAGE)
│   └── 35840_*             (NEO-PI-R)
├── processed/              # BIG5-CHAT preprocessed outputs
│   ├── big5_chat_eval.jsonl
│   └── eval_results.jsonl
├── personage/              # PERSONAGE evaluation (full OCEAN — best for eval)
│   ├── processed/
│   │   ├── personage_eval.jsonl
│   │   └── personage_eval_results.jsonl
│   └── README.md
├── scripts/
│   ├── preprocess_big5_chat.py
│   ├── preprocess_personage.py
│   ├── run_big5_eval.py
│   ├── run_personage_eval.py
│   ├── visualize_agreement.py
│   └── visualize_personage.py
└── README.md
```

## Current Contents

- **raw/**: BFI2, BIG5-CHAT, PERSONAGE, NEO-PI-R (partial)
- **processed/**: `big5_chat_eval.jsonl`, `big5_chat_eval.csv` (run `scripts/preprocess_big5_chat.py` to generate)

---

## Simulation Evaluation (User + Sessions)

Evaluation runs use a dedicated **eval user** so sessions are classified as **simulation, not real person**:

1. Run migration: `psql $DATABASE_URL -f Big5Loop/infra/database/migration-big5-eval.sql`
2. Create sessions: `python scripts/create_eval_sessions.py [--format jsonl|csv]`
3. Output saved to `processed/big5_eval_sessions.jsonl` or `.csv`
4. Sessions are stored in DB; review via Audit (login: big5_eval@big5loop.ch)

**Classification**: `user_id = eval user` → simulation evaluation. Exclude from real-user analytics.

---

## Evaluation (Feed Data → Save Detected OCEAN → Compare with Annotations)

**Evaluation** = feed inputs to Big5Loop → save detected OCEAN → compare with dataset annotations.

### PERSONAGE (recommended: full OCEAN per sample)

```bash
python scripts/preprocess_personage.py
python scripts/run_personage_eval.py --limit 50
python scripts/visualize_personage.py
```

Each sample has ground truth for all 5 traits (O, C, E, A, N). Best for correlation and MAE analysis.

### BIG5-CHAT (single-trait annotation)

### 1. Run evaluation (requires Big5Loop + N8N running)

**API-only (no DB migration):**

```bash
cd evaluation_data
pip install -r requirements-eval.txt
python scripts/preprocess_big5_chat.py --sample 100   # if not done
python scripts/run_big5_eval.py --api-only --limit 100
```

Reads from `big5_chat_eval.jsonl`, generates session IDs on the fly, POSTs to `/api/chat`. No database or migration needed.

**With DB (for audit/review):**

```bash
psql $DATABASE_URL -f Big5Loop/infra/database/migration-big5-eval.sql
python scripts/create_eval_sessions.py
python scripts/run_big5_eval.py --limit 100
```

This feeds each input to `/api/chat`, collects `personality_state.ocean` from the response, and saves to `processed/eval_results.jsonl`. The N8N workflow also persists turns and OCEAN to the database.

### 2. Visualize agreement (detected vs annotated)

```bash
# From eval results file
python scripts/visualize_agreement.py

# From database (after eval turns saved)
export $(grep -v '^#' ../.env | xargs)
python scripts/visualize_agreement.py --db

# Demo with synthetic OCEAN (when Big5Loop not running)
python scripts/visualize_agreement.py --demo
```

Output:
- **Agreement**: `agreement_by_trait.png`, `detected_vs_annotated.png`, `agreement_overall.png`
- **Data-science**: `detected_vs_ground_truth_scatter.png` (regression + correlation), `detected_ocean_heatmap.png`, `detected_distribution_by_ground_truth.png`, `eval_metrics_summary.png`
- **Export**: `eval_summary.csv` (detected vs ground truth per sample)

---

## Preprocessing

To generate Big5Loop-ready evaluation data from BIG5-CHAT:

```bash
cd evaluation_data
python3 scripts/preprocess_big5_chat.py --sample 100   # 1,000 rows
# or
python3 scripts/preprocess_big5_chat.py               # full dataset (~98k rows)
```

Output: `processed/big5_chat_eval.jsonl`, `processed/big5_chat_eval.csv`

---

## Simulated Evaluation Workflow (Proposed)

1. **Load ground truth** from BFI2, BIG5-CHAT, or PERSONAGE.
2. **Generate test cases**:
   - For BFI2: user profiles from item scores; sample prompts.
   - For BIG5-CHAT: `(train_input, trait, level)` → expected style in `train_output`.
   - For PERSONAGE: `realization` + `avg.*` ratings → expected personality.
3. **Run Big5Loop**:
   - Send user message → get response with OCEAN state.
   - Compare inferred OCEAN to ground truth (BFI2, NEO-PI-R).
   - Compare response style to expected (BIG5-CHAT, PERSONAGE) via LLM-as-judge or human rating.
4. **Report**:
   - OCEAN correlation (Pearson/Spearman)
   - Style consistency (personality match score)
   - Citation coverage and policy correctness (per Technical Spec §14)
