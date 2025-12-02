#!/usr/bin/env python3
"""
Reload CyborgDB with clean data
"""

import sys
sys.path.append('src')

from embedding import MedicalEmbedder
from cyborg_real_client import CyborgDBRealClient
import pandas as pd
import os
import hashlib
from dotenv import load_dotenv

class SimpleDataPrep:
    """Simple data prep without aggressive redaction"""
    
    def anonymize_id(self, record_id: str) -> str:
        return hashlib.sha256(f"{record_id}medsecure".encode()).hexdigest()[:16]
    
    def prepare_record(self, record):
        return {
            'anon_id': self.anonymize_id(str(record.get('record_id', 'unknown'))),
            'text': record.get('clinical_summary', ''),
            'metadata': {
                'age_range': record.get('age_range', 'Unknown'),
                'condition': record.get('primary_condition', 'Unknown'),
                'record_type': 'clinical_note'
            }
        }
    
    def prepare_records(self, df):
        print(f"Preparing {len(df)} records...")
        records = []
        for idx, row in df.iterrows():
            records.append(self.prepare_record(row.to_dict()))
        print(f"✅ Prepared {len(records)} records")
        return records

def main():
    load_dotenv()
    
    print("=" * 60)
    print("🔄 Reloading Clean Data into CyborgDB")
    print("=" * 60)
    
    # Check for clean data file
    clean_file = 'data/synthetic_records_clean.csv'
    if os.path.exists(clean_file):
        df = pd.read_csv(clean_file)
        print(f"\n✅ Using clean data: {clean_file}")
    else:
        df = pd.read_csv('data/synthetic_records.csv')
        print(f"\n⚠️  Using original data: data/synthetic_records.csv")
    
    # Prepare
    prep = SimpleDataPrep()
    records = prep.prepare_records(df)
    
    # Embed
    print("\n🧠 Generating embeddings...")
    embedder = MedicalEmbedder()
    embedded_records = embedder.embed_records(records)
    
    # Load to CyborgDB
    print("\n🔐 Loading to CyborgDB...")
    api_key = os.getenv('CYBORGDB_API_KEY')
    cyborg = CyborgDBRealClient(api_key=api_key)
    
    index_name = "medical_records"
    print(f"Creating index: {index_name}")
    cyborg.create_index(index_name, embedder.dimension)
    
    # Insert
    batch_size = 50
    for i in range(0, len(embedded_records), batch_size):
        batch = embedded_records[i:i+batch_size]
        cyborg.add_items(index_name, batch)
        progress = min(i + batch_size, len(embedded_records))
        print(f"  Loaded: {progress}/{len(embedded_records)} ({progress*100//len(embedded_records)}%)")
    
    # Test search
    print("\n🔍 Testing search...")
    query = "diabetes treatment"
    query_emb = embedder.embed_query(query)
    results = cyborg.search(index_name, query_emb.tolist(), top_k=3)
    
    if results['matches']:
        print(f"✅ Found {len(results['matches'])} matches")
        print("\nSample result:")
        print(results['matches'][0]['text'][:300] + "...")
    
    print("\n" + "=" * 60)
    print("✅ DATA RELOADED SUCCESSFULLY")
    print("=" * 60)
    print("\nNow restart API:")
    print("  python src/chatbot_autoload.py")

if __name__ == "__main__":
    main()
