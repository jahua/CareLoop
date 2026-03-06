#!/usr/bin/env python3
"""
Publication-Ready Statistical Analysis with Enhanced Visualizations
Personality-Adaptive Chatbot Performance Evaluation
Comparing Regulated vs Baseline Conditions

Features:
- Journal-quality figures (300 DPI, MDPI compliant)
- Professional color schemes
- Publication-ready styling
- A4-compatible dimensions
- Accessible design

Author: Generated for thesis analysis
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# UNIFIED PUBLICATION-READY STYLING (match reference diagram theme)
# ============================================================================

from visualization_config import configure_matplotlib, PUBLICATION_CONFIG as C

configure_matplotlib()

# Cohesive palette aligned with the Zurich mapping diagram
COLORS_PUBLICATION = {
    'regulated': C.COLOR_REGULATED,
    'baseline': C.COLOR_BASELINE,
    'accent': C.COLOR_ACCENT,
    'positive': C.COLOR_POSITIVE,
    'neutral': C.COLOR_NEUTRAL,
    'negative': C.COLOR_NEGATIVE,
    'fill_blue': C.FILL_BLUE,
    'fill_orange': C.FILL_ORANGE,
    'fill_green': C.FILL_GREEN,
}

# ============================================================================
# HELPER FUNCTIONS
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
    df_regulated['Personality_Type'] = df_regulated['MSG. NO.'].str[0]
    df_regulated['Conversation_ID'] = df_regulated['MSG. NO.'].str.split('-').str[:2].str.join('-')
    df_regulated['Turn_Number'] = df_regulated['MSG. NO.'].str.split('-').str[2].astype(int)
    
    df_baseline['Personality_Type'] = df_baseline['MSG. NO.'].str[0]
    df_baseline['Conversation_ID'] = df_baseline['MSG. NO.'].str.split('-').str[:2].str.join('-')
    df_baseline['Turn_Number'] = df_baseline['MSG. NO.'].str.split('-').str[2].astype(int)
    
    return df_regulated, df_baseline


def assess_data_quality(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Dict:
    """Assess data quality."""
    print("\n" + "="*80)
    print("STEP 2: DATA QUALITY ASSESSMENT")
    print("="*80)
    
    quality_report = {
        'n_regulated': len(df_regulated),
        'n_baseline': len(df_baseline),
        'n_conversations': df_regulated['Conversation_ID'].nunique(),
        'n_regulated_conversations': df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
    }
    
    print(f"\nRegulated conversations: {df_regulated['Conversation_ID'].nunique()}")
    print(f"Baseline conversations: {df_baseline['Conversation_ID'].nunique()}")
    
    return quality_report


def visualize_data_quality_publication(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame, 
                                       output_dir: str = "figures"):
    """Create publication-ready data quality visualizations."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("STEP 3: DATA QUALITY VISUALIZATIONS (PUBLICATION-READY)")
    print("="*80)
    
    # Figure 1: Sample Distribution
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=150)
    fig.suptitle('Data Quality: Sample Distribution', fontsize=12, fontweight='bold', y=1.02)
    
    # Personality type distribution
    reg_counts = df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
    axes[0].bar(reg_counts.index, reg_counts.values, 
               color=[COLORS_PUBLICATION['regulated'], COLORS_PUBLICATION['baseline']], 
               alpha=0.8, edgecolor='black', linewidth=1)
    axes[0].set_xlabel('Personality Type', fontweight='bold')
    axes[0].set_ylabel('Number of Conversations', fontweight='bold')
    axes[0].set_title('Conversations per Type', fontsize=10, pad=10)
    axes[0].grid(axis='y', alpha=0.3, linestyle='--')
    axes[0].set_axisbelow(True)
    
    # Messages per conversation
    msg_counts = df_regulated.groupby('Conversation_ID').size()
    axes[1].hist(msg_counts, bins=range(1, 10), 
                color=COLORS_PUBLICATION['regulated'], alpha=0.7, 
                edgecolor='black', linewidth=1)
    axes[1].set_xlabel('Turns per Conversation', fontweight='bold')
    axes[1].set_ylabel('Count', fontweight='bold')
    axes[1].set_title('Message Distribution', fontsize=10, pad=10)
    axes[1].grid(axis='y', alpha=0.3, linestyle='--')
    axes[1].set_axisbelow(True)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_sample_distribution.png", dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved: {output_dir}/01_sample_distribution.png")
    plt.close()


