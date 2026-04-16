#!/usr/bin/env python3
"""
Unified Figure Generation Script
=================================
Generates ALL publication figures from a single entry point:

  Section A: MDPI system/architecture diagrams  (Figures 1-7)
  Section B: Statistical analysis plots          (Figures 8-14)
  Section C: Dialogue illustrations              (Figures 15-16)

Uses unified style configuration from visualization_config.py to ensure
consistent fonts, sizes, spacing, and colors across all figures.

Usage:
    python generate_all_figures.py              # generate everything
    python generate_all_figures.py --mdpi       # only system diagrams
    python generate_all_figures.py --stats      # only statistical plots
    python generate_all_figures.py --dialogue   # only dialogue illustrations
"""

import sys
import os
import argparse
import textwrap
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Ensure we can import from this directory
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from visualization_config import (
    PUBLICATION_CONFIG as C,
    DIAGRAM_STYLE as DS,
    configure_matplotlib,
)
from enhanced_statistical_analysis import (
    load_and_prepare_data,
    convert_to_numeric,
    calculate_descriptive_statistics,
    calculate_effect_sizes,
    visualize_results,
    visualize_data_quality,
    analyze_personality_vectors,
    visualize_personality_vectors,
    analyze_weighted_scores,
    visualize_weighted_scores,
    visualize_selective_enhancement,
    visualize_data_quality_enhanced,
    perform_advanced_statistical_tests,
    perform_reliability_analysis,
)

# MDPI diagram scripts
MDPI_DIR = SCRIPT_DIR.parent / "figures" / "mdpi"
FIGURES_DIR = SCRIPT_DIR.parent / "figures"


# =========================================================================
# SECTION A: MDPI System/Architecture Diagrams (Figures 1-7)
# =========================================================================

def generate_mdpi_diagrams():
    """Generate all MDPI system diagrams using unified DiagramStyle."""
    print("\n" + "=" * 80)
    print("SECTION A: MDPI SYSTEM DIAGRAMS (Figures 1-7)")
    print("=" * 80)

    sys.path.insert(0, str(MDPI_DIR))

    scripts = [
        ("create_mdpi_study_design",        "create_mdpi_study_design",      "Fig 1"),
        ("create_mdpi_architecture",        "create_mdpi_architecture",      "Fig 2"),
        ("create_mdpi_data_flow",           "create_data_flow_pipeline",     "Fig 3"),
        ("create_mdpi_detection_pipeline",  "create_detection_pipeline",     "Fig 4"),
        ("create_mdpi_trait_mapping",       "create_trait_mapping",          "Fig 5"),
        ("create_mdpi_regulation_workflow", "create_regulation_workflow",    "Fig 6"),
        ("create_mdpi_evaluation_framework","create_evaluation_framework",   "Fig 7"),
    ]

    for module_name, func_name, label in scripts:
        print(f"\n  [{label}] {module_name}...")
        try:
            mod = __import__(module_name)
            fn = getattr(mod, func_name)
            fn()
        except Exception as e:
            print(f"    ERROR: {e}")

    print("\n  Section A complete.")


# =========================================================================
# SECTION B: Statistical Analysis Plots (Figures 8-14)
# =========================================================================

def generate_statistical_figures(data_dir: str, output_dir: str):
    """Generate all statistical analysis figures."""
    print("\n" + "=" * 80)
    print("SECTION B: STATISTICAL ANALYSIS PLOTS (Figures 8-14)")
    print("=" * 80)

    configure_matplotlib(use_matplotlib_papers_defaults=True)

    reg_path = os.path.join(data_dir, "regulated.csv")
    base_path = os.path.join(data_dir, "baseline.csv")

    if not os.path.exists(reg_path) or not os.path.exists(base_path):
        print(f"  Data not found at {data_dir}")
        return

    print("  [1/8] Loading data...")
    df_reg, df_base = load_and_prepare_data(reg_path, base_path)

    print("  [2/8] Data quality visualizations...")
    visualize_data_quality_enhanced(df_reg, df_base, output_dir=output_dir)

    print("  [3/8] Converting to numeric...")
    df_reg_num, df_base_num = convert_to_numeric(df_reg, df_base)

    print("  [4/8] Descriptive statistics & effect sizes...")
    df_stats = calculate_descriptive_statistics(df_reg_num, df_base_num)
    df_effects = calculate_effect_sizes(df_reg_num, df_base_num)

    print("  [5/8] Results visualizations...")
    visualize_results(df_stats, df_effects, output_dir=output_dir)

    print("  [6/8] Personality vector analysis...")
    df_valid = analyze_personality_vectors(df_reg)
    if df_valid is not None:
        visualize_personality_vectors(df_valid, output_dir=output_dir)

    print("  [7/8] Weighted scores...")
    df_reg_scored, df_base_scored = analyze_weighted_scores(df_reg, df_base)
    visualize_weighted_scores(df_reg_scored, df_base_scored, output_dir=output_dir)

    print("  [8/8] Selective enhancement & composition...")
    visualize_selective_enhancement(df_reg, df_base, output_dir=output_dir)

    print("\n  Section B complete.")
    return df_reg_scored, df_base_scored


