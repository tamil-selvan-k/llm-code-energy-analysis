"""
Task 11: Matrix Multiplication Benchmark
Multiplies two 300x300 matrices using pure Python (no numpy).
"""

import random
import hashlib
from typing import List

Matrix = List[List[float]]


def generate_random_matrix(rows: int, cols: int, seed: int = None) -> Matrix:
    """Generate a random matrix with values between 0 and 1."""
    if rows <= 0 or cols <= 0:
        raise ValueError("Dimensions must be positive")
    if seed is not None:
        random.seed(seed)
    matrix = []
    for row_index in range(rows):
        row = []
        for col_index in range(cols):
            value = random.random()
            row.append(value)
        matrix.append(row)
    return matrix


def create_zero_matrix(rows: int, cols: int) -> Matrix:
    """Create a matrix filled with zeros."""
    zero_matrix = []
    for _ in range(rows):
        row = [0.0] * cols
        zero_matrix.append(row)
    return zero_matrix


def multiply_matrices(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """Multiply two matrices using the standard O(n^3) algorithm.

    Args:
        matrix_a: First matrix (m x n)
        matrix_b: Second matrix (n x p)

    Returns:
        Result matrix (m x p)
    """
    if matrix_a is None or matrix_b is None:
        raise ValueError("Matrices cannot be None")

    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])

    if cols_a != rows_b:
        raise ValueError(f"Incompatible dimensions: {rows_a}x{cols_a} and {rows_b}x{cols_b}")

    result_matrix = create_zero_matrix(rows_a, cols_b)

    for i in range(rows_a):
        for j in range(cols_b):
            dot_product_sum = 0.0
            for k in range(cols_a):
                element_a = matrix_a[i][k]
                element_b = matrix_b[k][j]
                product = element_a * element_b
                dot_product_sum += product
            result_matrix[i][j] = dot_product_sum

    return result_matrix


def main():
    """Main function."""
    matrix_size = 300
    random.seed(42)
    matrix_a = generate_random_matrix(matrix_size, matrix_size)
    matrix_b = generate_random_matrix(matrix_size, matrix_size)
    result = multiply_matrices(matrix_a, matrix_b)
    checksum = hashlib.md5(f"{result[0][0]:.6f},{result[matrix_size-1][matrix_size-1]:.6f}".encode()).hexdigest()
    print(f"multiplied {matrix_size}x{matrix_size} matrices, checksum={checksum}")


if __name__ == "__main__":
    main()
