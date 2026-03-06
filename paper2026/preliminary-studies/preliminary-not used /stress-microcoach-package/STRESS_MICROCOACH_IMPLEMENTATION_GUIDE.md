# Stress Micro-Coach Implementation Guide
**Use Case:** Personality-Adaptive Stress Self-Regulation for Adult Learners  
**Version:** 1.0  
**Date:** 2025-10-13

---

## Executive Summary

This guide operationalizes the **Stress Self-Regulation Micro-Coach** as the primary use case for the personality-aware chatbot preliminary study. It provides concrete specifications for the three coaching modes, policy pack configuration, simulation scenarios, and market-ready features.

### Why This Use Case?
- ✅ **Market-validated**: $66B+ corporate wellness market; 60%+ students report overwhelming stress
- ✅ **Low regulatory risk**: Non-clinical coaching boundary; no medical advice
- ✅ **Zurich Model fit**: Perfect mapping to security, arousal, affiliation domains
- ✅ **Measurable outcomes**: Engagement, stress de-escalation, coping skill adoption
- ✅ **High transferability**: Education → workplace → customer service

---

## 1. Three Coaching Modes (Intent-Based Architecture)

### 1.1 Vent & Validate (Affiliation + Security)

**User Need:** Emotional release, affect labeling, validation  
**Zurich Domains:** Affiliation (connection), Security (comfort)  
**Trigger Patterns:** "I'm so overwhelmed...", "Everything is falling apart...", "I can't handle this anymore..."

**Personality Adaptations:**

| Trait | High Expression | Low Expression |
|-------|----------------|----------------|
| **Neuroticism (N)** | Extra reassurance: "It's completely understandable to feel this way. Many people experience this." + Grounding: "Let's take a moment to breathe together." | Pragmatic validation: "That sounds challenging. Let's identify what's within your control." (Move to action faster) |
| **Agreeableness (A)** | Warm, collaborative: "I'm here with you. We'll work through this together." + Empathetic mirroring | Direct acknowledgment: "I understand the situation is difficult." (Avoid excessive warmth) |
| **Extraversion (E)** | Social framing: "Have you been able to talk to anyone about this?" | Reflective space: "Take your time processing this internally." |
| **Openness (O)** | Creative reframing: "What if we looked at this from a different angle?" | Concrete validation: "Let's stick to the facts of what happened." |

**Example Directive (High N, High A):**
```yaml
mode: vent_validate
directives:
  - "Provide warm, empathetic acknowledgment of user's emotional state"
  - "Normalize feelings: 'It's completely understandable to feel overwhelmed'"
  - "Offer grounding: 'Let's take a moment to breathe' or 'You're safe right now'"
  - "Use collaborative language: 'We'll work through this together'"
  - "Ask 1 gentle question to help articulate feelings"
constraints:
  - "Stay grounded in user's exact words"
  - "No advice-giving yet; focus on validation"
  - "70-150 words"
```

---

### 1.2 Plan & Structure (Security + Arousal)

**User Need:** Time management, task prioritization, workload breakdown  
**Zurich Domains:** Security (control), Arousal (energy/activation)  
**Trigger Patterns:** "I have 3 deadlines...", "I don't know where to start...", "How do I organize all this?"

**Personality Adaptations:**

| Trait | High Expression | Low Expression |
|-------|----------------|----------------|
| **Conscientiousness (C)** | Detailed step-by-step: "1. Monday 9am: Draft outline (2h). 2. Monday 2pm: Review notes (1h)..." + Timelines, milestones | Flexible options: "You could start with whichever task feels most manageable right now." (Avoid rigid schedules) |
| **Openness (O)** | Creative prioritization: "What if we used the Eisenhower Matrix?" or "Let's try time-blocking with themes" | Proven frameworks: "A simple to-do list with A/B/C priorities works well." |
| **Neuroticism (N)** | Built-in buffers: "Let's add 30% extra time for each task to reduce pressure." | Realistic timelines: "This should take about 4 hours total." |
| **Extraversion (E)** | Collaborative framing: "Who could you work alongside for accountability?" | Solo strategies: "Find a quiet space where you can focus uninterrupted." |

