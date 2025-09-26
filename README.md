# WearSeek – 패션 메타 서치엔진 (Naver Shopping + Hybrid Search)

> 네이버 쇼핑 API를 기반으로 한 **패션 상품 메타 서치엔진**.  
> BM25 + 벡터검색(임베딩) **하이브리드 검색**, 중복 제거, 속성 정규화, 재랭킹까지 확장 가능.  
> ML 엔지니어링 포트폴리오를 염두에 둔 구조입니다.

## ✨ 핵심 기능
- **데이터 수집**: Naver Shopping Open API
- **정규화/클린징**: 브랜드/색상 간이 표준화, HTML 태그 제거, 중복 제거
- **검색 인덱스**: Elasticsearch (BM25 + dense_vector kNN)
- **하이브리드 검색**: BM25 후보 + 임베딩 kNN 후보 → RRF 머지
- **API**: FastAPI `/api/search`, `/api/similar`, `/api/health`
- **확장**: Cross-Encoder 재랭킹, 이미지 임베딩(CLIP/SigLIP), LTR, 개인화

---

## 🧱 아키텍처 개요
Naver Shopping API
        │
        ▼
[ETL] ingest → normalize → dedupe ─────┐
        │                               │
        └───▶ embeddings (SBERT)        │
                                        ▼
                              Elasticsearch (index)
                                        ▲
                                        │
                              FastAPI (backend)
                                        ▲
                                        │
                               Next.js (optional)

---

## 📁 폴더 구조
wearseek/
  backend/
    app/
      api/            # /search, /similar, /health
      core/           # config, es_client, embedder
      etl/            # naver_client, ingest, normalize, dedupe, indexer
      models/         # pydantic schemas
      main.py
    Dockerfile
    requirements.txt
  search/
    es/mappings/      # ES 인덱스 매핑 (products.json)
    notebooks/        # 오프라인 평가/실험 노트북
  web/
    next-app/         # (선택) Next.js 프런트
  infra/
    docker-compose.yml# ES + Kibana + backend
  docs/
    architecture.md
    api.md
    mapping.md
  .env.example
  README.md   

---

## ✅ 사전 준비
1. **Naver Developers**에서 앱 생성 → `Client ID/Secret` 발급  
2. Docker Desktop 설치(메모리 4~6GB 권장)  
3. 프로젝트 루트에 `.env` 생성 (아래 예시 참고)

### `.env` 예시
```
# NAVER OPEN API
NAVER_CLIENT_ID=__PUT_YOURS__
NAVER_CLIENT_SECRET=__PUT_YOURS__

# Elasticsearch
ES_HOST=http://elasticsearch:9200
ES_INDEX_PRODUCTS=products

# ML Models
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANK_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

PYTHONUNBUFFERED=1
```

---

## 🚀 빠른 시작 (Docker Compose)
# 1) 컨테이너 기동 (infra 폴더에서)
cd infra
docker compose up -d

# 2) 상태 확인
docker compose ps
docker compose logs -f elasticsearch
docker compose logs -f backend

Mac에서 바인드 마운트 경로는 기본적으로 ~/(사용자 홈) 하위만 허용됩니다.
홈 외 경로를 쓰면 Docker Desktop > Settings > Resources > File Sharing에 추가하세요.

## 📥 데이터 적재(ETL) → 인덱싱
# 컨테이너 진입
docker compose exec backend bash

# 1) 수집
python -m app.etl.ingest_shop --query "반팔 티셔츠" --limit 200 --out /data/raw/naver

# 2) 정규화
python -m app.etl.normalize --in_path /data/raw/naver --out_path /data/norm/naver

# 3) 중복 제거
python -m app.etl.dedupe --in_path /data/norm/naver --out_file /data/stage/products.jsonl

# 4) 인덱싱 (ES 매핑 적용 + 임베딩 벡터 생성)
python -m app.etl.indexer --src_file /data/stage/products.jsonl --mapping_path /search/es/mappings/products.json


## 🔎 API 사용법
- 헬스체크
GET http://localhost:8000/api/health
- 검색
GET http://localhost:8000/api/search?q=검정 오버핏 티셔츠&size=20
- 유사 아이템
GET http://localhost:8000/api/similar?id=<document_id>&size=12

## 🧪 오프라인 평가(ML 강조 포인트)
- search/notebooks/01_embedding_eval.ipynb: 한국어/다국어 임베딩 비교 (Recall@K, MRR@10)
- search/notebooks/02_rerank_offline.ipynb: BM25 vs Hybrid vs Hybrid+Cross-Encoder의 NDCG@10 비교
- search/notebooks/03_ltr_dataset.ipynb: 클릭 로그 스키마 → LTR 피처셋 구성 → LightGBM LTR 1차

## 🧾 라이선스
- 해당 저장소는 학습/개인 포트폴리오 목적을 우선합니다.
- 네이버 오픈API, 외부 모델/데이터 사용 시 각 서비스 약관을 반드시 준수하세요.
