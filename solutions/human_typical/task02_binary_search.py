import random
import hashlib

random.seed(42)
data = [random.randint(0, 10_000_000) for _ in range(1_000_000)]
data.sort()
queries = [random.randint(0, 10_000_000) for _ in range(10_000)]

def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

results = []
for q in queries:
    results.append(1 if binary_search(data, q) else 0)

found = sum(results)
checksum = hashlib.md5(str(found).encode()).hexdigest()
print(f"searched {len(queries)} queries in {len(data)} elements, found={found}, checksum={checksum}")
