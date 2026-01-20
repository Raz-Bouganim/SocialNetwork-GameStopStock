# 📂 Complete Project Structure

## Directory Tree

```
SocialNetwork/
│
├── 📄 main.py                              # Main entry point (Run this!)
├── 📄 setup.py                             # Package installation script
├── 📄 requirements.txt                     # Python dependencies
├── 📄 .gitignore                           # Git ignore rules
├── 📄 README.md                            # Main documentation (You are here!)
├── 📄 MIGRATION_GUIDE.md                   # How we restructured the code
├── 📄 PROJECT_STRUCTURE.md                 # This file
│
├── 📄 gamestop_network_analysis_OLD.py     # Backup of original monolithic file
│
├── 📁 src/                                 # Source code (modular architecture)
│   ├── 📄 __init__.py                      # Package initialization
│   │
│   ├── 📁 utils/                           # Utilities
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py                    # Central configuration (ALL constants here!)
│   │   └── 📄 helpers.py                   # Helper functions
│   │
│   ├── 📁 network/                         # Network construction
│   │   ├── 📄 __init__.py
│   │   ├── 📄 builder.py                   # Scale-free network builder (BA model)
│   │   └── 📄 bipartite.py                 # Bipartite graph & projection
│   │
│   ├── 📁 analysis/                        # Network analysis
│   │   ├── 📄 __init__.py
│   │   ├── 📄 centrality.py                # Centrality metrics (Degree, BC, CC)
│   │   ├── 📄 structure.py                 # Structure metrics (Density, Freeman)
│   │   └── 📄 network_value.py             # Network value laws (Sarnoff/Metcalfe/Reed)
│   │
│   ├── 📁 game_theory/                     # Game theory simulation
│   │   ├── 📄 __init__.py
│   │   └── 📄 tit_for_tat.py               # TFT simulation & analysis
│   │
│   └── 📁 visualization/                   # Visualization & reporting
│       ├── 📄 __init__.py
│       ├── 📄 plots.py                     # Plot generation (12-panel figure)
│       └── 📄 reporters.py                 # Text report generation
│
├── 📁 data/                                # Data files
│   ├── 📄 Reddit-GameStop-2021.pdf         # Reference PDF (English)
│   └── 📄 [Hebrew PDF]                     # Reference PDF (Hebrew)
│
├── 📁 docs/                                # Documentation
│   ├── 📄 README.md                        # Full project documentation (~6k words)
│   ├── 📄 QUICKSTART.md                    # 5-minute getting started guide
│   ├── 📄 ANALYSIS_REPORT.md               # Academic research paper (~12k words)
│   └── 📄 PROJECT_SUMMARY.md               # Delivery summary
│
└── 📁 output/                              # Generated outputs
    ├── 📄 .gitkeep                         # Keep directory in version control
    ├── 🖼️ gamestop_network_analysis.png    # (Generated) 12-panel visualization
    └── 📊 gamestop_network.gexf            # (Generated) Network export for Gephi
```

---

## 📊 File Statistics

| Category | Count | Total Lines |
|----------|-------|-------------|
| Python source files | 18 | ~2,500 |
| Documentation files | 6 | ~30,000 words |
| Data files | 2 | 3.2 MB |
| Configuration files | 3 | ~150 |
| **Total** | **29** | **~2,650 lines + 30k words** |

---

## 🎯 Module Responsibilities

### 🔧 `src/utils/` - Utilities & Configuration
**Purpose:** Centralized configuration and helper functions

| File | Lines | Exports | Purpose |
|------|-------|---------|---------|
| `config.py` | ~90 | 30+ constants | All configuration parameters |
| `helpers.py` | ~50 | 7 functions | Print formatting, number formatting, etc. |

**Key Constants:**
- `NETWORK_SIZE` = 1000
- `KEY_FIGURES` = ['DeepFuckingValue', ...]
- `TFT_TIME_STEPS` = 10
- `FIGURE_SIZE` = (20, 24)

---

### 🕸️ `src/network/` - Network Construction
**Purpose:** Build and manage network graphs

| File | Lines | Functions | Purpose |
|------|-------|-----------|---------|
| `builder.py` | ~180 | 4 public, 2 private | Create scale-free network |
| `bipartite.py` | ~150 | 3 public | Bipartite graph & projection |

**Main Functions:**
- `create_scale_free_network()` → Returns directed weighted graph
- `create_bipartite_graph()` → Returns user-post bipartite graph
- `project_to_users()` → Returns user projection
- `analyze_echo_chamber()` → Returns analysis dict

---

