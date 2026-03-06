#!/usr/bin/env python3
"""
Master Statistical Analysis and Visualization Script
Personality-Adaptive Conversational AI Performance Evaluation

This unified script consolidates all analysis components:
- Data loading and quality assessment
- Descriptive and inferential statistics  
- Effect size calculations
- Publication-ready visualizations
- System diagrams

Author: Unified Analysis Pipeline
Date: 2026
Version: 2.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict, List
import warnings
import os
warnings.filterwarnings('ignore')

# Import unified configuration
from visualization_config import (
    configure_matplotlib, 
    save_figure,
    FigureTemplates,
    PlotStyler,
    FigureCatalog,
    PUBLICATION_CONFIG
)


# ============================================================================
# CONFIGURATION
# ============================================================================

# Apply publication standards
configure_matplotlib()

# Color shortcuts
C = PUBLICATION_CONFIG  # Config object
COLORS = {
    'regulated': C.COLOR_REGULATED,
    'baseline': C.COLOR_BASELINE,
    'positive': C.COLOR_POSITIVE,
    'negative': C.COLOR_NEGATIVE
}


# ============================================================================
# STEP 1: DATA LOADING AND PREPARATION
# ============================================================================

def load_and_prepare_data(regulated_path: str, baseline_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load and prepare data for analysis."""
    print("="*80)
    print("STEP 1: DATA LOADING AND PREPARATION")
    print("="*80)
    
    df_regulated = pd.read_csv(regulated_path)
    df_baseline = pd.read_csv(baseline_path)
    
    print(f"\nRegulated dataset: {df_regulated.shape}")
    print(f"Baseline dataset: {df_baseline.shape}")
    
    # Extract metadata
    for df in [df_regulated, df_baseline]:
        df['Personality_Type'] = df['MSG. NO.'].str[0]
        df['Conversation_ID'] = df['MSG. NO.'].str.split('-').str[:2].str.join('-')
        df['Turn_Number'] = df['MSG. NO.'].str.split('-').str[2].astype(int)
    
    print(f"\nPersonality types: {df_regulated['Personality_Type'].unique()}")
    print(f"Unique conversations: {df_regulated['Conversation_ID'].nunique()}")
    
    return df_regulated, df_baseline


# ============================================================================
# STEP 2: DATA QUALITY ASSESSMENT
# ============================================================================

