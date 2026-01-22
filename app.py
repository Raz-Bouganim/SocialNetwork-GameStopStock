#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GameStop Social Network Analysis - Streamlit Web Application
============================================================

Interactive web application for analyzing the GameStop short squeeze
social network from r/WallStreetBets (2021).

Authors: Raz Bouganim, Omer Katz, Ohad Cohen
Course: Social Network Analysis
"""

import streamlit as st
import numpy as np
import pandas as pd
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from io import BytesIO
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Import project modules
from src.utils.config import KEY_FIGURES
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
from src.visualization import (
    plot_network_sample,
    get_top_influencers,
    get_top_bridges,
    get_degree_distribution
)

# ============================================================================
# CONSTANTS
# ============================================================================

# Consistent color scheme for key figures across all charts
KEY_FIGURE_COLOR = "#FF4B4B"  # Red for key figures
REGULAR_USER_COLOR = "#636EFA"  # Blue for regular users
BRIDGE_COLOR = "#FFA15A"  # Orange for bridges

# ============================================================================
# PRE-COMPUTED DEFAULT RESULTS (network_size=1000, seed=42, tft_steps=10, k=2)
# ============================================================================
# These results are pre-computed so users see data immediately without waiting.
# Users can still run custom analysis with different parameters.

DEFAULT_RESULTS = {
    'stats': {
        'n_nodes': 1000,
        'n_edges': 6804,
        'largest_wcc_pct': 100.0
    },
    'density': 0.0068108108108108105,
    'centralization': 0.18876190820078595,
    'cent_interpretation': 'DECENTRALIZED - Grassroots movement',
    'density_interpretation': 'SPARSE - Loose community structure',
    'community_info': {'n_communities': 14},

    # TFT Results
    'cooperation_history': [0.278, 0.513, 0.718, 0.887, 0.961, 0.984, 0.994, 1.0, 1.0, 1.0],
    'tft_analysis': {
        'initial_cooperation': 0.278,
        'final_cooperation': 1.0,
        'max_cooperation': 1.0,
        'tipping_point_reached': True,
        'tipping_point_day': 2
    },

    # Network Values
    'network_values': {
        'sarnoff': 1000.0,
        'metcalfe': 1000000.0,
        'reed': 2.6609188896406874e+23
    },

    # Echo Chamber
    'echo_analysis': {
        'n_users': 1000,
        'n_posts': 200,
        'n_comments': 5317,
        'n_nodes': 1000,
        'n_edges': 213643,
        'n_components': 81,
        'largest_component_size': 920,
        'largest_component_pct': 92.0,
        'mean_shared_posts': 2.42,
        'max_shared_posts': 6,
        'k_threshold': 2
    },
    'component_sizes': [920, 1, 1, 1, 1, 1, 1, 1, 1, 1],

    # Comparison with random network
    'random_centralization': 0.008229672558329872,
    'random_avg_degree': 13.59,
    'random_max_degree': 27,
    'sf_avg_degree': 13.608,
    'sf_max_degree': 260,

    # Top 20 Influencers (user, weighted_in_degree)
    'top_influencers': [
        ('DeepFuckingValue', 4778), ('zjz', 4338), ('SIR_JACK_A_LOT', 4056),
        ('bawse1', 3692), ('AutoModerator', 3458), ('OPINION_IS_UNPOPULAR', 3252),
        ('VisualMod', 3225), ('Stylux', 3187), ('wsbgod', 2589), ('ITradeBaconFutures', 1802),
        ('user_0004', 501), ('user_0006', 483), ('user_0007', 408), ('user_0005', 406),
        ('user_0012', 318), ('user_0003', 302), ('user_0034', 297), ('user_0008', 279),
        ('user_0000', 246), ('user_0022', 219)
    ],

    # Top 20 Bridges (user, betweenness)
    'top_bridges': [
        ('user_0004', 0.1968), ('bawse1', 0.1629), ('DeepFuckingValue', 0.1202),
        ('user_0007', 0.1082), ('zjz', 0.0986), ('AutoModerator', 0.0968),
        ('OPINION_IS_UNPOPULAR', 0.0961), ('user_0048', 0.0840), ('user_0012', 0.0834),
        ('wsbgod', 0.0796), ('user_0006', 0.0789), ('user_0029', 0.0778),
        ('user_0005', 0.0775), ('user_0000', 0.0754), ('user_0010', 0.0691),
        ('VisualMod', 0.0682), ('Stylux', 0.0635), ('SIR_JACK_A_LOT', 0.0604),
        ('user_0003', 0.0530), ('user_0022', 0.0509)
    ],

    # Degree distribution histogram data
    'degree_histogram': {
        'counts': [584, 236, 65, 5, 2, 32, 30, 12, 2, 4, 2, 2, 2, 0, 3, 1, 1, 1, 1, 0,
                   2, 0, 0, 0, 0, 1, 0, 2, 0, 1, 0, 2, 0, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        'bin_edges': [3.0, 8.14, 13.28, 18.42, 23.56, 28.7, 33.84, 38.98, 44.12, 49.26,
                      54.4, 59.54, 64.68, 69.82, 74.96, 80.1, 85.24, 90.38, 95.52, 100.66,
                      105.8, 110.94, 116.08, 121.22, 126.36, 131.5, 136.64, 141.78, 146.92, 152.06,
                      157.2, 162.34, 167.48, 172.62, 177.76, 182.9, 188.04, 193.18, 198.32, 203.46,
                      208.6, 213.74, 218.88, 224.02, 229.16, 234.3, 239.44, 244.58, 249.72, 254.86, 260.0]
    },

    # Key figures list
    'key_figures': ['DeepFuckingValue', 'zjz', 'OPINION_IS_UNPOPULAR', 'Stylux', 'bawse1',
                    'ITradeBaconFutures', 'VisualMod', 'AutoModerator', 'wsbgod', 'SIR_JACK_A_LOT']
}

DEFAULT_PARAMS = {
    'network_size': 1000,
    'seed': 42,
    'tft_steps': 10,
    'k_threshold': 2
}

# GameStop timeline events (actual dates from January 2021)
GAMESTOP_TIMELINE = [
    {"date": "Jan 11", "day": 1, "event": "GME at $19.95", "price": 19.95},
    {"date": "Jan 13", "day": 2, "event": "First major spike to $31", "price": 31.40},
    {"date": "Jan 22", "day": 3, "event": "Trading halted, closes at $65", "price": 65.01},
    {"date": "Jan 25", "day": 4, "event": "Elon Musk tweets 'Gamestonk!!'", "price": 76.79},
    {"date": "Jan 26", "day": 5, "event": "Price doubles to $147", "price": 147.98},
    {"date": "Jan 27", "day": 6, "event": "Peak frenzy, hits $347", "price": 347.51},
    {"date": "Jan 28", "day": 7, "event": "Robinhood restricts buying", "price": 193.60},
    {"date": "Jan 29", "day": 8, "event": "Partial recovery to $325", "price": 325.00},
    {"date": "Feb 1", "day": 9, "event": "Price stabilizes around $225", "price": 225.00},
    {"date": "Feb 2", "day": 10, "event": "Decline begins, $90", "price": 90.00},
]

# Page configuration
st.set_page_config(
    page_title="GameStop Network Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #FAFAFA;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: bold;
    }
    .interpretation-box {
        background-color: #1E1E1E;
        border-left: 4px solid #FF4B4B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 0.5rem 0.5rem 0;
    }
    .methodology-box {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .timeline-event {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
    }
    /* Sidebar: remove top padding, disable scroll, not collapsible */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-top: 0.5rem !important;
    }
    [data-testid="stSidebarHeader"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow: hidden;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
        display: none;
    }
    section[data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    /* Hide resize handle and disable resize cursor */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] > div:nth-child(2) {
        display: none !important;
    }
    div[data-testid="stSidebarResizeHandle"] {
        display: none !important;
        pointer-events: none !important;
    }
    /* Reduce spacing between sidebar elements */
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stNumberInput {
        margin-bottom: -0.5rem;
    }
    /* Compact authors section */
    .sidebar-authors {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def run_full_analysis_with_progress(network_size: int, seed: int, tft_steps: int, k_threshold: int, progress_callback=None):
    """
    Run the complete network analysis pipeline with progress reporting.
    """
    results = {}

    def update_progress(step, total_steps, message):
        if progress_callback:
            progress_callback(step / total_steps, message)

    total_steps = 7

    # Step 1: Build network
    update_progress(0, total_steps, "Step 1/7: Building scale-free network...")
    G, key_figures = create_scale_free_network(
        n_users=network_size,
        key_figures=KEY_FIGURES,
        seed=seed
    )
    results['G'] = G
    results['key_figures'] = key_figures
    results['stats'] = get_network_stats(G)
    update_progress(1, total_steps, "Step 1/7: Network built ✓")

    # Step 2: Calculate centralities
    update_progress(1, total_steps, "Step 2/7: Calculating centrality metrics...")
    centralities = calculate_all_centralities(G)
    results['centralities'] = centralities
    update_progress(2, total_steps, "Step 2/7: Centralities calculated ✓")

    # Step 3: Structure analysis
    update_progress(2, total_steps, "Step 3/7: Analyzing network structure...")
    results['density'] = calculate_network_density(G)
    results['centralization'] = calculate_freeman_centralization(G, 'in_degree')
    results['cent_interpretation'] = interpret_centralization(results['centralization'])
    results['density_interpretation'] = interpret_density(results['density'], G.number_of_nodes())
    update_progress(3, total_steps, "Step 3/7: Structure analyzed ✓")

    # Step 4: TFT simulation
    update_progress(3, total_steps, "Step 4/7: Running Tit-for-Tat simulation...")
    cooperation_history, final_cooperators = simulate_tft_dynamics(
        G, key_figures, tft_steps, initial_cooperators=0.15
    )
    results['cooperation_history'] = cooperation_history
    results['tft_analysis'] = analyze_tft_results(
        cooperation_history, final_cooperators, G.number_of_nodes()
    )
    update_progress(4, total_steps, "Step 4/7: TFT simulation complete ✓")

    # Step 5: Network value
    update_progress(4, total_steps, "Step 5/7: Computing network value laws...")
    sarnoff, metcalfe, reed = compare_network_values(G.number_of_nodes())
    results['network_values'] = {'sarnoff': sarnoff, 'metcalfe': metcalfe, 'reed': reed}
    results['community_info'] = detect_communities(G.to_undirected())
    update_progress(5, total_steps, "Step 5/7: Network values computed ✓")

    # Step 6: Bipartite & Echo Chamber
    update_progress(5, total_steps, "Step 6/7: Building bipartite graph & echo chamber analysis...")
    B, posts = create_bipartite_graph(G, key_figures, n_posts=200)
    results['B'] = B
    user_projection, shared_matrix, matrix_info = project_to_users(B, k_threshold=k_threshold)
    results['user_projection'] = user_projection
    results['matrix_info'] = matrix_info

    echo_analysis, components, largest_component = analyze_echo_chamber(user_projection)
    echo_analysis['n_users'] = matrix_info['n_users']
    echo_analysis['n_posts'] = matrix_info['n_posts']
    echo_analysis['n_comments'] = matrix_info['total_comments']
    echo_analysis['k_threshold'] = matrix_info['k_threshold']
    results['echo_analysis'] = echo_analysis
    results['component_sizes'] = [len(c) for c in components]
    update_progress(6, total_steps, "Step 6/7: Echo chamber analyzed ✓")

    # Step 7: Generate random network for comparison
    update_progress(6, total_steps, "Step 7/7: Generating comparison network...")
    random_G = nx.erdos_renyi_graph(network_size, results['density'], directed=True, seed=seed)
    results['random_density'] = nx.density(random_G)
    results['random_centralization'] = calculate_freeman_centralization(
        nx.DiGraph(random_G), 'in_degree'
    )
    random_degrees = [d for n, d in random_G.degree()]
    results['random_avg_degree'] = np.mean(random_degrees)
    results['random_max_degree'] = max(random_degrees)

    # Scale-free network stats
    sf_degrees = [d for n, d in G.degree()]
    results['sf_avg_degree'] = np.mean(sf_degrees)
    results['sf_max_degree'] = max(sf_degrees)
    update_progress(7, total_steps, "Analysis complete! ✓")

    return results


@st.cache_data(show_spinner=False)
def run_full_analysis(network_size: int, seed: int, tft_steps: int, k_threshold: int):
    """
    Run the complete network analysis pipeline.
    Cached to avoid re-running with same parameters.
    """
    results = {}

    # Step 1: Build network
    G, key_figures = create_scale_free_network(
        n_users=network_size,
        key_figures=KEY_FIGURES,
        seed=seed
    )
    results['G'] = G
    results['key_figures'] = key_figures
    results['stats'] = get_network_stats(G)

    # Step 2: Calculate centralities
    centralities = calculate_all_centralities(G)
    results['centralities'] = centralities

    # Step 3: Structure analysis
    results['density'] = calculate_network_density(G)
    results['centralization'] = calculate_freeman_centralization(G, 'in_degree')
    results['cent_interpretation'] = interpret_centralization(results['centralization'])
    results['density_interpretation'] = interpret_density(results['density'], G.number_of_nodes())

    # Step 4: TFT simulation
    cooperation_history, final_cooperators = simulate_tft_dynamics(
        G, key_figures, tft_steps, initial_cooperators=0.15
    )
    results['cooperation_history'] = cooperation_history
    results['tft_analysis'] = analyze_tft_results(
        cooperation_history, final_cooperators, G.number_of_nodes()
    )

    # Step 5: Network value
    sarnoff, metcalfe, reed = compare_network_values(G.number_of_nodes())
    results['network_values'] = {'sarnoff': sarnoff, 'metcalfe': metcalfe, 'reed': reed}
    results['community_info'] = detect_communities(G.to_undirected())

    # Step 6: Bipartite & Echo Chamber
    B, posts = create_bipartite_graph(G, key_figures, n_posts=200)
    results['B'] = B
    user_projection, shared_matrix, matrix_info = project_to_users(B, k_threshold=k_threshold)
    results['user_projection'] = user_projection
    results['matrix_info'] = matrix_info

    echo_analysis, components, largest_component = analyze_echo_chamber(user_projection)
    echo_analysis['n_users'] = matrix_info['n_users']
    echo_analysis['n_posts'] = matrix_info['n_posts']
    echo_analysis['n_comments'] = matrix_info['total_comments']
    echo_analysis['k_threshold'] = matrix_info['k_threshold']
    results['echo_analysis'] = echo_analysis
    results['component_sizes'] = [len(c) for c in components]

    # Step 7: Generate random network for comparison
    random_G = nx.erdos_renyi_graph(network_size, results['density'], directed=True, seed=seed)
    results['random_density'] = nx.density(random_G)
    results['random_centralization'] = calculate_freeman_centralization(
        nx.DiGraph(random_G), 'in_degree'
    )
    random_degrees = [d for n, d in random_G.degree()]
    results['random_avg_degree'] = np.mean(random_degrees)
    results['random_max_degree'] = max(random_degrees)

    # Scale-free network stats
    sf_degrees = [d for n, d in G.degree()]
    results['sf_avg_degree'] = np.mean(sf_degrees)
    results['sf_max_degree'] = max(sf_degrees)

    return results


# ============================================================================
# CHART FUNCTIONS
# ============================================================================

def create_degree_distribution_chart(G: nx.DiGraph = None, histogram_data: dict = None) -> go.Figure:
    """Create interactive degree distribution histogram with Plotly."""
    if histogram_data:
        # Use pre-computed histogram data
        counts = histogram_data['counts']
        bin_edges = histogram_data['bin_edges']
        # Create bar chart from histogram data
        bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(counts))]
        fig = go.Figure(go.Bar(
            x=bin_centers,
            y=counts,
            marker_color=REGULAR_USER_COLOR,
            width=[(bin_edges[i+1] - bin_edges[i]) * 0.9 for i in range(len(counts))]
        ))
    else:
        degrees = [d for n, d in G.degree()]
        fig = px.histogram(
            x=degrees,
            nbins=50,
            title="Degree Distribution (Power Law)",
            labels={'x': 'Degree (Number of Connections)', 'y': 'Frequency'},
            color_discrete_sequence=[REGULAR_USER_COLOR]
        )

    fig.update_layout(
        title="Degree Distribution (Power Law)",
        xaxis_title="Degree (Number of Connections)",
        yaxis_title="Frequency",
        yaxis_type="log",
        template="plotly_dark",
        showlegend=False,
        height=400
    )
    return fig


def create_top_influencers_chart(centralities: dict = None, key_figures: list = None, precomputed: list = None) -> go.Figure:
    """Create interactive bar chart of top influencers."""
    if precomputed:
        top_20 = precomputed
    else:
        top_20 = get_top_influencers(centralities, n=20)

    users, weights = zip(*top_20)
    key_figs = key_figures or DEFAULT_RESULTS['key_figures']
    colors = [KEY_FIGURE_COLOR if u in key_figs else REGULAR_USER_COLOR for u in users]

    fig = go.Figure(go.Bar(
        x=list(weights),
        y=[u[:15] + '...' if len(u) > 15 else u for u in users],
        orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>Weighted In-Degree: %{x:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title="Top 20 Most Influential Users",
        xaxis_title="Weighted In-Degree",
        yaxis_title="",
        template="plotly_dark",
        height=500,
        yaxis={'autorange': 'reversed'}
    )
    return fig


def create_top_bridges_chart(centralities: dict = None, key_figures: list = None, precomputed: list = None) -> go.Figure:
    """Create interactive bar chart of top bridges."""
    if precomputed:
        top_20 = precomputed
    else:
        top_20 = get_top_bridges(centralities, n=20)

    users, scores = zip(*top_20)
    key_figs = key_figures or DEFAULT_RESULTS['key_figures']
    colors = [KEY_FIGURE_COLOR if u in key_figs else BRIDGE_COLOR for u in users]

    fig = go.Figure(go.Bar(
        x=list(scores),
        y=[u[:15] + '...' if len(u) > 15 else u for u in users],
        orientation='h',
        marker_color=colors,
        hovertemplate='<b>%{y}</b><br>Betweenness: %{x:.4f}<extra></extra>'
    ))

    fig.update_layout(
        title="Top 20 Information Bridges",
        xaxis_title="Betweenness Centrality",
        yaxis_title="",
        template="plotly_dark",
        height=500,
        yaxis={'autorange': 'reversed'}
    )
    return fig


def create_tft_evolution_chart(cooperation_history: list, show_timeline: bool = True) -> go.Figure:
    """Create TFT evolution line chart with tipping point and optional GME timeline."""
    days = list(range(1, len(cooperation_history) + 1))
    cooperation_pct = [h * 100 for h in cooperation_history]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Main cooperation line
    fig.add_trace(
        go.Scatter(
            x=days,
            y=cooperation_pct,
            mode='lines+markers',
            name='HODL Rate (%)',
            line=dict(color='#00CC96', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(0, 204, 150, 0.2)',
            hovertemplate='Day %{x}<br>Cooperation: %{y:.1f}%<extra></extra>'
        ),
        secondary_y=False
    )

    # Add GME price timeline if enabled and we have enough days
    if show_timeline and len(cooperation_history) <= len(GAMESTOP_TIMELINE):
        timeline_days = [t['day'] for t in GAMESTOP_TIMELINE[:len(cooperation_history)]]
        timeline_prices = [t['price'] for t in GAMESTOP_TIMELINE[:len(cooperation_history)]]

        fig.add_trace(
            go.Scatter(
                x=timeline_days,
                y=timeline_prices,
                mode='lines+markers',
                name='GME Price ($)',
                line=dict(color='#FFD700', width=2, dash='dot'),
                marker=dict(size=8, symbol='diamond'),
                hovertemplate='Day %{x}<br>GME: $%{y:.2f}<extra></extra>'
            ),
            secondary_y=True
        )

    # Find and annotate tipping point
    for i, pct in enumerate(cooperation_pct):
        if pct > 50 and (i == 0 or cooperation_pct[i-1] <= 50):
            fig.add_annotation(
                x=i+1,
                y=pct,
                text="Tipping Point",
                showarrow=True,
                arrowhead=2,
                arrowcolor=KEY_FIGURE_COLOR,
                font=dict(color=KEY_FIGURE_COLOR, size=14, family='Arial Black'),
                ax=0,
                ay=-40
            )
            break

    # 50% threshold line
    fig.add_hline(y=50, line_dash="dash", line_color="gray",
                  annotation_text="50% Threshold", secondary_y=False)

    fig.update_layout(
        title="Tit-for-Tat Evolution vs. Actual GME Price Movement",
        template="plotly_dark",
        height=450,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )

    fig.update_xaxes(title_text="Day (Time Step)")
    fig.update_yaxes(title_text="% Holding (Cooperating)", secondary_y=False, range=[0, 100])
    fig.update_yaxes(title_text="GME Stock Price ($)", secondary_y=True)

    return fig


def create_network_value_chart(network_values: dict, n_nodes: int) -> go.Figure:
    """Create network value comparison bar chart."""
    laws = ['Sarnoff (N)', 'Metcalfe (N²)', "Reed (2^N)"]
    values = [network_values['sarnoff'], network_values['metcalfe'], network_values['reed']]
    values_log = [np.log10(v) for v in values]
    colors = [REGULAR_USER_COLOR, BRIDGE_COLOR, '#EF553B']

    fig = go.Figure(go.Bar(
        x=laws,
        y=values_log,
        marker_color=colors,
        text=[f"10^{v:.1f}" for v in values_log],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Value: %{text}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Network Value Laws Comparison (N={n_nodes:,})",
        yaxis_title="Network Value (log10 scale)",
        template="plotly_dark",
        height=400,
        showlegend=False
    )
    return fig


def create_centrality_comparison_chart(centralities: dict, key_figures: list) -> go.Figure:
    """Create grouped bar chart comparing centralities for key figures."""
    data = []
    for user in key_figures:
        if (user in centralities['degree_centrality'] and
            user in centralities['betweenness'] and
            user in centralities['closeness']):
            data.append({
                'User': user[:12] + '...' if len(user) > 12 else user,
                'Degree': centralities['degree_centrality'][user],
                'Betweenness': centralities['betweenness'][user],
                'Closeness': centralities['closeness'].get(user, 0)
            })

    if not data:
        return go.Figure()

    df = pd.DataFrame(data)

    fig = go.Figure()
    for metric, color in [('Degree', REGULAR_USER_COLOR), ('Betweenness', BRIDGE_COLOR), ('Closeness', '#00CC96')]:
        fig.add_trace(go.Bar(
            name=metric,
            x=df['User'],
            y=df[metric],
            marker_color=color
        ))

    fig.update_layout(
        title="Centrality Comparison (Key Influencers)",
        yaxis_title="Centrality Score",
        template="plotly_dark",
        height=400,
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig


def create_component_sizes_chart(component_sizes: list) -> go.Figure:
    """Create bar chart of connected component sizes."""
    sizes_sorted = sorted(component_sizes, reverse=True)[:20]

    colors = [KEY_FIGURE_COLOR] + ['#AB63FA'] * (len(sizes_sorted) - 1)

    fig = go.Figure(go.Bar(
        x=list(range(1, len(sizes_sorted) + 1)),
        y=sizes_sorted,
        marker_color=colors,
        hovertemplate='Rank %{x}<br>Size: %{y:,} users<extra></extra>'
    ))

    fig.update_layout(
        title=f"Connected Components (Giant: {sizes_sorted[0]:,} users)",
        xaxis_title="Component Rank",
        yaxis_title="Size (# Users)",
        template="plotly_dark",
        height=400
    )
    return fig


def create_network_comparison_chart(results: dict = None) -> go.Figure:
    """Create comparison chart between scale-free and random networks."""
    # Use defaults if no results provided
    r = results or DEFAULT_RESULTS

    metrics = ['Centralization', 'Max Degree', 'Avg Degree']
    n_nodes = r['stats']['n_nodes']

    scale_free_values = [
        r['centralization'],
        r['sf_max_degree'] / n_nodes,  # Normalized
        r['sf_avg_degree'] / n_nodes   # Normalized
    ]

    random_values = [
        r['random_centralization'],
        r['random_max_degree'] / n_nodes,
        r['random_avg_degree'] / n_nodes
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Scale-Free (WSB)',
        x=metrics,
        y=scale_free_values,
        marker_color=KEY_FIGURE_COLOR
    ))

    fig.add_trace(go.Bar(
        name='Random (Erdos-Renyi)',
        x=metrics,
        y=random_values,
        marker_color='#888888'
    ))

    fig.update_layout(
        title="Scale-Free vs Random Network Comparison",
        yaxis_title="Normalized Value",
        template="plotly_dark",
        height=400,
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def get_network_gexf(G: nx.DiGraph) -> bytes:
    """Export network to GEXF format."""
    buffer = BytesIO()
    nx.write_gexf(G, buffer)
    return buffer.getvalue()


def generate_pdf_report(results: dict, params: dict) -> bytes:
    """Generate a PDF summary report."""
    # Create a text-based report (PDF generation would require reportlab)
    report = f"""
