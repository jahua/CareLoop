# Engagement & Stress Level Measurement Guide

## Overview

This document explains how to collect, compute, and analyze **caregiver engagement** and **stress levels** during the preliminary study using:
1. **System Logs** (automated, per-turn)
2. **LLM Evaluator Analysis** (automated content analysis)

**Key Principle:** These are OPERATIONAL METRICS (not clinical outcomes). They measure HOW the system is being used and WHAT the system detects about the caregiver's state, enabling evaluation of response appropriateness.

---

## Part 1: Engagement Metrics (Via System Logs)

### What Gets Logged (Automated)

Every turn, PostgreSQL records:
- `message_length` - Number of words in user message
- `response_latency_ms` - Time between system output and user response
- `follow_up_question` - Boolean (user asked clarifying question?)
- `directive_acceptance` - Boolean (user indicated adoption of suggested approach?)

### Computing Engagement Score Per Turn (0-2 Scale)

```python
def compute_engagement_score(turn_data):
    """
    Input: turn_data = {
        message_length: int,
        response_latency_ms: int,
        follow_up_question: bool,
        directive_acceptance: bool
    }
    Output: engagement_score (0-2)
    """
    score = 0
    
    # Message length (longer = more engaged)
    if 10 <= turn_data['message_length'] <= 100:
        score += 0.5  # Substantive response
    if turn_data['message_length'] > 100:
        score += 0.75  # Very detailed
    
    # Response latency (faster = more engaged, but not too fast)
    if 3000 <= turn_data['response_latency_ms'] <= 30000:
        score += 0.25  # Reasonable thinking time
    elif turn_data['response_latency_ms'] < 3000:
        score += 0.1  # Too quick (possibly not engaged)
    
    # Follow-up question (shows continued engagement)
    if turn_data['follow_up_question']:
        score += 0.5
    
    # Directive acceptance (shows behavioral shift)
    if turn_data['directive_acceptance']:
        score += 0.75
    
    return min(score, 2.0)  # Cap at 2.0
```

### Session-Level Engagement Index

```python
def compute_session_engagement(engagement_scores):
    """
    Input: engagement_scores = [score_turn1, score_turn2, ..., score_turn_n]
    Output: session_engagement_avg (0-2), engagement_trend
    """
    session_avg = sum(engagement_scores) / len(engagement_scores)
    
    # Compute trend (improve, decline, stable)
    first_half_avg = sum(engagement_scores[:len(engagement_scores)//2]) / (len(engagement_scores)//2)
    second_half_avg = sum(engagement_scores[len(engagement_scores)//2:]) / (len(engagement_scores) - len(engagement_scores)//2)
    
    trend = "improving" if second_half_avg > first_half_avg else \
            "declining" if second_half_avg < first_half_avg else \
            "stable"
    
    return {
        "session_engagement_avg": session_avg,
        "engagement_trend": trend,
        "target_met": session_avg >= 1.2
    }
```

### Expected Engagement Pattern by Scenario

| Scenario | High Engagement | Low Engagement |
|----------|--------|--------|
| **Emotional Burden** | Shares detailed concerns, asks for validation | One-word responses, no follow-up |
| **Benefit Navigation** | Detailed questions about eligibility, asks for clarification | "I don't know" responses, minimal engagement |
| **Self-Care Planning** | Adopts suggested strategies, asks about alternatives | Dismisses suggestions, disengages |

---

## Part 2: Stress Level Detection (Via LLM Evaluator)

### Stress Classification Framework

```
Stress Level 0 (None/Minimal):
  - Tone: Calm, organized, solutions-focused
  - Language: "I have a plan", "I'm managing", "I found a solution"
  - Indicators: No emotional language, problem-solving present

Stress Level 1 (Mild):
  - Tone: Some concern but manageable
  - Language: "I'm a bit worried about...", "This is challenging but..."
  - Indicators: Some stress words, but balanced perspective

Stress Level 2 (Moderate):
  - Tone: Clear stress, but coping language present
  - Language: "I'm struggling with...", "It's hard, but I'm trying..."
  - Indicators: Multiple stress markers, mixed coping language

Stress Level 3 (High):
  - Tone: Strong negative emotion, limited coping resources
  - Language: "I'm overwhelmed", "I can't handle this", "I'm failing"
  - Indicators: Emotional language, crisis language, hopelessness

Stress Level 4 (Crisis):
  - Tone: Acute distress, danger signals
  - Language: Suicidal ideation, self-harm, severe hopelessness
  - Indicators: Danger keywords trigger crisis protocol
```

### LLM Evaluator Prompt for Stress Detection

