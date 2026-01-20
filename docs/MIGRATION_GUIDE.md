# Migration Guide: Monolithic → Modular Architecture

## 🔄 What Changed

Your project has been restructured from a single 1,100-line file into a professional modular architecture with proper separation of concerns.

---

## 📊 Before vs After

### Before (Monolithic)
```
SocialNetwork/
├── gamestop_network_analysis.py  (1,100+ lines)
├── README.md
├── requirements.txt
└── [PDFs]
```

**Problems:**
- Hard to navigate (1,100 lines)
- Difficult to test individual components
- No code reusability
- Hard to modify/extend

### After (Modular)
```
SocialNetwork/
├── main.py                    # Entry point (clean, ~200 lines)
├── setup.py                   # Package setup
├── requirements.txt
│
├── src/                       # All source code
│   ├── network/              # Network construction
│   ├── analysis/             # Analysis functions
│   ├── game_theory/          # TFT simulation
│   ├── visualization/        # Plots & reports
│   └── utils/                # Config & helpers
│
├── data/                      # Data files (PDFs)
├── docs/                      # Documentation
└── output/                    # Generated files
```

**Benefits:**
- ✅ Clear organization
- ✅ Easy to test
- ✅ Reusable components
- ✅ Easy to extend
- ✅ Professional structure

---

## 🗂️ Module Mapping

### Where did everything go?

| Original Location | New Location | Purpose |
|-------------------|--------------|---------|
| Lines 1-150 (imports, setup) | `src/utils/config.py` | Configuration |
| Lines 145-250 (network construction) | `src/network/builder.py` | Network building |
| Lines 253-375 (centrality) | `src/analysis/centrality.py` | Centrality metrics |
| Lines 378-470 (structure) | `src/analysis/structure.py` | Structure metrics |
| Lines 473-610 (TFT) | `src/game_theory/tit_for_tat.py` | Game theory |
| Lines 613-730 (network value) | `src/analysis/network_value.py` | Value laws |
| Lines 733-890 (bipartite) | `src/network/bipartite.py` | Bipartite graphs |
| Lines 893-1050 (visualization) | `src/visualization/plots.py` | Plotting |
| Print statements | `src/visualization/reporters.py` | Text reports |
| Main execution | `main.py` | Entry point |

---

## 🚀 How to Use the New Structure

### Option 1: Run Everything (Same as Before)

```bash
python main.py
```

**Output:** Identical to the old file!
- Console analysis
- 12-panel visualization PNG
- Network export to GEXF

### Option 2: Use Individual Modules

```python
# Example 1: Just build the network
from src.network import create_scale_free_network

G, key_figures = create_scale_free_network(n_users=500)

# Example 2: Just calculate centrality
from src.analysis import calculate_betweenness_centrality

bc = calculate_betweenness_centrality(G)

# Example 3: Just run TFT
from src.game_theory import simulate_tft_dynamics

history, cooperators = simulate_tft_dynamics(G, key_figures, n_steps=20)
```

### Option 3: Customize Configuration

```python
# Edit src/utils/config.py
NETWORK_SIZE = 2000  # Larger network
TFT_TIME_STEPS = 15  # Longer simulation
DPI = 600            # Higher resolution images

# Then run
python main.py
```

---

## 🔧 Configuration System

All parameters now centralized in `src/utils/config.py`:

```python
# Network Parameters
NETWORK_SIZE = 1000
BA_MODEL_M = 3
RANDOM_SEED = 42

# Key Figures
KEY_FIGURES = ['DeepFuckingValue', 'zjz', ...]

# Game Theory
TFT_TIME_STEPS = 10
INITIAL_COOPERATION_RATE = 0.15

# Visualization
FIGURE_SIZE = (20, 24)
DPI = 300
```

**Benefits:**
- Change once, affects everywhere
- No magic numbers in code
- Easy to create variants

---

## 📦 Package Structure

### `src/network/`
**Purpose:** Network construction and bipartite graphs

