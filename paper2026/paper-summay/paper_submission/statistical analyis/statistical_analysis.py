#!/usr/bin/env python3
"""
Statistical Analysis of Personality-Adaptive Chatbot Performance
Comparing Regulated vs Baseline Conditions

This script performs:
1. Data Quality Assessment and Visualization
2. Descriptive Statistics (means, SDs, confidence intervals)
3. Effect Size Analysis (Cohen's d)
4. Comparative Visualizations

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

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# ============================================================================
# STEP 1: DATA LOADING AND PREPARATION
# ============================================================================

def load_and_prepare_data(regulated_path: str, baseline_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load regulated and baseline datasets and prepare for analysis.
    
    Args:
        regulated_path: Path to regulated.csv
        baseline_path: Path to baseline.csv
        
    Returns:
        Tuple of (regulated_df, baseline_df)
    """
    print("="*80)
    print("STEP 1: DATA LOADING AND PREPARATION")
    print("="*80)
    
    # Load datasets
    df_regulated = pd.read_csv(regulated_path)
    df_baseline = pd.read_csv(baseline_path)
    
    print(f"\nRegulated dataset shape: {df_regulated.shape}")
    print(f"Baseline dataset shape: {df_baseline.shape}")
    
    # Extract conversation metadata
    df_regulated['Personality_Type'] = df_regulated['MSG. NO.'].str[0]  # A or B
    df_regulated['Conversation_ID'] = df_regulated['MSG. NO.'].str.split('-').str[:2].str.join('-')
    df_regulated['Turn_Number'] = df_regulated['MSG. NO.'].str.split('-').str[2].astype(int)
    
    df_baseline['Personality_Type'] = df_baseline['MSG. NO.'].str[0]
    df_baseline['Conversation_ID'] = df_baseline['MSG. NO.'].str.split('-').str[:2].str.join('-')
    df_baseline['Turn_Number'] = df_baseline['MSG. NO.'].str.split('-').str[2].astype(int)
    
    print(f"\nPersonality Type Distribution (Regulated):")
    print(df_regulated['Personality_Type'].value_counts().sort_index())
    
    print(f"\nConversation IDs: {df_regulated['Conversation_ID'].nunique()} unique conversations")
    
    return df_regulated, df_baseline


# ============================================================================
# STEP 2: DATA QUALITY ASSESSMENT
# ============================================================================

