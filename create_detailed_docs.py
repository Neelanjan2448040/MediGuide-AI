from fpdf import FPDF
import os

def create_medical_pdf(filename, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 10, text=title, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, text=content)
    pdf.output(filename)

os.makedirs("data/documents", exist_ok=True)

# Detailed Dengue PDF
dengue_detail = """
DENGUE FEVER: COMPLETE CLINICAL OVERVIEW

Pathology: Dengue virus (DENV) transmitted by Aedes aegypti mosquitoes.

Phases of Infection:
1. Febrile Phase: High fever, headache, retro-orbital pain.
2. Critical Phase: Around day 3-7. Risk of plasma leakage and hemorrhaging.
3. Recovery Phase: Fluid reabsorption.

Dietary Advice:
- WHAT TO EAT: Papaya leaf extract, Pomegranate, Coconut water, Ginger, and Turmeric.
- WHAT TO AVOID: Spicy foods, Caffeinated drinks, Alcohol, and Oily foods.

Medical Warnings:
Avoid Aspirin and NSAIDs (Ibuprofen) as they increase bleeding risk. Use Paracetamol only.
"""

# Detailed Cardiovascular Health
heart_detail = """
HYPERTENSION AND CARDIOVASCULAR WELLNESS

Definition: Chronic high blood pressure (140/90 mmHg or higher).

Symptoms: Often 'silent', but can include dizziness, blurred vision, and chest discomfort.

Diet (DASH Diet):
- EAT: Whole grains, fruits, vegetables, low-fat dairy.
- AVOID: Excessive Salt (Sodium), Saturated fats, and Processed meats.

Emergency Signs:
Severe chest pain radiating to the left arm, difficulty breathing, or sudden numbness are signs of a HEART ATTACK or STROKE. Seek immediate medical ER assistance.
"""

create_medical_pdf("data/documents/dengue_premium_guide.pdf", "Dengue Fever Clinical Guide", dengue_detail)
create_medical_pdf("data/documents/cardio_health_and_emergency.pdf", "Cardiovascular Wellness & Emergencies", heart_detail)

print("Detailed medical docs created.")
    