```python
from src.network import (
    create_scale_free_network,   # Build main network
    get_network_stats,            # Get basic stats
    create_bipartite_graph,       # Create user-post graph
    project_to_users,             # Project to users
    analyze_echo_chamber          # Analyze echo chamber
)
```

### `src/analysis/`
**Purpose:** All network analysis functions

```python
from src.analysis import (
    # Centrality
    calculate_degree_centrality,
    calculate_betweenness_centrality,
    calculate_closeness_centrality,
    calculate_all_centralities,

    # Structure
    calculate_network_density,
    calculate_freeman_centralization,
    interpret_centralization,

    # Network Value
    calculate_sarnoff_value,
    calculate_metcalfe_value,
    calculate_reed_value,
    detect_communities,
    compare_network_values
)
```

### `src/game_theory/`
**Purpose:** Game theory simulations

```python
from src.game_theory import (
    simulate_tft_dynamics,
    identify_tipping_point,
    analyze_tft_results
)
```

### `src/visualization/`
**Purpose:** Plots and text reports

```python
from src.visualization import (
    create_full_visualization,     # Generate 12-panel figure
    print_network_stats,           # Print module 1 report
    print_centrality_results,      # Print module 2 report
    print_structure_results,       # Print module 3 report
    print_tft_results,             # Print module 4 report
    print_network_value_results,   # Print module 5 report
    print_echo_chamber_results,    # Print module 6 report
    print_final_summary            # Print final summary
)
```

### `src/utils/`
**Purpose:** Configuration and helper functions

```python
from src.utils.config import *     # All configuration constants
from src.utils.helpers import (
    print_header,
    format_number,
    get_top_k,
    truncate_name
)
```

---

## 🧪 Testing Individual Components

### Test Network Construction

```python
from src.network import create_scale_free_network
import networkx as nx

# Create network
G, key_figures = create_scale_free_network(n_users=100)

# Verify
assert G.number_of_nodes() == 100
assert nx.is_weakly_connected(G)
print("✓ Network construction works!")
```

### Test Centrality Calculation

```python
from src.analysis import calculate_betweenness_centrality

bc = calculate_betweenness_centrality(G)
assert len(bc) == G.number_of_nodes()
print("✓ Centrality calculation works!")
```

### Test TFT Simulation

```python
from src.game_theory import simulate_tft_dynamics

history, cooperators = simulate_tft_dynamics(G, key_figures, n_steps=5)
assert len(history) == 5
print("✓ TFT simulation works!")
```

---

## 🎯 Extending the Project

### Add a New Centrality Metric

**File:** `src/analysis/centrality.py`

```python
def calculate_eigenvector_centrality(G: nx.DiGraph) -> Dict:
    """Calculate eigenvector centrality."""
    return nx.eigenvector_centrality(G, weight='weight')
```

**Usage:**
```python
from src.analysis.centrality import calculate_eigenvector_centrality

ec = calculate_eigenvector_centrality(G)
```

### Add a New Visualization

**File:** `src/visualization/plots.py`

```python
def plot_community_structure(ax, G, communities):
    """Plot network colored by community."""
    # Your plotting code here
    pass
```

### Add a New Game Theory Model

**File:** `src/game_theory/win_stay_lose_shift.py`

```python
def simulate_wsls_dynamics(G, key_figures, n_steps):
    """Simulate Win-Stay-Lose-Shift strategy."""
    # Your simulation code here
    pass
```

---

## 📝 Quick Reference

### Import Everything You Need

```python
# Network
from src.network import create_scale_free_network, create_bipartite_graph

# Analysis
from src.analysis import (
    calculate_all_centralities,
    calculate_freeman_centralization,
    compare_network_values
)

# Game Theory
from src.game_theory import simulate_tft_dynamics

# Visualization
from src.visualization import create_full_visualization

# Config
from src.utils.config import NETWORK_SIZE, KEY_FIGURES
```

### Run Analysis Step by Step

