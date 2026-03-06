#!/usr/bin/env python3
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

# MDPI-friendly figure defaults (clean, minimal)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.unicode_minus": False,
})

# Soft grayscale + subtle accents (kept consistent with earlier figures)
COL = {
    "ink": "#222222",
    "muted": "#555555",
    "light": "#EAEAEA",
    "panel": "#FFFFFF",
    # Keep accents extremely subtle (MDPI/journal style)
    "accent_d": "#666666",  # Detection
    "accent_r": "#666666",  # Regulation
    "accent_e": "#666666",  # Evaluation
}


def _wrap(s: str, width: int) -> str:
    return textwrap.fill(s, width=width)

def _clean_text(s: str) -> str:
    """Light cleanup for figure typography while keeping dataset wording."""
    if s is None:
        return ""
    # Pandas NaN
    try:
        if isinstance(s, float) and s != s:  # NaN check
            return ""
    except Exception:
        pass
    s = str(s)
    if s.strip().lower() == "nan":
        return ""
    s = s.replace("\n", " ").strip()
    # Remove common emoji characters to match MDPI print conventions
    for ch in ["😊", "💛", "💫", "🌿", "🕊️", "🕊", "✨", "❤️", "🙏"] :
        s = s.replace(ch, "")
    # Collapse whitespace
    while "  " in s:
        s = s.replace("  ", " ")
    return s.strip()

def _fix_mojibake(s: str) -> str:
    # Fix common encoding artifact seen in the dataset export
    return s.replace("ÔÇÉ", "–")

def _wrap_cell(s: str, width: int) -> str:
    s = _fix_mojibake(_clean_text(s))
    return textwrap.fill(s, width=width)

def _load_example_turns():
    """
    Pull two representative turns from the merged dataset, aligned with Section 4.5:
    - Type B (vulnerable): B-1-2
    - Type A (high-functioning): A-1-3

    Returns:
      dict with keys:
        fig15_user, fig15_reg, fig15_base,
        fig16_user, fig16_reg, fig16_base
    """
    candidates_reg = [
        Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/V8.3/statistical analyis/merged/regulated.csv"),
        Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/statistical analyis/merged/regulated.csv"),
    ]
    candidates_base = [
        Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/V8.3/statistical analyis/merged/baseline.csv"),
        Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/statistical analyis/merged/baseline.csv"),
    ]

    reg_path = next((p for p in candidates_reg if p.exists()), None)
    base_path = next((p for p in candidates_base if p.exists()), None)
    if not reg_path or not base_path:
        return None

    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)

    user_col = "USER REPLY"
    reg_col = "ASSISTANT REPLY (REG)"
    base_col = "ASSISTANT REPLY"

    def pick(msg_no: str):
        row_r = df_reg[df_reg["MSG. NO."].astype(str) == msg_no]
        row_b = df_base[df_base["MSG. NO."].astype(str) == msg_no]
        if row_r.empty or row_b.empty:
            return None
        rr = row_r.iloc[0]
        rb = row_b.iloc[0]

        user = _fix_mojibake(_clean_text(rr.get(user_col, "")))
        reg = _fix_mojibake(_clean_text(rr.get(reg_col, "")))
        base = _fix_mojibake(_clean_text(rb.get(base_col, "")))
        return user, reg, base

    # Match thesis Section 6.1 qualitative examples
    b = pick("B-4-1")
    a = pick("A-5-3")

    if not b or not a:
        return None

    return {
        "fig15_user": b[0],
        "fig15_reg": b[1],
        "fig15_base": b[2],
        "fig16_user": a[0],
        "fig16_reg": a[1],
        "fig16_base": a[2],
    }


def _module_chip(ax, x, y, w, h, text):
    """Small, light module label (low visual weight)."""
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.45,rounding_size=1.6",
            ec=COL["light"],
            fc="#FFFFFF",
            lw=0.9,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        _wrap(text, 30),
        ha="center",
        va="center",
        fontsize=9.0,
        color=COL["muted"],
    )

def _bubble(ax, x, y_top, w, text, who, field_label, align="left", fontsize=9.2, fc="#FFFFFF"):
    """Chat bubble with a small 'column' label tag. y_top is the top edge. Returns bubble height."""
    # Wider wrapping to reduce line count (prevents vertical overflow)
    wrapped = _wrap_cell(text, max(44, int(w * 1.05)))
    lines = wrapped.count("\n") + 1
    # Slightly tighter line-height to fit long excerpts
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

    # Field tag (e.g., ASSISTANT START / USER REPLY / ASSISTANT REPLY (REG))
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

    # Speaker (kept small; the field tag carries the main structure)
    ax.text(bx + 1.6, y_top - 5.0, who, fontsize=8.2, fontweight="bold", color=COL["muted"], va="top")
    ax.text(bx + 1.6, y_top - 7.6, wrapped, fontsize=fontsize, color=COL["ink"], va="top", linespacing=1.18)
    return h

def _meta_card(ax, x, y_top, w, title, body, fontsize=8.1):
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