**Example Directive (High C, Low O):**
```yaml
mode: plan_structure
directives:
  - "Provide detailed, step-by-step action plan with specific timelines"
  - "Use proven frameworks: to-do lists, A/B/C prioritization, time-blocking"
  - "Include clear milestones: 'By end of Monday, you'll have X completed'"
  - "Organize response with numbered steps or bullet points"
  - "Avoid abstract concepts; stay concrete and actionable"
constraints:
  - "Base plan strictly on user's mentioned tasks and constraints"
  - "Ask 1-2 clarifying questions if timeline/resources unclear"
  - "70-150 words"
```

---

### 1.3 Cope & Rehearse (Security + Arousal)

**User Need:** Immediate stress relief, behavioral rehearsal for challenging situations  
**Zurich Domains:** Security (regulation), Arousal (activation/deactivation)  
**Trigger Patterns:** "I need to calm down now...", "How do I handle this meeting?", "I'm panicking..."

**Personality Adaptations:**

| Trait | High Expression | Low Expression |
|-------|----------------|----------------|
| **Extraversion (E)** | Social coping: "Could you call a friend to talk this through?" or "Practice your response out loud." | Solitary techniques: "Try journaling your thoughts" or "Use box breathing: in-4, hold-4, out-4, hold-4." |
| **Neuroticism (N)** | Grounding exercises: "5-4-3-2-1: Name 5 things you see, 4 you hear..." + Safety anchors: "You've handled difficult situations before." | Challenge reframing: "This is tough, but you have the skills to navigate it." (Less reassurance, more empowerment) |
| **Openness (O)** | Creative visualization: "Imagine the meeting going well. What would that look like?" | Practical rehearsal: "Let's script your opening line: 'I'd like to discuss...'" |
| **Conscientiousness (C)** | Structured practice: "Let's break the conversation into 3 parts: opening, key points, closing." | Flexible approach: "Trust your instincts in the moment; you don't need a rigid script." |

**Example Directive (High N, Low E):**
```yaml
mode: cope_rehearse
directives:
  - "Guide grounding exercise: '5-4-3-2-1 sensory technique' or 'box breathing'"
  - "Provide safety anchor: 'You've successfully managed stress before'"
  - "Offer solitary coping: journaling, breathing, progressive muscle relaxation"
  - "Use calm, steady tone: 'Let's slow down and focus on this moment'"
  - "Normalize physiological response: 'Your body is reacting normally to stress'"
constraints:
  - "No social coping suggestions (avoid 'talk to someone')"
  - "Stay present-focused; avoid future catastrophizing"
  - "70-150 words"
```

---

## 2. Evidence-Based Techniques (Integrated)

### 2.1 Mental Contrasting with Implementation Intentions (MCII)
**When:** Plan & Structure mode  
**How:** "If [obstacle], then I will [specific action]"  
**Example:** "If I feel overwhelmed by the deadline, then I will take a 5-minute break and list just 3 priority tasks."

### 2.2 Cognitive Reappraisal
**When:** Cope & Rehearse mode (especially Low N)  
**How:** Reframe stressor as challenge, not threat  
**Example:** "This presentation is an opportunity to demonstrate your expertise, not a test you can fail."

### 2.3 Grounding Exercises
**When:** Cope & Rehearse mode (especially High N)  
**Techniques:**
- **5-4-3-2-1 Sensory:** Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste
- **Box Breathing:** Inhale 4 counts, hold 4, exhale 4, hold 4 (repeat 4 cycles)
- **Progressive Muscle Relaxation:** Tense and release muscle groups sequentially

### 2.4 Micro-Planning
**When:** Plan & Structure mode (especially High C)  
**How:** 15-minute time blocks, single-task focus  
**Example:** "9:00-9:15: Read first 3 pages of article. 9:15-9:30: Highlight key points. 9:30-9:45: Write 1-sentence summary."

---

## 3. Policy Pack Configuration (YAML)

