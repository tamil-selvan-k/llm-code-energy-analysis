"""
Task 18: Fuzzy Deduplication Benchmark
Deduplicates 200K records using simple string similarity.
Two records are considered duplicates if they have the same length
and differ by at most 1 character.
"""

import random
import hashlib
import string
from typing import List, Dict, Tuple


def generate_records(num_records: int, min_length: int = 5, max_length: int = 15, seed: int = 42) -> List[str]:
    """Generate random name records."""
    if num_records <= 0:
        raise ValueError("Number of records must be positive")
    random.seed(seed)
    records = []
    for _ in range(num_records):
        name_length = random.randint(min_length, max_length)
        characters = random.choices(string.ascii_lowercase, k=name_length)
        name = ''.join(characters)
        records.append(name)
    return records


def compute_string_similarity(string_a: str, string_b: str) -> bool:
    """Check if two strings are similar (differ by at most 1 character).

    Args:
        string_a: First string
        string_b: Second string

    Returns:
        True if strings are similar
    """
    if string_a is None or string_b is None:
        return False
    if len(string_a) != len(string_b):
        return False

    difference_count = 0
    for index in range(len(string_a)):
        if string_a[index] != string_b[index]:
            difference_count += 1
            if difference_count > 1:
                return False
    return True


def deduplicate_records(records: List[str]) -> List[str]:
    """Remove fuzzy duplicates from the record list.

    Uses bucketing by (length, first 3 chars) for efficiency.
    """
    if records is None:
        raise ValueError("Records cannot be None")

    buckets: Dict[Tuple, List[str]] = {}
    unique_records: List[str] = []

    for record in records:
        bucket_key = (len(record), record[:3])

        if bucket_key not in buckets:
            buckets[bucket_key] = []

        is_duplicate = False
        for existing_record in buckets[bucket_key]:
            if compute_string_similarity(record, existing_record):
                is_duplicate = True
                break

        if not is_duplicate:
            buckets[bucket_key].append(record)
            unique_records.append(record)

    return unique_records


def main():
    """Main function."""
    num_records = 200_000
    records = generate_records(num_records)
    unique = deduplicate_records(records)
    checksum = hashlib.md5(str(len(unique)).encode()).hexdigest()
    print(f"deduped {len(records)} -> {len(unique)} records, checksum={checksum}")


if __name__ == "__main__":
    main()
