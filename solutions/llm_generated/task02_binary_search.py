"""
Task 02: Binary Search Benchmark
This script performs binary search queries on a sorted array of integers.
It generates a sorted array of 1M elements and performs 10K search queries.
"""

import random
import hashlib
from typing import List, Optional


def generate_sorted_array(size: int, max_value: int, seed: int = 42) -> List[int]:
    """Generate a sorted array of random integers.

    Args:
        size: Number of elements to generate
        max_value: Maximum value for each element
        seed: Random seed for reproducibility

    Returns:
        Sorted list of random integers
    """
    if size <= 0:
        raise ValueError("Size must be positive")

    random.seed(seed)
    array = [random.randint(0, max_value) for _ in range(size)]
    sorted_array = sorted(array)
    return sorted_array


def generate_queries(count: int, max_value: int) -> List[int]:
    """Generate random search queries.

    Args:
        count: Number of queries to generate
        max_value: Maximum query value

    Returns:
        List of query integers
    """
    if count <= 0:
        raise ValueError("Count must be positive")

    queries = []
    for _ in range(count):
        query_value = random.randint(0, max_value)
        queries.append(query_value)
    return queries


def binary_search(sorted_array: List[int], target_value: int) -> Optional[int]:
    """Perform binary search on a sorted array.

    Args:
        sorted_array: Sorted list of integers to search in
        target_value: Value to search for

    Returns:
        Index of the target value if found, None otherwise
    """
    if sorted_array is None or len(sorted_array) == 0:
        return None

    left_pointer = 0
    right_pointer = len(sorted_array) - 1

    while left_pointer <= right_pointer:
        middle_index = (left_pointer + right_pointer) // 2
        middle_value = sorted_array[middle_index]

        if middle_value == target_value:
            return middle_index
        elif middle_value < target_value:
            left_pointer = middle_index + 1
        else:
            right_pointer = middle_index - 1

    return None


def execute_search_queries(sorted_array: List[int], queries: List[int]) -> List[int]:
    """Execute all search queries and return results.

    Args:
        sorted_array: Sorted array to search in
        queries: List of values to search for

    Returns:
        List of 1s (found) and 0s (not found)
    """
    search_results = []
    for query_value in queries:
        result = binary_search(sorted_array, query_value)
        if result is not None:
            search_results.append(1)
        else:
            search_results.append(0)
    return search_results


def main():
    """Main function to run the binary search benchmark."""
    array_size = 1_000_000
    max_value = 10_000_000
    num_queries = 10_000

    sorted_array = generate_sorted_array(array_size, max_value)
    queries = generate_queries(num_queries, max_value)
    results = execute_search_queries(sorted_array, queries)

    total_found = sum(results)
    checksum = hashlib.md5(str(total_found).encode()).hexdigest()
    print(f"searched {len(queries)} queries in {len(sorted_array)} elements, found={total_found}, checksum={checksum}")


if __name__ == "__main__":
    main()
