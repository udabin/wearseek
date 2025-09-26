# backend/app/etl/normalize.py

import re, argparse, orjson
from pathlib import Path


COLOR_MAP = {
  "블랙":"BLACK","검정":"BLACK","black":"BLACK","화이트":"WHITE","하양":"WHITE",
  "네이비":"NAVY","남색":"NAVY","그레이":"GRAY","회색":"GRAY","레드":"RED","빨강":"RED",
}
BRAND_RX = re.compile(r"\b([A-Za-z][A-Za-z0-9\-]{1,})\b")


def norm_color(title: str):
    for k,v in COLOR_MAP.items():
        if k in title:
            return v
    return None

def extract_brand(title: str):
    m = BRAND_RX.search(title)
    return m.group(1).upper() if m else None

def run(in_path: str, out_path: str):
    inp = Path(in_path); out = Path(out_path)
    out.mkdir(parents=True, exist_ok=True)
    
    for fp in inp.glob("*.jsonl"):
        dst = out / fp.name
        with open(fp, "rb") as f, open(dst, "wb") as g:
            for line in f:
                src = orjson.loads(line)
                title = re.sub(r"<[^>]+>","", src.get("title","")).strip()
                price = float(src.get("lprice") or 0.0)
                rec = {
                    "id": src.get("productId") or src.get("productId",""),
                    "source": "naver",
                    "title": title,
                    "brand": extract_brand(title),
                    "price": price,
                    "currency": "KRW",
                    "category_std": "TOPS" # 초안
                    "color_std": norm_color(title),
                    "size_std": None,
                    "url": src.get("link"),
                    "image_url": src.get("image"),
                    "in_stock": True
                }
                g.write(orjson.dumps(rec) + b"\n")
        
        print(f"[normalize] -> {dst}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_path", default="/data/raw/naver")
    ap.add_argument("--out_path", default="/data/norm/naver")
    args = ap.parse_args()
    run(args.in_path, args.out_path)
