"""
Task 07: Regex Pattern Matching Benchmark
Matches multiple complex regex patterns across 100K lines of generated text.
"""

import random
import hashlib
import re
import string
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PatternResult:
    """Stores the result of a pattern match operation."""
    pattern_string: str
    match_count: int


def generate_text_lines(num_lines: int, min_length: int = 20, max_length: int = 100, seed: int = 42) -> List[str]:
    """Generate random text lines for pattern matching."""
    if num_lines <= 0:
        raise ValueError("Number of lines must be positive")
    random.seed(seed)
    character_set = string.ascii_lowercase + string.digits + ' '
    text_lines = []
    for _ in range(num_lines):
        line_length = random.randint(min_length, max_length)
        characters = random.choices(character_set, k=line_length)
        text_line = ''.join(characters)
        text_lines.append(text_line)
    return text_lines


def get_patterns() -> List[str]:
    """Return the list of regex patterns to match."""
    patterns = [
        r'\b[a-z]{5}\d{3}\b',
        r'[aeiou]{3,}',
        r'\d{2,4}[a-z]+\d',
    ]
    return patterns


def count_matches_for_pattern(text_lines: List[str], pattern_string: str) -> int:
    """Count how many lines match a given pattern."""
    compiled_pattern = re.compile(pattern_string)
    match_count = 0
    for line in text_lines:
        search_result = compiled_pattern.search(line)
        if search_result is not None:
            match_count += 1
    return match_count


def run_all_pattern_matches(text_lines: List[str], patterns: List[str]) -> List[PatternResult]:
    """Run all pattern matches and return results."""
    results = []
    for pattern_string in patterns:
        count = count_matches_for_pattern(text_lines, pattern_string)
        result = PatternResult(pattern_string=pattern_string, match_count=count)
        results.append(result)
    return results


def main():
    """Main function."""
    num_lines = 100_000
    text_lines = generate_text_lines(num_lines)
    patterns = get_patterns()
    results = run_all_pattern_matches(text_lines, patterns)
    counts = [r.match_count for r in results]
    checksum = hashlib.md5(str(counts).encode()).hexdigest()
    print(f"matched patterns in {len(text_lines)} lines, counts={counts}, checksum={checksum}")


if __name__ == "__main__":
    main()
