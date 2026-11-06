"""
Task 01: Merge Sort Benchmark
This script generates a list of random integers and sorts them using
a merge sort algorithm implementation. The sorted result is verified
using an MD5 checksum of the first 100 elements.
"""

import random
import hashlib
from typing import List


def generate_random_integers(count: int, max_value: int, seed: int = 42) -> List[int]:
    """Generate a list of random integers with a fixed seed for reproducibility.

    Args:
        count: Number of integers to generate
        max_value: Maximum value for each integer
        seed: Random seed for reproducibility

    Returns:
        List of random integers
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer")
    if not isinstance(max_value, int) or max_value <= 0:
        raise ValueError("Max value must be a positive integer")

    random.seed(seed)
    random_integers = []
    for _ in range(count):
        random_integer = random.randint(0, max_value)
        random_integers.append(random_integer)
    return random_integers


def merge_sort(input_list: List[int]) -> List[int]:
    """Sort a list of integers using the merge sort algorithm.

    Args:
        input_list: List of integers to sort

    Returns:
        New sorted list of integers
    """
    if input_list is None:
        raise ValueError("Input list cannot be None")

    if len(input_list) <= 1:
        return input_list.copy()

    middle_index = len(input_list) // 2
    left_half = input_list[:middle_index]
    right_half = input_list[middle_index:]

    sorted_left_half = merge_sort(left_half)
    sorted_right_half = merge_sort(right_half)

    return merge_two_sorted_lists(sorted_left_half, sorted_right_half)


def merge_two_sorted_lists(left_list: List[int], right_list: List[int]) -> List[int]:
    """Merge two sorted lists into a single sorted list.

    Args:
        left_list: First sorted list
        right_list: Second sorted list

    Returns:
        Merged sorted list
    """
    merged_result = []
    left_index = 0
    right_index = 0

    while left_index < len(left_list) and right_index < len(right_list):
        if left_list[left_index] <= right_list[right_index]:
            merged_result.append(left_list[left_index])
            left_index += 1
        else:
            merged_result.append(right_list[right_index])
            right_index += 1

    while left_index < len(left_list):
        merged_result.append(left_list[left_index])
        left_index += 1

    while right_index < len(right_list):
        merged_result.append(right_list[right_index])
        right_index += 1

    return merged_result


def compute_checksum(data_list: List[int], num_elements: int = 100) -> str:
    """Compute MD5 checksum of the first N elements of a list.

    Args:
        data_list: List to compute checksum for
        num_elements: Number of elements to include in checksum

    Returns:
        MD5 hexdigest string
    """
    elements_for_checksum = data_list[:num_elements]
    string_representation = str(elements_for_checksum)
    checksum_hash = hashlib.md5(string_representation.encode()).hexdigest()
    return checksum_hash


def main():
    """Main function to run the merge sort benchmark."""
    number_of_elements = 100_000
    maximum_value = 10_000_000

    random_integers = generate_random_integers(number_of_elements, maximum_value)
    sorted_integers = merge_sort(random_integers)
    checksum = compute_checksum(sorted_integers)

    print(f"sorted {len(sorted_integers)} elements, checksum={checksum}")


if __name__ == "__main__":
    main()
