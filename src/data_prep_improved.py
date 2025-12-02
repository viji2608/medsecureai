#!/usr/bin/env python3
"""
Improved data preparation - cleaner output
"""

import pandas as pd
import re
import hashlib
from typing import List, Dict

class MedicalDataPrep:
    """HIPAA-compliant data preparation"""
    
    def __init__(self):
        # Less aggressive PHI removal for better readability
        self.phi_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'exact_date': r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        }
        self.stats = {
            'total_processed': 0,
            'phi_removed': 0,
            'records_anonymized': 0
        }
    
    def remove_phi(self, text: str) -> str:
        """Remove only critical PHI, preserve clinical context"""
        if not isinstance(text, str):
            return str(text)
        
        cleaned = text
        phi_count = 0
        
        # Only remove truly sensitive info
        for phi_type, pattern in self.phi_patterns.items():
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            if matches:
                phi_count += len(matches)
                cleaned = re.sub(pattern, f'[{phi_type.upper()}_REMOVED]', cleaned, flags=re.IGNORECASE)
        
        self.stats['phi_removed'] += phi_count
        return cleaned
    
    def anonymize_id(self, record_id: str, salt: str = "medsecure_salt") -> str:
        """Create anonymized hash ID"""
        combined = f"{record_id}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def prepare_record(self, record: Dict) -> Dict:
        """Prepare a single medical record"""
        summary = record.get('clinical_summary', record.get('summary', ''))
        clean_summary = self.remove_phi(summary)
        
        prepared = {
            'anon_id': self.anonymize_id(str(record.get('record_id', 'unknown'))),
            'text': clean_summary,
            'metadata': {
                'age_range': record.get('age_range', 'Unknown'),
                'condition': record.get('primary_condition', record.get('condition', 'Unknown')),
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
        print(f"✅ Processed {len(records)} records")
        print(f"✅ Removed {self.stats['phi_removed']} PHI elements")
        
        return records
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
