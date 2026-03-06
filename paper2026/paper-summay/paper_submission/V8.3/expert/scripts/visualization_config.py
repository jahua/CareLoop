#!/usr/bin/env python3
"""
Unified Visualization Configuration for Publication-Ready Figures
Academic Standards for MDPI, IEEE, Nature, and other peer-reviewed journals

Author: Statistical Analysis Pipeline
Date: 2026
Version: 1.0
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, Tuple, List
from dataclasses import dataclass


# ============================================================================
# PUBLICATION STANDARDS CONFIGURATION
# ============================================================================

@dataclass
class PublicationStandards:
    """
    Central configuration for all publication-standard visualizations.
    
    Based on FIGURE_STYLE_GUIDE.md requirements:
    - Export as PDF (vector) or PNG at ≥300 DPI (≥600 DPI for line art)
    - 1-column (~85mm): ≥2000 px width
    - 2-column (~170mm): ≥4000 px width
    - Typography: 8-9 pt labels, 9-10 pt legends
    - Line width: 1.0-1.5 pt
    - Colorblind-safe palette
    - Tight cropping
    """
    
    # Resolution and Format (FIGURE_STYLE_GUIDE.md compliant)
    DPI: int = 300  # Standard for photos/plots (use 600 for line art)
    DPI_LINE_ART: int = 600  # Higher resolution for text-heavy diagrams
    FORMAT: str = 'png'
    FORMAT_VECTOR: str = 'pdf'  # Preferred format per style guide
    FACECOLOR: str = 'white'
    BBOX_INCHES: str = 'tight'  # Tight cropping per guide
    
    # Figure Dimensions (MDPI column widths)
    # 1-column: 85mm = 3.35 inches → 2000px at 600 DPI
    # 2-column: 170mm = 6.69 inches → 4000px at 600 DPI
    FIGURE_WIDTH_SINGLE_MM: float = 85.0  # MDPI single column width
    FIGURE_WIDTH_DOUBLE_MM: float = 170.0  # MDPI double column width
    FIGURE_WIDTH_SINGLE: float = 3.35  # inches (85mm)
    FIGURE_WIDTH_DOUBLE: float = 6.69  # inches (170mm)
    FIGURE_HEIGHT_SHORT: float = 2.5
    FIGURE_HEIGHT_MEDIUM: float = 4.0
    FIGURE_HEIGHT_TALL: float = 6.0
    
    # Typography (FIGURE_STYLE_GUIDE.md: 8-9 pt labels, 9-10 pt legends)
    FONT_FAMILY: str = 'sans-serif'
    FONT_SANS_SERIF: List[str] = None
    FONT_SIZE_AXIS_LABELS: int = 9  # 8-9 pt per guide
    FONT_SIZE_TICK_LABELS: int = 8  # 8-9 pt per guide
    FONT_SIZE_LEGEND: int = 9  # 9-10 pt per guide
    FONT_SIZE_TITLE: int = 11  # Slightly larger for titles
    FONT_WEIGHT: str = 'regular'  # Avoid thin fonts per guide
    
    # Line Widths (FIGURE_STYLE_GUIDE.md: 1.0-1.5 pt)
    LINE_WIDTH: float = 1.25  # Within 1.0-1.5 pt range
    LINE_WIDTH_AXES: float = 1.0  # Slightly heavier than grid
    LINE_WIDTH_GRID: float = 0.5
    AXES_LINE_WIDTH: float = 1.0
    GRID_LINE_WIDTH: float = 0.5
    TICK_WIDTH: float = 0.8
    ERROR_BAR_WIDTH: float = 1.0
    ERROR_CAP_SIZE: float = 4
    
    # Colors (Okabe�Ito; colorblind-friendly, print-safe)
    # https://jfly.uni-koeln.de/color/
    COLOR_BLUE: str = '#0072B2'
    COLOR_ORANGE: str = '#E69F00'
    COLOR_GREEN: str = '#009E73'
    COLOR_RED: str = '#D55E00'
    COLOR_PURPLE: str = '#CC79A7'
    COLOR_GRAY: str = '#666666'
    
    # Alternative: matplotlib_for_papers color scheme
    # https://github.com/jbmouret/matplotlib_for_papers
    # These are the exact colors used in the guide's examples (optional)
    MPL_PAPERS_BLUE: str = '#006BB2'   # Primary blue
    MPL_PAPERS_RED: str = '#B22400'    # Primary red

    # Condition colors (using default Okabe-Ito scheme)
    COLOR_REGULATED: str = COLOR_BLUE    # Default: Okabe-Ito Blue
    COLOR_BASELINE: str = COLOR_ORANGE   # Default: Okabe-Ito Orange

    # Accents
    COLOR_POSITIVE: str = COLOR_GREEN
    COLOR_NEGATIVE: str = COLOR_RED
    COLOR_NEUTRAL: str = COLOR_GRAY
    COLOR_ACCENT: str = COLOR_PURPLE

    # Soft fills (very light tints for bars/boxes)
    FILL_BLUE: str = '#EAF2FB'
    FILL_ORANGE: str = '#FFF4DB'
    FILL_GREEN: str = '#EAF7EF'
    FILL_NEUTRAL: str = '#F5F6F7'
    FILL_RED: str = '#FDE7D5'
    FILL_PURPLE: str = '#F7ECF3'
    
    # Extended color palette for multi-category plots
    COLOR_PALETTE: List[str] = None
    
    # Grid and Style (publication-friendly)
    STYLE: str = 'whitegrid'
    GRID_ALPHA: float = 0.18
    GRID_LINESTYLE: str = '-'
    
    def __post_init__(self):
        if self.FONT_SANS_SERIF is None:
            # DejaVu Sans is always available with matplotlib; Arial/Helvetica if installed.
            self.FONT_SANS_SERIF = ['DejaVu Sans', 'Arial', 'Helvetica']
        if self.COLOR_PALETTE is None:
            self.COLOR_PALETTE = [
                self.COLOR_REGULATED,
                self.COLOR_BASELINE,
                self.COLOR_POSITIVE,
                self.COLOR_NEGATIVE,
                self.COLOR_NEUTRAL,
                self.COLOR_ACCENT,
            ]


# ============================================================================
# GLOBAL CONFIGURATION INSTANCE
# ============================================================================

PUBLICATION_CONFIG = PublicationStandards()


# ============================================================================
# MATPLOTLIB CONFIGURATION
# ============================================================================

def configure_matplotlib(config: PublicationStandards = PUBLICATION_CONFIG, 
                        use_matplotlib_papers_defaults: bool = True,
                        apply_style_guide: bool = True):
    """
    Apply publication-standard configuration to matplotlib.
    Now enhanced with FIGURE_STYLE_GUIDE.md requirements.
    
    Args:
        config: PublicationStandards configuration object
        use_matplotlib_papers_defaults: Use matplotlib_for_papers guide
        apply_style_guide: Apply FIGURE_STYLE_GUIDE.md requirements
    """
    if apply_style_guide:
        # FIGURE_STYLE_GUIDE.md compliant configuration
        params = {
            # Typography (8-9 pt labels, 9-10 pt legends per guide)
            'axes.labelsize': config.FONT_SIZE_AXIS_LABELS,  # 9 pt
            'xtick.labelsize': config.FONT_SIZE_TICK_LABELS,  # 8 pt
            'ytick.labelsize': config.FONT_SIZE_TICK_LABELS,  # 8 pt
            'legend.fontsize': config.FONT_SIZE_LEGEND,  # 9 pt
            'font.size': config.FONT_SIZE_TICK_LABELS,  # Base 8 pt
            'axes.titlesize': config.FONT_SIZE_TITLE,  # 11 pt
            'font.weight': config.FONT_WEIGHT,  # Regular weight
            
            # Line widths (1.0-1.5 pt per guide)
            'lines.linewidth': config.LINE_WIDTH,  # 1.25 pt
            'axes.linewidth': config.LINE_WIDTH_AXES,  # 1.0 pt
            'grid.linewidth': config.LINE_WIDTH_GRID,  # 0.5 pt
            'xtick.major.width': config.TICK_WIDTH,
            'ytick.major.width': config.TICK_WIDTH,
            
            # Format and resolution
            'savefig.dpi': config.DPI,  # 300 DPI minimum
            'savefig.bbox': config.BBOX_INCHES,  # Tight cropping
            'savefig.pad_inches': 0.05,  # Minimal padding
            'savefig.facecolor': config.FACECOLOR,
            'savefig.format': config.FORMAT,
            
            # Font family (consistent across figures)
            'font.family': config.FONT_FAMILY,
            
            # Figure appearance
            'figure.facecolor': config.FACECOLOR,
            'axes.facecolor': config.FACECOLOR,
            'text.usetex': False,
        }
        plt.rcParams.update(params)
        plt.rcParams['font.sans-serif'] = config.FONT_SANS_SERIF
        
    elif use_matplotlib_papers_defaults:
        # Exact configuration from matplotlib_for_papers guide
        # https://github.com/jbmouret/matplotlib_for_papers
        params = {
            'axes.labelsize': 8,
            'font.size': 8,
            'legend.fontsize': 10,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'text.usetex': False,
            'figure.figsize': [4.5, 4.5]
        }
        plt.rcParams.update(params)
        
        # Additional settings for modern matplotlib
        plt.rcParams['font.family'] = config.FONT_FAMILY
        plt.rcParams['font.sans-serif'] = config.FONT_SANS_SERIF
        plt.rcParams['lines.linewidth'] = 2  # Guide recommends linewidth=2
        plt.rcParams['savefig.dpi'] = config.DPI
        plt.rcParams['savefig.bbox'] = config.BBOX_INCHES
        plt.rcParams['savefig.facecolor'] = config.FACECOLOR
        plt.rcParams['figure.facecolor'] = config.FACECOLOR
        plt.rcParams['axes.facecolor'] = config.FACECOLOR
        
    else:
        # Original custom configuration
        sns.set_style(config.STYLE)
        
        # Font configuration
        plt.rcParams['font.family'] = config.FONT_FAMILY
        plt.rcParams['font.sans-serif'] = config.FONT_SANS_SERIF
        plt.rcParams['font.size'] = config.FONT_SIZE_BASE
        plt.rcParams['axes.labelsize'] = config.FONT_SIZE_MEDIUM
        plt.rcParams['axes.titlesize'] = config.FONT_SIZE_LARGE
        plt.rcParams['xtick.labelsize'] = config.FONT_SIZE_BASE
        plt.rcParams['ytick.labelsize'] = config.FONT_SIZE_BASE
        plt.rcParams['legend.fontsize'] = config.FONT_SIZE_BASE
        plt.rcParams['figure.titlesize'] = config.FONT_SIZE_TITLE
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['axes.labelweight'] = 'bold'
        
        # Line widths
        plt.rcParams['lines.linewidth'] = config.LINE_WIDTH
        plt.rcParams['axes.linewidth'] = config.AXES_LINE_WIDTH
        plt.rcParams['grid.linewidth'] = config.GRID_LINE_WIDTH
        plt.rcParams['xtick.major.width'] = config.TICK_WIDTH
        plt.rcParams['ytick.major.width'] = config.TICK_WIDTH
        
        # Figure defaults
        plt.rcParams['figure.dpi'] = 100  # Display DPI
        plt.rcParams['savefig.dpi'] = config.DPI  # Save DPI
        plt.rcParams['savefig.bbox'] = config.BBOX_INCHES
        plt.rcParams['savefig.facecolor'] = config.FACECOLOR
        plt.rcParams['savefig.format'] = config.FORMAT
        plt.rcParams['figure.facecolor'] = config.FACECOLOR
        plt.rcParams['axes.facecolor'] = config.FACECOLOR
        plt.rcParams['savefig.transparent'] = False
        
        # Grid
        plt.rcParams['grid.alpha'] = config.GRID_ALPHA
        plt.rcParams['grid.linestyle'] = config.GRID_LINESTYLE
        plt.rcParams['grid.color'] = '#DADCDC'

        # Colors / axes
        plt.rcParams['axes.edgecolor'] = '#DADCDC'
        plt.rcParams['axes.labelcolor'] = '#1F1F1F'
        plt.rcParams['xtick.color'] = '#1F1F1F'
        plt.rcParams['ytick.color'] = '#1F1F1F'
        plt.rcParams['text.color'] = '#1F1F1F'

        # Legend
        plt.rcParams['legend.frameon'] = True
        plt.rcParams['legend.framealpha'] = 1.0
        plt.rcParams['legend.edgecolor'] = '#DADCDC'


# ============================================================================
# FIGURE TEMPLATES
# ============================================================================

class FigureTemplates:
    """
    Pre-configured figure templates for common plot types.
    Now FIGURE_STYLE_GUIDE.md compliant with proper MDPI column widths.
    """
    
    @staticmethod
    def create_single_panel(height: str = 'medium', 
                          config: PublicationStandards = PUBLICATION_CONFIG) -> Tuple:
        """
        Create single-panel figure (MDPI 1-column: 85mm = 3.35")
        
        Args:
            height: 'short', 'medium', or 'tall'
            config: Publication configuration
            
        Returns:
            fig, ax tuple
            
        Note: Sized for MDPI single column (85mm) per FIGURE_STYLE_GUIDE.md
        """
        height_map = {
            'short': config.FIGURE_HEIGHT_SHORT,
            'medium': config.FIGURE_HEIGHT_MEDIUM,
            'tall': config.FIGURE_HEIGHT_TALL
        }
        h = height_map.get(height, config.FIGURE_HEIGHT_MEDIUM)
        
        # Use MDPI single-column width (85mm = 3.35 inches)
        fig, ax = plt.subplots(figsize=(config.FIGURE_WIDTH_SINGLE, h), dpi=150)
        return fig, ax
    
    @staticmethod
    def create_double_panel(height: str = 'medium',
                          config: PublicationStandards = PUBLICATION_CONFIG) -> Tuple:
        """
        Create double-panel figure (MDPI 2-column: 170mm = 6.69")
        
        Args:
            height: 'short', 'medium', or 'tall'
            config: Publication configuration
            
        Returns:
            fig, axes tuple (1x2 layout)
            
        Note: Sized for MDPI double column (170mm) per FIGURE_STYLE_GUIDE.md
        """
        height_map = {
            'short': config.FIGURE_HEIGHT_SHORT,
            'medium': config.FIGURE_HEIGHT_MEDIUM,
            'tall': config.FIGURE_HEIGHT_TALL
        }
        h = height_map.get(height, config.FIGURE_HEIGHT_MEDIUM)
        
        # Use MDPI double-column width (170mm = 6.69 inches)
        fig, axes = plt.subplots(1, 2, figsize=(config.FIGURE_WIDTH_DOUBLE, h), dpi=150)
        return fig, axes
    
    @staticmethod
    def create_quad_panel(config: PublicationStandards = PUBLICATION_CONFIG) -> Tuple:
        """Create quad-panel figure (2x2 layout)."""
        fig, axes = plt.subplots(2, 2, 
                                figsize=(config.FIGURE_WIDTH_DOUBLE, 
                                        config.FIGURE_HEIGHT_TALL),
                                dpi=150)
        return fig, axes
    
    @staticmethod
    def create_wide_panel(config: PublicationStandards = PUBLICATION_CONFIG) -> Tuple:
        """Create wide panel for complex visualizations."""
        fig, ax = plt.subplots(figsize=(config.FIGURE_WIDTH_DOUBLE, 
                                       config.FIGURE_HEIGHT_MEDIUM),
                              dpi=150)
        return fig, ax


# ============================================================================
# STYLING UTILITIES
# ============================================================================

class PlotStyler:
    """Utilities for consistent plot styling."""
    
    @staticmethod
    def style_bar_chart(ax, config: PublicationStandards = PUBLICATION_CONFIG,
                       use_guide_style: bool = True):
        """
        Apply consistent styling to bar charts.
        
        Args:
            ax: Matplotlib axes
            config: Configuration object
            use_guide_style: Use exact matplotlib_for_papers styling (default: True)
        """
        if use_guide_style:
            # matplotlib_for_papers exact approach
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
            ax.tick_params(axis='x', direction='out')
            ax.tick_params(axis='y', length=0)
            ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
            ax.set_axisbelow(True)
            for spine in ax.spines.values():
                if spine.get_visible():
                    spine.set_position(('outward', 5))
        else:
            # Original style
            ax.grid(axis='y', alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)
            ax.set_axisbelow(True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#DADCDC')
            ax.spines['bottom'].set_color('#DADCDC')
    
    @staticmethod
    def style_line_chart(ax, config: PublicationStandards = PUBLICATION_CONFIG,
                        use_guide_style: bool = True):
        """
        Apply consistent styling to line charts.
        
        Args:
            ax: Matplotlib axes
            config: Configuration object
            use_guide_style: Use exact matplotlib_for_papers styling (default: True)
        """
        if use_guide_style:
            # matplotlib_for_papers exact approach
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
            ax.tick_params(axis='x', direction='out')
            ax.tick_params(axis='y', length=0)
            ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
            ax.set_axisbelow(True)
            for spine in ax.spines.values():
                if spine.get_visible():
                    spine.set_position(('outward', 5))
        else:
            # Original style
            ax.grid(axis='both', alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)
            ax.set_axisbelow(True)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#DADCDC')
            ax.spines['bottom'].set_color('#DADCDC')
    
    @staticmethod
    def style_heatmap(ax, config: PublicationStandards = PUBLICATION_CONFIG):
        """Apply consistent styling to heatmaps."""
        ax.grid(False)
    
    @staticmethod
    def add_effect_size_reference_lines(ax, vertical: bool = True,
                                       config: PublicationStandards = PUBLICATION_CONFIG):
        """Add Cohen's d reference lines to effect size plots."""
        values = [0.2, 0.5, 0.8]
        if vertical:
            for val in values:
                ax.axvline(x=val, color=config.COLOR_GRAY, 
                          linestyle='--', alpha=0.4, linewidth=0.8)
                ax.axvline(x=-val, color=config.COLOR_GRAY, 
                          linestyle='--', alpha=0.4, linewidth=0.8)
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
        else:
            for val in values:
                ax.axhline(y=val, color=config.COLOR_GRAY, 
                          linestyle='--', alpha=0.4, linewidth=0.8)
                ax.axhline(y=-val, color=config.COLOR_GRAY, 
                          linestyle='--', alpha=0.4, linewidth=0.8)
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    @staticmethod
    def format_metric_label(label: str) -> str:
        """Format long metric names for better display."""
        replacements = {
            'EMOTIONAL TONE APPROPRIATE': 'Emotional\nTone',
            'RELEVANCE & COHERENCE': 'Relevance &\nCoherence',
            'PERSONALITY NEEDS ADDRESSED': 'Personality\nNeeds',
            'DETECTION ACCURATE': 'Detection\nAccuracy',
            'REGULATION EFFECTIVE': 'Regulation\nEffective'
        }
        return replacements.get(label, label.replace(' ', '\n'))
    
    @staticmethod
    def style_legend_guide(legend, style: str = 'gray'):
        """
        Style legend following matplotlib_for_papers guide.
        
        Args:
            legend: Legend object from ax.legend()
            style: 'gray' (gray background), 'white' (white background), 
                   'transparent' (no background)
        """
        frame = legend.get_frame()
        
        if style == 'gray':
            # Guide style: gray background
            frame.set_facecolor('0.9')
            frame.set_edgecolor('0.9')
        elif style == 'white':
            # Guide alternative: white/invisible
            frame.set_facecolor('1.0')
            frame.set_edgecolor('1.0')
        elif style == 'transparent':
            # Remove frame entirely
            frame.set_facecolor('none')
            frame.set_edgecolor('none')
            frame.set_alpha(0)
    
    @staticmethod
    def remove_chartjunk(ax, config: PublicationStandards = PUBLICATION_CONFIG):
        """
        Remove chartjunk following Tufte's principles.
        Removes top and right spines, lightens remaining spines.
        """
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#DADCDC')
        ax.spines['bottom'].set_color('#DADCDC')
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['bottom'].set_linewidth(0.8)
        ax.tick_params(axis='both', which='both', length=0)
    
    @staticmethod
    def add_median_labels(ax, bp, positions, format_str='{:.2f}',
                         offset=0.1, fontsize=9):
        """
        Add median value labels to boxplot.
        
        Args:
            ax: Matplotlib axes
            bp: Boxplot object returned from ax.boxplot()
            positions: X positions of boxes
            format_str: Format string for labels (default: '{:.2f}')
            offset: Vertical offset from median line
            fontsize: Font size for labels
        """
        for pos, median in zip(positions, bp['medians']):
            med_val = median.get_ydata()[0]
            ax.text(pos, med_val + offset, format_str.format(med_val),
                   ha='center', va='bottom', fontsize=fontsize,
                   fontweight='bold', color='0.2')
    
    @staticmethod
    def add_sample_size_labels(ax, positions, sample_sizes, y_position='bottom',
                              fontsize=8, offset=0.02):
        """
        Add sample size (n=X) labels to plots.
        
        Args:
            ax: Matplotlib axes
            positions: X positions for labels
            sample_sizes: List of sample sizes
            y_position: 'bottom' or 'top' (default: 'bottom')
            fontsize: Font size for labels
            offset: Offset from plot edge (as fraction of y-range)
        """
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        
        if y_position == 'bottom':
            y = y_min + (y_range * offset)
            va = 'bottom'
        else:
            y = y_max - (y_range * offset)
            va = 'top'
        
        for pos, n in zip(positions, sample_sizes):
            ax.text(pos, y, f'n={n}', ha='center', va=va,
                   fontsize=fontsize, style='italic', color='0.5')
    
    @staticmethod
    def create_color_palette(n_colors: int, palette_name: str = 'okabe_ito') -> list:
        """
        Create colorblind-friendly color palettes.
        
        Args:
            n_colors: Number of colors needed
            palette_name: 'okabe_ito' (default), 'wong', 'tol', or 'paul_tol'
        
        Returns:
            List of color hex codes
        """
        palettes = {
            'okabe_ito': [
                '#0072B2',  # Blue
                '#E69F00',  # Orange
                '#009E73',  # Green
                '#D55E00',  # Vermillion
                '#CC79A7',  # Purple
                '#56B4E9',  # Sky Blue
                '#F0E442',  # Yellow
                '#000000',  # Black
            ],
            'wong': [
                '#000000',  # Black
                '#E69F00',  # Orange
                '#56B4E9',  # Sky Blue
                '#009E73',  # Bluish Green
                '#F0E442',  # Yellow
                '#0072B2',  # Blue
                '#D55E00',  # Vermillion
                '#CC79A7',  # Purple
            ],
            'tol': [
                '#332288',  # Indigo
                '#88CCEE',  # Cyan
                '#44AA99',  # Teal
                '#117733',  # Green
                '#999933',  # Olive
                '#DDCC77',  # Sand
                '#CC6677',  # Rose
                '#882255',  # Wine
                '#AA4499',  # Purple
            ]
        }
        
        palette = palettes.get(palette_name, palettes['okabe_ito'])
        
        # Cycle through palette if more colors needed
        if n_colors > len(palette):
            return (palette * ((n_colors // len(palette)) + 1))[:n_colors]
        
        return palette[:n_colors]


# ============================================================================
# FIGURE CATALOG
# ============================================================================

class FigureCatalog:
    """Central catalog of all figures with metadata."""
    
    FIGURES = {
        '01_performance_comparison': {
            'title': 'Performance Comparison: Regulated vs Baseline',
            'type': 'bar_chart',
            'priority': 'high',
            'description': 'Core comparison across all metrics with confidence intervals'
        },
        '02_effect_sizes': {
            'title': "Effect Sizes (Cohen's d)",
            'type': 'horizontal_bar',
            'priority': 'high',
            'description': 'Effect size magnitudes with reference lines'
        },
        '03_personality_needs': {
            'title': 'Personality Needs Addressed: Dramatic Improvement',
            'type': 'bar_chart',
            'priority': 'high',
            'description': 'Focused visualization of primary outcome'
        },
        '04_sample_quality': {
            'title': 'Sample Distribution and Data Quality',
            'type': 'multi_panel',
            'priority': 'medium',
            'description': 'Sample characteristics and completeness'
        },
        '05_personality_profiles': {
            'title': 'OCEAN Personality Dimensions',
            'type': 'multi_panel',
            'priority': 'medium',
            'description': 'Distribution of personality traits'
        },
        '06_system_architecture': {
            'title': 'System Architecture Overview',
            'type': 'diagram',
            'priority': 'high',
            'description': 'Pipeline from input to response'
        },
        '07_study_workflow': {
            'title': 'Study Design and Workflow',
            'type': 'diagram',
            'priority': 'high',
            'description': 'Research methodology flowchart'
        }
    }
    
    @classmethod
    def get_figure_path(cls, figure_id: str, output_dir: str = "figures") -> str:
        """Get standardized figure path."""
        return f"{output_dir}/{figure_id}.png"
    
    @classmethod
    def get_figure_info(cls, figure_id: str) -> Dict:
        """Get figure metadata."""
        return cls.FIGURES.get(figure_id, {})


# ============================================================================
# SAVE UTILITIES
# ============================================================================

def save_figure(fig, filename: str, output_dir: str = "figures",
               config: PublicationStandards = PUBLICATION_CONFIG,
               verbose: bool = True):
    """
    Save figure with publication standards.
    
    Args:
        fig: Matplotlib figure object
        filename: Filename (with or without extension)
        output_dir: Output directory
        config: Publication configuration
        verbose: Print confirmation message
    """
    import os
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Add extension if not present
    if not filename.endswith(f'.{config.FORMAT}'):
        filename = f"{filename}.{config.FORMAT}"
    
    # Full path
    filepath = os.path.join(output_dir, filename)
    
    # Save with publication settings
    fig.savefig(
        filepath,
        dpi=config.DPI,
        bbox_inches=config.BBOX_INCHES,
        facecolor=config.FACECOLOR,
        format=config.FORMAT
    )
    
    if verbose:
        filesize = os.path.getsize(filepath) / 1024  # KB
        print(f"  ? Saved: {filepath} ({filesize:.1f} KB)")
    
    plt.close(fig)


def save_figure_multi_format(fig, basename: str, output_dir: str = "figures",
                            formats: list = None,
                            config: PublicationStandards = PUBLICATION_CONFIG,
                            verbose: bool = True,
                            high_res: bool = False):
    """
    Save figure in multiple formats following FIGURE_STYLE_GUIDE.md standards.
    
    Per style guide:
    - Prefer PDF (vector) for plots/diagrams
    - PNG at ≥300 DPI for photos, ≥600 DPI for line art/text-heavy plots
    - Target pixel widths: 1-column ≥2000px, 2-column ≥4000px
    
    Args:
        fig: Matplotlib figure object
        basename: Base filename without extension
        output_dir: Output directory
        formats: List of formats (default: ['png', 'pdf'] per guide)
        config: Publication configuration
        verbose: Print confirmation message
        high_res: Use 600 DPI for line art/text-heavy plots
    """
    import os
    
    # Default to both PNG and PDF per FIGURE_STYLE_GUIDE.md
    if formats is None:
        formats = ['png', 'pdf']
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Select appropriate DPI based on content type
    dpi = config.DPI_LINE_ART if high_res else config.DPI
    
    saved_files = []
    for fmt in formats:
        filepath = os.path.join(output_dir, f"{basename}.{fmt}")
        
        # Use appropriate DPI for each format
        if fmt in ['pdf', 'svg', 'eps']:
            # Vector formats - use higher DPI for rasterized elements
            fig.savefig(filepath, format=fmt, dpi=dpi,
                       bbox_inches=config.BBOX_INCHES,
                       facecolor=config.FACECOLOR,
                       pad_inches=0.05)  # Minimal padding per guide
        else:
            # Raster formats - ensure proper resolution
            fig.savefig(filepath, format=fmt, dpi=dpi,
                       bbox_inches=config.BBOX_INCHES,
                       facecolor=config.FACECOLOR,
                       pad_inches=0.05)  # Tight cropping per guide
        
        saved_files.append(filepath)
    
    if verbose:
        # Report all saved files with actual dimensions
        filesize = os.path.getsize(saved_files[0]) / 1024
        formats_str = ', '.join(formats)
        dpi_str = f"{dpi} DPI" if 'png' in formats else "vector"
        print(f"  ✓ Saved: {basename}.{{{formats_str}}} ({filesize:.1f} KB, {dpi_str})")
    
    # Don't close the figure here - let caller decide


def get_figure_size_for_journal(journal: str = 'default',
                                columns: int = 1,
                                aspect: float = 0.7) -> tuple:
    """
    Get figure size in inches for common journal formats.
    Enhanced with FIGURE_STYLE_GUIDE.md pixel width requirements.
    
    Based on typical column widths for major journals:
    - Nature: single column = 89mm, double column = 183mm
    - Science: single column = 56mm, double column = 120mm
    - PLOS: single column = 83mm, double column = 174mm
    - Elsevier: single column = 90mm, double column = 190mm
    - IEEE: single column = 88mm, double column = 181mm
    - MDPI: single column = 85mm, double column = 170mm (per FIGURE_STYLE_GUIDE.md)
    
    Per FIGURE_STYLE_GUIDE.md:
    - 1-column (~85mm): aim for ≥2000 px width (@ 600 DPI)
    - 2-column (~170mm): aim for ≥4000 px width (@ 600 DPI)
    
    Args:
        journal: Journal name or 'default'
        columns: 1 for single column, 2 for double column
        aspect: Height/width ratio (default: 0.7)
    
    Returns:
        Tuple of (width, height) in inches
    """
    # Convert mm to inches (1 inch = 25.4mm)
    MM_TO_INCH = 1 / 25.4
    
    # Column widths in mm (updated MDPI per FIGURE_STYLE_GUIDE.md)
    widths = {
        'nature': {1: 89, 2: 183},
        'science': {1: 56, 2: 120},
        'plos': {1: 83, 2: 174},
        'elsevier': {1: 90, 2: 190},
        'ieee': {1: 88, 2: 181},
        'mdpi': {1: 85, 2: 170},  # Updated per FIGURE_STYLE_GUIDE.md
        'default': {1: 85, 2: 170},  # MDPI defaults
    }
    
    journal = journal.lower()
    if journal not in widths:
        journal = 'default'
    
    width_mm = widths[journal].get(columns, widths[journal][1])
    width_inch = width_mm * MM_TO_INCH
    height_inch = width_inch * aspect
    
    return (width_inch, height_inch)


def verify_figure_resolution(fig, target_width_px: int = 2000, dpi: int = 300) -> dict:
    """
    Verify that figure meets FIGURE_STYLE_GUIDE.md resolution requirements.
    
    Per guide:
    - 1-column: ≥2000 px width
    - 2-column: ≥4000 px width
    - Minimum 300 DPI (600 DPI for line art)
    
    Args:
        fig: Matplotlib figure object
        target_width_px: Target width in pixels (2000 for 1-col, 4000 for 2-col)
        dpi: DPI setting used for export
        
    Returns:
        Dict with verification results
    """
    width_inch, height_inch = fig.get_size_inches()
    actual_width_px = int(width_inch * dpi)
    actual_height_px = int(height_inch * dpi)
    
    meets_requirement = actual_width_px >= target_width_px
    
    return {
        'width_inches': width_inch,
        'height_inches': height_inch,
        'width_px': actual_width_px,
        'height_px': actual_height_px,
        'dpi': dpi,
        'target_width_px': target_width_px,
        'meets_requirement': meets_requirement,
        'shortfall_px': max(0, target_width_px - actual_width_px)
    }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    """Demonstrate configuration usage."""
    
    print("="*70)
    print("PUBLICATION-STANDARD VISUALIZATION CONFIGURATION")
    print("="*70)
    
    # Configure matplotlib
    configure_matplotlib()
    
    print("\n? Matplotlib configured with publication standards")
    print(f"  - DPI: {PUBLICATION_CONFIG.DPI}")
    print(f"  - Format: {PUBLICATION_CONFIG.FORMAT}")
    print(f"  - Style: {PUBLICATION_CONFIG.STYLE}")
    print(f"  - Font: {PUBLICATION_CONFIG.FONT_FAMILY}")
    
    print("\n? Color Palette (Colorblind-friendly):")
    print(f"  - Regulated: {PUBLICATION_CONFIG.COLOR_REGULATED}")
    print(f"  - Baseline: {PUBLICATION_CONFIG.COLOR_BASELINE}")
    print(f"  - Positive: {PUBLICATION_CONFIG.COLOR_POSITIVE}")
    print(f"  - Negative: {PUBLICATION_CONFIG.COLOR_NEGATIVE}")
    
    print("\n? Available Figure Templates:")
    print("  - Single panel")
    print("  - Double panel (1x2)")
    print("  - Quad panel (2x2)")
    print("  - Wide panel")
    
    print("\n? Figure Catalog:")
    for fig_id, info in FigureCatalog.FIGURES.items():
        print(f"  - {fig_id}: {info['title']}")
    
    print("\n" + "="*70)
    print("READY FOR VISUALIZATION")
    print("="*70)
