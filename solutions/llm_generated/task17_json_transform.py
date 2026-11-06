"""
Task 17: JSON Transformation Benchmark
Transforms 50K nested JSON records into a flat structure.
"""

import random
import hashlib
import json
from typing import List, Dict, Any


def generate_nested_records(num_records: int, seed: int = 42) -> List[Dict[str, Any]]:
    """Generate nested JSON-like records."""
    if num_records <= 0:
        raise ValueError("Number of records must be positive")
    random.seed(seed)
    records = []
    for record_id in range(num_records):
        record = {
            "id": record_id,
            "name": f"user_{record_id}",
            "attrs": {
                "score": random.randint(0, 100),
                "level": random.choice(["a", "b", "c"]),
                "tags": [random.choice(["x", "y", "z"]) for _ in range(3)]
            }
        }
        records.append(record)
    return records


def transform_record(input_record: Dict[str, Any]) -> Dict[str, Any]:
    """Transform a single nested record into a flat structure.

    Args:
        input_record: Nested record with id, name, and attrs

    Returns:
        Flattened record
    """
    if input_record is None:
        raise ValueError("Record cannot be None")

    record_id = input_record.get("id")
    attributes = input_record.get("attrs", {})
    score_value = attributes.get("score", 0)
    level_value = attributes.get("level", "")
    tags_list = attributes.get("tags", [])
    tags_string = ",".join(tags_list)
    is_high_score = score_value > 75

    transformed = {
        "uid": record_id,
        "score": score_value,
        "level": level_value,
        "tag_str": tags_string,
        "high": is_high_score,
    }
    return transformed


def transform_all_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transform all records."""
    transformed_records = []
    for record in records:
        transformed_record = transform_record(record)
        transformed_records.append(transformed_record)
    return transformed_records


def main():
    """Main function."""
    num_records = 50_000
    records = generate_nested_records(num_records)
    transformed = transform_all_records(records)
    sample_json = json.dumps(transformed[:5])
    checksum = hashlib.md5(sample_json.encode()).hexdigest()
    print(f"transformed {len(transformed)} records, checksum={checksum}")


if __name__ == "__main__":
    main()
