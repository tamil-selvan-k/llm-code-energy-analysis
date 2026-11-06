#!/usr/bin/env python3
"""
Statistical analysis of benchmark results.
Computes descriptive stats, runs Mann-Whitney U tests, computes Cohen's d,
groups by category, and outputs analysis JSON + CSV.
"""

import csv
import json
import math
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")

METRICS = ["wall_time_s", "cpu_time_s", "peak_memory_bytes", "energy_estimate_j"]
COMPARISONS = [
    ("human_optimized", "llm_generated", "Optimized vs LLM"),
    ("human_typical", "llm_generated", "Typical vs LLM"),
    ("human_optimized", "human_typical", "Optimized vs Typical"),
]


def mann_whitney_u(x, y):
    """Manual Mann-Whitney U test (no scipy dependency)."""
    nx, ny = len(x), len(y)
    combined = [(val, 'x') for val in x] + [(val, 'y') for val in y]
    combined.sort(key=lambda t: t[0])

    # Assign ranks with tie handling
    ranks = [0.0] * len(combined)
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) and combined[j][0] == combined[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    r_x = sum(ranks[i] for i in range(len(combined)) if combined[i][1] == 'x')
    u_x = r_x - nx * (nx + 1) / 2.0
    u_y = nx * ny - u_x
    u = min(u_x, u_y)

    # Normal approximation for p-value
    mu = nx * ny / 2.0
    sigma = math.sqrt(nx * ny * (nx + ny + 1) / 12.0)
    if sigma == 0:
        return u, 1.0
    z = (u - mu) / sigma
    # Two-tailed p-value approximation
    p = 2.0 * _norm_cdf(-abs(z))
    return u, p


def _norm_cdf(z):
    """Approximate standard normal CDF."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def cohens_d(x, y):
    """Compute Cohen's d effect size."""
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return 0.0
    mean_x = sum(x) / nx
    mean_y = sum(y) / ny
    var_x = sum((v - mean_x) ** 2 for v in x) / (nx - 1)
    var_y = sum((v - mean_y) ** 2 for v in y) / (ny - 1)
    pooled_std = math.sqrt(((nx - 1) * var_x + (ny - 1) * var_y) / (nx + ny - 2))
    if pooled_std == 0:
        return 0.0
    return (mean_x - mean_y) / pooled_std


def compute_stats(values):
    """Compute descriptive statistics for a list of values."""
    n = len(values)
    if n == 0:
        return {}
    mean = sum(values) / n
    sorted_v = sorted(values)
    median = sorted_v[n // 2] if n % 2 == 1 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
    variance = sum((v - mean) ** 2 for v in values) / (n - 1) if n > 1 else 0
    stdev = math.sqrt(variance)
    se = stdev / math.sqrt(n) if n > 0 else 0
    return {
        "n": n,
        "mean": mean,
        "median": median,
        "stdev": stdev,
        "min": min(values),
        "max": max(values),
        "ci_95_lower": mean - 1.96 * se,
        "ci_95_upper": mean + 1.96 * se,
    }


def analyze():
    """Main analysis routine."""
    raw_path = os.path.join(RESULTS_DIR, "raw_results.json")
    if not os.path.exists(raw_path):
        print(f"ERROR: {raw_path} not found. Run benchmarks first.")
        sys.exit(1)

    with open(raw_path) as f:
        data = json.load(f)

    analysis = {
        "metadata": data.get("metadata", {}),
        "per_task": {},
        "per_category": {},
        "overall": {},
    }

    # Aggregate by category
    category_data = {}

    for task_name, task_info in data["tasks"].items():
        category = task_info.get("category", "uncategorized")
        solutions = task_info.get("solutions", {})

        task_analysis = {"category": category, "solutions": {}, "comparisons": {}}

        # Extract per-run metric values for each solution type
        sol_metrics = {}
        for sol_type, result in solutions.items():
            runs = result.get("runs", [])
            if not runs:
                continue
            sol_metrics[sol_type] = {}
            task_analysis["solutions"][sol_type] = {
                "correctness": result.get("correctness"),
            }
            for metric in METRICS:
                values = [r[metric] for r in runs if metric in r]
                sol_metrics[sol_type][metric] = values
                task_analysis["solutions"][sol_type][metric] = compute_stats(values)

                # Accumulate for category analysis
                key = (category, sol_type, metric)
                if key not in category_data:
                    category_data[key] = []
                category_data[key].extend(values)

        # Statistical comparisons
        for sol_a, sol_b, label in COMPARISONS:
            if sol_a not in sol_metrics or sol_b not in sol_metrics:
                continue
            comp = {}
            for metric in METRICS:
                va = sol_metrics[sol_a].get(metric, [])
                vb = sol_metrics[sol_b].get(metric, [])
                if len(va) < 2 or len(vb) < 2:
                    continue
                u_stat, p_val = mann_whitney_u(va, vb)
                d = cohens_d(va, vb)
                mean_a = sum(va) / len(va)
                mean_b = sum(vb) / len(vb)
                pct_diff = ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0
                comp[metric] = {
                    "mann_whitney_u": u_stat,
                    "p_value": p_val,
                    "significant": p_val < 0.05,
                    "cohens_d": d,
                    "effect_size": "large" if abs(d) >= 0.8 else "medium" if abs(d) >= 0.5 else "small" if abs(d) >= 0.2 else "negligible",
                    "mean_a": mean_a,
                    "mean_b": mean_b,
                    "pct_difference": pct_diff,
                }
            task_analysis["comparisons"][label] = comp

        analysis["per_task"][task_name] = task_analysis

    # Category-level aggregation
    categories = set()
    for (cat, _, _) in category_data:
        categories.add(cat)

    for cat in sorted(categories):
        analysis["per_category"][cat] = {"solutions": {}, "comparisons": {}}
        cat_sol_metrics = {}
        for sol_type in ["human_optimized", "human_typical", "llm_generated"]:
            analysis["per_category"][cat]["solutions"][sol_type] = {}
            cat_sol_metrics[sol_type] = {}
            for metric in METRICS:
                key = (cat, sol_type, metric)
                values = category_data.get(key, [])
                if values:
                    analysis["per_category"][cat]["solutions"][sol_type][metric] = compute_stats(values)
                    cat_sol_metrics[sol_type][metric] = values

        for sol_a, sol_b, label in COMPARISONS:
            comp = {}
            for metric in METRICS:
                va = cat_sol_metrics.get(sol_a, {}).get(metric, [])
                vb = cat_sol_metrics.get(sol_b, {}).get(metric, [])
                if len(va) < 2 or len(vb) < 2:
                    continue
                u_stat, p_val = mann_whitney_u(va, vb)
                d = cohens_d(va, vb)
                mean_a = sum(va) / len(va)
                mean_b = sum(vb) / len(vb)
                pct_diff = ((mean_b - mean_a) / mean_a * 100) if mean_a != 0 else 0
                comp[metric] = {
                    "mann_whitney_u": u_stat,
                    "p_value": p_val,
                    "significant": p_val < 0.05,
                    "cohens_d": d,
                    "effect_size": "large" if abs(d) >= 0.8 else "medium" if abs(d) >= 0.5 else "small" if abs(d) >= 0.2 else "negligible",
                    "pct_difference": pct_diff,
                }
            analysis["per_category"][cat]["comparisons"][label] = comp

    # Overall aggregation
    overall_metrics = {}
    for sol_type in ["human_optimized", "human_typical", "llm_generated"]:
        overall_metrics[sol_type] = {}
        analysis["overall"][sol_type] = {}
        for metric in METRICS:
            all_vals = []
            for cat in categories:
                key = (cat, sol_type, metric)
                all_vals.extend(category_data.get(key, []))
            if all_vals:
                analysis["overall"][sol_type][metric] = compute_stats(all_vals)
                overall_metrics[sol_type][metric] = all_vals

    # Save analysis JSON
    analysis_path = os.path.join(RESULTS_DIR, "analysis.json")
    with open(analysis_path, 'w') as f:
        json.dump(analysis, f, indent=2)

    # Generate CSV summary
    _write_task_csv(analysis)
    _write_comparison_csv(analysis)

    # Print summary table
    _print_summary(analysis)

    print(f"\nAnalysis saved to {analysis_path}")
    return analysis


def _write_task_csv(analysis):
    """Write per-task summary CSV."""
    csv_path = os.path.join(RESULTS_DIR, "task_summary.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "task", "category", "solution_type", "correct",
            "cpu_time_mean", "cpu_time_stdev",
            "wall_time_mean", "wall_time_stdev",
            "memory_mean_kb", "memory_stdev_kb",
            "energy_mean_j", "energy_stdev_j",
        ])
        for task_name, task_data in sorted(analysis["per_task"].items()):
            cat = task_data["category"]
            for sol_type, sol_data in sorted(task_data["solutions"].items()):
                correct = sol_data.get("correctness", "")
                cpu = sol_data.get("cpu_time_s", {})
                wall = sol_data.get("wall_time_s", {})
                mem = sol_data.get("peak_memory_bytes", {})
                energy = sol_data.get("energy_estimate_j", {})
                writer.writerow([
                    task_name, cat, sol_type, correct,
                    f"{cpu.get('mean', 0):.6f}", f"{cpu.get('stdev', 0):.6f}",
                    f"{wall.get('mean', 0):.6f}", f"{wall.get('stdev', 0):.6f}",
                    f"{mem.get('mean', 0) / 1024:.2f}", f"{mem.get('stdev', 0) / 1024:.2f}",
                    f"{energy.get('mean', 0):.6f}", f"{energy.get('stdev', 0):.6f}",
                ])
    print(f"Task CSV written to {csv_path}")


def _write_comparison_csv(analysis):
    """Write statistical comparison CSV."""
    csv_path = os.path.join(RESULTS_DIR, "comparisons.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "task", "category", "comparison", "metric",
            "mean_a", "mean_b", "pct_diff",
            "u_statistic", "p_value", "significant", "cohens_d", "effect_size",
        ])
        for task_name, task_data in sorted(analysis["per_task"].items()):
            cat = task_data["category"]
            for comp_label, comp_data in task_data.get("comparisons", {}).items():
                for metric, stats in comp_data.items():
                    writer.writerow([
                        task_name, cat, comp_label, metric,
                        f"{stats['mean_a']:.6f}", f"{stats['mean_b']:.6f}",
                        f"{stats['pct_difference']:.2f}%",
                        f"{stats['mann_whitney_u']:.1f}", f"{stats['p_value']:.6f}",
                        stats['significant'], f"{stats['cohens_d']:.4f}",
                        stats['effect_size'],
                    ])
    print(f"Comparison CSV written to {csv_path}")


