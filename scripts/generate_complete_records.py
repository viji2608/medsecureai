#!/usr/bin/env python3
import pandas as pd
import random
import os

def generate_complete_records(num=200):
    """Generate complete professional medical records"""
    
    conditions = {
        'Type 2 Diabetes Mellitus': {
            'symptoms': 'Patient reports polyuria, polydipsia, and recent weight loss over the past 3 months. Blood glucose levels consistently elevated at 180-220 mg/dL fasting. Patient has been compliant with current medication regimen but reports difficulty with dietary modifications.',
            'meds': ['Metformin 1000mg twice daily', 'Glipizide 5mg daily before breakfast', 'Insulin Glargine 20 units subcutaneous at bedtime'],
            'plan': 'Continue current diabetic regimen with dose adjustment. Increase metformin to 1000mg twice daily with meals. Patient extensively counseled on carbohydrate counting, portion control, and importance of regular blood glucose monitoring. HbA1c and comprehensive metabolic panel ordered for next visit in 3 months. Referral to certified diabetes educator provided.'
        },
        'Essential Hypertension': {
            'symptoms': 'Patient presents with persistently elevated blood pressure readings at home, averaging 145-155/90-95 mmHg over the past month. Reports occasional morning headaches that resolve spontaneously. Denies chest pain, shortness of breath, or visual changes. Blood pressure diary reviewed.',
            'meds': ['Lisinopril 20mg once daily', 'Amlodipine 5mg once daily', 'Hydrochlorothiazide 25mg once daily in morning'],
            'plan': 'Increase lisinopril to 20mg once daily for better blood pressure control. Patient extensively advised on DASH diet principles, sodium restriction to less than 2000mg daily, and importance of regular aerobic exercise. Home blood pressure monitoring log provided with instructions. Renal function panel and potassium levels ordered. Follow-up appointment scheduled in 4 weeks.'
        },
        'Chronic Obstructive Pulmonary Disease': {
            'symptoms': 'Patient reports increased shortness of breath with minimal exertion over the past week. Chronic productive cough with clear to white sputum. Denies fever, hemoptysis, or chest pain. Uses rescue inhaler 3-4 times daily. Sleep disturbed by coughing episodes.',
            'meds': ['Albuterol inhaler 2 puffs every 4-6 hours as needed', 'Tiotropium 18mcg inhaled once daily', 'Fluticasone/Salmeterol 250/50 one inhalation twice daily'],
            'plan': 'Continue current bronchodilator and corticosteroid therapy. Prescribed oral prednisone 40mg daily for 5 days for acute exacerbation. Extensive smoking cessation counseling provided with referral to cessation program. Pulmonary function testing scheduled. Patient educated on proper inhaler technique and importance of medication compliance. Emergency action plan reviewed.'
        },
        'Congestive Heart Failure': {
            'symptoms': 'Patient reports progressive bilateral lower extremity edema over past 2 weeks, now requiring elevation for relief. Orthopnea present, sleeping on 3 pillows. Dyspnea on exertion climbing one flight of stairs. Weight gain of 5 pounds over past week despite medication compliance.',
            'meds': ['Furosemide 40mg twice daily', 'Carvedilol 12.5mg twice daily', 'Lisinopril 20mg once daily', 'Spironolactone 25mg once daily'],
            'plan': 'Increase furosemide to 40mg twice daily for improved diuresis. Daily weight monitoring instructed with strict instructions to call if weight increases more than 3 pounds in one day. Fluid restriction to 2 liters daily. Sodium restriction emphasized. BNP level drawn today. Echocardiogram ordered to assess cardiac function. Cardiology follow-up arranged. Close monitoring plan established.'
        },
        'Hyperlipidemia': {
            'symptoms': 'Asymptomatic on routine screening. Recent lipid panel reveals significantly elevated LDL cholesterol at 165 mg/dL and triglycerides at 210 mg/dL despite statin therapy. HDL cholesterol low at 35 mg/dL. Patient has strong family history of premature coronary artery disease.',
            'meds': ['Atorvastatin 40mg once nightly', 'Ezetimibe 10mg once daily', 'Aspirin 81mg once daily', 'Fish oil 1000mg twice daily'],
            'plan': 'Continue atorvastatin 40mg nightly with plan to increase if needed. Patient extensively counseled on therapeutic lifestyle changes including low-fat, low-cholesterol diet with emphasis on plant sterols and soluble fiber. Regular aerobic exercise program recommended with target of 150 minutes weekly. Repeat lipid panel in 3 months to assess response to therapy. Discussed cardiovascular risk reduction strategies.'
        }
    }
    
    records = []
    for i in range(num):
        cond_name = random.choice(list(conditions.keys()))
        cond = conditions[cond_name]
        age = random.randint(45, 89)
        age_range = f"{age//10*10}-{age//10*10+9}"
        
        meds = random.sample(cond['meds'], min(random.randint(2, 3), len(cond['meds'])))
        
        bp_sys = random.randint(118, 155)
        bp_dia = random.randint(68, 95)
        hr = random.randint(65, 95)
        temp = f"98.{random.randint(2, 8)}"
        o2 = random.randint(94, 99)
        rr = random.randint(14, 20)
        
        clinical_note = f"""PATIENT CLINICAL NOTE

Age Group: {age_range} years
Visit Type: Follow-up appointment

PRIMARY DIAGNOSIS: {cond_name}

CHIEF COMPLAINT AND HISTORY:
{cond['symptoms']}

CURRENT MEDICATIONS:
{chr(10).join(f'  • {med}' for med in meds)}

VITAL SIGNS (Current Visit):
  • Blood Pressure: {bp_sys}/{bp_dia} mmHg
  • Heart Rate: {hr} beats per minute
  • Temperature: {temp}°F oral
  • Oxygen Saturation: {o2}% on room air
  • Respiratory Rate: {rr} breaths per minute
  • Weight: {random.randint(150, 220)} lbs
  • BMI: {random.randint(24, 32)} kg/m²

PHYSICAL EXAMINATION:
  • General: Patient is alert and oriented to person, place, and time. Appears stated age and in no acute distress. Well-nourished and well-developed.
  • Cardiovascular: Regular rate and rhythm without murmurs, rubs, or gallops. No jugular venous distension. Peripheral pulses 2+ bilaterally.
  • Respiratory: Clear to auscultation bilaterally in all lung fields. No wheezes, rales, or rhonchi appreciated. Symmetric chest expansion.
  • Abdomen: Soft, non-tender, non-distended. Bowel sounds present in all four quadrants. No hepatosplenomegaly or masses palpated.
  • Extremities: No cyanosis, clubbing, or edema noted in upper or lower extremities. Full range of motion preserved.
  • Neurological: Cranial nerves II-XII grossly intact. Motor strength 5/5 in all extremities. Sensation intact to light touch.

ASSESSMENT AND PLAN:
{cond['plan']}

PATIENT EDUCATION:
Patient demonstrates clear understanding of current diagnosis and treatment plan. Medication regimen reviewed in detail including proper dosing, timing, and potential side effects. Warning signs and symptoms requiring immediate medical attention discussed thoroughly. Patient verbalized understanding and had opportunity to ask questions. Written educational materials provided. Patient instructed to call office or present to emergency department for any concerning symptoms including chest pain, severe shortness of breath, uncontrolled bleeding, or altered mental status.

FOLLOW-UP: 
Scheduled for {random.choice(['2 weeks', '4 weeks', '6 weeks', '3 months'])}. Patient to call sooner if symptoms worsen or new concerns arise. Laboratory results will be reviewed at next visit.

Provider: Dr. Medical Professional, MD
Date: {random.choice(['2024-11-15', '2024-11-20', '2024-11-25', '2024-12-01'])}
Electronic signature on file."""
        
        record = {
            'record_id': f'MRN_{i:06d}',
            'age_range': age_range,
            'primary_condition': cond_name,
            'comorbidities': random.choice(['None', 'Hypertension', 'Hyperlipidemia', 'Diabetes Type 2']),
            'clinical_summary': clinical_note
        }
        records.append(record)
    
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("=" * 70)
    print("🏥 GENERATING COMPLETE PROFESSIONAL MEDICAL RECORDS")
    print("=" * 70)
    
    df = generate_complete_records(200)
    
    os.makedirs('data', exist_ok=True)
    output_file = 'data/synthetic_records.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Generated {len(df)} COMPLETE professional records")
    print(f"✅ Saved to: {output_file}")
    print(f"\n📊 Statistics:")
    print(f"  • Average text length: {df['clinical_summary'].str.len().mean():.0f} characters")
    print(f"  • Shortest record: {df['clinical_summary'].str.len().min()} characters")
    print(f"  • Longest record: {df['clinical_summary'].str.len().max()} characters")
    
    print("\n" + "=" * 70)
    print("📄 SAMPLE COMPLETE RECORD (first 500 chars):")
    print("=" * 70)
    print(df.iloc[0]['clinical_summary'][:500])
    print("...")
    print("=" * 70)
