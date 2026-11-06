import hashlib

def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fibs = fibonacci(10_000)
last_str = str(fibs[-1])
checksum = hashlib.md5(last_str[:100].encode()).hexdigest()
print(f"computed {len(fibs)} fibonacci numbers, digits in last={len(last_str)}, checksum={checksum}")
