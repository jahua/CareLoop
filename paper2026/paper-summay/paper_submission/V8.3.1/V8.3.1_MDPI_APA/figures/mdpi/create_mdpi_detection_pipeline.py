#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Personality Detection Pipeline Figure
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
    diagram_draw_layer_label,
    diagram_title_y,
    diagram_content_top_y,
)

OUT = Path(__file__).resolve().parent

FIG_W, FIG_H = 10, 9.5


def create_detection_pipeline():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
                       'Personality Detection Pipeline: Real-Time OCEAN Inference')

    c = {
        'input':     DS.COLOR_BLUE,
        'inference': DS.COLOR_GREEN,
        'state':     DS.COLOR_LAVENDER,
        'interface': ('#FFFFFF', DS.ARROW_COLOR),
    }

    cx = FIG_W / 2
    box_h = 1.05
    dot = "\u00b7"
    phat = r"$\hat{P}$"

    layer_gap = 1.8
    y_input = content_y - box_h
    y_inference = y_input - layer_gap
    y_state = y_inference - layer_gap - 0.6
    y_interface = y_state - layer_gap

    # INPUT LAYER
    diagram_draw_layer_label(ax, 0.6, y_input + box_h / 2, "INPUT\nLAYER")
    input_w, input_gap = 3.5, 0.5
    diagram_draw_box(ax, cx - input_gap / 2 - input_w, y_input, input_w, box_h,
                     "User Message\n(Current Turn)", facecolor=c['input'][0], edgecolor=c['input'][1])
    diagram_draw_box(ax, cx + input_gap / 2, y_input, input_w, box_h,
                     "Dialogue Context\n(History)", facecolor=c['input'][0], edgecolor=c['input'][1])

    y_input_bar = y_input - 0.45
    bar_x_start = cx - input_gap / 2 - input_w / 2
    bar_x_end = cx + input_gap / 2 + input_w / 2
    connector_lw = DS.ARROW_LINEWIDTH * 0.85
    connector_alpha = 0.55
    ax.plot([bar_x_start, bar_x_end], [y_input_bar, y_input_bar],
            color=DS.ARROW_COLOR, lw=connector_lw, alpha=connector_alpha)
    ax.plot([bar_x_start, bar_x_start], [y_input - 0.03, y_input_bar],
            color=DS.ARROW_COLOR, lw=connector_lw, alpha=connector_alpha,
            solid_capstyle='butt')
    ax.plot([bar_x_end, bar_x_end], [y_input - 0.03, y_input_bar],
            color=DS.ARROW_COLOR, lw=connector_lw, alpha=connector_alpha,
            solid_capstyle='butt')
    # Ensure this is a visible downward arrow into the inference section.
    diagram_draw_arrow(ax, cx, y_input_bar, cx, y_inference + box_h + 0.08)

    # INFERENCE LAYER
    diagram_draw_layer_label(ax, 0.45, y_inference + box_h / 2, "INFERENCE\nLAYER")
    ax.text(cx, y_inference + box_h + 0.45,
            "Parallel Trait Detectors (Per-Turn Inference)",
            ha='center', va='bottom', fontsize=DS.FOOTNOTE_FONTSIZE,
            fontweight='bold', color=DS.ANNOTATION_COLOR)

    inf_w, inf_gap = 1.7, 0.12
    inf_total_w = 5 * inf_w + 4 * inf_gap
    inf_start_x = cx - inf_total_w / 2

    traits = [
        ("Openness (O)",          f"curiosity {dot} novelty-seeking"),
        ("Conscientiousness\n(C)", f"organization {dot} structure"),
        ("Extraversion (E)",      f"social energy {dot} assertiveness"),
        ("Agreeableness\n(A)",     f"cooperation {dot} empathy"),
        ("Neuroticism (N)",       "emotional stability"),
    ]

    for i, (title, sub) in enumerate(traits):
        bx = inf_start_x + i * (inf_w + inf_gap)
        diagram_draw_box(ax, bx, y_inference, inf_w, box_h,
                         f"{title}\n{sub}",
                         facecolor=c['inference'][0], edgecolor=c['inference'][1],
                         fontsize=DS.CONTENT_FONTSIZE - 0.7,
                         wrap_width=18)

    y_inf_bar = y_inference - 0.32
    first_center = inf_start_x + inf_w / 2
    last_center = inf_start_x + 4 * (inf_w + inf_gap) + inf_w / 2
    ax.plot([first_center, last_center], [y_inf_bar, y_inf_bar],
            color=DS.ARROW_COLOR, lw=connector_lw, alpha=0.50)
    for i in range(5):
        bx_center = inf_start_x + i * (inf_w + inf_gap) + inf_w / 2
        # Start slightly below box border to avoid line/border overlap.
        ax.plot([bx_center, bx_center], [y_inference - 0.03, y_inf_bar],
                color=DS.ARROW_COLOR, lw=connector_lw, alpha=0.50)

    y_footnote = y_inf_bar - 0.20
    ax.text(cx, y_footnote, f"Per-trait prompts {dot} GPT-4 instance",
            ha='center', va='top', fontsize=DS.FOOTNOTE_FONTSIZE,
            fontstyle='italic', color=DS.ANNOTATION_COLOR)

    y_arrow_start = y_footnote - 0.25
    y_split = y_state + box_h + 0.35
    diagram_draw_arrow(ax, cx, y_arrow_start, cx, y_split)

    # STATE & OUTPUT LAYER
    diagram_draw_layer_label(ax, 0.6, y_state + box_h / 2, "STATE &\nOUTPUT LAYER")
    state_w, state_gap = 4.0, 0.6
    split_x_left = cx - state_gap / 2 - state_w / 2
    split_x_right = cx + state_gap / 2 + state_w / 2
    ax.plot([split_x_left, split_x_right], [y_split, y_split],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH)
    diagram_draw_arrow(ax, split_x_left, y_split, split_x_left, y_state + box_h)
    diagram_draw_arrow(ax, split_x_right, y_split, split_x_right, y_state + box_h)

    diagram_draw_box(ax, cx - state_gap / 2 - state_w, y_state, state_w, box_h,
                     "Personality State Update\ncumulative evidence across turns",
                     facecolor=c['state'][0], edgecolor=c['state'][1])
    diagram_draw_box(ax, cx + state_gap / 2, y_state, state_w, box_h,
                     f"OCEAN Vector Output\n{phat} = (O, C, E, A, N) + confidence",
                     facecolor=c['state'][0], edgecolor=c['state'][1],
                     wrap_width=DS.BOX_WRAP_WIDTH)

    # INTERFACE LAYER
    diagram_draw_layer_label(ax, 0.6, y_interface + box_h / 2, "INTERFACE\nLAYER")
    inter_w = 7.2
    y_merge = y_interface + box_h + 0.5
    ax.plot([split_x_left, split_x_right], [y_merge, y_merge],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH)
    ax.plot([split_x_left, split_x_left], [y_state - 0.03, y_merge],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    ax.plot([split_x_right, split_x_right], [y_state - 0.03, y_merge],
            color=DS.ARROW_COLOR, lw=DS.ARROW_LINEWIDTH, solid_capstyle='butt')
    diagram_draw_arrow(ax, cx, y_merge, cx, y_interface + box_h)

    diagram_draw_box(ax, cx - inter_w / 2, y_interface, inter_w, box_h,
                     f"Interface to Regulation Module\ntransmit {phat} + confidence for behavior adaptation",
                     facecolor=c['interface'][0], edgecolor=c['interface'][1])

    ax.set_ylim(y_interface - 0.25, FIG_H)
    DS.save(fig, "detection_pipeline_mdpi", str(OUT))


if __name__ == "__main__":
    create_detection_pipeline()
