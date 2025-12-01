#!/usr/bin/env python3
"""
Complete MedSecureAI pipeline demonstration
Runs the entire workflow for hackathon demo
"""

import sys
import os
sys.path.append('src')

from data_prep import MedicalDataPrep
from embedding import MedicalEmbedder
from cyborg_client import CyborgDBClient
from audit import AuditLogger
import pandas as pd
import json
import time

def main():
    print("=" * 60)
    print("🏥 MedSecureAI - Full Pipeline Demonstration")
    print("=" * 60)
    
    # Step 1: Data Preparation
    print("\n[1/6] 📋 Data Preparation & PHI Removal")
    print("-" * 60)
    prep = MedicalDataPrep()
    
    df = pd.read_csv('data/synthetic_records.csv')
    print(f"✓ Loaded {len(df)} medical records")
    
    records = prep.prepare_records(df)
    print(f"✓ Anonymized {len(records)} records (PHI removed)")
    
    # Step 2: Embedding Generation
    print("\n[2/6] 🧠 Medical Text Embedding Generation")
    print("-" * 60)
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    print(f"✓ Generated {len(embedded_records)} embeddings (dim={embedder.dimension})")
    
    # Step 3: CyborgDB Setup & Storage
    print("\n[3/6] 🔐 CyborgDB Encrypted Storage")
    print("-" * 60)
    cyborg = CyborgDBClient()
    
    collection_name = "medical_records"
    success = cyborg.create_collection(collection_name, embedder.dimension)
    
    if success:
        print(f"✓ Created collection: {collection_name}")
        
        # Insert in batches
        batch_size = 50
        for i in range(0, len(embedded_records), batch_size):
            batch = embedded_records[i:i+batch_size]
            metrics = cyborg.insert_encrypted(collection_name, batch)
            print(f"  Batch {i//batch_size + 1}: {len(batch)} records, "
                  f"{metrics.get('latency_ms', 0):.2f}ms")
    
    # Step 4: Query Testing
    print("\n[4/6] 🔍 Testing Encrypted Query Retrieval")
    print("-" * 60)
    
    test_queries = [
        "What are effective treatments for Type 2 Diabetes?",
        "How to manage hypertension in elderly patients?",
        "What medications interact with Metformin?"
    ]
    
    audit = AuditLogger()
    
    for query_text in test_queries:
        print(f"\nQuery: {query_text}")
        
        # Generate query embedding
        query_embedding = embedder.generate_embeddings([query_text])[0]
        
        # Log query
        query_id = audit.log_query("DEMO_USER", query_text)
        
        # Encrypted search
        results = cyborg.search_encrypted(
            collection_name,
            query_embedding.tolist(),
            top_k=3
        )
        
        print(f"  → Retrieved {len(results.get('matches', []))} matches")
        print(f"  → Query latency: {results['metrics']['query_latency_ms']:.2f}ms")
        
        audit.log_response(query_id, len(results.get('matches', [])), 
                          results['metrics']['query_latency_ms'])
    
    # Step 5: Performance Metrics
    print("\n[5/6] 📊 Performance Metrics Summary")
    print("-" * 60)
    
    perf_report = cyborg.get_performance_report()
    print(json.dumps(perf_report, indent=2))
    
    # Save metrics
    os.makedirs('docs', exist_ok=True)
    with open('docs/performance_report.json', 'w') as f:
        json.dump(perf_report, f, indent=2)
    
    # Step 6: Audit Trail
    print("\n[6/6] 📝 HIPAA Audit Trail Summary")
    print("-" * 60)
    
    audit_summary = audit.get_audit_summary()
    print(json.dumps(audit_summary, indent=2))
    
    print("\n" + "=" * 60)
    print("✅ Pipeline Completed Successfully!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Review performance metrics in docs/performance_report.json")
    print("2. Check audit logs in logs/audit_trail.jsonl")
    print("3. Start the web interface: python src/chatbot.py")
    print("4. Open web/index.html in your browser")

if __name__ == "__main__":
    main()
