#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GameStop (2021) Short Squeeze - Social Network Analysis
========================================================

Main execution script for comprehensive network analysis.

Authors: Raz Bouganim, Omer Katz, Ohad Cohen
Date: December 2025
Course: Social Network Analysis
"""

import os
import sys
import warnings
import numpy as np
import matplotlib.pyplot as plt

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import io
    # Force UTF-8 encoding for Windows console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    # Try to enable Unicode console mode (Windows 10+)
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass  # Fallback to basic UTF-8

warnings.filterwarnings('ignore')

# Import all modules
from src.utils.config import *
from src.utils.helpers import print_header
from src.network import create_scale_free_network, get_network_stats
from src.network import create_bipartite_graph, project_to_users, analyze_echo_chamber
from src.analysis import calculate_all_centralities
from src.analysis import (
    calculate_network_density,
    calculate_freeman_centralization,
    interpret_centralization,
    interpret_density
)
from src.analysis import detect_communities, compare_network_values
from src.game_theory import simulate_tft_dynamics, analyze_tft_results
from src.visualization import create_full_visualization
from src.visualization import (
    print_network_stats,
    print_centrality_results,
    print_structure_results,
    print_tft_results,
    print_network_value_results,
    print_echo_chamber_results,
    print_final_summary
)


def main():
    """Main execution function."""
    print("=" * 80)
    print("GAMESTOP SHORT SQUEEZE - SOCIAL NETWORK ANALYSIS")
    print("r/WallStreetBets Network Analysis (2021)")
    print("=" * 80)

    # ========================================================================
    # MODULE 1: Network Construction
    # ========================================================================
    print_header("MODULE 1: NETWORK CONSTRUCTION")

    G, key_figures = create_scale_free_network(
        n_users=NETWORK_SIZE,
        key_figures=KEY_FIGURES,
        seed=RANDOM_SEED
    )

    stats = get_network_stats(G)
    print_network_stats(stats)

    # ========================================================================
    # MODULE 2: Centrality Analysis
    # ========================================================================
    centralities = calculate_all_centralities(G)
    print_centrality_results(centralities, key_figures)

    # ========================================================================
    # MODULE 3: Network Structure
    # ========================================================================
    density = calculate_network_density(G)
    centralization = calculate_freeman_centralization(G, 'in_degree')
    cent_interpretation = interpret_centralization(centralization)
    density_interpretation = interpret_density(density, G.number_of_nodes())

    print_structure_results(density, centralization, cent_interpretation)

    # ========================================================================
    # MODULE 4: Game Theory - Tit-for-Tat
    # ========================================================================
    cooperation_history, final_cooperators = simulate_tft_dynamics(
        G, key_figures, TFT_TIME_STEPS, INITIAL_COOPERATION_RATE
    )

    tft_analysis = analyze_tft_results(
        cooperation_history, final_cooperators, G.number_of_nodes()
    )

    print_tft_results(cooperation_history, tft_analysis)

    # ========================================================================
    # MODULE 5: Network Value Laws
    # ========================================================================
    sarnoff, metcalfe, reed = compare_network_values(G.number_of_nodes())
    community_info = detect_communities(G.to_undirected())

    print_network_value_results(sarnoff, metcalfe, reed, G.number_of_nodes(), community_info)

    # ========================================================================
    # MODULE 6: Bipartite Graph & Echo Chamber (Matrix Method)
    # ========================================================================
    print_header("MODULE 6: BIPARTITE GRAPH & ECHO CHAMBER ANALYSIS")

    B, posts = create_bipartite_graph(G, key_figures, NUM_POSTS)

    print(f"\n✓ Bipartite graph created:")
    print(f"  - Users: {sum(1 for n, d in B.nodes(data=True) if d['bipartite'] == 0)}")
    print(f"  - Posts: {sum(1 for n, d in B.nodes(data=True) if d['bipartite'] == 1)}")
    print(f"  - Comments (edges): {B.number_of_edges()}")

    # Matrix-based projection with k-filtering
    user_projection, shared_matrix, matrix_info = project_to_users(B, k_threshold=K_THRESHOLD)

    # Save shared matrix to output
    matrix_output = os.path.join(OUTPUT_DIR, 'shared_posts_matrix.npy')
    np.save(matrix_output, shared_matrix)
    print(f"\n✓ Shared posts matrix saved to: {matrix_output}")
    print(f"  - Matrix shape: {shared_matrix.shape}")
    print(f"  - Use np.load('{matrix_output}') to load it")

    # Analyze echo chamber
    echo_analysis, components, largest_component = analyze_echo_chamber(user_projection)

    # Add bipartite and matrix stats
    echo_analysis['n_users'] = matrix_info['n_users']
    echo_analysis['n_posts'] = matrix_info['n_posts']
    echo_analysis['n_comments'] = matrix_info['total_comments']
    echo_analysis['k_threshold'] = matrix_info['k_threshold']
    echo_analysis['matrix_density'] = matrix_info['density']

    component_sizes = [len(c) for c in components]

    print_echo_chamber_results(echo_analysis, len(components))

    # ========================================================================
    # VISUALIZATION
    # ========================================================================
    print_header("GENERATING VISUALIZATIONS")

    network_stats_for_viz = {
        'freeman_centralization': centralization,
        'density': density
    }

    bipartite_stats_for_viz = {
        'n_users': echo_analysis['n_users'],
        'n_posts': echo_analysis['n_posts'],
        'n_comments': echo_analysis['n_comments'],
        'giant_component_size': echo_analysis['largest_component_size'],
        'giant_component_pct': echo_analysis['largest_component_pct'],
        'mean_shared_posts': echo_analysis['mean_shared_posts'],
        'max_shared_posts': echo_analysis['max_shared_posts']
    }

    print("\n>>> Creating comprehensive visualization...")
    fig = create_full_visualization(
        G,
        centralities,
        cooperation_history,
        network_stats_for_viz,
        (sarnoff, metcalfe, reed),
        bipartite_stats_for_viz,
        key_figures,
        component_sizes
    )

    # Save visualization
    output_path = os.path.join(OUTPUT_DIR, VISUALIZATION_FILENAME)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(output_path, dpi=DPI, bbox_inches='tight')
    print(f"\n✓ Visualizations saved to: {output_path}")

    # Optional: Export network to GEXF for Gephi
    gexf_path = os.path.join(OUTPUT_DIR, NETWORK_EXPORT_FILENAME)
    import networkx as nx
    nx.write_gexf(G, gexf_path)
    print(f"✓ Network exported to: {gexf_path} (for Gephi)")

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_final_summary(
        density,
        centralization,
        cooperation_history,
        echo_analysis['largest_component_pct']
    )

    return {
        'G': G,
        'B': B,
        'user_projection': user_projection,
        'centralities': centralities,
        'cooperation_history': cooperation_history,
        'stats': stats,
        'community_info': community_info,
        'echo_analysis': echo_analysis
    }


if __name__ == "__main__":
    results = main()
    print("\n💡 TIP: Results are stored in the 'results' variable for further analysis.")
    print("    Example: results['G'] to access the network graph")
