import random
import hashlib
import json

random.seed(42)
records = []
for i in range(50_000):
    record = {
        "id": i,
        "name": f"user_{i}",
        "attrs": {
            "score": random.randint(0, 100),
            "level": random.choice(["a", "b", "c"]),
            "tags": [random.choice(["x", "y", "z"]) for _ in range(3)]
        }
    }
    records.append(record)

transformed = []
for record in records:
    new_record = {
        "uid": record["id"],
        "score": record["attrs"]["score"],
        "level": record["attrs"]["level"],
        "tag_str": ",".join(record["attrs"]["tags"]),
        "high": record["attrs"]["score"] > 75
    }
    transformed.append(new_record)

sample = json.dumps(transformed[:5])
checksum = hashlib.md5(sample.encode()).hexdigest()
print(f"transformed {len(transformed)} records, checksum={checksum}")