================================================================================
GAMESTOP SHORT SQUEEZE - SOCIAL NETWORK ANALYSIS REPORT
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Authors: Raz Bouganim, Omer Katz, Ohad Cohen
Course: Social Network Analysis

================================================================================
PARAMETERS
================================================================================
Network Size: {params['network_size']} users
Random Seed: {params['seed']}
Simulation Days: {params['tft_steps']}
K-Threshold: {params['k_threshold']}

================================================================================
NETWORK STATISTICS
================================================================================
Nodes: {results['stats']['n_nodes']:,}
Edges: {results['stats']['n_edges']:,}
Density: {results['density']:.6f}
Freeman Centralization: {results['centralization']:.4f}
Structure: {results['density_interpretation']}
Centralization Type: {results['cent_interpretation']}
Communities Detected: {results['community_info']['n_communities']}

================================================================================
TOP 10 INFLUENCERS (by Weighted In-Degree)
================================================================================
"""
    top_10 = get_top_influencers(results['centralities'], n=10)
    for i, (user, score) in enumerate(top_10, 1):
        is_key = " [KEY FIGURE]" if user in results['key_figures'] else ""
        report += f"{i:2}. {user}: {score:,.0f}{is_key}\n"

    report += f"""
================================================================================
GAME THEORY ANALYSIS (Tit-for-Tat)
================================================================================
Initial Cooperation: {results['tft_analysis']['initial_cooperation']*100:.1f}%
Final Cooperation: {results['tft_analysis']['final_cooperation']*100:.1f}%
Maximum Cooperation: {results['tft_analysis']['max_cooperation']*100:.1f}%
Tipping Point Reached: {'Yes, Day ' + str(results['tft_analysis']['tipping_point_day']) if results['tft_analysis']['tipping_point_reached'] else 'No'}

