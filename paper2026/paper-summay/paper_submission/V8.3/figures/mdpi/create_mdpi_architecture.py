#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready System Architecture Diagram
Matches manuscript exactly with PROMISE orchestration, interaction storage, and proper regulation flow.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import textwrap
from typing import Dict, List, Optional

# Output directory
OUT = Path(__file__).resolve().parent


def setup_figure():
    """Create figure with MDPI-appropriate settings."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['font.size'] = 9
    # Ensure clear P-hat rendering in mathtext
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    
    # Wider canvas to prevent any text clipping/overlap.
    fig, ax = plt.subplots(figsize=(12.8, 10), dpi=600)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 10)
    ax.axis('off')
    return fig, ax


def _wrap_preserving_newlines(text: str, width: int) -> List[str]:
    """Wrap text to a fixed character width, preserving explicit newlines."""
    out: List[str] = []
    for seg in text.split("\n"):
        seg = seg.strip()
        if not seg:
            out.append("")
            continue
        out.extend(textwrap.wrap(seg, width=width, break_long_words=False, break_on_hyphens=False))
    return out


def _compute_box_height(n_title_lines: int, n_body_lines: int, *, pad_y: float, fontsize: float) -> float:
    """Compute a box height in axis units based on line count and padding."""
    # Tuned to axis units for figsize ~ (12.8, 10).
    title_line = 0.14 * (fontsize / 10.0)
    body_line = 0.12 * (max(8.0, fontsize - 1.0) / 10.0)
    gap = 0.08 if n_body_lines > 0 else 0.0
    text_h = n_title_lines * title_line + gap + n_body_lines * body_line
    return max(0.62, pad_y * 2 + text_h)


def draw_box(ax, x, y, w, h, text, facecolor='#E8F4F8', edgecolor='#2C5F7E', 
             linewidth=1.5, fontsize=9, fontweight='normal', text_color='#000000',
             bold_title=True, wrap_width: Optional[int] = None, pad: float = 0.03):
    """Draw a rounded rectangle box with wrapped text (bold title line only)."""
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth
    )
    ax.add_patch(box)
    
    cx = x + w / 2
    pad_y = pad

    # Wrap: keep first explicit line(s) as title block, remaining as body block
    parts = text.split("\n", 1)
    raw_title = parts[0]
    raw_body = parts[1] if len(parts) > 1 else ""

    if wrap_width is None:
        wrap_width = 32

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    # Approximate line heights in axis units
    title_lh = 0.14 * (fontsize / 10.0)
    body_fs = max(8.0, fontsize - 1.0)
    body_lh = 0.12 * (body_fs / 10.0)

    title_h = len(title_lines) * title_lh
    gap_h = 0.08 if body_lines else 0.0
    body_h = len(body_lines) * body_lh
    total_text_h = title_h + gap_h + body_h

    # Position: center-align inside box vertically
    cy = y + h / 2
    y_title_center = cy + (total_text_h / 2) - (title_h / 2)
    y_body_center = cy - (total_text_h / 2) + (body_h / 2) if body_lines else None

    title_text = "\n".join([ln for ln in title_lines if ln != ""])
    body_text = "\n".join([ln for ln in body_lines if ln != ""])

    if title_text:
        ax.text(
            cx,
            y_title_center,
            title_text,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold" if bold_title else fontweight,
            color=text_color,
            linespacing=1.12,
        )
    if body_text and y_body_center is not None:
        ax.text(
            cx,
            y_body_center,
            body_text,
            ha="center",
            va="center",
            fontsize=body_fs,
            fontweight=fontweight,
            color=text_color,
            linespacing=1.12,
        )
    return box


def draw_arrow(ax, x1, y1, x2, y2, style='solid', color='#444444', 
               linewidth=1.8, label='', label_offset=(0, 0),
               shrinkA: float = 10, shrinkB: float = 10):
    """Draw an arrow with various styles."""
    linestyle_map = {
        'solid': '-',
        'dashed': '--',
        'dotted': ':'
    }
    
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    color=color,
                    linewidth=linewidth,
                    linestyle=linestyle_map.get(style, '-'),
                    shrinkA=shrinkA,
                    shrinkB=shrinkB,
                ))
    
    if label:
        mid_x = (x1 + x2) / 2 + label_offset[0]
        mid_y = (y1 + y2) / 2 + label_offset[1]
        ax.text(mid_x, mid_y, label, fontsize=7, 
                style='italic', color='#666666',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                         edgecolor='none', alpha=0.8))


def draw_layer_label(ax, x, y, text, color='#2C5F7E', fontsize=9, fontweight='normal', alpha=0.7):
    """Draw subtle layer label on the left."""
    ax.text(
        x,
        y,
        text,
        fontsize=fontsize,
        fontweight=fontweight,
        color=color,
        alpha=alpha,
        ha='right',
        va='center',
    )


def create_mdpi_architecture():
    """Create the complete MDPI-ready architecture diagram."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(6, 9.5, 'System Architecture: Personality-Adaptive Conversational AI',
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Color scheme (MDPI-friendly pastels, grayscale-safe)
    colors = {
        # Low-saturation fills + neutral borders for grayscale/print.
        'input': ('#F3F9FC', '#3F3F3F'),
        'detection': ('#F3FAF6', '#3F3F3F'),
        'regulation': ('#FCF7EE', '#3F3F3F'),
        'generation': ('#F6F3FC', '#3F3F3F'),
        'evaluation': ('#FCF3F3', '#3F3F3F'),
        'storage': ('#FAFAFA', '#3F3F3F'),
        'promise': ('#F5F5F5', '#BDBDBD'),
    }
    
    # Layout constants (orthogonal arrows only)
    pipe_w = 6.4
    gap = 0.20  # normalized vertical spacing between all pipeline boxes
    promise_h = 0.32
    promise_margin_below = 0.18

    # Storage sizing and placement (further left per request)
    storage_w = 2.1
    storage_gap = 0.2 * storage_w  # further reduced gap

    # Center composition (pipeline + storage) horizontally
    total_w = pipe_w + storage_gap + storage_w
    pipe_x = (13 - total_w) / 2
    storage_x = pipe_x + pipe_w + storage_gap

    # PROMISE orchestration band (thin; no arrows)
    y_promise = 8.85
    draw_box(
        ax,
        pipe_x,
        y_promise,
        total_w,
        promise_h,
        "PROMISE orchestration (state transitions, prompt composition, storage access)",
        facecolor=colors["promise"][0],
        edgecolor=colors["promise"][1],
        linewidth=0.9,
        fontsize=8,
        bold_title=False,
        wrap_width=70,
        pad=0.03,
    )

    # Main vertical pipeline boxes (top to bottom)
    y_top = y_promise - promise_margin_below
    boxes = {}
    pipeline_specs = [
        ("input", "Input\nuser message · context", colors["input"]),
        ("detection", "Trait inference\nOCEAN prompts", colors["detection"]),
        ("trait_state", "Inferred trait state\n$\\hat{P}$ · confidence", colors["detection"]),
        ("regulation", "Trait-aligned regulation\nZurich Model:\nSecurity · Arousal · Affiliation", colors["regulation"]),
        ("prompt", "Prompt assembly\nbase + regulation", colors["generation"]),
        ("llm", "LLM response generation\n(GPT-4)", colors["generation"]),
        ("response", "Assistant response", colors["generation"]),
        ("evaluation", "Evaluation\nLLM judge · expert · stats", colors["evaluation"]),
    ]

    # Precompute heights based on wrapping (fixed char width).
    pipeline_wrap = 34
    font_main = 10
    pad = 0.035

    heights: Dict[str, float] = {}
    for key, txt, _c in pipeline_specs:
        title = txt.split("\n", 1)[0]
        body = txt.split("\n", 1)[1] if "\n" in txt else ""
        title_lines = _wrap_preserving_newlines(title, width=pipeline_wrap)
        body_lines = _wrap_preserving_newlines(body, width=pipeline_wrap) if body else []
        heights[key] = _compute_box_height(len(title_lines), len(body_lines), pad_y=pad, fontsize=font_main)

    # Layout sequentially with equal gaps (no local compression)
    y_cursor = y_top
    for key, txt, c in pipeline_specs:
        h = heights[key]
        y = y_cursor - h
        boxes[key] = draw_box(
            ax,
            pipe_x,
            y,
            pipe_w,
            h,
            txt,
            facecolor=c[0],
            edgecolor=c[1],
            fontsize=font_main,
            bold_title=True,
            wrap_width=pipeline_wrap,
            pad=pad,
        )
        y_cursor = y - gap

    # Interaction storage placement:
    # - closer to pipeline
    # - moved toward bottom (aligned with evaluation box)
    # - tall enough to catch both trait_state and evaluation arrows
    trait_mid_y = boxes["trait_state"].get_y() + boxes["trait_state"].get_height() / 2
    eval_mid_y = boxes["evaluation"].get_y() + boxes["evaluation"].get_height() / 2

    storage_bottom = boxes["evaluation"].get_y()
    storage_top = boxes["trait_state"].get_y() + boxes["trait_state"].get_height()
    
    storage_y = storage_bottom
    storage_h = storage_top - storage_bottom

    draw_box(
        ax,
        storage_x,
        storage_y,
        storage_w,
        storage_h,
        "Interaction storage\nAll states & metrics logged per turn",
        facecolor=colors["storage"][0],
        edgecolor=colors["storage"][1],
        fontsize=9,
        bold_title=True,
        wrap_width=22,
        pad=pad,
    )

    # Data-flow arrows (solid; vertical only)
    def mid_x() -> float:
        return pipe_x + pipe_w / 2

    def top_of(key: str) -> float:
        return boxes[key].get_y() + boxes[key].get_height()

    def bottom_of(key: str) -> float:
        return boxes[key].get_y()

    for a, b in [
        ("input", "detection"),
        ("detection", "trait_state"),
        ("trait_state", "regulation"),
        ("regulation", "prompt"),
        ("prompt", "llm"),
        ("llm", "response"),
        ("response", "evaluation"),
    ]:
        draw_arrow(
            ax,
            mid_x(),
            bottom_of(a),
            mid_x(),
            top_of(b),
            style="solid",
            shrinkA=0,
            shrinkB=0,
        )

    # Logging arrows (dashed per request; horizontal only) - EXACTLY TWO (no labels)
    # Start at visual right edge of pipeline, end at visual left edge of storage
    storage_left_visual = storage_x - pad
    pipeline_right_visual = pipe_x + pipe_w + pad

    draw_arrow(
        ax,
        pipeline_right_visual,
        trait_mid_y,
        storage_left_visual,
        trait_mid_y,
        style="dashed",
        label="",
        shrinkA=0,
        shrinkB=0,
    )
    draw_arrow(
        ax,
        pipeline_right_visual,
        eval_mid_y,
        storage_left_visual,
        eval_mid_y,
        style="dashed",
        label="",
        shrinkA=0,
        shrinkB=0,
    )

    # Subtle left-side layer labels (darker per request)
    label_x = pipe_x - 0.35
    dark = "#000000"
    draw_layer_label(ax, label_x, boxes["input"].get_y() + boxes["input"].get_height() / 2, "INPUT", color=dark, fontsize=9, fontweight="bold", alpha=1.0)
    draw_layer_label(ax, label_x, boxes["detection"].get_y() + boxes["detection"].get_height() / 2, "DETECTION", color=dark, fontsize=9, fontweight="bold", alpha=1.0)
    draw_layer_label(ax, label_x, boxes["regulation"].get_y() + boxes["regulation"].get_height() / 2, "REGULATION", color=dark, fontsize=9, fontweight="bold", alpha=1.0)
    draw_layer_label(ax, label_x, boxes["llm"].get_y() + boxes["llm"].get_height() / 2, "GENERATION", color=dark, fontsize=9, fontweight="bold", alpha=1.0)
    draw_layer_label(ax, label_x, boxes["evaluation"].get_y() + boxes["evaluation"].get_height() / 2, "EVALUATION", color=dark, fontsize=9, fontweight="bold", alpha=1.0)
    
    # Save outputs
    pdf_path = OUT / "system_architecture_mdpi.pdf"
    png_path = OUT / "system_architecture_mdpi.png"
    
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', 
                pad_inches=0.1, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight',
                pad_inches=0.1, dpi=600)
    
    plt.close(fig)
    
    print("Created MDPI-ready system architecture:")
    print(f"  PDF (vector): {pdf_path}")
    print(f"  PNG (600dpi): {png_path}")
    
    return pdf_path, png_path


if __name__ == "__main__":
    create_mdpi_architecture()
