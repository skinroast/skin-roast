import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
PATREON_LINK = "https://www.patreon.com/your_link_here" 

# --- 2. МЕДИЦИНСКАЯ МАТРИЦА ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Professional Deep Cleaning, IPL Therapy, Chemical Peels"},
    "Wrinkles / Aging": {"ingredients": "Retinol, Peptides, Vitamin C", "procedures": "Botox, RF-Lifting, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea, Hyaluronic Acid", "procedures": "Microcurrents, Lymphatic Drainage"},
    "Redness": {"ingredients": "Cica, Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask"},
    "Large Pores": {"ingredients": "Retinoids, BHA, Niacinamide", "procedures": "Fractional Laser, Carbon Peel"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA", "procedures": "Microneedling, Laser Resurfacing, Medium Peels"}
}

# --- 3. UTILS ---
def clean_text(text):
    if isinstance(text, str):
        replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-'}
        for char, rep in replacements.items():
            text = text.replace(char, rep)
        return text.encode('ascii', 'ignore').decode('ascii')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: ANALYSIS & REALITY CHECK
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    # Используем .get() для безопасного извлечения заголовка
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Report')).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    # PAGE 2: PROCEDURES & ACTIVES
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "3. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    # Проходим циклом по процедурам
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, f"[*] {clean_text(proc.get('name', ''))}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, txt=clean_text(proc.get('description', '')))
        pdf.ln(4)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "4. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name', ''))}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation', '')))
        
        # Блок предупреждений о безопасности
        pdf.set_font("Helvetica", 'B', 9)
        pdf.set_text_color(170, 0, 0)
        pdf.multi_cell(0, 5, txt=f"WARNING: {clean_text(weapon.get('safety_warning', ''))}")
        pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    # PAGE 3: ROUTINE (BATHROOM MIRROR VERSION)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "5. THE SEALING PROTOCOL (DAILY OPERATIONS)", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 9)
    pdf.cell(0, 10, "Cut along the line and tape this to your bathroom mirror.", ln=True, align='C')
    
    # Сплошная рамка для удобства вырезания
    pdf.set_line_width(0.5)
    pdf.rect(10, 40, 190, 160) 
    pdf.set_xy(15, 45)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    for step in data.get('morning_routine', []):
        pdf.set_x(15)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}")
        pdf.ln(3)

    pdf.ln(5)
    pdf.set_x(15)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data.get('evening_routine', []):
        pdf.set_x(15)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}")
        pdf.ln(3)

    # PAGE 4: FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12)
    pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    
    pdf.ln(10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(0, 10, "SAFETY DISCLAIMER:", ln=True)
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 4, txt=clean_text(data.get('safety_disclaimer', '')))
    
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(0, 10, "MEDICAL NOTICE:", ln=True)
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 4, txt=clean_text(data.get('medical_notice', '')))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name
