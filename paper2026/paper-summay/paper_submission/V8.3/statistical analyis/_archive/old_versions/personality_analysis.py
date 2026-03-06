#!/usr/bin/env python3
"""
Optional Personality Analysis Module
Extended OCEAN personality dimension analysis

This module provides supplementary personality-specific analyses
that may be useful for deeper insights into adaptation mechanisms.

Author: Unified Analysis Pipeline
Date: 2026
Version: 2.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import unified configuration
from visualization_config import (
    configure_matplotlib,
    save_figure,
    FigureTemplates,
    PlotStyler,
    PUBLICATION_CONFIG
)


# ============================================================================
# CONFIGURATION
# ============================================================================

configure_matplotlib()
C = PUBLICATION_CONFIG


# ============================================================================
# PERSONALITY VECTOR PARSING
# ============================================================================

def parse_personality_vector(vector_str):
    """
    Parse personality vector string like "(1, 1, 1, 1, 1)" to tuple.
    
    Returns:
        Tuple of (O, C, E, A, N) values or None if invalid
    """
    if pd.isna(vector_str):
        return None
    
    clean_str = str(vector_str).strip('()').replace(' ', '')
    try:
        values = [int(x) for x in clean_str.split(',')]
        if len(values) == 5:
            return tuple(values)
    except:
        return None
    return None


def extract_personality_dimensions(df: pd.DataFrame, 
                                   column: str = 'DETECTED PERSONALITY (O,C,E,A,N)') -> pd.DataFrame:
    """
    Extract individual OCEAN dimensions from personality vector column.
    
    Args:
        df: DataFrame with personality vector column
        column: Name of personality vector column
        
    Returns:
        DataFrame with added O, C, E, A, N columns
    """
    print("\n" + "="*80)
    print("EXTRACTING PERSONALITY DIMENSIONS")
    print("="*80)
    
    df = df.copy()
    
    # Parse vectors
    df['Personality_Vector'] = df[column].apply(parse_personality_vector)
    
    # Filter valid vectors
    df_valid = df[df['Personality_Vector'].notna()].copy()
    
    if len(df_valid) == 0:
        print("  ? No valid personality vectors found")
        return df
    
    # Extract individual dimensions
    df_valid['O'] = df_valid['Personality_Vector'].apply(lambda x: x[0] if x else None)
    df_valid['C'] = df_valid['Personality_Vector'].apply(lambda x: x[1] if x else None)
    df_valid['E'] = df_valid['Personality_Vector'].apply(lambda x: x[2] if x else None)
    df_valid['A'] = df_valid['Personality_Vector'].apply(lambda x: x[3] if x else None)
    df_valid['N'] = df_valid['Personality_Vector'].apply(lambda x: x[4] if x else None)
    
    print(f"? Extracted dimensions from {len(df_valid)} vectors")
    print(f"\nOCEAN Statistics:")
    for dim, name in [('O', 'Openness'), ('C', 'Conscientiousness'), 
                      ('E', 'Extraversion'), ('A', 'Agreeableness'), 
                      ('N', 'Neuroticism')]:
        mean_val = df_valid[dim].mean()
        std_val = df_valid[dim].std()
        print(f"  {name:20s} ({dim}): M={mean_val:+.2f}, SD={std_val:.2f}")
    
    return df_valid


# ============================================================================
# VISUALIZATION: PERSONALITY DIMENSIONS
# ============================================================================

def visualize_personality_dimensions(df: pd.DataFrame, 
                                    output_dir: str = "figures"):
    """
    Create comprehensive personality dimensions visualization.
    
    Generates a 2x3 panel figure showing distribution of each OCEAN dimension.
    """
    print("\n" + "="*80)
    print("CREATING FIGURE 5: PERSONALITY PROFILES")
    print("="*80)
    
    if 'O' not in df.columns:
        print("  ? Personality dimensions not extracted. Run extract_personality_dimensions() first.")
        return
    
    fig, axes = plt.subplots(2, 3, figsize=(C.FIGURE_WIDTH_DOUBLE, 
                                            C.FIGURE_HEIGHT_TALL), dpi=150)
    axes = axes.flatten()
    
    dimensions = ['O', 'C', 'E', 'A', 'N']
    dim_names = ['Openness', 'Conscientiousness', 'Extraversion', 
                'Agreeableness', 'Neuroticism']
    colors = [C.COLOR_PALETTE[i % len(C.COLOR_PALETTE)] for i in range(5)]
    
    for i, (dim, name, color) in enumerate(zip(dimensions, dim_names, colors)):
        counts = df[dim].value_counts().sort_index()
        
        bars = axes[i].bar(counts.index, counts.values, 
                          color=color, alpha=0.7, 
                          edgecolor='black', linewidth=1.5)
        
        axes[i].set_xlabel('Trait Value', fontweight='bold')
        axes[i].set_ylabel('Frequency', fontweight='bold')
        axes[i].set_title(f'{name} ({dim})', fontweight='bold', pad=10)
        axes[i].set_xticks([-1, 0, 1])
        PlotStyler.style_bar_chart(axes[i])
        
        # Add percentage labels
        for idx, val in zip(counts.index, counts.values):
            pct = val / len(df) * 100
            axes[i].text(idx, val + 0.5, f'{val}\n({pct:.1f}%)', 
                        ha='center', fontweight='bold', 
                        fontsize=C.FONT_SIZE_SMALL)
    
    # Hide the 6th subplot
    axes[5].axis('off')
    
    fig.suptitle('OCEAN Personality Dimensions Distribution', 
                fontsize=C.FONT_SIZE_TITLE, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    save_figure(fig, '05_personality_profiles', output_dir)


# ============================================================================
# ANALYSIS: PERSONALITY PROFILE SUMMARY
# ============================================================================

def summarize_personality_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create summary of unique personality profiles.
    
    Returns:
        DataFrame with profile counts and proportions
    """
    print("\n" + "="*80)
    print("PERSONALITY PROFILE SUMMARY")
    print("="*80)
    
    if 'Personality_Vector' not in df.columns:
        print("  ? Personality vectors not parsed")
        return pd.DataFrame()
    
    # Count unique profiles
    profile_col = 'DETECTED PERSONALITY (O,C,E,A,N)'
    if profile_col not in df.columns:
        print("  ? Personality column not found")
        return pd.DataFrame()
    
    profile_counts = df[profile_col].value_counts()
    
    summary = pd.DataFrame({
        'Profile': profile_counts.index,
        'Count': profile_counts.values,
        'Proportion': profile_counts.values / len(df)
    })
    
    print(f"\nUnique Profiles: {len(summary)}")
    print(f"\n{'Profile':<20} {'Count':<10} {'Proportion':<15}")
    print("-" * 45)
    for _, row in summary.iterrows():
        print(f"{row['Profile']:<20} {row['Count']:<10} {row['Proportion']:<15.1%}")
    
    return summary


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute personality analysis pipeline."""
    print("\n" + "="*80)
    print("OPTIONAL PERSONALITY ANALYSIS")
    print("Extended OCEAN Dimension Analysis")
    print("="*80)
    
    # Load regulated data
    regulated_path = "merged/regulated.csv"
    
    try:
        df_regulated = pd.read_csv(regulated_path)
        print(f"\n? Loaded: {regulated_path}")
        print(f"  Shape: {df_regulated.shape}")
    except FileNotFoundError:
        print(f"\n? File not found: {regulated_path}")
        print("  Please run master_analysis.py first to generate data.")
        return
    
    # Extract personality dimensions
    df_with_dims = extract_personality_dimensions(df_regulated)
    
    if len(df_with_dims) == 0:
        print("\n? No valid personality data found. Exiting.")
        return
    
    # Summarize profiles
    profile_summary = summarize_personality_profiles(df_with_dims)
    
    # Save summary
    if len(profile_summary) > 0:
        profile_summary.to_csv("analysis_results_personality_profiles.csv", index=False)
        print(f"\n? Saved: analysis_results_personality_profiles.csv")
    
    # Create visualization
    visualize_personality_dimensions(df_with_dims)
    
    print("\n" + "="*80)
    print("? PERSONALITY ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated:")
    print("  � 05_personality_profiles.png - OCEAN dimension distributions")
    print("  � analysis_results_personality_profiles.csv - Profile summary")
    print("\nNote: This is supplementary analysis. Core results are in master_analysis.py")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
