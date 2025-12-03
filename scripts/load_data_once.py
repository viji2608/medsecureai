#!/usr/bin/env python3
"""
Load data into CyborgDB - Run this ONCE before starting API
"""

import sys
sys.path.append('src')

from data_prep import MedicalDataPrep
from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
import pandas as pd
import os
import pickle
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("=" * 60)
    print("📦 ONE-TIME DATA LOADING")
    print("=" * 60)
    
    # Check if already done
    if os.path.exists('data/embeddings_cache.pkl'):
        print("\n⚠️  Data already prepared!")
        print("If you want to reload, delete: data/embeddings_cache.pkl")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Load data
    print("\n[1/5] Loading synthetic records...")
    df = pd.read_csv('data/synthetic_records.csv')
    print(f"✅ Loaded {len(df)} records")
    
    # Prepare
    print("\n[2/5] Preparing records...")
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    print(f"✅ Prepared {len(records)} records")
    
    # Embed
    print("\n[3/5] Generating embeddings (this takes time)...")
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    print(f"✅ Generated {len(embedded_records)} embeddings")
    
    # Save embeddings for reuse
    print("\n[4/5] Caching embeddings...")
    os.makedirs('data', exist_ok=True)
    cache_data = {
        'embedded_records': embedded_records,
        'dimension': embedder.dimension
    }
    with open('data/embeddings_cache.pkl', 'wb') as f:
        pickle.dump(cache_data, f)
    print("✅ Embeddings cached to data/embeddings_cache.pkl")
    
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
    
    print("\n" + "=" * 60)
    print("✅ DATA LOADED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start API: python src/api_fast.py")
    print("2. Access web interface")

if __name__ == "__main__":
    main()