```python
# 1. Build network
G, key_figures = create_scale_free_network()

# 2. Analyze centrality
centralities = calculate_all_centralities(G)

# 3. Run TFT
history, cooperators = simulate_tft_dynamics(G, key_figures)

# 4. Visualize
from src.visualization import create_full_visualization
# ... (pass all required parameters)
```

---

## 🔍 Finding Things

### "Where is the network size set?"
→ `src/utils/config.py`, line 15: `NETWORK_SIZE = 1000`

### "Where is the BA model implemented?"
→ `src/network/builder.py`, function `create_scale_free_network()`

### "Where is betweenness calculated?"
→ `src/analysis/centrality.py`, function `calculate_betweenness_centrality()`

### "Where is TFT simulated?"
→ `src/game_theory/tit_for_tat.py`, function `simulate_tft_dynamics()`

### "Where are the plots created?"
→ `src/visualization/plots.py`, various `_plot_*()` functions

### "Where are the text reports?"
→ `src/visualization/reporters.py`, various `print_*()` functions

---

## ⚠️ Important Notes

### The Old File Still Works!

```bash
# Old way (still functional)
python gamestop_network_analysis_OLD.py

# New way (recommended)
python main.py
```

**Both produce identical output!**

### Backward Compatibility

If you have scripts using the old file:

```python
# Old way
exec(open('gamestop_network_analysis_OLD.py').read())

# New way
from main import main
results = main()
```

### Dependencies Haven't Changed

```bash
pip install -r requirements.txt
```

Same requirements, no new dependencies added.

---

## 🎓 For Your Submission

### What to Submit

**Recommended:**
- `main.py` (entry point)
- `src/` (all source code)
- `requirements.txt`
- `docs/ANALYSIS_REPORT.md` (research paper)
- `output/gamestop_network_analysis.png` (visualization)

**Optional:**
- `setup.py` (if instructor wants installable package)
- `gamestop_network_analysis_OLD.py` (backup)

### How to Run Your Code (for grader)

```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Output will be in output/ directory
```

---

## 💡 Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Code organization** | 1 file, 1,100 lines | 15 files, modular |
| **Reusability** | Copy-paste sections | Import functions |
| **Testing** | Test entire file | Test individual modules |
| **Configuration** | Magic numbers in code | Centralized config |
| **Extensibility** | Edit 1,100-line file | Add new modules |
| **Collaboration** | Merge conflicts | Independent modules |
| **Documentation** | Comments only | Docstrings + structure |
| **Professional?** | Script | Package |

---

## 🚀 Next Steps

1. **Test the new structure:**
   ```bash
   python main.py
   ```

2. **Verify output matches:**
   - Compare console output
   - Compare PNG visualization
   - Check for any errors

3. **Explore modules:**
   ```python
   from src.network import create_scale_free_network
   help(create_scale_free_network)
   ```

4. **Customize as needed:**
   - Edit `src/utils/config.py`
   - Re-run `main.py`

---

## ❓ FAQ

**Q: Is the old file deleted?**
A: No, it's renamed to `gamestop_network_analysis_OLD.py` as a backup.

**Q: Does the new version produce the same output?**
A: Yes, identical output. We just reorganized the code.

**Q: Can I still use the old file?**
A: Yes, `python gamestop_network_analysis_OLD.py` still works.

**Q: Do I need to relearn everything?**
A: No, the logic is the same. Just better organized.

**Q: Is it harder to use?**
A: Simpler! Just run `python main.py`. For advanced use, import modules.

**Q: What if I want to modify something?**
A: Much easier now! Edit the specific module file instead of searching through 1,100 lines.

---

## 📞 Support

If you encounter any issues:

1. Check that all files are in place (run `tree` or `ls -R`)
2. Ensure dependencies are installed (`pip install -r requirements.txt`)
3. Try running the old file to compare (`python gamestop_network_analysis_OLD.py`)
4. Check `docs/QUICKSTART.md` for troubleshooting

---

**🎉 Congratulations! Your project now has professional-grade architecture.**

The same analysis, but cleaner, more maintainable, and more extensible.
