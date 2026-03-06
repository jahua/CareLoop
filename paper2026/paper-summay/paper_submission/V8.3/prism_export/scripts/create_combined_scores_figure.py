#!/usr/bin/env python3
"""
Create combined Figure 8+9: Weighted Scores and Total Score Distribution
Merges bar chart and boxplot into a single publication-quality figure
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from visualization_config import PublicationStandards as C
    from enhanced_statistical_analysis import (
        create_enhanced_boxplot, 
        style_publication_axes,
        style_legend_guide,
        save_figure_multi_format,
        analyze_weighted_scores
    )
except ImportError:
    print("⚠️  Warning: Using fallback configuration")
    # Fallback configuration
    class C:
        FIGURE_WIDTH_SINGLE = 7
        FIGURE_HEIGHT_MEDIUM = 5
        COLOR_REGULATED = '#4472C4'
        COLOR_BASELINE = '#ED7D31'

def create_combined_weighted_and_total_scores(df_reg_scored, df_base_scored, output_dir="figures"):
    """
    Create combined figure with weighted scores (bar chart) and total score (boxplot).
    
    Layout: 1 row x 2 columns
    - Left panel: Weighted scores for 3 metrics
    - Right panel: Total score boxplot
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("COMBINED WEIGHTED SCORES + TOTAL SCORE VISUALIZATION")
    print("="*80)
    
    # Create figure with 2 subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(C.FIGURE_WIDTH_SINGLE * 1.8, C.FIGURE_HEIGHT_MEDIUM), 
                                    dpi=150, gridspec_kw={'width_ratios': [1.2, 0.8]})
    
    # ==================== LEFT PANEL: WEIGHTED SCORES (BAR CHART) ====================
    
    common_scores = ['Emotional_Tone_Score', 'Relevance_Coherence_Score', 'Personality_Needs_Score']
    score_labels = ['Emotional\nTone', 'Relevance &\nCoherence', 'Personality\nNeeds']
    
    x_pos = np.arange(len(common_scores))
    width = 0.35
    
    reg_means = [df_reg_scored[score].mean() for score in common_scores]
    reg_stds = [df_reg_scored[score].std() for score in common_scores]
    base_means = [df_base_scored[score].mean() for score in common_scores]
    base_stds = [df_base_scored[score].std() for score in common_scores]
    
    # Create bars
    bars1 = ax1.bar(
        x_pos - width/2,
        reg_means,
        width,
        yerr=reg_stds,
        label='Regulated',
        color=C.COLOR_REGULATED,
        alpha=0.85,
        edgecolor='0.3',
        linewidth=1.5,
        capsize=4,
        error_kw={'linewidth': 1.5, 'ecolor': '0.3'},
    )
    bars2 = ax1.bar(
        x_pos + width/2,
        base_means,
        width,
        yerr=base_stds,
        label='Baseline',
        color=C.COLOR_BASELINE,
        alpha=0.85,
        edgecolor='0.3',
        linewidth=1.5,
        capsize=4,
        error_kw={'linewidth': 1.5, 'ecolor': '0.3'},
    )
    
    # Styling for left panel
    style_publication_axes(ax1, grid_axis='y', remove_spines=True, offset_spines=True)
    
    # Add value labels above bars
    for bar, mean, std in zip(bars1, reg_means, reg_stds):
        label_y = mean + std + 0.12
        ax1.text(bar.get_x() + bar.get_width()/2, label_y,
                f'{mean:.2f}', ha='center', va='bottom', fontweight='bold', 
                fontsize=8, color='0.2')
    
    for bar, mean, std in zip(bars2, base_means, base_stds):
        label_y = mean + std + 0.12
        ax1.text(bar.get_x() + bar.get_width()/2, label_y,
                f'{mean:.2f}', ha='center', va='bottom', fontweight='bold', 
                fontsize=8, color='0.2')
    
    ax1.set_xlabel('Evaluation Metric', fontsize=9, fontweight='bold')
    ax1.set_ylabel('Weighted Score (0–2 scale)', fontsize=9, fontweight='bold')
    ax1.set_title('(a) Component Scores', fontsize=10, fontweight='bold', pad=15)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(score_labels, fontsize=9)
    ax1.set_ylim([0, 2.5])
    
    # Legend for left panel
    legend = ax1.legend(fontsize=9, frameon=True, loc='lower left')
    style_legend_guide(legend, style='gray')
    
    # ==================== RIGHT PANEL: TOTAL SCORE (BOXPLOT) ====================
    
    total_data = [
        df_reg_scored['Total_Regulated_Score'].values,
        df_base_scored['Total_Baseline_Score'].values
    ]
    
    # Create enhanced boxplot
    bp = create_enhanced_boxplot(
        ax2,
        data=total_data,
        positions=[1, 2],
        labels=['Regulated', 'Baseline'],
        colors=[C.COLOR_REGULATED, C.COLOR_BASELINE],
        show_means=True,
        show_outliers=True
    )
    
    # Styling for right panel
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.get_xaxis().tick_bottom()
    ax2.get_yaxis().tick_left()
    ax2.tick_params(axis='x', direction='out')
    ax2.tick_params(axis='y', length=0)
    ax2.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
    ax2.set_axisbelow(True)
    
    # Add statistical annotations
    means = [np.mean(data) for data in total_data]
    medians = [np.median(data) for data in total_data]
    
    for i, (mean, median) in enumerate(zip(means, medians)):
        # Mean annotation
        ax2.text(i+1, mean + 0.35, f'μ={mean:.2f}', ha='center', 
                fontweight='bold', fontsize=8, color='0.2')
        # Median annotation
        ax2.text(i+1.3, median, f'M={median:.2f}', ha='left', va='center',
                fontweight='normal', fontsize=8, color='0.4',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='0.7', linewidth=0.5))
    
    ax2.set_xlabel('Condition', fontsize=9, fontweight='bold')
    ax2.set_ylabel('Total Score (0–6 scale)', fontsize=9, fontweight='bold')
    ax2.set_title('(b) Total Score Distribution', fontsize=10, fontweight='bold', pad=15)
    ax2.set_ylim([0, 6.5])
    ax2.set_xlim([0.5, 2.5])
    
    # Overall title
    fig.suptitle('Weighted Scores: Regulated vs Baseline', 
                fontsize=12, fontweight='bold', y=0.98)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save in multiple formats
    save_figure_multi_format(fig, "08_09_combined_scores", output_dir)
    plt.close()
    
    print(f"\n✓ Saved combined figure: 08_09_combined_scores.{{png,pdf}}")
    print(f"  Left panel: Component weighted scores (bar chart)")
    print(f"  Right panel: Total score distribution (boxplot)")


