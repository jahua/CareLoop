#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Personality Detection Pipeline Figure (Final Refinement).
Focus: Perfect symmetry, collector/collector bars, and rigorous alignment.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import textwrap
from typing import List, Optional

# Output directory
OUT = Path(__file__).resolve().parent


def setup_figure():
    """Create figure with MDPI-appropriate settings."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['font.size'] = 9
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    
    # Vertical layout for pipeline
    fig, ax = plt.subplots(figsize=(10, 11), dpi=600)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
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


def draw_box(ax, x, y, w, h, text, facecolor='#FAFAFA', edgecolor='#3F3F3F', 
             linewidth=1.2, fontsize=10, fontweight='normal', text_color='#000000',
             bold_title=True, wrap_width: Optional[int] = None, pad: float = 0.06, 
             body_fontsize_scale: float = 1.0):
    """Draw a rounded rectangle box with wrapped text centered vertically."""
    box = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth
    )
    ax.add_patch(box)
    
    cx = x + w / 2
    cy = y + h / 2
    
    parts = text.split("\n", 1)
    raw_title = parts[0]
    raw_body = parts[1] if len(parts) > 1 else ""

    if wrap_width is None:
        wrap_width = 24

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    title_lh = 0.22
    body_lh = 0.18 * body_fontsize_scale
    gap_h = 0.08 if body_lines else 0.0
    
    total_text_h = (len(title_lines) * title_lh) + gap_h + (len(body_lines) * body_lh)

    y_title_center = cy + (total_text_h / 2) - (len(title_lines) * title_lh / 2)
    y_body_center = cy - (total_text_h / 2) + (len(body_lines) * body_lh / 2) if body_lines else None

    title_text = "\n".join(title_lines)
    body_text = "\n".join(body_lines)

    if title_text:
        ax.text(cx, y_title_center, title_text, ha="center", va="center",
                fontsize=fontsize, fontweight="bold" if bold_title else fontweight,
                color=text_color, linespacing=1.1)
    if body_text and y_body_center is not None:
        ax.text(cx, y_body_center, body_text, ha="center", va="center",
                fontsize=(fontsize - 1.5) * body_fontsize_scale, fontweight=fontweight,
                color=text_color, linespacing=1.1, 
                fontstyle='italic' if ('curiosity' in body_text or r"$\hat{P}$" in body_text) else 'normal')
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='#3F3F3F', linewidth=1.2, shrinkA: float = 0, shrinkB: float = 0, alpha=1.0):
    """Draw a clean orthogonal arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    color=color,
                    linewidth=linewidth,
                    linestyle='-',
                    shrinkA=shrinkA,
                    shrinkB=shrinkB,
                    alpha=alpha
                ))


def draw_layer_label(ax, x, y, text):
    """Draw layer labels on the left, right-aligned to avoid box overlap."""
    ax.text(x, y, text, fontsize=8.5, fontweight='bold', color='#666666', ha='right', va='center', linespacing=1.0)


