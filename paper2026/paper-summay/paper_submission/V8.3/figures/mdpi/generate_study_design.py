#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standalone Study Design figure generator.
Produces study_design_mdpi.png in the same directory.
Does NOT depend on visualization_config.py.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

OUT = Path(__file__).resolve().parent

# ── Style constants ──────────────────────────────────────────────────────────
FONT_FAMILY   = "DejaVu Sans"
TITLE_FS      = 11
PHASE_FS      = 8.5
CONTENT_FS    = 8.5
FOOTNOTE_FS   = 7.5
ARROW_COLOR   = "#555555"
ARROW_LW      = 1.2
ANNOT_COLOR   = "#777777"
BOX_PAD       = 0.10
BOX_RADIUS    = 0.04
BOX_LW_NORMAL = 0.9
BOX_LW_BOLD   = 1.6
DPI           = 300

# Colour palette (face, edge)
C_BLUE   = ("#F7F9FF", "#555555")
C_GREEN  = ("#F7FFF9", "#555555")
C_GRAY   = ("#FBFBFB", "#555555")
C_PURPLE = ("#FAF7FF", "#AAAAAA")

plt.rcParams.update({
    "font.family":      FONT_FAMILY,
    "font.size":        CONTENT_FS,
    "axes.linewidth":   0.6,
    "figure.dpi":       DPI,
})

# ── Drawing helpers ──────────────────────────────────────────────────────────

def _setup_figure(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, figsize[0])
    ax.set_ylim(0, figsize[1])
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _draw_box(ax, x, y, w, h, text,
              facecolor="#FBFBFB", edgecolor="#555555",
              linewidth=BOX_LW_NORMAL):
    """Draw a rounded rectangle with centred multi-line text."""
    rect = mpatches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={BOX_RADIUS}",
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        zorder=2,
    )
    ax.add_patch(rect)
    lines = text.split("\n")
    n = len(lines)
    for i, line in enumerate(lines):
        vert = y + h / 2 + (n - 1 - 2 * i) / (2 * n) * h * 0.55
        bold = (i == 0 and n > 1)
        ax.text(
            x + w / 2, vert, line,
            ha="center", va="center",
            fontsize=CONTENT_FS,
            fontweight="bold" if bold else "normal",
            color="#333333",
            zorder=3,
        )


def _draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=ARROW_COLOR,
            lw=ARROW_LW,
            mutation_scale=8,
        ),
        zorder=4,
    )


def _draw_line(ax, xs, ys):
    ax.plot(xs, ys, color=ARROW_COLOR, lw=ARROW_LW,
            solid_capstyle="butt", zorder=4)


def _phase_label(ax, x, y, text):
    ax.text(x, y, text,
            ha="center", va="bottom",
            fontsize=PHASE_FS,
            fontweight="bold",
            color="#444444",
            zorder=3)


def _footnote(ax, x, y, text):
    ax.text(x, y, text,
            ha="center", va="top",
            fontsize=FOOTNOTE_FS,
            fontstyle="italic",
            color=ANNOT_COLOR,
            zorder=3)


def _bold_note(ax, x, y, text):
    ax.text(x, y, text,
            ha="center", va="top",
            fontsize=FOOTNOTE_FS,
            fontweight="bold",
            color=ANNOT_COLOR,
            zorder=3)


# ── Main figure ──────────────────────────────────────────────────────────────

