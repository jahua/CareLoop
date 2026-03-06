# ✅ Prism Import Checklist

## Pre-Import Preparation

- [ ] Verify you have Prism access at https://prism.openai.com/?d=2
- [ ] Review `QUICK_REFERENCE_GUIDE.md` to understand key references
- [ ] Check `paper_metadata.json` for paper overview

## Step 1: Import References (5 min)

- [ ] Go to https://prism.openai.com/?d=2
- [ ] Click **"Import"** or **"Add References"**
- [ ] Select **"BibTeX"** format
- [ ] Upload `references.bib` (18 KB, 68 references)
- [ ] Wait for Prism to process (should take ~1-2 minutes)
- [ ] Verify all 68 references imported successfully

### Expected Result:
```
✓ 68 references imported
✓ Articles: 45
✓ Books: 11
✓ Conference papers: 9
✓ Technical reports: 3
```

## Step 2: Create Collections (3 min)

Create the following collections and add references:

- [ ] **Core Theory**
  - Add: [4] Roberts, [9] John, [10] Quirin, [40-42] Big Five

- [ ] **Gap Evidence** ⭐ NEW
  - Add: [66] Ahmad, [67] Wanniarachchi, [68] Soni
  - Add: [22-24] Existing systems (ElliQ, Shah)

- [ ] **Implementation**
  - Add: [7] PROMISE, [46] GPT-4
  - Add: [47-50] Prompting methods

- [ ] **Methodology**
  - Add: [31-32] Experimental design
  - Add: [33-37] Reporting standards
  - Add: [60-63] Statistics

- [ ] **Evaluation**
  - Add: [55-56] LLM-as-judge
  - Add: [11, 57-58] Inter-rater reliability
  - Add: [25] FEEL framework

## Step 3: Add Tags (5 min)

Tag references by importance and topic:

### Priority Tags
- [ ] `key-citation` → [4, 7, 9, 10, 66, 67, 68]
- [ ] `new-evidence` → [66, 67, 68]
- [ ] `cited-in-abstract` → None (abstracts don't cite)
- [ ] `cited-in-intro` → [4, 8, 9, 22, 23, 24, 66, 67, 68]

### Topic Tags
- [ ] `personality-theory` → [3, 4, 9, 10, 40-42, 44, 45]
- [ ] `zurich-model` → [10, 26-29]
- [ ] `big-five` → [3, 9, 40-42]
- [ ] `digital-mental-health` → [22-24, 38, 39, 66, 67]
- [ ] `llm` → [5, 8, 15-20, 46-50, 64, 65]
- [ ] `conversational-ai` → [6, 8, 21, 30, 66, 68]
- [ ] `evaluation` → [11, 25, 55-58]
- [ ] `methodology` → [31-37]
- [ ] `statistics` → [43, 54, 57-63]

### Method Tags
- [ ] `simulation-study` → Paper focus
- [ ] `factorial-design` → [31, 32]
- [ ] `llm-as-judge` → [55, 56]

## Step 4: Add Key Notes (10 min)

Add notes to the most important references:

### [66] Ahmad et al. (2022) ⭐
```
Why cited: Evidence that current mental health CAs are "one-size-fits-all"
Key quote: "all three CAs represent a rather 'one-size-fits-all' solution"
Used in: Introduction [line 50]
Supports: Generic communication strategies claim
```

### [67] Wanniarachchi et al. (2025) ⭐
```
Why cited: Evidence of shallow personalization in DMHIs
Key finding: 51% of interventions use only ONE personalization dimension
Used in: Introduction [line 50]
Supports: Shallow personalization claim
```

### [68] Soni et al. (2023) ⭐
```
Why cited: Challenge of personality adaptation in chatbots
Key challenge: Developing chatbots that adapt to user personality
Used in: Introduction [line 50]
Supports: Dynamic adaptation gap
```

### [4] Roberts et al. (2007)
```
Why cited: Importance of personality for life outcomes
Used in: Introduction [line 50], Abstract
Supports: Why personality matters for emotional processing
```

### [10] Quirin et al. (2023)
```
Why cited: Zurich Model - theoretical foundation
Links: Big Five → Security, Arousal, Affiliation
Used in: Throughout paper
Foundation: Entire regulation strategy
```

### [7] Wu et al. (2024)
```
Why cited: PROMISE orchestration framework
Used for: Reproducible LLM control and state management
Implementation: Core system architecture
```

- [ ] Add similar notes for [46] GPT-4, [31-32] Design, [60] Cohen

## Step 5: Link Related Papers (5 min)

Create connections between related references:

- [ ] Link [66] ↔ [67] ↔ [68] (all discuss personalization gaps)
- [ ] Link [4] → [10] (personality theory → Zurich Model)
- [ ] Link [22] ↔ [23] ↔ [24] (existing systems - ElliQ, Shah)
- [ ] Link [55] ↔ [56] (LLM-as-judge methods)
- [ ] Link [31] ↔ [32] (experimental design)
- [ ] Link [9] → [40] → [41] → [42] (Big Five development)

## Step 6: Optional - Import Main Paper (2 min)

- [ ] Upload `V8.2.7_MDPI_APA.tex` to Prism
- [ ] Let Prism extract citations and cross-reference
- [ ] Verify citation links are correct

## Step 7: Verify Import (2 min)

Final checks:

- [ ] All 68 references visible in library
- [ ] 5 collections created
- [ ] Key citations ([4, 7, 10, 66, 67, 68]) tagged
- [ ] Notes added to top 10 references
- [ ] Related papers linked

## Troubleshooting

### If BibTeX import fails:
1. Try importing in smaller batches (20 refs at a time)
2. Check file encoding is UTF-8
3. Contact Prism support with error message

### If special characters display incorrectly:
- Already handled with LaTeX escapes (ö, ü, é, etc.)
- Should display correctly in Prism

### If DOIs don't link:
- DOIs included for refs [66, 67, 68]
- Prism should auto-detect and create links

## 📊 Post-Import Statistics

Once complete, you should have:

```
Total references: 68
Collections: 5
Tags: ~15
Notes: ~10 key references
Links: ~15 connections
Time invested: ~30 minutes
```

## 🎉 Next Steps

After import:
1. Export citation for your paper from Prism
2. Use Prism to search related work
3. Track citation counts over time
4. Share collections with collaborators

---

**Estimated Time:** 30 minutes  
**Difficulty:** Easy  
**Priority:** High (enables better reference management)

**Questions?** See `README.md` or `QUICK_REFERENCE_GUIDE.md`
