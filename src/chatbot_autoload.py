#!/usr/bin/env python3
"""
MedSecureAI API with auto-loading data
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uvicorn
import time
import os
import re
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
from audit import AuditLogger
from data_prep import MedicalDataPrep

app = FastAPI(title="MedSecureAI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedder = None
cyborg_client = None
audit_logger = None
INDEX_NAME = "medical_records"

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5)
    user_id: str
    top_k: int = Field(5, ge=1, le=20)

class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    metadata: Dict
    summary: str

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    sources: List[SearchResult]
    latency_ms: float
    timestamp: str
    encryption_status: str = "REAL CyborgDB 256-bit AES"

def clean_text(text: str) -> str:
    text = re.sub(r'\[NAME_REDACTED\]\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_summary(text: str) -> str:
    lines = text.split('\n')
    key_info = []
    for line in lines:
        clean_line = clean_text(line)
        if clean_line and len(clean_line) > 10:
            if any(word in clean_line.lower() for word in 
                   ['diabetes', 'hypertension', 'disease', 'medication', 
                    'treatment', 'diagnosis', 'patient', 'condition']):
                key_info.append(clean_line)
                if len(key_info) >= 3:
                    break
    
    if key_info:
        return ' • '.join(key_info[:3])
    else:
        clean = clean_text(text)
        return clean[:200] + '...' if len(clean) > 200 else clean

def load_data():
    """Load data into CyborgDB"""
    global cyborg_client, embedder
    
    print("\n📦 Loading medical data...")
    
    # Check if already loaded
    if INDEX_NAME in cyborg_client.indexes and cyborg_client.indexes[INDEX_NAME]['count'] > 0:
        print(f"✅ Data already loaded: {cyborg_client.indexes[INDEX_NAME]['count']} records")
        return
    
    # Load data
    df = pd.read_csv('data/synthetic_records.csv')
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    
    # Generate embeddings
    print("🧠 Generating embeddings...")
    embedded_records = embedder.embed_records(records)
    
    # Create index
    print(f"🔐 Creating encrypted index...")
    cyborg_client.create_index(INDEX_NAME, embedder.dimension)
    
    # Insert
    print("💾 Inserting encrypted records...")
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        cyborg_client.add_items(INDEX_NAME, batch)
    
    print(f"✅ Loaded {len(embedded_records)} encrypted records")

@app.on_event("startup")
async def startup():
    global embedder, cyborg_client, audit_logger
    
    print("\n" + "=" * 60)
    print("🚀 MedSecureAI - AUTO-LOADING DATA")
    print("=" * 60)
    
    api_key = os.getenv('CYBORGDB_API_KEY')
    if not api_key:
        raise ValueError("CYBORGDB_API_KEY not set")
    
    print(f"\n[1/4] 🔑 API Key: {api_key[:20]}...")
    
    print("\n[2/4] Loading embedding model...")
    embedder = MedicalEmbedder()
    
    print("\n[3/4] Connecting to CyborgDB...")
    cyborg_client = CyborgDBRealClient(api_key=api_key)
    
    print("\n[4/4] Loading medical data...")
    load_data()
    
    audit_logger = AuditLogger()
    
    print("\n" + "=" * 60)
    print("✅ READY WITH DATA LOADED")
    print(f"📊 {cyborg_client.indexes[INDEX_NAME]['count']} encrypted records ready")
    print("=" * 60 + "\n")

@app.get("/")
async def root():
    return {
        "service": "MedSecureAI",
        "version": "2.0.0",
        "encryption": "🔐 REAL 256-bit AES",
        "records_loaded": cyborg_client.indexes.get(INDEX_NAME, {}).get('count', 0) if cyborg_client else 0
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "cyborgdb": "connected",
        "records": cyborg_client.indexes.get(INDEX_NAME, {}).get('count', 0) if cyborg_client else 0
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start_time = time.time()
    query_id = audit_logger.log_query(request.user_id, request.question)
    
    try:
        query_embedding = embedder.embed_query(request.question)
        results = cyborg_client.search(INDEX_NAME, query_embedding.tolist(), request.top_k)
        
        num_results = len(results.get('matches', []))
        
        if num_results > 0:
            top_score = results['matches'][0]['score']
            answer = f"""🔐 **REAL ENCRYPTED SEARCH RESULTS**

✅ Retrieved **{num_results} matching records** from 256-bit AES encrypted database

**Query Analysis:**
- Search performed on FULLY ENCRYPTED vectors
- Top match similarity: {(1-top_score)*100:.1f}%
- Zero plaintext exposure during search

This demonstrates PRODUCTION-READY encrypted medical AI."""
        else:
            answer = "⚠️ No matching records found. Database may need more data."
        
        sources = []
        for m in results.get('matches', []):
            clean_text_content = clean_text(m['text'])
            summary = extract_summary(clean_text_content)
            
            sources.append(SearchResult(
                id=m['id'],
                score=m['score'],
                text=clean_text_content[:500],
                summary=summary,
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

@app.get("/metrics")
async def metrics():
    return {
        "performance": cyborg_client.get_performance_report(),
        "audit": audit_logger.get_audit_summary()
    }

if __name__ == "__main__":
    uvicorn.run("chatbot_autoload:app", host="0.0.0.0", port=8000, reload=False)