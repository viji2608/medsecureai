#!/usr/bin/env python3
"""
Data preparation WITHOUT PHI removal - for synthetic data only
"""

import pandas as pd
import hashlib
from typing import List, Dict

class MedicalDataPrep:
    """Prepare synthetic medical records without redaction"""
    
    def __init__(self):
        self.stats = {
            'total_processed': 0,
            'records_anonymized': 0
        }
    
    def anonymize_id(self, record_id: str) -> str:
        """Create anonymized hash ID"""
        return hashlib.sha256(f"{record_id}medsecure".encode()).hexdigest()[:16]
    
    def prepare_record(self, record: Dict) -> Dict:
        """Prepare a single medical record - NO REDACTION"""
        # Just take the clinical summary as-is
        clinical_summary = record.get('clinical_summary', '')
        
        prepared = {
            'anon_id': self.anonymize_id(str(record.get('record_id', 'unknown'))),
            'text': clinical_summary,  # Full text, no removal
            'metadata': {
                'age_range': record.get('age_range', 'Unknown'),
                'condition': record.get('primary_condition', 'Unknown'),
                'record_type': 'clinical_note',
                'data_source': 'synthetic'
            }
        }
        
        self.stats['records_anonymized'] += 1
        return prepared
    
    def prepare_records(self, df: pd.DataFrame) -> List[Dict]:
        """Prepare entire dataset"""
        print(f"Processing {len(df)} medical records...")
        
        records = []
        for idx, row in df.iterrows():
            try:
                prepared = self.prepare_record(row.to_dict())
                records.append(prepared)
            except Exception as e:
                print(f"⚠️  Warning: Failed to process record {idx}: {e}")
                continue
        
        self.stats['total_processed'] = len(records)
        print(f"✅ Processed {len(records)} records WITHOUT redaction")
        
        return records
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
