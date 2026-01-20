"""
Centrality Analysis
===================

Functions for calculating and analyzing network centrality metrics.
"""

import networkx as nx
from typing import Dict, Tuple


def calculate_degree_centrality(G: nx.DiGraph) -> Tuple[Dict, Dict, Dict, Dict]:
    """
    Calculate degree centrality metrics.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    in_degree : dict
        In-degree for each node
    in_degree_weighted : dict
        Weighted in-degree for each node
    out_degree : dict
        Out-degree for each node
    out_degree_weighted : dict
        Weighted out-degree for each node
    """
    in_degree = dict(G.in_degree())
    in_degree_weighted = dict(G.in_degree(weight='weight'))
    out_degree = dict(G.out_degree())
    out_degree_weighted = dict(G.out_degree(weight='weight'))

    return in_degree, in_degree_weighted, out_degree, out_degree_weighted


def calculate_betweenness_centrality(G: nx.DiGraph, weight: str = 'weight') -> Dict:
    """
    Calculate betweenness centrality.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph
    weight : str
        Edge attribute to use as weight

    Returns
    -------
    betweenness : dict
        Betweenness centrality for each node
    """
    betweenness = nx.betweenness_centrality(G, weight=weight, normalized=True)
    return betweenness


def calculate_closeness_centrality(G: nx.DiGraph) -> Dict:
    """
    Calculate closeness centrality.

    For directed graphs that aren't strongly connected, calculates on
    the largest strongly connected component.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    closeness : dict
        Closeness centrality for each node
    """
    if nx.is_strongly_connected(G):
        closeness = nx.closeness_centrality(G, distance='weight')
    else:
        # Calculate on largest strongly connected component
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        G_scc = G.subgraph(largest_scc).copy()
        closeness = nx.closeness_centrality(G_scc, distance='weight')

    return closeness


def calculate_all_centralities(G: nx.DiGraph) -> Dict:
    """
    Calculate all centrality metrics at once.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph

    Returns
    -------
    centralities : dict
        Dictionary containing all centrality metrics
    """
    print(">>> Calculating Degree Centrality...")
    in_deg, in_deg_w, out_deg, out_deg_w = calculate_degree_centrality(G)

    print(">>> Calculating Betweenness Centrality...")
    print("(This may take a moment for large networks...)")
    betweenness = calculate_betweenness_centrality(G)

    print(">>> Calculating Closeness Centrality...")
    closeness = calculate_closeness_centrality(G)

    # Also calculate normalized degree centrality
    degree_centrality = nx.degree_centrality(G)

    return {
        'in_degree': in_deg,
        'in_degree_weighted': in_deg_w,
        'out_degree': out_deg,
        'out_degree_weighted': out_deg_w,
        'betweenness': betweenness,
        'closeness': closeness,
        'degree_centrality': degree_centrality
    }
