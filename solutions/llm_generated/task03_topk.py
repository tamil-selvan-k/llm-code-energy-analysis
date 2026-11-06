"""
Task 03: Top-K Elements Benchmark
This script finds the top K largest elements from a large dataset
of random integers using a min-heap approach.
"""

import random
import hashlib
import heapq
from typing import List


def generate_random_data(num_elements: int, max_value: int, seed: int = 42) -> List[int]:
    """Generate a list of random integers for benchmarking.

    Args:
        num_elements: Number of elements to generate
        max_value: Maximum value for each element
        seed: Random seed for reproducibility

    Returns:
        List of random integers
    """
    if num_elements <= 0:
        raise ValueError("Number of elements must be positive")
    random.seed(seed)
    generated_data = []
    for _ in range(num_elements):
        random_value = random.randint(0, max_value)
        generated_data.append(random_value)
    return generated_data


def find_top_k_elements(data: List[int], k: int) -> List[int]:
    """Find the top K largest elements using a min-heap.

    This implementation maintains a min-heap of size K, which provides
    O(n log k) time complexity.

    Args:
        data: Input list of integers
        k: Number of top elements to find

    Returns:
        List of top K elements in descending order
    """
    if data is None or len(data) == 0:
        return []
    if k <= 0:
        raise ValueError("K must be a positive integer")
    if k > len(data):
        k = len(data)

    min_heap = []
    for i, value in enumerate(data):
        if len(min_heap) < k:
            heapq.heappush(min_heap, value)
        elif value > min_heap[0]:
            heapq.heapreplace(min_heap, value)

    top_k_elements = sorted(min_heap, reverse=True)
    return top_k_elements


def compute_checksum(elements: List[int]) -> str:
    """Compute MD5 checksum for verification."""
    return hashlib.md5(str(elements).encode()).hexdigest()


def main():
    """Main function to run the top-K benchmark."""
    num_elements = 500_000
    max_value = 10_000_000
    k_value = 100

    data = generate_random_data(num_elements, max_value)
    top_k_results = find_top_k_elements(data, k_value)
    checksum = compute_checksum(top_k_results)

    print(f"top {k_value} from {len(data)} elements, checksum={checksum}")


if __name__ == "__main__":
    main()
