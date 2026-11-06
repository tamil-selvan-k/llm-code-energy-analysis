"""
Task 15: Statistical Measures Benchmark
Computes mean, variance, standard deviation, skewness, and kurtosis for 1M numbers.
"""

import random
import hashlib
import math
from typing import List, Dict


class StatisticalCalculator:
    """Calculator for common statistical measures."""

    def __init__(self, data: List[float]):
        """Initialize with data."""
        if data is None or len(data) == 0:
            raise ValueError("Data must not be empty")
        self._data = data
        self._n = len(data)
        self._mean = None
        self._variance = None
        self._std_dev = None
        self._skewness = None
        self._kurtosis = None

    def compute_mean(self) -> float:
        """Compute the arithmetic mean."""
        if self._mean is None:
            total_sum = 0.0
            for value in self._data:
                total_sum += value
            self._mean = total_sum / self._n
        return self._mean

    def compute_variance(self) -> float:
        """Compute the population variance."""
        if self._variance is None:
            mean_value = self.compute_mean()
            sum_of_squared_differences = 0.0
            for value in self._data:
                difference = value - mean_value
                squared_difference = difference ** 2
                sum_of_squared_differences += squared_difference
            self._variance = sum_of_squared_differences / self._n
        return self._variance

    def compute_standard_deviation(self) -> float:
        """Compute the population standard deviation."""
        if self._std_dev is None:
            variance_value = self.compute_variance()
            self._std_dev = math.sqrt(variance_value)
        return self._std_dev

    def compute_skewness(self) -> float:
        """Compute the skewness (third standardized moment)."""
        if self._skewness is None:
            mean_value = self.compute_mean()
            std_dev_value = self.compute_standard_deviation()
            if std_dev_value == 0:
                self._skewness = 0.0
            else:
                sum_cubed_diff = 0.0
                for value in self._data:
                    difference = value - mean_value
                    cubed_difference = difference ** 3
                    sum_cubed_diff += cubed_difference
                third_moment = sum_cubed_diff / self._n
                self._skewness = third_moment / (std_dev_value ** 3)
        return self._skewness

    def compute_kurtosis(self) -> float:
        """Compute the excess kurtosis (fourth standardized moment minus 3)."""
        if self._kurtosis is None:
            mean_value = self.compute_mean()
            std_dev_value = self.compute_standard_deviation()
            if std_dev_value == 0:
                self._kurtosis = 0.0
            else:
                sum_fourth_diff = 0.0
                for value in self._data:
                    difference = value - mean_value
                    fourth_power = difference ** 4
                    sum_fourth_diff += fourth_power
                fourth_moment = sum_fourth_diff / self._n
                self._kurtosis = fourth_moment / (std_dev_value ** 4) - 3
        return self._kurtosis

    def compute_all_statistics(self) -> Dict[str, float]:
        """Compute all statistical measures."""
        return {
            "mean": self.compute_mean(),
            "variance": self.compute_variance(),
            "std_dev": self.compute_standard_deviation(),
            "skewness": self.compute_skewness(),
            "kurtosis": self.compute_kurtosis(),
        }


def generate_data(count: int, mean: float = 100, std: float = 25, seed: int = 42) -> List[float]:
    """Generate random Gaussian data."""
    random.seed(seed)
    return [random.gauss(mean, std) for _ in range(count)]


def main():
    """Main function."""
    n = 1_000_000
    data = generate_data(n)
    calculator = StatisticalCalculator(data)
    stats = calculator.compute_all_statistics()
    checksum = hashlib.md5(
        f"{stats['mean']:.6f},{stats['variance']:.6f},{stats['std_dev']:.6f},{stats['skewness']:.6f},{stats['kurtosis']:.6f}".encode()
    ).hexdigest()
    print(f"stats for {n} values: mean={stats['mean']:.4f}, var={stats['variance']:.4f}, std={stats['std_dev']:.4f}, skew={stats['skewness']:.4f}, kurt={stats['kurtosis']:.4f}, checksum={checksum}")


if __name__ == "__main__":
    main()
