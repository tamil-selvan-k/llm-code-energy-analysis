"""
Task 20: Dictionary Flattening Benchmark
Flattens 10K deeply nested dict structures (depth up to 10).
"""

import random
import hashlib
from typing import Any, Dict, List, Union


def generate_nested_dictionary(depth: int, breadth: int = 3) -> Union[Dict[str, Any], int]:
    """Generate a nested dictionary with specified depth and breadth.

    Args:
        depth: How deep to nest
        breadth: Number of keys per level

    Returns:
        Nested dictionary or leaf integer value
    """
    if depth <= 0:
        return random.randint(0, 100)

    nested_dict: Dict[str, Any] = {}
    for index in range(breadth):
        key_name = f"k{index}"
        nested_value = generate_nested_dictionary(depth - 1, breadth)
        nested_dict[key_name] = nested_value

    return nested_dict


def flatten_dictionary(nested_dict: Dict[str, Any], key_prefix: str = '', separator: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary into a single-level dictionary.

    Args:
        nested_dict: The dictionary to flatten
        key_prefix: Prefix for keys (used in recursion)
        separator: Separator between nested key levels

    Returns:
        Flattened dictionary with dot-separated keys
    """
    if nested_dict is None:
        raise ValueError("Input dictionary cannot be None")

    flattened_result: Dict[str, Any] = {}

    for current_key, current_value in nested_dict.items():
        if key_prefix:
            new_key = f"{key_prefix}{separator}{current_key}"
        else:
            new_key = current_key

        if isinstance(current_value, dict):
            nested_flattened = flatten_dictionary(current_value, new_key, separator)
            for nested_key, nested_val in nested_flattened.items():
                flattened_result[nested_key] = nested_val
        else:
            flattened_result[new_key] = current_value

    return flattened_result


def generate_test_dictionaries(count: int, seed: int = 42) -> List[Dict[str, Any]]:
    """Generate test dictionaries with varying depths."""
    random.seed(seed)
    test_dicts = []
    for _ in range(count):
        depth = random.randint(3, 10)
        nested_dict = generate_nested_dictionary(depth, 3)
        test_dicts.append(nested_dict)
    return test_dicts


def main():
    """Main function."""
    num_dicts = 10_000
    test_dicts = generate_test_dictionaries(num_dicts)

    flattened_results = []
    for nested_dict in test_dicts:
        flattened = flatten_dictionary(nested_dict)
        flattened_results.append(flattened)

    total_keys = 0
    for result in flattened_results:
        total_keys += len(result)

    checksum = hashlib.md5(str(total_keys).encode()).hexdigest()
    print(f"flattened {len(test_dicts)} dicts, total keys={total_keys}, checksum={checksum}")


if __name__ == "__main__":
    main()
