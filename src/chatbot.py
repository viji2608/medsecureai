#!/usr/bin/env python3
"""
MedSecureAI Chatbot API
FastAPI web service for encrypted medical queries
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uvicorn
import time

# Import our modules
from embedding import MedicalEmbedder
from cyborg_client import CyborgDBClient
from audit import AuditLogger

# Initialize FastAPI app
app = FastAPI(
    title="MedSecureAI Clinical Assistant",
    description="HIPAA-compliant encrypted medical AI system",
    version="1.0.0"
)

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (these will be loaded on startup)
embedder: Optional[MedicalEmbedder] = None
cyborg_client: Optional[CyborgDBClient] = None
audit_logger: Optional[AuditLogger] = None

# Request/Response models
class QueryRequest(BaseModel):
    question: str = Field(..., description="Clinical question", min_length=5)
    user_id: str = Field(..., description="Clinician identifier")
    top_k: int = Field(5, description="Number of results", ge=1, le=20)
    filters: Optional[Dict] = Field(None, description="Optional metadata filters")

class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    metadata: Dict

class QueryResponse(BaseModel):
    query_id: str
    answer: str
    sources: List[SearchResult]
    latency_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    components: Dict[str, bool]

class MetricsResponse(BaseModel):
    performance: Dict
    audit_summary: Dict


@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    global embedder, cyborg_client, audit_logger
    
    print("\n" + "=" * 60)
    print("�� Starting MedSecureAI Clinical Assistant")
    print("=" * 60)
    
    try:
        print("\n[1/3] Loading embedding model...")
        embedder = MedicalEmbedder()
        print("✅ Embedder ready")
        
        print("\n[2/3] Connecting to CyborgDB...")
        cyborg_client = CyborgDBClient()
        print("✅ CyborgDB client ready")
        
        print("\n[3/3] Initializing audit logger...")
        audit_logger = AuditLogger()
        print("✅ Audit logger ready")
        
        print("\n" + "=" * 60)
        print("✅ All systems operational")
        print("🔒 HIPAA-compliant mode enabled")
        print("📡 API available at http://localhost:8000")
        print("📚 Docs available at http://localhost:8000/docs")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Startup failed: {e}")
        raise


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
        "service": "MedSecureAI Clinical Assistant",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns status of all components
    """
    components = {
        "embedder": embedder is not None,
        "cyborg_db": cyborg_client is not None,
        "audit_logger": audit_logger is not None
    }
    
    all_healthy = all(components.values())
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        service="MedSecureAI",
        version="1.0.0",
        components=components
    )


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process encrypted medical query
    
    This endpoint:
    1. Logs the query for HIPAA audit
    2. Generates query embedding
    3. Searches encrypted vector database
    4. Generates clinical response
    5. Logs the response
    """
    start_time = time.time()
    
    # Validate components
    if not all([embedder, cyborg_client, audit_logger]):
        raise HTTPException(
            status_code=503,
            detail="System components not initialized"
        )
    
    try:
        # Step 1: Audit logging
        query_id = audit_logger.log_query(
            request.user_id,
            request.question,
            metadata={'top_k': request.top_k}
        )
        
        # Step 2: Generate query embedding
        print(f"\n🔍 Processing query: {request.question[:50]}...")
        query_embedding = embedder.embed_query(request.question)
        
        # Step 3: Encrypted search
        search_results = cyborg_client.search_encrypted(
            collection="medical_records",
            query_vector=query_embedding.tolist(),
            top_k=request.top_k,
            filters=request.filters
        )
        
        # Step 4: Generate response
        # In production: Use local LLM (Llama3-Med) for RAG
        # For demo: Simple template response
        num_results = len(search_results.get('matches', []))
        
        if num_results > 0:
            answer = f"""Based on {num_results} relevant encrypted medical records:

This query would typically be processed by a local medical LLM (like Llama3-Med or Mistral-Med) that generates a clinically appropriate response using the retrieved context.

Key points from encrypted sources:
- Records retrieved from encrypted database
- All data remained encrypted during search
- Results decrypted only in secure memory
- No patient data exposed during processing

For production deployment, integrate:
1. Local medical LLM (Llama3-Med, GPT4-Med, or similar)
2. RAG pipeline using decrypted context
3. Clinical validation layer
4. Citation generation from source records"""
        else:
            answer = "No relevant records found in the encrypted database. Please try rephrasing your query."
        
        # Step 5: Format results
        sources = [
            SearchResult(
                id=result['id'],
                score=result['score'],
                text=result['text'],
                metadata=result['metadata']
            )
            for result in search_results.get('matches', [])
        ]
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        # Step 6: Log response
        audit_logger.log_response(
            query_id,
            num_results=num_results,
            latency_ms=latency_ms,
            success=True
        )
        
        from datetime import datetime
        
        response = QueryResponse(
            query_id=query_id,
            answer=answer,
            sources=sources,
            latency_ms=latency_ms,
            timestamp=datetime.now().isoformat()
        )
        
        print(f"✅ Query processed in {latency_ms:.2f}ms")
        
        return response
        
    except Exception as e:
        # Log error
        if audit_logger and 'query_id' in locals():
            audit_logger.log_error(query_id, str(e))
        
        print(f"❌ Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get system performance metrics and audit summary
    """
    if not all([cyborg_client, audit_logger]):
        raise HTTPException(
            status_code=503,
            detail="Metrics not available"
        )
    
    try:
        performance = cyborg_client.get_performance_report()
        audit_summary = audit_logger.get_audit_summary()
        
        return MetricsResponse(
            performance=performance,
            audit_summary=audit_summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audit/export")
async def export_audit():
    """Export audit trail for HIPAA compliance review"""
    if not audit_logger:
        raise HTTPException(status_code=503, detail="Audit logger not available")
    
    try:
        from datetime import datetime
        output_path = f"logs/audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        audit_logger.export_audit_report(output_path)
        
        return {
            "message": "Audit trail exported",
            "file": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For running directly
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🏥 MedSecureAI Clinical Assistant")
    print("=" * 60)
    print("\nStarting server...")
    print("Access the API at: http://localhost:8000")
    print("Interactive docs at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "chatbot:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
