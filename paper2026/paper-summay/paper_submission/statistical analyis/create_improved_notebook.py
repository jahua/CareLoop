#!/usr/bin/env python3
"""
Script to create an improved Jupyter notebook with inline visualizations.
This notebook is designed for step-by-step interactive analysis.
"""

import nbformat as nbf

# Create a new notebook
nb = nbf.v4.new_notebook()

# Add cells
cells = []

# Title cell
cells.append(nbf.v4.new_markdown_cell("""# Statistical Analysis of Personality-Adaptive Chatbot Performance
## Regulated vs Baseline Comparison

This notebook performs comprehensive statistical analysis including:
- **Data quality assessment** with visualizations
- **Descriptive statistics** (means, SDs, confidence intervals)
- **Effect size analysis** (Cohen's d)
- **Comparative visualizations**
- **Inferential statistics** (illustrative)

---"""))

# Setup cell
cells.append(nbf.v4.new_markdown_cell("## Setup: Import Libraries"))

cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Enable inline plotting
%matplotlib inline

print("✓ Libraries loaded successfully!")"""))

# Load functions cell
cells.append(nbf.v4.new_markdown_cell("## Load Analysis Functions"))

cells.append(nbf.v4.new_code_cell("""# Import functions from the main script
from statistical_analysis import (
    load_and_prepare_data,
    assess_data_quality,
    convert_to_numeric,
    calculate_descriptive_statistics,
    calculate_effect_sizes,
    perform_inferential_tests
)

print("✓ Analysis functions loaded!")"""))

# Step 1
cells.append(nbf.v4.new_markdown_cell("""---
## Step 1: Load and Prepare Data

Load the regulated and baseline datasets:"""))

cells.append(nbf.v4.new_code_cell("""df_regulated, df_baseline = load_and_prepare_data(
    regulated_path="merged/regulated.csv",
    baseline_path="merged/baseline.csv"
)"""))

cells.append(nbf.v4.new_code_cell("""# Display first few rows
print("\\n📊 Regulated Dataset (first 3 rows):")
display(df_regulated[['MSG. NO.', 'Personality_Type', 'Conversation_ID', 
                       'DETECTION ACCURATE', 'REGULATION EFFECTIVE']].head(3))

print("\\n📊 Baseline Dataset (first 3 rows):")
display(df_baseline[['MSG. NO.', 'Personality_Type', 'Conversation_ID',
                      'EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE']].head(3))"""))

# Step 2
cells.append(nbf.v4.new_markdown_cell("""---
## Step 2: Data Quality Assessment"""))

cells.append(nbf.v4.new_code_cell("quality_report = assess_data_quality(df_regulated, df_baseline)"))

# Step 3 - Visualizations
cells.append(nbf.v4.new_markdown_cell("""---
## Step 3: Visualize Data Quality"""))

