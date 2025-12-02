#!/usr/bin/env python3
"""
Generate clean, professional medical records without excessive redaction
"""

import pandas as pd
import random
import os
from datetime import datetime, timedelta

def generate_clean_medical_data(num_records=200):
    """Generate clean medical records"""
    
    conditions = [
        'Type 2 Diabetes Mellitus',
        'Essential Hypertension', 
        'Chronic Obstructive Pulmonary Disease',
        'Congestive Heart Failure',
        'Asthma',
        'Coronary Artery Disease',
        'Chronic Kidney Disease',
        'Hyperlipidemia',
        'Atrial Fibrillation',
        'Osteoarthritis'
    ]
    
    medications = [
        'Metformin 1000mg twice daily',
        'Lisinopril 10mg once daily',
        'Atorvastatin 20mg at bedtime',
        'Amlodipine 5mg once daily',
        'Albuterol inhaler as needed',
        'Furosemide 40mg once daily',
        'Aspirin 81mg once daily',
        'Levothyroxine 50mcg once daily'
    ]
    
    symptoms = [
        'elevated fasting blood glucose levels',
        'shortness of breath on exertion',
        'persistent fatigue',
        'intermittent chest discomfort',
        'bilateral lower extremity edema',
        'chronic lower back pain'
    ]
    
    records = []
    
    for i in range(num_records):
        age = random.randint(40, 85)
        age_range = f"{age//10*10}-{age//10*10+9}"
        
        # Pick conditions
        num_conditions = random.randint(1, 3)
        patient_conditions = random.sample(conditions, num_conditions)
        primary_condition = patient_conditions[0]
        comorbidities = ', '.join(patient_conditions[1:]) if len(patient_conditions) > 1 else 'None documented'
        
        # Pick medications
        num_meds = random.randint(2, 4)
        patient_meds = random.sample(medications, num_meds)
        
        # Pick symptoms
        patient_symptoms = random.sample(symptoms, random.randint(1, 2))
        
        # Create clean clinical note
        summary = f"""Patient presents for routine follow-up visit.

AGE: {age_range} years
PRIMARY DIAGNOSIS: {primary_condition}
COMORBIDITIES: {comorbidities}

CHIEF COMPLAINT: Patient reports {' and '.join(patient_symptoms)}.

CURRENT MEDICATIONS:
{chr(10).join('• ' + med for med in patient_meds)}

VITAL SIGNS:
- Blood Pressure: {random.randint(110, 145)}/{random.randint(70, 90)} mmHg
- Heart Rate: {random.randint(65, 85)} bpm
- Temperature: 98.{random.randint(0, 9)}°F

ASSESSMENT: Stable condition with ongoing chronic disease management. Patient is adherent to medication regimen.

PLAN:
- Continue current medications
- Laboratory work ordered (HbA1c, lipid panel, comprehensive metabolic panel)
- Follow-up in {random.choice([1, 2, 3])} months
- Patient educated on lifestyle modifications and warning signs"""
        
        record = {
            'record_id': f'MRN_{i:06d}',
            'age_range': age_range,
            'primary_condition': primary_condition,
            'comorbidities': comorbidities,
            'medication_count': len(patient_meds),
            'clinical_summary': summary,
            'created_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

def main():
    print("=" * 60)
    print("🏥 Generating Clean Medical Records")
    print("=" * 60)
    
    df = generate_clean_medical_data(num_records=200)
    
    # Save
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'synthetic_records_clean.csv')
    
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Generated {len(df)} clean records")
    print(f"✅ Saved to: {output_path}")
    
    # Show sample
    print("\n📄 Sample Record:")
    print("-" * 60)
    print(df.iloc[0]['clinical_summary'])
    print("-" * 60)
    
    print("\n🔄 Now reload data:")
    print("   python scripts/reload_clean_data.py")

if __name__ == "__main__":
    main()
