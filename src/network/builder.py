"""
Network Builder
===============

Functions for constructing the GameStop social network.
"""

import networkx as nx
import numpy as np
from typing import List, Tuple

from ..utils.config import *
from ..utils.helpers import set_random_seed


def create_scale_free_network(
    n_users: int = NETWORK_SIZE,
    key_figures: List[str] = KEY_FIGURES,
    seed: int = RANDOM_SEED
) -> Tuple[nx.DiGraph, List[str]]:
    """
    Create a scale-free network following Barabási-Albert model.

    This represents the realistic power-law distribution seen in social networks.

    Parameters
    ----------
    n_users : int
        Total number of Reddit users
    key_figures : list
        List of known influential users
    seed : int
        Random seed for reproducibility

    Returns
    -------
    G : nx.DiGraph
        Directed weighted graph
    key_figures : list
        List of key influencer usernames
    """
    set_random_seed(seed)

    # Create directed graph
    G = nx.DiGraph()

    # Add key figures
    for user in key_figures:
        G.add_node(user, type='influencer', degree_rank='top')

    # Create scale-free network using Barabási-Albert model
    ba_graph = nx.barabasi_albert_graph(n_users - len(key_figures), BA_MODEL_M, seed=seed)

    # Add remaining users
    remaining_users = [f'user_{i:04d}' for i in range(n_users - len(key_figures))]

    for user in remaining_users:
        G.add_node(user, type='regular')

    # Add edges from BA graph with direction and weights
    for u, v in ba_graph.edges():
        user_u = remaining_users[u]
        user_v = remaining_users[v]

        # Add bidirectional edges with random weights
        weight_uv = np.random.randint(MIN_WEIGHT, MAX_WEIGHT_REGULAR)
        weight_vu = np.random.randint(MIN_WEIGHT, MAX_WEIGHT_REGULAR - 5)

        G.add_edge(user_u, user_v, weight=weight_uv)
        if np.random.random() > (1 - REPLY_PROBABILITY):
            G.add_edge(user_v, user_u, weight=weight_vu)

    # Connect key figures to the network
    _connect_influencers(G, key_figures, remaining_users)

    # Add inter-influencer connections
    _connect_influencers_to_each_other(G, key_figures)

    return G, key_figures


def _connect_influencers(
    G: nx.DiGraph,
    key_figures: List[str],
    remaining_users: List[str]
) -> None:
    """Connect influencers to the network with preferential attachment."""
    node_degrees = dict(G.degree())
    high_degree_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:100]

    for influencer in key_figures:
        # Determine number of connections
        if influencer == 'DeepFuckingValue':
            n_connections = DFV_CONNECTIONS
        else:
            n_connections = np.random.randint(
                INFLUENCER_MIN_CONNECTIONS,
                INFLUENCER_MAX_CONNECTIONS
            )

        # Preferential attachment: 70% to high-degree nodes, 30% random
        n_preferential = int(n_connections * PREFERENTIAL_RATIO)
        n_random = n_connections - n_preferential

        available_high_degree = [node for node, deg in high_degree_nodes if node in remaining_users]
        high_degree_targets = np.random.choice(
            available_high_degree,
            size=min(n_preferential, len(available_high_degree)),
            replace=False
        ) if len(available_high_degree) > 0 else []

        available_random = [u for u in remaining_users if u not in high_degree_targets]
        random_targets = np.random.choice(
            available_random,
            size=min(n_random, len(available_random)),
            replace=False
        ) if len(available_random) > 0 else []

        targets = list(high_degree_targets) + list(random_targets)

        for target in targets:
            # Heavy incoming edges (people replying to influencer)
            weight_in = np.random.randint(MIN_WEIGHT, MAX_WEIGHT_TO_INFLUENCER)
            G.add_edge(target, influencer, weight=weight_in)

            # Some outgoing edges (influencer replying back)
            if np.random.random() > 0.7:  # 30% reply rate
                weight_out = np.random.randint(
                    MIN_WEIGHT_FROM_INFLUENCER,
                    MAX_WEIGHT_FROM_INFLUENCER
                )
                G.add_edge(influencer, target, weight=weight_out)


def _connect_influencers_to_each_other(
    G: nx.DiGraph,
    key_figures: List[str]
) -> None:
    """Add connections between influencers."""
    for i, inf1 in enumerate(key_figures):
        for inf2 in key_figures[i+1:]:
            if np.random.random() > 0.3:  # 70% chance of connection
                w1 = np.random.randint(3, 25)
                w2 = np.random.randint(3, 25)
                G.add_edge(inf1, inf2, weight=w1)
                G.add_edge(inf2, inf1, weight=w2)


def get_network_stats(G: nx.DiGraph) -> dict:
    """
    Get basic network statistics.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    stats : dict
        Dictionary of network statistics
    """
    stats = {
        'n_nodes': G.number_of_nodes(),
        'n_edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_strongly_connected': nx.is_strongly_connected(G),
        'is_weakly_connected': nx.is_weakly_connected(G)
    }

    # Connected components
    if not nx.is_strongly_connected(G):
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        stats['largest_scc_size'] = len(largest_scc)
        stats['largest_scc_pct'] = len(largest_scc) / G.number_of_nodes() * 100

    largest_wcc = max(nx.weakly_connected_components(G), key=len)
    stats['largest_wcc_size'] = len(largest_wcc)
    stats['largest_wcc_pct'] = len(largest_wcc) / G.number_of_nodes() * 100

    return stats
