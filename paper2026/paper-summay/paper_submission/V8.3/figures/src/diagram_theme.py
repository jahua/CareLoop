#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared diagram theme utilities for generating consistent figures.

Features:
- Consistent sans-serif typography
- Muted, print-friendly color palette
- Rounded boxes with subtle borders
- Clear grayscale-safe arrows
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def setup_rcparams() -> None:
    """Configure matplotlib for publication-quality diagrams."""
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Inter", "Source Sans Pro", "Helvetica", "Arial", "DejaVu Sans"]


@dataclass(frozen=True)
class Theme:
    """Color palette for diagram elements."""
    blue_fill: str = "#EAF0FF"
    blue_edge: str = "#3557A4"
    green_fill: str = "#EAF7EF"
    green_edge: str = "#2F6B47"
    gray_fill: str = "#F3F5F6"
    gray_edge: str = "#6F7673"
    lav_fill: str = "#F2EDFB"
    lav_edge: str = "#6A5FA8"
    
    ink: str = "#1F1F1F"
    muted: str = "#4A4A4A"
    arrow: str = "#444444"
    frame: str = "#DADCDC"


def new_canvas(*, figsize: tuple[float, float], dpi: int = 300) -> tuple[Figure, Axes]:
    """Create a blank canvas for diagram drawing."""
    setup_rcparams()
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def title(ax: Axes, main: str, subtitle: str | None = None) -> None:
    """Add title and optional subtitle to diagram."""
    ax.text(0.5, 0.955, main, ha="center", va="center", fontsize=14, fontweight="bold", color="#1F1F1F")
    if subtitle:
        ax.text(0.5, 0.928, subtitle, ha="center", va="center", fontsize=9, fontstyle="italic", color="#4A4A4A")


def header(ax: Axes, x: float, y: float, s: str, *, size: int = 11, color: str = "#2A2A2A") -> None:
    """Add section header text."""
    ax.text(x, y, s, ha="left", va="bottom", fontsize=size, fontweight="bold", color=color)


def box(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    face: str,
    edge: str,
    lw: float = 1.4,
    rounding: float = 0.02,
) -> None:
    """Draw a rounded rectangle box."""
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


def center_text(
    ax: Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    s: str,
    *,
    size: int = 9,
    weight: str = "normal",
    color: str = "#1F1F1F",
    linespacing: float = 1.25,
) -> None:
    """Add centered text within a box."""
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


def v_arrow(ax: Axes, x: float, y0: float, y1: float, *, color: str = "#444444", lw: float = 2.0) -> None:
    """Draw a vertical arrow."""
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


def h_arrow(ax: Axes, x0: float, x1: float, y: float, *, color: str = "#444444", lw: float = 2.0) -> None:
    """Draw a horizontal arrow."""
    ax.add_patch(
        FancyArrowPatch(
            (x0, y),
            (x1, y),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
        )
    )


def frame(ax: Axes, *, pad: float = 0.02, color: str = "#DADCDC") -> None:
    """Draw a border frame around the entire diagram."""
    box(ax, pad, pad, 1 - pad * 2, 1 - pad * 2, face="white", edge=color, lw=1.0, rounding=0.015)


def save(fig: Figure, out_path: Path) -> None:
    """Save figure to file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, facecolor="white", bbox_inches='tight')
    plt.close(fig)
