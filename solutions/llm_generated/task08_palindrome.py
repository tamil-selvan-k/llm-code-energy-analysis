"""
Task 08: Palindromic Substring Detection
Finds all palindromic substrings in a 10K character string using
the expand-around-center approach.
"""

import random
import hashlib
import string
from typing import Tuple


def generate_random_string(length: int, seed: int = 42) -> str:
    """Generate a random lowercase string."""
    if length <= 0:
        raise ValueError("Length must be positive")
    random.seed(seed)
    characters = random.choices(string.ascii_lowercase, k=length)
    return ''.join(characters)


def expand_from_center(text: str, left_index: int, right_index: int) -> int:
    """Expand around a center and count palindromic substrings found.

    Args:
        text: The input string
        left_index: Starting left position
        right_index: Starting right position

    Returns:
        Number of palindromic substrings found from this center
    """
    palindrome_count = 0
    current_left = left_index
    current_right = right_index

    while current_left >= 0 and current_right < len(text):
        left_character = text[current_left]
        right_character = text[current_right]

        if left_character == right_character:
            palindrome_count += 1
            current_left -= 1
            current_right += 1
        else:
            break

    return palindrome_count


def count_all_palindromic_substrings(text: str) -> int:
    """Count all palindromic substrings in the text.

    Uses the expand-around-center approach considering both
    odd-length and even-length palindromes.

    Args:
        text: Input string

    Returns:
        Total count of palindromic substrings
    """
    if text is None or len(text) == 0:
        return 0

    total_palindromes = 0
    text_length = len(text)

    for center_index in range(text_length):
        odd_length_count = expand_from_center(text, center_index, center_index)
        total_palindromes += odd_length_count

        even_length_count = expand_from_center(text, center_index, center_index + 1)
        total_palindromes += even_length_count

    return total_palindromes


def main():
    """Main function."""
    string_length = 10_000
    text = generate_random_string(string_length)
    count = count_all_palindromic_substrings(text)
    checksum = hashlib.md5(str(count).encode()).hexdigest()
    print(f"found {count} palindromic substrings in {len(text)} chars, checksum={checksum}")


if __name__ == "__main__":
    main()
