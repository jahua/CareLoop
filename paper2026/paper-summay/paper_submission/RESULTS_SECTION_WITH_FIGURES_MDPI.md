# Results Section with MDPI-Formatted Figures and Tables

## Complete Results Section for V4_Healthcare_Submission_processed.md

# Results

## Data Quality and Sample Distribution

The evaluation dataset comprised 59 regulated agent interactions and 58-60 baseline agent interactions (varying by metric) across two extreme personality profiles (Type A: all traits +1; Type B: all traits −1). Figure 1 presents the sample distribution across conditions and personality types.

**[Figure 1 near here]**

**Figure 1.** Sample distribution across experimental conditions. Left panel shows distribution of dialogue turns by personality type (Type A: high-functioning profile; Type B: vulnerable profile). Right panel shows distribution by condition (Regulated vs. Baseline agents). Total n=120 dialogue turns across 20 agent instances.

Data quality assessment revealed minimal missing data (<2%) across all evaluation metrics, with no systematic patterns of missingness by condition or personality type (Figure 2).

**[Figure 2 near here]**

**Figure 2.** Missing data heatmap across evaluation metrics and experimental conditions. White cells indicate complete data; gray cells indicate missing values. Overall missingness rate: 1.7%. No systematic bias detected by condition or personality type.

## Detection and Regulation Performance

Personality detection achieved 100% accuracy (58/58 correct assessments) across extreme personality profiles, with perfect regulation effectiveness (59/59, 100%). Table 1 summarizes the core technical performance metrics.

**Table 1.** Detection and Regulation Performance Summary

| Metric | Success Rate | 95% CI | Performance Level |
|--------|-------------|---------|-------------------|
| Overall Detection Accuracy | 58/58 (100%) | [93.8, 100] | Perfect |
| Regulation Effectiveness | 59/59 (100%) | [93.9, 100] | Perfect |
| Combined Technical Performance | 117/117 (100%) | [96.9, 100] | Perfect |

*Note: Confidence intervals calculated using Clopper-Pearson method for binomial proportions. Perfect scores reflect simulation with extreme personality profiles (+1 or -1 for all traits) and automated GPT-4 evaluation.*

**Detection Performance Analysis**: The personality detection system demonstrated perfect accuracy for extreme personality profiles, validating the technical feasibility of prompt-based personality trait inference in highly controlled simulation conditions. The 100% success rate indicates that the LLM-based detection approach successfully identifies clear, consistent personality signals when traits are expressed at polar extremes.

**Critical Interpretation Context**: Perfect scores must be interpreted within the limitations of the controlled experimental design:
- **Extreme profiles only**: Detection tested exclusively on all-positive (+1,+1,+1,+1,+1) or all-negative (-1,-1,-1,-1,-1) trait combinations, representing the easiest possible detection scenario
- **Simulation environment**: All "user" messages were pre-scripted to consistently exhibit target personality traits across all dialogue turns
- **GPT-4 evaluation**: Automated assessment by the same model family used for detection may introduce systematic bias favoring AI-generated responses
- **Limited generalizability**: Performance with moderate trait values, mixed profiles, or inconsistent personality expressions remains completely untested and likely to be substantially lower

## Personality Vector Analysis

Analysis of detected personality vectors revealed consistent trait patterns across dialogue turns. Figure 3 visualizes the distribution of OCEAN trait values for regulated interactions.

**[Figure 3 near here]**

**Figure 3.** Distribution of detected Big Five (OCEAN) personality trait values. Each panel shows the frequency distribution of trait scores (−1, 0, +1) across all dialogue turns. Type A profiles (blue) cluster at +1; Type B profiles (orange) cluster at −1, confirming successful implementation of extreme personality profiles in simulation.

Figure 4 presents a heatmap visualization of personality patterns across individual agent instances, demonstrating the consistency of personality expression within profiles and clear differentiation between Type A and Type B profiles.

**[Figure 4 near here]**

**Figure 4.** Personality trait heatmap across agent instances and dialogue turns. Rows represent individual agents (A1-A10, B1-B10); columns represent Big Five traits (O, C, E, A, N). Color intensity indicates trait level: red (+1 = high), white (0 = neutral), blue (−1 = low). Clear clustering by personality type validates extreme profile implementation.

## Conversational Quality Assessment

