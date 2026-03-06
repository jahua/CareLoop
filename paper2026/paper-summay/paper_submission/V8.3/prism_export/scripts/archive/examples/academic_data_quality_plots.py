#!/usr/bin/env python3
"""
Academic Data Quality Visualizations
=====================================

Best practices for data quality reporting in academic papers:
1. CONSORT-style flow diagram (for clinical/experimental studies)
2. Data completeness lollipop chart (Nature/Science style)
3. Missing data pattern matrix (widely used in epidemiology)
4. Sample characteristics summary (APA/MDPI style)

References:
- Schulz et al. (2010) CONSORT guidelines
- Sterne et al. (2009) Multiple imputation guidelines
- van Buuren (2018) Flexible Imputation of Missing Data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import seaborn as sns

# Publication-quality settings
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.unicode_minus': False,
})

# Color scheme (colorblind-friendly)
COLORS = {
    'regulated': '#0173B2',
    'baseline': '#DE8F05', 
    'complete': '#029E73',
    'missing': '#D55E00',
    'threshold': '#CC78BC',
    'grid': '#E5E5E5'
}


def create_consort_flow_diagram(output_path='figures/data_quality_consort.png'):
    """
    Create a CONSORT-style flow diagram showing sample flow.
    Widely used in clinical trials and experimental studies.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Box style
    box_style = dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='#333333', linewidth=1.5)
    
    # Enrollment
    ax.text(5, 9.5, 'Enrollment', fontsize=14, fontweight='bold', 
            ha='center', va='center')
    ax.annotate('', xy=(5, 9.2), xytext=(5, 9.4),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    
    # Initial pool
    ax.text(5, 8.5, 'Simulated Dialogues Generated\n(N = 20 sessions)', 
            fontsize=10, ha='center', va='center', bbox=box_style)
    
    # Split arrow
    ax.annotate('', xy=(2.5, 7.2), xytext=(5, 8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    ax.annotate('', xy=(7.5, 7.2), xytext=(5, 8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    
    # Allocation
    ax.text(5, 7.5, 'Allocation', fontsize=14, fontweight='bold', 
            ha='center', va='center')
    
    # Two arms
    ax.text(2.5, 6.5, 'Regulated Condition\n(n = 10 sessions)\n- 5 Type A profiles\n- 5 Type B profiles', 
            fontsize=9, ha='center', va='center', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E3F2FD', 
                     edgecolor=COLORS['regulated'], linewidth=2))
    
    ax.text(7.5, 6.5, 'Baseline Condition\n(n = 10 sessions)\n- 5 Type A profiles\n- 5 Type B profiles', 
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF3E0', 
                     edgecolor=COLORS['baseline'], linewidth=2))
    
    # Arrows down
    ax.annotate('', xy=(2.5, 5.2), xytext=(2.5, 5.8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    ax.annotate('', xy=(7.5, 5.2), xytext=(7.5, 5.8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    
    # Analysis section
    ax.text(5, 5.5, 'Analysis', fontsize=14, fontweight='bold', 
            ha='center', va='center')
    
    # Turns analyzed
    ax.text(2.5, 4.5, 'Assistant Turns Evaluated\nn = 59 (98.3%)\n\nExcluded: 1 turn\n(incomplete response)', 
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', 
                     edgecolor=COLORS['complete'], linewidth=1.5))
    
    ax.text(7.5, 4.5, 'Assistant Turns Evaluated\nn = 60 (100%)\n\nExcluded: 0 turns', 
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', 
                     edgecolor=COLORS['complete'], linewidth=1.5))
    
    # Final arrows
    ax.annotate('', xy=(2.5, 3.2), xytext=(2.5, 3.8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    ax.annotate('', xy=(7.5, 3.2), xytext=(7.5, 3.8),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.5))
    
    # Primary outcome
    ax.text(5, 3.5, 'Primary Outcome', fontsize=14, fontweight='bold', 
            ha='center', va='center')
    
    ax.text(2.5, 2.5, 'Personality Needs\nAddressed: 59/59\n(100%)', 
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='#333333', linewidth=1.5))
    
    ax.text(7.5, 2.5, 'Personality Needs\nAddressed: 5/58\n(8.6%)', 
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='#333333', linewidth=1.5))
    
    # Title
    ax.text(5, 10.2, 'Sample Flow Diagram', fontsize=14, fontweight='bold',
            ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


def create_completeness_lollipop(output_path='figures/data_quality_completeness.png'):
    """
    Create a lollipop chart showing data completeness by metric.
    This style is commonly used in Nature, Science, and medical journals.
    """
    # Data
    metrics = [
        'Emotional Tone',
        'Relevance & Coherence',
        'Personality Needs',
        'Detection Accurate',
        'Regulation Effective'
    ]
    
    regulated_pct = [100.0, 100.0, 100.0, 98.3, 100.0]
    baseline_pct = [100.0, 100.0, 96.7, None, None]  # None for N/A
    
    fig, ax = plt.subplots(figsize=(9, 5))
    
    y_pos = np.arange(len(metrics))
    
    # Plot regulated (circles)
    ax.hlines(y_pos, 0, regulated_pct, color=COLORS['regulated'], linewidth=2, alpha=0.7)
    ax.scatter(regulated_pct, y_pos, s=120, color=COLORS['regulated'], 
               zorder=3, label='Regulated', edgecolors='white', linewidths=1.5)
    
    # Plot baseline (squares) - only where available
    baseline_valid = [(i, p) for i, p in enumerate(baseline_pct) if p is not None]
    if baseline_valid:
        b_idx, b_pct = zip(*baseline_valid)
        ax.hlines(list(b_idx), 0, list(b_pct), color=COLORS['baseline'], 
                  linewidth=2, alpha=0.7, linestyle='--')
        ax.scatter(list(b_pct), list(b_idx), s=120, color=COLORS['baseline'],
                   marker='s', zorder=3, label='Baseline', edgecolors='white', linewidths=1.5)
    
    # Add N/A labels
    for i, p in enumerate(baseline_pct):
        if p is None:
            ax.text(50, i, 'N/A', ha='center', va='center', 
                    fontsize=9, color='#666666', style='italic')
    
    # Add percentage labels
    for i, (r, b) in enumerate(zip(regulated_pct, baseline_pct)):
        ax.text(r + 1.5, i + 0.15, f'{r:.1f}%', ha='left', va='center',
                fontsize=9, color=COLORS['regulated'], fontweight='bold')
        if b is not None:
            ax.text(b + 1.5, i - 0.15, f'{b:.1f}%', ha='left', va='center',
                    fontsize=9, color=COLORS['baseline'], fontweight='bold')
    
    # 95% threshold line
    ax.axvline(x=95, color=COLORS['threshold'], linestyle=':', 
               linewidth=2, alpha=0.8, label='95% threshold')
    ax.fill_betweenx([-0.5, len(metrics)-0.5], 95, 100, 
                      color=COLORS['complete'], alpha=0.1)
    
    # Styling
    ax.set_xlim(0, 108)
    ax.set_ylim(-0.5, len(metrics) - 0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics)
    ax.set_xlabel('Data Completeness (%)', fontweight='bold')
    ax.invert_yaxis()
    
    # Grid
    ax.xaxis.grid(True, linestyle='-', alpha=0.3, color=COLORS['grid'])
    ax.set_axisbelow(True)
    
    # Legend
    ax.legend(loc='lower right', framealpha=0.95, edgecolor='#cccccc')
    
    # Title
    ax.set_title('Data Completeness by Evaluation Metric', fontweight='bold', pad=15)
    
    # Annotation
    ax.text(0.98, 0.02, 'All metrics exceed 95% completeness threshold',
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=8, color='#666666', style='italic')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


def create_missing_pattern_matrix(df_regulated, df_baseline, 
                                   output_path='figures/data_quality_missing_pattern.png'):
    """
    Create a missing data pattern matrix (binary heatmap).
    Standard in epidemiology and clinical research papers.
    """
    # Combine key metrics
    metrics_reg = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                   'PERSONALITY NEEDS ADDRESSED', 'DETECTION ACCURATE', 
                   'REGULATION EFFECTIVE']
    metrics_base = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                    'PERSONALITY NEEDS ADDRESSED']
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for idx, (df, metrics, title, color) in enumerate([
        (df_regulated, metrics_reg, 'Regulated (n=59)', COLORS['regulated']),
        (df_baseline, metrics_base, 'Baseline (n=60)', COLORS['baseline'])
    ]):
        ax = axes[idx]
        
        # Create missingness matrix (1 = present, 0 = missing)
        available_metrics = [m for m in metrics if m in df.columns]
        if available_metrics:
            missing_matrix = df[available_metrics].notna().astype(int).values
            
            # Plot heatmap
            cmap = plt.cm.colors.ListedColormap(['#FFCCCC', '#CCE5CC'])
            im = ax.imshow(missing_matrix, aspect='auto', cmap=cmap, 
                          interpolation='nearest')
            
            # Labels
            short_labels = [m.replace(' APPROPRIATE', '').replace(' ADDRESSED', '')
                           .replace('DETECTION ', 'DET.').replace('REGULATION ', 'REG.')
                           .title() for m in available_metrics]
            ax.set_xticks(range(len(short_labels)))
            ax.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=8)
            ax.set_ylabel('Observation', fontsize=10)
            ax.set_title(title, fontweight='bold', pad=10, color=color)
            
            # Add completeness summary below
            completeness = missing_matrix.mean(axis=0) * 100
            for i, c in enumerate(completeness):
                ax.text(i, len(df) + 1, f'{c:.0f}%', ha='center', va='top',
                       fontsize=8, fontweight='bold', color=COLORS['complete'])
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='#CCE5CC', edgecolor='gray', label='Present'),
        mpatches.Patch(facecolor='#FFCCCC', edgecolor='gray', label='Missing')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=2, 
               frameon=True, bbox_to_anchor=(0.5, -0.02))
    
    plt.suptitle('Missing Data Pattern Matrix', fontweight='bold', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


def create_sample_summary_figure(output_path='figures/data_quality_summary.png'):
    """
    Create a comprehensive sample summary figure.
    Combines key information in a single visualization.
    """
    fig = plt.figure(figsize=(12, 6))
    
    # Create grid
    gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
    
    # Panel A: Sample sizes
    ax1 = fig.add_subplot(gs[0, 0])
    conditions = ['Regulated', 'Baseline']
    sizes = [59, 60]
    bars = ax1.bar(conditions, sizes, color=[COLORS['regulated'], COLORS['baseline']],
                   edgecolor='white', linewidth=2)
    ax1.set_ylabel('N (turns)')
    ax1.set_title('A. Sample Size', fontweight='bold')
    ax1.set_ylim(0, 70)
    for bar, size in zip(bars, sizes):
        ax1.text(bar.get_x() + bar.get_width()/2, size + 1, str(size),
                ha='center', va='bottom', fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Panel B: Profile distribution
    ax2 = fig.add_subplot(gs[0, 1])
    profiles = ['Type A\n(all +1 traits)', 'Type B\n(all -1 traits)']
    counts = [5, 5]
    ax2.bar(profiles, counts, color=['#4CAF50', '#F44336'], edgecolor='white', linewidth=2)
    ax2.set_ylabel('N (conversations)')
    ax2.set_title('B. Personality Profiles', fontweight='bold')
    ax2.set_ylim(0, 7)
    for i, c in enumerate(counts):
        ax2.text(i, c + 0.2, f'n={c}', ha='center', fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Panel C: 2x2 Factorial Design Matrix
    ax3 = fig.add_subplot(gs[0, 2])
    design_matrix = np.array([[5, 5], [5, 5]])
    im = ax3.imshow(design_matrix, cmap='Blues', aspect='auto', vmin=0, vmax=10)
    ax3.set_xticks([0, 1])
    ax3.set_xticklabels(['Regulated', 'Baseline'], fontsize=8)
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['Type A', 'Type B'], fontsize=8)
    ax3.set_title('C. 2x2 Design Matrix', fontweight='bold')
    for i in range(2):
        for j in range(2):
            ax3.text(j, i, 'n=5', ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=10)
    
    # Panel D: Completeness comparison (bottom span)
    ax4 = fig.add_subplot(gs[1, :])
    
    metrics = ['Emotional\nTone', 'Relevance &\nCoherence', 'Personality\nNeeds', 
               'Detection\nAccurate', 'Regulation\nEffective']
    reg_complete = [100, 100, 100, 98.3, 100]
    base_complete = [100, 100, 96.7, 0, 0]  # 0 for N/A
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, reg_complete, width, label='Regulated',
                    color=COLORS['regulated'], edgecolor='white', linewidth=1.5)
    bars2 = ax4.bar(x + width/2, base_complete, width, label='Baseline',
                    color=COLORS['baseline'], edgecolor='white', linewidth=1.5)
    
    # Mark N/A
    for i in [3, 4]:
        ax4.text(x[i] + width/2, 5, 'N/A', ha='center', va='bottom',
                fontsize=8, color='#666666', style='italic')
    
    ax4.axhline(y=95, color=COLORS['threshold'], linestyle='--', linewidth=1.5,
                label='95% threshold')
    ax4.set_ylabel('Completeness (%)')
    ax4.set_title('D. Data Completeness by Metric', fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(metrics)
    ax4.set_ylim(0, 110)
    ax4.legend(loc='lower right', framealpha=0.95)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    
    plt.suptitle('Sample Characteristics and Data Quality', fontweight='bold', 
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")
    plt.close()


def generate_all_data_quality_figures(df_regulated=None, df_baseline=None, output_dir='figures'):
    """
    Generate all publication-quality data quality figures.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print("GENERATING ACADEMIC DATA QUALITY FIGURES")
    print("="*70 + "\n")
    
    # 1. CONSORT-style flow diagram
    print("1. CONSORT-style Flow Diagram...")
    create_consort_flow_diagram(f'{output_dir}/data_quality_consort.png')
    
    # 2. Completeness lollipop chart
    print("2. Completeness Lollipop Chart...")
    create_completeness_lollipop(f'{output_dir}/data_quality_completeness.png')
    
    # 3. Missing pattern matrix (requires data)
    if df_regulated is not None and df_baseline is not None:
        print("3. Missing Pattern Matrix...")
        create_missing_pattern_matrix(df_regulated, df_baseline,
                                       f'{output_dir}/data_quality_missing_pattern.png')
    
    # 4. Comprehensive summary figure
    print("4. Sample Summary Figure...")
    create_sample_summary_figure(f'{output_dir}/data_quality_summary.png')
    
    print("\n" + "="*70)
    print("? All data quality figures generated!")
    print("="*70)


if __name__ == '__main__':
    generate_all_data_quality_figures()