================================================================================
ECHO CHAMBER ANALYSIS
================================================================================
Users Analyzed: {results['echo_analysis']['n_users']:,}
Posts Analyzed: {results['echo_analysis']['n_posts']:,}
Giant Component Size: {results['echo_analysis']['largest_component_size']:,} ({results['echo_analysis']['largest_component_pct']:.1f}%)
Echo Chamber Status: {'CONFIRMED' if results['echo_analysis']['largest_component_pct'] > 50 else 'NOT DETECTED'}

================================================================================
NETWORK VALUE COMPARISON
================================================================================
Sarnoff's Law (N): {results['network_values']['sarnoff']:,.0f}
Metcalfe's Law (N²): {results['network_values']['metcalfe']:,.0f}
Reed's Law (2^N): {results['network_values']['reed']:,.0f}

================================================================================
KEY FINDINGS
================================================================================
1. The network exhibits scale-free properties with power-law degree distribution,
   indicating the presence of highly connected "hub" users.

2. Key influencers like DeepFuckingValue show significantly higher centrality
   metrics compared to average users, confirming their pivotal role.

3. The Tit-for-Tat simulation demonstrates how initial cooperation among
   influencers can cascade through the network, reaching a tipping point.

4. Echo chamber analysis confirms that the majority of users ({results['echo_analysis']['largest_component_pct']:.1f}%)
   are connected through shared content consumption.