```yaml
# policy_pack_stress_coach.yaml
version: "1.0.0"
use_case: "stress_self_regulation_micro_coach"
target_population: "adult_learners_msc_students"

coaching_modes:
  - id: "vent_validate"
    zurich_domains: ["affiliation", "security"]
    primary_traits: ["neuroticism", "agreeableness"]
    techniques: ["empathetic_mirroring", "affect_labeling", "normalization"]
    
  - id: "plan_structure"
    zurich_domains: ["security", "arousal"]
    primary_traits: ["conscientiousness", "openness"]
    techniques: ["mcii", "micro_planning", "prioritization_frameworks"]
    
  - id: "cope_rehearse"
    zurich_domains: ["security", "arousal"]
    primary_traits: ["extraversion", "neuroticism"]
    techniques: ["grounding_exercises", "cognitive_reappraisal", "behavioral_rehearsal"]

trait_mappings:
  neuroticism:
    high_threshold: 0.2
    high_directives:
      vent_validate: ["extra_reassurance", "grounding_offers", "normalize_feelings"]
      plan_structure: ["buffer_time", "stress_reduction_focus"]
      cope_rehearse: ["grounding_exercises", "safety_anchors"]
    low_directives:
      vent_validate: ["pragmatic_validation", "move_to_action"]
      plan_structure: ["realistic_timelines"]
      cope_rehearse: ["challenge_reframing", "empowerment_focus"]
  
  conscientiousness:
    high_threshold: 0.2
    high_directives:
      plan_structure: ["detailed_steps", "timelines", "milestones", "numbered_lists"]
      cope_rehearse: ["structured_practice", "scripted_rehearsal"]
    low_directives:
      plan_structure: ["flexible_options", "avoid_rigid_schedules"]
      cope_rehearse: ["trust_instincts", "minimal_structure"]
  
  extraversion:
    high_threshold: 0.2
    high_directives:
      vent_validate: ["social_framing", "collaborative_language"]
      plan_structure: ["accountability_partners", "group_work"]
      cope_rehearse: ["social_coping", "talk_out_loud"]
    low_directives:
      vent_validate: ["reflective_space", "internal_processing"]
      plan_structure: ["solo_strategies", "quiet_focus"]
      cope_rehearse: ["solitary_techniques", "journaling", "breathing"]
  
  agreeableness:
    high_threshold: 0.2
    high_directives:
      vent_validate: ["warm_tone", "empathetic_mirroring", "collaborative_we"]
      plan_structure: ["team_framing"]
    low_directives:
      vent_validate: ["direct_acknowledgment", "matter_of_fact"]
      plan_structure: ["autonomous_planning"]
  
  openness:
    high_threshold: 0.2
    high_directives:
      vent_validate: ["creative_reframing", "alternative_perspectives"]
      plan_structure: ["creative_frameworks", "novel_methods"]
      cope_rehearse: ["visualization", "metaphors"]
    low_directives:
      vent_validate: ["concrete_validation", "stick_to_facts"]
      plan_structure: ["proven_frameworks", "familiar_methods"]
      cope_rehearse: ["practical_rehearsal", "literal_scripts"]

safety_constraints:
  - "no_medical_advice"
  - "no_diagnosis"
  - "no_crisis_intervention"
  - "dialog_grounding_only"
  - "escalation_ready"

response_constraints:
  word_count: [70, 150]
  max_questions: 2
  tone: "supportive_non_clinical"
```

---

## 4. Simulation Scenarios (Detailed)

### Scenario 1: Workload Overload
**Profile:** Type A (High OCEAN: +0.8, +0.8, +0.8, +0.8, -0.8)  
**Expected Modes:** Vent & Validate (turns 1-3) → Plan & Structure (turns 4-8)

**Turn 1 (User):**  
"I have three major deadlines this week—a research paper, a group presentation, and a coding assignment. I'm feeling completely overwhelmed and don't know where to start. Everything feels equally urgent!"

**Expected Detection:** O≈0.7-0.9, C≈0.7-0.9, E≈0.6-0.8, A≈0.6-0.8, N≈-0.6 to -0.8 (emotionally stable despite stress)

**Expected Response (Regulated):**  
Mode: Vent & Validate → Plan & Structure transition  
Directives: Warm validation + Structured planning  
"It's completely understandable to feel overwhelmed with three major deadlines! Let's break this down together. First, can you tell me the exact due dates for each? Once we have that, we can create a detailed step-by-step plan with clear milestones for each day. You've got strong organizational skills—we'll put them to work here."

**Turn 4 (User):**  
"The paper is due Wednesday, presentation Thursday, coding Friday. I've started the paper but the other two I haven't touched yet."

