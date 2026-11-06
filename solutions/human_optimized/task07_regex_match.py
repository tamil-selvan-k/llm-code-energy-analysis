import random
import hashlib
import re
import string

random.seed(42)
lines = [''.join(random.choices(string.ascii_lowercase + string.digits + ' ', k=random.randint(20, 100))) for _ in range(100_000)]
patterns = [re.compile(p) for p in [r'\b[a-z]{5}\d{3}\b', r'[aeiou]{3,}', r'\d{2,4}[a-z]+\d']]
counts = [sum(1 for line in lines if p.search(line)) for p in patterns]
h = hashlib.md5(str(counts).encode()).hexdigest()
print(f"matched patterns in {len(lines)} lines, counts={counts}, checksum={h}")
