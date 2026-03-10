# Big5Loop — Manuscript Visualizations

This folder contains a single Jupyter notebook that generates **all figures** for the thesis manuscript (*manuscript_v2.md*) in **MDPI-compliant** style.

## Notebook

- **`manuscript_figures.ipynb`** — Generates:
  - **Figure 1:** System architecture (Client → API Pre → N8N 9-stage pipeline → PostgreSQL/NVIDIA → API Post → Output)
  - **Figure 2:** EMA trait convergence (Neuroticism: raw vs smoothed)
  - **Figure 3:** Trait stabilization trajectories (representative profiles)
  - **Figure 4:** Coaching quality comparison (adaptive vs baselines)
  - **Eval figures:** PERSONAGE detected vs ground truth; BIG5-CHAT agreement by trait (when evaluation data is present)

## How to run

1. From this directory:
   ```bash
   cd Big5Loop/visualization
   jupyter notebook manuscript_figures.ipynb
   ```
   Or run all cells in VS Code / Cursor.

2. Figures are written to **`Big5Loop/visualization/figures/`**.

## MDPI standards (applied in the notebook)

- **Resolution:** 300 DPI (and figure widths ≥1000 px where needed)
- **Clarity:** Readable when reduced to ~11 × 9 cm
- **Captions:** Kept in the manuscript; no caption text inside the image files
- **Fonts:** Sans-serif (Arial/Helvetica/DejaVu Sans), 8–10 pt

## Dependencies

- `matplotlib`, `numpy`
- `Graphviz` (`dot`) for Figure 1 layout and SVG export
- Optional: `pandas` if you use evaluation-data cells with CSV export

Evaluation data is loaded from `Big5Loop/evaluation_data/` when available (PERSONAGE and BIG5-CHAT results).

Figure 1 is now sourced from `figure1_architecture.dot` and exported to both PNG and SVG. The SVG can be opened in Illustrator for final manual touch-ups if needed.

### Optional figure caption (Figure 1)

*Figure 1. Big5Loop system architecture. Client requests pass through an API pre-processing layer that performs routing and retrieval gating before invoking an N8N workflow implementing the nine-stage coaching pipeline. The workflow integrates personality detection, regulation, retrieval-augmented generation, and grounding verification. Persistent state and policy evidence are stored in PostgreSQL with pgvector, while response generation uses the Gemma-3 large language model via the NVIDIA API. Post-processing applies citation overlay, grounding checks, and audit logging before returning the response to the client.*
