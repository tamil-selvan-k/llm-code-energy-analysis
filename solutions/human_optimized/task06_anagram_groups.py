import random
import hashlib
import string
from collections import defaultdict

random.seed(42)
words = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(50_000)]
groups = defaultdict(list)
for w in words:
    groups[''.join(sorted(w))].append(w)
num_groups = len(groups)
max_group = max(len(v) for v in groups.values())
h = hashlib.md5(f"{num_groups}-{max_group}".encode()).hexdigest()
print(f"{num_groups} anagram groups, largest={max_group}, checksum={h}")
