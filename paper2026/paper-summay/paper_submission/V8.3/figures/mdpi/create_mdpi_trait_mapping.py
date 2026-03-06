#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Mapping of Big Five Traits to Zurich Model Domains.
Horizontal flow: Inputs (Traits) -> Domains (Needs) -> Outputs (Effects).
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
    
    # Wide layout for mapping
    fig, ax = plt.subplots(figsize=(12, 8), dpi=600)
    ax.set_xlim(0, 12)
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
        wrap_width = 30

    title_lines = _wrap_preserving_newlines(raw_title, width=wrap_width)
    body_lines = _wrap_preserving_newlines(raw_body, width=wrap_width) if raw_body else []

    title_lh = 0.22
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
                fontsize=fontsize-1.5, fontweight=fontweight,
                color=text_color, linespacing=1.1, fontstyle='italic')
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='#3F3F3F', linewidth=1.2, shrinkA: float = 0, shrinkB: float = 0):
    """Draw a clean orthogonal or direct arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    color=color,
                    linewidth=linewidth,
                    linestyle='-',
                    shrinkA=shrinkA,
                    shrinkB=shrinkB,
                    connectionstyle="arc3,rad=0"
                ))


def create_trait_mapping():
    """Create the MDPI trait mapping figure."""
    fig, ax = setup_figure()
    
    # Title
    ax.text(6, 7.5, 'Mapping Big Five Traits to Zurich Model Domains and Behavioral Effects', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Colors
    c = {
        'trait': ('#FFF9F3', '#8B4513'),    # Light orange/brown
        'domain': ('#F3F3FF', '#00008B'),   # Light blue
        'effect': ('#F3FFF3', '#006400'),   # Light green
        'label': ('#EAEAEA', '#555555')
    }
    
    dot = "\u00b7"
    
    # Layout Config
    col1_x = 0.8
    col2_x = 4.2
    col3_x = 8.2
    
    box_w_traits = 2.4
    box_w_domains = 3.2
    box_w_effects = 3.4
    box_h = 0.85
    
    # Y positions for each row (5 traits, 4 domains, 4 effects)
    # Rows are aligned by domain
    y_security = 5.8
    y_affiliation = 4.4
    y_structure = 3.0
    y_arousal = 1.6
    
    # Trait Y positions
    y_n = y_security
    y_a = y_affiliation
    y_c = y_structure
    y_e = y_arousal + 0.35
    y_o = y_arousal - 0.35

    # --- Column Labels ---
    label_y = 6.9
    ax.text(col1_x + box_w_traits/2, label_y, "Big Five Traits\n(Inputs)", ha='center', fontweight='bold', fontsize=11)
    ax.text(col2_x + box_w_domains/2, label_y, "Zurich Model Domains\n(Needs)", ha='center', fontweight='bold', fontsize=11)
    ax.text(col3_x + box_w_effects/2, label_y, "Behavioral Effects\n(Outputs)", ha='center', fontweight='bold', fontsize=11)

    # --- TRAITS (Inputs) ---
    b_n = draw_box(ax, col1_x, y_n, box_w_traits, box_h, "Neuroticism (N)\nEmotional stability", *c['trait'])
    b_a = draw_box(ax, col1_x, y_a, box_w_traits, box_h, "Agreeableness (A)", *c['trait'])
    b_c = draw_box(ax, col1_x, y_c, box_w_traits, box_h, "Conscientiousness (C)", *c['trait'])
    b_e = draw_box(ax, col1_x, y_e, box_w_traits, box_h, "Extraversion (E)", *c['trait'])
    b_o = draw_box(ax, col1_x, y_o, box_w_traits, box_h, "Openness (O)", *c['trait'])
    
    # --- DOMAINS (Needs) ---
    b_sec = draw_box(ax, col2_x, y_security, box_w_domains, box_h, f"Security\nreassurance {dot} comfort", *c['domain'])
    b_aff = draw_box(ax, col2_x, y_affiliation, box_w_domains, box_h, f"Affiliation\nwarmth {dot} proximity", *c['domain'])
    b_str = draw_box(ax, col2_x, y_structure, box_w_domains, box_h, f"Structure\nguidance {dot} pacing", *c['domain'])
    b_aro = draw_box(ax, col2_x, y_arousal, box_w_domains, box_h, f"Arousal\nnovelty {dot} stimulation", *c['domain'])
    
    # --- EFFECTS (Outputs) ---
    b_eff1 = draw_box(ax, col3_x, y_security, box_w_effects, box_h, f"Reassurance & Comfort\nreduce threat {dot} support", *c['effect'])
    b_eff2 = draw_box(ax, col3_x, y_affiliation, box_w_effects, box_h, f"Warmth & Collaboration\nempathic {dot} neutral stance", *c['effect'])
    b_eff3 = draw_box(ax, col3_x, y_structure, box_w_effects, box_h, f"Structure & Pacing\norganized {dot} flexible", *c['effect'])
    b_eff4 = draw_box(ax, col3_x, y_arousal, box_w_effects, box_h, f"Novelty & Stimulation\nexploration {dot} familiarity", *c['effect'])

    # --- ARROWS (Traits -> Domains) ---
    draw_arrow(ax, col1_x + box_w_traits, y_n + box_h/2, col2_x, y_security + box_h/2)
    draw_arrow(ax, col1_x + box_w_traits, y_a + box_h/2, col2_x, y_affiliation + box_h/2)
    draw_arrow(ax, col1_x + box_w_traits, y_c + box_h/2, col2_x, y_structure + box_h/2)
    draw_arrow(ax, col1_x + box_w_traits, y_e + box_h/2, col2_x, y_arousal + box_h/2)
    draw_arrow(ax, col1_x + box_w_traits, y_o + box_h/2, col2_x, y_arousal + box_h/2)
    
    # --- ARROWS (Domains -> Effects) ---
    draw_arrow(ax, col2_x + box_w_domains, y_security + box_h/2, col3_x, y_security + box_h/2)
    draw_arrow(ax, col2_x + box_w_domains, y_affiliation + box_h/2, col3_x, y_affiliation + box_h/2)
    draw_arrow(ax, col2_x + box_w_domains, y_structure + box_h/2, col3_x, y_structure + box_h/2)
    draw_arrow(ax, col2_x + box_w_domains, y_arousal + box_h/2, col3_x, y_arousal + box_h/2)

    # Background column containers (subtle)
    for x_pos, w_pos in [(col1_x-0.3, box_w_traits+0.6), (col2_x-0.3, box_w_domains+0.6), (col3_x-0.3, box_w_effects+0.6)]:
        rect = mpatches.FancyBboxPatch((x_pos, 0.5), w_pos, 6.8, boxstyle="round,pad=0.1", 
                                       facecolor='#F9F9F9', edgecolor='#DDDDDD', linewidth=0.8, alpha=0.5, zorder=-1)
        ax.add_patch(rect)

    # Save
    pdf_path = OUT / "trait_mapping_mdpi.pdf"
    png_path = OUT / "trait_mapping_mdpi.png"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', pad_inches=0.3, dpi=600)
    fig.savefig(png_path, format='png', bbox_inches='tight', pad_inches=0.3, dpi=600)
    plt.close(fig)
    print(f"? Created MDPI trait mapping figure: {png_path}")

if __name__ == "__main__":
    create_trait_mapping()
