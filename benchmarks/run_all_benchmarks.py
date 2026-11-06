#!/usr/bin/env python3
"""
Orchestrator that discovers all benchmark tasks and solution variants,
runs them through benchmark_runner, and collects results.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from benchmark_runner import run_benchmark

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLUTIONS_DIR = os.path.join(PROJECT_ROOT, "solutions")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
TASKS_DIR = os.path.join(PROJECT_ROOT, "tasks")

SOLUTION_TYPES = ["human_optimized", "human_typical", "llm_generated"]

WARMUP = 2
ITERATIONS = 10


def discover_tasks():
    """Find all tasks by scanning the human_optimized directory for .py files."""
    tasks = []
    base = os.path.join(SOLUTIONS_DIR, "human_optimized")
    if not os.path.isdir(base):
        return tasks
    for fname in sorted(os.listdir(base)):
        if fname.endswith(".py"):
            task_name = fname[:-3]
            tasks.append(task_name)
    return tasks


def get_task_io(task_name):
    """Load input and expected output for a task if available."""
    input_path = os.path.join(TASKS_DIR, task_name, "input.txt")
    expected_path = os.path.join(TASKS_DIR, task_name, "expected_output.txt")

    input_data = ""
    if os.path.exists(input_path):
        with open(input_path) as f:
            input_data = f.read()

    expected_output = None
    if os.path.exists(expected_path):
        with open(expected_path) as f:
            expected_output = f.read()

    task_meta_path = os.path.join(TASKS_DIR, task_name, "meta.json")
    category = "uncategorized"
    if os.path.exists(task_meta_path):
        with open(task_meta_path) as f:
            meta = json.load(f)
            category = meta.get("category", "uncategorized")

    return input_data, expected_output, category


def run_all():
    """Run all benchmarks and collect results."""
    tasks = discover_tasks()
    if not tasks:
        print("ERROR: No tasks found. Ensure solutions exist in solutions/human_optimized/")
        sys.exit(1)

    print(f"Discovered {len(tasks)} tasks: {', '.join(tasks)}")
    print(f"Solution types: {', '.join(SOLUTION_TYPES)}")
    print(f"Config: {WARMUP} warmup + {ITERATIONS} measurement runs per solution")
    print("=" * 70)

    all_results = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "warmup_runs": WARMUP,
            "measurement_runs": ITERATIONS,
            "platform": sys.platform,
            "python_version": sys.version,
        },
        "tasks": {},
    }

    total = len(tasks) * len(SOLUTION_TYPES)
    done = 0

    for task_name in tasks:
        input_data, expected_output, category = get_task_io(task_name)
        all_results["tasks"][task_name] = {
            "category": category,
            "solutions": {},
        }

        for sol_type in SOLUTION_TYPES:
            sol_path = os.path.join(SOLUTIONS_DIR, sol_type, f"{task_name}.py")
            done += 1

            if not os.path.exists(sol_path):
                print(f"[{done}/{total}] SKIP {task_name}/{sol_type} (not found)")
                continue

            print(f"[{done}/{total}] Running {task_name}/{sol_type}...", end=" ", flush=True)
            start = time.time()

            result = run_benchmark(
                sol_path, input_data, expected_output,
                warmup=WARMUP, iterations=ITERATIONS,
            )

            elapsed = time.time() - start
            correct = result.get("correctness", False)
            error = result.get("error")

            if error:
                print(f"ERROR ({elapsed:.1f}s): {error}")
            elif not correct:
                print(f"INCORRECT OUTPUT ({elapsed:.1f}s)")
            else:
                summary = result.get("summary", {})
                cpu = summary.get("cpu_time_s", {}).get("mean", 0)
                mem = summary.get("peak_memory_bytes", {}).get("mean", 0)
                energy = summary.get("energy_estimate_j", {}).get("mean", 0)
                print(f"OK ({elapsed:.1f}s) cpu={cpu:.6f}s mem={mem/1024:.1f}KB energy={energy:.6f}J")

            all_results["tasks"][task_name]["solutions"][sol_type] = result

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_path = os.path.join(RESULTS_DIR, "raw_results.json")
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)

    print("=" * 70)
    print(f"Results saved to {output_path}")
    return all_results


if __name__ == "__main__":
    run_all()
