#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recreate submission diagrams (Figures 02-07) with the same visual system as Figure 01:
- same fonts
- same palette
- same rounded boxes + arrows
- consistent spacing and hierarchy

Outputs (overwritten):
  V8.3/complete_submission/10_system_architecture.png
  ...
  V8.3/complete_submission/12_evaluation_framework_alt.png
"""

from __future__ import annotations

from pathlib import Path

from diagram_theme import Theme, box, center_text, frame, h_arrow, header, new_canvas, save, title, v_arrow


# Output to parent figures/ directory
OUT = Path(__file__).resolve().parent.parent


def fig02_system_architecture() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 6.7), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "System Architecture: Personality-Adaptive Conversational AI")

    left, right = 0.08, 0.92
    w = right - left
    center_x = 0.5

    # Row heights / spacing
    y = 0.86
    row_h = 0.085
    gap = 0.06

    # INPUT LAYER
    header(ax, left, y, "INPUT LAYER", size=10, color=t.blue_edge)
    y -= 0.015 + row_h
    bw = (w - 0.06 * 2) / 3
    xs = [left, left + bw + 0.06, left + (bw + 0.06) * 2]
    for x, txt in zip(
        xs,
        ["Simulated User\n(OCEAN Profile)", "User Message", "Conversation\nContext"],
    ):
        box(ax, x, y, bw, row_h, face=t.blue_fill, edge=t.blue_edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y, bw, row_h, txt, size=9, weight="bold", linespacing=1.15)
    v_arrow(ax, center_x, y - 0.01, y - 0.04, color=t.arrow, lw=2.0)
    y -= gap

    # DETECTION LAYER
    header(ax, left, y, "DETECTION LAYER", size=10, color=t.blue_edge)
    y -= 0.015 + row_h
    bw2 = (w - 0.06) / 2
    xL = left
    xR = left + bw2 + 0.06
    box(ax, xL, y, bw2, row_h, face=t.blue_fill, edge=t.blue_edge, lw=1.4, rounding=0.02)
    box(ax, xR, y, bw2, row_h, face=t.blue_fill, edge=t.blue_edge, lw=1.4, rounding=0.02)
    center_text(ax, xL, y, bw2, row_h, "Personality Detection Module\n(Big Five Trait Detectors)", size=9, weight="bold")
    center_text(ax, xR, y, bw2, row_h, "OCEAN Vector\n[O, C, E, A, N]", size=9, weight="bold")
    h_arrow(ax, xL + bw2 + 0.01, xR - 0.01, y + row_h / 2, color=t.arrow, lw=2.0)
    v_arrow(ax, center_x, y - 0.01, y - 0.04, color=t.arrow, lw=2.0)
    y -= gap

    # REGULATION LAYER
    header(ax, left, y, "REGULATION LAYER", size=10, color=t.green_edge)
    y -= 0.015 + row_h
    bw3 = (w - 0.04 * 2) / 3
    xs3 = [left, left + bw3 + 0.04, left + (bw3 + 0.04) * 2]
    labels3 = [
        "Zurich Model Mapping\n(Motivation Domains)",
        "Behavior Regulation Engine\n(Dynamic Prompts)",
        "Conflict\nResolution",
    ]
    for x, txt in zip(xs3, labels3):
        box(ax, x, y, bw3, row_h, face=t.green_fill, edge=t.green_edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y, bw3, row_h, txt, size=9, weight="bold")
    v_arrow(ax, center_x, y - 0.01, y - 0.04, color=t.arrow, lw=2.0)
    y -= gap

    # GENERATION LAYER
    header(ax, left, y, "GENERATION LAYER", size=10, color=t.gray_edge)
    y -= 0.015 + row_h
    box(ax, xL, y, bw2, row_h, face=t.gray_fill, edge=t.gray_edge, lw=1.4, rounding=0.02)
    box(ax, xR, y, bw2, row_h, face="#FBF4E7", edge="#B68B3A", lw=1.4, rounding=0.02)
    center_text(ax, xL, y, bw2, row_h, "Regulated Assistant Response\n(Personality-Adaptive)", size=9, weight="bold")
    center_text(ax, xR, y, bw2, row_h, "Baseline Assistant Response\n(Generic/Static)", size=9, weight="bold")
    v_arrow(ax, center_x, y - 0.01, y - 0.04, color=t.arrow, lw=2.0)
    y -= gap

    # EVALUATION LAYER
    header(ax, left, y, "EVALUATION LAYER", size=10, color=t.lav_edge)
    y -= 0.015 + row_h
    bw4 = (w - 0.04 * 2) / 3
    xs4 = [left, left + bw4 + 0.04, left + (bw4 + 0.04) * 2]
    labels4 = ["Evaluator GPT\n(AI-Based)", "Human Expert Validation\n(2 PhD Experts)", "Analysis &\nStatistics"]
    for x, txt in zip(xs4, labels4):
        box(ax, x, y, bw4, row_h, face=t.lav_fill, edge=t.lav_edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y, bw4, row_h, txt, size=9, weight="bold")
    v_arrow(ax, center_x, y - 0.01, y - 0.04, color=t.arrow, lw=2.0)

    # Results strip
    y -= 0.08
    box(ax, left, y, w, 0.06, face=t.green_fill, edge=t.frame, lw=1.0, rounding=0.02)
    center_text(ax, left, y, w, 0.06, "Results: Detection Accuracy, Regulation Effectiveness, Effect Sizes (Cohen's d)", size=9, weight="bold")
    save(fig, OUT / "10_system_architecture.png")


def fig03_data_flow() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 6.2), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "Data Processing Pipeline")

    left, right = 0.08, 0.92
    w = right - left
    y = 0.82
    h = 0.1

    # Top pipeline
    step_w = (w - 0.05 * 3) / 4
    xs = [left + i * (step_w + 0.05) for i in range(4)]
    steps = [
        ("INPUT DATA\n120 Dialogues", t.blue_fill, t.blue_edge),
        ("PARSING\nExtract features", t.blue_fill, t.blue_edge),
        ("EVALUATION\nScore criteria", t.blue_fill, t.blue_edge),
        ("VALIDATION\nHuman review", t.blue_fill, t.blue_edge),
    ]
    for (x, (txt, face, edge)) in zip(xs, steps):
        box(ax, x, y, step_w, h, face=face, edge=edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y, step_w, h, txt, size=9, weight="bold", linespacing=1.15)
    for i in range(3):
        h_arrow(ax, xs[i] + step_w + 0.01, xs[i + 1] - 0.01, y + h / 2, color=t.arrow, lw=2.0)

    # Statistical analysis blocks
    y2 = 0.56
    header(ax, 0.5, y2 + 0.13, "STATISTICAL ANALYSIS", size=10, color=t.lav_edge)
    block_w = (w - 0.05 * 3) / 4
    xs2 = [left + i * (block_w + 0.05) for i in range(4)]
    blocks = [
        ("Descriptive Stats\n\nMean, SD, CI\nSample size", t.blue_fill, t.blue_edge),
        ("Effect Sizes\n\nCohen's d\nComparative metrics", t.green_fill, t.green_edge),
        ("Reliability\n\nKrippendorff alpha\nCohen k", t.lav_fill, t.lav_edge),
        ("Criterion Analysis\n\nPer-metric breakdown\nComparative stats", "#FBF4E7", "#B68B3A"),
    ]
    for x, (txt, face, edge) in zip(xs2, blocks):
        box(ax, x, y2, block_w, 0.1, face=face, edge=edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y2, block_w, 0.1, txt, size=8, weight="bold", linespacing=1.15)

    # Results & key findings
    y3 = 0.22
    box(ax, left + 0.1, y3, w - 0.2, 0.16, face=t.lav_fill, edge=t.lav_edge, lw=1.4, rounding=0.02)
    center_text(
        ax,
        left + 0.1,
        y3,
        w - 0.2,
        0.16,
        "RESULTS & KEY FINDINGS\n\n"
        "Detection Accuracy: 100% (58/58) | Regulation Effectiveness: 100% (59/59)\n\n"
        "Personality Needs (Regulated): 100% vs (Baseline): 8.62% | Cohen's d = 4.58 (p < 0.001)",
        size=8,
        weight="bold",
        linespacing=1.2,
    )
    save(fig, OUT / "13_data_flow_pipeline.png")


def _pipeline_row(ax, *, left: float, y: float, texts: list[str], face: str, edge: str, w: float, h: float) -> None:
    n = len(texts)
    gap = 0.02
    bw = (w - gap * (n - 1)) / n
    xs = [left + i * (bw + gap) for i in range(n)]
    for x, txt in zip(xs, texts):
        box(ax, x, y, bw, h, face=face, edge=edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y, bw, h, txt, size=8, weight="bold", linespacing=1.15)
    for i in range(n - 1):
        h_arrow(ax, xs[i] + bw + 0.006, xs[i + 1] - 0.006, y + h / 2)


def fig04_detection_process() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 2.2), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "Personality Detection Pipeline (OCEAN Inference)")

    left, right = 0.06, 0.94
    w = right - left
    y = 0.42
    h = 0.22
    texts = [
        "User message +\ndialogue history",
        "Assemble detection prompts\n(5 trait-specific prompts)",
        "LLM inference\n(score each trait: -1 / 0 / +1)",
        "Parse output -> OCEAN vector\nP_hat = (O,C,E,A,N)",
        "Update personality state\n(cumulative thresholds)",
        "Transmit P_hat\nto regulation module",
    ]
    _pipeline_row(ax, left=left, y=y, texts=texts, face=t.blue_fill, edge=t.blue_edge, w=w, h=h)
    save(fig, OUT / "10_system_overview.png")


def fig05_theoretical_framework() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 5.0), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "Mapping Big Five traits to Zurich Model domains and behavioral effects")

    left, right = 0.08, 0.92
    top = 0.82
    col_gap = 0.05
    col_w = (right - left - col_gap * 2) / 3
    col_x = [left, left + col_w + col_gap, left + (col_w + col_gap) * 2]

    # Column headers
    for x, txt in zip(col_x, ["Big Five traits (inputs)", "Zurich Model domains (needs)", "Behavioral effects (outputs)"]):
        box(ax, x, top, col_w, 0.08, face="white", edge=t.frame, lw=1.0, rounding=0.02)
        center_text(ax, x, top, col_w, 0.08, txt, size=10, weight="bold")

    # Rows
    rows_y = [0.68, 0.54, 0.40, 0.26, 0.12]
    left_items = [
        "Neuroticism / Emotional stability (N)",
        "Agreeableness (A)",
        "Conscientiousness (C)",
        "Extraversion (E)",
        "Openness (O)",
    ]
    mid_items = [
        "Security\n(reassurance / comfort)",
        "Affiliation\n(warmth & relational proximity)",
        "Structure / self-regulation\n(task guidance & pacing)",
        "Arousal\n(novelty & energy regulation)",
        "",
    ]
    right_items = [
        "Provide reassurance / reduce threat\n(or add comfort when vulnerable)",
        "Adjust warmth & collaboration\n(empathic vs. neutral stance)",
        "Adjust structure & pacing\n(organized vs. flexible guidance)",
        "Adjust novelty & stimulation\n(invite exploration vs. keep familiar)",
        "",
    ]

    for y, li, mi, ri in zip(rows_y, left_items, mid_items, right_items):
        box(ax, col_x[0], y, col_w, 0.1, face=t.lav_fill, edge=t.lav_edge, lw=1.4, rounding=0.02)
        center_text(ax, col_x[0], y, col_w, 0.1, li, size=9, weight="bold")

        if mi:
            box(ax, col_x[1], y, col_w, 0.1, face=t.blue_fill, edge=t.blue_edge, lw=1.4, rounding=0.02)
            center_text(ax, col_x[1], y, col_w, 0.1, mi, size=9, weight="bold")
            h_arrow(ax, col_x[0] + col_w + 0.01, col_x[1] - 0.01, y + 0.05)

        if ri:
            box(ax, col_x[2], y, col_w, 0.1, face=t.green_fill, edge=t.green_edge, lw=1.4, rounding=0.02)
            center_text(ax, col_x[2], y, col_w, 0.1, ri, size=9, weight="bold", linespacing=1.15)
            h_arrow(ax, col_x[1] + col_w + 0.01, col_x[2] - 0.01, y + 0.05)

    # Extra arrow O -> Arousal (as in original)
    h_arrow(ax, col_x[0] + col_w * 0.65, col_x[1] + col_w * 0.45, rows_y[-1] + 0.05, color=t.arrow, lw=1.6)
    save(fig, OUT / "11_study_workflow.png")


def fig06_regulation_system() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 2.3), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "Zurich Model-aligned regulation and prompt assembly")

    left, right = 0.05, 0.95
    w = right - left
    y = 0.42
    h = 0.22
    texts = [
        "Detected personality\nP_hat = (O,C,E,A,N)",
        "Map traits to motivational needs\n(Security / Arousal / Affiliation)",
        "Select trait prompts\n(ignore neutral traits: 0)",
        "Harmonize potential conflicts\n(e.g., high O + low E)",
        "Concatenate into one\nbehavior regulation instruction",
        "Response generation\n(assistant reply)",
    ]
    _pipeline_row(ax, left=left, y=y, texts=texts, face=t.green_fill, edge=t.green_edge, w=w, h=h)

    # Logging branch (dotted)
    log_x = 0.80
    log_y = 0.12
    box(ax, log_x, log_y, 0.17, 0.18, face=t.green_fill, edge=t.green_edge, lw=1.4, rounding=0.02)
    center_text(ax, log_x, log_y, 0.17, 0.18, "Log prompts + decisions\nfor traceability", size=8, weight="bold")
    ax.plot([0.77, log_x + 0.02], [y + h / 2, log_y + 0.18], color=t.arrow, lw=1.6, linestyle=(0, (4, 3)))
    ax.text(0.775, 0.32, "store", fontsize=7, color=t.muted)
    save(fig, OUT / "12_evaluation_framework.png")


def fig07_evaluation_framework() -> None:
    t = Theme()
    fig, ax = new_canvas(figsize=(9.0, 7.0), dpi=300)
    frame(ax, pad=0.02, color=t.frame)
    title(ax, "Evaluation Framework: Criteria & Scoring")

    left, right = 0.08, 0.92
    w = right - left

    # Top: criteria groups
    y = 0.83
    box(ax, left, y, w / 2 - 0.03, 0.06, face=t.blue_fill, edge=t.blue_edge, lw=1.2, rounding=0.02)
    box(ax, left + w / 2 + 0.03, y, w / 2 - 0.03, 0.06, face="#FBF4E7", edge="#B68B3A", lw=1.2, rounding=0.02)
    center_text(ax, left, y, w / 2 - 0.03, 0.06, "REGULATED AGENTS (5 Criteria)", size=9, weight="bold")
    center_text(ax, left + w / 2 + 0.03, y, w / 2 - 0.03, 0.06, "BASELINE AGENTS (3 Criteria)", size=9, weight="bold")

    # Criteria cards row
    y2 = 0.70
    card_h = 0.10
    card_w = 0.11
    gap = 0.02

    reg = [
        ("Detection\nAccuracy", "Correct trait\ninference", t.blue_fill, t.blue_edge),
        ("Regulation\nEffectiveness", "Adapted response\nalignment", t.blue_fill, t.blue_edge),
        ("Emotional\nTone", "Appropriate\nwarmth", t.blue_fill, t.blue_edge),
        ("Relevance &\nCoherence", "Logical\ncontinuation", t.blue_fill, t.blue_edge),
        ("Personality\nNeeds", "Trait-specific\nsupport", t.blue_fill, t.blue_edge),
    ]
    base = [
        ("Emotional\nTone", "Appropriate\nwarmth", "#FBF4E7", "#B68B3A"),
        ("Relevance &\nCoherence", "Logical\ncontinuation", "#FBF4E7", "#B68B3A"),
        ("Personality\nNeeds", "Generic\nsupport", "#FBF4E7", "#B68B3A"),
    ]

    x = left
    for (hdr, sub, face, edge) in reg:
        box(ax, x, y2, card_w, card_h, face=face, edge=edge, lw=1.2, rounding=0.02)
        center_text(ax, x, y2, card_w, card_h, f"{hdr}\n\n{sub}", size=7, weight="bold", linespacing=1.1)
        x += card_w + gap

    x = left + w / 2 + 0.03
    for (hdr, sub, face, edge) in base:
        box(ax, x, y2, card_w, card_h, face=face, edge=edge, lw=1.2, rounding=0.02)
        center_text(ax, x, y2, card_w, card_h, f"{hdr}\n\n{sub}", size=7, weight="bold", linespacing=1.1)
        x += card_w + gap

    # Scoring scale
    header(ax, left, 0.58, "SCORING SCALE (Ternary)", size=10, color=t.lav_edge)
    y3 = 0.49
    scale_w = (w - 0.05 * 2) / 3
    xs = [left, left + scale_w + 0.05, left + (scale_w + 0.05) * 2]
    scale = [
        ("YES (2)", "Strong alignment\nClear evidence", t.green_fill, t.green_edge),
        ("NOT SURE (1)", "Partial alignment\nAmbiguous cases", "#FBF4E7", "#B68B3A"),
        ("NO (0)", "Clear misalignment\nCriterion not met", t.lav_fill, t.lav_edge),
    ]
    for x, (hdr_txt, sub_txt, face, edge) in zip(xs, scale):
        box(ax, x, y3, scale_w, 0.085, face=face, edge=edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y3, scale_w, 0.085, f"{hdr_txt}\n\n{sub_txt}", size=8, weight="bold", linespacing=1.1)

    # Evaluation process
    header(ax, left, 0.37, "EVALUATION PROCESS", size=10, color=t.blue_edge)
    y4 = 0.26
    proc_w = (w - 0.05 * 2) / 3
    xs4 = [left, left + proc_w + 0.05, left + (proc_w + 0.05) * 2]
    proc = [
        ("1. AI EVALUATION", "Evaluator GPT scores\nall 120 turns\n(Complete coverage)", t.blue_fill, t.blue_edge),
        ("2. HUMAN VALIDATION", "30 turns (25% sample)\n2 PhD experts\nBlinded scoring", t.blue_fill, t.blue_edge),
        ("3. RELIABILITY ANALYSIS", "IRR calculation\nalpha=0.82 (human-human)\nk=0.89 (AI-human)", t.blue_fill, t.blue_edge),
    ]
    for x, (hdr_txt, sub_txt, face, edge) in zip(xs4, proc):
        box(ax, x, y4, proc_w, 0.1, face=face, edge=edge, lw=1.4, rounding=0.02)
        center_text(ax, x, y4, proc_w, 0.1, f"{hdr_txt}\n\n{sub_txt}", size=8, weight="bold", linespacing=1.1)
    for i in range(2):
        h_arrow(ax, xs4[i] + proc_w + 0.01, xs4[i + 1] - 0.01, y4 + 0.05)

    # Outcome
    y5 = 0.08
    box(ax, left, y5, w, 0.12, face=t.green_fill, edge=t.frame, lw=1.0, rounding=0.02)
    center_text(
        ax,
        left,
        y5,
        w,
        0.12,
        "OUTCOME: Validation of Evaluation Framework\n\n"
        "Strong human-to-human agreement (alpha=0.82) validates evaluation criteria\n"
        "Excellent AI-to-human alignment (k=0.89) demonstrates Evaluator GPT validity\n"
        "No systematic bias detected in criterion-specific analysis (k=0.86-0.92)",
        size=8,
        weight="bold",
        linespacing=1.15,
    )
    save(fig, OUT / "12_evaluation_framework_alt.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig02_system_architecture()
    fig03_data_flow()
    fig04_detection_process()
    fig05_theoretical_framework()
    fig06_regulation_system()
    fig07_evaluation_framework()
    print("Updated Figures 02-07 in complete_submission/")


if __name__ == "__main__":
    main()

