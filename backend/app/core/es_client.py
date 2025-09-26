# backend/app/core/es_client.py


from elasticsearch import Elasticsearch
from .config import ES_HOST, ES_INDEX_PRODUCTS

# es = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))
# INDEX = os.getenv("ES_INDEX_PRODEUCTS", "products")

es = Elasticsearch(ES_HOST)
INDEX = ES_INDEX_PRODUCTS