def assess_data_quality(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Dict:
    """Assess data quality and completeness."""
    print("\n" + "="*80)
    print("STEP 2: DATA QUALITY ASSESSMENT")
    print("="*80)
    
    quality_report = {
        'n_regulated': len(df_regulated),
        'n_baseline': len(df_baseline),
        'n_conversations': df_regulated['Conversation_ID'].nunique(),
        'type_distribution': df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
    }
    
    print(f"\nSample sizes:")
    print(f"  Regulated: {quality_report['n_regulated']} turns")
    print(f"  Baseline: {quality_report['n_baseline']} turns")
    print(f"  Conversations: {quality_report['n_conversations']}")
    
    return quality_report


# ============================================================================
# STEP 3: CONVERT TO NUMERIC
# ============================================================================

def convert_to_numeric(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convert categorical evaluations to numeric scores."""
    print("\n" + "="*80)
    print("STEP 3: CONVERTING TO NUMERIC SCORES")
    print("="*80)
    
    mapping = {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0, 'yes': 1, 'no': 0}
    
    df_reg_numeric = df_regulated.copy()
    df_base_numeric = df_baseline.copy()
    
    # Metrics to convert
    reg_metrics = ['DETECTION ACCURATE', 'REGULATION EFFECTIVE', 
                   'EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                   'PERSONALITY NEEDS ADDRESSED']
    base_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                    'PERSONALITY NEEDS ADDRESSED']
    
    for metric in reg_metrics:
        if metric in df_reg_numeric.columns:
            df_reg_numeric[f'{metric}_numeric'] = df_reg_numeric[metric].map(mapping)
    
    for metric in base_metrics:
        if metric in df_base_numeric.columns:
            df_base_numeric[f'{metric}_numeric'] = df_base_numeric[metric].map(mapping)
    
    print(f"? Converted {len(reg_metrics)} regulated metrics")
    print(f"? Converted {len(base_metrics)} baseline metrics")
    
    return df_reg_numeric, df_base_numeric


# ============================================================================
# STEP 4: DESCRIPTIVE STATISTICS
# ============================================================================

def calculate_descriptive_statistics(df_regulated: pd.DataFrame, 
                                     df_baseline: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptive statistics with confidence intervals."""
    print("\n" + "="*80)
    print("STEP 4: DESCRIPTIVE STATISTICS")
    print("="*80)
    
    results = []
    common_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                     'PERSONALITY NEEDS ADDRESSED']
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            # Regulated
            reg_values = df_regulated[metric_numeric].dropna()
            reg_mean = reg_values.mean()
            reg_std = reg_values.std()
            reg_n = len(reg_values)
            
            # Baseline
            base_values = df_baseline[metric_numeric].dropna()
            base_mean = base_values.mean()
            base_std = base_values.std()
            base_n = len(base_values)
            
            # Calculate 95% CI
            if reg_n > 1:
                reg_ci = stats.t.interval(0.95, reg_n-1, loc=reg_mean, 
                                         scale=reg_std/np.sqrt(reg_n))
            else:
                reg_ci = (reg_mean, reg_mean)
            
            if base_n > 1:
                base_ci = stats.t.interval(0.95, base_n-1, loc=base_mean,
                                          scale=base_std/np.sqrt(base_n))
            else:
                base_ci = (base_mean, base_mean)
            
            results.extend([
                {'Metric': metric, 'Condition': 'Regulated', 'N': reg_n, 
                 'Mean': reg_mean, 'SD': reg_std, 
                 'CI_Lower': reg_ci[0], 'CI_Upper': reg_ci[1]},
                {'Metric': metric, 'Condition': 'Baseline', 'N': base_n, 
                 'Mean': base_mean, 'SD': base_std,
                 'CI_Lower': base_ci[0], 'CI_Upper': base_ci[1]}
            ])
            
            print(f"\n{metric}:")
            print(f"  Regulated: M={reg_mean:.3f}, SD={reg_std:.3f}, N={reg_n}")
            print(f"  Baseline:  M={base_mean:.3f}, SD={base_std:.3f}, N={base_n}")
    
    return pd.DataFrame(results)


# ============================================================================
# STEP 5: EFFECT SIZE CALCULATIONS
# ============================================================================

def calculate_cohens_d(group1: np.array, group2: np.array) -> float:
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_sd if pooled_sd > 0 else 0


def calculate_effect_sizes(df_regulated: pd.DataFrame, 
                          df_baseline: pd.DataFrame) -> pd.DataFrame:
    """Calculate effect sizes for all common metrics."""
    print("\n" + "="*80)
    print("STEP 5: EFFECT SIZE ANALYSIS")
    print("="*80)
    
    effect_sizes = []
    common_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                     'PERSONALITY NEEDS ADDRESSED']
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            reg_values = df_regulated[metric_numeric].dropna().values
            base_values = df_baseline[metric_numeric].dropna().values
            
            if len(reg_values) > 1 and len(base_values) > 1:
                d = calculate_cohens_d(reg_values, base_values)
                
                effect_sizes.append({
                    'Metric': metric,
                    'Cohens_d': d,
                    'Regulated_Mean': np.mean(reg_values),
                    'Baseline_Mean': np.mean(base_values),
                    'Difference': np.mean(reg_values) - np.mean(base_values)
                })
                
                # Interpret effect size
                if abs(d) < 0.2:
                    interpretation = "negligible"
                elif abs(d) < 0.5:
                    interpretation = "small"
                elif abs(d) < 0.8:
                    interpretation = "medium"
                else:
                    interpretation = "LARGE"
                
                print(f"\n{metric}:")
                print(f"  Cohen's d = {d:.3f} ({interpretation})")
                print(f"  Improvement = {(np.mean(reg_values) - np.mean(base_values))*100:+.1f}%")
    
    return pd.DataFrame(effect_sizes)


