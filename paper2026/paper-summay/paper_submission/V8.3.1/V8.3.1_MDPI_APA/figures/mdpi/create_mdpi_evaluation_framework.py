#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Evaluation Framework & Scoring Pipeline (Figure 7)
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
    diagram_draw_section_header,
    diagram_title_y,
    diagram_content_top_y,
)

OUT = Path(__file__).resolve().parent

FIG_W, FIG_H = 10, 11.5


def create_evaluation_framework():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
        'Evaluation Framework: Criteria, Scoring, and Process')

    c_blue   = DS.COLOR_BLUE
    c_orange = DS.COLOR_ORANGE
    c_green  = DS.COLOR_GREEN
    c_lav    = DS.COLOR_LAVENDER

    cx = FIG_W / 2
    dot = "\u00b7"

    # PHASE I: EVALUATION CRITERIA
    phase1_y = content_y
    diagram_draw_section_header(ax, cx, phase1_y, "PHASE I: EVALUATION CRITERIA")

    ax.text(cx, phase1_y - 0.35, "Regulated Condition (5 Criteria)",
            fontsize=DS.CONTENT_FONTSIZE, fontweight='bold',
            ha='center', color=c_blue[1])

    y_reg = phase1_y - 1.65
    crit_h, crit_w, gap_x = 1.0, 1.6, 0.25

    reg_crit = [
        ("Detection\nAccuracy",    "trait inference\nfidelity"),
        ("Regulation\nEffectiveness", "instruction\nalignment"),
        ("Emotional\nTone",        f"warmth {dot} safety\nsupport"),
        ("Relevance &\nCoherence", "logical flow\ncontext"),
        ("Personality\nNeeds",     "trait-specific\nadaptation"),
    ]

    total_w_reg = 5 * crit_w + 4 * gap_x
    start_x_reg = cx - total_w_reg / 2
    for i, (title, sub) in enumerate(reg_crit):
        diagram_draw_box(ax, start_x_reg + i * (crit_w + gap_x), y_reg,
                         crit_w, crit_h, f"{title}\n{sub}",
                         facecolor=c_blue[0], edgecolor=c_blue[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)

    y_base = y_reg - 1.70
    ax.text(cx, y_base + 1.30, "Baseline Condition (3 Criteria)",
            fontsize=DS.CONTENT_FONTSIZE, fontweight='bold',
            ha='center', color=c_orange[1])

    base_crit = [
        ("Emotional\nTone",        "general warmth\nsupport"),
        ("Relevance &\nCoherence", "logical flow\ncontext"),
        ("Personality\nNeeds",     "non-adaptive\nsupport"),
    ]

    total_w_base = 3 * crit_w + 2 * gap_x
    start_x_base = cx - total_w_base / 2
    for i, (title, sub) in enumerate(base_crit):
        diagram_draw_box(ax, start_x_base + i * (crit_w + gap_x), y_base,
                         crit_w, crit_h, f"{title}\n{sub}",
                         facecolor=c_orange[0], edgecolor=c_orange[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)

    # PHASE II: SCORING SCALE
    phase2_y = y_base - 0.65
    diagram_draw_section_header(ax, cx, phase2_y, "PHASE II: SCORING SCALE (Ternary)")

    y_scale = phase2_y - 1.15
    scale_w, scale_h, gap_s = 2.8, 0.85, 0.3

    scale_items = [
        ("YES (2)",      "Strong alignment\nclear evidence",     c_green),
        ("NOT SURE (1)", "Partial alignment\nambiguous case",    c_orange),
        ("NO (0)",       "Clear misalignment\ncriterion not met", c_lav),
    ]

    total_w_scale = 3 * scale_w + 2 * gap_s
    start_x_scale = cx - total_w_scale / 2
    for i, (title, sub, col) in enumerate(scale_items):
        diagram_draw_box(ax, start_x_scale + i * (scale_w + gap_s), y_scale,
                         scale_w, scale_h, f"{title}\n{sub}",
                         facecolor=col[0], edgecolor=col[1])

    # PHASE III: EVALUATION PROCESS
    phase3_y = y_scale - 0.65
    diagram_draw_section_header(ax, cx, phase3_y, "PHASE III: EVALUATION PROCESS")

    y_proc = phase3_y - 1.30
    proc_w, proc_h, gap_p = 2.8, 1.0, 0.3

    proc_items = [
        ("1. AI Evaluation",      "Evaluator GPT scores\nall 120 turns"),
        ("2. Human Audit",        "Single domain expert\nqualitative review"),
        ("3. Statistical Analysis", f"Effect sizes {dot} CI\nreliability analysis"),
    ]

    total_w_proc = 3 * proc_w + 2 * gap_p
    start_x_proc = cx - total_w_proc / 2
    for i, (title, sub) in enumerate(proc_items):
        x_box = start_x_proc + i * (proc_w + gap_p)
        diagram_draw_box(ax, x_box, y_proc, proc_w, proc_h, f"{title}\n{sub}",
                         facecolor=c_blue[0], edgecolor=c_blue[1])
        if i < 2:
            diagram_draw_arrow(ax, x_box + proc_w + 0.05, y_proc + proc_h / 2,
                               x_box + proc_w + gap_p - 0.05, y_proc + proc_h / 2)

    # OUTCOME
    outcome_header_y = y_proc - 0.65
    diagram_draw_section_header(ax, cx, outcome_header_y, "SYSTEM VALIDATION OUTCOME")

    outcome_txt = (
        "Implementation Fidelity & Selective Enhancement\n"
        "Technical Verification: 100% detection and regulation fidelity confirmed.\n"
        "Comparative Finding: Personality needs addressed significantly better in regulated condition (d = 4.65).\n"
        "Quality Retention: Generic quality (tone, relevance) maintained at ceiling level."
    )
    outcome_box_y = outcome_header_y - 1.55
    diagram_draw_box(ax, 0.5, outcome_box_y, 9.0, 1.25, outcome_txt,
                     facecolor=c_green[0], edgecolor=c_green[1],
                     wrap_width=120)

    ax.set_ylim(outcome_box_y - 0.10, FIG_H)
    DS.save(fig, "evaluation_framework_mdpi", str(OUT))


if __name__ == "__main__":
    create_evaluation_framework()
