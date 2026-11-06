import random
import hashlib

random.seed(42)

def make_nested(depth, breadth=3):
    if depth <= 0:
        return random.randint(0, 100)
    return {f"k{i}": make_nested(depth - 1, breadth) for i in range(breadth)}

dicts = [make_nested(random.randint(3, 10), 3) for _ in range(10_000)]

def flatten(d, prefix=''):
    items = []
    stack = [(prefix, d)]
    while stack:
        p, v = stack.pop()
        if isinstance(v, dict):
            for k, val in v.items():
                stack.append((f"{p}.{k}" if p else k, val))
        else:
            items.append((p, v))
    return dict(items)

results = [flatten(d) for d in dicts]
total_keys = sum(len(r) for r in results)
h = hashlib.md5(str(total_keys).encode()).hexdigest()
print(f"flattened {len(dicts)} dicts, total keys={total_keys}, checksum={h}")
