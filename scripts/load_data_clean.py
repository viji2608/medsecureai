#!/usr/bin/env python3
"""
Load clean data without PHI redaction
"""

import sys
sys.path.append('src')

from data_prep_no_redaction import MedicalDataPrep  # Use the clean version
from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
import pandas as pd
import os
import pickle
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("=" * 60)
    print("📦 LOADING COMPLETE MEDICAL RECORDS (NO REDACTION)")
    print("=" * 60)
    
    # Load data
    print("\n[1/5] Loading synthetic records...")
    df = pd.read_csv('data/synthetic_records.csv')
    print(f"✅ Loaded {len(df)} records")
    
    # Show sample
    print("\n📄 Sample Record (first 500 chars):")
    print("-" * 60)
    print(df.iloc[0]['clinical_summary'][:500] + "...")
    print("-" * 60)
    
    # Prepare WITHOUT redaction
    print("\n[2/5] Preparing records (NO PHI removal)...")
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    print(f"✅ Prepared {len(records)} complete records")
    
    # Verify no truncation
    print(f"\n📊 Text length check:")
    print(f"  First record length: {len(records[0]['text'])} characters")
    print(f"  Average length: {sum(len(r['text']) for r in records) / len(records):.0f} characters")
    
    # Embed
    print("\n[3/5] Generating embeddings...")
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    print(f"✅ Generated {len(embedded_records)} embeddings")
    
    # Cache
    print("\n[4/5] Caching embeddings...")
    os.makedirs('data', exist_ok=True)
    cache_data = {
        'embedded_records': embedded_records,
        'dimension': embedder.dimension
    }
    with open('data/embeddings_cache.pkl', 'wb') as f:
        pickle.dump(cache_data, f)
    print("✅ Embeddings cached")
    
    # Load to CyborgDB
    print("\n[5/5] Loading to CyborgDB...")
    api_key = os.getenv('CYBORGDB_API_KEY')
    cyborg = CyborgDBRealClient(api_key=api_key)
    
    index_name = "medical_records"
    cyborg.create_index(index_name, embedder.dimension)
    
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        cyborg.add_items(index_name, batch)
        progress = min(i + batch_size, len(embedded_records))
        print(f"  Progress: {progress}/{len(embedded_records)} ({progress*100//len(embedded_records)}%)")
    
    # Test search
    print("\n🔍 Testing search...")
    query = "diabetes treatment"
    query_emb = embedder.embed_query(query)
    results = cyborg.search(index_name, query_emb.tolist(), top_k=1)
    
    if results['matches']:
        print(f"✅ Search working!")
        print(f"\n📄 Sample result (first 300 chars):")
        print("-" * 60)
        print(results['matches'][0]['text'][:300] + "...")
        print("-" * 60)
    
    print("\n" + "=" * 60)
    print("✅ DATA LOADED SUCCESSFULLY - COMPLETE RECORDS!")
    print("=" * 60)
    print("\nNow restart API:")
    print("  python src/api_fast.py")

if __name__ == "__main__":
    main()
