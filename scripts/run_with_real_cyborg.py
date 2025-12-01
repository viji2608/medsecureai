#!/usr/bin/env python3
"""
MedSecureAI with REAL CyborgDB Integration
Complete pipeline for hackathon demo
"""

import sys
sys.path.append('src')

from data_prep import MedicalDataPrep
from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
from audit import AuditLogger
import pandas as pd
import json
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("=" * 60)
    print("🏥 MedSecureAI - REAL Encrypted Vector Search")
    print("=" * 60)
    
    # Get API key
    api_key = os.getenv('CYBORGDB_API_KEY')
    if not api_key:
        print("❌ CYBORGDB_API_KEY not found in .env")
        return
    
    # Step 1: Data Preparation
    print("\n[1/6] 📋 Data Preparation")
    print("-" * 60)
    prep = MedicalDataPrep()
    df = pd.read_csv('data/synthetic_records.csv')
    records = prep.prepare_records(df)
    print(f"✅ Anonymized {len(records)} records")
    
    # Step 2: Generate Embeddings
    print("\n[2/6] 🧠 Generating Embeddings")
    print("-" * 60)
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    print(f"✅ Generated {len(embedded_records)} embeddings")
    
    # Step 3: Initialize REAL CyborgDB
    print("\n[3/6] 🔐 Connecting to REAL CyborgDB")
    print("-" * 60)
    cyborg = CyborgDBRealClient(api_key=api_key)
    
    # Step 4: Create Encrypted Index
    print("\n[4/6] 🔒 Creating Encrypted Index")
    print("-" * 60)
    index_name = "medical_records"
    cyborg.create_index(index_name, embedder.dimension)
    
    # Step 5: Insert Encrypted Data
    print("\n[5/6] 💾 Inserting ENCRYPTED Medical Records")
    print("-" * 60)
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        metrics = cyborg.add_items(index_name, batch)
        print(f"  Batch {i//batch_size + 1}: {len(batch)} records encrypted")
    
    # Step 6: Test Queries
    print("\n[6/6] 🔍 Testing Encrypted Search")
    print("-" * 60)
    
    audit = AuditLogger()
    
    test_queries = [
        "What are effective treatments for Type 2 Diabetes?",
        "How to manage hypertension in elderly patients?",
        "What medications interact with Metformin?"
    ]
    
    for query_text in test_queries:
        print(f"\n🔍 Query: {query_text}")
        
        # Generate query embedding
        query_embedding = embedder.embed_query(query_text)
        
        # Log query
        query_id = audit.log_query("DEMO_USER", query_text)
        
        # ENCRYPTED SEARCH
        results = cyborg.search(index_name, query_embedding.tolist(), top_k=3)
        
        print(f"   ✅ Found {len(results.get('matches', []))} encrypted matches")
        print(f"   ⏱️  Latency: {results['metrics']['query_latency_ms']:.2f}ms")
        
        # Show top match
        if results['matches']:
            top = results['matches'][0]
            print(f"   🥇 Top Match: {top['id']} (score: {top['score']:.4f})")
        
        audit.log_response(query_id, len(results.get('matches', [])), 
                          results['metrics']['query_latency_ms'])
    
    # Performance Report
    print("\n" + "=" * 60)
    print("📊 REAL CyborgDB Performance Report")
    print("=" * 60)
    
    report = cyborg.get_performance_report()
    print(json.dumps(report, indent=2))
    
    # Save report
    os.makedirs('docs', exist_ok=True)
    with open('docs/real_cyborg_performance.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ REAL CyborgDB Integration Complete!")
    print("🔐 All 200 medical records are END-TO-END ENCRYPTED")
    print("=" * 60)
    print("\n📁 Reports saved:")
    print("   - docs/real_cyborg_performance.json")
    print("   - logs/cyborg_real_metrics.jsonl")
    print("   - logs/audit_trail.jsonl")

if __name__ == "__main__":
    main()
