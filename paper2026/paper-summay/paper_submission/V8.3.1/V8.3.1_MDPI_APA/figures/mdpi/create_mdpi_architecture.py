#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready System Architecture Diagram
Uses unified DiagramStyle from visualization_config.
"""

import sys
from pathlib import Path
from typing import Dict

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
    _wrap_preserving_newlines,
)

OUT = Path(__file__).resolve().parent
FIG_W, FIG_H = 12.8, 9


def _compute_box_height(n_title_lines, n_body_lines, *, pad_y=None, fontsize=None):
    if pad_y is None:
        pad_y = DS.BOX_PAD
    if fontsize is None:
        fontsize = DS.CONTENT_FONTSIZE
    title_line = DS.BOX_TITLE_LH * (fontsize / 10.0)
    body_line = DS.BOX_BODY_LH * (DS.body_fontsize() / 10.0)
    gap = DS.BOX_GAP_H if n_body_lines > 0 else 0.0
    text_h = n_title_lines * title_line + gap + n_body_lines * body_line
    return max(0.62, pad_y * 2 + text_h)


def create_mdpi_architecture():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
                       'System Architecture: Personality-Adaptive Conversational AI')

    colors = {
        'input':      DS.COLOR_BLUE,
        'detection':  DS.COLOR_GREEN,
        'regulation': (DS.COLOR_ORANGE[0].replace('#FFF9F3', '#FCF7EE'), DS.ARROW_COLOR),
        'generation': DS.COLOR_LAVENDER,
        'evaluation': ('#FCF3F3', DS.ARROW_COLOR),
        'storage':    DS.COLOR_NEUTRAL,
        'promise':    DS.COLOR_PROMISE,
    }

    pipe_w = 6.4
    gap = 0.25
    promise_h = 0.30
    promise_margin_below = 0.12
    storage_w = 2.1
    storage_gap = 0.2 * storage_w
    total_w = pipe_w + storage_gap + storage_w
    pipe_x = (FIG_W - total_w) / 2
    storage_x = pipe_x + pipe_w + storage_gap

    y_promise = content_y - 0.15
    diagram_draw_box(ax, pipe_x, y_promise, total_w, promise_h,
                     "PROMISE orchestration (state transitions, prompt composition, storage access)",
                     facecolor=colors['promise'][0], edgecolor=colors['promise'][1],
                     linewidth=0.9, fontsize=DS.CONTENT_BODY_FONTSIZE,
                     bold_title=False, wrap_width=70)

    y_top = y_promise - promise_margin_below
    boxes = {}
    pipeline_wrap = 34

    pipeline_specs = [
        ("input",       "Input\nuser message \u00b7 context",                      colors["input"]),
        ("detection",   "Trait inference\nOCEAN prompts",                           colors["detection"]),
        ("trait_state", "Inferred trait state\n$\\hat{P}$ \u00b7 confidence",       colors["detection"]),
        ("regulation",  "Trait-aligned regulation\nZurich Model:\nSecurity \u00b7 Arousal \u00b7 Affiliation", colors["regulation"]),
        ("prompt",      "Prompt assembly\nbase + regulation",                       colors["generation"]),
        ("llm",         "LLM response generation\n(GPT-4)",                         colors["generation"]),
        ("response",    "Assistant response",                                       colors["generation"]),
        ("evaluation",  "Evaluation\nLLM judge \u00b7 expert \u00b7 stats",        colors["evaluation"]),
    ]

    heights: Dict[str, float] = {}
    for key, txt, _c in pipeline_specs:
        title = txt.split("\n", 1)[0]
        body = txt.split("\n", 1)[1] if "\n" in txt else ""
        tl = _wrap_preserving_newlines(title, width=pipeline_wrap)
        bl = _wrap_preserving_newlines(body, width=pipeline_wrap) if body else []
        heights[key] = _compute_box_height(len(tl), len(bl),
                           pad_y=DS.BOX_PAD, fontsize=DS.CONTENT_FONTSIZE)

    y_cursor = y_top
    for key, txt, c in pipeline_specs:
        h = heights[key]
        y = y_cursor - h
        boxes[key] = diagram_draw_box(
            ax, pipe_x, y, pipe_w, h, txt,
            facecolor=c[0], edgecolor=c[1],
            bold_title=True, wrap_width=pipeline_wrap)
        y_cursor = y - gap

    trait_mid_y = boxes["trait_state"].get_y() + boxes["trait_state"].get_height() / 2
    eval_mid_y = boxes["evaluation"].get_y() + boxes["evaluation"].get_height() / 2
    storage_y = boxes["evaluation"].get_y()
    storage_h = boxes["trait_state"].get_y() + boxes["trait_state"].get_height() - storage_y

    diagram_draw_box(ax, storage_x, storage_y, storage_w, storage_h,
                     "Interaction storage\nAll states & metrics logged per turn",
                     facecolor=colors['storage'][0], edgecolor=colors['storage'][1],
                     bold_title=True, wrap_width=22)

    def mid_x(): return pipe_x + pipe_w / 2
    def top_of(k): return boxes[k].get_y() + boxes[k].get_height()
    def bottom_of(k): return boxes[k].get_y()

    for a, b in [("input", "detection"), ("detection", "trait_state"),
                 ("trait_state", "regulation"), ("regulation", "prompt"),
                 ("prompt", "llm"), ("llm", "response"), ("response", "evaluation")]:
        diagram_draw_arrow(ax, mid_x(), bottom_of(a), mid_x(), top_of(b))

    storage_left = storage_x - DS.BOX_PAD
    pipeline_right = pipe_x + pipe_w + DS.BOX_PAD
    diagram_draw_arrow(ax, pipeline_right, trait_mid_y, storage_left, trait_mid_y, style='dashed')
    diagram_draw_arrow(ax, pipeline_right, eval_mid_y, storage_left, eval_mid_y, style='dashed')

    label_x = pipe_x - 0.35
    for key, label in [("input", "INPUT"), ("detection", "DETECTION"),
                       ("regulation", "REGULATION"), ("llm", "GENERATION"),
                       ("evaluation", "EVALUATION")]:
        diagram_draw_layer_label(
            ax, label_x,
            boxes[key].get_y() + boxes[key].get_height() / 2,
            label, color="#000000", alpha=1.0)

    ax.set_ylim(boxes["evaluation"].get_y() - 0.25, FIG_H)
    DS.save(fig, "system_architecture_mdpi", str(OUT))


if __name__ == "__main__":
    create_mdpi_architecture()
