#!/usr/bin/env python3
"""
Generate synthetic medical records for MedSecureAI demo
Creates realistic but fake patient data
"""

import pandas as pd
import random
import os
from datetime import datetime, timedelta

def generate_synthetic_medical_data(num_records=200):
    """Generate synthetic EHR-style records"""
    
    # Medical vocabulary for realistic records
    conditions = [
        'Type 2 Diabetes Mellitus',
        'Essential Hypertension', 
        'Chronic Obstructive Pulmonary Disease (COPD)',
        'Congestive Heart Failure (CHF)',
        'Asthma',
        'Coronary Artery Disease',
        'Chronic Kidney Disease Stage 3',
        'Hyperlipidemia',
        'Atrial Fibrillation',
        'Osteoarthritis',
        'Major Depressive Disorder',
        'Gastroesophageal Reflux Disease (GERD)',
        'Hypothyroidism',
        'Peripheral Artery Disease'
    ]
    
    medications = [
        'Metformin 1000mg twice daily',
        'Lisinopril 10mg once daily',
        'Atorvastatin 20mg at bedtime',
        'Amlodipine 5mg once daily',
        'Albuterol inhaler as needed',
        'Furosemide 40mg once daily',
        'Aspirin 81mg once daily',
        'Omeprazole 20mg once daily',
        'Levothyroxine 50mcg once daily',
        'Gabapentin 300mg three times daily',
        'Insulin glargine 20 units at bedtime',
        'Warfarin 5mg once daily',
        'Clopidogrel 75mg once daily',
        'Losartan 50mg once daily'
    ]
    
    symptoms = [
        'elevated fasting blood glucose (140-180 mg/dL)',
        'chest pain on exertion',
        'shortness of breath with minimal activity',
        'persistent fatigue and weakness',
        'intermittent dizziness',
        'chronic lower back pain',
        'persistent dry cough',
        'bilateral leg swelling',
        'frequent urination and increased thirst',
        'palpitations and irregular heartbeat',
        'difficulty sleeping',
        'numbness and tingling in extremities'
    ]
    
    treatments = [
        'Started on medication therapy, lifestyle modifications recommended',
        'Dosage adjustment made, follow-up in 4 weeks',
        'Referred to cardiology for further evaluation',
        'Labs ordered: HbA1c, lipid panel, BMP',
        'Physical therapy referral provided',
        'Dietary consultation scheduled',
        'Continue current medications, monitoring advised',
        'Emergency department visit if symptoms worsen'
    ]
    
    records = []
    
    for i in range(num_records):
        # Generate realistic demographics
        age = random.randint(30, 85)
        age_range = f"{age//10*10}-{age//10*10+9}"
        
        # Pick 1-3 conditions (comorbidities are common)
        num_conditions = random.randint(1, 3)
        patient_conditions = random.sample(conditions, num_conditions)
        
        # Medications based on conditions
        num_meds = random.randint(1, 4)
        patient_meds = random.sample(medications, num_meds)
        
        # Symptoms
        num_symptoms = random.randint(1, 2)
        patient_symptoms = random.sample(symptoms, num_symptoms)
        
        # Treatment plan
        treatment = random.choice(treatments)
        
        # Create clinical note
        summary = f"""Patient in {age_range} age range presents for follow-up. 

Active Diagnoses: {', '.join(patient_conditions)}

Chief Complaints: Reports {', and '.join(patient_symptoms)}.

Current Medications: {'; '.join(patient_meds)}

Assessment and Plan: {treatment}

Vital Signs: BP {random.randint(110, 150)}/{random.randint(70, 95)}, HR {random.randint(60, 90)}, Temp 98.{random.randint(0, 9)}°F

Follow-up scheduled in {random.choice([2, 4, 8, 12])} weeks."""
        
        # Create record
        record = {
            'record_id': f'MRN_{i:06d}',
            'age_range': age_range,
            'primary_condition': patient_conditions[0],
            'comorbidities': ', '.join(patient_conditions[1:]) if len(patient_conditions) > 1 else 'None',
            'medication_count': len(patient_meds),
            'clinical_summary': summary.strip(),
            'created_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

def main():
    print("=" * 60)
    print("🏥 Generating Synthetic Medical Records")
    print("=" * 60)
    
    # Generate data
    print("\n📋 Creating synthetic patient records...")
    df = generate_synthetic_medical_data(num_records=200)
    
    # Save to CSV
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'synthetic_records.csv')
    
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} records")
    print(f"✅ Saved to: {output_path}")
    
    # Show sample
    print("\n📊 Sample Record:")
    print("-" * 60)
    sample = df.iloc[0]
    print(f"Record ID: {sample['record_id']}")
    print(f"Age Range: {sample['age_range']}")
    print(f"Condition: {sample['primary_condition']}")
    print(f"\nClinical Summary:\n{sample['clinical_summary'][:200]}...")
    
    # Statistics
    print("\n📈 Dataset Statistics:")
    print(f"  - Total Records: {len(df)}")
    print(f"  - Age Ranges: {df['age_range'].nunique()} unique ranges")
    print(f"  - Conditions: {df['primary_condition'].nunique()} unique diagnoses")
    print(f"  - Avg Summary Length: {df['clinical_summary'].str.len().mean():.0f} characters")
    
    print("\n✅ Data generation complete!")
    print("Next: Run 'python scripts/verify_setup.py'")

if __name__ == "__main__":
    main()