### 📊 `src/analysis/` - Network Analysis
**Purpose:** Calculate network metrics and properties

| File | Lines | Functions | Purpose |
|------|-------|-----------|---------|
| `centrality.py` | ~110 | 4 functions | Degree, betweenness, closeness |
| `structure.py` | ~120 | 5 functions | Density, centralization, power law |
| `network_value.py` | ~100 | 5 functions | Sarnoff, Metcalfe, Reed laws |

**Main Metrics:**
- **Centrality:** Degree, Betweenness, Closeness
- **Structure:** Density, Freeman Centralization
- **Value:** Network value laws, community detection

---

### 🎮 `src/game_theory/` - Game Theory
**Purpose:** Simulate strategic interactions

| File | Lines | Functions | Purpose |
|------|-------|-----------|---------|
| `tit_for_tat.py` | ~160 | 4 functions | TFT simulation & analysis |

**Main Functions:**
- `simulate_tft_dynamics()` → Returns cooperation history
- `analyze_tft_results()` → Returns analysis dict
- `identify_tipping_point()` → Returns day number

---

### 📈 `src/visualization/` - Visualization & Reporting
**Purpose:** Create plots and generate reports

| File | Lines | Functions | Purpose |
|------|-------|-----------|---------|
| `plots.py` | ~480 | 14 functions | 12-panel visualization + helpers |
| `reporters.py` | ~200 | 7 functions | Console text reports |

**Main Outputs:**
- **Visual:** 12-panel comprehensive figure (PNG)
- **Text:** Module-by-module console reports
- **Export:** GEXF file for Gephi

---

## 🔄 Data Flow

```
1. Configuration (src/utils/config.py)
   │
   ↓
2. Network Construction (src/network/builder.py)
   │
   ↓
3. Analysis Branch A: Centrality (src/analysis/centrality.py)
   │
   ↓
4. Analysis Branch B: Structure (src/analysis/structure.py)
   │
   ↓
5. Analysis Branch C: Network Value (src/analysis/network_value.py)
   │
   ↓
6. Game Theory Simulation (src/game_theory/tit_for_tat.py)
   │
   ↓
7. Bipartite Graph & Echo Chamber (src/network/bipartite.py)
   │
   ↓
8. Visualization (src/visualization/plots.py)
   │
   ↓
9. Text Reports (src/visualization/reporters.py)
   │
   ↓
10. Output (output/*.png, output/*.gexf)
```

---

## 🎨 Visualization Pipeline

```
create_full_visualization()
  │
  ├── _plot_network_sample()           → Panel 1: Network graph
  ├── _plot_degree_distribution()      → Panel 2: Degree histogram
  ├── _plot_degree_loglog()            → Panel 3: Power law confirmation
  ├── _plot_top_influencers()          → Panel 4: Top 20 in-degree
  ├── _plot_top_betweenness()          → Panel 5: Top 20 betweenness
  ├── _plot_centrality_comparison()    → Panel 6: Multi-metric comparison
  ├── _plot_tft_evolution()            → Panel 7: TFT cooperation over time
  ├── _plot_value_comparison()         → Panel 8: Sarnoff/Metcalfe/Reed
  ├── _plot_freeman_centralization()   → Panel 9: Centralization score
  ├── _plot_network_density()          → Panel 10: Density visualization
  ├── _plot_bipartite_info()           → Panel 11: Bipartite stats
  └── _plot_component_sizes()          → Panel 12: Echo chamber components
```

---

## 📝 Import Patterns

### Basic Usage
```python
from src.network import create_scale_free_network
from src.analysis import calculate_all_centralities
from src.game_theory import simulate_tft_dynamics
```

### Advanced Usage
```python
# Specific centrality metrics
from src.analysis import (
    calculate_betweenness_centrality,
    calculate_closeness_centrality
)

# Network value laws
from src.analysis import (
    calculate_reed_value,
    detect_communities
)

# Custom configuration
from src.utils.config import NETWORK_SIZE, KEY_FIGURES
```

### Full Import
```python
# Import everything from a module
from src.analysis import *  # All analysis functions
from src.visualization import *  # All viz functions
```

---

## 🔍 Quick Navigation

### "I want to change network size"
→ **File:** `src/utils/config.py`
→ **Line:** 15
→ **Variable:** `NETWORK_SIZE = 1000`

### "I want to add a new key figure"
→ **File:** `src/utils/config.py`
→ **Line:** 20-30
→ **List:** `KEY_FIGURES = [...]`

