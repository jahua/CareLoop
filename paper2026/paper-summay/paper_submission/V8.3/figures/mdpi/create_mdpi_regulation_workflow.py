#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Regulation & Prompt Assembly Workflow (Refined Figure 15)
Strict horizontal flow: Detection -> Mapping -> Selection -> Harmonization -> Assembly -> Generation.
Audit logging branches below the final assembly stage.
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
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    
    # Wide layout for horizontal workflow
    fig, ax = plt.subplots(figsize=(15, 6), dpi=600)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 6)
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
        wrap_width = 25

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    title_lh = 0.22
    body_fs = max(8.0, fontsize - 1.5)
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
        # Check if text is the conflict example to italicize it
        is_example = "vs." in body_text or "e.g." in body_text
        ax.text(cx, y_body_center, body_text, ha="center", va="center",
                fontsize=body_fs, fontweight=fontweight,
                color=text_color, linespacing=1.1, fontstyle='italic' if is_example else 'normal')
    return box


def draw_arrow(ax, x1, y1, x2, y2, style='solid', color='#3F3F3F', 
               linewidth=1.2, shrinkA: float = 0, shrinkB: float = 0, label=''):
    """Draw a clean orthogonal or direct arrow."""
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
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.1, label, fontsize=8, ha='center', va='bottom', fontweight='normal')


def create_regulation_workflow():
    """Create the refined MDPI regulation workflow figure (Figure 15)."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(7.5, 5.5, 'Zurich Model–Aligned Regulation and Prompt Assembly', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Colors (MDPI-grade desaturated green palette)
    c = ('#F3FAF6', '#2E7D32') 
    
    dot = "\u00b7"
    phat = r"$\hat{P}$"
    
    # Layout Config
    box_w = 2.1
    box_h = 1.05
    gap = 0.35
    y_mid = 2.8
    
    # --- Sequence (Left to Right) ---
    x_start = 0.4
    
    # 1. Detection
    b1 = draw_box(ax, x_start, y_mid, box_w, box_h, f"Detected Personality\n{phat} = (O, C, E, A, N)", *c)
    
    # 2. Mapping
    x = x_start + box_w + gap
    b2 = draw_box(ax, x, y_mid, box_w, box_h, f"Map Traits to Needs\nSecurity {dot} Arousal {dot} Affiliation", *c)
    draw_arrow(ax, x-gap, y_mid+box_h/2, x, y_mid+box_h/2)
    
    # 3. Selection
    x += box_w + gap
    b3 = draw_box(ax, x, y_mid, box_w, box_h, "Select Trait Prompts\nselect non-neutral traits", *c)
    draw_arrow(ax, x-gap, y_mid+box_h/2, x, y_mid+box_h/2)
    
    # 4. Harmonization
    x += box_w + gap
    b4 = draw_box(ax, x, y_mid, box_w, box_h, "Harmonize Conflicts\ne.g., High O vs. Low E", *c)
    draw_arrow(ax, x-gap, y_mid+box_h/2, x, y_mid+box_h/2)
    
    # 5. Assembly
    x += box_w + gap
    b5 = draw_box(ax, x, y_mid, box_w, box_h, "Assemble Regulation Prompt\nsingle consolidated instruction block", *c)
    draw_arrow(ax, x-gap, y_mid+box_h/2, x, y_mid+box_h/2)
    
    # 6. Generation (Final Output in Main Flow)
    x_final = x + box_w + gap
    b6 = draw_box(ax, x_final, y_mid, box_w, box_h, "Response Generation\n(Assistant Reply)", *c)
    draw_arrow(ax, x_final-gap, y_mid+box_h/2, x_final, y_mid+box_h/2)
    
    # --- Branching Audit Log (Below Main Flow) ---
    # Centered under Response Generation for vertical alignment
    y_log = y_mid - box_h - 0.8
    b_log = draw_box(ax, x_final, y_log, box_w, box_h, "Audit Logging\nlog prompts + decisions", *c)
    
    # Orthogonal Dashed Arrow from Assembly to Log
    ax.plot([x + box_w/2, x + box_w/2, x_final], [y_mid, y_log + box_h/2, y_log + box_h/2], 
            color='#3F3F3F', linestyle='--', linewidth=1.2)
    draw_arrow(ax, x + box_w/2, y_log + box_h/2, x_final, y_log + box_h/2, style='dashed', label='log')

    # Save
    pdf_path = OUT / "regulation_workflow_mdpi.pdf"
    png_path = OUT / "regulation_workflow_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.3, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.3, dpi=600)
    plt.close(fig)
    print(f"✓ Created refined MDPI regulation workflow figure: {png_path}")

if __name__ == "__main__":
    create_regulation_workflow()
