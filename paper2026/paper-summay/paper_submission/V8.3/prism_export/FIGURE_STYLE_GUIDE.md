# Figure quality & design guide (for this project)

## 1) Export format (most important)
- **Plots/diagrams:** export as **PDF (vector)** whenever possible.
- If you must use raster: export as **PNG** at **final print size** with **≥300 dpi** (photos) or **≥600 dpi** (line art/text-heavy plots).
  - Rule of thumb: for a 1-column figure (~85 mm wide), aim for **≥2000 px width**; for 2-column (~170 mm), **≥4000 px width**.

## 2) Typography (consistency)
- Use **one font family** across all figures (preferably matching the paper).
- Minimum readable size at final placement: **8–9 pt** for axis labels; **9–10 pt** for legends.
- Avoid thin fonts; use regular/medium weights.

## 3) Lines, markers, and contrast
- Line width: **1.0–1.5 pt**; axes slightly heavier than gridlines.
- Marker size large enough for print; avoid tiny markers.
- Prefer **direct labels** or compact legends; remove redundant legend titles.

## 4) Color and accessibility
- Use a **colorblind-safe palette**; do not rely on red/green alone.
- Ensure strong contrast (especially for grayscale printing): pair color with **line style** (solid/dashed) or **marker shape**.

## 5) Layout & whitespace
- Crop tightly (no large margins); avoid “floating” plots inside big white canvases.
- Align multi-panel figures to a clean grid; keep panel spacing consistent.
- Keep y-axis limits consistent across comparable panels where interpretation depends on scale.

## 6) File naming & foldering (current convention)
- Method/design diagrams: `figures/mdpi/*.png` (consider switching these to `.pdf` if you re-export).
- Results figures: `figures/*.png` (high-res or vector preferred).

## 7) Quick triage (figures most likely to look soft)
Based on current sizes, check these first for resolution issues at final placement:
- `figures/07_personality_heatmap.png` (very small file size)
- `figures/08_weighted_scores.png`, `figures/09_total_score_boxplot.png`, `figures/10_selective_enhancement_paired.png`, `figures/11_metric_composition.png`

If you tell me which specific figures look blurry in the PDF, I can also adjust the LaTeX `\includegraphics` sizing so we don’t unintentionally upscale rasters.