def convert_to_numeric(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Convert categorical to numeric."""
    print("\n" + "="*80)
    print("STEP 4: CATEGORICAL TO NUMERIC CONVERSION")
    print("="*80)
    
    mapping = {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0, 'yes': 1, 'no': 0}
    
    reg_metrics = ['DETECTION ACCURATE', 'REGULATION EFFECTIVE', 
                   'EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                   'PERSONALITY NEEDS ADDRESSED']
    base_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                    'PERSONALITY NEEDS ADDRESSED']
    
    df_reg_numeric = df_regulated.copy()
    df_base_numeric = df_baseline.copy()
    
    for metric in reg_metrics:
        if metric in df_reg_numeric.columns:
            df_reg_numeric[f'{metric}_numeric'] = df_reg_numeric[metric].map(mapping)
    
    for metric in base_metrics:
        if metric in df_base_numeric.columns:
            df_base_numeric[f'{metric}_numeric'] = df_base_numeric[metric].map(mapping)
    
    return df_reg_numeric, df_base_numeric


def calculate_descriptive_statistics(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptive statistics."""
    print("\n" + "="*80)
    print("STEP 5: DESCRIPTIVE STATISTICS")
    print("="*80)
    
    results = []
    common_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 'PERSONALITY NEEDS ADDRESSED']
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            # Regulated
            reg_values = df_regulated[metric_numeric].dropna()
            reg_mean = reg_values.mean()
            reg_std = reg_values.std()
            reg_n = len(reg_values)
            reg_ci = stats.t.interval(0.95, reg_n-1, loc=reg_mean, scale=reg_std/np.sqrt(reg_n))
            
            # Baseline
            base_values = df_baseline[metric_numeric].dropna()
            base_mean = base_values.mean()
            base_std = base_values.std()
            base_n = len(base_values)
            base_ci = stats.t.interval(0.95, base_n-1, loc=base_mean, scale=base_std/np.sqrt(base_n))
            
            results.extend([
                {'Metric': metric, 'Condition': 'Regulated', 'N': reg_n, 'Mean': reg_mean, 
                 'SD': reg_std, 'CI_Lower': reg_ci[0], 'CI_Upper': reg_ci[1]},
                {'Metric': metric, 'Condition': 'Baseline', 'N': base_n, 'Mean': base_mean, 
                 'SD': base_std, 'CI_Lower': base_ci[0], 'CI_Upper': base_ci[1]}
            ])
    
    return pd.DataFrame(results)


def calculate_cohens_d(group1: np.array, group2: np.array) -> float:
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_sd if pooled_sd > 0 else 0


def calculate_effect_sizes(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    """Calculate effect sizes."""
    print("\n" + "="*80)
    print("STEP 6: EFFECT SIZE ANALYSIS (COHEN'S D)")
    print("="*80)
    
    effect_sizes = []
    common_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 'PERSONALITY NEEDS ADDRESSED']
    
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
    
    return pd.DataFrame(effect_sizes)


