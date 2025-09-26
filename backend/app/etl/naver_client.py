# backend/app/etl/naver_client.py

import os, httpx, math
from typing import Iterator, Dict, Any
from app.core.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

BASE = "https://openapi.naver.com/v1/search/shop.json"

def search_shop(query: str, display: int = 50, start: int = 1) -> Dict[str, Any]:
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        }
    params = {"query": query, "display": display, "start": start, "sort": "sim"}
    with httpx.Client(timeout=10) as c:
        r = c.get(BASE, headers=headers, params=params)
        r.raise_for_status()
        return r.json()

def paginate(query: str, max_items: int = 200) -> Iterator[Dict[str, Any]]:
    got = 0
    start = 1
    while got < max_items:
        batch = min(50, max_items - got)
        data = search_shop(query, display=batch, start=start)
        items = data.get("items", [])
        
        if not items:
            break

        for it in items:
            yield it
        
        got += len(items)
        start += batch