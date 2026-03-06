# Publication-Ready Figure Captions

Complete figure captions for manuscript integration.

---

## Figure 1. Performance Comparison: Regulated vs Baseline

**Filename:** `01_performance_comparison.png`

**Caption:**

Mean performance scores (0-1 scale) across three evaluation metrics for regulated (personality-adaptive) and baseline (non-adaptive) conditions. Error bars represent 95% confidence intervals. Both conditions achieved perfect emotional tone appropriateness (1.00). The regulated condition showed perfect relevance and coherence (1.00) compared to near-perfect baseline performance (0.98, d = 0.18). Most notably, personality-adaptive regulation dramatically outperformed baseline in addressing personality-specific needs (1.00 vs 0.09, Cohen's d = 4.58), demonstrating that theoretical grounding enables selective enhancement where personality matters most. N=59 (regulated), N=58-60 (baseline, varies by metric).

**Short Caption (if needed):**

Performance comparison showing dramatic improvement in personality needs addressed (Cohen's d = 4.58) while maintaining equivalent general conversational quality. Error bars show 95% CI.

---

## Figure 2. Effect Sizes (Cohen's d)

**Filename:** `02_effect_sizes.png`

**Caption:**

Effect sizes (Cohen's d) quantifying the magnitude of differences between regulated and baseline conditions across evaluation metrics. Vertical dashed lines indicate conventional effect size boundaries: |d| = 0.2 (small), 0.5 (medium), 0.8 (large). Personality-adaptive regulation produced a very large effect on addressing personality needs (d = 4.58), demonstrating substantial practical significance. Effect sizes for emotional tone (d = 0.00) and relevance (d = 0.18) were negligible, indicating that personality adaptation selectively enhances individualization without compromising general conversational quality. This pattern�dramatic gains where personality matters, no change elsewhere�validates theory-driven adaptation over generic quality improvements.

**Short Caption:**

Effect sizes showing very large improvement in personality needs (d = 4.58) with negligible effects on general quality metrics, confirming selective personalization enhancement.

---

## Figure 3. Personality Needs Addressed: Dramatic Improvement with Adaptation

**Filename:** `03_personality_needs.png`

**Caption:**

Success rates for addressing personality-specific needs (primary outcome). The personality-adaptive regulated condition achieved 100% success (59/59 responses appropriately aligned with detected Big Five profiles and Zurich Model predictions), compared to 8.6% in the non-adaptive baseline (5/58 responses). This 91.4 percentage point improvement (Cohen's d = 4.58, p < 0.001) represents a very large effect, demonstrating that explicit theoretical mapping from personality traits to motivational domains (security, arousal, affiliation) enables dramatic improvements in individualized support. This selective enhancement�present only for personality-specific metrics�confirms that observed improvements reflect genuine personalization rather than general quality increases.

**Short Caption:**

Primary outcome showing 91.4% improvement in addressing personality needs with adaptive regulation (Cohen's d = 4.58, very large effect).

---

## Figure 4. Sample Distribution and Data Quality

**Filename:** `04_sample_quality.png`

**Caption:**

Sample characteristics for the controlled simulation study. (A) Number of conversations per personality type, showing balanced representation across Type A (all OCEAN traits +1; n=5 conversations) and Type B (all traits -1; n=5 conversations). This 2�2 factorial design (2 personality types � 2 conditions) provides systematic evaluation of adaptation effects under boundary conditions. (B) Distribution of conversation lengths (dialogue turns), demonstrating consistent 6-turn structure across all conversations. This controlled design ensures valid comparisons by eliminating confounds from variable conversation lengths or unbalanced personality sampling, enabling precise quantification of personality-adaptive regulation effects.

**Short Caption:**

Sample characteristics showing (A) balanced representation of boundary-condition personality profiles and (B) consistent conversation length structure.

---

## Figure 5. OCEAN Personality Dimensions Distribution (Optional/Supplementary)

**Filename:** `05_personality_profiles.png`

**Caption:**

Distribution of detected Big Five (OCEAN) personality trait values across all regulated condition dialogue turns. Each panel shows frequency distribution for one dimension: Openness (O), Conscientiousness (C), Extraversion (E), Agreeableness (A), and Neuroticism (N). Values of +1 indicate high trait expression, -1 indicates low expression, and 0 indicates neutral/ambiguous. The bimodal distributions reflect the study's boundary-condition design comparing extreme profiles (Type A: all traits +1; Type B: all traits -1), enabling clear differentiation of adaptation effects. Perfect detection accuracy (100%, 58/58 valid responses) demonstrates feasibility of real-time personality inference for dynamic conversational adaptation.

**Short Caption:**

OCEAN personality trait distributions showing bimodal patterns reflecting boundary-condition design (Type A vs Type B profiles).

---

## Figure 6. System Architecture Overview

**Filename:** `06_system_architecture.png`

**Caption:**

Conceptual architecture of the personality-adaptive conversational system. The pipeline progresses through four stages: (1) User Input & Context collection, (2) Personality Detection using linguistic analysis to infer Big Five traits, (3) Behavior Adaptation applying Zurich Model mappings to regulate response strategies, and (4) Response generation tailored to detected personality and motivational needs. The evaluation framework consists of three components: AI-based evaluation of all 120 dialogue turns, human expert validation of a stratified 25% sample (n=30), and statistical analysis. High inter-rater reliability between AI and human evaluators (Cohen's ? = 0.89) and between human raters (Krippendorff's ? = 0.82) validates the evaluation methodology. This architecture demonstrates feasibility of theory-driven personality-adaptive conversational AI using current LLM technology.

**Short Caption:**

System architecture showing detection-adaptation-response pipeline with dual AI/human evaluation framework (? = 0.89).

---

## Figure 7. Study Design and Workflow

**Filename:** `07_study_workflow.png`

**Caption:**

Four-stage research methodology for controlled simulation study. Stage 1 (Setup): 20 conversational agents (10 per personality type) deployed across 2 conditions (regulated vs baseline) in a 2�2 factorial design. Stage 2 (Execution): 120 simulated dialogues (6 turns each) generated using standardized prompts with binary evaluation criteria (Yes=1, No=0) for consistent scoring. Stage 3 (Evaluation): Dual assessment combining exhaustive AI evaluation (n=120 turns) with human expert validation of stratified sample (n=30 turns, 25%), achieving strong inter-rater reliability (AI-human: ?=0.89; human-human: ?=0.82). Stage 4 (Results): Statistical analysis revealing dramatic personalization improvements (Cohen's d = 4.58) for personality needs while maintaining equivalent general quality. This rigorous methodology establishes proof-of-concept for personality-adaptive AI under controlled conditions while identifying validation requirements for real-world deployment.

**Short Caption:**

Four-stage research workflow: setup (20 agents, 2�2 design) ? execution (120 dialogues) ? evaluation (dual AI/human) ? results (d = 4.58).

---

## Usage Notes

### For Main Manuscript

Use Figures 1-4 and 6-7 (6 core figures) in the main Results section.

### For Supplementary Materials

Include Figure 5 (personality profiles) as supplementary analysis for readers interested in deeper personality distribution patterns.

### APA Style

```
Figure 1

[Insert figure]

Performance comparison showing dramatic improvement in personality needs 
addressed. Error bars show 95% CI.

Note. Regulated n=59, Baseline n=58-60 (varies by metric). Cohen's d values: 
Emotional Tone = 0.00, Relevance = 0.18, Personality Needs = 4.58.
```

### LaTeX Style

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\textwidth]{figures/01_performance_comparison.png}
  \caption{Performance comparison showing dramatic improvement in personality 
           needs addressed (Cohen's d = 4.58) while maintaining equivalent 
           general conversational quality. Error bars show 95\% CI. 
           Regulated n=59, Baseline n=58-60.}
  \label{fig:performance}
\end{figure}
```

### MDPI Style

```markdown
![Figure 1](figures/01_performance_comparison.png)

**Figure 1. Performance Comparison: Regulated vs Baseline.** Mean performance 
scores across three evaluation metrics. Error bars represent 95% confidence 
intervals. Personality-adaptive regulation produced very large effects for 
personality needs (Cohen's d = 4.58) while maintaining equivalent performance 
on general quality metrics.
```

---

## Caption Length Guidelines

| Journal | Recommended Length |
|---------|-------------------|
| **MDPI** | 100-300 words |
| **IEEE** | 50-150 words |
| **Nature** | 100-200 words |
| **Science** | 50-100 words |

Use **full captions** for MDPI/Nature journals. Use **short captions** for IEEE/Science journals.

---

## Accessibility Notes

All figures include:
- ? High contrast colors (WCAG AA compliant)
- ? Colorblind-friendly palette
- ? Clear axis labels
- ? Readable fonts (9-12pt)
- ? Alternative text in captions

For screen readers, captions should fully describe the figure content without relying on visual information alone.

---

**Last Updated:** January 16, 2026  
**Version:** 2.0  
**Status:** Publication Ready
