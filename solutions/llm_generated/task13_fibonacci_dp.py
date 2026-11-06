"""
Task 13: Fibonacci Sequence with Dynamic Programming
Computes the first 10,000 Fibonacci numbers using dynamic programming.
These are arbitrary-precision (big) integers.
"""

import hashlib
from typing import List


def compute_fibonacci_sequence(num_terms: int) -> List[int]:
    """Compute the Fibonacci sequence using dynamic programming.

    Args:
        num_terms: Number of Fibonacci numbers to compute

    Returns:
        List of Fibonacci numbers

    Raises:
        ValueError: If num_terms is not positive
    """
    if num_terms <= 0:
        raise ValueError("Number of terms must be positive")

    if num_terms == 1:
        return [0]

    fibonacci_sequence: List[int] = [0, 1]

    for term_index in range(2, num_terms):
        previous_term = fibonacci_sequence[term_index - 1]
        term_before_previous = fibonacci_sequence[term_index - 2]
        next_fibonacci_number = previous_term + term_before_previous
        fibonacci_sequence.append(next_fibonacci_number)

    return fibonacci_sequence


def main():
    """Main function."""
    number_of_terms = 10_000
    fibonacci_numbers = compute_fibonacci_sequence(number_of_terms)
    last_number = fibonacci_numbers[-1]
    last_number_string = str(last_number)
    num_digits = len(last_number_string)
    checksum = hashlib.md5(last_number_string[:100].encode()).hexdigest()
    print(f"computed {len(fibonacci_numbers)} fibonacci numbers, digits in last={num_digits}, checksum={checksum}")


if __name__ == "__main__":
    main()
