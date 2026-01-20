"""
Bipartite Graph Construction
=============================

Functions for creating and analyzing user-post bipartite graphs.
"""

import networkx as nx
import numpy as np
from typing import List, Tuple
from networkx.algorithms import bipartite

from ..utils.config import NUM_POSTS, VIRAL_POST_RATIO


def create_bipartite_graph(
    G: nx.DiGraph,
    key_figures: List[str],
    n_posts: int = NUM_POSTS
) -> Tuple[nx.Graph, List[str]]:
    """
    Create a bipartite graph of users and posts.

    Simulates realistic posting patterns where:
    - Key figures create influential posts
    - Popular posts attract more comments (preferential attachment)
    - Users cluster around similar content

    Parameters
    ----------
    G : nx.DiGraph
        Main network graph
    key_figures : list
        List of influential users
    n_posts : int
        Number of posts to create

    Returns
    -------
    B : nx.Graph
        Bipartite graph
    posts : list
        List of post IDs
    """
    B = nx.Graph()  # Bipartite graphs are undirected

    # Create viral posts from key figures
    viral_posts = []
    for i, user in enumerate(key_figures[:5]):
        post_id = f"POST_{user}_{i}"
        viral_posts.append(post_id)
        B.add_node(post_id, bipartite=1, type='viral_post', author=user)

    # Create regular posts
    posts = viral_posts.copy()
    for i in range(n_posts - len(viral_posts)):
        post_id = f"POST_{i:04d}"
        posts.append(post_id)
        B.add_node(post_id, bipartite=1, type='regular_post')

    # Add users
    for user in G.nodes():
        B.add_node(user, bipartite=0, type='user')

    # Create edges (user commented on post)
    for user in G.nodes():
        if user in key_figures:
            n_comments = np.random.randint(20, 50)
        else:
            n_comments = np.random.randint(1, 15)

        # 70% on viral posts, 30% on regular posts
        n_viral = int(n_comments * VIRAL_POST_RATIO)
        n_regular = n_comments - n_viral

        # Comment on viral posts
        viral_targets = np.random.choice(
            viral_posts,
            size=min(n_viral, len(viral_posts)),
            replace=True
        )
        for post in viral_targets:
            if not B.has_edge(user, post):
                B.add_edge(user, post)

        # Comment on regular posts
        regular_posts = [p for p in posts if p not in viral_posts]
        if len(regular_posts) > 0:
            regular_targets = np.random.choice(
                regular_posts,
                size=min(n_regular, len(regular_posts)),
                replace=False
            )
            for post in regular_targets:
                if not B.has_edge(user, post):
                    B.add_edge(user, post)

    return B, posts


def project_to_users(B: nx.Graph, k_threshold: int = 1) -> Tuple[nx.Graph, np.ndarray, dict]:
    """
    Project bipartite graph onto users using matrix multiplication.

    Creates USERS x POSTS incidence matrix, multiplies by its transpose to get
    USERS x USERS matrix where each cell represents shared posts count.
    Then filters by k-threshold.

    Parameters
    ----------
    B : nx.Graph
        Bipartite graph
    k_threshold : int
        Minimum number of shared posts to create an edge (default: 1)

    Returns
    -------
    user_projection : nx.Graph
        Projected user network (filtered by k)
    shared_matrix : np.ndarray
        Full USERS x USERS shared posts matrix
    matrix_info : dict
        Information about the matrices
    """
    print(f"\n  >>> Creating USER x POST incidence matrix...")

    # Get sorted lists of users and posts
    user_nodes = sorted([n for n, d in B.nodes(data=True) if d['bipartite'] == 0])
    post_nodes = sorted([n for n, d in B.nodes(data=True) if d['bipartite'] == 1])

    n_users = len(user_nodes)
    n_posts = len(post_nodes)

    # Create user and post index mappings
    user_to_idx = {user: i for i, user in enumerate(user_nodes)}
    post_to_idx = {post: i for i, post in enumerate(post_nodes)}

    # Create USERS x POSTS incidence matrix (1 if user commented on post, 0 otherwise)
    incidence_matrix = np.zeros((n_users, n_posts), dtype=np.int8)

    for user, post in B.edges():
        if B.nodes[user]['bipartite'] == 0:  # user is bipartite 0
            u_idx = user_to_idx[user]
            p_idx = post_to_idx[post]
        else:  # post is bipartite 0, user is bipartite 1
            u_idx = user_to_idx[post]
            p_idx = post_to_idx[user]
        incidence_matrix[u_idx, p_idx] = 1

    print(f"  - Incidence matrix: {n_users} users x {n_posts} posts")
    print(f"  - Total comments: {np.sum(incidence_matrix):,}")

    # Matrix multiplication: (USERS x POSTS) @ (POSTS x USERS) = USERS x USERS
    print(f"\n  >>> Computing shared posts matrix (M x M^T)...")
    shared_matrix = incidence_matrix @ incidence_matrix.T

    # Diagonal represents self-connections (how many posts each user commented on)
    user_post_counts = np.diag(shared_matrix)
    print(f"  - Shared posts matrix: {n_users} x {n_users}")
    print(f"  - Average posts per user: {np.mean(user_post_counts):.1f}")
    print(f"  - Max shared posts between two users: {np.max(shared_matrix[np.triu_indices_from(shared_matrix, k=1)])}")

    # Filter by k-threshold
    print(f"\n  >>> Filtering edges by k-threshold = {k_threshold}...")

    # Create adjacency matrix (k-filtered, excluding diagonal)
    adjacency = np.zeros_like(shared_matrix)
    adjacency[shared_matrix >= k_threshold] = shared_matrix[shared_matrix >= k_threshold]
    np.fill_diagonal(adjacency, 0)  # Remove self-loops

    # Make symmetric (upper triangle only to avoid double counting)
    adjacency = np.triu(adjacency, k=1)

    # Count edges
    total_possible_edges = (n_users * (n_users - 1)) // 2
    edges_created = np.count_nonzero(adjacency)

    print(f"  - Edges created (k >= {k_threshold}): {edges_created:,} / {total_possible_edges:,} ({edges_created/total_possible_edges*100:.1f}%)")

    # Build NetworkX graph from filtered matrix
    user_projection = nx.Graph()
    user_projection.add_nodes_from(user_nodes)

    # Add edges from adjacency matrix
    edge_count = 0
    for i in range(n_users):
        for j in range(i+1, n_users):
            weight = adjacency[i, j]
            if weight > 0:
                user_projection.add_edge(user_nodes[i], user_nodes[j], weight=int(weight))
                edge_count += 1

    print(f"  - NetworkX graph created: {edge_count:,} edges")

    matrix_info = {
        'n_users': n_users,
        'n_posts': n_posts,
        'k_threshold': k_threshold,
        'total_comments': int(np.sum(incidence_matrix)),
        'edges_created': edges_created,
        'total_possible_edges': total_possible_edges,
        'density': edges_created / total_possible_edges,
        'avg_posts_per_user': float(np.mean(user_post_counts)),
        'max_shared_posts': int(np.max(shared_matrix[np.triu_indices_from(shared_matrix, k=1)]))
    }

    return user_projection, shared_matrix, matrix_info


