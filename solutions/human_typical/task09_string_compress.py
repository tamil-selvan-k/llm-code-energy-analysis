import random
import hashlib
import string

random.seed(42)
text = ''.join(random.choices(string.ascii_lowercase[:5], k=1_000_000))

result = []
i = 0
while i < len(text):
    current_char = text[i]
    count = 1
    while i + count < len(text) and text[i + count] == current_char:
        count += 1
    result.append(current_char + str(count))
    i += count

compressed = ''.join(result)
checksum = hashlib.md5(compressed[:1000].encode()).hexdigest()
print(f"compressed {len(text)} -> {len(compressed)} chars, checksum={checksum}")
