# MDPI System Architecture Diagram - Complete Guide

## Overview

This document describes the MDPI-ready system architecture diagram created specifically for journal submission. The diagram precisely matches the manuscript description with proper PROMISE orchestration, interaction storage, and regulation flow.

## Files Generated

| File | Format | Size | Purpose |
|------|--------|------|---------|
| `system_architecture_mdpi.pdf` | Vector PDF | 42 KB | **Primary submission format** - scalable, publication-ready |
| `system_architecture_mdpi.png` | Raster PNG | 741 KB | High-resolution (600 DPI) for review/preview |

**Recommendation**: Submit the PDF version for final publication, use PNG for manuscript review.

## Key Features

### 1. **MDPI-Compliant Visual Style**
- [x] DejaVu Sans font (standard MDPI typeface)
- [x] Title: 14pt bold
- [x] Box text: 9-10pt
- [x] Rounded rectangles with pastel fills
- [x] Darker outlines for clarity
- [x] Grayscale-safe colors (legible when printed in B&W)
- [x] Consistent line widths
- [x] 600 DPI resolution for PNG
- [x] Tight bounding boxes with proper margins

### 2. **Content Matches Manuscript Exactly**

#### PROMISE Orchestration Band
- Horizontal band spanning the diagram
- Label: "PROMISE orchestration (state transitions, prompt composition, interaction storage)"
- Positioned between input and processing layers
- Shows system-wide coordination

#### Five Processing Layers
1. **INPUT**: User message + context, Dialogue history
2. **DETECTION**: Trait-state inference -> Inferred trait state P-hat (O,C,E,A,N) + confidence
3. **REGULATION**: Zurich Model mapping -> trait-aligned prompt augmentation
4. **GENERATION**: Prompt assembly -> LLM response generation (GPT-4 instance) -> Assistant response
   - Shows regulated condition: base + regulation
   - Shows baseline condition: base only
5. **EVALUATION**: Evaluator GPT (LLM-as-judge) + Human expert audit (qualitative; single expert) + Analysis & statistics (effect sizes, tests)

#### Interaction Storage
- Right-side box storing:
  - P-hat (trait state)
  - Confidence scores
  - Logs
  - Turn IDs
- Connected to detection, regulation, and evaluation layers

### 3. **Arrow Types (Semantic Distinctions)**

The diagram uses three arrow styles to distinguish different information flows:

| Style | Purpose | Examples |
|-------|---------|----------|
| **Solid (-)** | Data flow | User input -> Detection, P-hat -> Storage |
| **Dashed (--)** | Control flow / Prompt injection | Regulation -> Prompt assembly, PROMISE coordination |
| **Dotted (:)** | Logging | Evaluation metrics -> Storage |

**Legend included** at bottom of diagram for clarity.

### 4. **Critical Design Decisions**

#### Regulation as Prompt Augmentation (NOT LLM Modification)
The diagram explicitly shows:
- Regulation produces "trait-aligned regulation prompts"
- These prompts are **injected** into prompt assembly (dashed arrow)
- LLM itself remains unmodified
- This matches manuscript description: "trait-aligned prompt augmentation"

**Why this matters**: Reviewers need to see that regulation happens through prompt engineering, not model fine-tuning or modification.

#### Single LLM Block with Condition Switch
- One "LLM generation (GPT-4)" box
- Annotation below shows two conditions:
  - Regulated: base + regulation
  - Baseline: base only
- Avoids confusion about whether different LLMs are used

#### Explicit Interface to Storage
- Solid arrows: P-hat and detection outputs stored
- Dotted arrows: Evaluation metrics logged
- Shows that all intermediate states are persisted for traceability

## Architecture Description (For Manuscript)

### Suggested Figure Caption:

> **Figure X.** System architecture integrating personality detection (D-module), theory-driven regulation (R-module), and evaluation (E-module) within the PROMISE orchestration framework. The pipeline processes user inputs through five layers: (1) INPUT captures user messages and dialogue history, (2) DETECTION infers Big Five traits via parallel detectors, outputting personality vector P-hat with confidence scores, (3) REGULATION maps traits to Zurich Model motivational domains and generates trait-aligned prompt augmentation, (4) GENERATION assembles prompts (regulated condition: base + regulation; baseline: base only) for GPT-4 response generation, and (5) EVALUATION assesses outputs via LLM-based evaluation, human expert audit, and statistical analysis. Interaction storage persists personality states, confidence, and evaluation metrics across turns. Arrow styles indicate data flow (solid), control flow/prompt injection (dashed), and logging (dotted). All processing is orchestrated by PROMISE state machines and interaction storage.