The evaluation revealed a striking selective enhancement pattern: while both regulated and baseline agents performed equivalently on fundamental conversational quality metrics, personality adaptation dramatically improved the system's ability to address personality-specific user needs. Figure 5 presents the overall performance comparison.

**[Figure 5 near here]**

**Figure 5.** Performance comparison across evaluation metrics (Regulated vs. Baseline). Bar heights represent mean success rates; error bars show 95% confidence intervals. Asterisks indicate statistical significance: **p < 0.001; ns = not significant (p > 0.05). Regulated agents show dramatic advantage specifically in Personality Needs Addressed (***) while maintaining equivalent performance on basic quality metrics (Emotional Tone, Relevance & Coherence).

Table 2 provides detailed statistical analysis of performance differences across all evaluation criteria.

**Table 2.** Comprehensive Performance Comparison: Regulated vs. Baseline

| Evaluation Criterion | Regulated (n=59) | Baseline (n=58-60) | Mean Difference | Cohen's d | p-value | Effect Interpretation |
|---------------------|------------------|-------------------|----------------|-----------|---------|----------------------|
| **Detection Accuracy** | 100% (58/58) | N/A | N/A | N/A | N/A | Regulated-only metric |
| **Regulation Effectiveness** | 100% (59/59) | N/A | N/A | N/A | N/A | Regulated-only metric |
| **Emotional Tone Appropriateness** | 100% (59/59) | 100% (60/60) | 0.0% | 0.00 | 1.000 | No difference |
| **Relevance & Coherence** | 100% (59/59) | 98.33% (59/60) | +1.67% | 0.18 | 0.323 | Negligible difference |
| **Personality Needs Addressed** | 100% (59/59) | 8.62% (5/58) | **+91.38%** | **4.58** | **<0.001*** | Very large effect |

*Note: Cohen's d interpretation: 0.2 = small, 0.5 = medium, 0.8 = large, >2.0 = very large. *** indicates p<0.001 (highly significant). N/A = Not Applicable (baseline agents lack detection/regulation capabilities).*

**Key Performance Findings**:

1. **Perfect Technical Implementation**: Both detection (100%, 58/58) and regulation (100%, 59/59) achieved perfect accuracy in the controlled simulation environment, demonstrating technical feasibility of the approach.

