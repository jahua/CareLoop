import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

def create_system_overview_diagram(filename="10_system_overview.png"):
    """
    A4-optimized system overview - shows the main pipeline without overload
    Target: 1900 × 1267 px (160 × 107 mm @ 300 DPI) for A4 embedding with readable fonts
    """
    fig, ax = plt.subplots(figsize=(9.5, 6.33), dpi=200)  # Results in ~1900×1266 px
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Color scheme - friendly and clean
    color_input = "#E8F4F8"
    color_process = "#B3E5FC"
    color_decision = "#81D4FA"
    color_output = "#4FC3F7"
    
    # Title with friendly tone - LARGER FONTS FOR A4
    ax.text(6, 7.5, "How the System Works", fontsize=16, weight='bold', ha='center')
    ax.text(6, 7.1, "A simple journey from input to insights", fontsize=11, style='italic', ha='center', color='#666')
    
    # Step 1: Input
    box1 = FancyBboxPatch((0.5, 5.5), 2.5, 1, boxstyle="round,pad=0.1", 
                          facecolor=color_input, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box1)
    ax.text(1.75, 6, "User Input\n& Context", ha='center', va='center', fontsize=11, weight='bold')
    
    # Arrow 1
    arrow1 = FancyArrowPatch((3.2, 6), (3.8, 6), arrowstyle='->', lw=2.5, color="#01579B")
    ax.add_patch(arrow1)
    
    # Step 2: Detection
    box2 = FancyBboxPatch((3.8, 5.5), 2.5, 1, boxstyle="round,pad=0.1",
                          facecolor=color_process, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box2)
    ax.text(5.05, 6, "Personality\nDetection", ha='center', va='center', fontsize=11, weight='bold')
    
    # Arrow 2
    arrow2 = FancyArrowPatch((6.5, 6), (7.1, 6), arrowstyle='->', lw=2.5, color="#01579B")
    ax.add_patch(arrow2)
    
    # Step 3: Adaptation
    box3 = FancyBboxPatch((7.1, 5.5), 2.5, 1, boxstyle="round,pad=0.1",
                          facecolor=color_decision, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box3)
    ax.text(8.35, 6, "Behavior\nAdaptation", ha='center', va='center', fontsize=11, weight='bold')
    
    # Arrow 3
    arrow3 = FancyArrowPatch((9.7, 6), (10.3, 6), arrowstyle='->', lw=2.5, color="#01579B")
    ax.add_patch(arrow3)
    
    # Step 4: Output
    box4 = FancyBboxPatch((10.3, 5.5), 1.2, 1, boxstyle="round,pad=0.1",
                          facecolor=color_output, edgecolor="#01579B", linewidth=2)
    ax.add_patch(box4)
    ax.text(10.9, 6, "Response", ha='center', va='center', fontsize=10, weight='bold')
    
    # Evaluation section below - LARGER LABEL
    ax.text(6, 4.5, "Quality Assurance", fontsize=12, weight='bold', ha='center')
    
    # AI Evaluation
    box_ai = FancyBboxPatch((1, 2.5), 3.5, 1.2, boxstyle="round,pad=0.1",
                            facecolor="#FFF9C4", edgecolor="#F57F17", linewidth=2)
    ax.add_patch(box_ai)
    ax.text(2.75, 3.3, "AI Evaluation", ha='center', va='center', fontsize=11, weight='bold')
    ax.text(2.75, 2.8, "120 dialogue turns", ha='center', va='center', fontsize=9)
    
    # Human Validation
    box_human = FancyBboxPatch((5.5, 2.5), 3.5, 1.2, boxstyle="round,pad=0.1",
                               facecolor="#F8BBD0", edgecolor="#C2185B", linewidth=2)
    ax.add_patch(box_human)
    ax.text(7.25, 3.3, "Human Experts", ha='center', va='center', fontsize=11, weight='bold')
    ax.text(7.25, 2.8, "30 sampled turns (25%)", ha='center', va='center', fontsize=9)
    
    # Statistical Analysis
    box_stats = FancyBboxPatch((10, 2.5), 1.8, 1.2, boxstyle="round,pad=0.1",
                               facecolor="#E1BEE7", edgecolor="#6A1B9A", linewidth=2)
    ax.add_patch(box_stats)
    ax.text(10.9, 3.3, "Analysis", ha='center', va='center', fontsize=10, weight='bold')
    ax.text(10.9, 2.8, "Statistics\n& Insights", ha='center', va='center', fontsize=8)
    
    # Results summary at bottom
    result_box = FancyBboxPatch((0.5, 0.3), 11, 1.5, boxstyle="round,pad=0.1",
                                facecolor="#E8F5E9", edgecolor="#1B5E20", linewidth=2)
    ax.add_patch(result_box)
    ax.text(6, 1.5, "Key Results", ha='center', va='center', fontsize=12, weight='bold')
    ax.text(6, 1.0, "Detection: 100% accurate  |  Adaptation: 100% effective  |  Personality Match: 91.38% improvement", 
            ha='center', va='center', fontsize=9)
    ax.text(6, 0.5, "Effect Size (Cohen's d = 4.58) shows personality adaptation is highly impactful", 
            ha='center', va='center', fontsize=8, style='italic', color='#1B5E20')
    
    plt.tight_layout()
    plt.savefig(f"./figures/{filename}", bbox_inches='tight', facecolor='white', dpi=300)
    plt.close()
    print(f"✅ Created: {filename}")

