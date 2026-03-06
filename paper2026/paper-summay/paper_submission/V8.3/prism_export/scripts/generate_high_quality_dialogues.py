#!/usr/bin/env python3
"""
Generate high-quality dialogue illustrations with improved clarity
Uses higher DPI and better font rendering
"""

import sys
import os
from pathlib import Path
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# High-quality rendering settings
matplotlib.rcParams['figure.dpi'] = 600  # Double the DPI for sharper text
matplotlib.rcParams['savefig.dpi'] = 600
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
matplotlib.rcParams['font.size'] = 11  # Larger base font
matplotlib.rcParams['text.antialiased'] = True
matplotlib.rcParams['savefig.bbox'] = 'tight'
matplotlib.rcParams['savefig.pad_inches'] = 0.02  # Minimal padding to avoid cutting edges

# Color palette
COL = {
    "ink": "#222222",
    "muted": "#555555",
    "light": "#CCCCCC",  # Slightly darker for better visibility
    "panel": "#FFFFFF",
    "accent": "#666666",
}


def _clean_text(s: str) -> str:
    """Clean text for display."""
    if s is None:
        return ""
    try:
        if isinstance(s, float) and s != s:  # NaN
            return ""
    except:
        pass
    s = str(s)
    if s.strip().lower() == "nan":
        return ""
    s = s.replace("\n", " ").strip()
    # Remove emoji
    for ch in ["😊", "💛", "💫", "🌿", "🕊️", "🕊", "✨", "❤️", "🙏"]:
        s = s.replace(ch, "")
    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip().replace("ÔÇÉ", "–")


