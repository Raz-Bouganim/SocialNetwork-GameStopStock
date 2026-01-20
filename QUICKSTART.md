# Quick Start Guide
## GameStop Short Squeeze - Social Network Analysis

---

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install networkx numpy pandas matplotlib seaborn
```

### Step 2: Run the Analysis

```bash
python gamestop_network_analysis.py
```

### Step 3: View Results

The script will:
1. ✅ Print detailed analysis to console (~5 minutes)
2. ✅ Generate visualizations: `gamestop_network_analysis.png`
3. ✅ Provide comprehensive insights and interpretations

---

## 📊 What You'll Get

### Console Output Includes:

1. **Module 1: Network Construction**
   - Network statistics (nodes, edges, density)
   - Connected components analysis

2. **Module 2: Centrality Analysis**
   - Top 10 most influential users (Degree)
   - Top 10 information bridges (Betweenness)
   - Top 10 fastest spreaders (Closeness)

3. **Module 3: Structure Metrics**
   - Freeman Centralization score
   - Network density interpretation
   - Structure insights

4. **Module 4: Game Theory Simulation**
   - Tit-for-Tat dynamics over 10 days
   - Cooperation rate evolution
   - Tipping point analysis

5. **Module 5: Network Value Laws**
   - Comparison of Sarnoff, Metcalfe, Reed
   - Community detection results
   - Why Reed's Law applies

6. **Module 6: Echo Chamber Detection**
   - Bipartite graph analysis
   - User projection statistics
   - Giant component confirmation

7. **Final Summary Report**
   - Comprehensive findings
   - Key insights
   - Conclusions

### Visualization File Contains:

12 professional-quality plots:
- Network structure sample
- Degree distribution (power law)
- Top influencers ranking
- Information bridges ranking
- Centrality comparison
- TFT evolution graph
- Network value comparison
- Freeman centralization
- Network density
- Bipartite graph sample
- Echo chamber component analysis

---

## 🎯 Understanding the Output

### Key Metrics to Look For:

1. **High In-Degree Users**
   - These are the opinion leaders (e.g., DeepFuckingValue)
   - Look for names in red (known influencers)

2. **High Betweenness Users**
   - These are the information bridges
   - Critical for network cohesion

3. **Freeman Centralization**
   - Score closer to 1 = centralized (leader-driven)
   - Score closer to 0 = decentralized (grassroots)
   - GameStop: ~0.3-0.5 (hybrid model)

4. **TFT Evolution**
   - Watch for tipping point (when cooperation jumps)
   - Final rate shows sustained coordination

5. **Giant Component %**
   - >50% means echo chamber exists
   - GameStop: typically >70%

---

## 🔍 Customization Options

### Modify Network Size

In `gamestop_network_analysis.py`, line ~145:

```python
# Change n_users to analyze different network sizes
G, key_figures = create_scale_free_network(n_users=1000)  # Default: 1000
```

Try:
- `n_users=500` - Faster, less detailed
- `n_users=2000` - Slower, more realistic
- `n_users=100` - Quick test

### Modify TFT Parameters

In the simulation section, around line ~500:

```python
cooperation_history, final_cooperators = simulate_tft_dynamics(
    G, key_figures,
    n_steps=10,              # Change to 5, 15, 20
    initial_cooperators=0.15  # Change to 0.1, 0.2, 0.3
)
```

### Modify Bipartite Graph

Around line ~800:

```python
B, posts = create_bipartite_graph(
    G,
    n_posts=200,        # Change to 100, 500
    key_figures=key_figures
)
```

---

## 📈 Expected Runtime

| Network Size | Runtime | Memory |
|--------------|---------|--------|
| 100 nodes | ~30 sec | <100 MB |
| 500 nodes | ~2 min | <200 MB |
| 1,000 nodes | ~5 min | <500 MB |
| 2,000 nodes | ~15 min | ~1 GB |

*Runtime depends on CPU. Betweenness calculation is the slowest step.*

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'networkx'"

**Solution:**
```bash
pip install networkx
```

### Issue: "Visualization not showing"

**Solution:**
Check for the file `gamestop_network_analysis.png` in the same directory.
Open it with any image viewer.

### Issue: "Memory Error"

**Solution:**
Reduce network size:
```python
G, key_figures = create_scale_free_network(n_users=500)
```

### Issue: "Takes too long"

**Solution:**
The betweenness calculation is O(n³). For faster results:
- Reduce network size
- Or comment out betweenness section (lines ~290-310)

---

## 💡 Quick Interpretation Guide

### Reading the Results

**High Freeman Centralization (>0.6):**
→ Movement was leader-driven (centralized)
→ Few influencers controlled narrative

**Low Freeman Centralization (<0.3):**
→ Movement was grassroots (decentralized)
→ Organic coordination without clear leaders

**High TFT Final Cooperation (>60%):**
→ Social proof mechanisms worked
→ Sustained coordination achieved

**Low TFT Final Cooperation (<30%):**
→ Defection cascades occurred
→ Coordination collapsed

**Giant Component >70%:**
→ Strong echo chamber
→ Information homogenization

**Giant Component <40%:**
→ Fragmented network
→ Multiple isolated groups

---

## 📚 Next Steps

### For Deeper Analysis:

1. **Explore the Data:**
   ```python
   # After running the script, access variables:
   print(G.nodes())  # All users
   print(G.edges(data=True))  # All interactions with weights
   ```

2. **Export to Gephi:**
   ```python
   nx.write_gexf(G, "gamestop_network.gexf")
   ```
   Then open in Gephi for interactive visualization

3. **Statistical Tests:**
   - Compare degree distributions
   - Test for power-law fitting
   - Analyze temporal dynamics

4. **Extended Simulations:**
   - Run TFT for 30+ days
   - Add external shocks (trading halts)
   - Model different starting conditions

---

## 🎓 Educational Use

### For Presentations:

1. Run the script
2. Use the PNG visualization as slides
3. Reference key statistics from console output
4. Explain each module with real GameStop events

### For Reports:

1. Copy summary report from console
2. Include visualizations
3. Reference specific metrics
4. Connect to course concepts

### For Further Research:

1. Modify parameters to test hypotheses
2. Compare to other social movements
3. Validate against real Reddit data (if available)
4. Extend with sentiment analysis

---

## 📞 Getting Help

### Common Questions:

**Q: Is this real Reddit data?**
A: No, it's a statistically representative simulation based on known entities and realistic network properties.

**Q: Can I use different influencers?**
A: Yes! Edit the `key_figures` list in the code (line ~150).

**Q: How accurate is the model?**
A: The network structure and dynamics are based on well-established models (Barabási-Albert, TFT). While specific numbers are simulated, the patterns and insights are valid.

**Q: Can I analyze other events?**
A: Yes! The framework is general. Just modify the key figures and context.

---

## 🎯 Success Checklist

After running, you should have:

- ✅ Console output with all 6 modules
- ✅ PNG file with 12 visualizations
- ✅ Understanding of network structure
- ✅ Identification of key influencers
- ✅ Game theory insights
- ✅ Network value analysis
- ✅ Echo chamber confirmation
- ✅ Final summary report

---

## 🚀 Ready to Go!

```bash
# One command to rule them all:
python gamestop_network_analysis.py
```

**Estimated time:** 5 minutes
**Output:** Comprehensive analysis + visualizations
**Difficulty:** Just run it! 😊

---

*For detailed methodology, see [README.md](README.md)*
*For technical details, see code comments in the Python file*

**Happy Analyzing! 🚀📈**
