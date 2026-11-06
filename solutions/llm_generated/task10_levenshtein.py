"""
Task 10: Levenshtein Edit Distance Benchmark
Computes edit distance for 500 pairs of strings (~100 chars each).
Uses dynamic programming with full matrix approach.
"""

import random
import hashlib
import string
from typing import List, Tuple


def generate_string_pairs(num_pairs: int, min_length: int = 80, max_length: int = 120, seed: int = 42) -> List[Tuple[str, str]]:
    """Generate pairs of random strings for edit distance computation."""
    if num_pairs <= 0:
        raise ValueError("Number of pairs must be positive")
    random.seed(seed)
    string_pairs = []
    for _ in range(num_pairs):
        length_a = random.randint(min_length, max_length)
        length_b = random.randint(min_length, max_length)
        string_a = ''.join(random.choices(string.ascii_lowercase, k=length_a))
        string_b = ''.join(random.choices(string.ascii_lowercase, k=length_b))
        string_pairs.append((string_a, string_b))
    return string_pairs


def compute_levenshtein_distance(source_string: str, target_string: str) -> int:
    """Compute the Levenshtein edit distance between two strings.

    Uses the classic dynamic programming approach with a full matrix.

    Args:
        source_string: The source string
        target_string: The target string

    Returns:
        The minimum number of edit operations
    """
    if source_string is None or target_string is None:
        raise ValueError("Input strings cannot be None")

    source_length = len(source_string)
    target_length = len(target_string)

    distance_matrix = [[0] * (target_length + 1) for _ in range(source_length + 1)]

    for source_index in range(source_length + 1):
        distance_matrix[source_index][0] = source_index
    for target_index in range(target_length + 1):
        distance_matrix[0][target_index] = target_index

    for source_index in range(1, source_length + 1):
        for target_index in range(1, target_length + 1):
            source_character = source_string[source_index - 1]
            target_character = target_string[target_index - 1]

            if source_character == target_character:
                substitution_cost = 0
            else:
                substitution_cost = 1

            deletion_cost = distance_matrix[source_index - 1][target_index] + 1
            insertion_cost = distance_matrix[source_index][target_index - 1] + 1
            replacement_cost = distance_matrix[source_index - 1][target_index - 1] + substitution_cost

            distance_matrix[source_index][target_index] = min(
                deletion_cost,
                insertion_cost,
                replacement_cost
            )

    return distance_matrix[source_length][target_length]


def main():
    """Main function."""
    num_pairs = 500
    string_pairs = generate_string_pairs(num_pairs)
    distances = []
    for source, target in string_pairs:
        distance = compute_levenshtein_distance(source, target)
        distances.append(distance)
    total = sum(distances)
    checksum = hashlib.md5(str(total).encode()).hexdigest()
    print(f"computed {len(string_pairs)} edit distances, total={total}, checksum={checksum}")


if __name__ == "__main__":
    main()
