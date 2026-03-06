#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Study Design & Experimental Workflow (Horizontal Layout - Final Polish)
Final visual and typographic refinements for MDPI publication quality.
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
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    
    # Wide canvas for horizontal stage flow
    fig, ax = plt.subplots(figsize=(15, 8), dpi=600)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8)
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
        wrap_width = 32

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    title_lh = 0.22
    body_lh = 0.20
    gap_h = 0.10 if body_lines else 0.0
    
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
                fontsize=fontsize-1, fontweight=fontweight,
                color=text_color, linespacing=1.1)
    return box


def draw_arrow(ax, x1, y1, x2, y2, style='solid', color='#3F3F3F', 
               linewidth=1.2, shrinkA: float = 0, shrinkB: float = 0):
    """Draw a clean orthogonal arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    color=color,
                    linewidth=linewidth,
                    linestyle='-' if style == 'solid' else '--',
                    shrinkA=shrinkA,
                    shrinkB=shrinkB,
                ))


def draw_phase_label(ax, x, y, text):
    """Draw phase header anchored closer to boxes."""
    ax.text(x, y, text, fontsize=9.5, fontweight='bold', color='#888888', 
            ha='center', va='bottom')


def create_mdpi_study_design():
    """Final polished study design figure."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(7.5, 7.5, 'Study Design & Experimental Workflow', ha='center', va='center', fontsize=15, fontweight='bold')
    ax.text(7.5, 7.1, 'Simulation-based randomized controlled design', ha='center', va='center', fontsize=10, fontstyle='italic', color='#4A4A4A')
    
    # Colors (Reduced saturation)
    c = {
        'blue': ('#F7F9FF', '#555555'),
        'green': ('#F7FFF9', '#555555'),
        'gray': ('#FBFBFB', '#555555'),
        'purple': ('#FAF7FF', '#555555'),
    }
    
    # Grid Config
    box_w = 3.0
    box_h = 1.05
    v_gap = 0.8
    h_gap = 0.7
    x_start = 0.8
    y_top = 5.0
    y_bot = y_top - box_h - v_gap
    
    # --- PHASE I: CONFIGURATION ---
    x1 = x_start
    draw_phase_label(ax, x1 + box_w/2, 6.4, "PHASE I: CONFIGURATION")
    draw_box(ax, x1, y_top, box_w, box_h, "Experimental Setup\n20 agents · random assignment", *c['blue'])
    draw_box(ax, x1, y_bot, box_w, box_h, "Personality Profiles\nType A: High-functioning\nType B: Vulnerable", *c['blue'])
    ax.text(x1 + box_w/2, y_bot - 0.22, "Boundary-condition simulation", fontsize=7.5, ha='center', fontstyle='italic', color='#777777')
    draw_arrow(ax, x1 + box_w/2, y_top, x1 + box_w/2, y_bot + box_h)
    
    # --- PHASE II: INTERVENTION ---
    x2 = x1 + box_w + h_gap
    draw_phase_label(ax, x2 + box_w/2, 6.4, "PHASE II: INTERVENTION")
    ax.text(x2 + box_w/2, 6.15, "Same LLM instance", fontsize=8, ha='center', fontweight='bold', color='#666666')
    draw_box(ax, x2, y_top, box_w, box_h, "Regulated Condition\nRegulation: ON", *c['green'])
    draw_box(ax, x2, y_bot, box_w, box_h, "Baseline Condition\nRegulation: OFF", *c['green'])
    
    # --- PHASE III: COLLECTION ---
    x3 = x2 + box_w + h_gap
    draw_phase_label(ax, x3 + box_w/2, 6.4, "PHASE III: COLLECTION")
    draw_box(ax, x3, y_top, box_w, box_h, "Dialogue Protocol\n120 dialogues · 6 turns", *c['gray'])
    draw_box(ax, x3, y_bot, box_w, box_h, "Evaluation\nLLM-judge · Human audit", *c['gray'])
    draw_arrow(ax, x3 + box_w/2, y_top, x3 + box_w/2, y_bot + box_h)
    
    # --- PHASE IV: VALIDATION ---
    x4 = x3 + box_w + h_gap
    draw_phase_label(ax, x4 + box_w/2, 6.4, "PHASE IV: VALIDATION")
    # Outcome Analysis (Lighter border)
    draw_box(ax, x4, y_top, box_w, box_h, "Outcome Analysis\nEffect sizes · Reliability", facecolor=c['purple'][0], edgecolor='#AAAAAA', linewidth=0.8)
    # Outcome Comparison (Prominent)
    draw_box(ax, x4, y_bot, box_w, box_h, "Outcome Comparison\nRegulated vs Baseline", facecolor=c['purple'][0], edgecolor='#333333', linewidth=1.6)
    draw_arrow(ax, x4 + box_w/2, y_top, x4 + box_w/2, y_bot + box_h)
    
    # --- ARROW LOGIC (T-JUNCTIONS & CONVERGENCE) ---
    # Col 1 -> Col 2 (Fork)
    cx1 = x1 + box_w + h_gap/2
    ax.plot([x1+box_w, cx1], [y_bot+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    ax.plot([cx1, cx1], [y_top+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    draw_arrow(ax, cx1, y_top+box_h/2, x2, y_top+box_h/2)
    draw_arrow(ax, cx1, y_bot+box_h/2, x2, y_bot+box_h/2)
    
    # Col 2 -> Col 3 (Convergence to shared Dialogue Protocol)
    cx2 = x2 + box_w + h_gap/2
    ax.plot([x2+box_w, cx2], [y_top+box_h/2, y_top+box_h/2], color='#3F3F3F', lw=1.2)
    ax.plot([x2+box_w, cx2], [y_bot+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    ax.plot([cx2, cx2], [y_top+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    draw_arrow(ax, cx2, y_top+box_h/2, x3, y_top+box_h/2)
    
    # Col 3 -> Col 4 (Convergence to Validation)
    cx3 = x3 + box_w + h_gap/2
    ax.plot([x3+box_w, cx3], [y_top+box_h/2, y_top+box_h/2], color='#3F3F3F', lw=1.2)
    ax.plot([x3+box_w, cx3], [y_bot+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    ax.plot([cx3, cx3], [y_top+box_h/2, y_bot+box_h/2], color='#3F3F3F', lw=1.2)
    draw_arrow(ax, cx3, y_top+box_h/2, x4, y_top+box_h/2)

    # Adjust ylim to minimize bottom white space
    # Calculate the minimum y based on content
    min_y_content = y_bot - 0.3  # Bottom of lowest box with small margin
    ax.set_ylim(min_y_content, 8)  # Keep top at 8, adjust bottom
    
    # Save with minimal padding
    pdf_path = OUT / "study_design_mdpi.pdf"
    png_path = OUT / "study_design_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.02, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.02, dpi=600)
    plt.close(fig)
    print(f"✓ Final polished MDPI study design: {png_path}")
    print(f"  - Minimal padding: 0.02 inches (reduced from 0.2)")
    print(f"  - Dynamic ylim: ({min_y_content:.2f}, 8)")

if __name__ == "__main__":
    create_mdpi_study_design()
