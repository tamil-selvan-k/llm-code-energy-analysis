"""
Task 04: String Sorting Benchmark
Sorts 50,000 random strings first by length, then alphabetically.
"""

import random
import hashlib
import string
from typing import List, Tuple


def generate_random_strings(count: int, min_length: int = 3, max_length: int = 20, seed: int = 42) -> List[str]:
    """Generate random lowercase strings."""
    if count <= 0:
        raise ValueError("Count must be positive")
    random.seed(seed)
    generated_strings = []
    for _ in range(count):
        string_length = random.randint(min_length, max_length)
        random_characters = random.choices(string.ascii_lowercase, k=string_length)
        random_string = ''.join(random_characters)
        generated_strings.append(random_string)
    return generated_strings


def create_sort_key(input_string: str) -> Tuple[int, str]:
    """Create a composite sort key: (length, alphabetical)."""
    return (len(input_string), input_string)


def sort_strings_by_length_and_alpha(string_list: List[str]) -> List[str]:
    """Sort strings by length first, then alphabetically."""
    if string_list is None:
        raise ValueError("Input list cannot be None")
    sorted_result = sorted(string_list, key=create_sort_key)
    return sorted_result


def main():
    """Main function."""
    num_strings = 50_000
    random_strings = generate_random_strings(num_strings)
    sorted_strings = sort_strings_by_length_and_alpha(random_strings)
    first_50_joined = ''.join(sorted_strings[:50])
    checksum = hashlib.md5(first_50_joined.encode()).hexdigest()
    print(f"sorted {len(sorted_strings)} strings, checksum={checksum}")


if __name__ == "__main__":
    main()
