import random
import hashlib

random.seed(42)

def make_nested(depth, breadth=3):
    if depth <= 0:
        return random.randint(0, 100)
    result = {}
    for i in range(breadth):
        result[f"k{i}"] = make_nested(depth - 1, breadth)
    return result

dicts = []
for _ in range(10_000):
    depth = random.randint(3, 10)
    dicts.append(make_nested(depth, 3))

def flatten(d, prefix=''):
    result = {}
    for key, value in d.items():
        new_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            nested = flatten(value, new_key)
            result.update(nested)
        else:
            result[new_key] = value
    return result

results = []
for d in dicts:
    results.append(flatten(d))

total_keys = 0
for r in results:
    total_keys += len(r)

checksum = hashlib.md5(str(total_keys).encode()).hexdigest()
print(f"flattened {len(dicts)} dicts, total keys={total_keys}, checksum={checksum}")
