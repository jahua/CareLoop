#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Study Design & Experimental Workflow (Horizontal Layout)
Uses unified DiagramStyle from visualization_config.
"""

import sys
from pathlib import Path

# Allow imports from the statistical analysis directory
_STAT_DIR = str(Path(__file__).resolve().parent.parent.parent / "statistical analyis")
if _STAT_DIR not in sys.path:
    sys.path.insert(0, _STAT_DIR)

from visualization_config import (
    DIAGRAM_STYLE as DS,
    diagram_setup_figure,
    diagram_draw_box,
    diagram_draw_arrow,
    diagram_draw_title,
    diagram_draw_phase_label,
    diagram_title_y,
    diagram_content_top_y,
)

OUT = Path(__file__).resolve().parent

FIG_W, FIG_H = 14, 5.0

def create_mdpi_study_design():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
                       'Study Design & Experimental Workflow')

    c = {
        'blue':   ('#F7F9FF', '#555555'),
        'green':  ('#F7FFF9', '#555555'),
        'gray':   ('#FBFBFB', '#555555'),
        'purple': ('#FAF7FF', '#555555'),
    }

    box_w, box_h = 2.8, 0.9
    v_gap, h_gap = 0.35, 0.6
    x_start = (FIG_W - (4 * box_w + 3 * h_gap)) / 2
    y_top = content_y - box_h - 0.25
    phase_label_y = y_top + box_h + 0.12
    y_bot = y_top - box_h - v_gap

    pad = DS.BOX_PAD

    # PHASE I
    x1 = x_start
    diagram_draw_phase_label(ax, x1 + box_w / 2, phase_label_y, "PHASE I: CONFIGURATION")
    diagram_draw_box(ax, x1, y_top, box_w, box_h,
                     "Experimental Setup\n20 agents \u00b7 random assignment",
                     facecolor=c['blue'][0], edgecolor=c['blue'][1])
    diagram_draw_box(ax, x1, y_bot, box_w, box_h,
                     "Personality Profiles\nType A: all traits = +1\nType B: all traits = \u22121",
                     facecolor=c['blue'][0], edgecolor=c['blue'][1])
    ax.text(x1 + box_w / 2, y_bot - 0.22, "Boundary-condition simulation",
            fontsize=DS.FOOTNOTE_FONTSIZE, ha='center', fontstyle='italic',
            color=DS.ANNOTATION_COLOR)
    diagram_draw_arrow(ax, x1 + box_w / 2, y_top - pad, x1 + box_w / 2, y_bot + box_h + pad)

    # PHASE II
    x2 = x1 + box_w + h_gap
    diagram_draw_phase_label(ax, x2 + box_w / 2, phase_label_y, "PHASE II: INTERVENTION")
    ax.text(x2 + box_w / 2, phase_label_y - 0.2, "Same LLM instance",
            fontsize=DS.FOOTNOTE_FONTSIZE, ha='center', fontweight='bold',
            color=DS.ANNOTATION_COLOR)
    diagram_draw_box(ax, x2, y_top, box_w, box_h,
                     "Regulated Condition\nRegulation: ON",
                     facecolor=c['green'][0], edgecolor=c['green'][1])
    diagram_draw_box(ax, x2, y_bot, box_w, box_h,
                     "Baseline Condition\nRegulation: OFF",
                     facecolor=c['green'][0], edgecolor=c['green'][1])

    # PHASE III
    x3 = x2 + box_w + h_gap
    diagram_draw_phase_label(ax, x3 + box_w / 2, phase_label_y, "PHASE III: COLLECTION")
    diagram_draw_box(ax, x3, y_top, box_w, box_h,
                     "Dialogue Protocol\n120 dialogues \u00b7 6 turns",
                     facecolor=c['gray'][0], edgecolor=c['gray'][1])
    diagram_draw_box(ax, x3, y_bot, box_w, box_h,
                     "Evaluation\nLLM-judge \u00b7 Human audit",
                     facecolor=c['gray'][0], edgecolor=c['gray'][1])
    diagram_draw_arrow(ax, x3 + box_w / 2, y_top - pad, x3 + box_w / 2, y_bot + box_h + pad)

    # PHASE IV
    x4 = x3 + box_w + h_gap
    diagram_draw_phase_label(ax, x4 + box_w / 2, phase_label_y, "PHASE IV: VALIDATION")
    diagram_draw_box(ax, x4, y_top, box_w, box_h,
                     "Outcome Analysis\nEffect sizes \u00b7 Reliability",
                     facecolor=c['purple'][0], edgecolor='#AAAAAA',
                     linewidth=0.8)
    diagram_draw_box(ax, x4, y_bot, box_w, box_h,
                     "Outcome Comparison\nRegulated vs Baseline",
                     facecolor=c['purple'][0], edgecolor='#333333',
                     linewidth=1.6)
    diagram_draw_arrow(ax, x4 + box_w / 2, y_top - pad, x4 + box_w / 2, y_bot + box_h + pad)

    # T-junction & convergence arrows
    cx1 = x1 + box_w + h_gap / 2
    ax.plot([x1 + box_w + pad, cx1], [y_bot + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([cx1, cx1], [y_top + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    diagram_draw_arrow(ax, cx1, y_top + box_h / 2, x2 - pad, y_top + box_h / 2)
    diagram_draw_arrow(ax, cx1, y_bot + box_h / 2, x2 - pad, y_bot + box_h / 2)

    cx2 = x2 + box_w + h_gap / 2
    ax.plot([x2 + box_w + pad, cx2], [y_top + box_h / 2, y_top + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([x2 + box_w + pad, cx2], [y_bot + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([cx2, cx2], [y_top + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    diagram_draw_arrow(ax, cx2, y_top + box_h / 2, x3 - pad, y_top + box_h / 2)

    cx3 = x3 + box_w + h_gap / 2
    ax.plot([x3 + box_w + pad, cx3], [y_top + box_h / 2, y_top + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([x3 + box_w + pad, cx3], [y_bot + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([cx3, cx3], [y_top + box_h / 2, y_bot + box_h / 2],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    diagram_draw_arrow(ax, cx3, y_top + box_h / 2, x4 - pad, y_top + box_h / 2)

    min_y_content = y_bot - 0.3
    ax.set_ylim(min_y_content, FIG_H)

    DS.save(fig, "study_design_mdpi", str(OUT))


if __name__ == "__main__":
    create_mdpi_study_design()
