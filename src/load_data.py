#!/usr/bin/env python3
"""Load data into CyborgDB before starting API"""

import sys
sys.path.append('.')

from src.data_prep import MedicalDataPrep
from src.embedding import MedicalEmbedder
from src.cyborg_client import CyborgDBClient
import pandas as pd

print("=" * 60)
print("📦 Loading Medical Data into CyborgDB")
print("=" * 60)

# Load data
print("\n[1/4] Loading records...")
df = pd.read_csv('data/synthetic_records.csv')
prep = MedicalDataPrep()
records = prep.prepare_records(df)

# Generate embeddings
print("\n[2/4] Generating embeddings...")
embedder = MedicalEmbedder()
embedded_records = embedder.embed_records(records)

# Connect to CyborgDB
print("\n[3/4] Connecting to CyborgDB...")
client = CyborgDBClient()

# Create collection and insert
print("\n[4/4] Inserting into database...")
collection_name = "medical_records"
client.create_collection(collection_name, embedder.dimension)

batch_size = 50
for i in range(0, len(embedded_records), batch_size):
    batch = embedded_records[i:i+batch_size]
    client.insert_encrypted(collection_name, batch)
    print(f"  ✓ Batch {i//batch_size + 1}/{(len(embedded_records)-1)//batch_size + 1}")

print("\n" + "=" * 60)
print(f"✅ Successfully loaded {len(embedded_records)} records!")
print("=" * 60)
print("\nNow start the API:")
print("  python src/chatbot.py")
