"""
Generate Figure 2 - EMA Trait Convergence.

Matches Figure 1 style:
- Font: Helvetica Neue, Arial, Helvetica (same as figure1_architecture.dot)
- Font sizes: 10pt axes, 11pt title, 9pt ticks/legend (proportional to figure 1's 20-22pt)
- Margin ratio: pad=0.1, margin=0.02 (from figure1 dot)
- DPI: 300 (same as figure1_architecture.py)
- Single-column width: 3.54 in (~89 mm MDPI)
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# --- Match Figure 1 style ---
FIG1_DPI = 300
FIG1_FONT = ["Helvetica Neue", "Arial", "Helvetica", "sans-serif"]
FIG1_FONT_AXES = 10
FIG1_FONT_TITLE = 11
FIG1_FONT_TICKS = 9
FIG1_FONT_LEGEND = 9
# Figure 1: pad=0.1, margin=0.02 -> ~2% margin, 0.1 in padding
# Matplotlib equivalent: left/right/bottom/top ~0.12-0.15
FIG1_MARGIN_LEFT = 0.14
FIG1_MARGIN_RIGHT = 0.96
FIG1_MARGIN_BOTTOM = 0.14
FIG1_MARGIN_TOP = 0.94
# Single-column MDPI width
FIG_WIDTH_SINGLE = 3.54
FIG_HEIGHT = 2.8


def ema_smooth(observations, confidences, alpha_s=0.3, tau_c=0.4, prior=0.0):
    """In-session EMA with confidence gating."""
    out = [prior]
    for obs, c in zip(observations, confidences):
        if c >= tau_c:
            out.append(alpha_s * obs + (1 - alpha_s) * out[-1])
        else:
            out.append(out[-1])
    return np.array(out[1:])


def draw_figure2(out_path: Path) -> None:
    np.random.seed(42)
    turns = np.arange(1, 11)
    true_level = 0.5
    raw = true_level + np.random.randn(10) * 0.35
    raw = np.clip(raw, -1, 1)
    conf = np.clip(0.6 + np.random.randn(10) * 0.2, 0.2, 1.0)
    conf[2] = 0.25
    ema_vals = ema_smooth(raw, conf, alpha_s=0.3, tau_c=0.4, prior=0.0)

    plt.rcParams.update({
        "figure.dpi": FIG1_DPI,
        "savefig.dpi": FIG1_DPI,
        "savefig.bbox": "tight",
        "font.family": "sans-serif",
        "font.sans-serif": FIG1_FONT,
        "font.size": FIG1_FONT_TICKS,
        "axes.labelsize": FIG1_FONT_AXES,
        "axes.titlesize": FIG1_FONT_TITLE,
        "xtick.labelsize": FIG1_FONT_TICKS,
        "ytick.labelsize": FIG1_FONT_TICKS,
        "legend.fontsize": FIG1_FONT_LEGEND,
    })

    fig, ax = plt.subplots(figsize=(FIG_WIDTH_SINGLE, FIG_HEIGHT))
    fig.subplots_adjust(
        left=FIG1_MARGIN_LEFT,
        right=FIG1_MARGIN_RIGHT,
        bottom=FIG1_MARGIN_BOTTOM,
        top=FIG1_MARGIN_TOP,
    )

    # Data colors: red/blue for contrast; reference lines use figure 1 gray (#95A5A6)
    ax.plot(turns, raw, "o-", color="#E74C3C", markersize=6, label="Raw detection", alpha=0.9)
    ax.plot(turns, ema_vals, "s-", color="#2980B9", markersize=5, label="EMA-smoothed")
    ax.axhline(true_level, color="#95A5A6", linestyle="--", alpha=0.8, label="Underlying trait")
    ax.axvline(3, color="#95A5A6", linestyle=":", alpha=0.8, label="Low conf. (rejected)")

    ax.set_xlabel("Turn")
    ax.set_ylabel("Neuroticism estimate")
    ax.set_ylim(-0.2, 1.1)
    ax.legend(loc="lower right")
    ax.set_title("EMA Trait Convergence (Neuroticism)")

    plt.savefig(out_path, dpi=FIG1_DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path} (300 DPI, figure 1 style)")


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    out_dir = base_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    draw_figure2(out_dir / "figure2_ema_convergence.png")
