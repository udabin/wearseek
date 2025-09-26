# backend/app/core/embedder.py

import os
from sentence_transformers import SentenceTransformer
from .config import EMBED_MODEL

# _model = SentenceTransformer(os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
_model = SentenceTransforemr(EMBED_MODEL)

def embed_text(xs: list[str]):
    return _model.encode(xs, normalize_embeddings=True).tolist()
    