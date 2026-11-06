import random
import hashlib
import string

random.seed(42)
names = [''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 15))) for _ in range(200_000)]

seen = {}
unique = []
for name in names:
    key = name[:3]
    if key not in seen:
        seen[key] = []
    dup = False
    for existing in seen[key]:
        if len(name) == len(existing):
            diff = sum(a != b for a, b in zip(name, existing))
            if diff <= 1:
                dup = True
                break
    if not dup:
        seen[key].append(name)
        unique.append(name)

h = hashlib.md5(str(len(unique)).encode()).hexdigest()
print(f"deduped {len(names)} -> {len(unique)} records, checksum={h}")
