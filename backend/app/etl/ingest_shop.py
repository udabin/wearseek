# backend/app/etl/ingest_shop.py

import os, orjson, argparse
from pathlib import Path
from .naver_client import paginate

def main():
    ap = argparse.ArgumetnParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--out", default="/data/raw/naver")
    args = ap.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"{args.query}.jsonl"

    with open(outfile, "wb") as f:
        for item in paginate(args.query, args.limit):
            f.write(orjson.dumps(item) + b"\n")
    
    print(f"[ingest] saved -> {outfile}")

if __name__ == "__main__":
    main()