# =========================================================================
# SECTION C: Dialogue Illustrations (Figures 15-16)
# =========================================================================

COL = {
    "ink": "#222222",
    "muted": "#555555",
    "light": "#EAEAEA",
    "panel": "#FFFFFF",
    "accent": "#666666",
}


def _clean_text(s):
    if s is None:
        return ""
    try:
        if isinstance(s, float) and s != s:
            return ""
    except Exception:
        pass
    s = str(s)
    if s.strip().lower() == "nan":
        return ""
    s = s.replace("\n", " ").strip()
    for ch in ["\U0001f60a", "\U0001f49b", "\U0001f4ab", "\U0001f33f",
               "\U0001f54a\ufe0f", "\U0001f54a", "\u2728", "\u2764\ufe0f", "\U0001f64f"]:
        s = s.replace(ch, "")
    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip()


def _fix_mojibake(s):
    return s.replace("\u00d4\u00c7\u00c9", "\u2013")


def _wrap_cell(s, width):
    s = _fix_mojibake(_clean_text(s))
    return textwrap.fill(s, width=width)


def _bubble(ax, x, y_top, w, text, who, field_label, align="left",
            fontsize=9.2, fc="#FFFFFF"):
    wrapped = _wrap_cell(text, max(44, int(w * 1.05)))
    lines = wrapped.count("\n") + 1
    h = 6.8 + lines * 2.35
    bx = x if align == "left" else x - w
    by = y_top - h

    ax.add_patch(FancyBboxPatch(
        (bx, by), w, h,
        boxstyle="round,pad=0.75,rounding_size=2.0",
        ec=COL["light"], fc=fc, lw=1.0))

    tag_w = min(w - 3.2, max(18.0, len(field_label) * 0.95))
    ax.add_patch(FancyBboxPatch(
        (bx + 1.2, y_top - 3.6), tag_w, 2.6,
        boxstyle="round,pad=0.25,rounding_size=1.0",
        ec=COL["light"], fc="#F5F5F5", lw=0.8))
    ax.text(bx + 2.0, y_top - 2.3, field_label,
            fontsize=7.4, fontweight="bold", color=COL["muted"], va="center")
    ax.text(bx + 1.6, y_top - 5.0, who,
            fontsize=8.2, fontweight="bold", color=COL["muted"], va="top")
    ax.text(bx + 1.6, y_top - 7.6, wrapped,
            fontsize=fontsize, color=COL["ink"], va="top", linespacing=1.18)
    return h


def _meta_card(ax, x, y_top, w, title, body, fontsize=8.1):
    body_wrapped = _wrap_cell(body, max(40, int(w * 1.00)))
    lines = body_wrapped.count("\n") + 1
    h = 4.8 + lines * 2.15
    ax.add_patch(FancyBboxPatch(
        (x, y_top - h), w, h,
        boxstyle="round,pad=0.6,rounding_size=1.6",
        ec=COL["light"], fc="#FAFAFA", lw=0.9))
    ax.text(x + 1.2, y_top - 1.6, title,
            fontsize=8.3, fontweight="bold", color=COL["muted"], va="top")
    ax.text(x + 1.2, y_top - 3.9, body_wrapped,
            fontsize=fontsize, color=COL["ink"], va="top", linespacing=1.18)
    return h


