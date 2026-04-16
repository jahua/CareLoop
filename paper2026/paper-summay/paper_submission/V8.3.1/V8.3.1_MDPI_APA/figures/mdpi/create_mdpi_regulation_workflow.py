#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Regulation & Prompt Assembly Workflow
Uses unified DiagramStyle from visualization_config.
"""

import sys
from pathlib import Path

_STAT_DIR = str(Path(__file__).resolve().parent.parent.parent / "statistical analyis")
if _STAT_DIR not in sys.path:
    sys.path.insert(0, _STAT_DIR)

from visualization_config import (
    DIAGRAM_STYLE as DS,
    diagram_setup_figure,
    diagram_draw_box,
    diagram_draw_arrow,
    diagram_draw_title,
    diagram_title_y,
    diagram_content_top_y,
)

OUT = Path(__file__).resolve().parent

FIG_W, FIG_H = 15, 4.5


def create_regulation_workflow():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
        'Zurich Model\u2013Aligned Regulation and Prompt Assembly')

    c = DS.COLOR_GREEN
    dot = "\u00b7"
    phat = r"$\hat{P}$"

    box_w, box_h = 2.1, 1.0
    gap = 0.3
    y_mid = content_y - box_h - 0.15
    x_start = 0.4

    # 1-6: Main flow
    diagram_draw_box(ax, x_start, y_mid, box_w, box_h,
                     f"Detected Personality\n{phat} = (O, C, E, A, N)",
                     facecolor=c[0], edgecolor=c[1])

    x = x_start + box_w + gap
    diagram_draw_box(ax, x, y_mid, box_w, box_h,
                     f"Map Traits to Needs\nSecurity {dot} Arousal {dot} Affiliation",
                     facecolor=c[0], edgecolor=c[1])
    diagram_draw_arrow(ax, x - gap, y_mid + box_h / 2, x, y_mid + box_h / 2)

    x += box_w + gap
    diagram_draw_box(ax, x, y_mid, box_w, box_h,
                     "Select Trait Prompts\nselect non-neutral traits",
                     facecolor=c[0], edgecolor=c[1])
    diagram_draw_arrow(ax, x - gap, y_mid + box_h / 2, x, y_mid + box_h / 2)

    x += box_w + gap
    diagram_draw_box(ax, x, y_mid, box_w, box_h,
                     "Harmonize Conflicts\ne.g., High O vs. Low E",
                     facecolor=c[0], edgecolor=c[1])
    diagram_draw_arrow(ax, x - gap, y_mid + box_h / 2, x, y_mid + box_h / 2)

    x += box_w + gap
    x_assembly = x
    diagram_draw_box(ax, x, y_mid, box_w, box_h,
                     "Assemble Regulation Prompt\nsingle consolidated instruction block",
                     facecolor=c[0], edgecolor=c[1])
    diagram_draw_arrow(ax, x - gap, y_mid + box_h / 2, x, y_mid + box_h / 2)

    x_final = x + box_w + gap
    diagram_draw_box(ax, x_final, y_mid, box_w, box_h,
                     "Response Generation\n(Assistant Reply)",
                     facecolor=c[0], edgecolor=c[1])
    diagram_draw_arrow(ax, x_final - gap, y_mid + box_h / 2, x_final, y_mid + box_h / 2)

    # Audit logging branch
    y_log = y_mid - box_h - 0.4
    diagram_draw_box(ax, x_final, y_log, box_w, box_h,
                     "Audit Logging\nlog prompts + decisions",
                     facecolor=c[0], edgecolor=c[1])

    ax.plot([x_assembly + box_w / 2, x_assembly + box_w / 2, x_final],
            [y_mid, y_log + box_h / 2, y_log + box_h / 2],
            color=DS.ARROW_COLOR, linestyle='--', linewidth=DS.ARROW_LINEWIDTH)
    diagram_draw_arrow(ax, x_assembly + box_w / 2, y_log + box_h / 2,
                       x_final, y_log + box_h / 2,
                       style='dashed', label='log')

    ax.set_ylim(y_log - 0.25, FIG_H)
    DS.save(fig, "regulation_workflow_mdpi", str(OUT))


if __name__ == "__main__":
    create_regulation_workflow()