**Expected Response (Regulated):**  
Mode: Plan & Structure (High C, High O)  
"Perfect! Here's a structured plan:  
**Monday (today):** 9am-12pm: Finish paper draft (3h). 2pm-4pm: Outline presentation with group (2h).  
**Tuesday:** 9am-11am: Revise paper (2h). 1pm-5pm: Code assignment—break into modules (4h).  
**Wednesday morning:** Final paper polish (1h), submit. Afternoon: Presentation rehearsal.  
**Thursday:** Present, then finish coding.  
This gives you buffer time. Which task feels most urgent to tackle first?"

---

### Scenario 2: Deadline Anxiety
**Profile:** Type B (Low OCEAN: -0.8, -0.8, -0.8, -0.8, +0.8)  
**Expected Modes:** Cope & Rehearse (turns 1-4) → Plan & Structure (turns 5-8)

**Turn 1 (User):**  
"My thesis defense is in two days and I'm panicking. I can't focus, my mind keeps racing, and I feel like I'm going to fail. I don't know how to calm down."

**Expected Detection:** O≈-0.7 to -0.9, C≈-0.6 to -0.9, E≈-0.7 to -0.9, A≈-0.6 to -0.8, N≈0.7 to 0.9 (high anxiety)

**Expected Response (Regulated):**  
Mode: Cope & Rehearse (High N, Low E)  
Directives: Grounding exercise + Solitary coping + Safety anchor  
"Let's slow down and focus on this moment. Your body is reacting normally to stress. Try this with me: Breathe in for 4 counts, hold for 4, out for 4, hold for 4. Repeat 4 times. [Pause] You've prepared for this defense—you know your material. Right now, let's just get your nervous system calm. Can you find a quiet space where you won't be interrupted?"

**Turn 3 (User):**  
"Okay, the breathing helped a little. I'm in my room now. But I still feel unprepared."

**Expected Response (Regulated):**  
Mode: Cope & Rehearse → Plan & Structure transition (Low C)  
"Good—you're creating a calmer space for yourself. Let's focus on what you *can* control in the next 48 hours. You don't need a rigid plan; just a few flexible priorities. What's the one section of your thesis you feel least confident about? We can spend 30 minutes reviewing just that, then you'll feel more grounded."

---

### Scenario 3: Interpersonal Conflict
**Profile:** Type C (Mixed: +0.6, -0.7, +0.3, +0.8, -0.4)  
**Expected Modes:** Vent & Validate (turns 1-4) → Cope & Rehearse (turns 5-10)

**Turn 1 (User):**  
"I had a really difficult meeting with my supervisor today. She criticized my work in front of the whole team and I felt humiliated. I have to meet with her again tomorrow and I don't know how to handle it without getting emotional."

**Expected Detection:** O≈0.5-0.7, C≈-0.6 to -0.8, E≈0.2-0.4, A≈0.7-0.9, N≈-0.3 to -0.5

**Expected Response (Regulated):**  
Mode: Vent & Validate (High A, Moderate O)  
Directives: Warm empathetic validation + Creative reframing offer  
"That sounds really painful—being criticized publicly can feel humiliating, and it's completely valid to feel upset. You value collaboration and respect, so this hit hard. Let's first acknowledge that your feelings are justified. Then, if you're open to it, we could explore how to approach tomorrow's meeting in a way that protects your emotional space. Does that feel right?"

**Turn 5 (User):**  
"Yes, I need to figure out what to say tomorrow. I don't want to cry or get defensive."

**Expected Response (Regulated):**  
Mode: Cope & Rehearse (High A, Low C, Slight E)  
"Let's prepare in a flexible way—no rigid script, just some anchors. First, a grounding technique: If you feel emotion rising, press your feet firmly into the floor and take one slow breath. For the conversation, you could open with: 'I'd like to understand your feedback better.' Then listen, and respond with: 'I hear you. I'll work on [specific point].' You don't need to defend yourself in the moment. How does that feel?"

---

## 5. Success Metrics (Operationalized)

### 5.1 Technical Reliability
| Metric | Target | Measurement |
|--------|--------|-------------|
| JSON Contract Compliance | ≥ 99.5% | Valid JSON outputs / Total detection+generation calls |
| EMA Stabilization Rate | ≥ 80% sessions within 6-8 turns | Count sessions where `stable=TRUE` by turn 8 |
| Post-Stability Variance | < 0.15 per trait | Std dev of OCEAN values after `stable=TRUE` |
| Graceful Fallback Coverage | 100% | Zero unhandled exceptions in logs |

