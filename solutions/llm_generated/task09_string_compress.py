"""
Task 09: Run-Length Encoding (String Compression)
Performs run-length encoding on a 1M character string.
"""

import random
import hashlib
import string
from typing import List, Tuple


def generate_input_string(length: int, alphabet_size: int = 5, seed: int = 42) -> str:
    """Generate a random string with limited alphabet for RLE."""
    if length <= 0:
        raise ValueError("Length must be positive")
    random.seed(seed)
    alphabet = string.ascii_lowercase[:alphabet_size]
    characters = random.choices(alphabet, k=length)
    return ''.join(characters)


def run_length_encode(input_string: str) -> str:
    """Perform run-length encoding on the input string.

    Consecutive identical characters are replaced with the character
    followed by its count.

    Args:
        input_string: String to compress

    Returns:
        Run-length encoded string
    """
    if input_string is None:
        raise ValueError("Input string cannot be None")
    if len(input_string) == 0:
        return ""

    encoded_parts: List[str] = []
    current_character = input_string[0]
    current_run_length = 1

    for index in range(1, len(input_string)):
        character_at_position = input_string[index]

        if character_at_position == current_character:
            current_run_length += 1
        else:
            encoded_segment = f"{current_character}{current_run_length}"
            encoded_parts.append(encoded_segment)
            current_character = character_at_position
            current_run_length = 1

    final_segment = f"{current_character}{current_run_length}"
    encoded_parts.append(final_segment)

    compressed_string = ''.join(encoded_parts)
    return compressed_string


def main():
    """Main function."""
    string_length = 1_000_000
    input_text = generate_input_string(string_length)
    compressed_text = run_length_encode(input_text)
    checksum = hashlib.md5(compressed_text[:1000].encode()).hexdigest()
    print(f"compressed {len(input_text)} -> {len(compressed_text)} chars, checksum={checksum}")


if __name__ == "__main__":
    main()