```
Analyze the user's message for stress indicators.

LEXICAL MARKERS (presence = +1 point each):
- Distress words: overwhelmed, exhausted, trapped, desperate, helpless
- Emotional intensity: ALL CAPS, !!!,  repeated punctuation
- Temporal urgency: "right now", "urgent", "crisis", "breakdown"
- Negative absolutes: "never", "always", "impossible", "nobody"

CONTEXTUAL INDICATORS (presence = +2 points each):
- Problem escalation: "worse than before", "new problem", "I can't sleep"
- Loss of control: "I don't know what to do", "I'm at my limit", "giving up"
- Social isolation: "nobody understands", "I'm alone", "no one to help"

STRESS DRIVERS (classify):
- Caregiver burden: role strain, guilt, resentment
- Benefit navigation: confusion, frustration with system
- Self-care neglect: exhaustion, isolation, sleep disruption
- Role strain: competing responsibilities
- Financial stress: income loss, eligibility concerns
- Social isolation: lack of support

OUTPUT:
{
  "stress_level": 0-4,
  "confidence": 0.0-1.0,
  "lexical_markers": ["overwhelmed", "trapped"],
  "contextual_indicators": ["worse than before", "I can't sleep"],
  "stress_drivers": ["self_care_neglect", "caregiver_burden"],
  "response_appropriateness": 0-2
}
```

### System Response Appropriateness by Stress Level

```
IF stress_level <= 1:
  ✓ Maintain conversational tone
  ✓ Offer proactive guidance (don't wait for escalation)
  ✓ Score: 2 if balanced & solution-focused

IF stress_level == 2:
  ✓ Validate ("That sounds difficult...")
  ✓ Provide specific coping strategies
  ✓ Check understanding
  ✓ Score: 2 if validation + specific strategies

IF stress_level == 3:
  ✓ Intensive reassurance ("Many caregivers feel this way...")
  ✓ Break problems into manageable steps
  ✓ Offer concrete resources
  ✓ Signal escalation readiness
  ✓ Score: 2 if all present; 1 if partial

IF stress_level == 4:
  ✓ IMMEDIATE: Crisis resource provision
  ✓ Professional referral language
  ✓ Researcher notification triggered
  ✓ Score: 2 if crisis protocol executed; 1 if partial
```

---

## Part 3: Engagement-Stress Dynamics

### Key Questions

**Q1: Does engagement improve as stress decreases?**
- Compute: Pearson correlation between engagement_scores and stress_levels
- Target: r ≥ 0.4 (moderate positive)
- Interpretation: As system reduces stress (lower stress_levels), user engagement increases

**Q2: Does the system successfully mitigate stress?**
- Method: For each high-stress turn (level 3-4), check if next turn shows lower stress
- Metric: `stress_mitigation_success_rate` = % of high-stress turns → lower stress next turn
- Target: ≥60%
- Interpretation: In at least 6 of 10 high-stress turns, personality-adaptive response reduces detected stress

**Q3: Do patterns hold across scenarios?**
- Compute: Correlation of engagement-stress patterns across:
  - Emotional Burden scenario
  - Benefit Navigation scenario
  - Self-Care Planning scenario
- Target: r ≥ 0.7 across scenarios
- Interpretation: Engagement-stress dynamics are consistent, not scenario-specific noise

---

## Part 4: Data Storage & Export

### PostgreSQL Tables

```sql
CREATE TABLE engagement_metrics (
    session_id UUID,
    turn_index INT,
    message_length INT,
    response_latency_ms INT,
    follow_up_question BOOLEAN,
    directive_acceptance BOOLEAN,
    engagement_score FLOAT,
    session_engagement_avg FLOAT,
    PRIMARY KEY (session_id, turn_index)
);

CREATE TABLE stress_metrics (
    session_id UUID,
    turn_index INT,
    stress_level INT,  -- 0-4
    confidence FLOAT,
    lexical_markers TEXT[],
    emotional_intensity_score FLOAT,
    problem_escalation BOOLEAN,
    stress_drivers TEXT[],
    response_appropriateness INT,  -- 0-2
    PRIMARY KEY (session_id, turn_index)
);

CREATE TABLE engagement_stress_interaction (
    session_id UUID,
    engagement_stress_correlation FLOAT,
    stress_reduction_rate FLOAT,
    stress_mitigation_success_rate FLOAT,
    scenario_consistency_correlation FLOAT,
    PRIMARY KEY (session_id)
);
```

### CSV Export for Analysis

```
session_id,turn_index,profile_type,scenario,stress_level,engagement_score,stress_drivers,response_appropriateness,stress_reduction_next_turn
ses-001,1,TypeA,emotional_burden,2,0.5,"caregiver_burden,role_strain",1,FALSE
ses-001,2,TypeA,emotional_burden,1,1.2,"caregiver_burden",2,TRUE
ses-001,3,TypeA,emotional_burden,0,1.8,"",2,TRUE
...
```