def create():
    FIG_W, FIG_H = 14.0, 5.8   # taller to give breathing room
    fig, ax = _setup_figure((FIG_W, FIG_H))

    # Title
    ax.text(FIG_W / 2, FIG_H - 0.28,
            "Study Design & Experimental Workflow",
            ha="center", va="top",
            fontsize=TITLE_FS, fontweight="bold", color="#222222", zorder=3)

    # Layout geometry — more vertical space between elements
    box_w, box_h = 2.8, 0.90
    v_gap   = 0.55   # gap between top-row and bottom-row boxes
    h_gap   = 0.62
    x_start = (FIG_W - (4 * box_w + 3 * h_gap)) / 2

    # Anchor: top box sits below phase-label area
    phase_label_area = 0.42   # vertical space reserved for phase label text
    content_top = FIG_H - 0.68
    y_top = content_top - phase_label_area - box_h
    phase_label_y = y_top + box_h + 0.14   # bottom of phase-label text
    y_bot = y_top - v_gap - box_h
    # vertical midpoint between the two rows (for annotations)
    y_mid = y_top - v_gap / 2

    # ── PHASE I ──────────────────────────────────────────
    x1 = x_start
    _phase_label(ax, x1 + box_w / 2, phase_label_y, "PHASE I: CONFIGURATION")
    _draw_box(ax, x1, y_top, box_w, box_h,
              "Experimental Setup\n20 agents · random assignment",
              facecolor=C_BLUE[0], edgecolor=C_BLUE[1])
    _draw_box(ax, x1, y_bot, box_w, box_h,
              "Personality Profiles\nType A: all traits = +1\nType B: all traits = \u22121",
              facecolor=C_BLUE[0], edgecolor=C_BLUE[1])
    _footnote(ax, x1 + box_w / 2, y_bot - 0.14, "Boundary-condition simulation")
    _draw_arrow(ax, x1 + box_w / 2, y_top - BOX_PAD,
                x1 + box_w / 2, y_bot + box_h + BOX_PAD)

    # ── PHASE II ─────────────────────────────────────────
    x2 = x1 + box_w + h_gap
    _phase_label(ax, x2 + box_w / 2, phase_label_y, "PHASE II: INTERVENTION")
    # "Same LLM instance" note placed between the two rows — clear of phase label
    ax.text(x2 + box_w / 2, y_mid,
            "Same LLM instance",
            ha="center", va="center",
            fontsize=FOOTNOTE_FS, fontweight="bold",
            color=ANNOT_COLOR,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="#CCCCCC", linewidth=0.6),
            zorder=5)
    _draw_box(ax, x2, y_top, box_w, box_h,
              "Regulated Condition\nRegulation: ON",
              facecolor=C_GREEN[0], edgecolor=C_GREEN[1])
    _draw_box(ax, x2, y_bot, box_w, box_h,
              "Baseline Condition\nRegulation: OFF",
              facecolor=C_GREEN[0], edgecolor=C_GREEN[1])

    # ── PHASE III ────────────────────────────────────────
    x3 = x2 + box_w + h_gap
    _phase_label(ax, x3 + box_w / 2, phase_label_y, "PHASE III: COLLECTION")
    _draw_box(ax, x3, y_top, box_w, box_h,
              "Dialogue Protocol\n120 dialogues · 6 turns",
              facecolor=C_GRAY[0], edgecolor=C_GRAY[1])
    _draw_box(ax, x3, y_bot, box_w, box_h,
              "Evaluation\nLLM-judge · Human audit",
              facecolor=C_GRAY[0], edgecolor=C_GRAY[1])
    _draw_arrow(ax, x3 + box_w / 2, y_top - BOX_PAD,
                x3 + box_w / 2, y_bot + box_h + BOX_PAD)

    # ── PHASE IV ─────────────────────────────────────────
    x4 = x3 + box_w + h_gap
    _phase_label(ax, x4 + box_w / 2, phase_label_y, "PHASE IV: VALIDATION")
    _draw_box(ax, x4, y_top, box_w, box_h,
              "Outcome Analysis\nEffect sizes · Reliability",
              facecolor=C_PURPLE[0], edgecolor="#AAAAAA",
              linewidth=BOX_LW_NORMAL)
    _draw_box(ax, x4, y_bot, box_w, box_h,
              "Outcome Comparison\nRegulated vs Baseline",
              facecolor=C_PURPLE[0], edgecolor="#333333",
              linewidth=BOX_LW_BOLD)
    _draw_arrow(ax, x4 + box_w / 2, y_top - BOX_PAD,
                x4 + box_w / 2, y_bot + box_h + BOX_PAD)

    # ── T-junction: PHASE I → PHASE II ───────────────────
    cx1   = x1 + box_w + h_gap / 2
    mt    = y_top + box_h / 2   # mid of top row
    mb    = y_bot + box_h / 2   # mid of bottom row
    _draw_line(ax, [x1 + box_w + BOX_PAD, cx1], [mb, mb])
    _draw_line(ax, [cx1, cx1], [mt, mb])
    _draw_arrow(ax, cx1, mt, x2 - BOX_PAD, mt)
    _draw_arrow(ax, cx1, mb, x2 - BOX_PAD, mb)

    # ── T-junction: PHASE II → PHASE III ─────────────────
    cx2 = x2 + box_w + h_gap / 2
    _draw_line(ax, [x2 + box_w + BOX_PAD, cx2], [mt, mt])
    _draw_line(ax, [x2 + box_w + BOX_PAD, cx2], [mb, mb])
    _draw_line(ax, [cx2, cx2], [mt, mb])
    _draw_arrow(ax, cx2, mt, x3 - BOX_PAD, mt)

    # ── T-junction: PHASE III → PHASE IV ─────────────────
    cx3 = x3 + box_w + h_gap / 2
    _draw_line(ax, [x3 + box_w + BOX_PAD, cx3], [mt, mt])
    _draw_line(ax, [x3 + box_w + BOX_PAD, cx3], [mb, mb])
    _draw_line(ax, [cx3, cx3], [mt, mb])
    _draw_arrow(ax, cx3, mt, x4 - BOX_PAD, mt)

    ax.set_ylim(y_bot - 0.45, FIG_H)

    # ── Save ─────────────────────────────────────────────
    out_path = OUT / "study_design_mdpi.png"
    fig.savefig(str(out_path), dpi=DPI, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    create()
