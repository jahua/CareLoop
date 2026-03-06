# Quick Start Guide: Stress Micro-Coach Implementation
**For:** Immediate action after supervisor approval  
**Timeline:** 4 weeks to validated preliminary study  
**Goal:** Reusable, reliable, personality-adaptive chatbot architecture

---

## 🎯 **What You're Building**

```
┌─────────────────────────────────────────────────────────────┐
│  STRESS SELF-REGULATION MICRO-COACH FOR ADULT LEARNERS     │
│  Real-time personality adaptation via OCEAN + Zurich Model  │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │   Three Coaching Modes (Intent-Based)   │
        └─────────────────────────────────────────┘
                 ↓              ↓              ↓
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │   VENT &   │  │   PLAN &   │  │   COPE &   │
        │  VALIDATE  │  │  STRUCTURE │  │  REHEARSE  │
        └────────────┘  └────────────┘  └────────────┘
        Affiliation+    Security+       Security+
        Security        Arousal         Arousal
             ↓               ↓               ↓
        ┌────────────────────────────────────────────┐
        │  Personality Adaptations (OCEAN Traits)    │
        │  • High N: Extra reassurance + grounding   │
        │  • High C: Detailed plans + timelines      │
        │  • High E: Social coping strategies        │
        │  • High A: Warm, collaborative tone        │
        │  • High O: Creative frameworks             │
        └────────────────────────────────────────────┘
```

---

## 📋 **Week-by-Week Checklist**

### **WEEK 1: Policy Pack & Prompts** (Foundation)
**Goal:** Complete configuration and prompt engineering

#### Day 1-2: Policy Pack Configuration
```bash
# Create policy pack file
touch preliminary-studies/w9-Technical-Specifications/MVP/config/policy_pack_stress_coach.yaml
```

**Contents to define:**
- [ ] Three coaching modes (vent_validate, plan_structure, cope_rehearse)
- [ ] Trait mappings for each mode (N, C, E, A, O)
- [ ] Directive templates with intensity scaling
- [ ] Safety constraints (no medical advice, dialog grounding)
- [ ] Response constraints (70-150 words, max 2 questions)

**Template:** See `STRESS_MICROCOACH_IMPLEMENTATION_GUIDE.md` Section 3

#### Day 3-4: Prompt Engineering
**Three prompts to write:**

1. **Detection Prompt** (with mode classification)
```
Input: User message + conversation history
Output: {
  "ocean": {"O": float, "C": float, "E": float, "A": float, "N": float},
  "confidence": {"O": float, "C": float, "E": float, "A": float, "N": float},
  "coaching_mode": "vent_validate" | "plan_structure" | "cope_rehearse",
  "reasoning": "Brief motivational analysis"
}
```

2. **Generation Prompts** (one per mode)
- Vent & Validate: Empathetic validation + affect labeling
- Plan & Structure: Structured planning + prioritization
- Cope & Rehearse: Evidence-based coping techniques

3. **Evaluation Prompt** (for automated scoring)
- 7 criteria for regulated; 3 for baseline
- Trinary scoring (Yes=2, Partial=1, No=0)

**Location:** `preliminary-studies/w9-Technical-Specifications/MVP/prompts/`

#### Day 5: Simulation Scenario Scripts
**Create 9 scenarios (3 profiles × 3 stress contexts):**

| Profile | Workload Overload | Deadline Anxiety | Interpersonal Conflict |
|---------|-------------------|------------------|------------------------|
| Type A (High OCEAN) | 8-turn script | 8-turn script | 10-turn script |
| Type B (Low OCEAN) | 8-turn script | 8-turn script | 10-turn script |
| Type C (Mixed) | 8-turn script | 8-turn script | 10-turn script |

**Template:** See `STRESS_MICROCOACH_IMPLEMENTATION_GUIDE.md` Section 4

**Location:** `preliminary-studies/w9-Technical-Specifications/MVP/simulations/`

---

### **WEEK 2: N8N Workflow & EMA** (Implementation)
**Goal:** Functional detect→regulate→generate pipeline with EMA

#### Day 1-2: Mode Classification Node
**New N8N node:** "Coaching Mode Classifier"
- Input: User message + conversation history
- Output: Intent classification (vent, plan, cope) + confidence
- Logic: Keyword matching + LLM classification
- Fallback: Default to "vent_validate" if unclear