cells.append(nbf.v4.new_code_cell("""# Sample Distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

reg_counts = df_regulated.groupby('Personality_Type')['Conversation_ID'].nunique()
axes[0].bar(reg_counts.index, reg_counts.values, color=['#3498db', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=2)
axes[0].set_xlabel('Personality Type', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Number of Conversations', fontsize=12, fontweight='bold')
axes[0].set_title('Sample Distribution', fontsize=14, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

for i, v in enumerate(reg_counts.values):
    axes[0].text(i, v + 0.1, str(v), ha='center', fontweight='bold')

msg_counts = df_regulated.groupby('Conversation_ID').size()
axes[1].hist(msg_counts, bins=range(1, 10), color='#2ecc71', alpha=0.7, edgecolor='black', linewidth=2)
axes[1].set_xlabel('Messages per Conversation', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Count', fontsize=12, fontweight='bold')
axes[1].set_title('Message Distribution', fontsize=14, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_code_cell("""# Missing Data Heatmap
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

missing_reg = df_regulated.isnull().astype(int)
sns.heatmap(missing_reg.T, cmap='RdYlGn_r', cbar=True, ax=axes[0], 
            xticklabels=False, yticklabels=df_regulated.columns)
axes[0].set_title('Missing Data: Regulated', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Sample Index', fontsize=12)

missing_base = df_baseline.isnull().astype(int)
sns.heatmap(missing_base.T, cmap='RdYlGn_r', cbar=True, ax=axes[1],
            xticklabels=False, yticklabels=df_baseline.columns)
axes[1].set_title('Missing Data: Baseline', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Sample Index', fontsize=12)

plt.tight_layout()
plt.show()"""))

# Step 4
cells.append(nbf.v4.new_markdown_cell("""---
## Step 4: Convert Categorical to Numeric"""))

cells.append(nbf.v4.new_code_cell("df_reg_numeric, df_base_numeric = convert_to_numeric(df_regulated, df_baseline)"))

# Step 5
cells.append(nbf.v4.new_markdown_cell("""---
## Step 5: Descriptive Statistics"""))

cells.append(nbf.v4.new_code_cell("df_stats = calculate_descriptive_statistics(df_reg_numeric, df_base_numeric)"))

cells.append(nbf.v4.new_code_cell("""print("\\n📊 Descriptive Statistics Table:")
display(df_stats.round(3))"""))

cells.append(nbf.v4.new_code_cell("""# Visualize descriptive statistics
common_metrics = ['EMOTIONAL TONE APPROPRIATE', 'RELEVANCE & COHERENCE', 'PERSONALITY NEEDS ADDRESSED']
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, metric in enumerate(common_metrics):
    metric_data = df_stats[df_stats['Metric'] == metric]
    if len(metric_data) > 0:
        conditions = metric_data['Condition'].tolist()
        means = metric_data['Mean'].tolist()
        colors = ['#3498db' if c == 'Regulated' else '#e74c3c' for c in conditions]
        
        bars = axes[i].bar(conditions, means, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        axes[i].set_title(metric.replace(' ', '\\n'), fontsize=11, fontweight='bold')
        axes[i].set_ylabel('Mean Score', fontsize=10, fontweight='bold')
        axes[i].set_ylim([0, 1.1])
        axes[i].grid(axis='y', alpha=0.3)
        
        for j, (bar, mean) in enumerate(zip(bars, means)):
            axes[i].text(bar.get_x() + bar.get_width()/2, mean + 0.05, 
                        f'{mean*100:.1f}%', ha='center', fontweight='bold')

plt.suptitle('Descriptive Statistics by Condition', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""))

# Step 6
cells.append(nbf.v4.new_markdown_cell("""---
## Step 6: Effect Size Analysis (Cohen's d)"""))

cells.append(nbf.v4.new_code_cell("df_effects = calculate_effect_sizes(df_reg_numeric, df_base_numeric)"))

cells.append(nbf.v4.new_code_cell("""print("\\n📊 Effect Sizes Table:")
display(df_effects.round(3))"""))

cells.append(nbf.v4.new_code_cell("""# Visualize effect sizes
fig, ax = plt.subplots(figsize=(12, 6))

metrics = df_effects['Metric'].tolist()
cohens_d = df_effects['Cohens_d'].tolist()
colors = ['#2ecc71' if d > 0 else '#e74c3c' for d in cohens_d]

y_pos = np.arange(len(metrics))
bars = ax.barh(y_pos, cohens_d, color=colors, alpha=0.7, edgecolor='black', linewidth=2)

# Reference lines
ax.axvline(x=0, color='black', linestyle='-', linewidth=2)
for val in [0.2, 0.5, 0.8]:
    ax.axvline(x=val, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.axvline(x=-val, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)

# Labels
for i, (d, interpretation) in enumerate(zip(cohens_d, df_effects['Interpretation'])):
    label_x = d + (0.3 if d > 0 else -0.3)
    ax.text(label_x, i, f'd = {d:.3f}\\n({interpretation})', 
           va='center', ha='left' if d > 0 else 'right', fontweight='bold', fontsize=10)

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=11)
ax.set_xlabel("Cohen's d (Effect Size)", fontsize=12, fontweight='bold')
ax.set_title("Effect Sizes: Regulated vs Baseline", fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# Step 7
cells.append(nbf.v4.new_markdown_cell("""---
## Step 7: Performance Comparison"""))

cells.append(nbf.v4.new_code_cell("""# Percentage improvement
fig, ax = plt.subplots(figsize=(12, 6))

metrics = df_effects['Metric'].tolist()
improvement = (df_effects['Difference'] * 100).tolist()
colors = ['#2ecc71' if i > 0 else '#e74c3c' for i in improvement]

y_pos = np.arange(len(metrics))
bars = ax.barh(y_pos, improvement, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax.axvline(x=0, color='black', linestyle='-', linewidth=2)

# Value labels
for i, val in enumerate(improvement):
    label_x = val + (2 if val > 0 else -2)
    ax.text(label_x, i, f'{val:+.1f}%', 
           va='center', ha='left' if val > 0 else 'right', fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels(metrics, fontsize=11)
ax.set_xlabel('Percentage Point Difference (%)', fontsize=12, fontweight='bold')
ax.set_title('Percentage Point Improvement: Regulated vs Baseline', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# Step 8
cells.append(nbf.v4.new_markdown_cell("""---
## Step 8: Inferential Statistics (Illustrative)

**Note:** For illustration purposes only given the deterministic simulation."""))

cells.append(nbf.v4.new_code_cell("df_tests = perform_inferential_tests(df_reg_numeric, df_base_numeric)"))

cells.append(nbf.v4.new_code_cell("""print("\\n📊 Inferential Statistics:")
display(df_tests.round(4))"""))

# Step 9
cells.append(nbf.v4.new_markdown_cell("""---
## Step 9: Summary and Export"""))

cells.append(nbf.v4.new_code_cell("""# Save results
df_stats.to_csv("analysis_results_descriptive.csv", index=False)
df_effects.to_csv("analysis_results_effect_sizes.csv", index=False)
df_tests.to_csv("analysis_results_inferential.csv", index=False)

print("✅ Results saved successfully!")"""))

# Summary cell
cells.append(nbf.v4.new_code_cell("""# Create summary
print("="*80)
print("KEY FINDINGS")
print("="*80)
print(f"\\n📊 Sample: {quality_report['n_conversations']} conversations")
print(f"  • Regulated: {quality_report['n_regulated']} messages")
print(f"  • Baseline: {quality_report['n_baseline']} messages")

print(f"\\n🎯 Main Finding:")
for _, row in df_effects.iterrows():
    if abs(row['Cohens_d']) >= 0.8:
        print(f"\\n  • {row['Metric']}")
        print(f"    Cohen's d: {row['Cohens_d']:.3f} ({row['Interpretation']})")
        print(f"    Improvement: {row['Difference']*100:+.1f} percentage points")

print("\\n" + "="*80)
print("Analysis complete! ✅")
print("="*80)"""))

# Add all cells to notebook
nb['cells'] = cells

# Write notebook
output_path = "statistical_analysis_improved.ipynb"
with open(output_path, 'w') as f:
    nbf.write(nb, f)

print(f"✓ Improved notebook created: {output_path}")
print("\\nTo use the notebook:")
print("  1. Activate virtual environment")
print("  2. Run: jupyter notebook statistical_analysis_improved.ipynb")