def _draw_table(
    ax,
    col_labels,
    row_values,
    wrap_widths,
    col_fracs,
    header_color="#BFE7E5",
    body_color="#DDEFD0",
    edge="#2F74B5",
    fontsize=7.2,
):
    ax.axis("off")
    wrapped = [_wrap_cell(v, wrap_widths[i]) for i, v in enumerate(row_values)]
    max_lines = max((t.count("\n") + 1) for t in wrapped) if wrapped else 1
    table = ax.table(
        cellText=[wrapped],
        colLabels=col_labels,
        cellLoc="center",
        colLoc="center",
        loc="center",
        edges="closed",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)

    # Style cells
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(edge)
        cell.set_linewidth(1.0)
        if r == 0:
            cell.set_facecolor(header_color)
            cell.get_text().set_fontweight("bold")
        else:
            cell.set_facecolor(body_color)
        cell.get_text().set_color("#111111")
        cell.get_text().set_va("center")
        cell.get_text().set_ha("center")

    # Set consistent column widths (prevents cramped columns / overflow)
    ncols = len(col_labels)
    for c in range(ncols):
        frac = col_fracs[c] if c < len(col_fracs) else (1.0 / ncols)
        for r in range(0, 2):  # header + one body row
            key = (r, c)
            if key in table.get_celld():
                table.get_celld()[key].set_width(frac)

    # Scale row height based on how many wrapped lines exist
    yscale = max(2.8, min(8.0, 1.2 + 0.38 * max_lines))
    table.scale(1.0, yscale)
    return table


def _arrow(ax, x1, y1, x2, y2, color, label=None, label_pos=0.5):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", lw=0.9, color=color, shrinkA=0, shrinkB=0),
        zorder=0,
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos
        ly = y1 + (y2 - y1) * label_pos
        ax.text(lx, ly + 2.0, label, fontsize=8.2, color=COL["muted"], ha="center", va="bottom")

def create_qualitative_chat_figure(title, reg_row, base_row, output_path):
    """Conversational UI (not a table) with full text + metadata for regulated branch."""
    # Taller canvas to prevent overlap for long Type A content
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

    # Regulated conversation (assistant start -> user -> assistant regulated)
    y = top - 6
    if _clean_text(reg_start):
        y -= _bubble(ax, left_x + 2, y, w=col_w * 0.82, text=reg_start, who="Assistant", field_label="ASSISTANT START", align="left", fc="#FAFAFA")
        y -= 2.2
    # Make long user text wrap less by using wider bubble
    y -= _bubble(ax, left_x + col_w - 1.2, y, w=col_w * 0.94, text=reg_user, who="User", field_label="USER REPLY", align="right", fc="#FFFFFF", fontsize=9.0)
    y -= 2.2
    y -= _bubble(ax, left_x + 2, y, w=col_w * 0.94, text=reg_reply, who="Assistant", field_label="ASSISTANT REPLY (REG)", align="left", fc="#FFFFFF", fontsize=9.0)
    y -= 2.4

    # Metadata cards (kept small, below the chat)
    # IMPORTANT: meta cards must be BELOW bubbles -> use <= y (never above it)
    meta_top = min(y, 30)
    _meta_card(ax, left_x + 2, meta_top, w=col_w * 0.52, title="Detected personality (O,C,E,A,N)", body=det)
    _meta_card(ax, left_x + 2 + col_w * 0.54, meta_top, w=col_w * 0.44, title="Regulation prompt applied", body=prompt, fontsize=7.8)

    # Baseline conversation (assistant start -> user -> assistant baseline)
    yb = top - 6
    if _clean_text(base_start):
        yb -= _bubble(ax, right_x + 2, yb, w=col_w * 0.82, text=base_start, who="Assistant", field_label="ASSISTANT START (BASE)", align="left", fc="#FAFAFA")
        yb -= 2.2
    yb -= _bubble(ax, right_x + col_w - 1.2, yb, w=col_w * 0.94, text=base_user, who="User", field_label="USER REPLY (BASE)", align="right", fc="#FFFFFF", fontsize=9.0)
    yb -= 2.2
    _bubble(ax, right_x + 2, yb, w=col_w * 0.94, text=base_reply, who="Assistant", field_label="ASSISTANT REPLY (BASE)", align="left", fc="#FFFFFF", fontsize=9.0)

    plt.savefig(output_path, facecolor="white", dpi=300)
    plt.close()
    print(f"✓ Saved qualitative chat figure: {output_path}")


