#!/usr/bin/env python3
"""
Clean data preparation - Professional medical records
"""

import pandas as pd
import hashlib
from typing import List, Dict

class MedicalDataPrep:
    """Prepare clean, professional medical records"""
    
    def __init__(self):
        self.stats = {
            'total_processed': 0,
            'records_anonymized': 0
        }
    
    def anonymize_id(self, record_id: str) -> str:
        """Create anonymized hash ID"""
        return hashlib.sha256(f"{record_id}medsecure".encode()).hexdigest()[:16]
    
    def prepare_record(self, record: Dict) -> Dict:
        """Prepare a single medical record with clean text"""
        
        # Get the original summary
        summary = record.get('clinical_summary', '')
        
        # Create clean, professional clinical note
        age_range = record.get('age_range', 'Adult')
        condition = record.get('primary_condition', 'Unknown condition')
        comorbidities = record.get('comorbidities', 'None')
        
        # Build professional clinical text
        clinical_text = f"""Patient Age: {age_range} years

Primary Diagnosis: {condition}
Comorbidities: {comorbidities}

Clinical Summary:
{summary}

Assessment: Patient presents with stable condition requiring ongoing management and monitoring."""
        
        prepared = {
            'anon_id': self.anonymize_id(str(record.get('record_id', 'unknown'))),
            'text': clinical_text.strip(),
            'metadata': {
                'age_range': age_range,
                'condition': condition,
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
        print(f"✅ Processed {len(records)} clean records")
        
        return records
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