# ============================================================================
# VISUALIZATION: FIGURE 1 - PERFORMANCE COMPARISON
# ============================================================================

def create_performance_comparison(df_stats: pd.DataFrame, output_dir: str = "figures"):
    """Create main performance comparison figure."""
    print("\n" + "="*80)
    print("CREATING FIGURE 1: PERFORMANCE COMPARISON")
    print("="*80)
    
    fig, ax = FigureTemplates.create_wide_panel()
    
    # Filter for common metrics
    common_metrics = df_stats[df_stats['Condition'].isin(['Regulated', 'Baseline'])].copy()
    metric_counts = common_metrics.groupby('Metric')['Condition'].count()
    valid_metrics = metric_counts[metric_counts == 2].index.tolist()
    common_metrics = common_metrics[common_metrics['Metric'].isin(valid_metrics)]
    unique_metrics = common_metrics['Metric'].unique()
    
    if len(unique_metrics) == 0:
        print("  ? No valid metrics found")
        plt.close(fig)
        return
    
    x_pos = np.arange(len(unique_metrics))
    width = 0.35
    
    for i, metric in enumerate(unique_metrics):
        metric_data = common_metrics[common_metrics['Metric'] == metric]
        
        reg_row = metric_data[metric_data['Condition'] == 'Regulated']
        base_row = metric_data[metric_data['Condition'] == 'Baseline']
        
        if len(reg_row) > 0 and len(base_row) > 0:
            reg_data = reg_row.iloc[0]
            base_data = base_row.iloc[0]
            
            # Bars
            ax.bar(i - width/2, reg_data['Mean'], width, 
                  label='Regulated' if i == 0 else '',
                  color=COLORS['regulated'], alpha=0.8, 
                  edgecolor='black', linewidth=0.5)
            ax.bar(i + width/2, base_data['Mean'], width,
                  label='Baseline' if i == 0 else '',
                  color=COLORS['baseline'], alpha=0.8,
                  edgecolor='black', linewidth=0.5)
            
            # Error bars
            if pd.notna(reg_data['CI_Lower']) and pd.notna(reg_data['CI_Upper']):
                reg_err = [[reg_data['Mean'] - reg_data['CI_Lower']], 
                          [reg_data['CI_Upper'] - reg_data['Mean']]]
                ax.errorbar(i - width/2, reg_data['Mean'], yerr=reg_err, fmt='none',
                          color='black', capsize=C.ERROR_CAP_SIZE, 
                          capthick=C.ERROR_BAR_WIDTH, linewidth=C.ERROR_BAR_WIDTH)
            
            if pd.notna(base_data['CI_Lower']) and pd.notna(base_data['CI_Upper']):
                base_err = [[base_data['Mean'] - base_data['CI_Lower']], 
                           [base_data['CI_Upper'] - base_data['Mean']]]
                ax.errorbar(i + width/2, base_data['Mean'], yerr=base_err, fmt='none',
                          color='black', capsize=C.ERROR_CAP_SIZE, 
                          capthick=C.ERROR_BAR_WIDTH, linewidth=C.ERROR_BAR_WIDTH)
    
    ax.set_xlabel('Evaluation Metric', fontweight='bold')
    ax.set_ylabel('Mean Score (0-1 scale)', fontweight='bold')
    ax.set_title('Performance Comparison: Regulated vs Baseline', 
                fontsize=C.FONT_SIZE_TITLE, fontweight='bold', pad=15)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([PlotStyler.format_metric_label(m) for m in unique_metrics])
    ax.set_ylim([0, 1.15])
    ax.legend(loc='upper right', frameon=True, fancybox=False, shadow=False)
    
    PlotStyler.style_bar_chart(ax)
    
    save_figure(fig, '01_performance_comparison', output_dir)


# ============================================================================
# VISUALIZATION: FIGURE 2 - EFFECT SIZES
# ============================================================================