def create_study_workflow_diagram(filename="11_study_workflow.png"):
    """
    A4-optimized study workflow - clean and easy to follow
    Target: 1900 × 1425 px (160 × 120 mm @ 300 DPI) for A4 embedding with readable fonts
    """
    fig, ax = plt.subplots(figsize=(9.5, 7.13), dpi=200)  # Results in ~1900×1426 px
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Title
    ax.text(6, 8.5, "Our Study: From Setup to Insights", fontsize=16, weight='bold', ha='center')
    ax.text(6, 8.1, "A clear path through the research process", fontsize=11, style='italic', ha='center', color='#666')
    
    # Color scheme
    color_setup = "#C8E6C9"
    color_execution = "#BBDEFB"
    color_validation = "#FFE0B2"
    color_results = "#F8BBD0"
    
    # Row 1: Study Setup
    ax.text(6, 7.4, "1  SETUP", fontsize=12, weight='bold', ha='center')
    
    box_agents = FancyBboxPatch((1, 6.5), 3, 0.7, boxstyle="round,pad=0.05",
                                facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_agents)
    ax.text(2.5, 6.85, "20 Agents\n(10 per personality type)", ha='center', va='center', fontsize=9)
    
    box_types = FancyBboxPatch((5, 6.5), 3, 0.7, boxstyle="round,pad=0.05",
                               facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_types)
    ax.text(6.5, 6.85, "2 Personality Types\n(Type A & Type B)", ha='center', va='center', fontsize=9)
    
    box_conditions = FancyBboxPatch((9, 6.5), 2.5, 0.7, boxstyle="round,pad=0.05",
                                    facecolor=color_setup, edgecolor="#2E7D32", linewidth=1.5)
    ax.add_patch(box_conditions)
    ax.text(10.25, 6.85, "2 Conditions\n(Reg vs Base)", ha='center', va='center', fontsize=9)
    
    # Arrow down
    arrow_down1 = FancyArrowPatch((6, 6.5), (6, 5.7), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down1)
    
    # Row 2: Execution
    ax.text(6, 5.4, "2  EXECUTION", fontsize=12, weight='bold', ha='center')
    
    box_dialogues = FancyBboxPatch((2, 4.5), 4, 0.7, boxstyle="round,pad=0.05",
                                   facecolor=color_execution, edgecolor="#1565C0", linewidth=1.5)
    ax.add_patch(box_dialogues)
    ax.text(4, 4.85, "120 Dialogues Generated\n(6 turns each, carefully controlled)", ha='center', va='center', fontsize=9)
    
    box_scoring = FancyBboxPatch((6.5, 4.5), 4, 0.7, boxstyle="round,pad=0.05",
                                 facecolor=color_execution, edgecolor="#1565C0", linewidth=1.5)
    ax.add_patch(box_scoring)
    ax.text(8.5, 4.85, "Scoring System\nYes (2) | Unsure (1) | No (0)", ha='center', va='center', fontsize=9)
    
    # Arrow down
    arrow_down2 = FancyArrowPatch((6, 4.5), (6, 3.7), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down2)
    
    # Row 3: Evaluation & Validation
    ax.text(6, 3.4, "3  EVALUATION", fontsize=12, weight='bold', ha='center')
    
    box_ai_eval = FancyBboxPatch((1.5, 2.3), 3.5, 0.9, boxstyle="round,pad=0.05",
                                 facecolor=color_validation, edgecolor="#E65100", linewidth=1.5)
    ax.add_patch(box_ai_eval)
    ax.text(3.25, 2.9, "AI Evaluator", ha='center', va='center', fontsize=10, weight='bold')
    ax.text(3.25, 2.5, "All 120 turns", ha='center', va='center', fontsize=8)
    
    box_human_val = FancyBboxPatch((5.5, 2.3), 3.5, 0.9, boxstyle="round,pad=0.05",
                                   facecolor=color_validation, edgecolor="#E65100", linewidth=1.5)
    ax.add_patch(box_human_val)
    ax.text(7.25, 2.9, "Human Experts", ha='center', va='center', fontsize=10, weight='bold')
    ax.text(7.25, 2.5, "30 sampled turns", ha='center', va='center', fontsize=8)
    
    # Validation metrics
    ax.text(3.25, 1.8, "κ = 0.89 (AI-Human)", ha='center', fontsize=8, style='italic', color='#333')
    ax.text(7.25, 1.8, "α = 0.82 (Human-Human)", ha='center', fontsize=8, style='italic', color='#333')
    
    # Arrow down
    arrow_down3 = FancyArrowPatch((6, 2.3), (6, 1.5), arrowstyle='->', lw=2, color="#666")
    ax.add_patch(arrow_down3)
    
    # Row 4: Results
    ax.text(6, 1.2, "4  RESULTS", fontsize=12, weight='bold', ha='center')
    
    result_box = FancyBboxPatch((0.5, 0.05), 11, 1.0, boxstyle="round,pad=0.05",
                                facecolor=color_results, edgecolor="#880E4F", linewidth=2)
    ax.add_patch(result_box)
    ax.text(6, 0.7, "Personality Adaptation Dramatically Improves Agent Performance", 
            ha='center', va='center', fontsize=10, weight='bold')
    ax.text(6, 0.3, "Personality Needs: Regulated 100% vs Baseline 8.62%  |  Cohen's d = 4.58 (p < 0.001)", 
            ha='center', va='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f"./figures/{filename}", bbox_inches='tight', facecolor='white', dpi=300)
    plt.close()
    print(f"✅ Created: {filename}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Creating A4-Optimized Diagrams (Dashed Lines Removed)")
    print("="*70 + "\n")
    
    create_system_overview_diagram()
    create_study_workflow_diagram()
    
    print("\n" + "="*70)
    print("✨ A4-OPTIMIZED DIAGRAMS CREATED SUCCESSFULLY")
    print("="*70)
    print("\n📊 Diagrams Created (Clean Look - No Dashed Lines):")
    print("  ✅ Figure 10: System Overview")
    print("  ✅ Figure 11: Study Workflow")
    print("\n💡 Changes:")
    print("  • Removed all dashed lines for cleaner appearance")
    print("  • Kept main flow connections clear")
    print("  • Maintained professional, clean layout")
    print("\n📁 Location: ./figures/")
    print("="*70 + "\n")
