#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Data Processing Pipeline (Figure 3)
Horizontal flow: Input -> Detection -> Mapping -> Assembly -> Generation -> Evaluation -> Log.
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
    
    # Wide layout for horizontal pipeline
    fig, ax = plt.subplots(figsize=(15, 4), dpi=600)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 4)
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
        wrap_width = 20

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


def create_data_flow_pipeline():
    """Create the MDPI data flow pipeline figure (Figure 3)."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(7.5, 3.5, 'End-to-End Data Processing Pipeline', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Color Palette (consistent with other diagrams)
    c_blue = ('#F3F9FC', '#2C5F7E')
    c_green = ('#F3FAF6', '#2E7D32')
    c_lav = ('#F7F3FC', '#5E35B1')
    
    # Layout Config
    box_w = 1.8
    box_h = 1.0
    gap = 0.3
    y_mid = 1.2
    
    steps = [
        ("1. Input", "user message\ncontext history", c_blue),
        ("2. Detection", "linguistic analysis\nOCEAN inference", c_blue),
        ("3. Mapping", "Zurich Model\ntrait-to-need", c_green),
        ("4. Assembly", "prompt logic\naugmentation", c_green),
        ("5. Generation", "GPT-4 instance\nadaptive response", c_green),
        ("6. Evaluation", "LLM-as-judge\nexpert audit", c_lav),
        ("7. Logging", "state persistence\ntraceability", c_lav)
    ]
    
    start_x = (15 - (len(steps) * box_w + (len(steps)-1) * gap)) / 2
    
    for i, (title, sub, col) in enumerate(steps):
        x = start_x + i * (box_w + gap)
        draw_box(ax, x, y_mid, box_w, box_h, f"{title}\n{sub}", *col, fontsize=9)
        if i < len(steps) - 1:
            draw_arrow(ax, x + box_w + 0.05, y_mid + box_h/2, x + box_w + gap - 0.05, y_mid + box_h/2)

    # Save
    pdf_path = OUT / "data_flow_mdpi.pdf"
    png_path = OUT / "data_flow_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.3, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.3, dpi=600)
    plt.close(fig)
    print(f"? Created refined MDPI data flow pipeline figure: {png_path}")

if __name__ == "__main__":
    create_data_flow_pipeline()