def _print_summary(analysis):
    """Print a formatted summary table to stdout."""
    print("\n" + "=" * 90)
    print("BENCHMARK ANALYSIS SUMMARY")
    print("=" * 90)

    # Overall comparison
    print("\n--- Overall Means Across All Tasks ---")
    print(f"{'Solution Type':<20} {'CPU Time (s)':<15} {'Memory (KB)':<15} {'Energy (J)':<15} {'Wall Time (s)':<15}")
    print("-" * 80)
    for sol_type in ["human_optimized", "human_typical", "llm_generated"]:
        data = analysis.get("overall", {}).get(sol_type, {})
        cpu = data.get("cpu_time_s", {}).get("mean", 0)
        mem = data.get("peak_memory_bytes", {}).get("mean", 0) / 1024
        energy = data.get("energy_estimate_j", {}).get("mean", 0)
        wall = data.get("wall_time_s", {}).get("mean", 0)
        label = sol_type.replace("_", " ").title()
        print(f"{label:<20} {cpu:<15.6f} {mem:<15.2f} {energy:<15.6f} {wall:<15.6f}")

    # Per-category
    print("\n--- Per-Category Summary ---")
    for cat, cat_data in sorted(analysis.get("per_category", {}).items()):
        print(f"\n  Category: {cat}")
        print(f"  {'Solution':<20} {'CPU (s)':<12} {'Mem (KB)':<12} {'Energy (J)':<12}")
        print(f"  {'-'*56}")
        for sol_type in ["human_optimized", "human_typical", "llm_generated"]:
            sol_data = cat_data.get("solutions", {}).get(sol_type, {})
            cpu = sol_data.get("cpu_time_s", {}).get("mean", 0)
            mem = sol_data.get("peak_memory_bytes", {}).get("mean", 0) / 1024
            energy = sol_data.get("energy_estimate_j", {}).get("mean", 0)
            label = sol_type.replace("_", " ").title()
            print(f"  {label:<20} {cpu:<12.6f} {mem:<12.2f} {energy:<12.6f}")

    # Significant findings
    print("\n--- Statistically Significant Comparisons (p < 0.05) ---")
    print(f"{'Task':<25} {'Comparison':<25} {'Metric':<20} {'%Diff':<10} {'Effect':<12} {'p-value':<10}")
    print("-" * 90)
    found = False
    for task_name, task_data in sorted(analysis["per_task"].items()):
        for comp_label, comp_data in task_data.get("comparisons", {}).items():
            for metric, stats in comp_data.items():
                if stats.get("significant"):
                    found = True
                    metric_short = metric.replace("_s", "").replace("_bytes", "").replace("_j", "").replace("_", " ")
                    print(f"{task_name:<25} {comp_label:<25} {metric_short:<20} {stats['pct_difference']:>+8.1f}%  {stats['effect_size']:<12} {stats['p_value']:<.4f}")
    if not found:
        print("  (none found)")

    print("\n" + "=" * 90)


if __name__ == "__main__":
    analyze()