def analyze_echo_chamber(user_projection: nx.Graph) -> Tuple[dict, list, set]:
    """
    Analyze echo chamber effects from projection.

    Parameters
    ----------
    user_projection : nx.Graph
        Projected user network

    Returns
    -------
    analysis : dict
        Echo chamber analysis results
    components : list
        List of connected components
    largest_component : set
        Largest connected component
    """
    print(f"\n  >>> Analyzing echo chamber structure...")

    # Connected components
    components = list(nx.connected_components(user_projection))
    largest_component = max(components, key=len) if components else set()
    component_sizes = [len(c) for c in components]

    # Edge weights
    edge_weights = [d['weight'] for u, v, d in user_projection.edges(data=True)] if user_projection.number_of_edges() > 0 else [0]

    # Clustering coefficient (if graph is not too large)
    clustering = None
    if len(largest_component) > 2:
        largest_subgraph = user_projection.subgraph(largest_component)
        if len(largest_component) <= 1000:
            print(f"  - Computing clustering coefficient...")
            clustering = nx.average_clustering(largest_subgraph, weight='weight')
            print(f"  - Average clustering: {clustering:.4f}")
        else:
            print(f"  - Component too large for full clustering ({len(largest_component)} nodes)")
            # Sample-based clustering for large graphs
            sample_size = min(500, len(largest_component))
            sample_nodes = np.random.choice(list(largest_component), sample_size, replace=False)
            sample_subgraph = largest_subgraph.subgraph(sample_nodes)
            clustering = nx.average_clustering(sample_subgraph, weight='weight')
            print(f"  - Estimated clustering (sample of {sample_size}): {clustering:.4f}")

    # Network density
    if user_projection.number_of_nodes() > 1:
        density = nx.density(user_projection)
        print(f"  - Network density: {density:.6f}")
    else:
        density = 0.0

    analysis = {
        'n_nodes': user_projection.number_of_nodes(),
        'n_edges': user_projection.number_of_edges(),
        'n_components': len(components),
        'largest_component_size': len(largest_component),
        'largest_component_pct': len(largest_component) / user_projection.number_of_nodes() * 100 if user_projection.number_of_nodes() > 0 else 0,
        'avg_component_size': np.mean(component_sizes) if component_sizes else 0,
        'median_component_size': np.median(component_sizes) if component_sizes else 0,
        'mean_shared_posts': np.mean(edge_weights) if edge_weights else 0,
        'max_shared_posts': np.max(edge_weights) if edge_weights else 0,
        'clustering': clustering,
        'density': density
    }

    print(f"  - Components: {len(components)}, Largest: {len(largest_component)} ({analysis['largest_component_pct']:.1f}%)")

    return analysis, components, largest_component
