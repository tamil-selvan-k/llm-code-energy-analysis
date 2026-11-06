#!/usr/bin/env python3
"""
Benchmark runner for measuring code energy/performance metrics.
Runs a solution file multiple times in isolated subprocesses and collects
wall-clock time, CPU time, peak memory, and estimated energy consumption.
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time

WARMUP_RUNS = 5
MEASUREMENT_RUNS = 30
TDP_WATTS = 15.0  # Conservative TDP estimate for a typical laptop/cloud CPU core

WRAPPER_TEMPLATE = '''
import sys
import time
import tracemalloc
import json

tracemalloc.start()
cpu_start = time.process_time()
wall_start = time.perf_counter()

# Run the solution
exec(open(sys.argv[1]).read())

wall_end = time.perf_counter()
cpu_end = time.process_time()
_, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

metrics = {
    "wall_time_s": wall_end - wall_start,
    "cpu_time_s": cpu_end - cpu_start,
    "peak_memory_bytes": peak_mem,
}
print("__METRICS__" + json.dumps(metrics), file=sys.stderr)
'''


def run_single(solution_path, input_data, timeout=180):
    """Run a single benchmark iteration in an isolated subprocess."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as wrapper_file:
        wrapper_file.write(WRAPPER_TEMPLATE)
        wrapper_path = wrapper_file.name

    try:
        result = subprocess.run(
            [sys.executable, '-I', wrapper_path, solution_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        stdout = result.stdout
        stderr = result.stderr

        metrics = None
        stderr_lines = []
        for line in stderr.splitlines():
            if line.startswith("__METRICS__"):
                metrics = json.loads(line[len("__METRICS__"):])
            else:
                stderr_lines.append(line)

        if result.returncode != 0:
            return None, stdout, '\n'.join(stderr_lines), result.returncode

        if metrics is None:
            return None, stdout, "No metrics captured", -1

        metrics["energy_estimate_j"] = metrics["cpu_time_s"] * TDP_WATTS

        return metrics, stdout, '\n'.join(stderr_lines), result.returncode

    except subprocess.TimeoutExpired:
        return None, "", "Timeout", -1
    finally:
        os.unlink(wrapper_path)


def run_benchmark(solution_path, input_data, expected_output=None,
                  warmup=WARMUP_RUNS, iterations=MEASUREMENT_RUNS):
    """Run full benchmark: warmup + measurement iterations."""
    results = {
        "solution_path": solution_path,
        "warmup_runs": warmup,
        "measurement_runs": iterations,
        "tdp_watts": TDP_WATTS,
        "correctness": None,
        "runs": [],
        "error": None,
    }

    # Warmup
    for i in range(warmup):
        metrics, stdout, stderr, rc = run_single(solution_path, input_data)
        if metrics is None:
            results["error"] = f"Warmup run {i} failed: {stderr}"
            return results

    # Check correctness on first measurement run
    first_metrics, first_stdout, first_stderr, first_rc = run_single(solution_path, input_data)
    if first_metrics is None:
        results["error"] = f"First measurement run failed: {first_stderr}"
        return results

    if expected_output is not None:
        results["correctness"] = first_stdout.strip() == expected_output.strip()
    else:
        results["correctness"] = True

    results["runs"].append(first_metrics)

    # Remaining measurement runs
    for i in range(iterations - 1):
        metrics, stdout, stderr, rc = run_single(solution_path, input_data)
        if metrics is None:
            results["error"] = f"Measurement run {i+1} failed: {stderr}"
            return results
        results["runs"].append(metrics)

    # Compute summary statistics
    wall_times = [r["wall_time_s"] for r in results["runs"]]
    cpu_times = [r["cpu_time_s"] for r in results["runs"]]
    memories = [r["peak_memory_bytes"] for r in results["runs"]]
    energies = [r["energy_estimate_j"] for r in results["runs"]]

    results["summary"] = {}
    for name, data in [("wall_time_s", wall_times), ("cpu_time_s", cpu_times),
                       ("peak_memory_bytes", memories), ("energy_estimate_j", energies)]:
        results["summary"][name] = {
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0,
            "min": min(data),
            "max": max(data),
            "ci_95_lower": statistics.mean(data) - 1.96 * (statistics.stdev(data) / (len(data) ** 0.5)) if len(data) > 1 else statistics.mean(data),
            "ci_95_upper": statistics.mean(data) + 1.96 * (statistics.stdev(data) / (len(data) ** 0.5)) if len(data) > 1 else statistics.mean(data),
        }

    return results


def main():
    parser = argparse.ArgumentParser(description="Benchmark a Python solution")
    parser.add_argument("solution", help="Path to the solution .py file")
    parser.add_argument("--input", help="Path to input data file", default=None)
    parser.add_argument("--expected", help="Path to expected output file", default=None)
    parser.add_argument("--warmup", type=int, default=WARMUP_RUNS)
    parser.add_argument("--iterations", type=int, default=MEASUREMENT_RUNS)
    parser.add_argument("--output", help="Output JSON file path", default=None)
    args = parser.parse_args()

    input_data = ""
    if args.input and os.path.exists(args.input):
        with open(args.input) as f:
            input_data = f.read()

    expected_output = None
    if args.expected and os.path.exists(args.expected):
        with open(args.expected) as f:
            expected_output = f.read()

    results = run_benchmark(
        args.solution, input_data, expected_output,
        warmup=args.warmup, iterations=args.iterations,
    )

    output = json.dumps(results, indent=2)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