#### Day 3: Policy Pack Loader
**Update "Enhanced Regulation" node:**
```javascript
// Load policy pack
const policyPack = require('./policy_pack_stress_coach.yaml');

// Get coaching mode from previous node
const mode = $input.item.json.coaching_mode;

// Get OCEAN traits
const ocean = $input.item.json.ocean;

// Map traits to directives for this mode
const directives = [];
for (const trait in ocean) {
  const value = ocean[trait];
  const confidence = $input.item.json.confidence[trait];
  
  if (Math.abs(value) >= 0.2 && confidence >= 0.4) {
    const directiveKey = value > 0 ? 'high_directives' : 'low_directives';
    const modeDirectives = policyPack.trait_mappings[trait][directiveKey][mode];
    directives.push(...modeDirectives);
  }
}

return { directives, mode, ocean };
```

#### Day 4: EMA Smoothing Enhancement
**Update "Zurich Model Detection" node:**
- Retrieve previous state from PostgreSQL
- Apply EMA: `smoothed = 0.3 * current + 0.7 * previous`
- Filter low-confidence updates (< 0.4)
- Calculate stability flag (variance < 0.15 after 6 turns)

#### Day 5: Contract Validation & Fallbacks
**Add validation nodes:**
- JSON schema validation for detection output
- Response length check (70-150 words)
- Question count check (≤ 2)
- Graceful fallback: "I'm here to support you. Could you tell me more?"

**Test:** Run 3 test conversations; verify all contracts pass

---

### **WEEK 3: Simulation & Baseline** (Data Generation)
**Goal:** 90-135 regulated conversations + parallel baseline

#### Day 1-2: Regulated Conversations
**Run simulations:**
```bash
# For each profile (A, B, C) and scenario (workload, deadline, interpersonal)
for profile in A B C; do
  for scenario in workload deadline interpersonal; do
    for session in {1..12}; do
      curl -X POST http://localhost:5678/webhook/zurich \
        -H "Content-Type: application/json" \
        -d @simulations/profile_${profile}_${scenario}_session_${session}.json
    done
  done
done
```

**Expected output:** 108 conversations (3×3×12)

#### Day 3: Baseline Conversations
**Modify workflow:**
- Disable personality detection node
- Use generic empathetic prompt (no directives)
- Keep same user messages as regulated condition

**Run:** Same 108 conversations with baseline bot

#### Day 4-5: Data Export & Validation
**PostgreSQL queries:**
```sql
-- Export regulated conversations
COPY (
  SELECT s.session_id, t.turn_index, t.user_message, t.assistant_response,
         ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
         ps.confidence_o, ps.confidence_c, ps.confidence_e, ps.confidence_a, ps.confidence_n,
         ps.stable, t.directives_applied, t.coaching_mode
  FROM chat_sessions s
  JOIN conversation_turns t ON s.session_id = t.session_id
  JOIN personality_states ps ON s.session_id = ps.session_id AND t.turn_index = ps.turn_index
  WHERE s.evaluation_mode = 'regulated'
  ORDER BY s.session_id, t.turn_index
) TO '/tmp/regulated_conversations.csv' CSV HEADER;

-- Export baseline conversations
COPY (
  SELECT s.session_id, t.turn_index, t.user_message, t.assistant_response
  FROM chat_sessions s
  JOIN conversation_turns t ON s.session_id = t.session_id
  WHERE s.evaluation_mode = 'baseline'
  ORDER BY s.session_id, t.turn_index
) TO '/tmp/baseline_conversations.csv' CSV HEADER;
```

**Validation checks:**
- [ ] All 108 regulated sessions have complete OCEAN evolution
- [ ] All 108 baseline sessions have matching user messages
- [ ] No missing turns or null values
- [ ] Coaching mode distribution: ~40% vent, 35% plan, 25% cope

---

### **WEEK 4: Evaluation & Analysis** (Results)
**Goal:** Statistical validation of +20% improvement