def create_dialogue_figure(title, reg_row, base_row, output_path):
    fig, ax = plt.subplots(figsize=(12.8, 9.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 120)
    ax.axis("off")
    ax.text(0, 118, title, fontsize=12.6, fontweight="bold",
            color=COL["ink"], ha="left", va="top")

    left_x, right_x = 4, 52
    col_w = 44
    top = 110
    ax.text(left_x, top, "Regulated", fontsize=10.5, fontweight="bold",
            color=COL["muted"], va="top")
    ax.text(right_x, top, "Baseline", fontsize=10.5, fontweight="bold",
            color=COL["muted"], va="top")

    reg_start = reg_row.get("ASSISTANT START", "")
    reg_user = reg_row.get("USER REPLY", "")
    reg_reply = reg_row.get("ASSISTANT REPLY (REG)", "")
    det = str(reg_row.get("DETECTED PERSONALITY (O,C,E,A,N)", ""))
    prompt = str(reg_row.get("REGULATION PROMPT APPLIED", ""))
    base_start = base_row.get("ASSISTANT START", "")
    base_user = base_row.get("USER REPLY", "")
    base_reply = base_row.get("ASSISTANT REPLY", "")

    y = top - 6
    if _clean_text(reg_start):
        y -= _bubble(ax, left_x + 2, y, w=col_w * 0.82, text=reg_start,
                     who="Assistant", field_label="ASSISTANT START",
                     align="left", fc="#FAFAFA")
        y -= 2.2
    y -= _bubble(ax, left_x + col_w - 1.2, y, w=col_w * 0.94, text=reg_user,
                 who="User", field_label="USER REPLY", align="right",
                 fontsize=9.0)
    y -= 2.2
    y -= _bubble(ax, left_x + 2, y, w=col_w * 0.94, text=reg_reply,
                 who="Assistant", field_label="ASSISTANT REPLY (REG)",
                 align="left", fontsize=9.0)
    y -= 2.4

    meta_top = min(y, 30)
    _meta_card(ax, left_x + 2, meta_top, w=col_w * 0.52,
               title="Detected personality (O,C,E,A,N)", body=det)
    _meta_card(ax, left_x + 2 + col_w * 0.54, meta_top, w=col_w * 0.44,
               title="Regulation prompt applied", body=prompt, fontsize=7.8)

    yb = top - 6
    if _clean_text(base_start):
        yb -= _bubble(ax, right_x + 2, yb, w=col_w * 0.82, text=base_start,
                      who="Assistant", field_label="ASSISTANT START (BASE)",
                      align="left", fc="#FAFAFA")
        yb -= 2.2
    yb -= _bubble(ax, right_x + col_w - 1.2, yb, w=col_w * 0.94,
                  text=base_user, who="User", field_label="USER REPLY (BASE)",
                  align="right", fontsize=9.0)
    yb -= 2.2
    _bubble(ax, right_x + 2, yb, w=col_w * 0.94, text=base_reply,
            who="Assistant", field_label="ASSISTANT REPLY (BASE)",
            align="left", fontsize=9.0)

    plt.savefig(output_path, facecolor="white", dpi=300)
    plt.close()
    print(f"    Saved: {output_path}")


def generate_dialogue_illustrations(data_dir: str, output_dir: str):
    """Generate dialogue comparison figures (Figures 15-16)."""
    print("\n" + "=" * 80)
    print("SECTION C: DIALOGUE ILLUSTRATIONS (Figures 15-16)")
    print("=" * 80)

    reg_path = os.path.join(data_dir, "regulated.csv")
    base_path = os.path.join(data_dir, "baseline.csv")

    if not os.path.exists(reg_path) or not os.path.exists(base_path):
        print(f"  Data not found at {data_dir}")
        return

    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)

    def get_row(msg_no):
        rr = df_reg[df_reg["MSG. NO."].astype(str) == msg_no]
        rb = df_base[df_base["MSG. NO."].astype(str) == msg_no]
        if rr.empty or rb.empty:
            return None, None
        return rr.iloc[0].to_dict(), rb.iloc[0].to_dict()

    print("  [Fig 15] Type B (Vulnerable)...")
    rr_b, rb_b = get_row("B-4-1")
    if rr_b and rb_b:
        create_dialogue_figure(
            "Personality Type B Example (Low OCEAN): Regulated vs Baseline",
            rr_b, rb_b, os.path.join(output_dir, "dialogue_illustration_1.png"))

    print("  [Fig 16] Type A (High-functioning)...")
    rr_a, rb_a = get_row("A-5-3")
    if rr_a and rb_a:
        create_dialogue_figure(
            "Personality Type A Example (High OCEAN): Regulated vs Baseline",
            rr_a, rb_a, os.path.join(output_dir, "dialogue_illustration_2.png"))

    print("\n  Section C complete.")


# =========================================================================
# MAIN
# =========================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate all publication figures")
    parser.add_argument("--mdpi", action="store_true", help="Only MDPI diagrams")
    parser.add_argument("--stats", action="store_true", help="Only statistical plots")
    parser.add_argument("--dialogue", action="store_true", help="Only dialogue illustrations")
    args = parser.parse_args()

    run_all = not (args.mdpi or args.stats or args.dialogue)

    os.chdir(SCRIPT_DIR)
    data_dir = str(SCRIPT_DIR / "merged")
    output_dir = str(FIGURES_DIR)
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("UNIFIED FIGURE GENERATION")
    print("=" * 80)
    print(f"  Script dir:  {SCRIPT_DIR}")
    print(f"  Data dir:    {data_dir}")
    print(f"  Output dir:  {output_dir}")
    print(f"  MDPI dir:    {MDPI_DIR}")
    print(f"  DiagramStyle title: {DS.TITLE_FONTSIZE}pt, "
          f"content: {DS.CONTENT_FONTSIZE}pt, "
          f"body: {DS.CONTENT_BODY_FONTSIZE}pt, "
          f"DPI: {DS.DPI}")

    if run_all or args.mdpi:
        generate_mdpi_diagrams()

    if run_all or args.stats:
        generate_statistical_figures(data_dir, output_dir)

    if run_all or args.dialogue:
        generate_dialogue_illustrations(data_dir, output_dir)

    print("\n" + "=" * 80)
    print("ALL DONE")
    print("=" * 80)


if __name__ == "__main__":
    main()
