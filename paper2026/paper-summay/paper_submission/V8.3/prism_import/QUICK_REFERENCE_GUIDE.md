# Quick Reference Guide

## 🎯 Most Important References

### Core Theory
1. **[4] Roberts et al. (2007)** - Power of Personality
   - Why personality matters for life outcomes
   - Cited for: "personality differences shape emotional processing"

2. **[10] Quirin et al. (2023)** - Zurich Model of Motivation
   - Links Big Five to Security, Arousal, Affiliation domains
   - Foundation for behavioral regulation strategy

3. **[9] John et al. (2008)** - Big Five Trait Taxonomy
   - Big Five framework and measurement
   - Cited for: OCEAN trait framework

### Digital Mental Health - NEWLY ADDED ⭐

4. **[66] Ahmad et al. (2022)** - Personality-Adaptive CAs for Mental Health
   - **KEY QUOTE:** "one-size-fits-all solution, by not adequately adapting to the specificities of their users"
   - **WHY CITED:** Evidence that current systems use generic strategies

5. **[67] Wanniarachchi et al. (2025)** - Personalization in DMHIs
   - **KEY FINDING:** 51% of interventions use only ONE personalization dimension
   - **WHY CITED:** Evidence of shallow personalization in current systems

6. **[68] Soni et al. (2023)** - Personality-Adaptive Chatbots Review
   - **KEY CHALLENGE:** "Developing chatbots capable of generating human-like replies that adapt to users' personalities"
   - **WHY CITED:** Confirms lack of dynamic personality adaptation

### Implementation Framework
7. **[7] Wu et al. (2024)** - PROMISE Framework
   - Orchestration system for reproducible LLM control
   - State machine approach for conversation management

8. **[46] OpenAI (2023)** - GPT-4 Technical Report
   - Model used for all agents in the study
   - Capabilities and architecture

### Existing Systems
9. **[22] Broadbent et al. (2024)** - ElliQ Robot
10. **[23-24] Shah et al. (2019, 2021)** - Digital Interventions for Loneliness
    - Evidence of generic/fixed strategies in deployed systems

---

## 📊 By Research Question

### RQ1: Can personality be detected from conversational cues?
- [3, 9] Big Five framework
- [6] Linguistic style and personality
- [40-42] Personality stability and structure
- [44-45] Personality judgment accuracy

### RQ2: Does personality-adaptive regulation improve outcomes?
- [4] Why personality matters
- [10, 26-29] Zurich Model foundation
- [66-68] Evidence of generic approaches (gap)
- [51] Clinical safety priorities

### RQ3: How should we evaluate AI-generated responses?
- [55-56] LLM-as-judge approaches
- [11, 57-58] Inter-rater reliability
- [25] Emotional support evaluation frameworks

---

## 🔬 By Methodology

### Experimental Design
- [31] Montgomery - Factorial designs
- [32] Collins et al. - Multiple independent variables
- [33] Carroll et al. - Implementation fidelity

### Statistical Analysis
- [60] Cohen - Effect sizes (d = 4.651 interpretation)
- [34] Faul et al. - Power analysis
- [59] Little & Rubin - Missing data
- [61] Efron & Tibshirani - Bootstrap methods

### Reporting Standards
- [35] CONSORT 2010 - RCT reporting
- [36] SPIRIT 2013 - Protocol standards
- [37] Helsinki Declaration - Ethics

---

## 💻 By Technology

### Large Language Models
- [46] GPT-4 Technical Report
- [47] Brown et al. - Few-shot learning
- [65] Ouyang et al. - RLHF
- [48-50] Prompt engineering

### Conversational AI Systems
- [8] Bickmore & Picard - Long-term relationships
- [15-20] Recent LLM-based emotional support systems
- [21] Companion chatbots user experiences

### Evaluation Tools
- [55] MT-Bench and Chatbot Arena
- [56] LLM-as-judge validation
- [25] FEEL framework

---

## 📝 Citation Usage in Paper

### Abstract
- NO citations (standard practice)
- Softened language: "Many... rely on... do not yet incorporate..."

### Introduction
- **[22-24, 66, 67]** - Generic/one-size-fits-all strategies
- **[4]** - Personality shapes emotional processing
- **[66, 68]** - Seldom incorporated or dynamically adapted

### Methods
- **[7]** - PROMISE orchestration
- **[31-32]** - Factorial design
- **[46]** - GPT-4 model

### Results
- **[60]** - Cohen's d interpretation
- **[55-56]** - LLM evaluation approach

### Discussion
- **[66-68]** - Comparison with field limitations
- **[4, 10]** - Theory grounding

---

## 🚀 Import Strategy for Prism

1. **Import references.bib first**
2. **Create these collections:**
   - Core Theory (refs 4, 9, 10)
   - New Evidence (refs 66, 67, 68) ⭐
   - Implementation (refs 7, 46)
   - Methodology (refs 31-37, 60)

3. **Add tags:**
   - `key-citation` for 4, 7, 10, 66, 67, 68
   - `theory` for personality psychology refs
   - `gap-evidence` for 66, 67, 68
   - `methods` for statistics/design refs

4. **Link related papers:**
   - Connect 66→67→68 (all discuss personalization gaps)
   - Connect 4→10 (personality theory chain)
   - Connect 22→23→24 (existing systems)

---

**Last Updated:** February 1, 2026
