#!/usr/bin/env python3
"""
System Diagrams Generator
Creates publication-ready architectural and workflow diagrams

Author: Unified Analysis Pipeline
Date: 2026
Version: 2.0
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Import unified configuration
from visualization_config import configure_matplotlib, save_figure, PUBLICATION_CONFIG


# ============================================================================
# CONFIGURATION
# ============================================================================

configure_matplotlib()
OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
# FIGURE 6: SYSTEM ARCHITECTURE OVERVIEW
# ============================================================================

def create_system_architecture(output_dir: str = OUTPUT_DIR):
    """
    Create system architecture diagram showing the main processing pipeline.
    A4-optimized for publication: 160 � 107 mm @ 300 DPI
    """
    print("Creating Figure 6: System Architecture Overview...")
    
    fig, ax = plt.subplots(figsize=(9.5, 6.33), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Color scheme
    color_input = "#E8F4F8"
    color_process = "#B3E5FC"
    color_decision = "#81D4FA"
    color_output = "#4FC3F7"
    
    # Title
    ax.text(6, 7.5, "System Architecture", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_TITLE + 4, 
           weight='bold', ha='center')
    ax.text(6, 7.1, "Personality-adaptive conversation pipeline", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, 
           style='italic', ha='center', color='#666')
    
    # Step 1: Input
    box1 = FancyBboxPatch((0.5, 5.5), 2.5, 1, boxstyle="round,pad=0.1", 
                          facecolor=color_input, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box1)
    ax.text(1.75, 6, "User Input\n& Context", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, weight='bold')
    
    # Arrow 1
    arrow1 = FancyArrowPatch((3.2, 6), (3.8, 6), arrowstyle='->', 
                            lw=2.5, color="#01579B")
    ax.add_patch(arrow1)
    
    # Step 2: Detection
    box2 = FancyBboxPatch((3.8, 5.5), 2.5, 1, boxstyle="round,pad=0.1",
                          facecolor=color_process, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box2)
    ax.text(5.05, 6, "Personality\nDetection", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, weight='bold')
    
    # Arrow 2
    arrow2 = FancyArrowPatch((6.5, 6), (7.1, 6), arrowstyle='->', 
                            lw=2.5, color="#01579B")
    ax.add_patch(arrow2)
    
    # Step 3: Adaptation
    box3 = FancyBboxPatch((7.1, 5.5), 2.5, 1, boxstyle="round,pad=0.1",
                          facecolor=color_decision, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box3)
    ax.text(8.35, 6, "Behavior\nAdaptation", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, weight='bold')
    
    # Arrow 3
    arrow3 = FancyArrowPatch((9.7, 6), (10.3, 6), arrowstyle='->', 
                            lw=2.5, color="#01579B")
    ax.add_patch(arrow3)
    
    # Step 4: Output
    box4 = FancyBboxPatch((10.3, 5.5), 1.2, 1, boxstyle="round,pad=0.1",
                          facecolor=color_output, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box4)
    ax.text(10.9, 6, "Response", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_MEDIUM, weight='bold')
    
    # Evaluation section below
    ax.text(6, 4.5, "Evaluation Framework", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, 
           weight='bold', ha='center')
    
    # AI Evaluation
    box_ai = FancyBboxPatch((1, 2.5), 3.5, 1.2, boxstyle="round,pad=0.1",
                            facecolor="#FFF9C4", edgecolor="#F57F17", linewidth=2)
    ax.add_patch(box_ai)
    ax.text(2.75, 3.3, "AI Evaluator", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, weight='bold')
    ax.text(2.75, 2.8, "120 dialogue turns", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    # Human Validation
    box_human = FancyBboxPatch((5.5, 2.5), 3.5, 1.2, boxstyle="round,pad=0.1",
                               facecolor="#F8BBD0", edgecolor="#C2185B", linewidth=2)
    ax.add_patch(box_human)
    ax.text(7.25, 3.3, "Human Experts", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, weight='bold')
    ax.text(7.25, 2.8, "30 sampled turns (25%)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    # Statistical Analysis
    box_stats = FancyBboxPatch((10, 2.5), 1.8, 1.2, boxstyle="round,pad=0.1",
                               facecolor="#E1BEE7", edgecolor="#6A1B9A", linewidth=2)
    ax.add_patch(box_stats)
    ax.text(10.9, 3.3, "Analysis", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_MEDIUM, weight='bold')
    ax.text(10.9, 2.8, "Statistics\n& Results", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL)
    
    # Results summary at bottom
    result_box = FancyBboxPatch((0.5, 0.3), 11, 1.5, boxstyle="round,pad=0.1",
                                facecolor="#E8F5E9", edgecolor="#1B5E20", linewidth=2)
    ax.add_patch(result_box)
    ax.text(6, 1.5, "Key Results", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, weight='bold')
    ax.text(6, 1.0, "Detection: 100% accurate  |  Adaptation: 100% effective  |  Personality Match: 91.4% improvement", 
           ha='center', va='center', fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    ax.text(6, 0.5, "Effect Size (Cohen's d = 4.58) demonstrates strong personalization impact", 
           ha='center', va='center', fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL, 
           style='italic', color='#1B5E20')
    
    plt.tight_layout()
    save_figure(fig, '06_system_architecture', output_dir, verbose=True)


# ============================================================================
# FIGURE 7: STUDY WORKFLOW
# ============================================================================

def create_study_workflow(output_dir: str = OUTPUT_DIR):
    """
    Create study design and workflow diagram.
    A4-optimized: 160 � 120 mm @ 300 DPI
    """
    print("Creating Figure 7: Study Workflow...")
    
    fig, ax = plt.subplots(figsize=(9.5, 7.13), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Title
    ax.text(6, 8.5, "Study Design and Workflow", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_TITLE + 4, 
           weight='bold', ha='center')
    ax.text(6, 8.1, "Controlled simulation methodology", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE, 
           style='italic', ha='center', color='#666')
    
    # Color scheme for stages
    color_setup = "#C8E6C9"
    color_execution = "#BBDEFB"
    color_validation = "#FFE0B2"
    color_results = "#F8BBD0"
    
    # Stage 1: Study Setup
    ax.text(6, 7.4, "1. STUDY SETUP", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, 
           weight='bold', ha='center')
    
    box_agents = FancyBboxPatch((1, 6.5), 3, 0.7, boxstyle="round,pad=0.05",
                                facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_agents)
    ax.text(2.5, 6.85, "20 Agents\n(10 per type)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    box_types = FancyBboxPatch((5, 6.5), 3, 0.7, boxstyle="round,pad=0.05",
                               facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_types)
    ax.text(6.5, 6.85, "2 Personality Types\n(Type A & B)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    box_conditions = FancyBboxPatch((9, 6.5), 2.5, 0.7, boxstyle="round,pad=0.05",
                                    facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_conditions)
    ax.text(10.25, 6.85, "2 Conditions\n(Reg vs Base)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    # Arrow down
    arrow_down1 = FancyArrowPatch((6, 6.5), (6, 5.7), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down1)
    
    # Stage 2: Execution
    ax.text(6, 5.4, "2. EXECUTION", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, 
           weight='bold', ha='center')
    
    box_dialogues = FancyBboxPatch((2, 4.5), 4, 0.7, boxstyle="round,pad=0.05",
                                   facecolor=color_execution, edgecolor="#1565C0", linewidth=1.5)
    ax.add_patch(box_dialogues)
    ax.text(4, 4.85, "120 Dialogues\n(6 turns each)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    box_scoring = FancyBboxPatch((6.5, 4.5), 4, 0.7, boxstyle="round,pad=0.05",
                                 facecolor=color_execution, edgecolor="#1565C0", linewidth=1.5)
    ax.add_patch(box_scoring)
    ax.text(8.5, 4.85, "Binary Evaluation\nYes (1) | No (0)", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_BASE)
    
    # Arrow down
    arrow_down2 = FancyArrowPatch((6, 4.5), (6, 3.7), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down2)
    
    # Stage 3: Evaluation & Validation
    ax.text(6, 3.4, "3. EVALUATION", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, 
           weight='bold', ha='center')
    
    box_ai_eval = FancyBboxPatch((1.5, 2.3), 3.5, 0.9, boxstyle="round,pad=0.05",
                                 facecolor=color_validation, edgecolor="#E65100", linewidth=1.5)
    ax.add_patch(box_ai_eval)
    ax.text(3.25, 2.9, "AI Evaluator", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_MEDIUM, weight='bold')
    ax.text(3.25, 2.5, "All 120 turns", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL)
    
    box_human_val = FancyBboxPatch((5.5, 2.3), 3.5, 0.9, boxstyle="round,pad=0.05",
                                   facecolor=color_validation, edgecolor="#E65100", linewidth=1.5)
    ax.add_patch(box_human_val)
    ax.text(7.25, 2.9, "Human Experts", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_MEDIUM, weight='bold')
    ax.text(7.25, 2.5, "30 sampled turns", ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL)
    
    # Validation metrics
    ax.text(3.25, 1.8, "? = 0.89 (AI-Human)", ha='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL, style='italic', color='#333')
    ax.text(7.25, 1.8, "? = 0.82 (Human-Human)", ha='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL, style='italic', color='#333')
    
    # Arrow down
    arrow_down3 = FancyArrowPatch((6, 2.3), (6, 1.5), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down3)
    
    # Stage 4: Results
    ax.text(6, 1.2, "4. RESULTS", 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_LARGE + 1, 
           weight='bold', ha='center')
    
    result_box = FancyBboxPatch((0.5, 0.05), 11, 1.0, boxstyle="round,pad=0.05",
                                facecolor=color_results, edgecolor="#880E4F", linewidth=2)
    ax.add_patch(result_box)
    ax.text(6, 0.7, "Personality Adaptation Shows Dramatic Improvement", 
           ha='center', va='center', 
           fontsize=PUBLICATION_CONFIG.FONT_SIZE_MEDIUM, weight='bold')
    ax.text(6, 0.3, "Personality Needs: 100% vs 8.6%  |  Cohen's d = 4.58 (p < 0.001)", 
           ha='center', va='center', fontsize=PUBLICATION_CONFIG.FONT_SIZE_SMALL)
    
    plt.tight_layout()
    save_figure(fig, '07_study_workflow', output_dir, verbose=True)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Generate all system diagrams."""
    print("\n" + "="*70)
    print("SYSTEM DIAGRAMS GENERATOR")
    print("Publication-Ready Architecture and Workflow Figures")
    print("="*70 + "\n")
    
    create_system_architecture()
    create_study_workflow()
    
    print("\n" + "="*70)
    print("? DIAGRAMS CREATED SUCCESSFULLY")
    print("="*70)
    print("\n?? Generated Figures:")
    print("  � 06_system_architecture.png - System processing pipeline")
    print("  � 07_study_workflow.png - Research methodology")
    print("\n?? Features:")
    print("  � A4-optimized dimensions")
    print("  � 300 DPI publication quality")
    print("  � Colorblind-friendly colors")
    print("  � Clean, professional styling")
    print("\n?? Location: ./figures/")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
