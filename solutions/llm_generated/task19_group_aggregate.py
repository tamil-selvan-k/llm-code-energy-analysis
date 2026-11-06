"""
Task 19: Group-By and Aggregate Benchmark
Performs group-by operations on 500K records with aggregations.
"""

import random
import hashlib
from typing import List, Tuple, Dict, Any
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class AggregateResult:
    """Stores aggregation results for a group."""
    total_sum: float = 0.0
    count: int = 0
    minimum: float = float('inf')
    maximum: float = float('-inf')

    def add_value(self, value: float) -> None:
        """Add a value to the aggregation."""
        self.total_sum += value
        self.count += 1
        if value < self.minimum:
            self.minimum = value
        if value > self.maximum:
            self.maximum = value

    def get_average(self) -> float:
        """Compute the average."""
        if self.count == 0:
            return 0.0
        return self.total_sum / self.count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "avg": self.get_average(),
            "count": self.count,
            "min": self.minimum,
            "max": self.maximum,
        }


def generate_records(num_records: int, seed: int = 42) -> List[Tuple[str, str, float]]:
    """Generate random records with category, region, and value."""
    if num_records <= 0:
        raise ValueError("Number of records must be positive")
    random.seed(seed)
    categories = [f"cat_{i}" for i in range(50)]
    regions = ['north', 'south', 'east', 'west']
    records = []
    for _ in range(num_records):
        category = random.choice(categories)
        region = random.choice(regions)
        value = random.uniform(10, 1000)
        records.append((category, region, value))
    return records


def group_and_aggregate(records: List[Tuple[str, str, float]]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Group records by (category, region) and compute aggregates."""
    if records is None:
        raise ValueError("Records cannot be None")

    group_aggregates: Dict[Tuple[str, str], AggregateResult] = {}

    for category, region, value in records:
        group_key = (category, region)
        if group_key not in group_aggregates:
            group_aggregates[group_key] = AggregateResult()
        group_aggregates[group_key].add_value(value)

    result = {}
    for key in sorted(group_aggregates.keys()):
        result[key] = group_aggregates[key].to_dict()
    return result


def main():
    """Main function."""
    num_records = 500_000
    records = generate_records(num_records)
    result = group_and_aggregate(records)
    checksum = hashlib.md5(str(len(result)).encode()).hexdigest()
    print(f"grouped {len(records)} records into {len(result)} groups, checksum={checksum}")


if __name__ == "__main__":
    main()
