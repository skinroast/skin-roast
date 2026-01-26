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
    "Wrinkles / Aging": {"ingredients": "Retinol (Vitamin A), Peptides, Vitamin C", "procedures": "Botox Injections, RF-Lifting, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid", "procedures": "Microcurrent Therapy, Lymphatic Drainage, Eye Peels"},
    "Redness": {"ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask, Laser for capillaries"},
    "Large Pores": {"ingredients": "Retinoids, BHA (Salicylic Acid), Niacinamide", "procedures": "Fractional Laser, Carbon Peel, Microneedling"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA (Glycolic)", "procedures": "Microneedling (Dermapen), Laser Resurfacing, Medium Peels"}
}

# --- 3. ГЕНЕРАТОР PDF ---
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
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Report')).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    # PAGE 2: CLINICAL STRATEGY
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "3. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc.get('description'))); pdf.ln(4)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation')))
        pdf.set_font("Helvetica", 'B', 9); pdf.set_text_color(170, 0, 0)
        pdf.multi_cell(0, 5, txt=f"WARNING: {clean_text(weapon.get('safety_warning'))}")
        pdf.set_text_color(0, 0, 0); pdf.ln(4)

    # PAGE 3: DAILY OPERATIONS (WITH BORDER)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. THE SEALING PROTOCOL (DAILY OPERATIONS)", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 9); pdf.cell(0, 10, "Cut along the line and tape this to your bathroom mirror.", ln=True, align='C')
    
    pdf.set_line_width(0.5)
    pdf.rect(10, 40, 1
