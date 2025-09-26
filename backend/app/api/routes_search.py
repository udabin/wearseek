from fastapi import APIRouter, Query
from app.core.es_client import es, INDEX
from app.core.embedder import embed_text

router = APIRouter()

@router.get("/search")
def search(q: str = Query(..., min_length=1), size: int = 20):
    # 1) BM25
    bm25 = {
        "size" : size,
        "query" : {"multi_match": {"query": q,
            "fields": ["title^2", "brand", "category_std"]}}
    }
    hits_bm25 = es.search(index=INDEX, body=bm25)["hits"]["hits"]

    # 2) kNN (dense_vector)
    vec = embed_text([q])[0]
    knn = {
        "knn": {"field": "title_vector",
                "query_vector": vec,
                "k": size,
                "num_candidates": max(100, size*5)}
    }
    hits_knn = es.search(index=INDEX, body=knn)["hits"]["hits"]

    # 3) 간단한 RRF 머지 (가중 합도 가능) -> 상위 K 반환 (BM25 우선)
    merged = {} 
    # { h["_id"]: (1000/(10+i)) for i,h in enumerate(hits_bm25) }
    for i,h in enumerate(hits_bm25):
        merged[h["_id"]] = merged.get(h["_id"],0) + 1000/(10+i+1)
    for i,h in enumerate(hits_knn):
        merged[h["_id"]] = merged.get(h["_id"], 0) + 1000/(10+i+1)
    
    # 스코어에 따라 sort
    ids_sorted = sorted(merged.items(), key=lambda x: x[1], reverse=True)[:size]
    res = [es.get(index=INDEX, id=_id)["_source"] | {"_id": _id, "_score": sc} for _id, sc in ids_sorted]
    return {"query": q, "count": len(res), "items": res}


@router.get("/similar")
def similar(id: str, size: int = 12):
    doc = es.get(index=INDEX, id=id)["_source"]
    vec = doc.get("title_vector")
    body = { "knn": { "field": "title_vector",
            "query_vector": vec,
            "k": size+1,
            "num_candidates": 100 }}
    hits = es.search(index=INDEX, body=body)["hits"]["hits"]
    items = [h for h in hits if h["_id"] != id][:size]
    return {"base_id": id, "items": [x["_source"] | {"_id": x["_id"], "_score": x["_score"]} for x in items]}
    