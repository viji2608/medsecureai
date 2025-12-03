#!/usr/bin/env python3
"""
Generate clean, complete medical records - NO truncation, NO excessive redaction
"""

import pandas as pd
import random
import os
import hashlib

def generate_professional_records(num_records=200):
    """Generate complete, professional medical records"""
    
    conditions_data = {
        'Type 2 Diabetes Mellitus': {
            'symptoms': 'Patient reports polyuria, polydipsia, and recent weight loss. Blood glucose levels elevated at 180-220 mg/dL fasting.',
            'medications': ['Metformin 1000mg BID', 'Glipizide 5mg daily', 'Insulin Glargine 20 units QHS'],
            'vitals': {'bp_sys': (120, 140), 'bp_dia': (70, 85), 'hr': (70, 85)},
            'plan': 'Continue current diabetic regimen. Increase metformin to 1000mg BID. Patient counseled on carbohydrate counting and portion control. HbA1c ordered for next visit.'
        },
        'Essential Hypertension': {
            'symptoms': 'Patient presents with elevated blood pressure readings at home (145-155/90-95 mmHg). Reports occasional headaches, no chest pain or shortness of breath.',
            'medications': ['Lisinopril 20mg daily', 'Amlodipine 5mg daily', 'Hydrochlorothiazide 25mg daily'],
            'vitals': {'bp_sys': (135, 155), 'bp_dia': (85, 95), 'hr': (65, 80)},
            'plan': 'Increase lisinopril to 20mg daily. Patient advised on DASH diet and sodium restriction. Blood pressure monitoring log provided. Renal function panel and potassium levels ordered.'
        },
        'Chronic Obstructive Pulmonary Disease': {
            'symptoms': 'Patient reports increased shortness of breath with exertion, chronic productive cough with clear sputum. Denies fever or hemoptysis.',
            'medications': ['Albuterol inhaler 2 puffs PRN', 'Tiotropium 18mcg daily', 'Fluticasone/Salmeterol 250/50 BID'],
            'vitals': {'bp_sys': (118, 135), 'bp_dia': (72, 82), 'hr': (78, 92)},
            'plan': 'Continue current bronchodilator therapy. Prescribed oral prednisone 40mg daily for 5 days for acute exacerbation. Smoking cessation counseling provided. Pulmonary function testing scheduled.'
        },
        'Congestive Heart Failure': {
            'symptoms': 'Patient reports bilateral lower extremity edema, orthopnea (sleeps on 3 pillows), and dyspnea on exertion. Weight gain of 5 pounds over past week.',
            'medications': ['Furosemide 40mg BID', 'Carvedilol 12.5mg BID', 'Lisinopril 20mg daily', 'Spironolactone 25mg daily'],
            'vitals': {'bp_sys': (110, 130), 'bp_dia': (68, 80), 'hr': (72, 88)},
            'plan': 'Increase furosemide to 40mg BID. Daily weight monitoring instructed. Fluid restriction to 2 liters daily. BNP level and echocardiogram ordered. Follow-up in 1 week.'
        },
        'Hyperlipidemia': {
            'symptoms': 'Asymptomatic. Routine lipid panel shows elevated LDL cholesterol at 165 mg/dL, triglycerides 210 mg/dL. Patient has family history of coronary artery disease.',
            'medications': ['Atorvastatin 40mg QHS', 'Ezetimibe 10mg daily', 'Aspirin 81mg daily'],
            'vitals': {'bp_sys': (122, 138), 'bp_dia': (74, 84), 'hr': (68, 78)},
            'plan': 'Continue atorvastatin 40mg nightly. Patient counseled on therapeutic lifestyle changes including low-fat diet and regular aerobic exercise. Repeat lipid panel in 3 months.'
        },
        'Chronic Kidney Disease Stage 3': {
            'symptoms': 'Patient reports fatigue and decreased appetite. GFR estimated at 45 mL/min. Trace proteinuria on urinalysis. Blood pressure well controlled.',
            'medications': ['Lisinopril 10mg daily', 'Calcium carbonate 1000mg TID with meals', 'Epoetin alfa 4000 units SC weekly'],
            'vitals': {'bp_sys': (125, 140), 'bp_dia': (75, 85), 'hr': (70, 82)},
            'plan': 'Nephrology referral placed. Continue ACE inhibitor for renal protection. Restrict dietary potassium and phosphorus. Monitor renal function monthly. Patient educated on progression.'
        },
        'Osteoarthritis': {
            'symptoms': 'Patient reports bilateral knee pain, worse with prolonged standing and stair climbing. Morning stiffness lasting 15-20 minutes. No joint swelling or warmth noted.',
            'medications': ['Acetaminophen 1000mg TID PRN', 'Meloxicam 15mg daily', 'Glucosamine 1500mg daily'],
            'vitals': {'bp_sys': (128, 142), 'bp_dia': (76, 86), 'hr': (72, 84)},
            'plan': 'Continue current analgesic regimen. Physical therapy referral for strengthening exercises. Weight loss counseling provided (target 10 pound reduction). Intra-articular corticosteroid injection offered.'
        },
        'Atrial Fibrillation': {
            'symptoms': 'Patient reports palpitations and occasional lightheadedness. ECG confirms atrial fibrillation with rapid ventricular response (110-130 bpm). CHADS-VASC score calculated at 4.',
            'medications': ['Metoprolol 50mg BID', 'Apixaban 5mg BID', 'Digoxin 0.125mg daily'],
            'vitals': {'bp_sys': (115, 132), 'bp_dia': (70, 82), 'hr': (88, 115)},
            'plan': 'Rate control strategy with beta blocker. Anticoagulation with apixaban for stroke prevention. Cardiology referral for possible cardioversion. TSH and echocardiogram ordered.'
        }
    }
    
    records = []
    
    for i in range(num_records):
        # Select random condition
        condition_name = random.choice(list(conditions_data.keys()))
        condition = conditions_data[condition_name]
        
        # Generate demographics
        age = random.randint(45, 89)
        age_range = f"{age//10*10}-{age//10*10+9}"
        
        # Select 2-3 medications
        num_meds = random.randint(2, 3)
        meds = random.sample(condition['medications'], min(num_meds, len(condition['medications'])))
        
        # Generate vitals
        bp_sys = random.randint(*condition['vitals']['bp_sys'])
        bp_dia = random.randint(*condition['vitals']['bp_dia'])
        hr = random.randint(*condition['vitals']['hr'])
        temp = f"98.{random.randint(0, 9)}"
        o2_sat = random.randint(94, 99)
        
        # Create complete clinical note
        clinical_note = f"""PATIENT CLINICAL NOTE

Age Group: {age_range} years
Visit Type: Follow-up appointment

PRIMARY DIAGNOSIS: {condition_name}

CHIEF COMPLAINT AND HISTORY:
{condition['symptoms']}

CURRENT MEDICATIONS:
{chr(10).join(f'  • {med}' for med in meds)}

VITAL SIGNS (Current Visit):
  • Blood Pressure: {bp_sys}/{bp_dia} mmHg
  • Heart Rate: {hr} bpm
  • Temperature: {temp}°F
  • Oxygen Saturation: {o2_sat}% on room air
  • Respiratory Rate: {random.randint(14, 18)} breaths/min

PHYSICAL EXAMINATION:
  • General: Alert and oriented, appears stated age, in no acute distress
  • Cardiovascular: Regular rate and rhythm, no murmurs, rubs, or gallops
  • Respiratory: Clear to auscultation bilaterally, no wheezes or crackles
  • Extremities: No cyanosis, clubbing, or edema noted

ASSESSMENT AND PLAN:
{condition['plan']}

PATIENT EDUCATION:
Patient demonstrates understanding of treatment plan and medication regimen. Warning signs discussed. Patient instructed to call or present to ED for any concerning symptoms.

FOLLOW-UP: Scheduled for {random.choice(['2 weeks', '1 month', '3 months'])}"""
        
        # Create record
        record = {
            'record_id': f'MRN_{i:06d}',
            'age_range': age_range,
            'primary_condition': condition_name,
            'comorbidities': random.choice(['Hypertension', 'Hyperlipidemia', 'Diabetes', 'None documented']),
            'medication_count': len(meds),
            'clinical_summary': clinical_note
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

def main():
    print("=" * 70)
    print("🏥 GENERATING COMPLETE PROFESSIONAL MEDICAL RECORDS")
    print("=" * 70)
    
    # Generate records
    df = generate_professional_records(200)
    
    # Save
    os.makedirs('data', exist_ok=True)
    output_file = 'data/synthetic_records.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Generated {len(df)} complete professional records")
    print(f"✅ Saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("📄 SAMPLE RECORD (Full Length):")
    print("=" * 70)
    print(df.iloc[0]['clinical_summary'])
    print("=" * 70)
    
    # Show stats
    print(f"\n📊 Statistics:")
    print(f"  • Total Records: {len(df)}")
    print(f"  • Conditions: {df['primary_condition'].nunique()}")
    print(f"  • Avg Text Length: {df['clinical_summary'].str.len().mean():.0f} characters")
    
    print("\n🔄 Next Steps:")
    print("  1. rm -f data/embeddings_cache.pkl")
    print("  2. python scripts/load_data_once.py")
    print("  3. python src/api_fast.py")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
