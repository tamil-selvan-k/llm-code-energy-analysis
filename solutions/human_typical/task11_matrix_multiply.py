import random
import hashlib

random.seed(42)
N = 300
A = [[random.random() for _ in range(N)] for _ in range(N)]
B = [[random.random() for _ in range(N)] for _ in range(N)]

C = [[0.0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        total = 0.0
        for k in range(N):
            total += A[i][k] * B[k][j]
        C[i][j] = total

checksum = hashlib.md5(f"{C[0][0]:.6f},{C[N-1][N-1]:.6f}".encode()).hexdigest()
print(f"multiplied {N}x{N} matrices, checksum={checksum}")
