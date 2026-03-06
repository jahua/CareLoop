#!/usr/bin/env python3
"""
Example Script: Publication-Quality Plotting
Demonstrates the improved plotting functions and best practices
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Import our enhanced configuration
from visualization_config import (
    configure_matplotlib, 
    PUBLICATION_CONFIG as C,
    PlotStyler,
    get_figure_size_for_journal,
    save_figure_multi_format
)

# Configure matplotlib with guide's exact standards
# Set to True to use matplotlib_for_papers exact params (8pt labels, 10pt legend, etc.)
configure_matplotlib(use_matplotlib_papers_defaults=True)

# Import enhanced plotting functions
import sys
sys.path.insert(0, '.')
from enhanced_statistical_analysis import (
    style_publication_axes,
    create_enhanced_boxplot,
    add_significance_bar,
    save_figure_multi_format,
    style_legend_guide
)


def example_1_simple_bar_chart():
    """Example 1: Clean bar chart with publication styling"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Bar Chart")
    print("="*70)
    
    # Data
    categories = ['Baseline', 'Treatment A', 'Treatment B']
    values = [23.5, 45.2, 32.8]
    errors = [2.1, 3.5, 2.8]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    
    # Create bars with default colorblind-friendly colors
    colors = [C.COLOR_BASELINE, C.COLOR_REGULATED, C.COLOR_POSITIVE]
    bars = ax.bar(
        categories, 
        values, 
        yerr=errors,
        color=colors,
        alpha=0.85,
        edgecolor='0.3',
        linewidth=1.5,
        capsize=4,
        error_kw={'linewidth': 1.5, 'ecolor': '0.3'}
    )
    
    # Apply guide styling (exact from matplotlib_for_papers)
    style_publication_axes(ax, grid_axis='y', offset_spines=True)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1,
               f'{val:.1f}',
               ha='center', va='bottom', fontweight='bold',
               fontsize=8, color='0.2')
    
    # Labels (guide font sizes: 8pt for labels)
    ax.set_ylabel('Response Score', fontsize=8, fontweight='bold')
    ax.set_xlabel('Condition', fontsize=8, fontweight='bold')
    ax.set_title('Treatment Comparison', fontsize=10, fontweight='bold', pad=15)
    ax.set_ylim(0, max(values) + max(errors) + 5)
    
    # Add legend (guide style: gray background)
    legend = ax.legend(fontsize=10, loc='upper left')
    style_legend_guide(legend, style='gray')
    
    plt.tight_layout()
    
    # Save in multiple formats
    save_figure_multi_format(fig, "example_1_bar_chart", 
                           output_dir="figures/examples")
    print("? Saved: example_1_bar_chart.{png,pdf}")
    plt.close()