def create_high_quality_dialogue(title, reg_row, base_row, output_path, assistant_start):
    """
    Create high-quality dialogue comparison figure.
    Optimized for clarity and readability.
    
    Args:
        title: Figure title
        reg_row: Regulated conversation data
        base_row: Baseline conversation data
        output_path: Where to save the figure
        assistant_start: Shared assistant opening message
    """
    # Larger figure size for better clarity
    fig, ax = plt.subplots(figsize=(16, 13), dpi=600)  # Taller to fit assistant start
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    
    # Title with larger font
    ax.text(50, 98, title, fontsize=16, fontweight='bold', 
            color=COL["ink"], ha="center", va="top")
    
    # Column headers
    left_x, right_x = 5, 52.5
    col_w = 45
    top = 92
    
    ax.text(left_x + col_w/2, top, "Regulated Response", 
            fontsize=13, fontweight='bold', color=COL["muted"], ha="center", va="top")
    ax.text(right_x + col_w/2, top, "Baseline Response", 
            fontsize=13, fontweight='bold', color=COL["muted"], ha="center", va="top")
    
    # Get content
    user_msg = _clean_text(reg_row.get("USER REPLY", ""))
    reg_reply = _clean_text(reg_row.get("ASSISTANT REPLY (REG)", ""))
    base_reply = _clean_text(base_row.get("ASSISTANT REPLY", ""))
    personality = _clean_text(reg_row.get("DETECTED PERSONALITY (O,C,E,A,N)", ""))
    regulation = _clean_text(reg_row.get("REGULATION PROMPT APPLIED", ""))
    
    # SHARED: Assistant start message (across both columns)
    y = top - 5
    assist_wrapped = textwrap.fill(assistant_start, width=90)
    assist_lines = assist_wrapped.count('\n') + 1
    assist_h = 4 + assist_lines * 1.8
    
    ax.add_patch(FancyBboxPatch(
        (5, y - assist_h), 90, assist_h,
        boxstyle="round,pad=0.8", ec="#9370DB", fc="#F0E6FF", lw=1.5
    ))
    ax.text(7, y - 1.5, "Assistant Start (Shared):", fontsize=11, fontweight='bold', 
            color="#7B68EE", va="top")
    ax.text(7, y - 3.5, assist_wrapped, fontsize=11, color=COL["ink"], 
            va="top", linespacing=1.4)
    
    # SHARED: User message
    y = y - assist_h - 3
    user_wrapped = textwrap.fill(user_msg, width=90)
    user_lines = user_wrapped.count('\n') + 1
    user_h = 4 + user_lines * 1.8
    
    ax.add_patch(FancyBboxPatch(
        (5, y - user_h), 90, user_h,
        boxstyle="round,pad=0.8", ec=COL["light"], fc="#F8F8F8", lw=1.5
    ))
    ax.text(7, y - 1.5, "User Message:", fontsize=11, fontweight='bold', 
            color=COL["muted"], va="top")
    ax.text(7, y - 3.5, user_wrapped, fontsize=11, color=COL["ink"], 
            va="top", linespacing=1.4)
    
    # Response boxes (side by side)
    y = y - user_h - 4
    
    # Regulated response (LEFT)
    reg_wrapped = textwrap.fill(reg_reply, width=40)
    reg_lines = reg_wrapped.count('\n') + 1
    reg_h = 4 + reg_lines * 1.8
    
    ax.add_patch(FancyBboxPatch(
        (left_x, y - reg_h), col_w, reg_h,
        boxstyle="round,pad=0.8", ec="#0072B2", fc="#E8F4F8", lw=2.0
    ))
    ax.text(left_x + 2, y - 1.5, "Assistant Reply (Regulated):", fontsize=11, 
            fontweight='bold', color="#0072B2", va="top")
    ax.text(left_x + 2, y - 3.5, reg_wrapped, fontsize=11, color=COL["ink"], 
            va="top", linespacing=1.4)
    
    # Baseline response (RIGHT)
    base_wrapped = textwrap.fill(base_reply, width=40)
    base_lines = base_wrapped.count('\n') + 1
    base_h = 4 + base_lines * 1.8
    
    ax.add_patch(FancyBboxPatch(
        (right_x, y - base_h), col_w, base_h,
        boxstyle="round,pad=0.8", ec="#E69F00", fc="#FFF8E8", lw=2.0
    ))
    ax.text(right_x + 2, y - 1.5, "Assistant Reply (Baseline):", fontsize=11, 
            fontweight='bold', color="#E69F00", va="top")
    ax.text(right_x + 2, y - 3.5, base_wrapped, fontsize=11, color=COL["ink"], 
            va="top", linespacing=1.4)
    
    # Metadata section (ONLY for regulated - left side)
    y = y - max(reg_h, base_h) - 4
    
    # Personality detection (left)
    pers_wrapped = textwrap.fill(personality, width=35)
    pers_lines = pers_wrapped.count('\n') + 1
    pers_h = 3.5 + pers_lines * 1.6
    
    ax.add_patch(FancyBboxPatch(
        (left_x, y - pers_h), col_w * 0.48, pers_h,
        boxstyle="round,pad=0.6", ec=COL["light"], fc="#FAFAFA", lw=1.2
    ))
    ax.text(left_x + 1.5, y - 1.2, "Detected Personality:", fontsize=10, 
            fontweight='bold', color=COL["muted"], va="top")
    ax.text(left_x + 1.5, y - 2.8, pers_wrapped, fontsize=10, color=COL["ink"], 
            va="top", linespacing=1.3)
    
    # Regulation prompt (right of personality detection, still in left column)
    reg_wrapped_meta = textwrap.fill(regulation, width=35)
    reg_lines_meta = reg_wrapped_meta.count('\n') + 1
    reg_h_meta = 3.5 + reg_lines_meta * 1.6
    
    ax.add_patch(FancyBboxPatch(
        (left_x + col_w * 0.52, y - reg_h_meta), col_w * 0.48, reg_h_meta,
        boxstyle="round,pad=0.6", ec=COL["light"], fc="#FAFAFA", lw=1.2
    ))
    ax.text(left_x + col_w * 0.52 + 1.5, y - 1.2, "Regulation Applied:", 
            fontsize=10, fontweight='bold', color=COL["muted"], va="top")
    ax.text(left_x + col_w * 0.52 + 1.5, y - 2.8, reg_wrapped_meta, 
            fontsize=10, color=COL["ink"], va="top", linespacing=1.3)
    
    # Calculate the actual minimum y position (bottom of the lowest element)
    min_y = y - max(pers_h, reg_h_meta)
    
    # Adjust ylim to eliminate white space at bottom
    # Keep a small margin (1 unit) below the lowest element
    ax.set_ylim(min_y - 1, 100)
    
    # Save with high quality and minimal padding
    plt.savefig(output_path, facecolor="white", dpi=600, bbox_inches='tight', 
                pad_inches=0.02, format='png', pil_kwargs={'optimize': True})
    plt.close()
    print(f"✓ Saved high-quality dialogue: {output_path}")