2. **Equivalent Basic Quality**: Both conditions performed equivalently on fundamental conversational quality:
   - **Emotional Tone**: Both 100% appropriate (no significant difference, Cohen's d = 0.00, p = 1.000)
   - **Relevance & Coherence**: Minimal difference (Regulated 100% vs Baseline 98.33%; difference = 1.67%, Cohen's d = 0.18, p = 0.323)

3. **Dramatic Personalization Advantage**: The largest and most significant difference emerged in personality-specific adaptation:
   - **Personality Needs Addressed**: Regulated 100% vs Baseline 8.62%
   - **Effect Size**: Cohen's d = 4.58 (very large effect)
   - **Statistical Significance**: p < 0.001 (highly significant)
   - **Practical Impact**: 91.38 percentage point improvement

## Effect Size Analysis

Figure 6 visualizes the effect sizes (Cohen's d) for each evaluation metric, highlighting the magnitude of performance differences.

**[Figure 6 near here]**

**Figure 6.** Effect sizes (Cohen's d) for performance differences between regulated and baseline agents. Horizontal dashed lines indicate conventional effect size thresholds: small (d = 0.2), medium (d = 0.5), large (d = 0.8). The dramatic effect for Personality Needs Addressed (d = 4.58) far exceeds conventional thresholds, while Emotional Tone and Relevance show negligible effects (d < 0.2), confirming selective enhancement pattern.

Figure 7 presents the percentage improvement across metrics, providing an alternative visualization of the selective enhancement pattern.

**[Figure 7 near here]**

**Figure 7.** Percentage improvement from baseline to regulated conditions across evaluation metrics. Personality Needs Addressed shows 91.38 percentage point improvement (1059% relative improvement from 8.62% baseline), while other metrics show minimal or no improvement, demonstrating that personality adaptation specifically targets personalization without affecting basic quality standards.

## Weighted Scoring Analysis

To provide additional quantitative perspective, we analyzed performance using a weighted scoring system where evaluations were scored as YES=2 points, NOT SURE=1 point, NO=0 points (Table 3).

**Table 3.** Weighted Score Performance Comparison (0-2 Scale)

| Metric | Regulated Mean (SD) | Baseline Mean (SD) | Mean Difference | Cohen's d | Improvement % |
|--------|---------------------|-------------------|-----------------|-----------|---------------|
| Emotional Tone | 2.00 (0.00) | 2.00 (0.00) | 0.00 | 0.00 | 0.0% |
| Relevance & Coherence | 2.00 (0.00) | 1.97 (0.26) | +0.03 | 0.18 | 1.7% |
| Personality Needs | 2.00 (0.00) | 0.20 (0.58) | **+1.80** | **4.42** | **90.0%** |

Figure 8 visualizes the weighted score distributions for each metric.

**[Figure 8 near here]**

**Figure 8.** Distribution of weighted scores (0-2 scale) across evaluation metrics by condition. Box plots show median (center line), interquartile range (box), and full range (whiskers). Regulated agents (blue) achieve consistently maximal scores (median = 2.0) across all metrics. Baseline agents (orange) show equivalent performance for Emotional Tone and Relevance but dramatically lower scores for Personality Needs (median = 0.0).

Figure 9 provides a complementary visualization focusing on the total quality scores.

**[Figure 9 near here]**

**Figure 9.** Box plot comparison of total quality scores (summed across Emotional Tone, Relevance & Coherence, and Personality Needs metrics). Regulated agents show consistently high total scores (median = 6.0, perfect performance), while baseline agents show substantially lower total scores due to failure in addressing personality needs. The lack of overlap between distributions confirms the robustness of the selective enhancement effect.

## Statistical Robustness Analysis

To ensure the robustness of our findings, we conducted both parametric (independent t-tests) and non-parametric (Mann-Whitney U) statistical tests. Table 4 summarizes the results of advanced statistical testing.

**Table 4.** Advanced Statistical Testing Results

| Metric | Independent t-test | Mann-Whitney U | Levene's Test | Normality (Shapiro-Wilk) |
|--------|-------------------|----------------|---------------|-------------------------|
| Emotional Tone | t=0, p=1.000 | U=1770, p=1.000 | p>0.05 (equal var.) | Reg: p=1.000, Base: p=1.000 |
| Relevance & Coherence | t=0.99, p=0.323 | U=1799.5, p=0.330 | p=0.323 (equal var.) | Reg: p=1.000, Base: p<0.001 |
| Personality Needs | t=23.99, p<0.001 | U=3392.5, p<0.001 | p=0.009 (unequal var.) | Reg: p=1.000, Base: p<0.001 |

*Note: Both parametric and non-parametric tests converge on identical conclusions, strengthening confidence in findings despite normality violations for baseline scores.*

**Interpretation**: Both parametric (t-test) and non-parametric (Mann-Whitney U) tests converge on identical conclusions:
- No significant difference in emotional tone (p=1.000)
- No significant difference in relevance & coherence (p=0.323-0.330)
- Highly significant difference in personality needs addressed (p<0.001 for both tests)

The violation of normality assumptions for baseline scores (particularly for Personality Needs) justifies the inclusion of non-parametric tests. Crucially, both test families yield consistent results, strengthening confidence in the findings despite the simulation-based design.

**Important Caveat**: These inferential statistics are included for methodological completeness and to facilitate comparison with related empirical studies. However, given the deterministic simulation design (predefined personality profiles, pre-scripted responses), these p-values should NOT be interpreted as evidence of generalizable population effects. The effect sizes (Cohen's d) provide more appropriate interpretation for this proof-of-concept study.

## Criterion-Specific Analysis

**Regulated Agent Performance Across All Metrics**:
- Detection Accuracy: 58/58 (100%) - All personality trait inferences correct
- Regulation Effectiveness: 59/59 (100%) - All behavioral adaptations appropriate
- Emotional Tone: 59/59 (100%) - All responses emotionally appropriate
- Relevance & Coherence: 59/59 (100%) - All responses relevant and coherent
- Personality Needs: 59/59 (100%) - All personality-specific needs addressed

**Baseline Agent Performance**:
- Emotional Tone: 60/60 (100%) - Equivalent to regulated
- Relevance & Coherence: 59/60 (98.33%) - Nearly equivalent to regulated
- Personality Needs: 5/58 (8.62%) - **Critical failure in personalization**

**Performance Gap Analysis**: The baseline agents demonstrated competent performance on fundamental conversational quality dimensions (emotional appropriateness and logical coherence) but exhibited near-complete failure in addressing personality-specific user needs. This pattern highlights the critical limitation of non-adaptive systems: they can maintain basic interaction quality but cannot provide the personalization essential for optimizing therapeutic effectiveness in healthcare contexts where individual differences significantly influence treatment outcomes.

## Qualitative Examples Demonstrating Personality Adaptation

**Example 1: Vulnerable Population Interaction**

*Detected Profile*: P̂ = (−1, 0, −1, −1, −1) [Low Openness, Neutral Conscientiousness, Low Extraversion, Low Agreeableness, High Neuroticism]

*User Message*: "I'm feeling really overwhelmed and anxious. I don't think talking helps."

*Regulated Response* (Zurich Model-Aligned):
> "I understand you're going through a difficult time, and feeling exhausted is completely natural. This is a safe space where we can focus on small, familiar steps that feel manageable for you right now. We don't have to rush into anything—let's just take it one moment at a time."

*Baseline Response* (Non-Adaptive):
> "It's understandable to feel overwhelmed. Talking about your concerns can help organize your thoughts and develop coping strategies."

**Analysis**: The regulated response demonstrates therapeutic attunement through:
- **Security Domain Activation** (High Neuroticism): Explicit validation, safety reassurance ("This is a safe space")
- **Reduced Arousal** (Low Openness/Extraversion): Emphasis on "familiar steps," calm pacing ("one moment at a time")
- **Respectful Distance** (Low Agreeableness): Non-pressuring approach ("We don't have to rush")

In contrast, the baseline response provides generic support without addressing the user's specific personality-driven needs for emotional security, reduced stimulation, and autonomous pacing.

**Example 2: High-Functioning Population Interaction**

*Detected Profile*: P̂ = (+1, +1, +1, +1, +1) [All traits high]

*User Message*: "I'm ready to make some changes. What should I try first?"

*Regulated Response* (Zurich Model-Aligned):
> "Excellent! Your enthusiasm for exploring new approaches is wonderful. Let's create a structured plan together that builds on your natural strengths. What specific goals would you like to focus on first? We can brainstorm multiple options and organize them systematically."

*Baseline Response* (Non-Adaptive):
> "That's great to hear. Setting goals can be very helpful. What would you like to work on?"

**Analysis**: The regulated response actively engages the user's personality strengths:
- **Arousal Domain** (High Openness/Extraversion): Encourages exploration, multiple options, collaborative energy
- **Affiliation Domain** (High Agreeableness): Warm, collaborative framing ("together")
- **Conscientiousness Engagement**: Structured planning, systematic organization

The baseline response provides generic encouragement without leveraging the user's personality-specific strengths for goal-setting and treatment engagement.

## Summary of Key Findings

1. **Technical Feasibility Demonstrated**: Perfect detection (100%, 58/58) and regulation effectiveness (100%, 59/59) establish proof-of-concept for prompt-based personality-adaptive conversational systems in controlled conditions.

2. **Selective Performance Enhancement**: Personality adaptation specifically enhanced personalization (91.38% improvement, Cohen's d = 4.58, p<0.001) without compromising fundamental conversational quality (emotional tone and relevance maintained at ≥98% for both conditions).

3. **Very Large Effect Size**: The Cohen's d = 4.58 effect for personality needs addressed represents an exceptionally large effect, suggesting substantial practical significance if even partially maintained in real-world validation.

4. **Baseline Limitation Identified**: Non-adaptive baseline agents exhibited critical failure (8.62% success) in addressing personality-specific needs despite adequate performance on generic quality metrics, highlighting the necessity of personalization for therapeutic applications.

5. **Simulation-Specific Context**: All findings derive from controlled simulation with extreme personality profiles and automated evaluation, requiring extensive human subject validation before any claims about real-world effectiveness can be made.

---

## Figure File References for Manuscript Preparation

When preparing the final manuscript, insert the following figure files from the `statistical analyis/figures/` directory:

- **Figure 1**: `01_sample_distribution.png`
- **Figure 2**: `02_missing_data_heatmap.png`
- **Figure 3**: `06_personality_dimensions.png`
- **Figure 4**: `07_personality_heatmap.png`
- **Figure 5**: `03_performance_comparison.png`
- **Figure 6**: `04_effect_sizes.png`
- **Figure 7**: `05_percentage_improvement.png`
- **Figure 8**: `08_weighted_scores.png`
- **Figure 9**: `09_total_score_boxplot.png`

All figures are publication-ready at 300 DPI minimum resolution and follow MDPI formatting guidelines.



