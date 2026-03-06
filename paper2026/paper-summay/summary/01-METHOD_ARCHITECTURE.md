# Method and Architecture

- Personality Detection
  - Output: OCEAN vector per turn with values in {+1,0,−1}; Neuroticism inverted (+1 stable, −1 sensitive)
  - Design: modular Java submodules (one per trait), prompt/rule patterns; concurrent execution; cumulative updates with neutral default until evidence
- Behavior Regulation
  - Map each non‑neutral trait to a prompt (e.g., low O → familiar topics; high C → structured guidance; low E → calm/reflective; low A → neutral stance; low N → extra comfort)
  - Concatenate prompts each turn to form a behavior instruction, aligned to Zurich Model (security, arousal, affiliation)
- Evaluation
  - Regulated: Detection Accuracy, Regulation Effectiveness, Tone, Relevance/Coherence, Needs Addressed
  - Baseline: Tone, Relevance/Coherence, Needs Addressed
  - Scoring 0/1/2 per criterion; aggregate per dialogue and bot; visualize totals
- Simulation
  - Two extreme personas: Type A (+1,+1,+1,+1,+1) and Type B (−1,−1,−1,−1,−1)
  - 5 regulated and 5 baseline bots per persona; 6 turns each; 120 total turns