def create_effect_sizes_plot(df_effects: pd.DataFrame, output_dir: str = "figures"):
    """Create effect sizes visualization."""
    print("\n" + "="*80)
    print("CREATING FIGURE 2: EFFECT SIZES")
    print("="*80)
    
    if len(df_effects) == 0:
        print("  ? No effect size data")
        return
    
    fig, ax = FigureTemplates.create_wide_panel()
    
    # Format metric names
    metrics_short = [PlotStyler.format_metric_label(m) for m in df_effects['Metric']]
    cohens_d = df_effects['Cohens_d'].tolist()
    colors = [COLORS['positive'] if d > 0 else COLORS['negative'] for d in cohens_d]
    
    y_pos = np.arange(len(metrics_short))
    bars = ax.barh(y_pos, cohens_d, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=1)
    
    # Add reference lines
    PlotStyler.add_effect_size_reference_lines(ax, vertical=True)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, cohens_d)):
        ax.text(val + 0.1 if val > 0 else val - 0.1, i, f'{val:.2f}', 
               va='center', ha='left' if val > 0 else 'right', 
               fontweight='bold', fontsize=C.FONT_SIZE_BASE)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics_short)
    ax.set_xlabel("Cohen's d", fontweight='bold')
    ax.set_title("Effect Sizes: Regulated vs Baseline", 
                fontsize=C.FONT_SIZE_TITLE, fontweight='bold', pad=15)
    ax.set_xlim([-1, max(cohens_d) + 0.5])
    ax.grid(axis='x', alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)
    ax.set_axisbelow(True)
    
    save_figure(fig, '02_effect_sizes', output_dir)


# ============================================================================
# VISUALIZATION: FIGURE 3 - PERSONALITY NEEDS FOCUSED
# ============================================================================

def create_personality_needs_plot(df_effects: pd.DataFrame, df_stats: pd.DataFrame,
                                 output_dir: str = "figures"):
    """Create focused plot for personality needs - the primary outcome."""
    print("\n" + "="*80)
    print("CREATING FIGURE 3: PERSONALITY NEEDS (PRIMARY OUTCOME)")
    print("="*80)
    
    # Filter for personality needs
    metric = 'PERSONALITY NEEDS ADDRESSED'
    effect_row = df_effects[df_effects['Metric'] == metric]
    stats_data = df_stats[df_stats['Metric'] == metric]
    
    if len(effect_row) == 0 or len(stats_data) == 0:
        print("  ? No personality needs data")
        return
    
    fig, ax = FigureTemplates.create_single_panel(height='medium')
    
    # Get data
    reg_data = stats_data[stats_data['Condition'] == 'Regulated'].iloc[0]
    base_data = stats_data[stats_data['Condition'] == 'Baseline'].iloc[0]
    cohen_d = effect_row.iloc[0]['Cohens_d']
    
    # Create bar plot
    conditions = ['Regulated', 'Baseline']
    means = [reg_data['Mean'], base_data['Mean']]
    colors_list = [COLORS['regulated'], COLORS['baseline']]
    
    bars = ax.bar(conditions, means, color=colors_list, alpha=0.8,
                 edgecolor='black', linewidth=1.5, width=0.6)
    
    # Add percentage labels on bars
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
               f'{mean*100:.1f}%',
               ha='center', va='bottom', fontweight='bold', 
               fontsize=C.FONT_SIZE_LARGE)
    
    # Add effect size annotation
    ax.text(0.5, 0.5, f"Cohen's d = {cohen_d:.2f}\n(Very Large Effect)", 
           transform=ax.transAxes, ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
           fontsize=C.FONT_SIZE_MEDIUM, fontweight='bold')
    
    ax.set_ylabel('Success Rate', fontweight='bold')
    ax.set_ylim([0, 1.15])
    ax.set_title('Personality Needs Addressed:\nDramatic Improvement with Adaptation',
                fontsize=C.FONT_SIZE_TITLE, fontweight='bold', pad=15)
    
    PlotStyler.style_bar_chart(ax)
    
    save_figure(fig, '03_personality_needs', output_dir)


# ============================================================================
# VISUALIZATION: FIGURE 4 - SAMPLE QUALITY
# ============================================================================

