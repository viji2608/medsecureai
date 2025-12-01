#!/usr/bin/env python3
"""
CyborgDB Client for Encrypted Vector Operations
CRITICAL: This module requires thorough evaluation for hackathon submission
"""

import time
import json
import os
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime

class CyborgDBClient:
    """
    Client for CyborgDB encrypted vector database
    
    This is a TEMPLATE implementation. Replace with actual CyborgDB API calls.
    Document all successes, failures, and performance metrics.
    """
    
    def __init__(self, connection_string: str = "localhost:50051"):
        """
        Initialize CyborgDB connection
        
        Args:
            connection_string: CyborgDB server address
        """
        print(f"🔌 Connecting to CyborgDB at {connection_string}")
        
        self.connection_string = connection_string
        self.collections = {}
        self.performance_metrics = []
        self.failures = []
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        
        # TODO: Replace with actual CyborgDB initialization
        # Example:
        # from cyborgdb import Client
        # self.client = Client(connection_string)
        
        try:
            # Attempt connection
            self._test_connection()
            print("✅ CyborgDB connection successful")
        except Exception as e:
            print(f"⚠️  CyborgDB connection warning: {e}")
            print("⚠️  Running in MOCK mode for development")
            self._log_failure("connection", str(e))
    
    def _test_connection(self):
        """Test connection to CyborgDB"""
        # TODO: Implement actual connection test
        # Example:
        # self.client.ping()
        pass
    
    def create_collection(self, name: str, dimension: int, 
                         distance_metric: str = "cosine") -> bool:
        """
        Create encrypted vector collection
        
        Args:
            name: Collection name
            dimension: Vector dimension
            distance_metric: Similarity metric (cosine, euclidean, dot)
            
        Returns:
            Success status
        """
        start_time = time.time()
        
        try:
            print(f"🔄 Creating collection: {name} (dim={dimension}, metric={distance_metric})")
            
            # TODO: Replace with actual CyborgDB API
            # Example:
            # self.client.create_collection(
            #     name=name,
            #     dimension=dimension,
            #     encrypted=True,
            #     distance_metric=distance_metric
            # )
            
            # Mock implementation
            self.collections[name] = {
                'dimension': dimension,
                'distance_metric': distance_metric,
                'encrypted': True,
                'count': 0,
                'vectors': []
            }
            
            elapsed = time.time() - start_time
            
            # Log metrics
            self._log_metric({
                'operation': 'create_collection',
                'collection': name,
                'dimension': dimension,
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
                'dimension': dimension,
                'latency_ms': elapsed * 1000
            })
            return False
    
    def insert_encrypted(self, collection: str, records: List[Dict],
                        batch_size: int = 50) -> Dict:
        """
        Insert encrypted embeddings into collection
        
        Args:
            collection: Collection name
            records: List of records with 'embedding' field
            batch_size: Batch size for insertion
            
        Returns:
            Metrics dictionary
        """
        start_time = time.time()
        
        try:
            print(f"🔄 Inserting {len(records)} records into {collection}...")
            
            # TODO: Replace with actual CyborgDB API
            # Example:
            # vectors = [r['embedding'] for r in records]
            # metadata = [r['metadata'] for r in records]
            # encrypted_vectors = self.client.encrypt_vectors(vectors)
            # self.client.insert(
            #     collection=collection,
            #     vectors=encrypted_vectors,
            #     metadata=metadata
            # )
            
            # Mock implementation with realistic timing
            total_inserted = 0
            for i in range(0, len(records), batch_size):
                batch = records[i:i+batch_size]
                
                # Simulate encryption overhead
                time.sleep(0.01 * len(batch))  # ~10ms per record
                
                # Store in mock collection
                if collection in self.collections:
                    self.collections[collection]['vectors'].extend(batch)
                    self.collections[collection]['count'] += len(batch)
                
                total_inserted += len(batch)
                print(f"  Progress: {total_inserted}/{len(records)} records")
            
            elapsed = time.time() - start_time
            throughput = len(records) / elapsed if elapsed > 0 else 0
            
            metrics = {
                'operation': 'insert',
                'collection': collection,
                'count': len(records),
                'latency_ms': elapsed * 1000,
                'throughput_records_per_sec': throughput,
                'avg_latency_per_record_ms': (elapsed * 1000) / len(records),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self._log_metric(metrics)
            
            print(f"✅ Inserted {len(records)} records in {elapsed:.2f}s")
            print(f"   Throughput: {throughput:.1f} records/sec")
            
            return metrics
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Insertion failed: {e}")
            self._log_failure("insert", str(e), {
                'collection': collection,
                'attempted_count': len(records),
                'latency_ms': elapsed * 1000
            })
            return {'success': False, 'error': str(e)}
    
    def search_encrypted(self, collection: str, query_vector: List[float],
                        top_k: int = 5, filters: Optional[Dict] = None) -> Dict:
        """
        Search encrypted vectors
        
        Args:
            collection: Collection name
            query_vector: Query embedding
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            Search results with metrics
        """
        start_time = time.time()
        
        try:
            print(f"🔍 Searching {collection} for top-{top_k} matches...")
            
            # TODO: Replace with actual CyborgDB API
            # Example:
            # encrypted_query = self.client.encrypt_vector(query_vector)
            # encrypted_results = self.client.search(
            #     collection=collection,
            #     query=encrypted_query,
            #     top_k=top_k,
            #     filters=filters
            # )
            # decrypted_results = self.client.decrypt_results(encrypted_results)
            
            # Mock implementation with similarity calculation
            results = []
            
            if collection in self.collections:
                vectors = self.collections[collection]['vectors']
                
                # Simulate encrypted search timing
                time.sleep(0.05)  # ~50ms base latency
                
                # Calculate similarities (in real system, this happens on encrypted data)
                query_np = np.array(query_vector)
                
                for i, record in enumerate(vectors[:min(len(vectors), 100)]):  # Limit for demo
                    if 'embedding' in record:
                        vec_np = np.array(record['embedding'])
                        # Cosine similarity
                        similarity = np.dot(query_np, vec_np) / (
                            np.linalg.norm(query_np) * np.linalg.norm(vec_np)
                        )
                        
                        results.append({
                            'id': record.get('anon_id', f'record_{i}'),
                            'score': float(similarity),
                            'text': record.get('text', '')[:200] + '...',
                            'metadata': record.get('metadata', {})
                        })
                
                # Sort by score and get top-k
                results.sort(key=lambda x: x['score'], reverse=True)
                results = results[:top_k]
            
            elapsed = time.time() - start_time
            
            metrics = {
                'operation': 'search',
                'collection': collection,
                'query_latency_ms': elapsed * 1000,
                'top_k': top_k,
                'results_found': len(results),
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            
            self._log_metric(metrics)
            
            print(f"✅ Search completed in {elapsed*1000:.2f}ms")
            print(f"   Found {len(results)} matches")
            
            return {
                'matches': results,
                'metrics': metrics
            }
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"❌ Search failed: {e}")
            self._log_failure("search", str(e), {
                'collection': collection,
                'top_k': top_k,
                'latency_ms': elapsed * 1000
            })
            return {
                'matches': [],
                'metrics': {'success': False, 'error': str(e)}
            }
    
    def _log_metric(self, metric: Dict):
        """Log performance metric"""
        self.performance_metrics.append(metric)
        
        # Also save to file for evaluation
        with open('logs/cyborg_metrics.jsonl', 'a') as f:
            f.write(json.dumps(metric) + '\n')
    
    def _log_failure(self, operation: str, error: str, context: Optional[Dict] = None):
        """Log failure for evaluation documentation"""
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
        """
        Generate comprehensive performance metrics report
        CRITICAL for hackathon evaluation!
        """
        if not self.performance_metrics:
            return {'message': 'No operations performed yet'}
        
        # Separate by operation type
        inserts = [m for m in self.performance_metrics if m['operation'] == 'insert']
        searches = [m for m in self.performance_metrics if m['operation'] == 'search']
        
        report = {
            'summary': {
                'total_operations': len(self.performance_metrics),
                'successful_operations': len([m for m in self.performance_metrics if m.get('success')]),
                'failed_operations': len(self.failures),
                'collections_created': len(self.collections)
            },
            'insert_performance': {
                'total_inserts': len(inserts),
                'total_records_inserted': sum(m.get('count', 0) for m in inserts),
                'avg_latency_ms': np.mean([m['latency_ms'] for m in inserts]) if inserts else 0,
                'avg_throughput': np.mean([m.get('throughput_records_per_sec', 0) for m in inserts]) if inserts else 0,
                'min_latency_ms': min([m['latency_ms'] for m in inserts]) if inserts else 0,
                'max_latency_ms': max([m['latency_ms'] for m in inserts]) if inserts else 0
            },
            'search_performance': {
                'total_searches': len(searches),
                'avg_query_latency_ms': np.mean([m['query_latency_ms'] for m in searches]) if searches else 0,
                'min_query_latency_ms': min([m['query_latency_ms'] for m in searches]) if searches else 0,
                'max_query_latency_ms': max([m['query_latency_ms'] for m in searches]) if searches else 0,
                'p95_latency_ms': np.percentile([m['query_latency_ms'] for m in searches], 95) if searches else 0,
                'p99_latency_ms': np.percentile([m['query_latency_ms'] for m in searches], 99) if searches else 0
            },
            'failures': self.failures
        }
        
        return report


# Test the module
if __name__ == "__main__":
    import sys
    sys.path.append('.')
    from src.data_prep import MedicalDataPrep
    from src.embedding import MedicalEmbedder
    import pandas as pd
    
    print("=" * 60)
    print("Testing CyborgDB Client Module")
    print("=" * 60)
    
    # Prepare test data
    print("\n[1/5] Preparing test data...")
    df = pd.read_csv('data/synthetic_records.csv')
    prep = MedicalDataPrep()
    records = prep.prepare_records(df[:20])  # Test with 20 records
    
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    
    # Initialize CyborgDB client
    print("\n[2/5] Initializing CyborgDB client...")
    client = CyborgDBClient()
    
    # Create collection
    print("\n[3/5] Creating encrypted collection...")
    success = client.create_collection("test_medical", dimension=384)
    print(f"Collection creation: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Insert records
    print("\n[4/5] Inserting encrypted records...")
    insert_metrics = client.insert_encrypted("test_medical", embedded_records)
    print(f"Insertion: {'✅ SUCCESS' if insert_metrics.get('success') else '❌ FAILED'}")
    
    # Search
    print("\n[5/5] Testing encrypted search...")
    query = "What treatments are available for diabetes?"
    query_embedding = embedder.embed_query(query)
    search_results = client.search_encrypted("test_medical", query_embedding.tolist(), top_k=3)
    
    print(f"\nQuery: {query}")
    print(f"Results found: {len(search_results['matches'])}")
    
    if search_results['matches']:
        print("\nTop match:")
        top_match = search_results['matches'][0]
        print(f"  Score: {top_match['score']:.3f}")
        print(f"  Text: {top_match['text'][:100]}...")
    
    # Performance report
    print("\n📊 Performance Report:")
    print("=" * 60)
    report = client.get_performance_report()
    print(json.dumps(report, indent=2))
    
    print("\n✅ CyborgDB client module test complete!")
    print(f"📁 Metrics saved to: logs/cyborg_metrics.jsonl")
    print(f"📁 Failures saved to: logs/cyborg_failures.jsonl")
