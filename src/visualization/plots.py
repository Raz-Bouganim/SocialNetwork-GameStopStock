"""
Visualization Functions
=======================

Functions for creating publication-quality visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple

from ..utils.config import (
    FIGURE_SIZE, DPI, SAMPLE_SIZE_NETWORK,
    NODE_SIZE_INFLUENCER, NODE_SIZE_REGULAR,
    COLOR_INFLUENCER, COLOR_REGULAR
)
from ..utils.helpers import truncate_name


def setup_plot_style():
    """Set up matplotlib/seaborn style."""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")


def create_full_visualization(
    G: nx.DiGraph,
    centralities: Dict,
    cooperation_history: List[float],
    network_stats: Dict,
    value_comparison: Tuple,
    bipartite_stats: Dict,
    key_figures: List[str],
    component_sizes: List[int]
) -> plt.Figure:
    """
    Create comprehensive 12-panel visualization.

    Parameters
    ----------
    G : nx.DiGraph
        Main network graph
    centralities : dict
        Dictionary of centrality metrics
    cooperation_history : list
        TFT cooperation rates over time
    network_stats : dict
        Network structure statistics
    value_comparison : tuple
        (sarnoff, metcalfe, reed) values
    bipartite_stats : dict
        Bipartite graph statistics
    key_figures : list
        List of influential users
    component_sizes : list
        Sizes of connected components

    Returns
    -------
    fig : plt.Figure
        Matplotlib figure object
    """
    setup_plot_style()
    fig = plt.figure(figsize=FIGURE_SIZE)

    # 1. Network Sample
    ax1 = plt.subplot(4, 3, 1)
    _plot_network_sample(ax1, G, key_figures)

    # 2. Degree Distribution
    ax2 = plt.subplot(4, 3, 2)
    _plot_degree_distribution(ax2, G)

    # 3. Log-Log Degree Distribution
    ax3 = plt.subplot(4, 3, 3)
    _plot_degree_loglog(ax3, G)

    # 4. Top Influencers (In-Degree)
    ax4 = plt.subplot(4, 3, 4)
    _plot_top_influencers(ax4, centralities['in_degree_weighted'], key_figures)

    # 5. Top Bridges (Betweenness)
    ax5 = plt.subplot(4, 3, 5)
    _plot_top_betweenness(ax5, centralities['betweenness'], key_figures)

    # 6. Centrality Comparison
    ax6 = plt.subplot(4, 3, 6)
    _plot_centrality_comparison(ax6, centralities, key_figures)

    # 7. TFT Evolution
    ax7 = plt.subplot(4, 3, 7)
    _plot_tft_evolution(ax7, cooperation_history)

    # 8. Network Value Comparison
    ax8 = plt.subplot(4, 3, 8)
    _plot_value_comparison(ax8, value_comparison, G.number_of_nodes())

    # 9. Freeman Centralization
    ax9 = plt.subplot(4, 3, 9)
    _plot_freeman_centralization(ax9, network_stats['freeman_centralization'])

    # 10. Network Density
    ax10 = plt.subplot(4, 3, 10)
    _plot_network_density(ax10, network_stats['density'])

    # 11. Bipartite Graph Sample
    ax11 = plt.subplot(4, 3, 11)
    _plot_bipartite_info(ax11, bipartite_stats)

    # 12. Echo Chamber Components
    ax12 = plt.subplot(4, 3, 12)
    _plot_component_sizes(ax12, component_sizes)

    plt.tight_layout()
    return fig


def _plot_network_sample(ax, G: nx.DiGraph, key_figures: List[str]):
    """Plot network structure sample."""
    # Sample the network
    sample_nodes = list(key_figures) + list(np.random.choice(
        [n for n in G.nodes() if n not in key_figures],
        size=min(SAMPLE_SIZE_NETWORK, G.number_of_nodes() - len(key_figures)),
        replace=False
    ))
    G_sample = G.subgraph(sample_nodes)

    pos = nx.spring_layout(G_sample, k=0.5, iterations=50, seed=42)
    node_colors = [COLOR_INFLUENCER if n in key_figures else COLOR_REGULAR
                   for n in G_sample.nodes()]
    node_sizes = [NODE_SIZE_INFLUENCER if n in key_figures else NODE_SIZE_REGULAR
                  for n in G_sample.nodes()]

    nx.draw_networkx(G_sample, pos, ax=ax,
                    node_color=node_colors,
                    node_size=node_sizes,
                    with_labels=False,
                    edge_color='gray',
                    alpha=0.6,
                    arrows=True,
                    arrowsize=5,
                    width=0.5)

    ax.set_title('Network Structure Sample\n(Red = Key Influencers)',
                fontsize=12, fontweight='bold')
    ax.axis('off')


def _plot_degree_distribution(ax, G: nx.DiGraph):
    """Plot degree distribution histogram."""
    degrees = [d for n, d in G.degree()]
    ax.hist(degrees, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Degree (Number of Connections)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.set_title('Degree Distribution\n(Power Law - Few Hubs Dominate)',
                fontsize=12, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)


def _plot_degree_loglog(ax, G: nx.DiGraph):
    """Plot log-log degree distribution."""
    degrees = [d for n, d in G.degree()]
    degree_count = Counter(degrees)
    degrees_sorted = sorted(degree_count.keys())
    counts = [degree_count[d] for d in degrees_sorted]

    ax.loglog(degrees_sorted, counts, 'o', color='darkred', alpha=0.6)
    ax.set_xlabel('Degree (log scale)', fontsize=10)
    ax.set_ylabel('Frequency (log scale)', fontsize=10)
    ax.set_title('Power Law Confirmation\n(Log-Log Scale)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)


def _plot_top_influencers(ax, in_degree_weighted: Dict, key_figures: List[str]):
    """Plot top 20 influencers by in-degree."""
    top_20 = sorted(in_degree_weighted.items(), key=lambda x: x[1], reverse=True)[:20]
    users, weights = zip(*top_20)
    colors = [COLOR_INFLUENCER if u in key_figures else 'steelblue' for u in users]

    ax.barh(range(len(users)), weights, color=colors, alpha=0.7)
    ax.set_yticks(range(len(users)))
    ax.set_yticklabels([truncate_name(u) for u in users], fontsize=8)
    ax.set_xlabel('Weighted In-Degree', fontsize=10)
    ax.set_title('Top 20 Most Influential Users\n(Received Most Replies)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()


def _plot_top_betweenness(ax, betweenness: Dict, key_figures: List[str]):
    """Plot top 20 users by betweenness centrality."""
    top_20 = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:20]
    users, bc_values = zip(*top_20)
    colors = [COLOR_INFLUENCER if u in key_figures else 'orange' for u in users]

    ax.barh(range(len(users)), bc_values, color=colors, alpha=0.7)
    ax.set_yticks(range(len(users)))
    ax.set_yticklabels([truncate_name(u) for u in users], fontsize=8)
    ax.set_xlabel('Betweenness Centrality', fontsize=10)
    ax.set_title('Top 20 Information Bridges\n(Critical Connectors)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()


def _plot_centrality_comparison(ax, centralities: Dict, key_figures: List[str]):
    """Plot centrality comparison for key figures."""
    import pandas as pd

    centrality_data = []
    for user in key_figures:
        if (user in centralities['degree_centrality'] and
            user in centralities['betweenness'] and
            user in centralities['closeness']):
            centrality_data.append({
                'User': user,
                'Degree': centralities['degree_centrality'][user],
                'Betweenness': centralities['betweenness'][user],
                'Closeness': centralities['closeness'][user]
            })

    if centrality_data:
        df_cent = pd.DataFrame(centrality_data)
        x = np.arange(len(df_cent))
        width = 0.25

        ax.bar(x - width, df_cent['Degree'], width, label='Degree', alpha=0.8)
        ax.bar(x, df_cent['Betweenness'], width, label='Betweenness', alpha=0.8)
        ax.bar(x + width, df_cent['Closeness'], width, label='Closeness', alpha=0.8)

        ax.set_ylabel('Centrality Score', fontsize=10)
        ax.set_title('Centrality Comparison\n(Key Influencers)',
                    fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([truncate_name(u, 15) for u in df_cent['User']],
                          rotation=45, ha='right', fontsize=8)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')


def _plot_tft_evolution(ax, cooperation_history: List[float]):
    """Plot Tit-for-Tat evolution over time."""
    days = list(range(1, len(cooperation_history) + 1))
    cooperation_pct = [h * 100 for h in cooperation_history]

    ax.plot(days, cooperation_pct, marker='o', linewidth=2, markersize=8, color='green')
    ax.fill_between(days, cooperation_pct, alpha=0.3, color='green')
    ax.set_xlabel('Day (Time Step)', fontsize=10)
    ax.set_ylabel('% Holding (Cooperating)', fontsize=10)
    ax.set_title('Tit-for-Tat Evolution\n(HODL Behavior Over Time)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 100])

    # Add tipping point annotation if cooperation crosses 50%
    for i, pct in enumerate(cooperation_pct):
        if pct > 50 and (i == 0 or cooperation_pct[i-1] <= 50):
            ax.annotate('Tipping Point',
                       xy=(i+1, pct),
                       xytext=(i+1, pct + 15),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2),
                       fontsize=10, color='red', fontweight='bold')
            break


def _plot_value_comparison(ax, value_comparison: Tuple, n: int):
    """Plot network value laws comparison."""
    sarnoff, metcalfe, reed = value_comparison

    values_log = [np.log10(sarnoff), np.log10(metcalfe), np.log10(reed)]
    laws = ['Sarnoff\n(N)', 'Metcalfe\n(N²)', "Reed\n(2^N)"]
    colors_law = ['blue', 'orange', 'red']

    bars = ax.bar(laws, values_log, color=colors_law, alpha=0.7,
                  edgecolor='black', linewidth=2)
    ax.set_ylabel('Network Value (log₁₀ scale)', fontsize=10)
    ax.set_title('Network Value Laws Comparison\n(Exponential Power of Groups)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, val_log, val_real in zip(bars, values_log, [sarnoff, metcalfe, reed]):
        height = bar.get_height()
        label = f'10^{val_log:.1f}' if val_real > 1000 else f'{val_real:,.0f}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
               label, ha='center', va='bottom', fontsize=8, fontweight='bold')


def _plot_freeman_centralization(ax, centralization: float):
    """Plot Freeman centralization with benchmarks."""
    categories = ['GameStop\nNetwork', 'Decentralized\n(Random)', 'Centralized\n(Star)']
    values_freeman = [centralization, 0.1, 0.95]
    colors_freeman = ['orange', 'green', 'red']

    bars = ax.bar(categories, values_freeman, color=colors_freeman,
                  alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_ylabel('Freeman Centralization Score', fontsize=10)
    ax.set_title('Freeman Centralization\n(0=Decentralized, 1=Centralized)',
                fontsize=12, fontweight='bold')
    ax.set_ylim([0, 1])
    ax.axhline(y=0.5, color='gray', linestyle='--', label='Threshold', alpha=0.5)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()

    # Add interpretation
    if centralization > 0.6:
        interp = "Highly\nCentralized"
    elif centralization > 0.4:
        interp = "Moderately\nCentralized"
    else:
        interp = "Decentralized"

    ax.text(0, centralization + 0.05, f"{centralization:.3f}\n{interp}",
           ha='center', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def _plot_network_density(ax, density: float):
    """Plot network density."""
    density_pct = density * 100

    ax.barh(['Actual\nDensity'], [density_pct], color='steelblue',
           alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_xlim([0, max(0.5, density_pct * 1.5)])
    ax.set_xlabel('Density (%)', fontsize=10)
    ax.set_title(f'Network Density: {density:.6f}\n(Low Density = Loose Community)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')

    # Add interpretation
    if density < 0.01:
        density_interp = "Very Sparse"
    elif density < 0.05:
        density_interp = "Sparse"
    else:
        density_interp = "Moderate"

    ax.text(density_pct/2, 0, f'{density_interp}\n{density_pct:.4f}%',
           ha='center', va='center', fontsize=10, fontweight='bold', color='white')


def _plot_bipartite_info(ax, bipartite_stats: Dict):
    """Plot bipartite graph information."""
    ax.axis('off')

    info_text = f"""BIPARTITE GRAPH ANALYSIS