def main():
    """Generate high-quality dialogue illustrations."""
    print("="*80)
    print("HIGH-QUALITY DIALOGUE ILLUSTRATION GENERATION")
    print("="*80)
    print("\nSettings:")
    print("  DPI: 600 (2x higher than before)")
    print("  Font size: 10-16 pt (larger)")
    print("  Line width: 1.5-2.0 pt (thicker)")
    print("  Antialiasing: Enabled\n")
    
    # Load data
    data_dir = 'data/merged'
    reg_candidates = [
        os.path.join(data_dir, 'regulated.csv'),
        'data/merged/regulated.csv',
    ]
    base_candidates = [
        os.path.join(data_dir, 'baseline.csv'),
        'data/merged/baseline.csv',
    ]
    
    reg_path = next((p for p in reg_candidates if os.path.exists(p)), None)
    base_path = next((p for p in base_candidates if os.path.exists(p)), None)
    
    if not reg_path or not base_path:
        print("⚠️  Data files not found")
        return
    
    print(f"Loading data from:")
    print(f"  Regulated: {reg_path}")
    print(f"  Baseline: {base_path}\n")
    
    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)
    
    def get_row(msg_no: str):
        reg_row = df_reg[df_reg["MSG. NO."].astype(str) == msg_no]
        base_row = df_base[df_base["MSG. NO."].astype(str) == msg_no]
        if reg_row.empty or base_row.empty:
            return None, None
        return reg_row.iloc[0].to_dict(), base_row.iloc[0].to_dict()
    
    output_dir = 'figures'
    os.makedirs(output_dir, exist_ok=True)
    
    # Figure 15: Type B (Vulnerable)
    print("[1/2] Generating Figure 15 (Type B - Vulnerable, High Quality)...")
    rr_b, rb_b = get_row("B-4-1")
    if rr_b and rb_b:
        create_high_quality_dialogue(
            title="Type B (Vulnerable Profile): Regulated vs Baseline Comparison",
            reg_row=rr_b,
            base_row=rb_b,
            output_path=os.path.join(output_dir, "dialogue_illustration_1_hq.png"),
            assistant_start="How are you feeling today? If there's anything on your mind, I'm here to listen."
        )
    
    # Figure 16: Type A (High-functioning)
    print("[2/2] Generating Figure 16 (Type A - High-functioning, High Quality)...")
    rr_a, rb_a = get_row("A-5-3")
    if rr_a and rb_a:
        create_high_quality_dialogue(
            title="Type A (High-functioning Profile): Regulated vs Baseline Comparison",
            reg_row=rr_a,
            base_row=rb_a,
            output_path=os.path.join(output_dir, "dialogue_illustration_2_hq.png"),
            assistant_start="I'm here to help you. How are you feeling today?"
        )
    
    print("\n" + "="*80)
    print("HIGH-QUALITY GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  ✓ figures/dialogue_illustration_1_hq.png (600 DPI)")
    print("  ✓ figures/dialogue_illustration_2_hq.png (600 DPI)")
    print("\nImprovements:")
    print("  • 2x higher DPI (600 vs 300)")
    print("  • Larger font sizes (10-16 pt vs 8-12 pt)")
    print("  • Thicker borders (1.5-2.0 pt vs 0.9-1.0 pt)")
    print("  • Better text antialiasing")
    print("  • Optimized PNG compression")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
