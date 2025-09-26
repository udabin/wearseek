# backend/app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_INDEX_PRODUCTS = os.getenv("ES_INDEX_PRODUCTS", "products")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")