def main():
    """Generate combined weighted scores figure"""
    print("="*80)
    print("COMBINED SCORES FIGURE GENERATION")
    print("="*80)
    print("\nMerging Figure 8 + Figure 9 into a single publication-quality figure")
    print("Layout: [Component Scores | Total Score Distribution]\n")
    
    # Load data
    data_dir = 'data/merged'
    
    # Try different paths
    reg_candidates = [
        os.path.join(data_dir, 'regulated.csv'),
        'data/merged/regulated.csv',
        '../data/merged/regulated.csv',
    ]
    base_candidates = [
        os.path.join(data_dir, 'baseline.csv'),
        'data/merged/baseline.csv',
        '../data/merged/baseline.csv',
    ]
    
    reg_path = next((p for p in reg_candidates if os.path.exists(p)), None)
    base_path = next((p for p in base_candidates if os.path.exists(p)), None)
    
    if not reg_path or not base_path:
        print("❌ Error: Data files not found")
        print(f"   Tried: {reg_candidates[0]}")
        return
    
    print(f"Loading data:")
    print(f"  Regulated: {reg_path}")
    print(f"  Baseline: {base_path}")
    
    df_reg = pd.read_csv(reg_path)
    df_base = pd.read_csv(base_path)
    
    # Use the analyze_weighted_scores function to properly convert and score the data
    df_reg_scored, df_base_scored = analyze_weighted_scores(df_reg, df_base)
    
    print(f"\nDataset statistics:")
    print(f"  Regulated: {len(df_reg_scored)} conversations")
    print(f"  Baseline: {len(df_base_scored)} conversations")
    
    # Create combined figure
    output_dir = 'figures'
    os.makedirs(output_dir, exist_ok=True)
    
    create_combined_weighted_and_total_scores(df_reg_scored, df_base_scored, output_dir)
    
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  ✓ figures/08_09_combined_scores.png")
    print("  ✓ figures/08_09_combined_scores.pdf")
    print("\nBenefits of merged figure:")
    print("  • Saves space in manuscript")
    print("  • Easier side-by-side comparison")
    print("  • Shows both detail and summary in one view")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    main()
