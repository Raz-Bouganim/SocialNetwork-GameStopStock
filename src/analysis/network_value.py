"""
Network Value Analysis
======================

Functions for analyzing network value according to different laws.
"""

import numpy as np
import networkx as nx
from typing import Tuple


def calculate_sarnoff_value(n: int) -> float:
    """
    Calculate Sarnoff's Law value: V = N

    Parameters
    ----------
    n : int
        Number of users

    Returns
    -------
    value : float
        Network value
    """
    return float(n)


def calculate_metcalfe_value(n: int) -> float:
    """
    Calculate Metcalfe's Law value: V = N²

    Parameters
    ----------
    n : int
        Number of users

    Returns
    -------
    value : float
        Network value
    """
    return float(n ** 2)


def calculate_reed_value(n: int, max_group_size: int = 10) -> float:
    """
    Calculate Reed's Law value (approximation): V = 2^N

    For computational feasibility, we calculate the number of possible
    subgroups of size 2 to max_group_size.

    Parameters
    ----------
    n : int
        Number of users
    max_group_size : int
        Maximum group size to consider

    Returns
    -------
    value : float
        Network value (approximation)
    """
    max_group_size = min(max_group_size, n)
    value = sum(np.math.comb(n, k) for k in range(2, max_group_size + 1))
    return float(value)


def detect_communities(G: nx.Graph, weight: str = 'weight') -> dict:
    """
    Detect communities in the network using greedy modularity.

    Parameters
    ----------
    G : nx.Graph
        Network graph (undirected)
    weight : str
        Edge attribute to use as weight

    Returns
    -------
    community_info : dict
        Dictionary with community information
    """
    # Convert to undirected if needed
    if G.is_directed():
        G_undirected = G.to_undirected()
    else:
        G_undirected = G

    # Detect communities
    communities_generator = nx.community.greedy_modularity_communities(
        G_undirected,
        weight=weight
    )
    communities = list(communities_generator)

    # Analyze communities
    n_communities = len(communities)
    community_sizes = [len(c) for c in communities]

    return {
        'n_communities': n_communities,
        'communities': communities,
        'largest_community_size': max(community_sizes),
        'smallest_community_size': min(community_sizes),
        'avg_community_size': np.mean(community_sizes),
        'median_community_size': np.median(community_sizes)
    }


def compare_network_values(n: int) -> Tuple[float, float, float]:
    """
    Calculate and compare all three network value laws.

    Parameters
    ----------
    n : int
        Number of users

    Returns
    -------
    sarnoff : float
        Sarnoff's Law value
    metcalfe : float
        Metcalfe's Law value
    reed : float
        Reed's Law value
    """
    sarnoff = calculate_sarnoff_value(n)
    metcalfe = calculate_metcalfe_value(n)
    reed = calculate_reed_value(n)

    return sarnoff, metcalfe, reed
