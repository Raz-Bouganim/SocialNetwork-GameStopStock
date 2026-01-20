"""
Configuration and Constants
============================

Central configuration file for the GameStop network analysis.
"""

# Network Parameters
NETWORK_SIZE = 1000  # Number of users in the network
BA_MODEL_M = 3  # Number of edges to attach from new node (Barabási-Albert)
RANDOM_SEED = 42  # For reproducibility

# Known Key Figures (Real entities from GameStop saga)
KEY_FIGURES = [
    'DeepFuckingValue',      # Keith Gill - The catalyst
    'zjz',                    # WSB Moderator
    'OPINION_IS_UNPOPULAR',  # WSB Moderator
    'Stylux',                 # WSB Moderator
    'bawse1',                 # WSB Moderator
    'ITradeBaconFutures',    # WSB Moderator
    'VisualMod',             # Bot account
    'AutoModerator',         # Bot account
    'wsbgod',                # Influential trader
    'SIR_JACK_A_LOT'         # Influential trader
]

# Influencer Connection Parameters
INFLUENCER_MIN_CONNECTIONS = 50
INFLUENCER_MAX_CONNECTIONS = 200
DFV_CONNECTIONS = 300  # DeepFuckingValue had the most
PREFERENTIAL_RATIO = 0.7  # 70% connect to high-degree nodes

# Edge Weight Parameters
MIN_WEIGHT = 1
MAX_WEIGHT_REGULAR = 20
MAX_WEIGHT_TO_INFLUENCER = 50
MIN_WEIGHT_FROM_INFLUENCER = 1
MAX_WEIGHT_FROM_INFLUENCER = 10
REPLY_PROBABILITY = 0.7  # Probability of bidirectional edge

# Game Theory Parameters
TFT_TIME_STEPS = 10
INITIAL_COOPERATION_RATE = 0.15
INFLUENCER_WEIGHT_MULTIPLIER = 3
COOPERATION_THRESHOLD = 0.5
STICKY_THRESHOLD = 0.4

# Bipartite Graph Parameters
NUM_POSTS = 200
VIRAL_POST_RATIO = 0.7  # 70% of comments on viral posts
K_THRESHOLD = 2  # Minimum shared posts to create edge in projection

# Visualization Parameters
FIGURE_SIZE = (20, 24)
DPI = 300
SAMPLE_SIZE_NETWORK = 100  # For network visualization
NODE_SIZE_INFLUENCER = 500
NODE_SIZE_REGULAR = 50
COLOR_INFLUENCER = 'red'
COLOR_REGULAR = 'lightblue'

# Output Paths
OUTPUT_DIR = 'output'
VISUALIZATION_FILENAME = 'gamestop_network_analysis.png'
NETWORK_EXPORT_FILENAME = 'gamestop_network.gexf'

# Display Settings
PRINT_WIDTH = 80
