# Executive Summary

Objective: Test whether real‑time personality‑aware regulation (based on Big Five/OCEAN and Zurich Model) improves emotional‑support chatbot interactions versus non‑adaptive baselines.

Approach: Detect per‑turn OCEAN traits (+1/0/−1) from user text via modular prompt‑engineered detectors; immediately map traits to behavior prompts aligned with Zurich Model domains (security, arousal, affiliation); regenerate assistant reply accordingly. Evaluate regulated vs baseline on tone, relevance/coherence, and personality‑need satisfaction; regulated also on detection/regulation correctness.

Findings: Regulated assistants outperform baselines. On shared criteria (tone, relevance/coherence, needs), regulated reached 36/36 for both extreme personas; baselines ~24/36. Overall, ~34% improvement. Qualitative examples show better emotional alignment and tailored structure.

Implications: Dynamic personality detection + trait‑to‑prompt regulation reliably improves perceived support quality in controlled, short dialogues. Useful for elder care and supportive AI. Requires real‑user validation and a robust, non‑brittle detector for deployment.
