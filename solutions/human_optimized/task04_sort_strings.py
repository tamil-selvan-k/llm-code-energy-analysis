import random
import hashlib
import string

random.seed(42)
data = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 20))) for _ in range(50_000)]
data.sort(key=lambda s: (len(s), s))
h = hashlib.md5(''.join(data[:50]).encode()).hexdigest()
print(f"sorted {len(data)} strings, checksum={h}")
