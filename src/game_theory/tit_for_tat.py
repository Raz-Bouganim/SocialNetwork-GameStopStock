"""
Tit-for-Tat Simulation
======================

Functions for simulating game theory dynamics on the network.
"""

import networkx as nx
import numpy as np
from typing import List, Set, Tuple

from ..utils.config import (
    TFT_TIME_STEPS,
    INITIAL_COOPERATION_RATE,
    INFLUENCER_WEIGHT_MULTIPLIER,
    COOPERATION_THRESHOLD,
    STICKY_THRESHOLD
)


def simulate_tft_dynamics(
    G: nx.DiGraph,
    key_figures: List[str],
    n_steps: int = TFT_TIME_STEPS,
    initial_cooperators: float = INITIAL_COOPERATION_RATE
) -> Tuple[List[float], Set[str]]:
    """
    Simulate Tit-for-Tat (TFT) dynamics on the network.

    Strategy:
    - Initially, a fraction of users cooperate (Hold)
    - Each step, users observe their neighbors
    - If majority of neighbors cooperate, user cooperates next round
    - Otherwise, user defects

    Key influencers have higher weight in decision-making.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph
    key_figures : list
        List of influential users
    n_steps : int
        Number of time steps to simulate
    initial_cooperators : float
        Initial fraction of cooperators

    Returns
    -------
    cooperation_history : list
        Cooperation rate at each time step
    final_cooperators : set
        Set of cooperating users at final step
    """
    print("\n>>> Running Tit-for-Tat Simulation...")
    print("-" * 80)

    # Initialize: influencers + random early adopters
    cooperators = set(key_figures)

    all_users = list(G.nodes())
    n_early_adopters = int(len(all_users) * initial_cooperators)
    early_adopters = np.random.choice(
        [u for u in all_users if u not in cooperators],
        size=n_early_adopters,
        replace=False
    )
    cooperators.update(early_adopters)

    cooperation_history = []

    print(f"Initial cooperators (HODL): {len(cooperators)} " +
          f"({len(cooperators)/G.number_of_nodes()*100:.1f}%)")
    print(f"\nSimulating {n_steps} time steps (days during the squeeze)...\n")

    for step in range(n_steps):
        new_cooperators = _update_cooperators(
            G, cooperators, key_figures
        )

        cooperators = new_cooperators
        cooperation_rate = len(cooperators) / G.number_of_nodes()
        cooperation_history.append(cooperation_rate)

        change_str = ""
        if step > 0:
            change = cooperation_history[step] - cooperation_history[step-1]
            change_str = f"  [Change: {change*100:+.1f}%]"

        print(f"Day {step + 1}: {len(cooperators):4d} holders " +
              f"({cooperation_rate*100:5.1f}%){change_str}")

    return cooperation_history, cooperators


def _update_cooperators(
    G: nx.DiGraph,
    cooperators: Set[str],
    key_figures: List[str]
) -> Set[str]:
    """
    Update cooperator set for one time step.

    Parameters
    ----------
    G : nx.DiGraph
        Network graph
    cooperators : set
        Current set of cooperating users
    key_figures : list
        List of influential users

    Returns
    -------
    new_cooperators : set
        Updated set of cooperating users
    """
    new_cooperators = set()

    for node in G.nodes():
        # Get neighbors (users this person sees/interacts with)
        neighbors = list(G.predecessors(node)) + list(G.successors(node))

        if not neighbors:
            # Isolated node - maintain previous state or follow influencers
            if node in cooperators:
                new_cooperators.add(node)
            continue

        # Calculate weighted influence
        influence_weight = sum(
            INFLUENCER_WEIGHT_MULTIPLIER if n in key_figures else 1
            for n in neighbors if n in cooperators
        )
        total_influence = sum(
            INFLUENCER_WEIGHT_MULTIPLIER if n in key_figures else 1
            for n in neighbors
        )

        cooperation_ratio = influence_weight / total_influence if total_influence > 0 else 0

        # Decision logic
        if cooperation_ratio > COOPERATION_THRESHOLD:
            # Majority cooperates
            new_cooperators.add(node)
        elif node in key_figures:
            # Influencers stay committed (public commitment)
            new_cooperators.add(node)
        elif cooperation_ratio > STICKY_THRESHOLD and node in cooperators:
            # Sticky cooperation
            new_cooperators.add(node)
        # else: defect

    return new_cooperators


def identify_tipping_point(cooperation_history: List[float]) -> int:
    """
    Identify the tipping point in cooperation history.

    Tipping point = first step where cooperation crosses 50%.

    Parameters
    ----------
    cooperation_history : list
        List of cooperation rates over time

    Returns
    -------
    tipping_point : int
        Step number of tipping point, or -1 if never reached
    """
    for i, rate in enumerate(cooperation_history):
        if rate > 0.5:
            return i + 1  # Return day number (1-indexed)

    return -1  # Never reached


def analyze_tft_results(
    cooperation_history: List[float],
    final_cooperators: Set[str],
    total_users: int
) -> dict:
    """
    Analyze TFT simulation results.

    Parameters
    ----------
    cooperation_history : list
        Cooperation rates over time
    final_cooperators : set
        Final set of cooperators
    total_users : int
        Total number of users

    Returns
    -------
    analysis : dict
        Analysis results
    """
    tipping_point = identify_tipping_point(cooperation_history)

    return {
        'initial_cooperation': cooperation_history[0],
        'final_cooperation': cooperation_history[-1],
        'max_cooperation': max(cooperation_history),
        'tipping_point_day': tipping_point,
        'tipping_point_reached': tipping_point > 0,
        'n_final_cooperators': len(final_cooperators),
        'cooperation_growth': cooperation_history[-1] - cooperation_history[0]
    }
