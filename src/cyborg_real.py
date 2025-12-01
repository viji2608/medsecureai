#!/usr/bin/env python3
"""
Real CyborgDB Integration
Replace mock implementation with actual CyborgDB API calls
"""

import time
import json
import os
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

# Import actual CyborgDB client
try:
    from cyborgdb import Client, Collection
    CYBORGDB_AVAILABLE = True
except ImportError:
    print("⚠️  CyborgDB client not installed. Install with: pip install cyborgdb")
    CYBORGDB_AVAILABLE = False

class CyborgDBRealClient:
    """
    Real CyborgDB client implementation
    """
    
    def __init__(self, host: str = "localhost", port: int = 50051, api_key: Optional[str] = None):
        """
        Initialize real CyborgDB connection
        
        Args:
            host: CyborgDB server host
            port: CyborgDB server port
            api_key: API key for authentication (if required)
        """
        self.host = host
        self.port = port
        self.api_key = api_key or os.getenv('CYBORGDB_API_KEY')
        self.performance_metrics = []
        self.failures = []
        
        os.makedirs('logs', exist_ok=True)
        
        if not CYBORGDB_AVAILABLE:
            raise ImportError("CyborgDB client not available")
        
        try:
            print(f"🔌 Connecting to CyborgDB at {host}:{port}")
            
            # Initialize real CyborgDB client
            self.client = Client(
                host=host,
                port=port,
                api_key=self.api_key
            )
            
            # Test connection
            self.client.health_check()
            print("✅ Connected to CyborgDB successfully")
            
        except Exception as e:
            print(f"❌ CyborgDB connection failed: {e}")
            self._log_failure("connection", str(e))
            raise
    
    def create_collection(self, name: str, dimension: int, 
                         distance_metric: str = "cosine",
                         encryption_enabled: bool = True) -> bool:
        """
        Create encrypted vector collection in CyborgDB
        
        Args:
            name: Collection name
            dimension: Vector dimension
            distance_metric: Similarity metric
            encryption_enabled: Enable encryption
            
        Returns:
            Success status
        """
        start_time = time.time()
        
        try:
            print(f"🔄 Creating encrypted collection: {name}")
            
            # Create collection with encryption
            collection = self.client.create_collection(
                name=name,
                dimension=dimension,
                distance_metric=distance_metric,
                encryption=encryption_enabled
            )
            
            elapsed = time.time() - start_time
            
            self._log_metric({
                'operation': 'create_collection',
                'collection': name,
                'dimension': dimension,
                'encrypted': encryption_enabled,
                'latency_ms': elapsed * 1000,
                'success': True,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ Collection created in {elapsed*1000:.2f}ms")
            return True
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Collection creation failed: {e}")
            self._log_failure("create_collection", str(e), {
                'collection': name,
                'latency_ms': elapsed * 1000
            })
            return False
    
    def insert_encrypted(self, collection: str, records: List[Dict]) -> Dict:
        """
        Insert encrypted vectors into CyborgDB
        
        Args:
            collection: Collection name
            records: List of records with embeddings
            
        Returns:
            Performance metrics
        """
        start_time = time.time()
        
        try:
            print(f"🔄 Inserting {len(records)} encrypted records...")
            
            # Extract vectors and metadata
            vectors = [r['embedding'] for r in records]
            metadata = [r.get('metadata', {}) for r in records]
            ids = [r.get('anon_id', f'record_{i}') for i, r in enumerate(records)]
            
            # Insert with encryption
            col = self.client.get_collection(collection)
            result = col.insert(
                vectors=vectors,
                metadata=metadata,
                ids=ids,
                encrypt=True  # Ensure encryption
            )
            
            elapsed = time.time() - start_time
            throughput = len(records) / elapsed if elapsed > 0 else 0
            
            metrics = {
                'operation': 'insert',
                'collection': collection,
                'count': len(records),
                'latency_ms': elapsed * 1000,
                'throughput_records_per_sec': throughput,
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self._log_metric(metrics)
            print(f"✅ Inserted {len(records)} records in {elapsed:.2f}s ({throughput:.1f} rec/s)")
            
            return metrics
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Insertion failed: {e}")
            self._log_failure("insert", str(e), {
                'collection': collection,
                'attempted_count': len(records)
            })
            return {'success': False, 'error': str(e)}
    
    def search_encrypted(self, collection: str, query_vector: List[float],
                        top_k: int = 5) -> Dict:
        """
        Search encrypted vectors in CyborgDB
        
        Args:
            collection: Collection name
            query_vector: Query embedding
            top_k: Number of results
            
        Returns:
            Search results with metrics
        """
        start_time = time.time()
        
        try:
            print(f"🔍 Searching encrypted database for top-{top_k}...")
            
            # Get collection
            col = self.client.get_collection(collection)
            
            # Perform encrypted search
            results = col.search(
                query=query_vector,
                k=top_k,
                encrypt_query=True  # Encrypt the query vector
            )
            
            elapsed = time.time() - start_time
            
            # Format results
            matches = []
            for result in results:
                matches.append({
                    'id': result.id,
                    'score': float(result.score),
                    'text': result.metadata.get('text', '')[:200] + '...',
                    'metadata': result.metadata
                })
            
            metrics = {
                'operation': 'search',
                'collection': collection,
                'query_latency_ms': elapsed * 1000,
                'top_k': top_k,
                'results_found': len(matches),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self._log_metric(metrics)
            print(f"✅ Search completed in {elapsed*1000:.2f}ms, found {len(matches)} matches")
            
            return {
                'matches': matches,
                'metrics': metrics
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Search failed: {e}")
            self._log_failure("search", str(e), {
                'collection': collection,
                'top_k': top_k
            })
            return {
                'matches': [],
                'metrics': {'success': False, 'error': str(e)}
            }
    
    def _log_metric(self, metric: Dict):
        """Log performance metric"""
        self.performance_metrics.append(metric)
        with open('logs/cyborg_metrics.jsonl', 'a') as f:
            f.write(json.dumps(metric) + '\n')
    
    def _log_failure(self, operation: str, error: str, context: Optional[Dict] = None):
        """Log failure"""
        failure = {
            'operation': operation,
            'error': error,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }
        self.failures.append(failure)
        with open('logs/cyborg_failures.jsonl', 'a') as f:
            f.write(json.dumps(failure) + '\n')
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        if not self.performance_metrics:
            return {'message': 'No operations performed yet'}
        
        inserts = [m for m in self.performance_metrics if m['operation'] == 'insert']
        searches = [m for m in self.performance_metrics if m['operation'] == 'search']
        
        return {
            'summary': {
                'total_operations': len(self.performance_metrics),
                'successful_operations': len([m for m in self.performance_metrics if m.get('success')]),
                'failed_operations': len(self.failures)
            },
            'insert_performance': {
                'total_inserts': len(inserts),
                'total_records_inserted': sum(m.get('count', 0) for m in inserts),
                'avg_latency_ms': np.mean([m['latency_ms'] for m in inserts]) if inserts else 0,
                'avg_throughput': np.mean([m.get('throughput_records_per_sec', 0) for m in inserts]) if inserts else 0
            },
            'search_performance': {
                'total_searches': len(searches),
                'avg_query_latency_ms': np.mean([m['query_latency_ms'] for m in searches]) if searches else 0,
                'p95_latency_ms': np.percentile([m['query_latency_ms'] for m in searches], 95) if searches else 0
            },
            'failures': self.failures
        }


# Instructions for setup
if __name__ == "__main__":
    print("""
    ============================================================
    CyborgDB Real Integration Setup
    ============================================================
    
    To use real CyborgDB:
    
    1. Install CyborgDB:
       pip install cyborgdb
    
    2. Start CyborgDB server (follow their docs):
       # Option A: Docker
       docker run -p 50051:50051 cyborgdb/server
       
       # Option B: Local installation
       cyborgdb start --port 50051
    
    3. Set API key (if required):
       export CYBORGDB_API_KEY="your-api-key"
    
    4. Update chatbot.py to use CyborgDBRealClient instead of CyborgDBClient
    
    5. Test connection:
       python src/cyborg_real.py
    
    For hackathon demo without real CyborgDB:
    - Use the mock implementation (current chatbot.py)
    - Document this as "Phase 1 - Proof of Concept"
    - Mention "Production deployment requires CyborgDB server"
    
    ============================================================
    """)