Users: {bipartite_stats['n_users']:,}
Posts: {bipartite_stats['n_posts']:,}
Comments: {bipartite_stats['n_comments']:,}

USER PROJECTION:
Giant Component: {bipartite_stats['giant_component_pct']:.1f}%
({bipartite_stats['giant_component_size']:,} users)

Avg Shared Posts: {bipartite_stats['mean_shared_posts']:.1f}
Max Shared Posts: {bipartite_stats['max_shared_posts']}

ECHO CHAMBER: {'CONFIRMED ✓' if bipartite_stats['giant_component_pct'] > 50 else 'NOT DETECTED'}
"""

    ax.text(0.5, 0.5, info_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='center', horizontalalignment='center',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
           family='monospace')

    ax.set_title('Echo Chamber Detection\n(Bipartite Projection)',
                fontsize=12, fontweight='bold')


def _plot_component_sizes(ax, component_sizes: List[int]):
    """Plot connected component size distribution."""
    component_sizes_sorted = sorted(component_sizes, reverse=True)[:20]

    ax.bar(range(len(component_sizes_sorted)), component_sizes_sorted,
          color='purple', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Component Rank', fontsize=10)
    ax.set_ylabel('Component Size (# Users)', fontsize=10)
    ax.set_title(f'Connected Components in User Projection\n' +
                f'(Giant Component: {component_sizes_sorted[0] if component_sizes_sorted else 0} users)',
                fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # Highlight giant component
    if len(component_sizes_sorted) > 0:
        ax.bar(0, component_sizes_sorted[0], color='red', alpha=0.7,
              edgecolor='black', linewidth=2)
        ax.text(0, component_sizes_sorted[0], 'GIANT\nCOMPONENT',
               ha='center', va='bottom', fontsize=8, fontweight='bold', color='red')
