"""
Network Structure Analysis
===========================

Functions for analyzing network structure metrics.
"""

import networkx as nx
import numpy as np
from typing import Tuple


def calculate_network_density(G: nx.DiGraph) -> float:
    """
    Calculate network density.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    density : float
        Network density
    """
    return nx.density(G)


def calculate_freeman_centralization(G: nx.DiGraph, centrality_type: str = 'in_degree') -> float:
    """
    Calculate Freeman Centralization score.

    Formula: Σ(C_max - C_i) / [(n-1)(n-2)]

    Parameters
    ----------
    G : nx.DiGraph
        Network graph
    centrality_type : str
        Type of centrality to use ('in_degree', 'out_degree', 'degree')

    Returns
    -------
    centralization : float
        Freeman centralization score (0 = decentralized, 1 = star network)
    """
    if centrality_type == 'in_degree':
        degrees = [deg for node, deg in G.in_degree()]
    elif centrality_type == 'out_degree':
        degrees = [deg for node, deg in G.out_degree()]
    else:
        degrees = [deg for node, deg in G.degree()]

    max_degree = max(degrees)
    sum_differences = sum(max_degree - deg for deg in degrees)

    n = G.number_of_nodes()
    max_possible_sum = (n - 1) * (n - 2)

    if max_possible_sum == 0:
        return 0.0

    centralization = sum_differences / max_possible_sum
    return centralization


def interpret_centralization(score: float) -> str:
    """
    Interpret Freeman centralization score.

    Parameters
    ----------
    score : float
        Centralization score

    Returns
    -------
    interpretation : str
        Human-readable interpretation
    """
    if score > 0.6:
        return "HIGHLY CENTRALIZED - Leader-driven movement"
    elif score > 0.4:
        return "MODERATELY CENTRALIZED - Hybrid structure"
    elif score > 0.2:
        return "SOMEWHAT CENTRALIZED - Mix of leaders and grassroots"
    else:
        return "DECENTRALIZED - Grassroots movement"


def interpret_density(density: float, n_nodes: int) -> str:
    """
    Interpret network density.

    Parameters
    ----------
    density : float
        Network density
    n_nodes : int
        Number of nodes

    Returns
    -------
    interpretation : str
        Human-readable interpretation
    """
    # Density typically decreases with network size
    expected_low = 1 / n_nodes

    if density > 0.1:
        return "DENSE - Tight-knit community"
    elif density > 0.01:
        return "MODERATE - Connected but not tight"
    elif density > expected_low * 2:
        return "SPARSE - Loose community structure"
    else:
        return "VERY SPARSE - Highly fragmented"


def analyze_power_law(G: nx.DiGraph) -> Tuple[list, dict]:
    """
    Analyze degree distribution for power law properties.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    degrees : list
        List of all degree values
    degree_count : dict
        Count of nodes for each degree
    """
    degrees = [d for n, d in G.degree()]
    degree_count = {}

    for d in degrees:
        degree_count[d] = degree_count.get(d, 0) + 1

    return degrees, degree_count