#### Day 1-2: LLM Evaluator Runs
**Run 3 independent evaluations:**
```bash
# Run 1
python evaluation.py --input regulated_conversations.csv --output eval_run1_regulated.csv --seed 42

python evaluation.py --input baseline_conversations.csv --output eval_run1_baseline.csv --seed 42

# Run 2 (different seed)
python evaluation.py --input regulated_conversations.csv --output eval_run2_regulated.csv --seed 123

python evaluation.py --input baseline_conversations.csv --output eval_run2_baseline.csv --seed 123

# Run 3 (different seed)
python evaluation.py --input regulated_conversations.csv --output eval_run3_regulated.csv --seed 456

python evaluation.py --input baseline_conversations.csv --output eval_run3_baseline.csv --seed 456
```

**Evaluator criteria:**
- Regulated: 7 criteria (detection accuracy, EMA convergence, confidence calibration, regulation effectiveness, tone, relevance, needs)
- Baseline: 3 criteria (tone, relevance, needs)

#### Day 3: Statistical Analysis
**Python script:**
```python
import pandas as pd
from scipy import stats

# Load evaluation results
reg = pd.read_csv('eval_run1_regulated.csv')
base = pd.read_csv('eval_run1_baseline.csv')

# Shared criteria
shared = ['Emotional_Tone', 'Relevance_Coherence', 'Personality_Needs']

for criterion in shared:
    reg_scores = reg[criterion]
    base_scores = base[criterion]
    
    # T-test
    t_stat, p_value = stats.ttest_ind(reg_scores, base_scores)
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt(((len(reg_scores)-1)*reg_scores.var() + 
                          (len(base_scores)-1)*base_scores.var()) / 
                         (len(reg_scores)+len(base_scores)-2))
    cohens_d = (reg_scores.mean() - base_scores.mean()) / pooled_std
    
    # Relative improvement
    improvement = (reg_scores.mean() - base_scores.mean()) / base_scores.mean() * 100
    
    print(f"{criterion}:")
    print(f"  Regulated: {reg_scores.mean():.2f} ± {reg_scores.std():.2f}")
    print(f"  Baseline: {base_scores.mean():.2f} ± {base_scores.std():.2f}")
    print(f"  Improvement: {improvement:.1f}%")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Cohen's d: {cohens_d:.2f}")
    print(f"  Significant: {p_value < 0.05}\n")

# Inter-run consistency
run1 = pd.read_csv('eval_run1_regulated.csv')
run2 = pd.read_csv('eval_run2_regulated.csv')
consistency = run1[shared].corrwith(run2[shared])
print(f"Inter-run consistency (Pearson r): {consistency.mean():.3f}")
```

**Success thresholds:**
- [ ] Improvement ≥ 20% on all shared criteria
- [ ] p-value < 0.05 for all comparisons
- [ ] Inter-run consistency ≥ 0.85

#### Day 4: Visualizations
**Create 4 charts:**

1. **OCEAN Evolution (Time Series)**
```python
import matplotlib.pyplot as plt

# Select one session
session = reg[reg['session_id'] == 'type_a_workload_session_1']

fig, axes = plt.subplots(5, 1, figsize=(10, 12))
traits = ['O', 'C', 'E', 'A', 'N']

for i, trait in enumerate(traits):
    axes[i].plot(session['turn_index'], session[f'ocean_{trait.lower()}'], 
                 marker='o', label='EMA-smoothed')
    axes[i].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    axes[i].set_ylabel(trait)
    axes[i].set_ylim(-1, 1)
    axes[i].legend()
    
axes[-1].set_xlabel('Turn Index')
plt.suptitle('OCEAN Trait Evolution with EMA Smoothing (Type A, Workload)')
plt.tight_layout()
plt.savefig('ocean_evolution.png', dpi=300)
```

2. **Performance Comparison (Bar Chart)**
```python
# Mean scores by condition
comparison = pd.DataFrame({
    'Regulated': [reg[c].mean() for c in shared],
    'Baseline': [base[c].mean() for c in shared]
}, index=shared)

comparison.plot(kind='bar', figsize=(10, 6), color=['skyblue', 'lightcoral'])
plt.ylabel('Mean Score (0-2)')
plt.title('Performance Comparison: Regulated vs. Baseline')
plt.xticks(rotation=45)
plt.legend(title='Condition')
plt.tight_layout()
plt.savefig('performance_comparison.png', dpi=300)
```

3. **Coaching Mode Distribution (Pie Chart)**
4. **EMA Convergence Curves (Line Chart)**

