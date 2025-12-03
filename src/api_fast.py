#!/usr/bin/env python3
"""
Fast API - Returns COMPLETE medical records
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict
import uvicorn
import time
import os
import pickle
from dotenv import load_dotenv

load_dotenv()

from cyborg_real_client import CyborgDBRealClient
from audit import AuditLogger

app = FastAPI(title="MedSecureAI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cyborg_client = None
audit_logger = None
INDEX_NAME = "medical_records"
DIMENSION = 384

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    user_id: str
    top_k: int = Field(5, ge=1, le=20)

class SearchResult(BaseModel):
    id: str
    score: float
    text: str  # FULL text, no truncation
    metadata: Dict

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    sources: List[SearchResult]
    latency_ms: float
    timestamp: str

def load_from_cache():
    """Load pre-computed embeddings"""
    global cyborg_client, DIMENSION
    
    print("\n📦 Loading from cache...")
    
    if not os.path.exists('data/embeddings_cache.pkl'):
        print("❌ No cache found! Run: python scripts/load_data_clean.py")
        return False
    
    with open('data/embeddings_cache.pkl', 'rb') as f:
        cache_data = pickle.load(f)
    
    embedded_records = cache_data['embedded_records']
    DIMENSION = cache_data['dimension']
    print(f"✅ Loaded {len(embedded_records)} records")
    
    # Verify record length
    sample_length = len(embedded_records[0]['text'])
    print(f"📊 Sample record length: {sample_length} characters")
    
    api_key = os.getenv('CYBORGDB_API_KEY')
    cyborg_client = CyborgDBRealClient(api_key=api_key)
    
    cyborg_client.create_index(INDEX_NAME, DIMENSION)
    
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        cyborg_client.add_items(INDEX_NAME, batch)
    
    print(f"✅ Loaded {len(embedded_records)} COMPLETE records to CyborgDB")
    return True

@app.on_event("startup")
async def startup():
    global audit_logger
    
    print("\n" + "=" * 60)
    print("🚀 MedSecureAI API - COMPLETE RECORDS MODE")
    print("=" * 60)
    
    if not load_from_cache():
        raise Exception("Data not loaded")
    
    audit_logger = AuditLogger()
    
    print("\n" + "=" * 60)
    print("✅ API READY - FULL RECORDS LOADED")
    print("=" * 60 + "\n")

@app.get("/")
def root():
    records = cyborg_client.indexes.get(INDEX_NAME, {}).get('count', 0) if cyborg_client else 0
    return {
        "service": "MedSecureAI",
        "version": "2.0.0",
        "records": records,
        "status": "operational"
    }

@app.get("/health")
def health():
    records = cyborg_client.indexes.get(INDEX_NAME, {}).get('count', 0) if cyborg_client else 0
    return {"status": "healthy", "records": records}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start_time = time.time()
    query_id = audit_logger.log_query(request.user_id, request.question)
    
    try:
        from embedding import MedicalEmbedder
        embedder = MedicalEmbedder()
        query_embedding = embedder.embed_query(request.question)
        
        results = cyborg_client.search(INDEX_NAME, query_embedding.tolist(), request.top_k)
        num_results = len(results.get('matches', []))
        
        if num_results > 0:
            top_score = results['matches'][0]['score']
            answer = f"""🔐 **COMPLETE ENCRYPTED MEDICAL RECORDS**

✅ Retrieved {num_results} FULL records from encrypted database
🎯 Top match similarity: {(1-top_score)*100:.1f}%
📄 Complete clinical notes with all details
🔒 All data searched while fully encrypted

This demonstrates PRODUCTION-READY encrypted medical AI with COMPLETE records."""
        else:
            answer = "No matches found."
        
        # Return FULL text - no truncation
        sources = []
        for m in results.get('matches', []):
            sources.append(SearchResult(
                id=m['id'],
                score=m['score'],
                text=m['text'],  # COMPLETE TEXT
                metadata=m.get('metadata', {})
            ))
        
        latency_ms = (time.time() - start_time) * 1000
        audit_logger.log_response(query_id, num_results, latency_ms)
        
        from datetime import datetime
        return QueryResponse(
            query_id=query_id,
            answer=answer,
            sources=sources,
            latency_ms=latency_ms,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        audit_logger.log_error(query_id, str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
