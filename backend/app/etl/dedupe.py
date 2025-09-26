# backend/app/etl/dedupe.py

import orjson, argparse, hashlib
from pathlib import Path

def norm_key(title: str):
    t = "".join(ch for ch in title.lower() if ch.isalnum() or ch.isspace()).strip()
    return hashlib.md5(t.encode()).hexdigest()

def run(in_path: str, out_file: str):
    seen = set()
    out = Path(out_file); out.parent.mkdir(parents=True, exist_ok=True)
    
    with open(out, "wb") as g:
        for fp in Path(in_path).glob("*.jsonl"):
            with open(fp, "rb") as f:
                for line in f:
                    rec = orjson.loads(line)
                    key = norm_key(rec["title"])
                    if key in seen:
                        continue
                    seen.add(key)
                    g.write(orjson.dumps(rec) + b"\n")
    print(f"[dedupe] -> {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_path", default="/data/norm/naver")
    ap.add_argument("--out_file", default="/data/stage/products.jsonl")
    args = ap.parse_args()
    run(args.in_path, args.out_file)