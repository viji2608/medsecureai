#!/usr/bin/env python3
"""Test all Phase 2 modules together"""

import sys
sys.path.append('src')

print("=" * 60)
print("🧪 Phase 2 Integration Test")
print("=" * 60)

# Test 1: Import all modules
print("\n[1/5] Testing imports...")
try:
    from data_prep import MedicalDataPrep
    from embedding import MedicalEmbedder
    from cyborg_client import CyborgDBClient
    from audit import AuditLogger
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Data preparation
print("\n[2/5] Testing data preparation...")
import pandas as pd
df = pd.read_csv('data/synthetic_records.csv')
prep = MedicalDataPrep()
records = prep.prepare_records(df[:10])
print(f"✅ Prepared {len(records)} records")

# Test 3: Embedding generation
print("\n[3/5] Testing embedding generation...")
embedder = MedicalEmbedder()
embedded_records = embedder.embed_records(records)
print(f"✅ Generated embeddings for {len(embedded_records)} records")

# Test 4: CyborgDB operations
print("\n[4/5] Testing CyborgDB...")
client = CyborgDBClient()
client.create_collection("integration_test", 384)
client.insert_encrypted("integration_test", embedded_records)
query_emb = embedder.embed_query("test query")
results = client.search_encrypted("integration_test", query_emb.tolist())
print(f"✅ CyborgDB operations complete: {len(results['matches'])} results")

# Test 5: Audit logging
print("\n[5/5] Testing audit logging...")
audit = AuditLogger()
query_id = audit.log_query("TEST_USER", "integration test query")
audit.log_response(query_id, len(results['matches']), 100.0)
summary = audit.get_audit_summary()
print(f"✅ Audit logging complete: {summary['total_events']} events logged")

print("\n" + "=" * 60)
print("🎉 All Phase 2 modules working correctly!")
print("=" * 60)
print("\nNext steps:")
print("1. Start the API: python src/chatbot.py")
print("2. Open web interface: open web/index.html")
print("3. Begin Phase 3: CyborgDB evaluation")
