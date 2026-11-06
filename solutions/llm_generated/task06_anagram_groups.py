"""
Task 06: Anagram Grouping Benchmark
Groups 50K randomly generated words into anagram groups.
Two words are anagrams if they contain the same characters.
"""

import random
import hashlib
import string
from typing import List, Dict
from collections import defaultdict


def generate_random_words(num_words: int, min_length: int = 3, max_length: int = 8, seed: int = 42) -> List[str]:
    """Generate random words for anagram grouping."""
    if num_words <= 0:
        raise ValueError("Number of words must be positive")
    random.seed(seed)
    word_list = []
    for _ in range(num_words):
        word_length = random.randint(min_length, max_length)
        characters = random.choices(string.ascii_lowercase, k=word_length)
        word = ''.join(characters)
        word_list.append(word)
    return word_list


def compute_anagram_key(word: str) -> str:
    """Compute the canonical key for anagram detection."""
    if not isinstance(word, str):
        raise TypeError("Input must be a string")
    sorted_characters = sorted(word.lower())
    canonical_key = ''.join(sorted_characters)
    return canonical_key


def group_anagrams(words: List[str]) -> Dict[str, List[str]]:
    """Group words by their anagram equivalence class."""
    if words is None:
        raise ValueError("Word list cannot be None")
    anagram_groups = defaultdict(list)
    for word in words:
        anagram_key = compute_anagram_key(word)
        anagram_groups[anagram_key].append(word)
    return dict(anagram_groups)


def find_largest_group_size(groups: Dict[str, List[str]]) -> int:
    """Find the size of the largest anagram group."""
    if not groups:
        return 0
    largest_size = 0
    for key, group_members in groups.items():
        current_size = len(group_members)
        if current_size > largest_size:
            largest_size = current_size
    return largest_size


def main():
    """Main function."""
    num_words = 50_000
    words = generate_random_words(num_words)
    anagram_groups = group_anagrams(words)
    num_groups = len(anagram_groups)
    max_group = find_largest_group_size(anagram_groups)
    checksum = hashlib.md5(f"{num_groups}-{max_group}".encode()).hexdigest()
    print(f"{num_groups} anagram groups, largest={max_group}, checksum={checksum}")


if __name__ == "__main__":
    main()
