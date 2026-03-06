#!/usr/bin/env python3
"""
Generate System Architecture diagram (Figure 2)
With even top and bottom white space
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# High-quality settings
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.unicode_minus": False,
})


def create_system_architecture_mdpi(output_path="figures/mdpi/system_architecture_mdpi.png"):
    """
    Create system architecture diagram with even top/bottom margins.
    
    Shows: INPUT → DETECTION → REGULATION → GENERATION → EVALUATION
    """
    # Figure size optimized for even spacing
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    # Set coordinate system
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'header': '#F5F5F5',
        'input': '#E8F5E9',
        'detection': '#E3F2FD',
        'regulation': '#FFF3E0',
        'generation': '#F3E5F5',
        'evaluation': '#FCE4EC',
        'storage': '#FFF9C4',
        'border': '#666666',
        'text': '#222222',
        'arrow': '#555555',
    }
    
    # Calculate vertical spacing for even top/bottom margins
    top_margin = 8
    bottom_margin = 8
    title_height = 8
    
    # Available space for content
    content_start_y = 100 - top_margin - title_height
    content_end_y = bottom_margin
    content_height = content_start_y - content_end_y
    
    # =========================================================================
    # TITLE
    # =========================================================================
    title_y = 100 - top_margin - 3
    ax.text(50, title_y, 'System Architecture: Personality-Adaptive Conversational AI',
            fontsize=13, fontweight='bold', ha='center', va='top', color=colors['text'])
    
    # =========================================================================
    # PROMISE ORCHESTRATION (Top banner)
    # =========================================================================
    promise_y = content_start_y - 2
    promise_box = FancyBboxPatch(
        (5, promise_y - 6), 90, 5,
        boxstyle="round,pad=0.3", 
        facecolor=colors['header'],
        edgecolor=colors['border'],
        linewidth=1.0
    )
    ax.add_patch(promise_box)
    ax.text(50, promise_y - 3.5, 
            'PROMISE orchestration (state transitions, prompt composition, storage\naccess)',
            fontsize=9, ha='center', va='center', color=colors['text'])
    
    # =========================================================================
    # MAIN PIPELINE (5 stages)
    # =========================================================================
    
    # Layout parameters
    box_width = 80
    box_height = 7
    box_x = 10
    
    # Calculate spacing between boxes
    num_stages = 5  # INPUT, DETECTION, REGULATION, GENERATION, EVALUATION
    pipeline_start_y = promise_y - 8
    pipeline_height = content_height - (100 - pipeline_start_y) - bottom_margin - 18  # Space for storage box
    stage_spacing = pipeline_height / num_stages
    
    # Storage box parameters (right side)
    storage_width = 25
    storage_x = box_x + box_width + 5
    
    stages = [
        {
            'y': pipeline_start_y,
            'label_left': 'INPUT',
            'title': 'Input',
            'subtitle': 'user message · context',
            'color': colors['input'],
        },
        {
            'y': pipeline_start_y - stage_spacing,
            'label_left': 'DETECTION',
            'title': 'Trait inference',
            'subtitle': 'OCEAN prompts',
            'color': colors['detection'],
        },
        {
            'y': pipeline_start_y - 2 * stage_spacing,
            'label_left': '',  # No label for inferred state
            'title': 'Inferred trait state',
            'subtitle': 'P · confidence',
            'color': colors['detection'],
            'arrow_to_storage': True,
        },
        {
            'y': pipeline_start_y - 3 * stage_spacing,
            'label_left': 'REGULATION',
            'title': 'Trait-aligned regulation',
            'subtitle': 'Zurich Model:\nSecurity · Arousal · Affiliation',
            'color': colors['regulation'],
        },
        {
            'y': pipeline_start_y - 4 * stage_spacing,
            'label_left': '',  # No label for prompt assembly
            'title': 'Prompt assembly',
            'subtitle': 'base + regulation',
            'color': colors['regulation'],
        },
    ]
    
    # Draw main pipeline stages
    for i, stage in enumerate(stages):
        y = stage['y']
        
        # Left label
        if stage['label_left']:
            ax.text(box_x - 2, y - box_height/2, stage['label_left'],
                   fontsize=9, fontweight='bold', ha='right', va='center',
                   color=colors['text'])
        
        # Main box
        box = FancyBboxPatch(
            (box_x, y - box_height), box_width, box_height,
            boxstyle="round,pad=0.3",
            facecolor=stage['color'],
            edgecolor=colors['border'],
            linewidth=1.2
        )
        ax.add_patch(box)
        
        # Title
        ax.text(50, y - 2.5, stage['title'],
               fontsize=10, fontweight='bold', ha='center', va='top',
               color=colors['text'])
        
        # Subtitle
        subtitle_lines = stage['subtitle'].split('\n')
        subtitle_y_start = y - 3.8
        for j, line in enumerate(subtitle_lines):
            ax.text(50, subtitle_y_start - j*1.8, line,
                   fontsize=8, ha='center', va='top', color=colors['text'])
        
        # Arrow to next stage (except last)
        if i < len(stages) - 1:
            arrow_y_start = y - box_height - 0.5
            arrow_y_end = stages[i+1]['y'] + 0.5
            arrow = FancyArrowPatch(
                (50, arrow_y_start), (50, arrow_y_end),
                arrowstyle='->', 
                lw=2.0,
                color=colors['arrow'],
                mutation_scale=20
            )
            ax.add_patch(arrow)
        
        # Arrow to storage (for inferred state)
        if stage.get('arrow_to_storage'):
            arrow_storage = FancyArrowPatch(
                (box_x + box_width, y - box_height/2), 
                (storage_x - 1, y - box_height/2),
                arrowstyle='->', 
                lw=1.5,
                color=colors['arrow'],
                mutation_scale=15
            )
            ax.add_patch(arrow_storage)
    
    # =========================================================================
    # GENERATION stage
    # =========================================================================
    gen_y = stages[-1]['y'] - stage_spacing
    
    ax.text(box_x - 2, gen_y - box_height/2, 'GENERATION',
           fontsize=9, fontweight='bold', ha='right', va='center',
           color=colors['text'])
    
    gen_box = FancyBboxPatch(
        (box_x, gen_y - box_height), box_width, box_height,
        boxstyle="round,pad=0.3",
        facecolor=colors['generation'],
        edgecolor=colors['border'],
        linewidth=1.2
    )
    ax.add_patch(gen_box)
    
    ax.text(50, gen_y - 2.5, 'LLM response generation',
           fontsize=10, fontweight='bold', ha='center', va='top',
           color=colors['text'])
    ax.text(50, gen_y - 4.3, '(GPT-4)',
           fontsize=8, ha='center', va='top', color=colors['text'])
    
    # Arrow down
    arrow = FancyArrowPatch(
        (50, gen_y - box_height - 0.5), (50, gen_y - stage_spacing + 0.5),
        arrowstyle='->', 
        lw=2.0,
        color=colors['arrow'],
        mutation_scale=20
    )
    ax.add_patch(arrow)
    
    # =========================================================================
    # Assistant response (simple box)
    # =========================================================================
    resp_y = gen_y - stage_spacing
    
    resp_box = FancyBboxPatch(
        (box_x, resp_y - box_height), box_width, box_height,
        boxstyle="round,pad=0.3",
        facecolor='#FFFFFF',
        edgecolor=colors['border'],
        linewidth=1.2
    )
    ax.add_patch(resp_box)
    
    ax.text(50, resp_y - 3.5, 'Assistant response',
           fontsize=10, fontweight='bold', ha='center', va='center',
           color=colors['text'])
    
    # Arrow down to evaluation
    arrow = FancyArrowPatch(
        (50, resp_y - box_height - 0.5), (50, resp_y - stage_spacing + 0.5),
        arrowstyle='->', 
        lw=2.0,
        color=colors['arrow'],
        mutation_scale=20
    )
    ax.add_patch(arrow)
    
    # =========================================================================
    # EVALUATION stage
    # =========================================================================
    eval_y = resp_y - stage_spacing
    
    ax.text(box_x - 2, eval_y - box_height/2, 'EVALUATION',
           fontsize=9, fontweight='bold', ha='right', va='center',
           color=colors['text'])
    
    eval_box = FancyBboxPatch(
        (box_x, eval_y - box_height), box_width, box_height,
        boxstyle="round,pad=0.3",
        facecolor=colors['evaluation'],
        edgecolor=colors['border'],
        linewidth=1.2
    )
    ax.add_patch(eval_box)
    
    ax.text(50, eval_y - 2.5, 'Evaluation',
           fontsize=10, fontweight='bold', ha='center', va='top',
           color=colors['text'])
    ax.text(50, eval_y - 4.3, 'LLM judge · expert · stats',
           fontsize=8, ha='center', va='top', color=colors['text'])
    
    # Arrow to storage
    arrow_storage = FancyArrowPatch(
        (box_x + box_width, eval_y - box_height/2), 
        (storage_x - 1, eval_y - box_height/2),
        arrowstyle='->', 
        lw=1.5,
        color=colors['arrow'],
        mutation_scale=15
    )
    ax.add_patch(arrow_storage)
    
    # =========================================================================
    # INTERACTION STORAGE (right side)
    # =========================================================================
    
    # Calculate storage box position and height
    storage_top_y = stages[2]['y']  # Align with inferred state
    storage_bottom_y = eval_y - box_height
    storage_height = storage_top_y - storage_bottom_y
    
    storage_box = FancyBboxPatch(
        (storage_x, storage_bottom_y), storage_width, storage_height,
        boxstyle="round,pad=0.3",
        facecolor=colors['storage'],
        edgecolor=colors['border'],
        linewidth=1.2
    )
    ax.add_patch(storage_box)
    
    storage_center_y = (storage_top_y + storage_bottom_y) / 2
    ax.text(storage_x + storage_width/2, storage_center_y + 2,
           'Interaction storage',
           fontsize=9, fontweight='bold', ha='center', va='center',
           color=colors['text'])
    ax.text(storage_x + storage_width/2, storage_center_y - 2,
           'All states & metrics\nlogged per turn',
           fontsize=7.5, ha='center', va='center', color=colors['text'])
    
    # =========================================================================
    # SAVE with minimal padding
    # =========================================================================
    
    # Adjust ylim to ensure even top/bottom margins
    # This is the key fix: set ylim AFTER drawing all elements
    min_y_content = eval_y - box_height  # Bottom of eval box
    max_y_content = 100 - top_margin  # Top (after title)
    
    # Set ylim to include all content with even margins
    ax.set_ylim(min_y_content - bottom_margin, 100)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save with minimal padding
    plt.savefig(
        output_path,
        facecolor='white',
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.05  # Minimal padding
    )
    plt.close()
    
    print(f"✓ Generated: {output_path}")
    print(f"  - Even top/bottom margins: {top_margin} units")
    print(f"  - Content height: {content_height:.1f} units")
    print(f"  - Minimal padding: 0.05 inches")


def main():
    """Generate system architecture diagram."""
    print("="*80)
    print("SYSTEM ARCHITECTURE DIAGRAM GENERATION")
    print("="*80)
    print("\nFeatures:")
    print("  • Even top and bottom white space")
    print("  • Minimal padding (0.05 inches)")
    print("  • Clean MDPI style")
    print("  • 300 DPI resolution")
    print()
    
    create_system_architecture_mdpi()
    
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
