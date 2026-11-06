import hashlib

def fib_seq(n):
    a, b = 0, 1
    result = [a]
    for _ in range(n - 1):
        a, b = b, a + b
        result.append(a)
    return result

fibs = fib_seq(10_000)
h = hashlib.md5(str(fibs[-1])[:100].encode()).hexdigest()
print(f"computed {len(fibs)} fibonacci numbers, digits in last={len(str(fibs[-1]))}, checksum={h}")
