"""
Task 12: Sieve of Eratosthenes Benchmark
Finds all prime numbers up to 1,000,000.
"""

import hashlib
import math
from typing import List


def sieve_of_eratosthenes(upper_limit: int) -> List[int]:
    """Find all prime numbers up to the given limit using the Sieve of Eratosthenes.

    Args:
        upper_limit: The upper bound for prime number search

    Returns:
        List of all prime numbers up to upper_limit
    """
    if upper_limit < 2:
        return []

    is_prime_number = [True] * (upper_limit + 1)
    is_prime_number[0] = False
    is_prime_number[1] = False

    square_root_limit = int(math.sqrt(upper_limit))

    for current_number in range(2, square_root_limit + 1):
        if is_prime_number[current_number]:
            multiple = current_number * current_number
            while multiple <= upper_limit:
                is_prime_number[multiple] = False
                multiple += current_number

    prime_numbers = []
    for number in range(2, upper_limit + 1):
        if is_prime_number[number]:
            prime_numbers.append(number)

    return prime_numbers


def main():
    """Main function."""
    limit = 1_000_000
    prime_numbers = sieve_of_eratosthenes(limit)
    total_primes = len(prime_numbers)
    largest_prime = prime_numbers[-1] if prime_numbers else 0
    checksum = hashlib.md5(f"{total_primes}-{largest_prime}".encode()).hexdigest()
    print(f"found {total_primes} primes up to {limit}, last={largest_prime}, checksum={checksum}")


if __name__ == "__main__":
    main()
