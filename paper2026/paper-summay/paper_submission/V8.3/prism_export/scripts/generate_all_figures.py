#!/usr/bin/env python3
"""
Complete Figure Generation Script
Generates all publication figures including dialogue illustrations

IMPORTANT: Uses Cliff's delta (NOT Cohen's d) for effect sizes
"""

import sys
import os
from pathlib import Path
import textwrap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_statistical_analysis import (
    load_and_prepare_data,
    convert_to_numeric,
    calculate_descriptive_statistics,
    calculate_effect_sizes,  # Uses Cliff's delta, NOT Cohen's d
    visualize_results,
    analyze_weighted_scores,
    visualize_weighted_scores,
)

# =============================================================================
# DIALOGUE ILLUSTRATION GENERATION
# =============================================================================

# MDPI-friendly figure defaults
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.unicode_minus": False,
})

# Color palette
COL = {
    "ink": "#222222",
    "muted": "#555555",
    "light": "#EAEAEA",
    "panel": "#FFFFFF",
    "accent": "#666666",
}


def _wrap(s: str, width: int) -> str:
    """Wrap text to specified width."""
    return textwrap.fill(s, width=width)


def _clean_text(s: str) -> str:
    """Clean text for figure display."""
    if s is None:
        return ""
    try:
        if isinstance(s, float) and s != s:  # NaN check
            return ""
    except Exception:
        pass
    s = str(s)
    if s.strip().lower() == "nan":
        return ""
    s = s.replace("\n", " ").strip()
    # Remove emoji
    for ch in ["😊", "💛", "💫", "🌿", "🕊️", "🕊", "✨", "❤️", "🙏"]:
        s = s.replace(ch, "")
    # Collapse whitespace
    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip()


def _fix_mojibake(s: str) -> str:
    """Fix common encoding artifacts."""
    return s.replace("ÔÇÉ", "–")


def _wrap_cell(s: str, width: int) -> str:
    """Wrap cell content."""
    s = _fix_mojibake(_clean_text(s))
    return textwrap.fill(s, width=width)


def _bubble(ax, x, y_top, w, text, who, field_label, align="left", fontsize=9.2, fc="#FFFFFF"):
    """Draw a chat bubble."""
    wrapped = _wrap_cell(text, max(44, int(w * 1.05)))
    lines = wrapped.count("\n") + 1
    h = 6.8 + lines * 2.35
    bx = x if align == "left" else x - w
    by = y_top - h
    
    ax.add_patch(
        FancyBboxPatch(
            (bx, by),
            w,
            h,
            boxstyle="round,pad=0.75,rounding_size=2.0",
            ec=COL["light"],
            fc=fc,
            lw=1.0,
        )
    )
    
    # Field tag
    tag_w = min(w - 3.2, max(18.0, len(field_label) * 0.95))
    ax.add_patch(
        FancyBboxPatch(
            (bx + 1.2, y_top - 3.6),
            tag_w,
            2.6,
            boxstyle="round,pad=0.25,rounding_size=1.0",
            ec=COL["light"],
            fc="#F5F5F5",
            lw=0.8,
        )
    )
    ax.text(bx + 2.0, y_top - 2.3, field_label, fontsize=7.4, fontweight="bold", color=COL["muted"], va="center")
    
    # Speaker and content
    ax.text(bx + 1.6, y_top - 5.0, who, fontsize=8.2, fontweight="bold", color=COL["muted"], va="top")
    ax.text(bx + 1.6, y_top - 7.6, wrapped, fontsize=fontsize, color=COL["ink"], va="top", linespacing=1.18)
    return h


def _meta_card(ax, x, y_top, w, title, body, fontsize=8.1):
    """Draw a metadata card."""
    body_wrapped = _wrap_cell(body, max(40, int(w * 1.00)))
    lines = body_wrapped.count("\n") + 1
    h = 4.8 + lines * 2.15
    ax.add_patch(
        FancyBboxPatch(
            (x, y_top - h),
            w,
            h,
            boxstyle="round,pad=0.6,rounding_size=1.6",
            ec=COL["light"],
            fc="#FAFAFA",
            lw=0.9,
        )
    )
    ax.text(x + 1.2, y_top - 1.6, title, fontsize=8.3, fontweight="bold", color=COL["muted"], va="top")
    ax.text(x + 1.2, y_top - 3.9, body_wrapped, fontsize=fontsize, color=COL["ink"], va="top", linespacing=1.18)
    return h