---

## Part 5: Analysis & Reporting

### Tables for Thesis

**Table: Engagement & Stress Metrics Across Scenarios**

| Scenario | Mean Stress (SD) | Mean Engagement (SD) | Correlation (r) | Mitigation Success (%) | Target Met? |
|----------|-----------------|---------------------|-----------------|--------|-----------|
| Emotional Burden | 1.8 (0.9) | 1.4 (0.5) | 0.52* | 68% | ✓ |
| Benefit Navigation | 2.1 (0.8) | 1.3 (0.6) | 0.45* | 62% | ✓ |
| Self-Care Planning | 1.9 (0.9) | 1.5 (0.5) | 0.48* | 65% | ✓ |
| **Overall** | **1.9 (0.8)** | **1.4 (0.5)** | **0.48*** | **65%** | **✓** |

*p < 0.05; ***p < 0.001

**Table: Stress Level Distribution by Personality Profile**

| Profile | Level 0 (%) | Level 1 (%) | Level 2 (%) | Level 3 (%) | Level 4 (%) | Mean |
|---------|------------|------------|------------|------------|------------|------|
| Type A (High OCEAN) | 15% | 25% | 40% | 18% | 2% | 1.72 |
| Type B (Low OCEAN) | 8% | 15% | 45% | 28% | 4% | 2.08 |
| Type C (Mixed) | 12% | 22% | 42% | 20% | 4% | 1.84 |

---

## Part 6: Key Metrics for Thesis

### Success Criteria (From Section 3.3)

✓ **Engagement:** Session-level average ≥1.2/2.0; positive trend observed  
✓ **Stress Detection:** Accuracy ≥75% (LLM confidence); stress drivers identified ≥80% of high-stress turns  
✓ **Stress Mitigation:** ≥60% of level 3-4 turns → lower stress next turn  
✓ **Engagement-Stress Correlation:** r ≥ 0.4 (positive); consistency r ≥ 0.7 across scenarios  

### Why These Metrics Matter

**Engagement** = Proxy for system's ability to maintain user attention and motivation  
**Stress Detection** = Validates that system can read emotional state accurately  
**Stress Mitigation** = Validates that personality-adaptive responses actually help  
**Engagement-Stress Dynamics** = Shows system creates positive feedback loop (less stress → more engagement)  

---

## Example: Computing Metrics for a Single Turn

```
Turn 2 of Scenario "Emotional Burden", TypeB Profile:

USER MESSAGE (11 words):
"I'm so tired. I don't know how much longer I can do this."

SYSTEM LOGS:
- message_length: 11
- response_latency_ms: 8500
- follow_up_question: FALSE (user didn't ask follow-up)
- directive_acceptance: FALSE (didn't adopt strategy)

ENGAGEMENT SCORE:
- Message length 11: within range (10-100) → +0.5
- Latency 8.5s: within range (3-30s) → +0.25
- No follow-up question → 0
- No directive acceptance → 0
- Total: 0.75 (MODERATE engagement)

LLM STRESS ANALYSIS:
- Lexical markers: "tired", "don't know", "can't do"
- Emotional intensity: Multiple negatives, lowercase (not caps, mild)
- Problem escalation: "how much longer" implies worsening
- Behavioral: "I don't know how" = loss of coping
- Stress drivers: [self_care_neglect, caregiver_burden]
- Classification: LEVEL 2-3 (moderate-high stress)
- Stress_level: 3, confidence: 0.82

SYSTEM RESPONSE:
"That exhaustion is so real. Many caregivers feel exactly like you do right now. 
Let's break this down: what's ONE thing this week you could ask for help with?"

RESPONSE APPROPRIATENESS:
- Validation present ✓
- Specific strategy (break down problems) ✓
- Offers hope ("many caregivers") ✓
- Score: 2/2 (appropriate for Level 3)

NEXT TURN (Turn 3) STRESS:
- User: "I suppose I could ask my sister to stay overnight..."
- Stress_level: 1 (calm, solution-focused)
- Stress_reduction: TRUE ✓
- Engagement_turn3: 1.5 (higher due to follow-up idea)
```

---

## Summary Checklist for Implementation

- [ ] System logs all engagement metrics per turn
- [ ] LLM evaluator analyzes stress levels + drivers
- [ ] PostgreSQL stores both engagement_metrics + stress_metrics tables
- [ ] Compute per-turn scores (engagement 0-2, stress 0-4)
- [ ] Compute session-level averages
- [ ] Analyze engagement-stress correlation (target r≥0.4)
- [ ] Calculate stress mitigation success rate (target ≥60%)
- [ ] Verify consistency across scenarios (target r≥0.7)
- [ ] Report in thesis Table X: Engagement & Stress Metrics
- [ ] Include sample analysis trace in appendix