def example_2_enhanced_boxplot():
    """Example 2: Enhanced boxplot with statistical testing"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Enhanced Boxplot with Significance")
    print("="*70)
    
    # Generate sample data
    np.random.seed(42)
    control = np.random.normal(5.0, 1.2, 50)
    treatment = np.random.normal(6.5, 1.3, 50)
    
    # Statistical test
    t_stat, p_value = stats.ttest_ind(control, treatment)
    print(f"  t-statistic: {t_stat:.3f}")
    print(f"  p-value: {p_value:.4f}")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    
    # Create enhanced boxplot with default colors
    bp = create_enhanced_boxplot(
        ax,
        data=[control, treatment],
        positions=[1, 2],
        labels=['Control', 'Treatment'],
        colors=[C.COLOR_BASELINE, C.COLOR_REGULATED],
        show_means=True,
        show_outliers=True
    )
    
    # Apply guide styling (removes left spine for boxplots)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.tick_params(axis='x', direction='out')
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
    ax.set_axisbelow(True)
    
    # Add significance bar (guide's annotate method)
    y_max = max(control.max(), treatment.max())
    add_significance_bar(ax, 1, 2, y_max + 0.8, p_value)
    
    # Add sample sizes
    PlotStyler.add_sample_size_labels(ax, [1, 2], [len(control), len(treatment)])
    
    # Labels (guide font sizes: 8pt labels, 10pt title)
    ax.set_ylabel('Score (arbitrary units)', fontsize=8, fontweight='bold')
    ax.set_xlabel('Condition', fontsize=8, fontweight='bold')
    ax.set_title('Effect of Treatment on Score', fontsize=10, fontweight='bold', pad=15)
    ax.set_ylim(0, y_max + 2)
    ax.set_xlim(0.5, 2.5)
    
    # Guide-style legend (gray background)
    legend = ax.legend(fontsize=10, frameon=True, loc='upper left')
    style_legend_guide(legend, style='gray')
    
    # Adjust spacing (guide recommendation for y-labels)
    plt.subplots_adjust(left=0.2)
    
    plt.tight_layout()
    
    # Save
    save_figure_multi_format(fig, "example_2_boxplot",
                           output_dir="figures/examples")
    print("? Saved: example_2_boxplot.{png,pdf}")
    plt.close()


def example_3_paired_data():
    """Example 3: Paired data with connecting lines"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Paired Data Visualization")
    print("="*70)
    
    # Generate paired data
    np.random.seed(42)
    n_pairs = 15
    pre = np.random.normal(50, 10, n_pairs)
    post = pre + np.random.normal(15, 8, n_pairs)  # Positive effect
    
    # Statistical test (paired)
    t_stat, p_value = stats.ttest_rel(pre, post)
    print(f"  Paired t-statistic: {t_stat:.3f}")
    print(f"  p-value: {p_value:.4f}")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(5, 6), dpi=150)
    
    # Plot connecting lines
    for i in range(n_pairs):
        ax.plot([0, 1], [pre[i], post[i]], 
               color='0.7', alpha=0.4, linewidth=0.8, zorder=1)
    
    # Plot individual points with default colors
    ax.scatter([0]*n_pairs, pre, color=C.COLOR_BASELINE, 
              s=60, alpha=0.7, edgecolors='white', linewidths=1.5,
              zorder=3, label='Pre-treatment')
    ax.scatter([1]*n_pairs, post, color=C.COLOR_REGULATED,
              s=60, alpha=0.7, edgecolors='white', linewidths=1.5,
              zorder=3, label='Post-treatment')
    
    # Add mean line (bold for emphasis)
    mean_pre = np.mean(pre)
    mean_post = np.mean(post)
    ax.plot([0, 1], [mean_pre, mean_post],
           color='black', linewidth=2.5, alpha=0.8, zorder=2)
    
    # Mean markers
    ax.scatter([0], [mean_pre], color=C.COLOR_BASELINE,
              s=120, marker='D', edgecolor='white', linewidths=2, zorder=4)
    ax.scatter([1], [mean_post], color=C.COLOR_REGULATED,
              s=120, marker='D', edgecolor='white', linewidths=2, zorder=4)
    
    # Apply guide styling
    style_publication_axes(ax, grid_axis='y', offset_spines=True)
    
    # Add significance (guide's annotate method)
    y_max = max(pre.max(), post.max())
    add_significance_bar(ax, 0, 1, y_max + 5, p_value)
    
    # Labels (guide font sizes)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Pre', 'Post'], fontsize=10)
    ax.set_ylabel('Score', fontsize=8, fontweight='bold')
    ax.set_title('Treatment Effect (Paired Data)', 
                fontsize=10, fontweight='bold', pad=15)
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(0, y_max + 10)
    
    # Guide-style legend (gray background)
    legend = ax.legend(fontsize=10, frameon=True, loc='upper left')
    style_legend_guide(legend, style='gray')
    
    plt.tight_layout()
    
    # Save
    save_figure_multi_format(fig, "example_3_paired",
                           output_dir="figures/examples")
    print("? Saved: example_3_paired.{png,pdf}")
    plt.close()


