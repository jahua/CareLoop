#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Study Design & Experimental Workflow (journal-ready)

Recreates the original study-design flowchart with:
- strict alignment grid + improved spacing
- muted, print-friendly, higher-contrast colors by category
- consistent sans-serif typography
- thicker/darker arrows (grayscale-safe)

Output:
  statistical analyis/figures/11_study_design_flowchart.png
"""

from __future__ import annotations

from pathlib import Path
import shutil
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


OUT_DIR = Path(__file__).resolve().parent / "figures"
OUT_PATH = OUT_DIR / "11_study_design_flowchart.png"
SUBMISSION_DIR = Path(__file__).resolve().parents[1] / "complete_submission"
SUBMISSION_PATH = SUBMISSION_DIR / "Figure_01_Study_Design.png"


def setup_rcparams() -> None:
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Inter", "Source Sans Pro", "Helvetica", "Arial", "DejaVu Sans"]


def box(ax, x, y, w, h, *, face, edge, lw=1.4, rounding=0.02) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0.012,rounding_size={rounding}",
            facecolor=face,
            edgecolor=edge,
            linewidth=lw,
        )
    )


def header(ax, x, y, s, *, size=11, color="#2A2A2A") -> None:
    ax.text(x, y, s, ha="left", va="bottom", fontsize=size, fontweight="bold", color=color)


def center_text(ax, x, y, w, h, s, *, size=9, weight="normal", color="#1F1F1F", linespacing=1.25) -> None:
    ax.text(
        x + w / 2,
        y + h / 2,
        s,
        ha="center",
        va="center",
        fontsize=size,
        fontweight=weight,
        color=color,
        linespacing=linespacing,
    )


def v_arrow(ax, x, y0, y1, *, color="#444444", lw=2.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x, y0),
            (x, y1),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )


def h_arrow(ax, x0, x1, y, *, color="#444444", lw=1.7) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x0, y),
            (x1, y),
            arrowstyle="<->",
            mutation_scale=12,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    setup_rcparams()

    fig = plt.figure(figsize=(7.6, 10.8), dpi=300, facecolor="white")
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Category palette (muted but readable in print)
    blue_fill, blue_edge = "#EAF0FF", "#3557A4"   # setup & profiles
    green_fill, green_edge = "#EAF7EF", "#2F6B47" # conditions
    gray_fill, gray_edge = "#F3F5F6", "#6F7673"   # dialogues & evaluation
    lav_fill, lav_edge = "#F2EDFB", "#6A5FA8"     # stats & key finding

    # Title
    ax.text(0.5, 0.965, "Study Design & Experimental Workflow", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#1F1F1F")
    ax.text(0.5, 0.94, "(Simulation-Based Randomized Controlled Design)", ha="center", va="center",
            fontsize=9, fontstyle="italic", color="#4A4A4A")

    # Grid
    left, right = 0.08, 0.92
    center = 0.5
    gutter = 0.04
    y = 0.88

    # Heights
    # NOTE: these values are tuned so the full diagram fits inside y in [0, 1]
    # without clipping (previously STATISTICAL ANALYSIS was cut off at bottom).
    h_setup = 0.07
    h_pair = 0.09
    h_dialogues = 0.10
    h_eval = 0.085
    h_stats = 0.10
    h_key = 0.06
    gap_after_arrow = 0.045
    header_pad = 0.010

    # STUDY SETUP
    header(ax, left, y, "STUDY SETUP")
    y -= header_pad + h_setup
    box(ax, left, y, right - left, h_setup, face=blue_fill, edge=blue_edge)
    center_text(
        ax, left, y, right - left, h_setup,
        "20 Agent Instances\n(10 per personality type)\nType A: High-functioning\nType B: Vulnerable",
        size=9, linespacing=1.28
    )
    v_arrow(ax, center, y - 0.008, y - 0.03)
    y -= gap_after_arrow

    # PERSONALITY PROFILES
    header(ax, left, y, "PERSONALITY PROFILES")
    y -= header_pad + h_pair
    w = (right - left - gutter) / 2
    xL = left
    xR = left + w + gutter
    box(ax, xL, y, w, h_pair, face=blue_fill, edge=blue_edge)
    box(ax, xR, y, w, h_pair, face=blue_fill, edge=blue_edge)
    center_text(ax, xL, y, w, h_pair, "Type A\n(High-Functioning)\n\nO=+1, C=+1\nE=+1, A=+1, N=+1",
                size=9, weight="bold", linespacing=1.22)
    center_text(ax, xR, y, w, h_pair, "Type B\n(Vulnerable)\n\nO=-1, C=-1\nE=-1, A=-1, N=-1",
                size=9, weight="bold", linespacing=1.22)
    h_arrow(ax, xL + w + 0.01, xR - 0.01, y + h_pair * 0.5)
    v_arrow(ax, center, y - 0.008, y - 0.03)
    y -= gap_after_arrow

    # CONDITIONS
    header(ax, left, y, "CONDITIONS")
    y -= header_pad + h_pair
    box(ax, xL, y, w, h_pair, face=green_fill, edge=green_edge)
    box(ax, xR, y, w, h_pair, face=green_fill, edge=green_edge)
    center_text(ax, xL, y, w, h_pair, "Regulated\nCondition\n\n5 Agents per type\nPersonality detection\n+ ZM regulation",
                size=9, weight="bold", linespacing=1.22)
    center_text(ax, xR, y, w, h_pair, "Baseline\nCondition\n\n5 Agents per type\nStatic supportive\nresponses",
                size=9, weight="bold", linespacing=1.22)
    h_arrow(ax, xL + w + 0.01, xR - 0.01, y + h_pair * 0.5)
    v_arrow(ax, center, y - 0.008, y - 0.03)
    y -= gap_after_arrow

    # DIALOGUES
    header(ax, left, y, "DIALOGUES")
    y -= header_pad + h_dialogues
    box(ax, left, y, right - left, h_dialogues, face=gray_fill, edge=gray_edge)
    center_text(
        ax, left, y, right - left, h_dialogues,
        "120 Total Dialogues (6-turn structure)\n\n10 agents x 2 personality types x 6 turns = 120 turns\nRandom assignment to conditions\nControlled dialogue structure for consistency",
        size=9, linespacing=1.28
    )
    v_arrow(ax, center, y - 0.008, y - 0.03)
    y -= gap_after_arrow

    # EVALUATION
    header(ax, left, y, "EVALUATION")
    y -= header_pad + h_eval
    w2 = (right - left - gutter) / 2
    xEL = left
    xER = left + w2 + gutter
    box(ax, xEL, y, w2, h_eval, face=gray_fill, edge=gray_edge)
    box(ax, xER, y, w2, h_eval, face=gray_fill, edge=gray_edge)
    center_text(ax, xEL, y, w2, h_eval, "AI Evaluation\n\nAll 120 turns\nEvaluator GPT\n5 criteria (Y/NS/N)",
                size=9, weight="bold", linespacing=1.22)
    center_text(ax, xER, y, w2, h_eval, "Human Validation\n\n30 turns (25%)\n2 PhD experts\nBlinded evaluation",
                size=9, weight="bold", linespacing=1.22)
    h_arrow(ax, xEL + w2 + 0.01, xER - 0.01, y + h_eval * 0.5)
    ax.text(center, y + h_eval * 0.12, "k=0.89", ha="center", va="center", fontsize=8, color="#4A4A4A")
    v_arrow(ax, center, y - 0.008, y - 0.03)
    y -= gap_after_arrow

    # STATISTICAL ANALYSIS
    header(ax, left, y, "STATISTICAL ANALYSIS")
    y -= header_pad + h_stats
    box(ax, left, y, right - left, h_stats, face=lav_fill, edge=lav_edge)
    center_text(
        ax, left, y, right - left, h_stats,
        "Descriptive Statistics & Effect Sizes\nMean, SD, Confidence Intervals (95%)\nCohen's d (effect size)\nCriterion-specific analysis (5 metrics)\nReliability analysis (alpha, k, IRR)",
        size=9, linespacing=1.28
    )
    # Place KEY FINDING below with a clear gap (avoid border overlap).
    y_stats_bottom = y
    v_arrow(ax, center, y_stats_bottom - 0.008, y_stats_bottom - 0.032)

    gap_between_boxes = 0.045  # vertical whitespace between the two rounded boxes
    y = y_stats_bottom - gap_between_boxes - h_key

    # KEY FINDING
    box(ax, left, y, right - left, h_key, face=lav_fill, edge=lav_edge)
    center_text(ax, left, y, right - left, h_key, "Key Finding: Personality Adaptation Effect (d=4.58, p<0.001)",
                size=9, weight="bold", linespacing=1.2)

    fig.savefig(OUT_PATH, dpi=300, facecolor="white")
    shutil.copyfile(OUT_PATH, SUBMISSION_PATH)
    plt.close(fig)
    print(f"Created: {OUT_PATH}")
    print(f"Updated: {SUBMISSION_PATH}")


if __name__ == "__main__":
    main()

