#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Evaluation Framework & Scoring Pipeline (Figure 7)
Layout: Criteria (Regulated vs Baseline) -> Scoring Scale -> Evaluation Process -> Outcome.
Fixed overlaps and improved spacing for journal publication.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import textwrap
from typing import List, Optional

# Output directory (save in the same directory as script)
OUT = Path(__file__).resolve().parent


def setup_figure():
    """Create figure with MDPI-appropriate settings."""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['font.size'] = 9
    
    # Vertical layout for evaluation framework
    fig, ax = plt.subplots(figsize=(10, 14), dpi=600)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
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
             linewidth=1.2, fontsize=9.5, fontweight='normal', text_color='#000000',
             bold_title=True, wrap_width: Optional[int] = None, pad: float = 0.06):
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
        wrap_width = 18 # Reduced default wrap width for better containment

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    title_lh = 0.22
    body_fs = max(7.5, fontsize - 1.5)
    body_lh = 0.18
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
                fontsize=body_fs, fontweight=fontweight,
                color=text_color, linespacing=1.1, fontstyle='italic')
    return box


def draw_arrow(ax, x1, y1, x2, y2, style='solid', color='#3F3F3F', 
               linewidth=1.2, shrinkA: float = 0, shrinkB: float = 0):
    """Draw a clean orthogonal arrow."""
    linestyle = '-' if style == 'solid' else '--'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    color=color,
                    linewidth=linewidth,
                    linestyle=linestyle,
                    shrinkA=shrinkA,
                    shrinkB=shrinkB,
                    connectionstyle="arc3,rad=0"
                ))


def draw_section_header(ax, x, y, text):
    """Draw a bold section header."""
    ax.text(x, y, text, fontsize=11, fontweight='bold', color='#333333', ha='center', va='center')


def create_evaluation_framework():
    """Create the MDPI evaluation framework figure (Figure 7)."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(5, 13.5, 'Evaluation Framework: Criteria, Scoring, and Process', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Colors
    c_blue = ('#F3F9FC', '#2C5F7E')
    c_orange = ('#FFF9F3', '#B68B3A')
    c_green = ('#F3FFF3', '#2E7D32')
    c_lav = ('#F7F3FC', '#5E35B1')
    
    cx = 5.0
    dot = "\u00b7"
    
    # --- PHASE I: EVALUATION CRITERIA ---
    draw_section_header(ax, cx, 12.8, "PHASE I: EVALUATION CRITERIA")
    
    # 1. Regulated Row
    ax.text(cx, 12.3, "Regulated Condition (5 Criteria)", fontsize=9.5, fontweight='bold', ha='center', color=c_blue[1])
    
    y_reg = 11.0
    crit_h = 1.0
    crit_w = 1.6
    gap_x = 0.25
    
    reg_crit = [
        ("Detection\nAccuracy", "trait inference\nfidelity"),
        ("Regulation\nEffectiveness", "instruction\nalignment"),
        ("Emotional\nTone", f"warmth {dot} safety\nsupport"),
        ("Relevance &\nCoherence", "logical flow\ncontext"),
        ("Personality\nNeeds", "trait-specific\nadaptation")
    ]
    
    # Center the row of 5
    total_w_reg = 5 * crit_w + 4 * gap_x
    start_x_reg = cx - total_w_reg / 2
    
    for i, (title, sub) in enumerate(reg_crit):
        draw_box(ax, start_x_reg + i*(crit_w+gap_x), y_reg, crit_w, crit_h, f"{title}\n{sub}", *c_blue, fontsize=8.5)

    # 2. Baseline Row (separated by vertical gap)
    y_base = 9.2
    ax.text(cx, 10.5, "Baseline Condition (3 Criteria)", fontsize=9.5, fontweight='bold', ha='center', color=c_orange[1])
    
    base_crit = [
        ("Emotional\nTone", "general warmth\nsupport"),
        ("Relevance &\nCoherence", "logical flow\ncontext"),
        ("Personality\nNeeds", "non-adaptive\nsupport")
    ]
    
    # Center the row of 3
    total_w_base = 3 * crit_w + 2 * gap_x
    start_x_base = cx - total_w_base / 2
    
    for i, (title, sub) in enumerate(base_crit):
        draw_box(ax, start_x_base + i*(crit_w+gap_x), y_base, crit_w, crit_h, f"{title}\n{sub}", *c_orange, fontsize=8.5)

    # --- PHASE II: SCORING SCALE ---
    draw_section_header(ax, cx, 8.2, "PHASE II: SCORING SCALE (Ternary)")
    
    y_scale = 7.0
    scale_w = 2.8
    scale_h = 0.85
    gap_s = 0.4
    
    scale_items = [
        ("YES (2)", "Strong alignment\nclear evidence", c_green),
        ("NOT SURE (1)", "Partial alignment\nambiguous case", c_orange),
        ("NO (0)", "Clear misalignment\ncriterion not met", c_lav)
    ]
    
    # Center the row of 3
    total_w_scale = 3 * scale_w + 2 * gap_s
    start_x_scale = cx - total_w_scale / 2
    
    for i, (title, sub, col) in enumerate(scale_items):
        draw_box(ax, start_x_scale + i*(scale_w+gap_s), y_scale, scale_w, scale_h, f"{title}\n{sub}", *col)

    # --- PHASE III: EVALUATION PROCESS ---
    draw_section_header(ax, cx, 5.8, "PHASE III: EVALUATION PROCESS")
    
    y_proc = 4.4
    proc_w = 2.8
    proc_h = 1.0
    gap_p = 0.6
    
    proc_items = [
        ("1. AI Evaluation", "Evaluator GPT scores\nall 120 turns"),
        ("2. Human Audit", "Single domain expert\nqualitative review"),
        ("3. Statistical Analysis", f"Effect sizes {dot} CI\nreliability analysis")
    ]
    
    # Center the row of 3
    total_w_proc = 3 * proc_w + 2 * gap_p
    start_x_proc = cx - total_w_proc / 2
    
    for i, (title, sub) in enumerate(proc_items):
        x_box = start_x_proc + i*(proc_w+gap_p)
        draw_box(ax, x_box, y_proc, proc_w, proc_h, f"{title}\n{sub}", *c_blue)
        if i < 2:
            # Arrow between boxes
            arrow_start_x = x_box + proc_w + 0.05
            arrow_end_x = x_box + proc_w + gap_p - 0.05
            draw_arrow(ax, arrow_start_x, y_proc + proc_h/2, arrow_end_x, y_proc + proc_h/2)

    # --- FINAL OUTCOME ---
    draw_section_header(ax, cx, 3.0, "SYSTEM VALIDATION OUTCOME")
    
    outcome_txt = (
        "Implementation Fidelity & Selective Enhancement\n"
        "Technical Verification: 100% detection and regulation fidelity confirmed.\n"
        "Comparative Finding: Personality needs addressed significantly better in regulated condition (d = 4.65).\n"
        "Quality Retention: Generic quality (tone, relevance) maintained at ceiling level."
    )
    # Spans full width
    draw_box(ax, 0.5, 0.8, 9.0, 1.8, outcome_txt, *c_green, wrap_width=80, pad=0.1)

    # Save
    pdf_path = OUT / "evaluation_framework_mdpi.pdf"
    png_path = OUT / "evaluation_framework_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.3, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.3, dpi=600)
    plt.close(fig)
    print(f"✓ Created refined MDPI evaluation framework figure: {png_path}")

if __name__ == "__main__":
    create_evaluation_framework()