### Key Terms for Text

When referencing the diagram in manuscript text, use these exact terms:
- "PROMISE orchestration framework"
- "P-hat (personality vector)"
- "trait-aligned prompt augmentation"
- "interaction storage"
- "parallel Big Five trait detectors"
- "Zurich Model mapping"
- "LLM-as-judge evaluation"

## Technical Implementation

### Color Scheme (Grayscale-Safe)

Each layer uses distinct but muted colors that remain distinguishable in grayscale:

```python
colors = {
    'input':      ('#E8F4F8', '#2C5F7E'),  # Light blue
    'detection':  ('#E8F8E8', '#2D6B2D'),  # Light green
    'regulation': ('#FFF4E6', '#8B6914'),  # Light amber
    'generation': ('#F0E8F8', '#5E3A7E'),  # Light purple
    'evaluation': ('#FFE8E8', '#8B3A3A'),  # Light rose
    'storage':    ('#F8F8F8', '#5A5A5A'),  # Light gray
    'promise':    ('#E0E0E0', '#404040')   # Gray
}
```

First color = fill, second color = edge/text

### Layout Coordinates

The diagram uses a 12x10 coordinate system with explicit positioning:
- Layer 1 (INPUT): y = 8.2
- PROMISE band: y = 7.4
- Layer 2 (DETECTION): y = 6.8
- Layer 3 (REGULATION): y = 5.4
- Layer 4 (GENERATION): y = 4.0
- Layer 5 (EVALUATION): y = 2.3
- Storage (right): x = 10.5, y = 5.5-8.0
- Legend: y = 0.8

### Regeneration

To regenerate the diagram:
```bash
cd figures/src
python create_mdpi_architecture.py
```

Output files will be created in `figures/` directory.

To regenerate all figures including MDPI architecture:
```bash
cd figures/src
python generate_all.py
```

## Comparison with Other Architecture Figures

| Figure | Style | Best For | Format |
|--------|-------|----------|--------|
| `10_system_overview.png` | Simple 4-box flow | Presentations, quick overview | PNG |
| `14_detection_pipeline_layered.png` | Detailed 3-layer detection | Technical deep-dive | PNG |
| **`system_architecture_mdpi.pdf`** | **Complete 5-layer system** | **Journal submission** | **PDF + PNG** |

The MDPI version is the most comprehensive, showing:
- [x] All 5 processing layers
- [x] PROMISE orchestration explicitly
- [x] Interaction storage with details
- [x] Three arrow types for semantic clarity
- [x] Condition switching (regulated vs baseline)
- [x] Human + AI evaluation components

## Compliance Checklist

Before submission, verify:
- [ ] PDF file opens correctly in Adobe Reader
- [ ] All text is readable at 100% zoom
- [ ] Colors are distinguishable in grayscale (print test)
- [ ] No overlapping text or arrows
- [ ] Legend is present and clear
- [ ] Tight bounding box (no excessive whitespace)
- [ ] File size < 5 MB (currently 42 KB PDF, well under limit)
- [ ] Resolution is 600 DPI for raster version
- [ ] Font is DejaVu Sans (standard sans-serif)

## Known Limitations & Future Improvements

### Current Implementation
- Single-page diagram (all layers visible simultaneously)
- Fixed aspect ratio optimized for A4/Letter page
- Minimal text per box (<=6 words per requirement)

### Potential Enhancements (If Requested by Reviewers)
- Add numbers to each processing step (1, 2, 3...)
- Include timing information (e.g., "2.3+/-0.8s per turn")
- Add color-coded boxes for different module types
- Include example trait values in P-hat output

**Current version is submission-ready as-is.**

## Citation in Manuscript

When citing this figure in your manuscript:

### In-text reference:
> "The complete system architecture (Figure X) integrates detection, regulation, and evaluation within the PROMISE orchestration framework..."

### Figure placement:
Place after Section 3.2 (System Architecture) in the manuscript.

### Cross-references:
- Detection layer: See Section 3.3.1, Figure 14 (detection pipeline)
- Regulation layer: See Section 3.3.2, Figures 15-16 (regulation & mapping)
- Evaluation layer: See Section 3.5, Figure 12 (evaluation framework)

## Support

For questions or modifications:
1. Review the source code: `figures/src/create_mdpi_architecture.py`
2. Modify helper functions: `draw_box()`, `draw_arrow()`, `draw_layer_label()`
3. Adjust colors in the `colors` dictionary
4. Change coordinates for repositioning elements
5. Regenerate using `python create_mdpi_architecture.py`

All code is well-commented with clear variable names for easy modification.
