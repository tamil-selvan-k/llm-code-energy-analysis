import random
import hashlib
import json

random.seed(42)
records = [{"id": i, "name": f"user_{i}", "attrs": {"score": random.randint(0, 100), "level": random.choice(["a", "b", "c"]), "tags": [random.choice(["x", "y", "z"]) for _ in range(3)]}} for i in range(50_000)]

transformed = [{"uid": r["id"], "score": r["attrs"]["score"], "level": r["attrs"]["level"], "tag_str": ",".join(r["attrs"]["tags"]), "high": r["attrs"]["score"] > 75} for r in records]

h = hashlib.md5(json.dumps(transformed[:5]).encode()).hexdigest()
print(f"transformed {len(transformed)} records, checksum={h}")
