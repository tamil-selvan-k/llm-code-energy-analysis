import random
import hashlib
import string

random.seed(42)
names = []
for _ in range(200_000):
    length = random.randint(5, 15)
    name = ''.join(random.choices(string.ascii_lowercase, k=length))
    names.append(name)

def is_similar(a, b):
    if len(a) != len(b):
        return False
    diffs = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            diffs += 1
            if diffs > 1:
                return False
    return True

buckets = {}
unique = []
for name in names:
    key = (len(name), name[0])
    if key not in buckets:
        buckets[key] = []
    is_dup = False
    for existing in buckets[key]:
        if is_similar(name, existing):
            is_dup = True
            break
    if not is_dup:
        buckets[key].append(name)
        unique.append(name)

checksum = hashlib.md5(str(len(unique)).encode()).hexdigest()
print(f"deduped {len(names)} -> {len(unique)} records, checksum={checksum}")
