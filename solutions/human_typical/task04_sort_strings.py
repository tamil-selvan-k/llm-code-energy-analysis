import random
import hashlib
import string

random.seed(42)
strings = []
for i in range(50_000):
    length = random.randint(3, 20)
    s = ''.join(random.choices(string.ascii_lowercase, k=length))
    strings.append(s)

sorted_strings = sorted(strings, key=lambda s: (len(s), s))

first_50 = sorted_strings[:50]
checksum = hashlib.md5(''.join(first_50).encode()).hexdigest()
print(f"sorted {len(sorted_strings)} strings, checksum={checksum}")
