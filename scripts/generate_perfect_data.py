#!/usr/bin/env python3
"""
Generate perfectly formatted medical records for hackathon demo
"""

import pandas as pd
import random
import os

def generate_perfect_records(num_records=200):
    """Generate clean, professional medical records"""
    
    conditions = {
        'Type 2 Diabetes Mellitus': {
            'meds': ['Metformin 1000mg BID', 'Insulin Glargine 20 units QHS', 'Glipizide 5mg daily'],
            'symptoms': 'elevated blood glucose, polydipsia, polyuria',
            'vitals': {'bp': (120, 140), 'hr': (70, 85)}
        },
        'Essential Hypertension': {
            'meds': ['Lisinopril 10mg daily', 'Amlodipine 5mg daily', 'HCTZ 25mg daily'],
            'symptoms': 'occasional headaches, no chest pain',
            'vitals': {'bp': (135, 150), 'hr': (65, 80)}
        },
        'COPD': {
            'meds': ['Albuterol inhaler PRN', 'Tiotropium 18mcg daily', 'Prednisone 10mg daily'],
            'symptoms': 'shortness of breath, chronic cough',
            'vitals': {'bp': (115, 130), 'hr': (75, 90)}
        },
        'Congestive Heart Failure': {
            'meds': ['Furosemide 40mg daily', 'Carvedilol 12.5mg BID', 'Lisinopril 20mg daily'],
            'symptoms': 'bilateral leg edema, dyspnea on exertion',
            'vitals': {'bp': (110, 130), 'hr': (70, 85)}
        },
        'Hyperlipidemia': {
            'meds': ['Atorvastatin 40mg QHS', 'Ezetimibe 10mg daily'],
            'symptoms': 'asymptomatic, found on routine labs',
            'vitals': {'bp': (118, 132), 'hr': (68, 78)}
        }
    }
    
    records = []
    
    for i in range(num_records):
        age = random.randint(45, 85)
        age_range = f"{age//10*10}-{age//10*10+9}"
        
        # Select primary condition
        condition_name = random.choice(list(conditions.keys()))
        condition_data = conditions[condition_name]
        
        # Select medications
        num_meds = random.randint(2, 3)
        meds = random.sample(condition_data['meds'], num_meds)
        
        # Vitals
        bp_range = condition_data['vitals']['bp']
        hr_range = condition_data['vitals']['hr']
        bp_sys = random.randint(*bp_range)
        bp_dia = random.randint(70, 90)
        hr = random.randint(*hr_range)
        
        # Create clean summary
        summary = f"""PATIENT SUMMARY

Age Range: {age_range} years
Primary Diagnosis: {condition_name}

Chief Complaint: Patient reports {condition_data['symptoms']}

Current Medications:
{chr(10).join(f'  • {med}' for med in meds)}

Vital Signs:
  • Blood Pressure: {bp_sys}/{bp_dia} mmHg
  • Heart Rate: {hr} bpm  
  • Temperature: 98.{random.randint(0,9)}°F
  • O2 Saturation: {random.randint(95,99)}%

Assessment: Stable chronic condition with good medication adherence. Patient demonstrates understanding of disease management and lifestyle modifications.

Plan: Continue current medication regimen. Laboratory work ordered (HbA1c, lipid panel, BMP). Follow-up appointment in {random.choice([1,2,3])} months. Patient counseled on warning signs and when to seek emergency care."""
        
        record = {
            'record_id': f'MRN_{i:06d}',
            'age_range': age_range,
            'primary_condition': condition_name,
            'comorbidities': 'None documented',
            'medication_count': len(meds),
            'clinical_summary': summary
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("=" * 60)
    print("🏥 Generating Perfect Medical Records for Hackathon")
    print("=" * 60)
    
    df = generate_perfect_records(200)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_records.csv', index=False)
    
    print(f"\n✅ Generated {len(df)} perfect records")
    print(f"✅ Saved to: data/synthetic_records.csv")
    
    print("\n📄 Sample Record:")
    print("-" * 60)
    print(df.iloc[0]['clinical_summary'])
    print("-" * 60)
    
    print("\n🔄 Now reload data:")
    print("   rm data/embeddings_cache.pkl")
    print("   python scripts/load_data_once.py")