def example_4_multi_panel():
    """Example 4: Multi-panel figure with consistent styling"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Multi-Panel Figure")
    print("="*70)
    
    # Generate data
    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
    y2 = np.cos(x) + np.random.normal(0, 0.1, 100)
    y3 = np.sin(x) * np.cos(x) + np.random.normal(0, 0.1, 100)
    
    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), dpi=150)
    
    data_sets = [
        (y1, 'sin(x)', C.COLOR_REGULATED),
        (y2, 'cos(x)', C.COLOR_BASELINE),
        (y3, 'sin(x)*cos(x)', C.COLOR_POSITIVE)
    ]
    
    for ax, (y, label, color) in zip(axes, data_sets):
        # Plot (guide: linewidth=2)
        ax.plot(x, y, color=color, linewidth=2, alpha=0.8, label=label)
        ax.scatter(x[::10], y[::10], color=color, s=30, alpha=0.6,
                  edgecolors='white', linewidths=1, zorder=3)
        
        # Apply guide styling
        style_publication_axes(ax, grid_axis='both', offset_spines=True)
        
        # Labels (guide font sizes)
        ax.set_xlabel('x', fontsize=8, fontweight='bold')
        ax.set_ylabel('y', fontsize=8, fontweight='bold')
        ax.set_title(label, fontsize=10, fontweight='bold', pad=10)
        
        # Legend (guide style: gray background)
        legend = ax.legend(fontsize=10, frameon=True, loc='best')
        style_legend_guide(legend, style='gray')
    
    # Panel labels
    for i, ax in enumerate(axes):
        ax.text(-0.15, 1.05, chr(65+i), transform=ax.transAxes,
               fontsize=C.FONT_SIZE_TITLE, fontweight='bold',
               va='top', ha='right')
    
    plt.tight_layout()
    
    # Save
    save_figure_multi_format(fig, "example_4_multi_panel",
                           output_dir="figures/examples")
    print("? Saved: example_4_multi_panel.{png,pdf}")
    plt.close()


def example_5_journal_sizing():
    """Example 5: Journal-specific figure sizing"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Journal-Specific Figure Sizes")
    print("="*70)
    
    journals = ['nature', 'science', 'plos', 'mdpi']
    
    for journal in journals:
        # Get journal-specific size
        figsize = get_figure_size_for_journal(journal=journal, columns=1, aspect=0.7)
        
        print(f"\n  {journal.upper()}: {figsize[0]:.2f}\" ? {figsize[1]:.2f}\"")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize, dpi=150)
        
        # Simple plot with default color
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x)
        ax.plot(x, y, color=C.COLOR_REGULATED, linewidth=2)
        
        # Styling
        style_publication_axes(ax, grid_axis='both')
        
        # Labels
        ax.set_xlabel('x', fontweight='bold')
        ax.set_ylabel('sin(x)', fontweight='bold')
        ax.set_title(f'{journal.upper()} Format\n({figsize[0]:.1f}\" ? {figsize[1]:.1f}\")',
                    fontweight='bold', pad=10)
        
        plt.tight_layout()
        
        # Save
        save_figure_multi_format(fig, f"example_5_journal_{journal}",
                               output_dir="figures/examples", verbose=False)
        plt.close()
    
    print("\n? Saved: example_5_journal_*.{png,pdf}")


def main():
    """Run all examples"""
    import os
    os.makedirs("figures/examples", exist_ok=True)
    
    print("="*70)
    print("PUBLICATION-QUALITY PLOTTING EXAMPLES")
    print("="*70)
    print("\nGenerating example figures demonstrating best practices...")
    
    example_1_simple_bar_chart()
    example_2_enhanced_boxplot()
    example_3_paired_data()
    example_4_multi_panel()
    example_5_journal_sizing()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\nGenerated files in: figures/examples/")
    print("  - Each example saved as both PNG and PDF")
    print("  - PNG for viewing, PDF for publication")
    print("\nNext steps:")
    print("  1. Review the generated figures")
    print("  2. Compare PNG vs PDF quality")
    print("  3. Try opening PDFs in Adobe Illustrator for editing")
    print("  4. Include PDFs in your LaTeX document")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
