#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDPI-Ready Mapping of Big Five Traits to Zurich Model Domains.
Uses unified DiagramStyle from visualization_config.
"""

import sys
from pathlib import Path
import matplotlib.patches as mpatches

_STAT_DIR = str(Path(__file__).resolve().parent.parent.parent / "statistical analyis")
if _STAT_DIR not in sys.path:
    sys.path.insert(0, _STAT_DIR)

from visualization_config import (
    DIAGRAM_STYLE as DS,
    diagram_setup_figure,
    diagram_draw_box,
    diagram_draw_arrow,
    diagram_draw_title,
    diagram_title_y,
    diagram_content_top_y,
)

OUT = Path(__file__).resolve().parent

FIG_W, FIG_H = 12, 7.5


def create_trait_mapping():
    fig, ax = diagram_setup_figure(figsize=(FIG_W, FIG_H))

    title_y = diagram_title_y(FIG_H)
    content_y = diagram_content_top_y(FIG_H)
    diagram_draw_title(ax, FIG_W / 2, title_y,
        'Mapping Big Five Traits to Zurich Model Domains and Behavioral Effects')

    c_trait  = DS.COLOR_TRAIT
    c_domain = DS.COLOR_DOMAIN
    c_effect = DS.COLOR_EFFECT

    dot = "\u00b7"

    col1_x, col2_x, col3_x = 0.8, 4.2, 8.2
    box_w_traits, box_w_domains, box_w_effects = 2.4, 3.2, 3.4
    box_h = 0.85

    label_y = content_y - 0.2
    row_gap = 1.4
    y_security    = label_y - 1.1
    y_affiliation = y_security - row_gap
    y_structure   = y_affiliation - row_gap
    y_arousal     = y_structure - row_gap

    y_n = y_security
    y_a = y_affiliation
    y_c = y_structure
    y_e = y_arousal + 0.40
    y_o = y_arousal - 0.60

    ax.text(col1_x + box_w_traits / 2, label_y, "Big Five Traits (Inputs)",
            ha='center', fontweight='bold', fontsize=DS.SECTION_HEADER_FONTSIZE)
    ax.text(col2_x + box_w_domains / 2, label_y, "Zurich Model Domains (Needs)",
            ha='center', fontweight='bold', fontsize=DS.SECTION_HEADER_FONTSIZE)
    ax.text(col3_x + box_w_effects / 2, label_y, "Behavioral Effects (Outputs)",
            ha='center', fontweight='bold', fontsize=DS.SECTION_HEADER_FONTSIZE)

    # TRAITS
    for y, txt in [(y_n, "Neuroticism (N)\nEmotional stability"),
                    (y_a, "Agreeableness (A)"),
                    (y_c, "Conscientiousness (C)"),
                    (y_e, "Extraversion (E)"),
                    (y_o, "Openness (O)")]:
        diagram_draw_box(ax, col1_x, y, box_w_traits, box_h, txt,
                         facecolor=c_trait[0], edgecolor=c_trait[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)

    # DOMAINS
    for y, txt in [(y_security,    f"Security\nreassurance {dot} comfort"),
                    (y_affiliation, f"Affiliation\nwarmth {dot} proximity"),
                    (y_structure,   f"Structure\nguidance {dot} pacing"),
                    (y_arousal,     f"Arousal\nnovelty {dot} stimulation")]:
        diagram_draw_box(ax, col2_x, y, box_w_domains, box_h, txt,
                         facecolor=c_domain[0], edgecolor=c_domain[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)

    # EFFECTS
    for y, txt in [(y_security,    f"Reassurance & Comfort\nreduce threat {dot} support"),
                    (y_affiliation, f"Warmth & Collaboration\nempathic {dot} neutral stance"),
                    (y_structure,   f"Structure & Pacing\norganized {dot} flexible"),
                    (y_arousal,     f"Novelty & Stimulation\nexploration {dot} familiarity")]:
        diagram_draw_box(ax, col3_x, y, box_w_effects, box_h, txt,
                         facecolor=c_effect[0], edgecolor=c_effect[1],
                         wrap_width=DS.BOX_WRAP_WIDTH)

    arrow_pad = 0.08

    # Traits -> Domains
    for src_y, dst_y in [(y_n, y_security), (y_a, y_affiliation),
                          (y_c, y_structure), (y_e, y_arousal), (y_o, y_arousal)]:
        diagram_draw_arrow(ax, col1_x + box_w_traits + arrow_pad, src_y + box_h / 2,
                           col2_x - arrow_pad, dst_y + box_h / 2)

    # Domains -> Effects
    for y in [y_security, y_affiliation, y_structure, y_arousal]:
        diagram_draw_arrow(ax, col2_x + box_w_domains + arrow_pad, y + box_h / 2,
                           col3_x - arrow_pad, y + box_h / 2)

    # Background columns
    panel_bottom = y_o - 0.15
    panel_h = label_y + 0.35 - panel_bottom
    for x_pos, w_pos in [(col1_x - 0.3, box_w_traits + 0.6),
                          (col2_x - 0.3, box_w_domains + 0.6),
                          (col3_x - 0.3, box_w_effects + 0.6)]:
        rect = mpatches.FancyBboxPatch(
            (x_pos, panel_bottom), w_pos, panel_h, boxstyle="round,pad=0.1",
            facecolor=DS.BG_PANEL_FACECOLOR, edgecolor=DS.BG_PANEL_EDGECOLOR,
            linewidth=DS.BG_PANEL_LINEWIDTH, alpha=DS.BG_PANEL_ALPHA, zorder=-1)
        ax.add_patch(rect)

    ax.set_ylim(panel_bottom - 0.1, FIG_H)
    DS.save(fig, "trait_mapping_mdpi", str(OUT))


if __name__ == "__main__":
    create_trait_mapping()