5. The network's value grows exponentially with group formation (Reed's Law),
   explaining the rapid coordination observed during the short squeeze.

================================================================================
REFERENCES
================================================================================
- Barabasi, A.L. & Albert, R. (1999). Emergence of Scaling in Random Networks.
- Metcalfe, R. (2013). Metcalfe's Law after 40 Years of Ethernet.
- Reed, D.P. (1999). That Sneaky Exponential (Reed's Law).
- Axelrod, R. (1984). The Evolution of Cooperation.
================================================================================
"""
    return report.encode('utf-8')


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown('<p class="main-header">GAMESTOP SHORT SQUEEZE - SOCIAL NETWORK ANALYSIS</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">r/WallStreetBets Network Analysis (2021)</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        # Check if analysis is currently running (need this before inputs)
        is_running = st.session_state.get('analysis_running', False)

        st.header("Parameters")

        network_size = st.slider(
            "Network Size",
            min_value=500,
            max_value=2000,
            value=1000,
            step=100,
            help="Number of users in the simulated network",
            disabled=is_running
        )

        random_seed = st.number_input(
            "Random Seed",
            min_value=1,
            max_value=9999,
            value=42,
            help="Seed for reproducibility",
            disabled=is_running
        )

        tft_steps = st.slider(
            "Simulation Days",
            min_value=5,
            max_value=20,
            value=10,
            help="Number of days to simulate TFT dynamics",
            disabled=is_running
        )

        k_threshold = st.slider(
            "K-Threshold",
            min_value=1,
            max_value=5,
            value=2,
            help="Minimum shared posts to create edge in user projection",
            disabled=is_running
        )

        st.divider()

        # Check if current params match defaults
        is_default = (network_size == 1000 and random_seed == 42 and
                      tft_steps == 10 and k_threshold == 2)

        # Check if current params match stored custom results
        stored_params = st.session_state.get('custom_params', {})
        matches_custom = (
            stored_params.get('network_size') == network_size and
            stored_params.get('seed') == random_seed and
            stored_params.get('tft_steps') == tft_steps and
            stored_params.get('k_threshold') == k_threshold
        )

        # Show appropriate message
        if is_running:
            st.warning("⏳ Analysis running... please wait")
        elif is_default:
            st.info("Showing pre-computed results (default parameters)")
        elif matches_custom:
            st.success("Showing custom analysis results")
        else:
            st.warning("Parameters changed - click below to re-run")

        run_button = st.button("Run Custom Analysis", type="primary", use_container_width=True,
                               disabled=(is_default or matches_custom or is_running))

        st.divider()
        st.markdown('<p class="sidebar-authors">By: Raz Bouganim, Omer Katz, Ohad Cohen<br>Course: Social Network Analysis</p>', unsafe_allow_html=True)

    # Determine which results to use
    use_custom = False

    # Handle button click - set running flag and rerun to update sidebar
    if run_button and not is_default and not is_running:
        st.session_state['analysis_running'] = True
        st.session_state['run_params'] = {
            'network_size': network_size,
            'seed': random_seed,
            'tft_steps': tft_steps,
            'k_threshold': k_threshold
        }
        st.rerun()

    # Actually run analysis if flag is set
    if is_running:
        params_to_run = st.session_state.get('run_params', {})

        # Run custom analysis with progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(pct, msg):
            progress_bar.progress(pct)
            status_text.text(msg)

        # Capture print output and run analysis
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            results = run_full_analysis_with_progress(
                params_to_run['network_size'],
                params_to_run['seed'],
                params_to_run['tft_steps'],
                params_to_run['k_threshold'],
                update_progress
            )

            # Store custom results
            st.session_state['custom_results'] = results
            st.session_state['custom_params'] = params_to_run
            st.session_state['analysis_running'] = False
            status_text.empty()
            progress_bar.empty()

        finally:
            sys.stdout = old_stdout

        # Rerun to update sidebar message
        st.rerun()

    elif 'custom_results' in st.session_state and not is_default:
        # Show custom results unless user went back to defaults
        use_custom = True

    # Select results source
    if use_custom:
        results = st.session_state['custom_results']
        params = st.session_state['custom_params']
        using_defaults = False
    else:
        results = DEFAULT_RESULTS
        params = DEFAULT_PARAMS
        using_defaults = True

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Overview", "Centrality", "Game Theory", "Network Value", "Echo Chamber", "Conclusions", "Methodology"
    ])

    # ====================================================================
    # TAB 1: OVERVIEW
    # ====================================================================
    with tab1:
        if using_defaults:
            st.caption("Showing pre-computed results with default parameters (N=1000, seed=42)")

        st.subheader("Network Statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nodes", f"{results['stats']['n_nodes']:,}")
        with col2:
            st.metric("Edges", f"{results['stats']['n_edges']:,}")
        with col3:
            st.metric("Density", f"{results['density']:.6f}")
        with col4:
            st.metric("Centralization", f"{results['centralization']:.3f}")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Network Sample")
            if not using_defaults and 'G' in results:
                fig = plot_network_sample(results['G'], results['key_figures'], figsize=(8, 6))
                st.pyplot(fig)
                plt.close()
            else:
                # Show pre-generated network sample image for defaults
                import os
                if os.path.exists("output/network_sample.png"):
                    st.image("output/network_sample.png", use_container_width=True)
                else:
                    st.info("Run custom analysis to generate network visualization.")

            # Interpretation
            st.markdown("""
            > **Interpretation:** The visualization shows a sample of the network structure.
            > Red nodes represent key influencers (DeepFuckingValue, moderators, etc.) who
            > are highly connected hubs. The star-like patterns around them demonstrate
            > preferential attachment - new users tend to connect to already popular figures.
            """)

        with col2:
            st.subheader("Degree Distribution")
            if using_defaults:
                fig = create_degree_distribution_chart(histogram_data=results.get('degree_histogram'))
            else:
                fig = create_degree_distribution_chart(G=results['G'])
            st.plotly_chart(fig, use_container_width=True)

            # Interpretation
            st.markdown("""
            > **Interpretation:** The log-scale histogram reveals a power-law distribution -
            > most users have few connections, while a small number of "hubs" have many.
            > This is characteristic of scale-free networks like social media platforms,
            > where popularity breeds more popularity (the "rich get richer" phenomenon).
            """)

        st.divider()

        # Network comparison section
        st.subheader("Scale-Free vs Random Network")

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = create_network_comparison_chart(results)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("""
            **Why Scale-Free Matters:**

            Unlike random networks where connections are evenly distributed,
            scale-free networks have:

            - **Higher centralization** - Power concentrated in hubs
            - **Higher max degree** - Super-connectors exist
            - **Resilience** - Network survives random failures
            - **Vulnerability** - Targeted attacks on hubs are devastating

            This explains why banning key WSB figures would have
            disrupted the movement more than removing random users.
            """)

        st.divider()

        st.subheader("Key Findings")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Network Structure:** {results['density_interpretation']}")
            st.info(f"**Communities Detected:** {results['community_info']['n_communities']}")
        with col2:
            st.info(f"**Centralization:** {results['cent_interpretation']}")
            is_wcc = results['stats'].get('largest_wcc_pct', 100)
            st.info(f"**Largest Component:** {is_wcc:.1f}% of network")

    # ====================================================================
    # TAB 2: CENTRALITY
    # ====================================================================
    with tab2:
        st.subheader("Centrality Analysis")

        # Get key figures list
        key_figs = results.get('key_figures', DEFAULT_RESULTS['key_figures'])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Top Influencers** (Most Received Replies)")
            st.caption(f"🔴 Key Figure  🔵 Regular User")
            if using_defaults:
                fig = create_top_influencers_chart(precomputed=results['top_influencers'], key_figures=key_figs)
            else:
                fig = create_top_influencers_chart(centralities=results['centralities'], key_figures=key_figs)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            > **Interpretation:** Weighted in-degree measures how much attention a user receives.
            > High values indicate users whose posts generate significant engagement.
            > DeepFuckingValue's prominence here reflects his role as the movement's catalyst -
            > his DD (Due Diligence) posts were heavily discussed and shared.
            """)

        with col2:
            st.markdown(f"**Top Bridges** (Information Flow Control)")
            st.caption(f"🔴 Key Figure  🟠 Bridge Node")
            if using_defaults:
                fig = create_top_bridges_chart(precomputed=results['top_bridges'], key_figures=key_figs)
            else:
                fig = create_top_bridges_chart(centralities=results['centralities'], key_figures=key_figs)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            > **Interpretation:** Betweenness centrality identifies users who bridge different
            > parts of the network. These "information brokers" control how ideas spread.
            > Moderators often rank high here as they connect disparate user groups and
            > regulate the flow of content.
            """)

        st.divider()

        st.subheader("Key Influencer Comparison")
        if not using_defaults and 'centralities' in results:
            fig = create_centrality_comparison_chart(results['centralities'], key_figs)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run custom analysis to see centrality comparison chart for key figures.")

        st.markdown("""
        > **Interpretation:** This comparison shows how different key figures serve different roles:
        > - **High Degree** = Popular, many connections
        > - **High Betweenness** = Bridge between communities, information broker
        > - **High Closeness** = Can reach everyone quickly, efficient spreader
        >
        > DeepFuckingValue excels in influence (degree), while moderators often excel in
        > bridging (betweenness) due to their structural position in the community.
        """)

        st.divider()

        st.subheader("Top Influencers Table")
        if using_defaults:
            top_20 = results['top_influencers']
        else:
            top_20 = get_top_influencers(results['centralities'], n=20)
        df = pd.DataFrame(top_20, columns=['User', 'Weighted In-Degree'])
        df['Is Key Figure'] = df['User'].apply(lambda x: 'Yes' if x in key_figs else 'No')
        df.index = df.index + 1
        df.index.name = 'Rank'
        st.dataframe(df, use_container_width=True)

    # ====================================================================
    # TAB 3: GAME THEORY
    # ====================================================================
    with tab3:
        st.subheader("Tit-for-Tat Game Theory Analysis")

        tft = results['tft_analysis']

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Initial Cooperation", f"{tft['initial_cooperation']*100:.1f}%")
        with col2:
            st.metric("Final Cooperation", f"{tft['final_cooperation']*100:.1f}%")
        with col3:
            st.metric("Max Cooperation", f"{tft['max_cooperation']*100:.1f}%")
        with col4:
            tipping = tft['tipping_point_day'] if tft['tipping_point_reached'] else "N/A"
            st.metric("Tipping Point", f"Day {tipping}" if isinstance(tipping, int) else tipping)

        st.divider()

        # TFT Evolution with GME Timeline
        fig = create_tft_evolution_chart(results['cooperation_history'], show_timeline=True)
        st.plotly_chart(fig, use_container_width=True)

        # Timeline events - Create a proper timeline chart
        st.markdown("**Historical Timeline (January 2021):**")

        # Create timeline data
        n_events = min(len(results['cooperation_history']), 10)
        timeline_data = GAMESTOP_TIMELINE[:n_events]

        # Build a timeline visualization
        fig_timeline = go.Figure()

        # Add price line
        fig_timeline.add_trace(go.Scatter(
            x=[e['date'] for e in timeline_data],
            y=[e['price'] for e in timeline_data],
            mode='lines+markers+text',
            name='GME Price',
            line=dict(color='#FFD700', width=3),
            marker=dict(size=12, symbol='diamond'),
            text=[f"${e['price']:.0f}" for e in timeline_data],
            textposition='top center',
            textfont=dict(size=10, color='#FFD700'),
            hovertemplate='<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>'
        ))

        # Add event annotations below the chart
        for i, event in enumerate(timeline_data):
            fig_timeline.add_annotation(
                x=event['date'],
                y=event['price'],
                text=event['event'][:30] + ('...' if len(event['event']) > 30 else ''),
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor='#888888',
                ax=0,
                ay=40 if i % 2 == 0 else 60,  # Alternate heights to avoid overlap
                font=dict(size=9, color='#FAFAFA'),
                bgcolor='rgba(38, 39, 48, 0.8)',
                borderpad=4
            )

        fig_timeline.update_layout(
            title="GME Stock Price During the Squeeze",
            yaxis_title="Price ($)",
            template="plotly_dark",
            height=350,
            showlegend=False,
            margin=dict(b=100)  # Extra bottom margin for annotations
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

        st.markdown("""
        > **Interpretation:** The simulation models "HODL" (Hold On for Dear Life) behavior using
        > Tit-for-Tat strategy. Users observe their neighbors - if most are holding, they hold too.
        > The **tipping point** marks when cooperation becomes self-sustaining (>50%).
        >
        > The overlay with actual GME prices shows how network coordination correlates with
        > price movement. The peak cooperation aligns with the stock's peak price around Day 6-7.
        """)

    # ====================================================================
    # TAB 4: NETWORK VALUE
    # ====================================================================
    with tab4:
        st.subheader("Network Value Laws")

        st.markdown("""
        Network value laws describe how the value of a network scales with the number of users.
        Understanding which law applies helps explain the power of group coordination.
        """)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig = create_network_value_chart(results['network_values'], results['stats']['n_nodes'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("""
            **The Three Laws:**

            - **Sarnoff's Law (N):** Linear value - traditional broadcast media (TV, radio)
            - **Metcalfe's Law (N²):** Quadratic - peer-to-peer connections (Facebook, telephone)
            - **Reed's Law (2^N):** Exponential - group-forming networks (Reddit, Discord)
            """)

        st.divider()

        st.markdown("""
        ### Why WSB Follows Reed's Law

        The value of r/WallStreetBets isn't just in individual connections but in the
        ability to form **coordinated groups**. Each new member exponentially increases
        possible group combinations.

        With **N = {:,}** users:
        - Sarnoff value: **{:,}** (linear)
        - Metcalfe value: **{:,}** (quadratic)
        - Reed value: **10^{:.0f}** (exponential)

        This explains how a subreddit could challenge Wall Street hedge funds - the
        group-forming capability created exponential coordination power.
        """.format(
            results['stats']['n_nodes'],
            int(results['network_values']['sarnoff']),
            int(results['network_values']['metcalfe']),
            np.log10(results['network_values']['reed'])
        ))

        st.info("""
        **Key Insight:** Traditional financial analysis underestimated WSB because it measured
        individual trader power (Sarnoff) or pairwise connections (Metcalfe), not group
        coordination potential (Reed).
        """)

    # ====================================================================
    # TAB 5: ECHO CHAMBER
    # ====================================================================
    with tab5:
        st.subheader("Echo Chamber Analysis")

        echo = results['echo_analysis']

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Users", f"{echo['n_users']:,}")
        with col2:
            st.metric("Posts", f"{echo['n_posts']:,}")
        with col3:
            st.metric("Giant Component", f"{echo['largest_component_pct']:.1f}%")
        with col4:
            echo_detected = "CONFIRMED" if echo['largest_component_pct'] > 50 else "NOT DETECTED"
            st.metric("Echo Chamber", echo_detected)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Echo Chamber Coverage")
            # Create a pie chart showing in vs out of echo chamber
            in_chamber = echo['largest_component_size']
            out_chamber = echo['n_users'] - in_chamber
            fig = go.Figure(go.Pie(
                labels=['In Echo Chamber', 'Outside'],
                values=[in_chamber, out_chamber],
                marker_colors=[KEY_FIGURE_COLOR, '#888888'],
                hole=0.4,
                textinfo='percent+value',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>%{value:,} users (%{percent})<extra></extra>'
            ))
            fig.update_layout(
                template="plotly_dark",
                height=350,
                showlegend=True,
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
                annotations=[dict(text=f'{echo["largest_component_pct"]:.0f}%', x=0.5, y=0.5,
                                 font_size=24, font_color=KEY_FIGURE_COLOR, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("""
            > **Interpretation:** The pie chart shows what proportion of users are part of the
            > giant connected component (echo chamber). When this exceeds 50%, most users
            > consume similar information, creating a self-reinforcing information environment.
            """)

        with col2:
            st.subheader("Bipartite Graph Statistics")

            st.markdown(f"""
            **User-Post Bipartite Graph:**
            - Users: {echo['n_users']:,}
            - Posts: {echo['n_posts']:,}
            - Comments (edges): {echo['n_comments']:,}

            **User Projection (k >= {echo.get('k_threshold', 2)}):**
            - Nodes: {echo['n_nodes']:,}
            - Edges: {echo['n_edges']:,}
            - Components: {echo['n_components']}

            **Giant Component:**
            - Size: {echo['largest_component_size']:,} users
            - Coverage: {echo['largest_component_pct']:.1f}%

            **Shared Content:**
            - Avg shared posts: {echo['mean_shared_posts']:.1f}
            - Max shared posts: {echo['max_shared_posts']}
            """)

            if echo['largest_component_pct'] > 50:
                st.success("Echo chamber CONFIRMED: Majority of users share common content!")
            else:
                st.warning("Echo chamber not strongly detected.")

            st.markdown("""
            > **Methodology:** We create a bipartite graph (users ↔ posts), then project
            > it onto users only. Two users are connected if they commented on the same
            > posts. The k-threshold filters weak connections - only users sharing k+
            > posts are linked, revealing true content overlap.
            """)

    # ====================================================================
    # TAB 6: CONCLUSIONS
    # ====================================================================
    with tab6:
        st.subheader("Key Findings & Conclusions")

        st.markdown("---")

        # Finding 1
        st.markdown("### 1. Scale-Free Network Structure")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            The r/WallStreetBets network exhibits clear **scale-free properties** with a
            power-law degree distribution. This means:

            - A small number of "hub" users (like DeepFuckingValue) have disproportionate influence
            - The network is resilient to random user departures but vulnerable to targeted removal of hubs
            - Information can spread rapidly through these well-connected hubs

            **Evidence:** Network centralization of **{results['centralization']:.3f}**
            (vs ~{results['random_centralization']:.3f} for equivalent random network)
            """)
        with col2:
            st.metric("Centralization", f"{results['centralization']:.3f}",
                     delta=f"+{(results['centralization']-results['random_centralization']):.3f} vs random")

        st.markdown("---")

        # Finding 2
        st.markdown("### 2. Key Influencer Impact")
        st.markdown(f"""
        The analysis confirms that **key figures played a catalytic role** in the movement:

        | Key Figure | Role | Impact |
        |------------|------|--------|
        | DeepFuckingValue | Catalyst/Thought Leader | Highest weighted in-degree, started the movement |
        | zjz, Moderators | Information Gatekeepers | High betweenness, controlled information flow |
        | wsbgod, SIR_JACK_A_LOT | Social Proof | Demonstrated large gains, encouraged participation |

        These users form the structural backbone of the network - their removal would
        fragment the community significantly.
        """)

        st.markdown("---")

        # Finding 3
        st.markdown("### 3. Tit-for-Tat Dynamics Explain Coordination")
        tft = results['tft_analysis']
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            The **Tit-for-Tat game theory model** successfully explains how mass coordination
            emerged from individual decisions:

            1. **Initial State:** Only {tft['initial_cooperation']*100:.0f}% of users were "holding"
            2. **Cascade Effect:** Influenced by neighbors (especially key figures), cooperation spread
            3. **Tipping Point:** {'Reached on Day ' + str(tft['tipping_point_day']) if tft['tipping_point_reached'] else 'Not reached'} when majority began holding
            4. **Final State:** {tft['final_cooperation']*100:.0f}% cooperation achieved

            This demonstrates how **social proof** and **network effects** can create
            coordinated action without explicit organization.
            """)
        with col2:
            delta = tft['final_cooperation'] - tft['initial_cooperation']
            st.metric("Cooperation Growth",
                     f"+{delta*100:.0f}%",
                     delta=f"{tft['initial_cooperation']*100:.0f}% → {tft['final_cooperation']*100:.0f}%")

        st.markdown("---")

        # Finding 4
        st.markdown("### 4. Echo Chamber Formation")
        echo = results['echo_analysis']
        st.markdown(f"""
        The bipartite projection analysis reveals a **strong echo chamber effect**:

        - **{echo['largest_component_pct']:.1f}%** of users belong to a single giant component
        - Users share an average of **{echo['mean_shared_posts']:.1f}** posts with their connections
        - This creates a self-reinforcing information environment

        **Implications:**
        - Ideas spread quickly within the echo chamber
        - Contrarian views struggle to gain traction
        - Group polarization intensifies over time
        - Perfect conditions for coordinated action (or coordinated mistakes)
        """)

        st.markdown("---")

        # Finding 5
        st.markdown("### 5. Reed's Law and Exponential Power")
        st.markdown(f"""
        The network's value follows **Reed's Law** (2^N), not just Metcalfe's Law (N²):

        - With {results['stats']['n_nodes']:,} users, the network value is approximately **10^{np.log10(results['network_values']['reed']):.0f}**
        - This exponential growth comes from **group-forming capability**
        - Explains how a Reddit community could challenge institutional investors

        **Key Insight:** The real power of WSB wasn't in individual traders but in their
        ability to form coordinated groups with aligned interests and shared information.
        """)

        st.markdown("---")

        st.subheader("Final Conclusion")
        st.success("""
        **The GameStop short squeeze was a network phenomenon.** The combination of:

        1. **Scale-free structure** (concentrated influence in hubs)
        2. **Key catalysts** (DeepFuckingValue and moderators)
        3. **Tit-for-Tat dynamics** (social proof driving coordination)
        4. **Echo chamber effects** (reinforcing shared beliefs)
        5. **Reed's Law value** (exponential group power)

        Created conditions for unprecedented retail investor coordination. This wasn't
        market manipulation in the traditional sense - it was emergent collective behavior
        arising from network structure and game-theoretic incentives.
        """)

    # ====================================================================
    # TAB 7: METHODOLOGY
    # ====================================================================
    with tab7:
        st.subheader("Methodology & References")

        st.markdown("### Network Construction")
        st.markdown("""
        **Why Barabási-Albert (Scale-Free) Model?**

        We use the Barabási-Albert model to generate our network because real social networks
        like Reddit exhibit **preferential attachment** - new users tend to follow/engage with
        already popular users. This creates the characteristic "power law" degree distribution
        observed in empirical studies of social media.

        **Parameters:**
        - `m = 3`: Each new node attaches to 3 existing nodes
        - Preferential attachment probability proportional to node degree
        - Key figures added with enhanced connectivity to simulate their outsized influence

        **Validation:** The resulting degree distribution matches observed patterns in
        Reddit data, with a small number of highly connected "hubs" and many peripheral users.
        """)

        st.markdown("---")

        st.markdown("### Centrality Measures")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Measure**")
        col2.markdown("**Formula**")
        col3.markdown("**Interpretation**")

        st.markdown("---")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Degree Centrality**")
        col2.latex(r"C_D(v) = \frac{deg(v)}{n-1}")
        col3.markdown("How connected a user is")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Weighted In-Degree**")
        col2.latex(r"\sum_{u \in N(v)} w_{uv}")
        col3.markdown("Total engagement received")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Betweenness Centrality**")
        col2.latex(r"C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}")
        col3.markdown("How often user bridges shortest paths")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Closeness Centrality**")
        col2.latex(r"C_C(v) = \frac{n-1}{\sum_{u} d(v,u)}")
        col3.markdown("How quickly user can reach everyone")

        col1, col2, col3 = st.columns([1.5, 2, 2])
        col1.markdown("**Freeman Centralization**")
        col2.latex(r"C = \frac{\sum(C_{max} - C_i)}{max\_possible}")
        col3.markdown("Overall network concentration")

        st.markdown("---")

        st.markdown("### Game Theory: Tit-for-Tat")
        st.markdown("""
        **The HODL Dilemma:**

        Each user faces a choice similar to the Prisoner's Dilemma:
        - **Cooperate (HOLD):** If everyone holds, price rises, everyone benefits
        - **Defect (SELL):** Individual can profit by selling early, but if many sell, price crashes

        **Tit-for-Tat Strategy:**
        1. Start with cooperation (initial holders + key figures)
        2. Each round, observe neighbors' behavior
        3. If majority of neighbors cooperated last round → cooperate
        4. Otherwise → defect

        **Key Figure Influence:**
        - Influencers' actions weighted 3x more than regular users
        - Simulates their outsized impact on sentiment
        - Creates cascade effect from hubs to periphery

        **Tipping Point:**
        When cooperation exceeds 50%, it becomes self-sustaining as the "majority cooperates"
        condition is met for most users.
        """)

        st.markdown("---")

        st.markdown("### Echo Chamber Detection")
        st.markdown("""
        **Bipartite Projection Method:**

        1. **Create Bipartite Graph:** Users ↔ Posts (edge if user commented on post)
        2. **Matrix Representation:** Users × Posts incidence matrix M
        3. **Projection:** M × M^T = Users × Users matrix (shared posts count)
        4. **K-Filtering:** Only connect users sharing ≥ k posts
        5. **Component Analysis:** Find connected components in filtered graph

        **Echo Chamber Indicator:**
        If the giant component contains >50% of users, they all share common content exposure,
        indicating echo chamber formation.
        """)

        st.markdown("---")

        st.markdown("### Network Value Laws")

        col1, col2, col3 = st.columns([1.5, 1.5, 2])
        col1.markdown("**Law**")
        col2.markdown("**Formula**")
        col3.markdown("**Application**")

        st.markdown("---")

        col1, col2, col3 = st.columns([1.5, 1.5, 2])
        col1.markdown("**Sarnoff's Law**")
        col2.latex(r"V = N")
        col3.markdown("Broadcast networks (TV, radio)")

        col1, col2, col3 = st.columns([1.5, 1.5, 2])
        col1.markdown("**Metcalfe's Law**")
        col2.latex(r"V = N^2")
        col3.markdown("Communication networks (phone, email)")

        col1, col2, col3 = st.columns([1.5, 1.5, 2])
        col1.markdown("**Reed's Law**")
        col2.latex(r"V = 2^N")
        col3.markdown("Group-forming networks (social media)")

        st.markdown("""
        Reed's Law applies to WSB because value comes from:
        - Possible subgroups that can form
        - Coordinated action capability
        - Shared identity and purpose
        """)

        st.markdown("---")

        st.markdown("### References")
        st.markdown("""
        1. **Barabási, A.L. & Albert, R.** (1999). "Emergence of Scaling in Random Networks."
           *Science*, 286(5439), 509-512.

        2. **Metcalfe, R.** (2013). "Metcalfe's Law after 40 Years of Ethernet."
           *IEEE Computer*, 46(12), 26-31.

        3. **Reed, D.P.** (1999). "That Sneaky Exponential—Beyond Metcalfe's Law to the
           Power of Community Building." *Context Magazine*.

        4. **Axelrod, R.** (1984). *The Evolution of Cooperation*. Basic Books.

        5. **Freeman, L.C.** (1978). "Centrality in Social Networks: Conceptual Clarification."
           *Social Networks*, 1(3), 215-239.

        6. **Granovetter, M.** (1978). "Threshold Models of Collective Behavior."
           *American Journal of Sociology*, 83(6), 1420-1443.

        7. **Sunstein, C.R.** (2001). *Echo Chambers: Bush v. Gore, Impeachment, and Beyond*.
           Princeton University Press.
        """)

    # ====================================================================
    # EXPORT SECTION
    # ====================================================================
    st.divider()
    st.subheader("Export Data")

    if using_defaults:
        st.info("Run custom analysis to enable data exports (GEXF network file requires generated graph)")
        col1, col2 = st.columns(2)
        with col1:
            # Can still export pre-computed influencers
            df_export = pd.DataFrame(results['top_influencers'], columns=['User', 'Weighted_In_Degree'])
            csv_data = df_export.to_csv(index=False)
            st.download_button(
                label="Download Influencers (CSV)",
                data=csv_data,
                file_name="top_influencers.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            tft_df = pd.DataFrame({
                'Day': range(1, len(results['cooperation_history']) + 1),
                'Cooperation_Rate': results['cooperation_history']
            })
            tft_csv = tft_df.to_csv(index=False)
            st.download_button(
                label="Download TFT Data (CSV)",
                data=tft_csv,
                file_name="tft_history.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            gexf_data = get_network_gexf(results['G'])
            st.download_button(
                label="Download Network (GEXF)",
                data=gexf_data,
                file_name="gamestop_network.gexf",
                mime="application/gexf+xml",
                use_container_width=True
            )

        with col2:
            top_influencers = get_top_influencers(results['centralities'], n=50)
            df_export = pd.DataFrame(top_influencers, columns=['User', 'Weighted_In_Degree'])
            csv_data = df_export.to_csv(index=False)
            st.download_button(
                label="Download Influencers (CSV)",
                data=csv_data,
                file_name="top_influencers.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col3:
            tft_df = pd.DataFrame({
                'Day': range(1, len(results['cooperation_history']) + 1),
                'Cooperation_Rate': results['cooperation_history']
            })
            tft_csv = tft_df.to_csv(index=False)
            st.download_button(
                label="Download TFT Data (CSV)",
                data=tft_csv,
                file_name="tft_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col4:
            pdf_data = generate_pdf_report(results, params)
            st.download_button(
                label="Download Report (TXT)",
                data=pdf_data,
                file_name="analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )


if __name__ == "__main__":
    main()