#### Day 5: Manuscript Update & Documentation
**Update `Preliminary-Study-V2.1.md`:**
- [ ] Add Results section with statistical findings
- [ ] Insert visualizations (Figures 2-5)
- [ ] Write Discussion interpreting findings
- [ ] Document limitations and future work
- [ ] Finalize References

**Create reproducibility package:**
- [ ] Export all prompts with version hashes
- [ ] Archive model versions and API endpoints
- [ ] Package simulation scripts and data
- [ ] Write `REPLICATION_GUIDE.md`

---

## ✅ **Success Checklist (End of Week 4)**

### **Technical Deliverables**
- [ ] N8N workflow JSON with all nodes implemented
- [ ] Policy pack YAML with complete trait mappings
- [ ] Detection, generation, and evaluation prompts (versioned)
- [ ] 9 simulation scenarios (3 profiles × 3 contexts)
- [ ] PostgreSQL database with 216 conversations (108 regulated + 108 baseline)
- [ ] Evaluation results (3 runs × 2 conditions)

### **Analysis Deliverables**
- [ ] Statistical analysis showing ≥ 20% improvement (p < 0.05)
- [ ] Inter-run consistency ≥ 0.85
- [ ] 4 publication-quality visualizations
- [ ] Results and Discussion sections written

### **Reproducibility Deliverables**
- [ ] Complete JSONL logs for all conversations
- [ ] Configuration snapshots (seeds, versions, parameters)
- [ ] Replication guide with step-by-step instructions
- [ ] Automated testing suite (contract validation, EMA convergence)

### **Documentation Deliverables**
- [ ] Updated manuscript (Preliminary-Study-V2.1.md)
- [ ] Implementation guide (STRESS_MICROCOACH_IMPLEMENTATION_GUIDE.md)
- [ ] One-pager for stakeholders (STRESS_MICROCOACH_ONE_PAGER.md)
- [ ] Confirmation summary (USE_CASE_CONFIRMATION_SUMMARY.md)

---

## 🚨 **Common Pitfalls & Solutions**

| Pitfall | Solution |
|---------|----------|
| **LLM API rate limits** | Add exponential backoff; spread simulations over 2 days |
| **Inconsistent JSON outputs** | Add retry logic with schema validation; use temperature 0.1 for detection |
| **EMA not converging** | Check α parameter (0.3 is optimal); verify confidence filtering (≥0.4) |
| **Low evaluator consistency** | Fix evaluation prompt; use same seed; check for order effects |
| **Baseline too strong** | Ensure baseline has NO personality detection; use truly generic prompt |
| **Simulation scripts unrealistic** | Validate with psychology expert; add natural variability (±0.15) |

---

## 📞 **Support Resources**

### **Technical Issues**
- N8N workflow debugging: `preliminary-studies/w9-Technical-Specifications/MVP/Phase-1/docs/WORKFLOW_DETAILED_EXPLANATION.md`
- PostgreSQL schema: `MVP/Docs/DATABASE_DESIGN_AND_DATAFLOW.md`
- EMA implementation: `MVP/Docs/EMA_IMPLEMENTATION_DETAILED.md`

### **Conceptual Questions**
- Zurich Model application: `MVP/Docs/ZURICH_MODEL_APPLICATION.md`
- Continuous vs. discrete values: `MVP/Docs/CONTINUOUS_VS_DISCRETE_PERSONALITY_VALUES.md`
- Confidence calculation: `MVP/Docs/CONFIDENCE_CALCULATION_EXPLAINED.md`

### **Supervisor Meetings**
- **Week 1 checkpoint:** Policy pack review; prompt validation
- **Week 2 checkpoint:** Workflow demo; EMA verification
- **Week 3 checkpoint:** Data quality check; preliminary stats
- **Week 4 checkpoint:** Results review; manuscript feedback

---

## 🎉 **What Success Looks Like**

**End of Week 4, you will have:**
1. ✅ A working personality-adaptive stress micro-coach
2. ✅ Statistical proof of ≥ 20% improvement over baseline
3. ✅ Reusable architecture (Personality Adapter + policy packs)
4. ✅ Complete preliminary study manuscript
5. ✅ Pilot-ready package for thesis phase
6. ✅ Clear pathway to commercialization

**This is not just a research project—it's a market-ready product with academic rigor.**

---

**Ready to start? Begin with Week 1, Day 1: Create `policy_pack_stress_coach.yaml`**

Good luck! 🚀

