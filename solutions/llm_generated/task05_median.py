"""
Task 05: Median Finding Benchmark
Finds the median value of 500K unsorted integers.
"""

import random
import hashlib
from typing import List, Union


def generate_random_integers(count: int, max_value: int, seed: int = 42) -> List[int]:
    """Generate random integers for testing."""
    if count <= 0:
        raise ValueError("Count must be positive")
    random.seed(seed)
    return [random.randint(0, max_value) for _ in range(count)]


def find_median(numbers: List[int]) -> Union[int, float]:
    """Find the median of a list of numbers.

    For even-length lists, returns the average of the two middle elements.
    For odd-length lists, returns the middle element.

    Args:
        numbers: List of integers

    Returns:
        Median value
    """
    if numbers is None or len(numbers) == 0:
        raise ValueError("List must not be empty")

    sorted_numbers = sorted(numbers)
    total_count = len(sorted_numbers)
    middle_index = total_count // 2

    if total_count % 2 == 0:
        left_middle_value = sorted_numbers[middle_index - 1]
        right_middle_value = sorted_numbers[middle_index]
        median_value = (left_middle_value + right_middle_value) / 2
    else:
        median_value = sorted_numbers[middle_index]

    return median_value


def main():
    """Main function."""
    num_elements = 500_000
    max_value = 10_000_000
    data = generate_random_integers(num_elements, max_value)
    median_result = find_median(data)
    checksum = hashlib.md5(str(median_result).encode()).hexdigest()
    print(f"median of {len(data)} elements = {median_result}, checksum={checksum}")


if __name__ == "__main__":
    main()
