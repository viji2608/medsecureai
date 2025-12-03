#!/usr/bin/env python3
"""
Clean data prep - NO PHI removal for synthetic data
"""
import hashlib
from typing import List, Dict

class MedicalDataPrep:
    def __init__(self):
        self.stats = {'total_processed': 0}
    
    def anonymize_id(self, record_id: str) -> str:
        """Create anonymized hash ID"""
        return hashlib.sha256(f"{record_id}".encode()).hexdigest()[:16]
    
    def prepare_record(self, record: Dict) -> Dict:
        """Prepare record - NO REDACTION"""
        return {
            'id': self.anonymize_id(str(record.get('record_id', 'unknown'))),
            'text': record.get('clinical_summary', ''),  # Full text, no removal
            'metadata': {
                'age_range': record.get('age_range', 'Unknown'),
                'condition': record.get('primary_condition', 'Unknown')
            }
        }
    
    def prepare_records(self, df) -> List[Dict]:
        """Prepare all records"""
        records = []
        for idx, row in df.iterrows():
            records.append(self.prepare_record(row.to_dict()))
        self.stats['total_processed'] = len(records)
        return records
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