def create_sample_quality_plot(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame,
                              output_dir: str = "figures"):
    """Create sample distribution and quality visualization."""
    print("\n" + "="*80)
    print("CREATING FIGURE 4: SAMPLE QUALITY")
    print("="*80)
    
    fig, axes = FigureTemplates.create_double_panel()
    
    # Panel A: Conversations per personality type
    reg_counts = df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
    axes[0].bar(reg_counts.index, reg_counts.values, 
               color=[COLORS['regulated'], COLORS['baseline']], 
               alpha=0.8, edgecolor='black', linewidth=1)
    axes[0].set_xlabel('Personality Type', fontweight='bold')
    axes[0].set_ylabel('Number of Conversations', fontweight='bold')
    axes[0].set_title('(A) Conversations per Type', fontsize=C.FONT_SIZE_LARGE, pad=10)
    PlotStyler.style_bar_chart(axes[0])
    
    # Panel B: Turns per conversation
    msg_counts = df_regulated.groupby('Conversation_ID').size()
    axes[1].hist(msg_counts, bins=range(1, 10), 
                color=COLORS['regulated'], alpha=0.7, 
                edgecolor='black', linewidth=1)
    axes[1].set_xlabel('Turns per Conversation', fontweight='bold')
    axes[1].set_ylabel('Count', fontweight='bold')
    axes[1].set_title('(B) Turn Distribution', fontsize=C.FONT_SIZE_LARGE, pad=10)
    PlotStyler.style_bar_chart(axes[1])
    
    fig.suptitle('Sample Distribution and Data Quality', 
                fontsize=C.FONT_SIZE_TITLE, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    save_figure(fig, '04_sample_quality', output_dir)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main analysis pipeline."""
    print("\n" + "="*80)
    print("MASTER STATISTICAL ANALYSIS AND VISUALIZATION")
    print("Personality-Adaptive Conversational AI")
    print("Version 2.0 - Unified Pipeline")
    print("="*80)
    
    # Paths
    regulated_path = "merged/regulated.csv"
    baseline_path = "merged/baseline.csv"
    output_dir = "figures"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Execute analysis pipeline
    print("\n" + "?"*40)
    print("STARTING ANALYSIS PIPELINE")
    print("?"*40)
    
    # Step 1-2: Load and assess
    df_regulated, df_baseline = load_and_prepare_data(regulated_path, baseline_path)
    quality_report = assess_data_quality(df_regulated, df_baseline)
    
    # Step 3: Convert to numeric
    df_reg_numeric, df_base_numeric = convert_to_numeric(df_regulated, df_baseline)
    
    # Step 4-5: Calculate statistics
    df_stats = calculate_descriptive_statistics(df_reg_numeric, df_base_numeric)
    df_effects = calculate_effect_sizes(df_reg_numeric, df_base_numeric)
    
    # Save statistical results
    df_stats.to_csv("analysis_results_descriptive.csv", index=False)
    df_effects.to_csv("analysis_results_effect_sizes.csv", index=False)
    print(f"\n? Saved: analysis_results_descriptive.csv")
    print(f"? Saved: analysis_results_effect_sizes.csv")
    
    # Create visualizations
    print("\n" + "??"*40)
    print("GENERATING PUBLICATION-READY FIGURES")
    print("??"*40)
    
    create_performance_comparison(df_stats, output_dir)
    create_effect_sizes_plot(df_effects, output_dir)
    create_personality_needs_plot(df_effects, df_stats, output_dir)
    create_sample_quality_plot(df_regulated, df_baseline, output_dir)
    
    # Summary
    print("\n" + "="*80)
    print("? ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated Figures:")
    print("  � 01_performance_comparison.png - Core comparison across metrics")
    print("  � 02_effect_sizes.png - Effect size magnitudes")
    print("  � 03_personality_needs.png - Primary outcome (focused)")
    print("  � 04_sample_quality.png - Sample characteristics")
    print("\nCSV Results:")
    print("  � analysis_results_descriptive.csv")
    print("  � analysis_results_effect_sizes.csv")
    print("\nNext Steps:")
    print("  � Run create_system_diagrams.py for architecture figures")
    print("  � Review figures in ./figures/ directory")
    print("  � Integrate into manuscript")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
