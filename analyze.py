"""
Quick A/B Test Analysis Script
===============================
Runs statistical analysis without Jupyter Notebook.

Usage:
    python analyze.py
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_ab_test(data_path='data/ab_test_data.csv', alpha=0.05):
    """
    Performs complete A/B test analysis.
    
    Parameters:
    -----------
    data_path : str
        Path to test data CSV
    alpha : float
        Significance level (default: 0.05)
    """
    
    print("=" * 60)
    print("A/B TEST ANALYSIS: CONVERSATION SCRIPTS")
    print("=" * 60)
    
    # ============================================================
    # 1. LOAD DATA
    # ============================================================
    
    print("\n📂 Loading data...")
    
    if not Path(data_path).exists():
        print(f"\n❌ ERROR: Data file not found at {data_path}")
        print("Run 'python src/generate_ab_data.py' first to generate data.")
        return False
    
    df = pd.read_csv(data_path)
    df['call_date'] = pd.to_datetime(df['call_date'])
    
    print(f"  ✓ Loaded {len(df):,} calls")
    print(f"  ✓ Date range: {df['call_date'].min().date()} to {df['call_date'].max().date()}")
    
    # ============================================================
    # 2. SAMPLE RATIO MISMATCH CHECK
    # ============================================================
    
    print("\n" + "=" * 60)
    print("SAMPLE RATIO MISMATCH CHECK")
    print("=" * 60)
    
    control_size = len(df[df['variant'] == 'Control'])
    treatment_size = len(df[df['variant'] == 'Treatment'])
    
    print(f"\n📊 Sample sizes:")
    print(f"  Control:   {control_size:,}")
    print(f"  Treatment: {treatment_size:,}")
    print(f"  Ratio:     {control_size / treatment_size:.3f} (expected: 1.000)")
    
    # Chi-squared test
    observed = [control_size, treatment_size]
    expected = [len(df)/2, len(df)/2]
    chi2, p_value_srm = stats.chisquare(observed, expected)
    
    print(f"\n🔬 Chi-squared test:")
    print(f"  χ² = {chi2:.4f}")
    print(f"  p-value = {p_value_srm:.4f}")
    
    if p_value_srm > alpha:
        print(f"  ✅ PASS: Sample sizes are balanced")
    else:
        print(f"  ⚠️  WARNING: Sample size imbalance detected!")
    
    # ============================================================
    # 3. PRIMARY METRIC: RESULT RATE
    # ============================================================
    
    print("\n" + "=" * 60)
    print("PRIMARY METRIC: RESULT RATE")
    print("=" * 60)
    
    control_results = df[df['variant'] == 'Control']['is_result']
    treatment_results = df[df['variant'] == 'Treatment']['is_result']
    
    control_mean = control_results.mean()
    treatment_mean = treatment_results.mean()
    
    absolute_lift = treatment_mean - control_mean
    relative_lift = (absolute_lift / control_mean) * 100 if control_mean > 0 else 0
    
    print(f"\n📊 Observed Metrics:")
    print(f"  Control:       {control_mean:.4f} ({control_mean:.2%})")
    print(f"  Treatment:     {treatment_mean:.4f} ({treatment_mean:.2%})")
    print(f"  Absolute Lift: {absolute_lift:+.4f} ({absolute_lift:+.2%})")
    print(f"  Relative Lift: {relative_lift:+.1f}%")
    
    # T-test
    t_stat, p_value = stats.ttest_ind(treatment_results, control_results)
    
    print(f"\n🔬 Two-Sample T-Test:")
    print(f"  t-statistic = {t_stat:.4f}")
    print(f"  p-value = {p_value:.6f}")
    
    is_significant = p_value < alpha
    
    if is_significant:
        print(f"\n  ✅ SIGNIFICANT (p < {alpha})")
        print(f"  → Treatment is statistically better than Control")
    else:
        print(f"\n  ❌ NOT SIGNIFICANT (p >= {alpha})")
        print(f"  → Cannot conclude Treatment is better")
    
    # Confidence Interval
    n1, n2 = len(control_results), len(treatment_results)
    s1, s2 = control_results.std(), treatment_results.std()
    
    se = np.sqrt(s1**2/n1 + s2**2/n2)
    df_val = n1 + n2 - 2
    t_crit = stats.t.ppf(0.975, df_val)
    
    ci_lower = absolute_lift - t_crit * se
    ci_upper = absolute_lift + t_crit * se
    
    print(f"\n📊 95% Confidence Interval:")
    print(f"  [{ci_lower:.4f}, {ci_upper:.4f}]")
    print(f"  [{ci_lower:.2%}, {ci_upper:.2%}]")
    
    # ============================================================
    # 4. SECONDARY METRICS
    # ============================================================
    
    print("\n" + "=" * 60)
    print("SECONDARY METRICS")
    print("=" * 60)
    
    secondary_metrics = {
        'Contact Rate': 'is_contact',
        'Agreement Rate': 'is_agreement',
        'Call Duration': 'call_duration_sec'
    }
    
    secondary_results = []
    
    for metric_name, metric_col in secondary_metrics.items():
        
        control_data = df[df['variant'] == 'Control'][metric_col]
        treatment_data = df[df['variant'] == 'Treatment'][metric_col]
        
        control_avg = control_data.mean()
        treatment_avg = treatment_data.mean()
        
        diff = treatment_avg - control_avg
        rel_diff = (diff / control_avg) * 100 if control_avg != 0 else 0
        
        t_stat_sec, p_val_sec = stats.ttest_ind(treatment_data, control_data)
        
        is_sig = p_val_sec < alpha
        
        secondary_results.append({
            'Metric': metric_name,
            'Control': control_avg,
            'Treatment': treatment_avg,
            'Diff': diff,
            'Rel %': rel_diff,
            'p-value': p_val_sec,
            'Sig': '✅' if is_sig else '❌'
        })
        
        print(f"\n📊 {metric_name}:")
        print(f"  Control:   {control_avg:.4f}")
        print(f"  Treatment: {treatment_avg:.4f}")
        print(f"  Change:    {diff:+.4f} ({rel_diff:+.1f}%)")
        print(f"  p-value:   {p_val_sec:.4f} {('✅' if is_sig else '❌')}")
    
    # ============================================================
    # 5. SUMMARY TABLE
    # ============================================================
    
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    summary_df = pd.DataFrame(secondary_results)
    
    print("\n" + summary_df.to_string(index=False))
    
    # ============================================================
    # 6. RECOMMENDATION
    # ============================================================
    
    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    
    if is_significant and absolute_lift > 0:
        print("\n✅ RECOMMENDATION: LAUNCH Treatment Script")
        print(f"\nReasons:")
        print(f"  1. Statistically significant improvement (p = {p_value:.4f})")
        print(f"  2. Strong effect size: {relative_lift:+.1f}% relative lift")
        print(f"  3. 95% CI does not include zero: [{ci_lower:.2%}, {ci_upper:.2%}]")
        
        # Check secondary metrics
        contact_change = secondary_results[0]['Rel %']
        duration_change = secondary_results[2]['Rel %']
        
        if contact_change > -5:
            print(f"  4. No negative impact on Contact Rate ({contact_change:+.1f}%)")
        
        if duration_change < 0:
            print(f"  5. Bonus: Reduced call duration by {abs(duration_change):.1f}%")
        
        print(f"\n💡 Expected business impact:")
        print(f"  - Assuming 50,000 calls/month for this segment")
        print(f"  - Current results: {int(50000 * control_mean):,}/month")
        print(f"  - Expected results: {int(50000 * treatment_mean):,}/month")
        print(f"  - Additional results: +{int(50000 * absolute_lift):,}/month")
        
    elif is_significant and absolute_lift < 0:
        print("\n❌ RECOMMENDATION: DO NOT Launch Treatment")
        print(f"\nTreatment performs WORSE than Control:")
        print(f"  - {relative_lift:.1f}% decline in Result Rate")
        print(f"  - Statistically significant (p = {p_value:.4f})")
        
    else:
        print("\n⚠️  RECOMMENDATION: Inconclusive - Do Not Launch Yet")
        print(f"\nReasons:")
        print(f"  1. No statistically significant difference (p = {p_value:.4f})")
        print(f"  2. Observed lift: {relative_lift:+.1f}% (but could be due to chance)")
        print(f"\nOptions:")
        print(f"  - Increase sample size and re-test")
        print(f"  - Try a different Treatment variant")
        print(f"  - Keep current Control script")
    
    # ============================================================
    # 7. SAVE RESULTS
    # ============================================================
    
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    print("=" * 60)
    
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)
    
    # Save statistical summary
    summary_text = f"""
