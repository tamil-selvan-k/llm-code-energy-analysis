"""
Task 14: Newton's Method Square Root Benchmark
Computes square roots for 100K numbers using Newton's method (Babylonian method).
"""

import random
import hashlib
from typing import List


def generate_random_numbers(count: int, min_val: float = 1.0, max_val: float = 1_000_000.0, seed: int = 42) -> List[float]:
    """Generate random floating-point numbers."""
    if count <= 0:
        raise ValueError("Count must be positive")
    random.seed(seed)
    return [random.uniform(min_val, max_val) for _ in range(count)]


def newton_square_root(number: float, tolerance: float = 1e-10, max_iterations: int = 1000) -> float:
    """Compute square root using Newton's method (Babylonian method).

    Args:
        number: The number to compute the square root of
        tolerance: Convergence tolerance
        max_iterations: Maximum number of iterations

    Returns:
        Approximate square root

    Raises:
        ValueError: If number is negative
    """
    if number < 0:
        raise ValueError("Cannot compute square root of negative number")
    if number == 0:
        return 0.0

    initial_guess = number / 2.0
    current_guess = initial_guess

    for iteration in range(max_iterations):
        next_guess = (current_guess + number / current_guess) / 2.0
        difference = abs(next_guess - current_guess)

        if difference < tolerance:
            return next_guess

        current_guess = next_guess

    return current_guess


def compute_all_square_roots(numbers: List[float]) -> List[float]:
    """Compute square roots for all numbers in the list."""
    square_root_results = []
    for number in numbers:
        sqrt_value = newton_square_root(number)
        square_root_results.append(sqrt_value)
    return square_root_results


def main():
    """Main function."""
    num_values = 100_000
    numbers = generate_random_numbers(num_values)
    results = compute_all_square_roots(numbers)
    checksum = hashlib.md5(f"{results[0]:.10f},{results[-1]:.10f}".encode()).hexdigest()
    print(f"computed sqrt for {len(numbers)} numbers, checksum={checksum}")


if __name__ == "__main__":
    main()