def visualize_results_publication(df_stats: pd.DataFrame, df_effects: pd.DataFrame, 
                                  output_dir: str = "figures"):
    """Create publication-ready result visualizations."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("STEP 7: RESULTS VISUALIZATION (PUBLICATION-READY)")
    print("="*80)
    
    # Figure 3: Performance Comparison with CI
    common_metrics = df_stats[df_stats['Condition'].isin(['Regulated', 'Baseline'])].copy()
    metric_counts = common_metrics.groupby('Metric')['Condition'].count()
    valid_metrics = metric_counts[metric_counts == 2].index.tolist()
    common_metrics = common_metrics[common_metrics['Metric'].isin(valid_metrics)]
    unique_metrics = common_metrics['Metric'].unique()
    
    if len(unique_metrics) > 0:
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.suptitle('Performance Comparison: Regulated vs Baseline', fontsize=12, fontweight='bold', y=0.98)
        
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
                      color=COLORS_PUBLICATION['regulated'], alpha=0.8, edgecolor='black', linewidth=0.5)
                ax.bar(i + width/2, base_data['Mean'], width,
                      label='Baseline' if i == 0 else '',
                      color=COLORS_PUBLICATION['baseline'], alpha=0.8, edgecolor='black', linewidth=0.5)
                
                # Error bars
                if pd.notna(reg_data['CI_Lower']) and pd.notna(reg_data['CI_Upper']):
                    reg_err = [[reg_data['Mean'] - reg_data['CI_Lower']], 
                              [reg_data['CI_Upper'] - reg_data['Mean']]]
                    ax.errorbar(i - width/2, reg_data['Mean'], yerr=reg_err, fmt='none',
                              color='black', capsize=4, capthick=1, linewidth=1)
                
                if pd.notna(base_data['CI_Lower']) and pd.notna(base_data['CI_Upper']):
                    base_err = [[base_data['Mean'] - base_data['CI_Lower']], 
                               [base_data['CI_Upper'] - base_data['Mean']]]
                    ax.errorbar(i + width/2, base_data['Mean'], yerr=base_err, fmt='none',
                              color='black', capsize=4, capthick=1, linewidth=1)
        
        ax.set_xlabel('Evaluation Metric', fontweight='bold')
        ax.set_ylabel('Mean Score (0–1 scale)', fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([m.replace(' ', '\n') for m in unique_metrics], fontsize=9)
        ax.set_ylim([0, 1.15])
        ax.legend(loc='upper right', frameon=True, fancybox=False, shadow=False)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/03_performance_comparison.png", dpi=300, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Saved: {output_dir}/03_performance_comparison.png")
        plt.close()
    
    # Figure 4: Effect Sizes (Horizontal Bar)
    if len(df_effects) > 0:
        fig, ax = plt.subplots(figsize=(10, 4.8), dpi=150)
        fig.suptitle("Effect Sizes: Cohen's d (Regulated vs Baseline)", fontsize=C.FONT_SIZE_TITLE, fontweight='bold', y=0.98)
        
        metrics_short = [m.replace('EMOTIONAL TONE APPROPRIATE', 'Emotional Tone')
                        .replace('RELEVANCE & COHERENCE', 'Relevance')
                        .replace('PERSONALITY NEEDS ADDRESSED', 'Personality Needs') 
                        for m in df_effects['Metric']]
        cohens_d = df_effects['Cohens_d'].tolist()
        colors = [COLORS_PUBLICATION['positive'] if d > 0 else COLORS_PUBLICATION['negative'] 
                 for d in cohens_d]
        
        y_pos = np.arange(len(metrics_short))
        bars = ax.barh(y_pos, cohens_d, color=colors, alpha=0.85, edgecolor=C.COLOR_GRAY, linewidth=1.0)
        
        # Reference lines
        ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
        ax.axvline(x=0.2, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
        ax.axvline(x=-0.2, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
        ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
        ax.axvline(x=-0.5, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
        
        # Axis limits: include large effects without inflating whitespace
        max_abs = max(1.0, float(max(abs(v) for v in cohens_d)))
        pad = max_abs * 0.15
        xmin, xmax = -max_abs - pad, max_abs + pad
        ax.set_xlim([xmin, xmax])

        # Add value labels (kept inside axes so bbox doesn't explode)
        for i, val in enumerate(cohens_d):
            if val >= 0:
                x = min(val + 0.05 * max_abs, xmax - 0.06 * max_abs)
                ha = 'left'
            else:
                x = max(val - 0.05 * max_abs, xmin + 0.06 * max_abs)
                ha = 'right'
            ax.text(x, i, f'{val:.2f}', va='center', ha=ha, fontweight='bold', fontsize=C.FONT_SIZE_BASE)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics_short, fontsize=C.FONT_SIZE_BASE)
        ax.set_xlabel("Cohen's d", fontweight='bold')
        ax.grid(axis='x', alpha=C.GRID_ALPHA, linestyle=C.GRID_LINESTYLE)
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/04_effect_sizes.png", dpi=300, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Saved: {output_dir}/04_effect_sizes.png")
        plt.close()
    
    # Figure 5: Percentage Improvement
    if len(df_effects) > 0:
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.suptitle('Percentage Improvement: Regulated vs Baseline', fontsize=12, fontweight='bold', y=0.98)
        
        metrics_short = [m.replace('EMOTIONAL TONE APPROPRIATE', 'Emotional Tone')
                        .replace('RELEVANCE & COHERENCE', 'Relevance')
                        .replace('PERSONALITY NEEDS ADDRESSED', 'Personality Needs') 
                        for m in df_effects['Metric']]
        improvement = (df_effects['Difference'] * 100).tolist()
        colors = [COLORS_PUBLICATION['positive'] if i > 0 else COLORS_PUBLICATION['negative'] 
                 for i in improvement]
        
        y_pos = np.arange(len(metrics_short))
        bars = ax.barh(y_pos, improvement, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, improvement)):
            ax.text(val + 0.5 if val > 0 else val - 0.5, i, f'{val:+.1f}%', 
                   va='center', ha='left' if val > 0 else 'right', fontweight='bold', fontsize=9)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics_short, fontsize=9)
        ax.set_xlabel('Improvement (%)', fontweight='bold')
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/05_percentage_improvement.png", dpi=300, bbox_inches='tight', facecolor='white')
        print(f"  ✓ Saved: {output_dir}/05_percentage_improvement.png")
        plt.close()


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("PUBLICATION-READY STATISTICAL ANALYSIS")
    print("Personality-Adaptive Chatbot Performance Evaluation")
    print("="*80)
    
    regulated_path = "merged/regulated.csv"
    baseline_path = "merged/baseline.csv"
    
    # Execute analysis
    df_regulated, df_baseline = load_and_prepare_data(regulated_path, baseline_path)
    quality_report = assess_data_quality(df_regulated, df_baseline)
    visualize_data_quality_publication(df_regulated, df_baseline)
    
    df_reg_numeric, df_base_numeric = convert_to_numeric(df_regulated, df_baseline)
    df_stats = calculate_descriptive_statistics(df_reg_numeric, df_base_numeric)
    df_effects = calculate_effect_sizes(df_reg_numeric, df_base_numeric)
    
    visualize_results_publication(df_stats, df_effects)
    
    # Save results
    df_stats.to_csv("analysis_results_descriptive.csv", index=False)
    df_effects.to_csv("analysis_results_effect_sizes.csv", index=False)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated publication-ready figures:")
    print("  • figures/01_sample_distribution.png")
    print("  • figures/03_performance_comparison.png")
    print("  • figures/04_effect_sizes.png")
    print("  • figures/05_percentage_improvement.png")
    print("\nCSV Results:")
    print("  • analysis_results_descriptive.csv")
    print("  • analysis_results_effect_sizes.csv")
    print("\n")


if __name__ == "__main__":
    main()
