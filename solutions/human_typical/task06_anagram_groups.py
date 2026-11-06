import random
import hashlib
import string

random.seed(42)
words = []
for _ in range(50_000):
    length = random.randint(3, 8)
    word = ''.join(random.choices(string.ascii_lowercase, k=length))
    words.append(word)

groups = {}
for word in words:
    key = ''.join(sorted(word))
    if key not in groups:
        groups[key] = []
    groups[key].append(word)

num_groups = len(groups)
max_group = 0
for key in groups:
    if len(groups[key]) > max_group:
        max_group = len(groups[key])

checksum = hashlib.md5(f"{num_groups}-{max_group}".encode()).hexdigest()
print(f"{num_groups} anagram groups, largest={max_group}, checksum={checksum}")