A/B TEST STATISTICAL RESULTS
============================

Test Period: {df['call_date'].min().date()} to {df['call_date'].max().date()}
Total Calls: {len(df):,}
Significance Level: α = {alpha}

SAMPLE SIZES:
-------------
Control:   {control_size:,}
Treatment: {treatment_size:,}

PRIMARY METRIC: RESULT RATE
----------------------------
Control:       {control_mean:.4f} ({control_mean:.2%})
Treatment:     {treatment_mean:.4f} ({treatment_mean:.2%})
Absolute Lift: {absolute_lift:+.4f} ({absolute_lift:+.2%})
Relative Lift: {relative_lift:+.1f}%

Statistical Test:
  t-statistic: {t_stat:.4f}
  p-value: {p_value:.6f}
  Significant: {'Yes ✅' if is_significant else 'No ❌'}

95% Confidence Interval:
  [{ci_lower:.4f}, {ci_upper:.4f}]
  [{ci_lower:.2%}, {ci_upper:.2%}]

SECONDARY METRICS:
------------------
"""
    
    for res in secondary_results:
        summary_text += f"\n{res['Metric']}:"
        summary_text += f"\n  Control:   {res['Control']:.4f}"
        summary_text += f"\n  Treatment: {res['Treatment']:.4f}"
        summary_text += f"\n  Change:    {res['Diff']:+.4f} ({res['Rel %']:+.1f}%)"
        summary_text += f"\n  p-value:   {res['p-value']:.4f} {res['Sig']}\n"
    
    summary_text += f"\nRECOMMENDATION: "
    if is_significant and absolute_lift > 0:
        summary_text += "✅ LAUNCH Treatment Script"
    elif is_significant and absolute_lift < 0:
        summary_text += "❌ DO NOT Launch Treatment"
    else:
        summary_text += "⚠️  Inconclusive - Do Not Launch Yet"
    
    output_file = results_dir / 'statistical_results.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print("✓✓✓ ANALYSIS COMPLETE ✓✓✓")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    
    import sys
    
    # Parse command line arguments
    data_path = 'data/ab_test_data.csv'
    alpha = 0.05
    
    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        alpha = float(sys.argv[2])
    
    # Run analysis
    try:
        success = analyze_ab_test(data_path, alpha)
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)