### 5.2 Effectiveness (vs. Baseline)
| Metric | Target | Measurement |
|--------|--------|-------------|
| Tone Appropriateness | +20% (95% CI) | Mean score: Regulated vs. Baseline (t-test) |
| Relevance & Coherence | +20% (95% CI) | Mean score: Regulated vs. Baseline (t-test) |
| Personality Needs Addressed | +20% (95% CI) | Mean score: Regulated vs. Baseline (t-test) |
| Intent Classification Accuracy | ≥ 85% | Correct mode classification / Total turns |
| Directive-Outcome Alignment | ≥ 80% | Evaluator-assessed: Directives correctly applied |

### 5.3 Reusability
| Metric | Target | Measurement |
|--------|--------|-------------|
| Policy Pack Swap Time | < 30 minutes | Timed test: Stress coach → Customer service config |
| Contract Breaking Changes | 0 during study | Version control: API signature changes |
| Documentation Coverage | 100% | All API endpoints + examples documented |

---

## 6. Implementation Checklist (4-Week Sprint)

### Week 1: Policy Pack & Prompts
- [ ] Finalize `policy_pack_stress_coach.yaml` with all trait mappings
- [ ] Write detection prompt with coaching mode classification
- [ ] Write generation prompts for 3 modes (vent, plan, cope)
- [ ] Draft 9 simulation scenarios (3 profiles × 3 scenarios)
- [ ] Set up PostgreSQL schema with `coaching_mode` column

### Week 2: N8N Workflow & EMA
- [ ] Implement mode classification node (intent detection)
- [ ] Update regulation node with policy pack loader
- [ ] Enable EMA smoothing with α=0.3, confidence filtering ≥0.4
- [ ] Add contract validation (JSON schema checks)
- [ ] Implement graceful fallbacks for all failure modes

### Week 3: Simulation & Baseline
- [ ] Generate 90-135 regulated conversations (10-15 per profile×scenario)
- [ ] Generate parallel baseline conversations (same user messages)
- [ ] Export JSONL logs with mode classifications, directives, OCEAN evolution
- [ ] Validate data completeness (no missing turns, all metadata present)

### Week 4: Evaluation & Analysis
- [ ] Run LLM evaluator (3 independent runs for consistency)
- [ ] Calculate inter-run reliability (Pearson r ≥ 0.85)
- [ ] Perform t-tests on shared criteria (tone, relevance, needs)
- [ ] Generate visualizations (OCEAN evolution, mode distribution, performance comparison)
- [ ] Document findings and update manuscript

---

## 7. Market-Ready Extensions (Post-Preliminary Study)

### Phase 2: Pilot-Ready Features
- **Admin Dashboard:** Cohort analytics, anonymized conversation logs, engagement metrics
- **Escalation Policy:** Crisis language detection → human referral workflow
- **Session Limits:** 10-minute timeout, max 3 sessions/day, cooldown periods
- **Privacy Compliance:** GDPR-compliant data handling, no PII storage, audit trails

### Phase 3: Commercial Deployment
- **SSO Integration:** SAML/OAuth for university/corporate systems
- **LMS Embedding:** Canvas, Moodle, Blackboard plugins
- **Outcome Tracking:** Retention rates, engagement metrics, NPS surveys
- **Multi-Language:** German, French for Swiss market; Spanish for US/LatAm

### Adjacent Use Cases (Policy Pack Reuse)
- **Customer Service Tone Coach:** Real-time personality-adaptive guidance for support agents
- **Manager Micro-Coach:** Onboarding, performance conversations, conflict resolution
- **Educational Tutor:** Adaptive learning assistance with personality-aware pacing

---

## 8. References & Resources

**Evidence Base:**
- Mental Contrasting with Implementation Intentions (MCII): Stadler et al. (2010), *Journal of Personality and Social Psychology*
- Cognitive Reappraisal: Gross & John (2003), *Journal of Personality and Social Psychology*
- Grounding Techniques: Najavits (2002), *Seeking Safety: A Treatment Manual*
- Microinterventions for Stress: Stieger et al. (2021), *PMC8479600*

**Market Data:**
- Corporate Wellness Market: Global Wellness Institute (2024)
- Student Mental Health: American College Health Association (2024)
- AI Coaching Trends: Gartner Digital Markets (2025)

---

**Document Owner:** [Your Name]  
**Last Updated:** 2025-10-13  
**Next Review:** After Week 2 implementation milestone

