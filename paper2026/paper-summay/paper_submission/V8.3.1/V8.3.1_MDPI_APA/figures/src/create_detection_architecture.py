#!/usr/bin/env python3
"""
Create layered detection architecture figure with parallel OCEAN trait detectors.

Implements the improved topology from the manuscript:
- Top layer: Input (user message + dialogue context)
- Middle layer: Parallel Big Five trait detectors (5 parallel components)
- Bottom layer: State update & interface to regulation module
"""

from pathlib import Path
from diagram_theme import Theme, box, center_text, new_canvas, save, title, h_arrow, v_arrow

# Output to parent figures/ directory
OUT = Path(__file__).resolve().parent.parent


def create_detection_architecture():
    """Generate layered detection pipeline with parallel trait inference."""
    t = Theme()
    fig, ax = new_canvas(figsize=(11.0, 7.5), dpi=300)
    
    # Title
    title(ax, "Personality Detection Pipeline: Real-Time OCEAN Inference",
          "Layered architecture with parallel trait detectors")
    
    # Layout parameters
    left_margin = 0.08
    right_margin = 0.92
    width = right_margin - left_margin
    
    # Layer 1: INPUT LAYER (top)
    y1 = 0.82
    h1 = 0.10
    
    ax.text(left_margin, y1 + h1 + 0.02, "INPUT LAYER", 
            fontsize=11, fontweight="bold", color=t.blue_edge)
    
    # Two input boxes
    input_w = (width - 0.05) / 2
    box(ax, left_margin, y1, input_w, h1, 
        face=t.blue_fill, edge=t.blue_edge, lw=2.2, rounding=0.015)
    center_text(ax, left_margin, y1, input_w, h1, 
                "User Message\n(Current Turn)", size=10, weight="bold")
    
    box(ax, left_margin + input_w + 0.05, y1, input_w, h1,
        face=t.blue_fill, edge=t.blue_edge, lw=2.2, rounding=0.015)
    center_text(ax, left_margin + input_w + 0.05, y1, input_w, h1,
                "Dialogue Context\n(History)", size=10, weight="bold")
    
    # Arrow down to inference layer
    center_x = 0.5
    v_arrow(ax, center_x, y1 - 0.01, y1 - 0.06, color=t.arrow, lw=2.5)
    
    # Layer 2: INFERENCE LAYER (middle) - 5 parallel trait detectors
    y2 = 0.60
    h2 = 0.12
    
    ax.text(left_margin, y2 + h2 + 0.02, "INFERENCE LAYER (Parallel Trait Detectors)",
            fontsize=11, fontweight="bold", color=t.green_edge)
    
    # 5 parallel OCEAN trait boxes
    trait_w = (width - 4 * 0.015) / 5
    traits = [
        ("Openness\n(O)", "Curiosity\nnovelty-seeking"),
        ("Conscientiousness\n(C)", "Organization\nstructure"),
        ("Extraversion\n(E)", "Social energy\nassertiveness"),
        ("Agreeableness\n(A)", "Cooperation\nempathy"),
        ("Neuroticism\n(N)", "Emotional\nstability"),
    ]
    
    for i, (label, desc) in enumerate(traits):
        x = left_margin + i * (trait_w + 0.015)
        box(ax, x, y2, trait_w, h2,
            face=t.green_fill, edge=t.green_edge, lw=2.0, rounding=0.012)
        
        # Trait label
        ax.text(x + trait_w/2, y2 + h2*0.70, label,
                ha="center", va="center", fontsize=9, fontweight="bold", color=t.ink)
        
        # Description
        ax.text(x + trait_w/2, y2 + h2*0.30, desc,
                ha="center", va="center", fontsize=7, color=t.muted, linespacing=1.1)
        
        # Small down arrow from each trait
        v_arrow(ax, x + trait_w/2, y2 - 0.01, y2 - 0.04, color=t.arrow, lw=1.8)
    
    # Annotation: LLM inference
    ax.text(right_margin + 0.01, y2 + h2/2, "GPT-4\nper-trait\nprompts",
            ha="left", va="center", fontsize=7, color=t.muted, style="italic")
    
    # Layer 3: STATE & INTERFACE LAYER (bottom)
    y3 = 0.35
    h3 = 0.10
    
    ax.text(left_margin, y3 + h3 + 0.02, "STATE & INTERFACE LAYER",
            fontsize=11, fontweight="bold", color=t.lav_edge)
    
    # Accumulation box
    accum_w = width * 0.42
    box(ax, left_margin, y3, accum_w, h3,
        face=t.lav_fill, edge=t.lav_edge, lw=2.0, rounding=0.015)
    center_text(ax, left_margin, y3, accum_w, h3,
                "Personality State Update\n(Cumulative Evidence)", 
                size=10, weight="bold")
    
    # Arrow to output
    h_arrow(ax, left_margin + accum_w + 0.01, 
            left_margin + accum_w + 0.08, 
            y3 + h3/2, color=t.arrow, lw=2.5)
    
    # OCEAN vector box
    vector_w = width * 0.50
    vector_x = right_margin - vector_w
    box(ax, vector_x, y3, vector_w, h3,
        face=t.lav_fill, edge=t.lav_edge, lw=2.0, rounding=0.015)
    
    # Vector output with formula
    ax.text(vector_x + vector_w/2, y3 + h3*0.70, "OCEAN Vector Output",
            ha="center", va="center", fontsize=10, fontweight="bold", color=t.ink)
    ax.text(vector_x + vector_w/2, y3 + h3*0.35,
            "P = (O, C, E, A, N)   with confidence scores",
            ha="center", va="center", fontsize=8, color=t.muted, family="monospace")
    
    # Arrow down to regulation interface
    v_arrow(ax, 0.5, y3 - 0.01, y3 - 0.06, color=t.arrow, lw=2.5)
    
    # Interface to regulation module
    y4 = 0.15
    h4 = 0.08
    interface_w = width * 0.65
    interface_x = (1 - interface_w) / 2
    
    box(ax, interface_x, y4, interface_w, h4,
        face="#F8F9FA", edge=t.gray_edge, lw=2.5, rounding=0.015)
    
    ax.text(interface_x + interface_w/2, y4 + h4*0.65,
            "Interface to Regulation Module",
            ha="center", va="center", fontsize=11, fontweight="bold", color=t.ink)
    ax.text(interface_x + interface_w/2, y4 + h4*0.25,
            "Transmits personality vector + confidence for behavior adaptation",
            ha="center", va="center", fontsize=8, color=t.muted, style="italic")
    
    # Side annotations
    # Processing note
    ax.text(left_margin - 0.01, y2 + h2/2, "Per-turn\nprocessing",
            ha="right", va="center", fontsize=7, color=t.muted, style="italic")
    
    # Confidence threshold note
    ax.text(right_margin + 0.01, y3 + h3/2, "? = 0.7\nthreshold",
            ha="left", va="center", fontsize=7, color=t.muted, style="italic")
    
    save(fig, OUT / "14_detection_pipeline_layered.png")
    print("? Created 14_detection_pipeline_layered.png")


if __name__ == "__main__":
    create_detection_architecture()
