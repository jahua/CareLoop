# Phase 5: PANDORA Big Five Evaluation (overview)

**Canonical specification:** **[PHASE5-SPECIFICATION.md](./PHASE5-SPECIFICATION.md)** — file layout, dataset organization, data transforms, N8N workflow naming, testing levels, and versioning.

This page is a short overview; use the spec for implementation details.

---

## References

| Resource | URL |
|----------|-----|
| **PANDORA Big5 (HF)** | [jingjietan/pandora-big5](https://huggingface.co/datasets/jingjietan/pandora-big5) |
| **Automated Personality Prediction (subset, HF)** | [Fatima0923/Automated-Personality-Prediction](https://huggingface.co/datasets/Fatima0923/Automated-Personality-Prediction) |
| **Original paper (ACL)** | [PANDORA Talks (ACL 2020)](https://aclanthology.org/2020.acl-main.614/) |

---

## Quick facts

| Item | Value |
|------|--------|
| **Workflow export** | `workflows/n8n/big5loop-pandora-eval-v4.json` |
| **Webhook path** | `big5loop-pandora-eval-v4` (POST) |
| **Raw data (local)** | `evaluation_data/pandora/raw/` (gitignored) |
| **Processed eval rows** | `evaluation_data/pandora/processed/pandora_eval.jsonl` (see spec §5.2) |
| **Download** | `python scripts/download_pandora.py` |

---

## Example webhook body

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "turn_index": 1,
  "message": "Your Reddit post text here...",
  "evaluation_mode": true,
  "ground_truth_ocean": { "O": 0.2, "C": -0.1, "E": 0.5, "A": 0.0, "N": -0.3 },
  "pandora_sample_id": "pandora-12345"
}
```

Ground truth must use **`O, C, E, A, N`** in **[-1, 1]** after preprocessing (see **PHASE5-SPECIFICATION.md §5.3**).

---

## Metrics & privacy

- **Metrics:** Same family as PERSONAGE/BIG5-CHAT (correlation, MAE per trait) — see **PHASE5-SPECIFICATION.md §5.4**.
- **Privacy:** PANDORA uses public Reddit data; follow HF licenses and institutional ethics when citing samples.
