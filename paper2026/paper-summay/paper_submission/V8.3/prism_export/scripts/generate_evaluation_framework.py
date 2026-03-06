#!/usr/bin/env python3
"""
Generate Evaluation Framework diagram with Cliff's delta (NOT Cohen's d)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
import matplotlib

# High-quality settings
matplotlib.rcParams['figure.dpi'] = 600
matplotlib.rcParams['savefig.dpi'] = 600
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
matplotlib.rcParams['font.size'] = 10

def create_evaluation_framework():
    """Create evaluation framework diagram with Cliff's delta"""
    
    fig, ax = plt.subplots(figsize=(14, 12), dpi=600)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Colors
    regulated_color = '#D4E6F1'  # Light blue
    baseline_color = '#FCF3CF'   # Light yellow
    scoring_yes = '#D5F4E6'      # Light green
    scoring_maybe = '#FFF4E6'    # Light orange
    scoring_no = '#FFE6E6'       # Light red
    outcome_color = '#E8F8F5'    # Light teal
    
    # Title
    ax.text(50, 97, 'Evaluation Framework: Criteria, Scoring, and Process',
            fontsize=18, fontweight='bold', ha='center', va='top')
    
    # ==================== PHASE I: EVALUATION CRITERIA ====================
    y_phase1 = 88
    ax.text(50, y_phase1, 'PHASE I: EVALUATION CRITERIA',
            fontsize=14, fontweight='bold', ha='center', va='top')
    
    # Regulated Condition (5 Criteria)
    y_reg = y_phase1 - 4
    ax.text(50, y_reg, 'Regulated Condition (5 Criteria)',
            fontsize=12, fontweight='bold', ha='center', va='top', color='#2874A6')
    
    # 5 regulated criteria boxes
    y_reg_boxes = y_reg - 3
    criteria_reg = [
        ('Detection', 'Accuracy\ntrait inference\nfidelity'),
        ('Regulation', 'Effectiveness\ninstruction\nalignment'),
        ('Emotional', 'Tone\nwarmth · safety\nsupport'),
        ('Relevance &', 'Coherence\nlogical flow\ncontext'),
        ('Personality', 'Needs\ntrait-specific\nadaptation')
    ]
    
    box_w = 17
    box_h = 10
    spacing = 1
    start_x = 50 - (5 * box_w + 4 * spacing) / 2
    
    for i, (title, desc) in enumerate(criteria_reg):
        x = start_x + i * (box_w + spacing)
        ax.add_patch(FancyBboxPatch(
            (x, y_reg_boxes - box_h), box_w, box_h,
            boxstyle="round,pad=0.3", ec='#2874A6', fc=regulated_color, lw=1.5
        ))
        ax.text(x + box_w/2, y_reg_boxes - 1.5, title,
                fontsize=10, fontweight='bold', ha='center', va='top')
        ax.text(x + box_w/2, y_reg_boxes - 3.5, desc,
                fontsize=8, ha='center', va='top', style='italic', linespacing=1.3)
    
    # Baseline Condition (3 Criteria)
    y_base = y_reg_boxes - box_h - 4
    ax.text(50, y_base, 'Baseline Condition (3 Criteria)',
            fontsize=12, fontweight='bold', ha='center', va='top', color='#B9770E')
    
    criteria_base = [
        ('Emotional', 'Tone\ngeneral warmth\nsupport'),
        ('Relevance &', 'Coherence\nlogical flow\ncontext'),
        ('Personality', 'Needs\nnon-adaptive\nsupport')
    ]
    
    y_base_boxes = y_base - 3
    start_x_base = 50 - (3 * box_w + 2 * spacing) / 2
    
    for i, (title, desc) in enumerate(criteria_base):
        x = start_x_base + i * (box_w + spacing)
        ax.add_patch(FancyBboxPatch(
            (x, y_base_boxes - box_h), box_w, box_h,
            boxstyle="round,pad=0.3", ec='#B9770E', fc=baseline_color, lw=1.5
        ))
        ax.text(x + box_w/2, y_base_boxes - 1.5, title,
                fontsize=10, fontweight='bold', ha='center', va='top')
        ax.text(x + box_w/2, y_base_boxes - 3.5, desc,
                fontsize=8, ha='center', va='top', style='italic', linespacing=1.3)
    
    # ==================== PHASE II: SCORING SCALE ====================
    y_phase2 = y_base_boxes - box_h - 4
    ax.text(50, y_phase2, 'PHASE II: SCORING SCALE (Ternary)',
            fontsize=14, fontweight='bold', ha='center', va='top')
    
    y_scoring = y_phase2 - 3
    score_w = 28
    score_h = 8
    
    scoring_items = [
        ('YES (2)', 'Strong alignment\nclear evidence', scoring_yes, '#27AE60'),
        ('NOT SURE (1)', 'Partial alignment\nambiguous case', scoring_maybe, '#F39C12'),
        ('NO (0)', 'Clear misalignment\ncriterion not met', scoring_no, '#E74C3C')
    ]
    
    start_x_score = 50 - (3 * score_w + 2 * 2) / 2
    
    for i, (title, desc, bg, border) in enumerate(scoring_items):
        x = start_x_score + i * (score_w + 2)
        ax.add_patch(FancyBboxPatch(
            (x, y_scoring - score_h), score_w, score_h,
            boxstyle="round,pad=0.4", ec=border, fc=bg, lw=2.0
        ))
        ax.text(x + score_w/2, y_scoring - 1.5, title,
                fontsize=11, fontweight='bold', ha='center', va='top')
        ax.text(x + score_w/2, y_scoring - 3.5, desc,
                fontsize=9, ha='center', va='top', linespacing=1.3)
    
    # ==================== PHASE III: EVALUATION PROCESS ====================
    y_phase3 = y_scoring - score_h - 4
    ax.text(50, y_phase3, 'PHASE III: EVALUATION PROCESS',
            fontsize=14, fontweight='bold', ha='center', va='top')
    
    y_process = y_phase3 - 3
    process_w = 26
    process_h = 8
    
    process_items = [
        ('1. AI Evaluation', 'Evaluator GPT\nscores\nall 120 turns'),
        ('2. Human Audit', 'Single domain\nexpert\nqualitative review'),
        ('3. Statistical\nAnalysis', 'Effect sizes · CI\nreliability\nanalysis')
    ]
    
    start_x_proc = 50 - (3 * process_w + 2 * 3) / 2
    
    for i, (title, desc) in enumerate(process_items):
        x = start_x_proc + i * (process_w + 3)
        ax.add_patch(FancyBboxPatch(
            (x, y_process - process_h), process_w, process_h,
            boxstyle="round,pad=0.4", ec='#34495E', fc='#ECF0F1', lw=1.5
        ))
        ax.text(x + process_w/2, y_process - 1.5, title,
                fontsize=10, fontweight='bold', ha='center', va='top')
        ax.text(x + process_w/2, y_process - 4, desc,
                fontsize=8, ha='center', va='top', style='italic', linespacing=1.3)
        
        # Arrows between boxes
        if i < 2:
            arrow = FancyArrowPatch(
                (x + process_w, y_process - process_h/2),
                (x + process_w + 3, y_process - process_h/2),
                arrowstyle='->', mutation_scale=20, lw=2, color='#34495E'
            )
            ax.add_patch(arrow)
    
    # ==================== SYSTEM VALIDATION OUTCOME ====================
    y_outcome = y_process - process_h - 4
    ax.text(50, y_outcome, 'SYSTEM VALIDATION OUTCOME',
            fontsize=14, fontweight='bold', ha='center', va='top')
    
    y_outcome_box = y_outcome - 3
    outcome_w = 88
    outcome_h = 16
    
    ax.add_patch(FancyBboxPatch(
        (50 - outcome_w/2, y_outcome_box - outcome_h), outcome_w, outcome_h,
        boxstyle="round,pad=0.6", ec='#148F77', fc=outcome_color, lw=2.0
    ))
    
    # Outcome title
    ax.text(50, y_outcome_box - 2, 'Implementation Fidelity & Selective Enhancement',
            fontsize=12, fontweight='bold', ha='center', va='top')
    
    # Outcome content - UPDATED WITH CLIFF'S DELTA
    outcome_text = (
        "Technical Verification: 100% detection and regulation fidelity confirmed.\n"
        "Comparative Finding: Personality needs addressed significantly better in\n"
        "regulated condition (δ = 0.917, large effect).\n"
        "Quality Retention: Generic quality (tone, relevance) maintained at ceiling level."
    )
    
    ax.text(50, y_outcome_box - 5, outcome_text,
            fontsize=9, ha='center', va='top', style='italic', linespacing=1.5)
    
    plt.savefig('figures/mdpi/evaluation_framework_mdpi.png',
                bbox_inches='tight', pad_inches=0.3, dpi=600, facecolor='white')
    plt.close()
    print("✓ Generated: evaluation_framework_mdpi.png (with Cliff's delta δ = 0.917)")


def main():
    """Generate evaluation framework diagram"""
    print("="*80)
    print("EVALUATION FRAMEWORK GENERATION")
    print("="*80)
    print("\n⚠️  IMPORTANT: Using Cliff's delta (δ = 0.917), NOT Cohen's d")
    print("   Cohen's d was inappropriate for bounded ordinal data\n")
    
    import os
    os.makedirs('figures/mdpi', exist_ok=True)
    
    create_evaluation_framework()
    
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated:")
    print("  ✓ figures/mdpi/evaluation_framework_mdpi.png")
    print("\nKey update:")
    print("  • Replaced: Cohen's d = 4.65")
    print("  • With: Cliff's delta δ = 0.917 (large effect)")
    print("\nReason:")
    print("  • Cliff's delta is appropriate for bounded, ordinal data")
    print("  • Cohen's d overestimated effect size due to ceiling effects")


if __name__ == "__main__":
    import os
    from pathlib import Path
    os.chdir(Path(__file__).parent)
    main()
