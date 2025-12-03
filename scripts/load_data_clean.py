#!/usr/bin/env python3
import sys
sys.path.append('src')

import pandas as pd
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

from data_prep_clean import MedicalDataPrep  # Use CLEAN version
from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient

def main():
    print("=" * 60)
    print("📦 LOADING COMPLETE RECORDS (NO REDACTION)")
    print("=" * 60)
    
    print("\n[1/5] Loading synthetic records...")
    df = pd.read_csv('data/synthetic_records.csv')
    print(f"✅ Loaded {len(df)} records")
    
    print("\n[2/5] Preparing records (NO PHI removal)...")
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    print(f"✅ Prepared {len(records)} complete records")
    
    # Verify
    print(f"\n📄 Sample record preview (first 200 chars):")
    print("-" * 60)
    print(records[0]['text'][:200] + "...")
    print("-" * 60)
    
    print("\n[3/5] Generating embeddings...")
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    print(f"✅ Generated {len(embedded_records)} embeddings")
    
    print("\n[4/5] Caching embeddings...")
    os.makedirs('data', exist_ok=True)
    with open('data/embeddings_cache.pkl', 'wb') as f:
        pickle.dump({
            'embedded_records': embedded_records,
            'dimension': embedder.dimension
        }, f)
    print("✅ Embeddings cached")
    
    print("\n[5/5] Loading to CyborgDB...")
    api_key = os.getenv('CYBORGDB_API_KEY')
    cyborg = CyborgDBRealClient(api_key=api_key)
    cyborg.create_index("medical_records", embedder.dimension)
    
    for i in range(0, len(embedded_records), 50):
        batch = embedded_records[i:i+50]
        cyborg.add_items("medical_records", batch)
        print(f"  Progress: {min(i+50, len(embedded_records))}/{len(embedded_records)}")
    
    print("\n" + "=" * 60)
    print("✅ DATA LOADED - COMPLETE RECORDS WITH NO REDACTION!")
    print("=" * 60)
    print("\nNext: python src/api_fast.py")

if __name__ == "__main__":
    main()
