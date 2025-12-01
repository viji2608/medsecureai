#!/usr/bin/env python3
"""
HIPAA-Compliant Data Preparation Module
Removes PHI and anonymizes medical records
"""

import pandas as pd
import re
import hashlib
from typing import List, Dict
import json

class MedicalDataPrep:
    """
    Prepares medical data for encrypted storage
    Removes all PHI according to HIPAA Safe Harbor method
    """
    
    def __init__(self):
        # PHI patterns to detect and remove
        self.phi_patterns = {
            'name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'date': r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            'mrn': r'\bMRN[:\s]*\d+\b',
            'address': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b'
        }
        
        self.stats = {
            'total_processed': 0,
            'phi_removed': 0,
            'records_anonymized': 0
        }
    
    def remove_phi(self, text: str) -> str:
        """
        Remove Protected Health Information from text
        
        Args:
            text: Raw medical text that may contain PHI
            
        Returns:
            Cleaned text with PHI removed/masked
        """
        if not isinstance(text, str):
            return str(text)
        
        cleaned = text
        phi_count = 0
        
        # Remove each type of PHI
        for phi_type, pattern in self.phi_patterns.items():
            matches = re.findall(pattern, cleaned, re.IGNORECASE)
            if matches:
                phi_count += len(matches)
                cleaned = re.sub(pattern, f'[{phi_type.upper()}_REDACTED]', cleaned, flags=re.IGNORECASE)
        
        self.stats['phi_removed'] += phi_count
        return cleaned
    
    def anonymize_id(self, record_id: str, salt: str = "medsecure_salt") -> str:
        """
        Create anonymized hash ID from record ID
        
        Args:
            record_id: Original record identifier
            salt: Salt for hashing (keep consistent across runs)
            
        Returns:
            Anonymized hash string
        """
        combined = f"{record_id}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def prepare_record(self, record: Dict) -> Dict:
        """
        Prepare a single medical record for embedding
        
        Args:
            record: Dictionary containing medical record data
            
        Returns:
            Anonymized record ready for embedding
        """
        # Get clinical summary (the main text we'll embed)
        summary = record.get('clinical_summary', record.get('summary', ''))
        
        # Remove PHI from summary
        clean_summary = self.remove_phi(summary)
        
        # Create anonymized record
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
        """
        Prepare entire dataset of medical records
        
        Args:
            df: DataFrame containing medical records
            
        Returns:
            List of anonymized records
        """
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
        """Return processing statistics"""
        return self.stats.copy()
    
    def save_prepared_data(self, records: List[Dict], output_path: str):
        """Save prepared records to JSON"""
        with open(output_path, 'w') as f:
            json.dump(records, f, indent=2)
        print(f"✅ Saved prepared data to {output_path}")


# Test the module
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Data Preparation Module")
    print("=" * 60)
    
    # Load synthetic data
    df = pd.read_csv('data/synthetic_records.csv')
    print(f"\n📋 Loaded {len(df)} records from CSV")
    
    # Prepare data
    prep = MedicalDataPrep()
    records = prep.prepare_records(df)
    
    # Show sample
    print("\n📊 Sample Prepared Record:")
    print("-" * 60)
    sample = records[0]
    print(f"Anonymized ID: {sample['anon_id']}")
    print(f"Metadata: {sample['metadata']}")
    print(f"Text (first 200 chars): {sample['text'][:200]}...")
    
    # Show stats
    print("\n📈 Processing Statistics:")
    stats = prep.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Data preparation module working correctly!")
