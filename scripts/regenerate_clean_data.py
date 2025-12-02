#!/usr/bin/env python3
"""
Regenerate data with clean, professional formatting
"""

import sys
sys.path.append('src')

from data_prep_clean import MedicalDataPrep
from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
import pandas as pd
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    print("=" * 60)
    print("🔄 Regenerating Clean Medical Data")
    print("=" * 60)
    
    # Load original data
    df = pd.read_csv('data/synthetic_records.csv')
    
    # Prepare with clean formatting
    print("\n[1/4] Preparing clean records...")
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    
    # Show sample
    print("\n📄 Sample Record:")
    print("-" * 60)
    print(records[0]['text'][:300] + "...")
    print("-" * 60)
    
    # Generate embeddings
    print("\n[2/4] Generating embeddings...")
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    
    # Connect to CyborgDB
    print("\n[3/4] Connecting to CyborgDB...")
    api_key = os.getenv('CYBORGDB_API_KEY')
    cyborg = CyborgDBRealClient(api_key=api_key)
    
    # Create new index
    print("\n[4/4] Creating clean encrypted index...")
    index_name = "medical_records"
    
    # Note: If index exists, CyborgDB will overwrite or you may need to use a new name
    cyborg.create_index(index_name, embedder.dimension)
    
    # Insert clean data
    print("\nInserting clean encrypted records...")
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        cyborg.add_items(index_name, batch)
        print(f"  ✅ Batch {i//batch_size + 1}/{(len(embedded_records)-1)//batch_size + 1}")
    
    print("\n" + "=" * 60)
    print("✅ Clean data regenerated successfully!")
    print("🔐 All records encrypted with professional formatting")
    print("=" * 60)
    print("\nRestart your API server to use the new data:")
    print("  python src/chatbot_real.py")

if __name__ == "__main__":
    main()