### "I want to modify TFT parameters"
→ **File:** `src/utils/config.py`
→ **Line:** 40-45
→ **Variables:** `TFT_TIME_STEPS`, `INITIAL_COOPERATION_RATE`, etc.

### "I want to add a new centrality metric"
→ **File:** `src/analysis/centrality.py`
→ **Add:** New function following existing pattern

### "I want to add a new visualization"
→ **File:** `src/visualization/plots.py`
→ **Add:** New `_plot_*()` function

### "I want to change visualization DPI"
→ **File:** `src/utils/config.py`
→ **Line:** 60
→ **Variable:** `DPI = 300`

---

## 🧪 Testing Individual Modules

```python
# Test network construction
from src.network import create_scale_free_network
G, key_figures = create_scale_free_network(n_users=100)
assert G.number_of_nodes() == 100

# Test centrality
from src.analysis import calculate_betweenness_centrality
bc = calculate_betweenness_centrality(G)
assert len(bc) == 100

# Test TFT
from src.game_theory import simulate_tft_dynamics
history, _ = simulate_tft_dynamics(G, key_figures, n_steps=5)
assert len(history) == 5

print("✅ All tests passed!")
```

---

## 📦 Package Installation

```bash
# Development mode (editable install)
pip install -e .

# Then use anywhere:
from src.network import create_scale_free_network
```

---

## 🎓 For Submission

### Minimal Submission
```
SocialNetwork/
├── main.py
├── requirements.txt
├── src/  (entire directory)
└── docs/ANALYSIS_REPORT.md
```

### Complete Submission
```
SocialNetwork/  (entire project directory)
```

### How to Run (for grader)
```bash
pip install -r requirements.txt
python main.py
# Output appears in output/ directory
```

---

## 📊 Complexity Comparison

| Aspect | Monolithic (OLD) | Modular (NEW) |
|--------|------------------|---------------|
| **Total lines** | 1,100 in 1 file | ~2,500 in 18 files |
| **Longest file** | 1,100 lines | ~480 lines |
| **Average file** | 1,100 lines | ~140 lines |
| **Reusability** | 0% | 100% |
| **Testability** | Hard | Easy |
| **Maintainability** | Low | High |
| **Extensibility** | Difficult | Easy |
| **Professional** | Script | Package |

---

## 💡 Key Advantages

### 1. Separation of Concerns
Each module has a single, clear responsibility

### 2. Reusability
Import any function independently:
```python
from src.analysis import calculate_betweenness_centrality
bc = calculate_betweenness_centrality(my_graph)
```

### 3. Testability
Test each module in isolation:
```python
import pytest
from src.network import create_scale_free_network

def test_network_size():
    G, _ = create_scale_free_network(n_users=100)
    assert G.number_of_nodes() == 100
```

### 4. Maintainability
Modify one module without affecting others

### 5. Extensibility
Add new modules easily:
```
src/
└── sentiment_analysis/  (new module!)
    ├── __init__.py
    └── analyzer.py
```

### 6. Configuration Management
All constants in one place (`config.py`)

### 7. Professional Structure
Industry-standard package layout

---

## 🚀 Future Enhancements

Easy to add:

1. **New centrality metrics** → Add to `src/analysis/centrality.py`
2. **New game theory models** → Add to `src/game_theory/`
3. **Temporal network analysis** → Add new module `src/temporal/`
4. **Sentiment analysis** → Add new module `src/sentiment/`
5. **Alternative visualizations** → Add to `src/visualization/plots.py`
6. **Interactive plots** → Use Plotly, add to new file
7. **Unit tests** → Create `tests/` directory
8. **CI/CD** → Add `.github/workflows/`

---

## 📖 Documentation Structure

```
docs/
├── README.md               # Full documentation (methodology, results)
├── QUICKSTART.md          # 5-minute setup guide
├── ANALYSIS_REPORT.md     # Academic paper (~12,000 words)
└── PROJECT_SUMMARY.md     # Delivery overview
```

Plus root-level guides:
```
MIGRATION_GUIDE.md         # How we restructured
PROJECT_STRUCTURE.md       # This file
```

---

## 🎉 Summary

You now have a **professional, modular, maintainable** social network analysis package that:

- ✅ Separates concerns into logical modules
- ✅ Centralizes configuration
- ✅ Enables code reuse
- ✅ Facilitates testing
- ✅ Supports extensibility
- ✅ Follows industry best practices
- ✅ Produces identical output to the original

**Same analysis. Better structure. Professional quality.**

---

**Last Updated:** December 2025
**Authors:** Raz Bouganim, Omer Katz, Ohad Cohen
**Course:** Social Network Analysis