def create_dialogue_figure(title, reg_row, base_row, output_path):
    """Create dialogue comparison figure (Figures 15 & 16)."""
    fig, ax = plt.subplots(figsize=(12.8, 9.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis("off")
    
    ax.text(0, 118, title, fontsize=12.6, fontweight="bold", color=COL["ink"], ha="left", va="top")
    
    # Split screen columns
    left_x, right_x = 4, 52
    col_w = 44
    top = 110
    
    ax.text(left_x, top, "Regulated", fontsize=10.5, fontweight="bold", color=COL["muted"], va="top")
    ax.text(right_x, top, "Baseline", fontsize=10.5, fontweight="bold", color=COL["muted"], va="top")
    
    # Pull content
    reg_start = reg_row.get("ASSISTANT START", "")
    reg_user = reg_row.get("USER REPLY", "")
    reg_reply = reg_row.get("ASSISTANT REPLY (REG)", "")
    det = str(reg_row.get("DETECTED PERSONALITY (O,C,E,A,N)", ""))
    prompt = str(reg_row.get("REGULATION PROMPT APPLIED", ""))
    
    base_start = base_row.get("ASSISTANT START", "")
    base_user = base_row.get("USER REPLY", "")
    base_reply = base_row.get("ASSISTANT REPLY", "")
    
    # Regulated conversation
    y = top - 6
    if _clean_text(reg_start):
        y -= _bubble(ax, left_x + 2, y, w=col_w * 0.82, text=reg_start, who="Assistant", 
                    field_label="ASSISTANT START", align="left", fc="#FAFAFA")
        y -= 2.2
    y -= _bubble(ax, left_x + col_w - 1.2, y, w=col_w * 0.94, text=reg_user, who="User", 
                field_label="USER REPLY", align="right", fc="#FFFFFF", fontsize=9.0)
    y -= 2.2
    y -= _bubble(ax, left_x + 2, y, w=col_w * 0.94, text=reg_reply, who="Assistant", 
                field_label="ASSISTANT REPLY (REG)", align="left", fc="#FFFFFF", fontsize=9.0)
    y -= 2.4
    
    # Metadata cards
    meta_top = min(y, 30)
    _meta_card(ax, left_x + 2, meta_top, w=col_w * 0.52, title="Detected personality (O,C,E,A,N)", body=det)
    _meta_card(ax, left_x + 2 + col_w * 0.54, meta_top, w=col_w * 0.44, title="Regulation prompt applied", 
              body=prompt, fontsize=7.8)
    
    # Baseline conversation
    yb = top - 6
    if _clean_text(base_start):
        yb -= _bubble(ax, right_x + 2, yb, w=col_w * 0.82, text=base_start, who="Assistant", 
                     field_label="ASSISTANT START (BASE)", align="left", fc="#FAFAFA")
        yb -= 2.2
    yb -= _bubble(ax, right_x + col_w - 1.2, yb, w=col_w * 0.94, text=base_user, who="User", 
                 field_label="USER REPLY (BASE)", align="right", fc="#FFFFFF", fontsize=9.0)
    yb -= 2.2
    _bubble(ax, right_x + 2, yb, w=col_w * 0.94, text=base_reply, who="Assistant", 
           field_label="ASSISTANT REPLY (BASE)", align="left", fc="#FFFFFF", fontsize=9.0)
    
    plt.savefig(output_path, facecolor="white", dpi=300)
    plt.close()
    print(f"✓ Saved dialogue figure: {output_path}")


# =============================================================================
# MAIN GENERATION SCRIPT
# =============================================================================

def generate_statistical_figures(data_dir='data/merged', output_dir='figures'):
    """
    Generate statistical analysis figures.
    
    IMPORTANT: Uses Cliff's delta for effect sizes (NOT Cohen's d).
    Cohen's d is inappropriate for bounded ordinal data.
    """
    print("="*80)
    print("STATISTICAL FIGURES GENERATION")
    print("="*80)
    print(f"\n⚠️  Using Cliff's delta (NOT Cohen's d) for effect sizes")
    print(f"   Reason: Data is bounded, ordinal, with ceiling effects\n")
    
    # Load data
    reg_path = os.path.join(data_dir, 'regulated.csv')
    base_path = os.path.join(data_dir, 'baseline.csv')
    
    print("[1/5] Loading data...")
    df_regulated, df_baseline = load_and_prepare_data(reg_path, base_path)
    
    print("\n[2/5] Converting to numeric...")
    df_reg_numeric, df_base_numeric = convert_to_numeric(df_regulated, df_baseline)
    
    print("\n[3/5] Calculating descriptive statistics...")
    df_stats = calculate_descriptive_statistics(df_reg_numeric, df_base_numeric)
    
    print("\n[4/5] Calculating effect sizes (Cliff's delta)...")
    df_effects = calculate_effect_sizes(df_reg_numeric, df_base_numeric)
    
    # Verify Cliff's delta is being used
    if 'Cliffs_delta' in df_effects.columns:
        print("✓ Confirmed: Using Cliff's delta")
        print(f"  Effect sizes: {df_effects['Cliffs_delta'].tolist()}")
    else:
        print("⚠️  WARNING: Cliff's delta not found in results!")
    
    print("\n[5/5] Generating visualizations...")
    visualize_results(df_stats, df_effects, output_dir=output_dir)
    
    # Also generate weighted scores
    df_reg_scored, df_base_scored = analyze_weighted_scores(df_regulated, df_baseline)
    visualize_weighted_scores(df_reg_scored, df_base_scored, output_dir=output_dir)
    
    print("✓ Statistical figures complete")


def generate_dialogue_illustrations(data_dir='data/merged', output_dir='figures'):
    """Generate dialogue comparison figures (Figures 15 & 16)."""
    print("\n" + "="*80)
    print("DIALOGUE ILLUSTRATION GENERATION")
    print("="*80)
    
    # Try multiple possible data locations
    reg_candidates = [
        os.path.join(data_dir, 'regulated.csv'),
        'data/merged/regulated.csv',
        '../data/merged/regulated.csv',
    ]
    base_candidates = [
        os.path.join(data_dir, 'baseline.csv'),
        'data/merged/baseline.csv',
        '../data/merged/baseline.csv',
    ]
    
    reg_path = next((p for p in reg_candidates if os.path.exists(p)), None)
    base_path = next((p for p in base_candidates if os.path.exists(p)), None)
    
    if not reg_path or not base_path:
        print(f"⚠️  Data files not found. Tried:")
        print(f"   Regulated: {reg_candidates}")
        print(f"   Baseline: {base_candidates}")
        print(f"⚠️  Skipping dialogue illustrations")
        return
    
    print(f"Loading data from:")
    print(f"  Regulated: {reg_path}")
    print(f"  Baseline: {base_path}")
    
    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)
    
    def get_row(msg_no: str):
        """Get regulated and baseline rows for a message."""
        reg_row = df_reg[df_reg["MSG. NO."].astype(str) == msg_no]
        base_row = df_base[df_base["MSG. NO."].astype(str) == msg_no]
        if reg_row.empty or base_row.empty:
            return None, None
        return reg_row.iloc[0].to_dict(), base_row.iloc[0].to_dict()
    
    # Figure 15: Type B (Vulnerable) - Example from conversation B-4-1
    print("\n[1/2] Generating Figure 15 (Type B - Vulnerable)...")
    rr_b, rb_b = get_row("B-4-1")
    if rr_b and rb_b:
        create_dialogue_figure(
            title="Personality Type B Example (Low OCEAN): Regulated vs Baseline Dialogue Excerpt",
            reg_row=rr_b,
            base_row=rb_b,
            output_path=os.path.join(output_dir, "dialogue_illustration_1.png"),
        )
    else:
        print("⚠️  B-4-1 not found in data")
    
    # Figure 16: Type A (High-functioning) - Example from conversation A-5-3
    print("\n[2/2] Generating Figure 16 (Type A - High-functioning)...")
    rr_a, rb_a = get_row("A-5-3")
    if rr_a and rb_a:
        create_dialogue_figure(
            title="Personality Type A Example (High OCEAN): Regulated vs Baseline Dialogue Excerpt",
            reg_row=rr_a,
            base_row=rb_a,
            output_path=os.path.join(output_dir, "dialogue_illustration_2.png"),
        )
    else:
        print("⚠️  A-5-3 not found in data")
    
    print("✓ Dialogue illustrations complete")


def main():
    """Generate all publication figures."""
    print("="*80)
    print("COMPLETE FIGURE GENERATION SCRIPT")
    print("="*80)
    print("\n⚠️  IMPORTANT: This script uses Cliff's delta (NOT Cohen's d)")
    print("   Cohen's d is inappropriate for bounded ordinal data\n")
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Create output directory
    output_dir = 'figures'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate all figures
    try:
        generate_statistical_figures(data_dir='data/merged', output_dir=output_dir)
    except Exception as e:
        print(f"⚠️  Error generating statistical figures: {e}")
    
    try:
        generate_dialogue_illustrations(data_dir='data/merged', output_dir=output_dir)
    except Exception as e:
        print(f"⚠️  Error generating dialogue illustrations: {e}")
    
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)
    print(f"\nGenerated figures in: {output_dir}/")
    print("\nNote: System architecture diagrams (mdpi/*.png) are")
    print("      typically created with diagram tools (draw.io, etc.)")
    print("      and are not auto-generated from data.")


if __name__ == "__main__":
    main()