def create_detection_pipeline():
    """Create the final refined MDPI personality detection pipeline figure."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(5, 10.5, 'Personality Detection Pipeline: Real-Time OCEAN Inference', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Layer Colors
    c = {
        'input': ('#F3F9FC', '#3F3F3F'),
        'inference': ('#F3FCF5', '#3F3F3F'),
        'state': ('#F7F3FC', '#3F3F3F'),
        'interface': ('#FFFFFF', '#3F3F3F'),
    }
    
    # Center axis
    cx = 5.0
    
    # Vertical distribution (Equalized spacing)
    # y_top to y_bottom: 10 to 1
    # 4 layers, 3 gaps
    box_h = 1.05
    y_input = 9.0
    y_inference = 6.4
    y_state = 3.5  # Slightly lowered for breathing room
    y_interface = 1.0  # Slightly lowered
    
    dot = "\u00b7"
    phat = r"$\hat{P}$"
    
    # --- 1. INPUT LAYER ---
    draw_layer_label(ax, 0.6, y_input + box_h/2, "INPUT\nLAYER")
    input_w = 3.5
    input_gap = 0.5
    
    draw_box(ax, cx - input_gap/2 - input_w, y_input, input_w, box_h, 
             "User Message\n(Current Turn)", *c['input'])
    draw_box(ax, cx + input_gap/2, y_input, input_w, box_h, 
             "Dialogue Context\n(History)", *c['input'])
    
    # Horizontal connector bar beneath input (Shortened)
    y_input_bar = y_input - 0.45
    # Just the gap between the box edges or slightly more? User says "Shorten the horizontal connector"
    # Old bar was from centers. New bar:
    bar_x_start = cx - input_gap/2 - input_w/2
    bar_x_end = cx + input_gap/2 + input_w/2
    ax.plot([bar_x_start, bar_x_end], [y_input_bar, y_input_bar], color='#3F3F3F', lw=1.2)
    # Vertical connections from boxes to bar
    ax.plot([bar_x_start, bar_x_start], [y_input, y_input_bar], color='#3F3F3F', lw=1.2)
    ax.plot([bar_x_end, bar_x_end], [y_input, y_input_bar], color='#3F3F3F', lw=1.2)
    # Single vertical arrow to inference
    draw_arrow(ax, cx, y_input_bar, cx, y_inference + box_h + 0.35)
    
    # --- 2. INFERENCE LAYER (Parallel Trait Detectors) ---
    draw_layer_label(ax, 0.45, y_inference + box_h/2, "INFERENCE\nLAYER")
    ax.text(cx, y_inference + box_h + 0.25, "Parallel Trait Detectors (Per-Turn Inference)", 
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#444444')
    
    inf_w = 1.7
    inf_gap = 0.12
    inf_total_w = 5 * inf_w + 4 * inf_gap
    inf_start_x = cx - inf_total_w/2
    
    traits = [
        ("Openness (O)", f"curiosity {dot} novelty-seeking"),
        ("Conscientiousness (C)", f"organization {dot} structure"),
        ("Extraversion (E)", f"social energy {dot} assertiveness"),
        ("Agreeableness (A)", f"cooperation {dot} empathy"),
        ("Neuroticism (N)", "emotional stability")
    ]
    
    for i, (title, sub) in enumerate(traits):
        bx = inf_start_x + i * (inf_w + inf_gap)
        draw_box(ax, bx, y_inference, inf_w, box_h, f"{title}\n{sub}", *c['inference'], 
                 fontsize=9, wrap_width=18, body_fontsize_scale=0.92)
        
    # Horizontal collector line beneath inference (Raised slightly)
    y_inf_bar = y_inference - 0.32
    ax.plot([inf_start_x, inf_start_x + inf_total_w], [y_inf_bar, y_inf_bar], color='#3F3F3F', lw=1.2, alpha=0.75)
    for i in range(5):
        bx_center = inf_start_x + i * (inf_w + inf_gap) + inf_w/2
        ax.plot([bx_center, bx_center], [y_inference, y_inf_bar], color='#3F3F3F', lw=1.2, alpha=0.75)
    
    # Subtitle footnote (Placed between collector and arrow start)
    y_footnote = y_inf_bar - 0.20
    ax.text(cx, y_footnote, f"Per-trait prompts {dot} GPT-4 instance", 
            ha='center', va='top', fontsize=7.5, fontstyle='italic', color='#777777')

    # Single vertical arrow to state layer (Starts below footnote to avoid overlap)
    y_arrow_start = y_footnote - 0.25
    y_split = y_state + box_h + 0.35
    draw_arrow(ax, cx, y_arrow_start, cx, y_split)
    
    # --- 3. STATE & OUTPUT LAYER ---
    draw_layer_label(ax, 0.6, y_state + box_h/2, "STATE &\nOUTPUT LAYER")
    state_w = 4.0
    state_gap = 0.6
    
    # Split connections
    split_x_left = cx - state_gap/2 - state_w/2
    split_x_right = cx + state_gap/2 + state_w/2
    ax.plot([split_x_left, split_x_right], [y_split, y_split], color='#3F3F3F', lw=1.2)
    draw_arrow(ax, split_x_left, y_split, split_x_left, y_state + box_h)
    draw_arrow(ax, split_x_right, y_split, split_x_right, y_state + box_h)
    
    # Exactly equal width and aligned tops
    draw_box(ax, cx - state_gap/2 - state_w, y_state, state_w, box_h, 
             "Personality State Update\ncumulative evidence across turns", *c['state'])
    
    draw_box(ax, cx + state_gap/2, y_state, state_w, box_h, 
             f"OCEAN Vector Output\n{phat} = (O, C, E, A, N) + confidence", *c['state'], wrap_width=28)
    
    # --- 4. INTERFACE LAYER ---
    draw_layer_label(ax, 0.6, y_interface + box_h/2, "INTERFACE\nLAYER")
    inter_w = 7.2
    
    # Merge connections
    y_merge = y_interface + box_h + 0.5
    ax.plot([split_x_left, split_x_right], [y_merge, y_merge], color='#3F3F3F', lw=1.2)
    ax.plot([split_x_left, split_x_left], [y_state, y_merge], color='#3F3F3F', lw=1.2)
    ax.plot([split_x_right, split_x_right], [y_state, y_merge], color='#3F3F3F', lw=1.2)
    draw_arrow(ax, cx, y_merge, cx, y_interface + box_h)
    
    draw_box(ax, cx - inter_w/2, y_interface, inter_w, box_h, 
             f"Interface to Regulation Module\ntransmit {phat} + confidence for behavior adaptation", *c['interface'])

    # Save
    pdf_path = OUT / "detection_pipeline_mdpi.pdf"
    png_path = OUT / "detection_pipeline_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.3, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.3, dpi=600)
    plt.close(fig)
    print(f"✓ Created final refined MDPI detection pipeline: {png_path}")

if __name__ == "__main__":
    create_detection_pipeline()
