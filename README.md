# GameStop (2021) Social Network Analysis

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Academic-green)](LICENSE)

A comprehensive social network analysis of the 2021 GameStop short squeeze on r/WallStreetBets, demonstrating how network structure, centrality metrics, and game theory dynamics enabled unprecedented retail investor coordination.

**Authors:** Raz Bouganim, Omer Katz, Ohad Cohen
**Course:** Social Network Analysis
**Date:** December 2025

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis (generates visualizations + console report)
python main.py
```

**Output:** Console analysis (~5 min) + `output/gamestop_network_analysis.png`

---

## 📁 Project Structure

```
SocialNetwork/
│
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
│
├── src/                             # Source code (modular architecture)
│   ├── __init__.py
│   │
│   ├── utils/                       # Utilities and configuration
│   │   ├── config.py                # Central configuration
│   │   ├── helpers.py               # Helper functions
│   │   └── __init__.py
│   │
│   ├── network/                     # Network construction
│   │   ├── builder.py               # Scale-free network builder
│   │   ├── bipartite.py             # Bipartite graph & projection
│   │   └── __init__.py
│   │
│   ├── analysis/                    # Network analysis
│   │   ├── centrality.py            # Centrality metrics
│   │   ├── structure.py             # Structure metrics
│   │   ├── network_value.py         # Network value laws
│   │   └── __init__.py
│   │
│   ├── game_theory/                 # Game theory simulation
│   │   ├── tit_for_tat.py           # TFT simulation
│   │   └── __init__.py
│   │
│   └── visualization/               # Visualization & reporting
│       ├── plots.py                 # Plot generation
│       ├── reporters.py             # Text reports
│       └── __init__.py
│
├── data/                            # Data files
│   ├── Reddit-GameStop-2021.pdf     # Reference PDF (English)
│   └── [Hebrew PDF]                 # Reference PDF (Hebrew)
│
├── docs/                            # Documentation
│   ├── README.md                    # Full project documentation
│   ├── QUICKSTART.md                # 5-minute getting started guide
│   ├── ANALYSIS_REPORT.md           # Academic research paper (~12k words)
│   └── PROJECT_SUMMARY.md           # Delivery summary
│
└── output/                          # Generated outputs
    ├── gamestop_network_analysis.png  # 12-panel visualization
    └── gamestop_network.gexf          # Network export (for Gephi)
```

---

## 🎯 Modules Overview

### Module 1: Network Construction
- **File:** `src/network/builder.py`
- **Function:** Creates 1,000-user scale-free network using Barabási-Albert model
- **Features:** Power-law distribution, weighted edges, real key figures

### Module 2: Centrality Analysis
- **File:** `src/analysis/centrality.py`
- **Metrics:** Degree, Betweenness, Closeness
- **Output:** Top 10 rankings for each metric

### Module 3: Structure Metrics
- **File:** `src/analysis/structure.py`
- **Metrics:** Network density, Freeman centralization
- **Insight:** Hybrid structure (leadership + resilience)

### Module 4: Game Theory (TFT)
- **File:** `src/game_theory/tit_for_tat.py`
- **Model:** Spatial Tit-for-Tat on network
- **Output:** Cooperation evolution over 10 days

### Module 5: Network Value
- **File:** `src/analysis/network_value.py`
- **Laws:** Sarnoff (N), Metcalfe (N²), Reed (2^N)
- **Result:** Reed's Law applies (group-forming power)

### Module 6: Echo Chamber
- **File:** `src/network/bipartite.py`
- **Method:** User-Post bipartite projection
- **Result:** 96.7% giant component (massive echo chamber)

---

## 🔧 Configuration

Edit `src/utils/config.py` to customize:

```python
# Network size
NETWORK_SIZE = 1000  # Change to 500, 2000, etc.

# Game theory parameters
TFT_TIME_STEPS = 10
INITIAL_COOPERATION_RATE = 0.15

# Visualization
DPI = 300
FIGURE_SIZE = (20, 24)
```

---

## 📊 Key Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Network Density | 0.003 | Loose but connected |
| Freeman Centralization | 0.42 | Hybrid structure |
| TFT Tipping Point | Day 5 | Cooperation crossed 50% |
| Final Cooperation | 79.5% | Sustained coordination |
| Giant Component | 96.7% | Massive echo chamber |
| Network Value | Reed > Metcalfe | Exponential advantage |

---

## 📖 Documentation

- **[Full Documentation](docs/README.md)** - Complete methodology and results
- **[Quick Start](docs/QUICKSTART.md)** - 5-minute setup guide
- **[Research Report](docs/ANALYSIS_REPORT.md)** - Academic paper format
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Delivery overview

---

## 🎓 Academic Use

### For Your Submission:
1. **Code:** `main.py` + `src/` directory
2. **Report:** `docs/ANALYSIS_REPORT.md`
3. **Visualization:** `output/gamestop_network_analysis.png`

### For Your Presentation:
- Run `python main.py`
- Use generated PNG as slides
- Reference console output statistics

---

## 🛠️ Advanced Usage

### Export to Gephi
```python
import networkx as nx
from src.network import create_scale_free_network

G, _ = create_scale_free_network()
nx.write_gexf(G, "output/network.gexf")
```

### Customize Analysis
```python
from src.analysis import calculate_betweenness_centrality

# Custom betweenness calculation
bc = calculate_betweenness_centrality(G, weight=None)  # Unweighted
```

### Run Specific Modules
```python
from src.game_theory import simulate_tft_dynamics

# Longer simulation
history, cooperators = simulate_tft_dynamics(G, key_figures, n_steps=20)
```

---

## 📦 Dependencies

- **Core:** NetworkX, NumPy, Pandas
- **Visualization:** Matplotlib, Seaborn
- **Optional:** python-louvain (community detection)

Install all: `pip install -r requirements.txt`

---

## 🔬 Methodology

### Data Construction
Since complete Reddit data is unavailable, we use:
- **Real entities:** DeepFuckingValue, known moderators
- **Statistically valid model:** Barabási-Albert for scale-free properties
- **Validation:** Power-law distribution confirmed

### Network Properties
- Scale-free topology ✓
- Power-law degree distribution ✓
- Small-world properties ✓
- Hybrid centralization ✓

---

## 💡 Key Insights

1. **Network Structure Enabled Coordination**
   - Hybrid centralization (0.42) balanced leadership and resilience
   - Small-world properties enabled rapid spread

2. **TFT Solved Collective Action**
   - Tipping point on day 5 (50%+ cooperation)
   - Digital reputation systems implemented TFT

3. **Reed's Law Explains Power**
   - Group-forming capability (2^N) beat hierarchies (N²)
   - 47 sub-communities detected

4. **Echo Chamber Was Functional**
   - 96.7% in giant component
   - Information homogenization prevented defection

---

## 📞 Support

For questions or issues:
- Check `docs/QUICKSTART.md` troubleshooting
- Review code comments (extensive documentation)
- See `docs/ANALYSIS_REPORT.md` for methodology

---

## 📜 License

Academic use only. Created for university coursework.

---

## 🙏 Acknowledgments

- Course instructor for guidance
- r/WallStreetBets community for the phenomenon
- NetworkX developers
- Network science community

---

**"In January 2021, Reddit proved that when network structure is optimal, coordination beats capital."**

*Analysis completed: December 2025*