def create_qualitative_table_figure(title, reg_row, base_row, output_path, variant="B"):
    """
    Create thesis-style qualitative illustration with full columns.
    variant:
      - 'B': shows regulated 5-col table + baseline 3-col table
      - 'A': shows regulated 4-col table + baseline 2-col table
    """
    fig = plt.figure(figsize=(11, 9.0), dpi=300)
    gs = fig.add_gridspec(3, 1, height_ratios=[0.10, 0.55, 0.35], hspace=0.28)

    # Title
    ax_title = fig.add_subplot(gs[0, 0])
    ax_title.axis("off")
    ax_title.text(0.0, 0.65, title, fontsize=12.5, fontweight="bold", color=COL["ink"], ha="left", va="center")

    ax_reg = fig.add_subplot(gs[1, 0])
    ax_base = fig.add_subplot(gs[2, 0])

    if variant == "B":
        reg_cols = [
            "ASSISTANT START",
            "USER REPLY",
            "DETECTED PERSONALITY\n(O,C,E,A,N)",
            "REGULATION PROMPT\nAPPLIED",
            "ASSISTANT REPLY\n(REG)",
        ]
        reg_vals = [
            reg_row.get("ASSISTANT START", ""),
            reg_row.get("USER REPLY", ""),
            reg_row.get("DETECTED PERSONALITY (O,C,E,A,N)", ""),
            reg_row.get("REGULATION PROMPT APPLIED", ""),
            reg_row.get("ASSISTANT REPLY (REG)", ""),
        ]
        _draw_table(
            ax_reg,
            reg_cols,
            reg_vals,
            wrap_widths=[16, 34, 16, 36, 36],
            col_fracs=[0.14, 0.28, 0.14, 0.22, 0.22],
            header_color="#BFE7E5",
            body_color="#DDEFD0",
            edge="#2F74B5",
            fontsize=7.0,
        )

        base_cols = [
            "ASSISTANT START (BASE)",
            "USER REPLY (BASE)",
            "ASSISTANT REPLY (BASE)",
        ]
        base_vals = [
            base_row.get("ASSISTANT START", ""),
            base_row.get("USER REPLY", ""),
            base_row.get("ASSISTANT REPLY", ""),
        ]
        _draw_table(
            ax_base,
            base_cols,
            base_vals,
            wrap_widths=[26, 44, 44],
            col_fracs=[0.26, 0.44, 0.30],
            header_color="#D9CCF0",
            body_color="#F3DCE8",
            edge="#2F74B5",
            fontsize=7.0,
        )
    else:
        reg_cols = [
            "USER REPLY",
            "DETECTED\nPERSONALITY\n(O,C,E,A,N)",
            "REGULATION PROMPT\nAPPLIED",
            "ASSISTANT REPLY\n(REG)",
        ]
        reg_vals = [
            reg_row.get("USER REPLY", ""),
            reg_row.get("DETECTED PERSONALITY (O,C,E,A,N)", ""),
            reg_row.get("REGULATION PROMPT APPLIED", ""),
            reg_row.get("ASSISTANT REPLY (REG)", ""),
        ]
        _draw_table(
            ax_reg,
            reg_cols,
            reg_vals,
            wrap_widths=[46, 16, 34, 46],
            col_fracs=[0.32, 0.14, 0.24, 0.30],
            header_color="#BFE7E5",
            body_color="#DDEFD0",
            edge="#2F74B5",
            fontsize=7.0,
        )

        base_cols = [
            "USER REPLY (BASE)",
            "ASSISTANT REPLY (BASE)",
        ]
        base_vals = [
            base_row.get("USER REPLY", ""),
            base_row.get("ASSISTANT REPLY", ""),
        ]
        _draw_table(
            ax_base,
            base_cols,
            base_vals,
            wrap_widths=[60, 60],
            col_fracs=[0.50, 0.50],
            header_color="#D9CCF0",
            body_color="#F3DCE8",
            edge="#2F74B5",
            fontsize=7.0,
        )

    plt.savefig(output_path, facecolor="white", dpi=300)
    plt.close()
    print(f"✓ Saved qualitative table figure: {output_path}")



if __name__ == "__main__":
    examples = _load_example_turns()
    # Load raw rows for full-column illustration
    reg_path = Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/V8.3/statistical analyis/merged/regulated.csv")
    base_path = Path("/Users/huaduojiejia/MyProject/hslu/2026/paper-summay/paper_submission/V8.3/statistical analyis/merged/baseline.csv")
    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)

    def row_for(msg):
        rr = df_reg[df_reg["MSG. NO."].astype(str) == msg].iloc[0].to_dict()
        rb = df_base[df_base["MSG. NO."].astype(str) == msg].iloc[0].to_dict()
        return rr, rb

    # Figure 15: Type B (conversational UI)
    rr_b, rb_b = row_for("B-4-1")
    create_qualitative_chat_figure(
        title="Personality Type B Example (Low OCEAN): Regulated vs Baseline Dialogue Excerpt",
        reg_row=rr_b,
        base_row=rb_b,
        output_path="figures/dialogue_illustration_1.png",
    )

    # Figure 16: Type A (conversational UI)
    rr_a, rb_a = row_for("A-5-3")
    create_qualitative_chat_figure(
        title="Personality Type A Example (High OCEAN): Regulated vs Baseline Dialogue Excerpt",
        reg_row=rr_a,
        base_row=rb_a,
        output_path="figures/dialogue_illustration_2.png",
    )
