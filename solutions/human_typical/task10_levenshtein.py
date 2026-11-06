import random
import hashlib
import string

random.seed(42)
pairs = []
for _ in range(500):
    a = ''.join(random.choices(string.ascii_lowercase, k=random.randint(80, 120)))
    b = ''.join(random.choices(string.ascii_lowercase, k=random.randint(80, 120)))
    pairs.append((a, b))

def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

distances = []
for a, b in pairs:
    distances.append(levenshtein(a, b))

total = sum(distances)
checksum = hashlib.md5(str(total).encode()).hexdigest()
print(f"computed {len(pairs)} edit distances, total={total}, checksum={checksum}")
