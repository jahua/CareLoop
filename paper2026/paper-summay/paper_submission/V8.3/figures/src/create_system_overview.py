#!/usr/bin/env python3
"""
Create simplified system architecture overview figure.

Matches manuscript Section 3.2: A = (D, R, E) pipeline
Uses clean topology from 10_system_overview.png
"""

from pathlib import Path
from diagram_theme import Theme, box, center_text, new_canvas, save, title

# Output to parent figures/ directory
OUT = Path(__file__).resolve().parent.parent


def create_system_overview():
    """Generate system overview figure with clean topology."""
    t = Theme()
    fig, ax = new_canvas(figsize=(10.0, 6.0), dpi=300)
    
    # Title
    title(ax, "How the System Works", "A simple journey from input to insights")
    
    # Main Flow (top section)
    y_top = 0.78
    box_h = 0.14
    box_w = 0.18
    gap = 0.06
    
    # Calculate positions for 4 boxes centered
    total_width = 4 * box_w + 3 * gap
    left_start = (1 - total_width) / 2
    
    positions = [left_start + i * (box_w + gap) for i in range(4)]
    
    # Flow boxes
    flow_boxes = [
        ("User Input\n& Context", t.blue_fill, t.blue_edge),
        ("Personality\nDetection", t.blue_fill, t.blue_edge),
        ("Behavior\nAdaptation", t.green_fill, t.green_edge),
        ("Response", t.blue_fill, t.blue_edge),
    ]
    
    for i, (label, face, edge) in enumerate(flow_boxes):
        x = positions[i]
        box(ax, x, y_top, box_w, box_h, face=face, edge=edge, lw=2.5, rounding=0.015)
        center_text(ax, x, y_top, box_w, box_h, label, size=11, weight="bold")
        
        # Arrow to next box
        if i < 3:
            arrow_start = x + box_w + 0.01
            arrow_end = positions[i + 1] - 0.01
            arrow_y = y_top + box_h / 2
            ax.annotate('', xy=(arrow_end, arrow_y), xytext=(arrow_start, arrow_y),
                       arrowprops=dict(arrowstyle='->', lw=3, color=t.arrow))
    
    # Quality Assurance section
    y_qa_title = 0.50
    ax.text(0.5, y_qa_title, "Quality Assurance", ha="center", va="center",
            fontsize=13, fontweight="bold", color=t.ink)
    
    y_qa = 0.35
    qa_box_h = 0.12
    qa_box_w = 0.22
    qa_gap = 0.08
    
    # Calculate QA box positions
    qa_total = 3 * qa_box_w + 2 * qa_gap
    qa_start = (1 - qa_total) / 2
    qa_positions = [qa_start + i * (qa_box_w + qa_gap) for i in range(3)]
    
    qa_boxes = [
        ("AI Evaluation", "120 dialogue turns", "#FEF3E2", "#D97D0D"),
        ("Human Experts", "30 sampled turns (25%)", "#FDEAEF", "#C8447B"),
        ("Analysis", "Statistics\n& Insights", "#F0ECFB", "#7C52CC"),
    ]
    
    for i, (label, sublabel, face, edge) in enumerate(qa_boxes):
        x = qa_positions[i]
        box(ax, x, y_qa, qa_box_w, qa_box_h, face=face, edge=edge, lw=2.5, rounding=0.015)
        ax.text(x + qa_box_w/2, y_qa + qa_box_h*0.65, label,
                ha="center", va="center", fontsize=11, fontweight="bold", color=t.ink)
        ax.text(x + qa_box_w/2, y_qa + qa_box_h*0.30, sublabel,
                ha="center", va="center", fontsize=9, color=t.muted)
    
    # Key Results section
    y_results = 0.12
    results_w = 0.90
    results_h = 0.14
    results_x = (1 - results_w) / 2
    
    box(ax, results_x, y_results, results_w, results_h, 
        face="#EDF8F0", edge="#2D8659", lw=2.0, rounding=0.015)
    
    ax.text(0.5, y_results + results_h*0.75, "Key Results",
            ha="center", va="center", fontsize=12, fontweight="bold", color=t.ink)
    
    ax.text(0.5, y_results + results_h*0.45,
            "Detection: 100% accurate  |  Adaptation: 100% effective  |  Personality Match: 91.38% improvement",
            ha="center", va="center", fontsize=10, color=t.ink)
    
    ax.text(0.5, y_results + results_h*0.18,
            "Effect Size (Cohen's d = 4.58) shows personality adaptation is highly impactful",
            ha="center", va="center", fontsize=9, fontstyle="italic", color=t.muted)
    
    save(fig, OUT / "10_system_overview.png")
    print("? Created 10_system_overview.png")


if __name__ == "__main__":
    create_system_overview()
