#!/usr/bin/env python3
"""
Enhanced Statistical Analysis for MDPI Academic Rigor
Includes personality vector analysis and weighted scoring system
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PERSONALITY VECTOR ANALYSIS
# ============================================================================

def parse_personality_vector(vector_str):
    """
    Parse personality vector string like "(0, 0, 1, 1, 1)" to numpy array.
    Returns: tuple of (O, C, E, A, N) values
    """
    if pd.isna(vector_str):
        return None
    
    # Remove parentheses and split
    clean_str = str(vector_str).strip('()').replace(' ', '')
    try:
        values = [int(x) for x in clean_str.split(',')]
        if len(values) == 5:
            return tuple(values)
    except:
        return None
    return None


def analyze_personality_vectors(df_regulated):
    """
    Analyze personality vectors in the regulated dataset.
    """
    print("\n" + "="*80)
    print("PERSONALITY VECTOR ANALYSIS")
    print("="*80)
    
    # Parse personality vectors
    df_regulated['Personality_Vector'] = df_regulated['DETECTED PERSONALITY (O,C,E,A,N)'].apply(parse_personality_vector)
    
    # Filter valid vectors
    df_valid = df_regulated[df_regulated['Personality_Vector'].notna()].copy()
    
    if len(df_valid) == 0:
        print("⚠️ No valid personality vectors found")
        return None
    
    # Extract individual dimensions
    df_valid['O'] = df_valid['Personality_Vector'].apply(lambda x: x[0] if x else None)
    df_valid['C'] = df_valid['Personality_Vector'].apply(lambda x: x[1] if x else None)
    df_valid['E'] = df_valid['Personality_Vector'].apply(lambda x: x[2] if x else None)
    df_valid['A'] = df_valid['Personality_Vector'].apply(lambda x: x[3] if x else None)
    df_valid['N'] = df_valid['Personality_Vector'].apply(lambda x: x[4] if x else None)
    
    print(f"\n✓ Parsed {len(df_valid)} personality vectors")
    print(f"\nOCEAN Dimension Statistics:")
    print(f"  Openness (O):        Mean={df_valid['O'].mean():.2f}, SD={df_valid['O'].std():.2f}")
    print(f"  Conscientiousness (C): Mean={df_valid['C'].mean():.2f}, SD={df_valid['C'].std():.2f}")
    print(f"  Extraversion (E):    Mean={df_valid['E'].mean():.2f}, SD={df_valid['E'].std():.2f}")
    print(f"  Agreeableness (A):   Mean={df_valid['A'].mean():.2f}, SD={df_valid['A'].std():.2f}")
    print(f"  Neuroticism (N):     Mean={df_valid['N'].mean():.2f}, SD={df_valid['N'].std():.2f}")
    
    # Distribution of unique personality profiles
    print(f"\n✓ Unique Personality Profiles:")
    profile_counts = df_valid['DETECTED PERSONALITY (O,C,E,A,N)'].value_counts()
    for profile, count in profile_counts.items():
        print(f"  {profile}: {count} instances ({count/len(df_valid)*100:.1f}%)")
    
    return df_valid


def visualize_personality_vectors(df_valid, output_dir="figures"):
    """
    Create visualizations for personality vector analysis.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("PERSONALITY VECTOR VISUALIZATIONS")
    print("="*80)
    
    # Figure 1: OCEAN Dimensions Distribution
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    dimensions = ['O', 'C', 'E', 'A', 'N']
    dim_names = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    for i, (dim, name, color) in enumerate(zip(dimensions, dim_names, colors)):
        counts = df_valid[dim].value_counts().sort_index()
        axes[i].bar(counts.index, counts.values, color=color, alpha=0.7, edgecolor='black', linewidth=2)
        axes[i].set_xlabel('Trait Value', fontsize=11, fontweight='bold')
        axes[i].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[i].set_title(f'{name} ({dim})', fontsize=13, fontweight='bold')
        axes[i].grid(axis='y', alpha=0.3)
        axes[i].set_xticks([-1, 0, 1])
        
        # Add percentage labels
        for idx, val in zip(counts.index, counts.values):
            axes[i].text(idx, val + 0.5, f'{val}\\n({val/len(df_valid)*100:.1f}%)', 
                        ha='center', fontweight='bold', fontsize=9)
    
    # Hide the 6th subplot
    axes[5].axis('off')
    
    plt.suptitle('OCEAN Personality Dimensions Distribution', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/06_personality_dimensions.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/06_personality_dimensions.png")
    plt.close()
    
    # Figure 2: Personality Profile Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create matrix of personality vectors
    personality_matrix = df_valid[['O', 'C', 'E', 'A', 'N']].values
    
    # Sort by conversation
    df_sorted = df_valid.sort_values('Conversation_ID')
    personality_matrix_sorted = df_sorted[['O', 'C', 'E', 'A', 'N']].values
    
    im = ax.imshow(personality_matrix_sorted.T, aspect='auto', cmap='RdYlGn', vmin=-1, vmax=1)
    
    ax.set_yticks(range(5))
    ax.set_yticklabels(['O', 'C', 'E', 'A', 'N'], fontsize=12, fontweight='bold')
    ax.set_xlabel('Message Index', fontsize=12, fontweight='bold')
    ax.set_ylabel('OCEAN Dimensions', fontsize=12, fontweight='bold')
    ax.set_title('Personality Vector Heatmap Across Messages', fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Trait Value', fontsize=11, fontweight='bold')
    cbar.set_ticks([-1, 0, 1])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/07_personality_heatmap.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/07_personality_heatmap.png")
    plt.close()


# ============================================================================
# WEIGHTED SCORING SYSTEM
# ============================================================================

def calculate_weighted_scores(df, metrics_columns):
    """
    Calculate weighted scores using YES=2, NOT SURE=1, NO=0.
    
    Args:
        df: DataFrame with metric columns
        metrics_columns: List of column names to score
        
    Returns:
        Series with weighted scores
    """
    score_mapping = {'YES': 2, 'NOT SURE': 1, 'NO': 0, 
                     'Yes': 2, 'Not Sure': 1, 'No': 0,
                     'yes': 2, 'not sure': 1, 'no': 0}
    
    scores = pd.Series(0, index=df.index)
    
    for col in metrics_columns:
        if col in df.columns:
            col_scores = df[col].map(score_mapping).fillna(0)
            scores += col_scores
    
    return scores


def analyze_weighted_scores(df_regulated, df_baseline):
    """
    Compute and analyze weighted scores for all metrics.
    """
    print("\n" + "="*80)
    print("WEIGHTED SCORING ANALYSIS")
    print("="*80)
    
    # Define metric groups
    reg_metrics = {
        'Detection_Accuracy': ['DETECTION ACCURATE'],
        'Regulation_Effectiveness': ['REGULATION EFFECTIVE'],
        'Emotional_Tone': ['EMOTIONAL TONE APPROPRIATE'],
        'Relevance_Coherence': ['RELEVANCE & COHERENCE'],
        'Personality_Needs': ['PERSONALITY NEEDS ADDRESSED']
    }
    
    base_metrics = {
        'Emotional_Tone': ['EMOTIONAL TONE APPROPRIATE'],
        'Relevance_Coherence': ['RELEVANCE & COHERENCE'],
        'Personality_Needs': ['PERSONALITY NEEDS ADDRESSED']
    }
    
    # Calculate scores for regulated
    df_reg_scored = df_regulated.copy()
    for score_name, cols in reg_metrics.items():
        df_reg_scored[f'{score_name}_Score'] = calculate_weighted_scores(df_regulated, cols)
    
    # Calculate total regulated score (Emotional Tone + Relevance + Personality Needs)
    total_cols = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 'PERSONALITY NEEDS ADDRESSED']
    df_reg_scored['Total_Regulated_Score'] = calculate_weighted_scores(df_regulated, total_cols)
    
    # Calculate scores for baseline
    df_base_scored = df_baseline.copy()
    for score_name, cols in base_metrics.items():
        df_base_scored[f'{score_name}_Score'] = calculate_weighted_scores(df_baseline, cols)
    
    # Calculate total baseline score
    df_base_scored['Total_Baseline_Score'] = calculate_weighted_scores(df_baseline, total_cols)
    
    # Print statistics
    print("\n📊 Regulated Scores (Mean ± SD, Max=2 per metric):")
    for score_name in reg_metrics.keys():
        col = f'{score_name}_Score'
        if col in df_reg_scored.columns:
            mean = df_reg_scored[col].mean()
            std = df_reg_scored[col].std()
            max_val = df_reg_scored[col].max()
            print(f"  {score_name:<30}: {mean:.3f} ± {std:.3f} (max={max_val:.0f})")
    
    print(f"\n  {'Total_Regulated (max=6)':<30}: {df_reg_scored['Total_Regulated_Score'].mean():.3f} ± {df_reg_scored['Total_Regulated_Score'].std():.3f}")
    
    print("\n📊 Baseline Scores (Mean ± SD, Max=2 per metric):")
    for score_name in base_metrics.keys():
        col = f'{score_name}_Score'
        if col in df_base_scored.columns:
            mean = df_base_scored[col].mean()
            std = df_base_scored[col].std()
            max_val = df_base_scored[col].max()
            print(f"  {score_name:<30}: {mean:.3f} ± {std:.3f} (max={max_val:.0f})")
    
    print(f"\n  {'Total_Baseline (max=6)':<30}: {df_base_scored['Total_Baseline_Score'].mean():.3f} ± {df_base_scored['Total_Baseline_Score'].std():.3f}")
    
    return df_reg_scored, df_base_scored


def visualize_weighted_scores(df_reg_scored, df_base_scored, output_dir="figures"):
    """
    Visualize weighted scores comparison.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("WEIGHTED SCORE VISUALIZATIONS")
    print("="*80)
    
    # Figure 3: Score Comparison
    common_scores = ['Emotional_Tone_Score', 'Relevance_Coherence_Score', 'Personality_Needs_Score']
    score_labels = ['Emotional\nTone', 'Relevance &\nCoherence', 'Personality\nNeeds']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x_pos = np.arange(len(common_scores))
    width = 0.35
    
    reg_means = [df_reg_scored[score].mean() for score in common_scores]
    reg_stds = [df_reg_scored[score].std() for score in common_scores]
    base_means = [df_base_scored[score].mean() for score in common_scores]
    base_stds = [df_base_scored[score].std() for score in common_scores]
    
    bars1 = ax.bar(x_pos - width/2, reg_means, width, yerr=reg_stds,
                   label='Regulated', color='#3498db', alpha=0.8, 
                   edgecolor='black', linewidth=1.5, capsize=5)
    bars2 = ax.bar(x_pos + width/2, base_means, width, yerr=base_stds,
                   label='Baseline', color='#e74c3c', alpha=0.8,
                   edgecolor='black', linewidth=1.5, capsize=5)
    
    # Add value labels
    for i, (bar, mean) in enumerate(zip(bars1, reg_means)):
        ax.text(bar.get_x() + bar.get_width()/2, mean + reg_stds[i] + 0.05,
               f'{mean:.2f}', ha='center', fontweight='bold', fontsize=10)
    
    for i, (bar, mean) in enumerate(zip(bars2, base_means)):
        ax.text(bar.get_x() + bar.get_width()/2, mean + base_stds[i] + 0.05,
               f'{mean:.2f}', ha='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Evaluation Metric', fontsize=13, fontweight='bold')
    ax.set_ylabel('Weighted Score (0-2 scale)', fontsize=13, fontweight='bold')
    ax.set_title('Weighted Score Comparison: Regulated vs Baseline\\n(Error bars show ±1 SD)', 
                fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(score_labels, fontsize=11)
    ax.legend(fontsize=12)
    ax.set_ylim([0, 2.5])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/08_weighted_scores.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/08_weighted_scores.png")
    plt.close()
    
    # Figure 4: Total Score Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    
    total_data = [
        df_reg_scored['Total_Regulated_Score'].values,
        df_base_scored['Total_Baseline_Score'].values
    ]
    
    bp = ax.boxplot(total_data, labels=['Regulated', 'Baseline'],
                    patch_artist=True, widths=0.6,
                    boxprops=dict(facecolor='#3498db', alpha=0.7, edgecolor='black', linewidth=2),
                    medianprops=dict(color='red', linewidth=2),
                    whiskerprops=dict(color='black', linewidth=1.5),
                    capprops=dict(color='black', linewidth=1.5))
    
    bp['boxes'][1].set_facecolor('#e74c3c')
    
    # Add mean markers
    means = [np.mean(data) for data in total_data]
    ax.plot([1, 2], means, 'D', color='yellow', markersize=10, 
           markeredgecolor='black', markeredgewidth=2, label='Mean', zorder=3)
    
    # Add value annotations
    for i, (mean, median) in enumerate(zip(means, [np.median(d) for d in total_data])):
        ax.text(i+1, mean + 0.3, f'μ={mean:.2f}', ha='center', fontweight='bold', fontsize=11)
        ax.text(i+1, median - 0.3, f'M={median:.2f}', ha='center', fontweight='bold', fontsize=10, color='red')
    
    ax.set_ylabel('Total Score (0-6 scale)', fontsize=13, fontweight='bold')
    ax.set_title('Total Score Distribution: Regulated vs Baseline\\n(Box: Q1-Q3, Line: Median, Diamond: Mean)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([0, 7])
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/09_total_score_boxplot.png", dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_dir}/09_total_score_boxplot.png")
    plt.close()


# ============================================================================
# ADVANCED STATISTICAL TESTS (MDPI Academic Rigor)
# ============================================================================

def perform_advanced_statistical_tests(df_reg_scored, df_base_scored):
    """
    Perform comprehensive statistical tests for academic rigor.
    """
    print("\n" + "="*80)
    print("ADVANCED STATISTICAL TESTS")
    print("="*80)
    
    results = []
    
    # Common scores
    common_scores = ['Emotional_Tone_Score', 'Relevance_Coherence_Score', 'Personality_Needs_Score']
    
    for score in common_scores:
        if score in df_reg_scored.columns and score in df_base_scored.columns:
            reg_values = df_reg_scored[score].dropna().values
            base_values = df_base_scored[score].dropna().values
            
            # 1. Independent t-test
            t_stat, p_value = stats.ttest_ind(reg_values, base_values)
            
            # 2. Mann-Whitney U test (non-parametric)
            u_stat, p_mann = stats.mannwhitneyu(reg_values, base_values, alternative='two-sided')
            
            # 3. Effect size (Cohen's d)
            n1, n2 = len(reg_values), len(base_values)
            var1, var2 = np.var(reg_values, ddof=1), np.var(base_values, ddof=1)
            pooled_sd = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
            cohens_d = (np.mean(reg_values) - np.mean(base_values)) / pooled_sd if pooled_sd > 0 else 0
            
            # 4. Confidence interval for mean difference
            mean_diff = np.mean(reg_values) - np.mean(base_values)
            se_diff = np.sqrt(var1/n1 + var2/n2)
            ci_lower, ci_upper = stats.t.interval(0.95, n1+n2-2, loc=mean_diff, scale=se_diff)
            
            # 5. Levene's test for equality of variances
            levene_stat, p_levene = stats.levene(reg_values, base_values)
            
            # 6. Shapiro-Wilk test for normality
            _, p_shapiro_reg = stats.shapiro(reg_values) if len(reg_values) > 3 else (None, 1.0)
            _, p_shapiro_base = stats.shapiro(base_values) if len(base_values) > 3 else (None, 1.0)
            
            results.append({
                'Metric': score.replace('_Score', '').replace('_', ' '),
                'Mean_Diff': mean_diff,
                'CI_95_Lower': ci_lower,
                'CI_95_Upper': ci_upper,
                't_statistic': t_stat,
                'p_value_t': p_value,
                'U_statistic': u_stat,
                'p_value_mann_whitney': p_mann,
                'Cohens_d': cohens_d,
                'Levene_statistic': levene_stat,
                'p_value_levene': p_levene,
                'p_shapiro_reg': p_shapiro_reg,
                'p_shapiro_base': p_shapiro_base,
                'Normality_Met': (p_shapiro_reg > 0.05) and (p_shapiro_base > 0.05)
            })
    
    df_tests = pd.DataFrame(results)
    
    print("\n📊 Statistical Test Results:")
    print(f"{'Metric':<25} {'Mean Diff':<12} {'95% CI':<25} {'t':<8} {'p(t)':<10} {'p(MW)':<10} {'d':<8}")
    print("-"*105)
    
    for _, row in df_tests.iterrows():
        ci_str = f"[{row['CI_95_Lower']:.3f}, {row['CI_95_Upper']:.3f}]"
        sig_t = "***" if row['p_value_t'] < 0.001 else "**" if row['p_value_t'] < 0.01 else "*" if row['p_value_t'] < 0.05 else "ns"
        sig_mw = "***" if row['p_value_mann_whitney'] < 0.001 else "**" if row['p_value_mann_whitney'] < 0.01 else "*" if row['p_value_mann_whitney'] < 0.05 else "ns"
        
        print(f"{row['Metric']:<25} {row['Mean_Diff']:>11.3f} {ci_str:<25} {row['t_statistic']:>7.3f} {row['p_value_t']:>9.4f}{sig_t:<2} {row['p_value_mann_whitney']:>9.4f}{sig_mw:<2} {row['Cohens_d']:>7.3f}")
    
    print("\nSignificance: *** p<0.001, ** p<0.01, * p<0.05, ns = not significant")
    print("\n📊 Assumption Checks:")
    print(f"{'Metric':<25} {'Equal Var (Levene)':<25} {'Normality (Shapiro-Wilk)':<30}")
    print("-"*80)
    
    for _, row in df_tests.iterrows():
        var_test = f"F={row['Levene_statistic']:.3f}, p={row['p_value_levene']:.4f}"
        norm_status = "✓ Met" if row['Normality_Met'] else "⚠ Violated"
        print(f"{row['Metric']:<25} {var_test:<25} {norm_status:<30}")
    
    return df_tests


# ============================================================================
# RELIABILITY ANALYSIS
# ============================================================================

def calculate_cronbachs_alpha(df, columns):
    """
    Calculate Cronbach's Alpha for internal consistency.
    """
    # Convert to numeric
    data = df[columns].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data = data.dropna()
    
    if len(data) < 2:
        return None
    
    # Number of items
    k = len(columns)
    
    # Variance of each item
    item_variances = data.var(axis=0, ddof=1)
    
    # Variance of total scores
    total_variance = data.sum(axis=1).var(ddof=1)
    
    # Cronbach's Alpha
    if total_variance == 0:
        return None
    
    alpha = (k / (k - 1)) * (1 - item_variances.sum() / total_variance)
    
    return alpha


def perform_reliability_analysis(df_reg_scored):
    """
    Perform reliability analysis on evaluation metrics.
    """
    print("\n" + "="*80)
    print("RELIABILITY ANALYSIS")
    print("="*80)
    
    score_columns = ['Detection_Accuracy_Score', 'Regulation_Effectiveness_Score',
                    'Emotional_Tone_Score', 'Relevance_Coherence_Score', 'Personality_Needs_Score']
    
    available_cols = [col for col in score_columns if col in df_reg_scored.columns]
    
    if len(available_cols) < 2:
        print("⚠️ Insufficient metrics for reliability analysis")
        return None
    
    alpha = calculate_cronbachs_alpha(df_reg_scored, available_cols)
    
    if alpha is not None:
        print(f"\n📊 Cronbach's Alpha: {alpha:.3f}")
        
        if alpha >= 0.9:
            interpretation = "Excellent internal consistency"
        elif alpha >= 0.8:
            interpretation = "Good internal consistency"
        elif alpha >= 0.7:
            interpretation = "Acceptable internal consistency"
        elif alpha >= 0.6:
            interpretation = "Questionable internal consistency"
        else:
            interpretation = "Poor internal consistency"
        
        print(f"   Interpretation: {interpretation}")
        print(f"   (Based on {len(available_cols)} metrics across {len(df_reg_scored)} observations)")
        
        # Inter-item correlations
        print(f"\n📊 Inter-item Correlation Matrix:")
        corr_matrix = df_reg_scored[available_cols].corr()
        print(corr_matrix.round(3))
    
    return alpha


print("✓ Enhanced analysis functions loaded!")

