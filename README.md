#  A/B Test Analysis: Conversation Scripts Optimization

Statistical analysis of A/B test comparing two conversation scripts for robotic debt collection calls.

---

##  Business Problem

In robotic debt collection, the **conversation script** directly impacts success rates. We need to determine:
- Does the new script perform better than the current one?
- Is the difference **statistically significant**?
- Should we roll out the new script to production?

**Cost of wrong decision:**
-  False positive → Implement worse script → Lost revenue
-  False negative → Miss improvement opportunity → Lost revenue

**Solution:** Rigorous A/B test with statistical validation.

---

##  Experiment Design

### Variants:

**Control (A) - Current Script:**
- Standard conversation flow
- 15-second greeting
- Detailed payment options explanation
- Average duration: 150 seconds

**Treatment (B) - Optimized Script:**
- Shortened greeting (5 seconds)
- Urgency cue in first 10 seconds
- Simplified payment options
- Social proof element added
- Average duration: 120 seconds

### Metrics:

**Primary Metric:**
- **Result Rate** - % of calls resulting in payment promise

**Secondary Metrics:**
- **Contact Rate** - % of calls where client answered
- **Agreement Rate** - % of results with formal agreement
- **Call Duration** - Average call length (seconds)

### Sample Size:
- **10,000 total calls** (5,000 per variant)
- **Test period:** Feb 1-28, 2025 (4 weeks)
- **Segment:** 3-6 НБ (non-performing debt)

---

##  Key Results

### Primary Metric: Result Rate

| Variant       |-------- Result Rate | Absolute Lift | Relative Lift | p-value | Significant |
|---------------|---------------------|---------------|---------------|---------|-------------|
| **Control**   | 8.02%               | -             | -             | -       | -           |
| **Treatment** | 11.98%              | **+3.96%**    | **+49.4%**    | <0.001  | ✅ Yes      |

**95% Confidence Interval:** [+3.2%, +4.7%]

### Secondary Metrics

| Metric | Control | Treatment | Change | p-value | Significant |
|--------|---------|-----------|--------|---------|-------------|
| Contact Rate | 44.8% | 44.9% | +0.1% | 0.853 | ❌ No |
| Agreement Rate | 5.6% | 8.4% | +50.0% | <0.001 | ✅ Yes |
| Call Duration | 150s | 120s | -20.0% | <0.001 | ✅ Yes |

---

## Recommendation

### **LAUNCH Treatment Script**

The new conversation script demonstrates:
-  **Statistically significant improvement** in Result Rate (p < 0.001)
-  **50% relative lift** over current script
-  **No negative impact** on Contact Rate
-  **20% shorter calls** (increased efficiency)

### Expected Business Impact:

**Assumptions:**
- Current monthly volume: 50,000 calls for this segment
- Current result rate: 8%
- New result rate: 12%

**Expected gains:**
- Additional **2,000 results per month**
- **25% reduction** in total call time → cost savings
- Higher agreement rate → better conversion

### Next Steps:

1. **Immediate:** Roll out Treatment script to 3-6 НБ segment
2. **Week 1-2:** Monitor production metrics daily
3. **Week 3-4:** Analyze actual vs. expected performance
4. **Month 2:** Expand to other segments (1-2 РБ, Promises)

---

## Project Structure

ab-test-conversation-scripts/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── data/
│   ├── ab_test_data.csv              # Experiment data (10,000 calls)
│   └── test_config.yaml              # Test configuration
├── notebooks/
│   └── ab_test_analysis.ipynb        # Full statistical analysis
├── src/
│   └── generate_ab_data.py           # Data generation script
├── results/
│   ├── distribution_plots.png        # Metric distributions
│   ├── executive_summary.png         # Summary chart
│   ├── recommendation.md             # Final recommendation
│   └── statistical_results.txt       # Detailed stats
└── analyze.py                         # Quick analysis script

---

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Data

```bash
# Generate synthetic A/B test data
python src/generate_ab_data.py
```

**Output:**
- `data/ab_test_data.csv` - 10,000 calls (5k per variant)
- `data/test_config.yaml` - Test configuration

### 3. Run Analysis

**Option A: Jupyter Notebook (Recommended)**

```bash
jupyter notebook
# Open notebooks/ab_test_analysis.ipynb
# Run all cells
```

**Option B: Quick Script**

```bash
python analyze.py
```

**Output:**
- Statistical test results (console)
- Visualizations saved to `results/`
- Recommendation saved to `results/recommendation.md`

---

## Statistical Methods Used

### 1. Sample Ratio Mismatch (SRM) Check

**Purpose:** Validate experiment integrity  
**Method:** Chi-squared test  
**Expected:** 50/50 split between Control and Treatment

### 2. Two-Sample T-Test

**Purpose:** Test if Treatment mean differs from Control  
**Null Hypothesis (H₀):** μ_treatment = μ_control  
**Alternative (H₁):** μ_treatment ≠ μ_control  
**Significance Level:** α = 0.05

**Formula:**
t = (x̄₁ - x̄₂) / SE
SE = √(s₁²/n₁ + s₂²/n₂)

### 3. Confidence Intervals

**Purpose:** Quantify uncertainty in the lift estimate  
**Method:** 95% CI for difference in means  
**Interpretation:** True lift lies within this range with 95% probability

### 4. Effect Size (Relative Lift)

**Purpose:** Measure practical significance (business impact)  
**Formula:** `(Treatment - Control) / Control × 100%`

---

## Key Insights from Analysis

### What Worked:

1. **Shortened greeting** (15s → 5s)
   - No impact on contact rate
   - Faster path to value proposition

2. **Urgency cue** in first 10 seconds
   - Likely drove higher result rate
   - Clients more engaged early

3. **Simplified explanations**
   - Reduced call duration by 20%
   - Maintained (improved) result quality

### What Stayed Neutral:

- **Contact Rate** (44.8% vs 44.9%)
  - Script doesn't affect whether client answers
  - Validates test design (no confounding factors)

---

## How to Interpret Results

### Reading the P-value:

- **p < 0.05** → Reject H₀ → **Statistically significant**
- **p ≥ 0.05** → Fail to reject H₀ → **Not significant**

**Our result:** p < 0.001 → **Strong evidence** Treatment is better

### Reading Confidence Intervals:

**95% CI for lift: [+3.2%, +4.7%]**

**Interpretation:**
- We're 95% confident the true lift is between 3.2% and 4.7%
- **Does not include zero** → Confirms statistical significance
- Even the lower bound (+3.2%) represents meaningful business impact

### Statistical vs Practical Significance:

- **Statistical significance** → Difference is real (not due to chance)
- **Practical significance** → Difference matters for business

**Our case:**
-  Statistically significant (p < 0.001)
-  Practically significant (+50% relative lift)
-  **Strong recommendation to implement**

---

## 🛠️ Technologies Used

- **Python 3.9+**
- **pandas** - Data manipulation
- **scipy** - Statistical tests
- **matplotlib / seaborn** - Visualizations
- **numpy** - Numerical operations
- **Jupyter** - Interactive analysis

---


## Author

**Serik Karybayev**  
Data Analyst |  Data Scientist

- GitHub: [@your-username](https://https://github.com/SerikKarybaev)
- LinkedIn: [Your Profile](https://www.linkedin.com/in/serik-karybaev-29a544116)

---

## 📄 License

MIT License

---

## Acknowledgments

- Synthetic data generated for demonstration purposes
- Inspired by real-world A/B tests in debt collection analytics
- Statistical methodology based on industry best practices

---