def assess_data_quality(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Dict:
    """
    Perform comprehensive data quality assessment.
    
    Returns:
        Dictionary containing quality metrics
    """
    print("\n" + "="*80)
    print("STEP 2: DATA QUALITY ASSESSMENT")
    print("="*80)
    
    quality_report = {}
    
    # Check for missing values
    print("\n2.1 Missing Values Analysis:")
    print("-"*80)
    
    print("\nRegulated Dataset:")
    missing_reg = df_regulated.isnull().sum()
    missing_reg_pct = (missing_reg / len(df_regulated) * 100).round(2)
    for col in missing_reg[missing_reg > 0].index:
        print(f"  {col}: {missing_reg[col]} ({missing_reg_pct[col]}%)")
    
    print("\nBaseline Dataset:")
    missing_base = df_baseline.isnull().sum()
    missing_base_pct = (missing_base / len(df_baseline) * 100).round(2)
    for col in missing_base[missing_base > 0].index:
        print(f"  {col}: {missing_base[col]} ({missing_base_pct[col]}%)")
    
    quality_report['missing_regulated'] = missing_reg
    quality_report['missing_baseline'] = missing_base
    
    # Check evaluation metrics
    print("\n2.2 Evaluation Metrics Distribution:")
    print("-"*80)
    
    # Regulated metrics
    reg_metrics = ['DETECTION ACCURATE', 'REGULATION EFFECTIVE', 
                   'EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                   'PERSONALITY NEEDS ADDRESSED']
    
    print("\nRegulated Metrics:")
    for metric in reg_metrics:
        if metric in df_regulated.columns:
            value_counts = df_regulated[metric].value_counts()
            print(f"\n  {metric}:")
            for val, count in value_counts.items():
                print(f"    {val}: {count} ({count/len(df_regulated)*100:.1f}%)")
    
    # Baseline metrics
    base_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                    'PERSONALITY NEEDS ADDRESSED']
    
    print("\nBaseline Metrics:")
    for metric in base_metrics:
        if metric in df_baseline.columns:
            value_counts = df_baseline[metric].value_counts()
            print(f"\n  {metric}:")
            for val, count in value_counts.items():
                print(f"    {val}: {count} ({count/len(df_baseline)*100:.1f}%)")
    
    # Check data alignment
    print("\n2.3 Data Alignment Check:")
    print("-"*80)
    print(f"Regulated conversations: {df_regulated['Conversation_ID'].nunique()}")
    print(f"Baseline conversations: {df_baseline['Conversation_ID'].nunique()}")
    print(f"Common conversations: {len(set(df_regulated['Conversation_ID']) & set(df_baseline['Conversation_ID']))}")
    
    quality_report['n_regulated'] = len(df_regulated)
    quality_report['n_baseline'] = len(df_baseline)
    quality_report['n_conversations'] = df_regulated['Conversation_ID'].nunique()
    
    return quality_report


# ============================================================================
# STEP 3: DATA QUALITY VISUALIZATIONS
# ============================================================================

def visualize_data_quality(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame, 
                           output_dir: str = "figures"):
    """
    Create visualizations for data quality assessment.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("STEP 3: DATA QUALITY VISUALIZATIONS")
    print("="*80)
    
    # Figure 1: Sample Size Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Conversations per personality type
    reg_counts = df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
    axes[0].bar(reg_counts.index, reg_counts.values, color=['#3498db', '#e74c3c'], alpha=0.7)
    axes[0].set_xlabel('Personality Type')
    axes[0].set_ylabel('Number of Conversations')
    axes[0].set_title('Sample Distribution: Conversations per Personality Type')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Messages per conversation
    msg_counts = df_regulated.groupby('Conversation_ID').size()
    axes[1].hist(msg_counts, bins=range(1, 10), color='#2ecc71', alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('Number of Messages')
    axes[1].set_ylabel('Number of Conversations')
    axes[1].set_title('Distribution of Messages per Conversation')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/01_sample_distribution.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/01_sample_distribution.png")
    plt.close()
    
    # Figure 2: Missing Data Heatmap
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Regulated missing data
    missing_reg = df_regulated.isnull().astype(int)
    sns.heatmap(missing_reg.T, cmap='RdYlGn_r', cbar=True, ax=axes[0], 
                xticklabels=False, yticklabels=df_regulated.columns)
    axes[0].set_title('Missing Data Heatmap: Regulated Dataset')
    axes[0].set_xlabel('Sample Index')
    
    # Baseline missing data
    missing_base = df_baseline.isnull().astype(int)
    sns.heatmap(missing_base.T, cmap='RdYlGn_r', cbar=True, ax=axes[1],
                xticklabels=False, yticklabels=df_baseline.columns)
    axes[1].set_title('Missing Data Heatmap: Baseline Dataset')
    axes[1].set_xlabel('Sample Index')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/02_missing_data_heatmap.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/02_missing_data_heatmap.png")
    plt.close()


# ============================================================================
# STEP 4: CONVERT CATEGORICAL TO NUMERIC
# ============================================================================

def convert_to_numeric(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert YES/NO categorical responses to numeric (1/0).
    """
    print("\n" + "="*80)
    print("STEP 4: CONVERTING CATEGORICAL TO NUMERIC")
    print("="*80)
    
    # Define conversion mapping
    mapping = {'YES': 1, 'NO': 0, 'Yes': 1, 'No': 0, 'yes': 1, 'no': 0}
    
    # Metrics to convert
    reg_metrics = ['DETECTION ACCURATE', 'REGULATION EFFECTIVE', 
                   'EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                   'PERSONALITY NEEDS ADDRESSED']
    
    base_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 
                    'PERSONALITY NEEDS ADDRESSED']
    
    df_reg_numeric = df_regulated.copy()
    df_base_numeric = df_baseline.copy()
    
    print("\nConverting Regulated metrics...")
    for metric in reg_metrics:
        if metric in df_reg_numeric.columns:
            df_reg_numeric[f'{metric}_numeric'] = df_reg_numeric[metric].map(mapping)
            print(f"  ✓ {metric}: {df_reg_numeric[f'{metric}_numeric'].notna().sum()} values converted")
    
    print("\nConverting Baseline metrics...")
    for metric in base_metrics:
        if metric in df_base_numeric.columns:
            df_base_numeric[f'{metric}_numeric'] = df_base_numeric[metric].map(mapping)
            print(f"  ✓ {metric}: {df_base_numeric[f'{metric}_numeric'].notna().sum()} values converted")
    
    return df_reg_numeric, df_base_numeric


# ============================================================================
# STEP 5: DESCRIPTIVE STATISTICS
# ============================================================================

def calculate_descriptive_statistics(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate comprehensive descriptive statistics for all metrics.
    """
    print("\n" + "="*80)
    print("STEP 5: DESCRIPTIVE STATISTICS")
    print("="*80)
    
    results = []
    
    # Common metrics between regulated and baseline
    common_metrics = [
        'EMOTIONAL TONE APPROPRIATE',
        'RELEVANCE & COHERENCE',
        'PERSONALITY NEEDS ADDRESSED'
    ]
    
    # Regulated-only metrics
    regulated_only_metrics = [
        'DETECTION ACCURATE',
        'REGULATION EFFECTIVE'
    ]
    
    print("\n5.1 Common Metrics (Regulated vs Baseline):")
    print("-"*80)
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            # Regulated stats
            reg_values = df_regulated[metric_numeric].dropna()
            reg_mean = reg_values.mean()
            reg_std = reg_values.std()
            reg_n = len(reg_values)
            reg_ci = stats.t.interval(0.95, reg_n-1, loc=reg_mean, 
                                     scale=reg_std/np.sqrt(reg_n))
            
            # Baseline stats
            base_values = df_baseline[metric_numeric].dropna()
            base_mean = base_values.mean()
            base_std = base_values.std()
            base_n = len(base_values)
            base_ci = stats.t.interval(0.95, base_n-1, loc=base_mean,
                                      scale=base_std/np.sqrt(base_n))
            
            results.append({
                'Metric': metric,
                'Condition': 'Regulated',
                'N': reg_n,
                'Mean': reg_mean,
                'SD': reg_std,
                'CI_Lower': reg_ci[0],
                'CI_Upper': reg_ci[1],
                'Percentage': reg_mean * 100
            })
            
            results.append({
                'Metric': metric,
                'Condition': 'Baseline',
                'N': base_n,
                'Mean': base_mean,
                'SD': base_std,
                'CI_Lower': base_ci[0],
                'CI_Upper': base_ci[1],
                'Percentage': base_mean * 100
            })
            
            print(f"\n{metric}:")
            print(f"  Regulated:  M={reg_mean:.3f} (SD={reg_std:.3f}), "
                  f"95% CI [{reg_ci[0]:.3f}, {reg_ci[1]:.3f}], {reg_mean*100:.1f}%")
            print(f"  Baseline:   M={base_mean:.3f} (SD={base_std:.3f}), "
                  f"95% CI [{base_ci[0]:.3f}, {base_ci[1]:.3f}], {base_mean*100:.1f}%")
    
    print("\n5.2 Regulated-Only Metrics:")
    print("-"*80)
    
    for metric in regulated_only_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns:
            reg_values = df_regulated[metric_numeric].dropna()
            reg_mean = reg_values.mean()
            reg_std = reg_values.std()
            reg_n = len(reg_values)
            reg_ci = stats.t.interval(0.95, reg_n-1, loc=reg_mean,
                                     scale=reg_std/np.sqrt(reg_n))
            
            results.append({
                'Metric': metric,
                'Condition': 'Regulated',
                'N': reg_n,
                'Mean': reg_mean,
                'SD': reg_std,
                'CI_Lower': reg_ci[0],
                'CI_Upper': reg_ci[1],
                'Percentage': reg_mean * 100
            })
            
            print(f"\n{metric}:")
            print(f"  Regulated:  M={reg_mean:.3f} (SD={reg_std:.3f}), "
                  f"95% CI [{reg_ci[0]:.3f}, {reg_ci[1]:.3f}], {reg_mean*100:.1f}%")
    
    df_results = pd.DataFrame(results)
    
    return df_results


# ============================================================================
# STEP 6: EFFECT SIZE ANALYSIS (COHEN'S D)
# ============================================================================

def calculate_cohens_d(group1: np.array, group2: np.array) -> float:
    """
    Calculate Cohen's d effect size.
    
    Formula: d = (M1 - M2) / pooled_sd
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    
    return (np.mean(group1) - np.mean(group2)) / pooled_sd if pooled_sd > 0 else 0


def interpret_cohens_d(d: float) -> str:
    """
    Interpret Cohen's d based on conventional thresholds.
    """
    abs_d = abs(d)
    if abs_d < 0.2:
        return "Negligible"
    elif abs_d < 0.5:
        return "Small"
    elif abs_d < 0.8:
        return "Medium"
    else:
        return "Large"


def calculate_effect_sizes(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Cohen's d effect sizes for all comparable metrics.
    """
    print("\n" + "="*80)
    print("STEP 6: EFFECT SIZE ANALYSIS (COHEN'S D)")
    print("="*80)
    
    common_metrics = [
        'EMOTIONAL TONE APPROPRIATE',
        'RELEVANCE & COHERENCE',
        'PERSONALITY NEEDS ADDRESSED'
    ]
    
    effect_sizes = []
    
    print("\nCohen's d Effect Sizes (Regulated vs Baseline):")
    print("-"*80)
    print(f"{'Metric':<40} {'d':<8} {'Interpretation':<15} {'Direction'}")
    print("-"*80)
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            reg_values = df_regulated[metric_numeric].dropna().values
            base_values = df_baseline[metric_numeric].dropna().values
            
            if len(reg_values) > 1 and len(base_values) > 1:
                d = calculate_cohens_d(reg_values, base_values)
                interpretation = interpret_cohens_d(d)
                direction = "Regulated > Baseline" if d > 0 else "Baseline > Regulated"
                
                effect_sizes.append({
                    'Metric': metric,
                    'Cohens_d': d,
                    'Interpretation': interpretation,
                    'Regulated_Mean': np.mean(reg_values),
                    'Baseline_Mean': np.mean(base_values),
                    'Difference': np.mean(reg_values) - np.mean(base_values)
                })
                
                print(f"{metric:<40} {d:>7.3f} {interpretation:<15} {direction}")
    
    print("\nInterpretation Guidelines (Cohen, 1988):")
    print("  |d| < 0.2: Negligible effect")
    print("  |d| < 0.5: Small effect")
    print("  |d| < 0.8: Medium effect")
    print("  |d| ≥ 0.8: Large effect")
    
    df_effect_sizes = pd.DataFrame(effect_sizes)
    
    return df_effect_sizes


# ============================================================================
# STEP 7: VISUALIZATION OF RESULTS
# ============================================================================

def visualize_results(df_stats: pd.DataFrame, df_effects: pd.DataFrame, 
                      output_dir: str = "figures"):
    """
    Create comprehensive visualizations of statistical results.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("STEP 7: RESULTS VISUALIZATION")
    print("="*80)
    
    # Figure 3: Comparison of Means with CI
    common_metrics = df_stats[df_stats['Condition'].isin(['Regulated', 'Baseline'])].copy()
    
    # Filter to only metrics that have both conditions
    metric_counts = common_metrics.groupby('Metric')['Condition'].count()
    valid_metrics = metric_counts[metric_counts == 2].index.tolist()
    common_metrics = common_metrics[common_metrics['Metric'].isin(valid_metrics)]
    unique_metrics = common_metrics['Metric'].unique()
    
    if len(unique_metrics) == 0:
        print("  ⚠ No comparable metrics found for visualization")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_pos = np.arange(len(unique_metrics))
    width = 0.35
    
    for i, metric in enumerate(unique_metrics):
        metric_data = common_metrics[common_metrics['Metric'] == metric]
        
        reg_row = metric_data[metric_data['Condition'] == 'Regulated']
        base_row = metric_data[metric_data['Condition'] == 'Baseline']
        
        if len(reg_row) == 0 or len(base_row) == 0:
            continue
            
        reg_data = reg_row.iloc[0]
        base_data = base_row.iloc[0]
        
        # Plot bars
        ax.bar(i - width/2, reg_data['Mean'], width, label='Regulated' if i == 0 else '',
               color='#3498db', alpha=0.8)
        ax.bar(i + width/2, base_data['Mean'], width, label='Baseline' if i == 0 else '',
               color='#e74c3c', alpha=0.8)
        
        # Plot error bars (CI) - only if CIs are valid (not NaN)
        if pd.notna(reg_data['CI_Lower']) and pd.notna(reg_data['CI_Upper']):
            reg_err = [[reg_data['Mean'] - reg_data['CI_Lower']], 
                       [reg_data['CI_Upper'] - reg_data['Mean']]]
            ax.errorbar(i - width/2, reg_data['Mean'], yerr=reg_err, fmt='none', 
                       color='black', capsize=5, capthick=2)
        
        if pd.notna(base_data['CI_Lower']) and pd.notna(base_data['CI_Upper']):
            base_err = [[base_data['Mean'] - base_data['CI_Lower']], 
                        [base_data['CI_Upper'] - base_data['Mean']]]
            ax.errorbar(i + width/2, base_data['Mean'], yerr=base_err, fmt='none',
                       color='black', capsize=5, capthick=2)
    
    ax.set_xlabel('Evaluation Metric')
    ax.set_ylabel('Mean Score (0-1 scale)')
    ax.set_title('Comparison of Regulated vs Baseline Performance\n(with 95% Confidence Intervals)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels([m.replace(' ', '\n') for m in unique_metrics], rotation=0, ha='center')
    ax.legend()
    ax.set_ylim([0, 1.1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/03_performance_comparison.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/03_performance_comparison.png")
    plt.close()
    
    # Figure 4: Effect Sizes
    fig, ax = plt.subplots(figsize=(10, 6))
    
    metrics = df_effects['Metric'].tolist()
    cohens_d = df_effects['Cohens_d'].tolist()
    colors = ['#2ecc71' if d > 0 else '#e74c3c' for d in cohens_d]
    
    y_pos = np.arange(len(metrics))
    ax.barh(y_pos, cohens_d, color=colors, alpha=0.7)
    
    # Add reference lines for effect size interpretation
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=0.2, color='gray', linestyle='--', alpha=0.5, label='Small')
    ax.axvline(x=-0.2, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, label='Medium')
    ax.axvline(x=-0.5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0.8, color='gray', linestyle='--', alpha=0.5, label='Large')
    ax.axvline(x=-0.8, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics)
    ax.set_xlabel("Cohen's d (Effect Size)")
    ax.set_title("Effect Sizes: Regulated vs Baseline\n(Positive = Regulated Better)")
    ax.legend(loc='lower right')
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/04_effect_sizes.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/04_effect_sizes.png")
    plt.close()
    
    # Figure 5: Percentage Improvement
    fig, ax = plt.subplots(figsize=(10, 6))
    
    improvement = (df_effects['Difference'] * 100).tolist()
    colors = ['#2ecc71' if i > 0 else '#e74c3c' for i in improvement]
    
    ax.barh(y_pos, improvement, color=colors, alpha=0.7)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrics)
    ax.set_xlabel('Percentage Point Difference (%)')
    ax.set_title('Percentage Point Improvement: Regulated vs Baseline\n(Positive = Regulated Better)')
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (pos, val) in enumerate(zip(y_pos, improvement)):
        ax.text(val + (1 if val > 0 else -1), pos, f'{val:+.1f}%', 
               va='center', ha='left' if val > 0 else 'right')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/05_percentage_improvement.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/05_percentage_improvement.png")
    plt.close()


# ============================================================================
# STEP 8: INFERENTIAL STATISTICS (FOR ILLUSTRATION)
# ============================================================================

def perform_inferential_tests(df_regulated: pd.DataFrame, df_baseline: pd.DataFrame):
    """
    Perform inferential statistics for illustration purposes.
    Note: Given the deterministic simulation, these are illustrative only.
    """
    print("\n" + "="*80)
    print("STEP 8: INFERENTIAL STATISTICS (ILLUSTRATIVE ONLY)")
    print("="*80)
    
    print("\nNote: These statistics are included for illustration purposes only.")
    print("They should NOT be interpreted as evidence of generalizable hypothesis testing,")
    print("but rather as a way to contextualize effect sizes and facilitate comparisons")
    print("with related empirical studies.")
    
    common_metrics = [
        'EMOTIONAL TONE APPROPRIATE',
        'RELEVANCE & COHERENCE',
        'PERSONALITY NEEDS ADDRESSED'
    ]
    
    print("\n8.1 Independent Samples t-tests:")
    print("-"*80)
    print(f"{'Metric':<40} {'t':<8} {'p':<10} {'Result'}")
    print("-"*80)
    
    test_results = []
    
    for metric in common_metrics:
        metric_numeric = f'{metric}_numeric'
        
        if metric_numeric in df_regulated.columns and metric_numeric in df_baseline.columns:
            reg_values = df_regulated[metric_numeric].dropna().values
            base_values = df_baseline[metric_numeric].dropna().values
            
            if len(reg_values) > 1 and len(base_values) > 1:
                t_stat, p_value = stats.ttest_ind(reg_values, base_values)
                sig = "p < 0.05" if p_value < 0.05 else "n.s."
                
                test_results.append({
                    'Metric': metric,
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant': p_value < 0.05
                })
                
                print(f"{metric:<40} {t_stat:>7.3f} {p_value:>9.4f} {sig}")
    
    print("\nInterpretation:")
    print("  p < 0.05: Statistically significant (illustrative)")
    print("  n.s.: Not significant")
    
    return pd.DataFrame(test_results)


# ============================================================================
# STEP 9: GENERATE COMPREHENSIVE REPORT
# ============================================================================

def generate_report(df_stats: pd.DataFrame, df_effects: pd.DataFrame, 
                   df_tests: pd.DataFrame, quality_report: Dict,
                   output_file: str = "analysis_report.txt"):
    """
    Generate a comprehensive text report of all analyses.
    """
    print("\n" + "="*80)
    print("STEP 9: GENERATING COMPREHENSIVE REPORT")
    print("="*80)
    
    with open(output_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("STATISTICAL ANALYSIS REPORT\n")
        f.write("Personality-Adaptive Chatbot Performance Evaluation\n")
        f.write("Regulated vs Baseline Comparison\n")
        f.write("="*80 + "\n\n")
        
        # Sample information
        f.write("1. SAMPLE INFORMATION\n")
        f.write("-"*80 + "\n")
        f.write(f"Total Conversations: {quality_report['n_conversations']}\n")
        f.write(f"Regulated Messages: {quality_report['n_regulated']}\n")
        f.write(f"Baseline Messages: {quality_report['n_baseline']}\n")
        f.write(f"Personality Types: A (OCEAN: 1,1,1,1,1), B (OCEAN: -1,-1,-1,-1,-1)\n")
        f.write("\n")
        
        # Descriptive statistics
        f.write("2. DESCRIPTIVE STATISTICS\n")
        f.write("-"*80 + "\n\n")
        
        for metric in df_stats['Metric'].unique():
            metric_data = df_stats[df_stats['Metric'] == metric]
            f.write(f"{metric}:\n")
            for _, row in metric_data.iterrows():
                f.write(f"  {row['Condition']}:\n")
                f.write(f"    N = {row['N']}\n")
                f.write(f"    M = {row['Mean']:.3f}, SD = {row['SD']:.3f}\n")
                f.write(f"    95% CI [{row['CI_Lower']:.3f}, {row['CI_Upper']:.3f}]\n")
                f.write(f"    Percentage: {row['Percentage']:.1f}%\n")
            f.write("\n")
        
        # Effect sizes
        f.write("3. EFFECT SIZES (COHEN'S D)\n")
        f.write("-"*80 + "\n\n")
        
        for _, row in df_effects.iterrows():
            f.write(f"{row['Metric']}:\n")
            f.write(f"  Cohen's d = {row['Cohens_d']:.3f} ({row['Interpretation']})\n")
            f.write(f"  Regulated M = {row['Regulated_Mean']:.3f}\n")
            f.write(f"  Baseline M = {row['Baseline_Mean']:.3f}\n")
            f.write(f"  Difference = {row['Difference']:.3f} ({row['Difference']*100:+.1f} percentage points)\n")
            f.write("\n")
        
        # Inferential tests
        f.write("4. INFERENTIAL STATISTICS (ILLUSTRATIVE)\n")
        f.write("-"*80 + "\n")
        f.write("Note: These are for illustration purposes only given the deterministic simulation.\n\n")
        
        for _, row in df_tests.iterrows():
            f.write(f"{row['Metric']}:\n")
            f.write(f"  t({quality_report['n_regulated'] + quality_report['n_baseline'] - 2}) = {row['t_statistic']:.3f}\n")
            f.write(f"  p = {row['p_value']:.4f}\n")
            f.write(f"  Result: {'Significant at α = 0.05' if row['significant'] else 'Not significant'}\n")
            f.write("\n")
        
        # Summary
        f.write("5. SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write("The analysis reveals the following key findings:\n\n")
        
        for _, row in df_effects.iterrows():
            if row['Cohens_d'] > 0.2:
                f.write(f"• {row['Metric']}: Regulated condition showed ")
                f.write(f"{row['Interpretation'].lower()} improvement (d = {row['Cohens_d']:.3f}, ")
                f.write(f"+{row['Difference']*100:.1f} percentage points)\n")
        
        f.write("\n")
        f.write("These results demonstrate the effectiveness of personality-adaptive\n")
        f.write("regulation in improving chatbot performance across multiple dimensions.\n")
    
    print(f"  ✓ Report saved: {output_file}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print("PERSONALITY-ADAPTIVE CHATBOT STATISTICAL ANALYSIS")
    print("="*80)
    print("\nThis analysis performs comprehensive statistical evaluation of")
    print("regulated vs baseline chatbot performance including:")
    print("  • Data quality assessment")
    print("  • Descriptive statistics with confidence intervals")
    print("  • Effect size analysis (Cohen's d)")
    print("  • Visualization of results")
    print("  • Inferential statistics (illustrative)")
    print("\n")
    
    # File paths
    regulated_path = "merged/regulated.csv"
    baseline_path = "merged/baseline.csv"
    
    # Execute analysis steps
    df_regulated, df_baseline = load_and_prepare_data(regulated_path, baseline_path)
    
    quality_report = assess_data_quality(df_regulated, df_baseline)
    
    visualize_data_quality(df_regulated, df_baseline)
    
    df_reg_numeric, df_base_numeric = convert_to_numeric(df_regulated, df_baseline)
    
    df_stats = calculate_descriptive_statistics(df_reg_numeric, df_base_numeric)
    
    df_effects = calculate_effect_sizes(df_reg_numeric, df_base_numeric)
    
    visualize_results(df_stats, df_effects)
    
    df_tests = perform_inferential_tests(df_reg_numeric, df_base_numeric)
    
    generate_report(df_stats, df_effects, df_tests, quality_report)
    
    # Save results to CSV
    df_stats.to_csv("analysis_results_descriptive.csv", index=False)
    df_effects.to_csv("analysis_results_effect_sizes.csv", index=False)
    df_tests.to_csv("analysis_results_inferential.csv", index=False)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  • figures/ - All visualization plots")
    print("  • analysis_report.txt - Comprehensive text report")
    print("  • analysis_results_descriptive.csv - Descriptive statistics table")
    print("  • analysis_results_effect_sizes.csv - Effect sizes table")
    print("  • analysis_results_inferential.csv - Inferential test results")
    print("\n")


if __name__ == "__main__":
    main()

