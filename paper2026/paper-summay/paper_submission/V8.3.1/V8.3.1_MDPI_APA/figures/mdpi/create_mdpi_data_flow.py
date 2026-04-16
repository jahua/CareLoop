#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Data Processing Pipeline (Figure 3)
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

FIG_W, FIG_H = 15, 3.2


def create_data_flow_pipeline():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y, 'End-to-End Data Processing Pipeline')

    c_blue = DS.COLOR_BLUE
    c_green = DS.COLOR_GREEN
    c_lav = DS.COLOR_LAVENDER

    box_w, box_h = 1.8, 1.0
    gap = 0.3
    # Keep content compact near the title and trim empty lower area.
    y_mid = content_y - box_h - 0.10

    steps = [
        ("1. Input",      "user message\ncontext history",        c_blue),
        ("2. Detection",  "linguistic analysis\nOCEAN inference",  c_blue),
        ("3. Mapping",    "Zurich Model\ntrait-to-need",          c_green),
        ("4. Assembly",   "prompt logic\naugmentation",           c_green),
        ("5. Generation", "GPT-4 instance\nadaptive response",    c_green),
        ("6. Evaluation", "LLM-as-judge\nexpert audit",           c_lav),
        ("7. Logging",    "state persistence\ntraceability",      c_lav),
    ]

    start_x = (FIG_W - (len(steps) * box_w + (len(steps) - 1) * gap)) / 2

    for i, (title, sub, col) in enumerate(steps):
        x = start_x + i * (box_w + gap)
        diagram_draw_box(ax, x, y_mid, box_w, box_h, f"{title}\n{sub}",
                         facecolor=col[0], edgecolor=col[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)
        if i < len(steps) - 1:
            diagram_draw_arrow(ax, x + box_w + 0.05, y_mid + box_h / 2,
                               x + box_w + gap - 0.05, y_mid + box_h / 2)

    ax.set_ylim(y_mid - 0.25, FIG_H)
    DS.save(fig, "data_flow_mdpi", str(OUT))


if __name__ == "__main__":
    create_data_flow_pipeline()
