# backend/app/etl/indexer.py

import os, orjson, argparse, time
from elasticsearch import helpers
from app.core.es_client import es, INDEX
from app.core.embedder import embed_text


def ensure_index(mapping_path: str):
    if es.indices.exists(index=INDEX):
        return
    with open(mapping_path, "r", encoding="utf-8") as f:
        body = f.read()
    es.indices.create(index=INDEX, body=body)
    print(f"[index] created {INDEX}")

def run(src_file: str, mapping_path: str):
    ensure_index(mapping_path)
    docs = []
    titles = []

    with open(src_file, "rb") as f:
        for line in f:
            rec = orjson.loads(line)
            docs.append(rec); titles.append(rec["title"])
    vecs = embed_text(titles)

    def gen_actions():
        for rec, vec in zip(docs, vecs):
            _id = rec["id"] or f'{rec["source"]}_{hash(rec["title"])}'
            rec["title_vector"] = vec
            rec["updated_at"] = int(time.time()*1000)
            yield {"_op_type":"index", "_index":INDEX, "_id":_id, "_source":rec}

    helpers.bulk(es, gen_actions(), chunk_size=500)
    es.indices.refresh(index=INDEX)
    print(f"[index] indexed {len(docs)} docs -> {INDEX}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_file", default="/data/stage/products.jsonl")
    ap.add_argument("--mapping_path", default="/app/../../search/es/mappings/products.json")
    args = ap.parse_args()
    run(args.src_file, args.mapping_path)