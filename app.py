import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# Настройка API клиента
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
PATREON_LINK = "https://www.patreon.com/your_link" # ЗАМЕНИ НА СВОЮ

# --- 2. MEDICAL LOGIC MATRIX ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Chemical Peels, IPL Therapy"},
    "Wrinkles / Aging": {"ingredients": "Retinol, Peptides, Vitamin C", "procedures": "Botox, RF-Lifting"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea, Hyaluronic Acid", "procedures": "Microcurrents"},
    "Redness": {"ingredients": "Cica, Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy"},
    "Large Pores": {"ingredients": "Retinoids, BHA", "procedures": "Fractional Laser"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA", "procedures": "Microneedling, Laser Resurfacing"}
}

# --- 3. UTILS & PDF GENERATOR ---

def clean_text(text):
    """Ультимативная очистка для FPDF: только ASCII символы"""
    if isinstance(text, str):
        # Замена типичных юникод-символов на ASCII аналоги
        replacements = {
            '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '-', '\u2026': '...', '’': "'", '‘': "'",
            '“': '"', '”': '"', '—': '-'
        }
        for char, rep in replacements.items():
            text = text.replace(char, rep)
        # Удаляем всё остальное, что не входит в ASCII (включая кириллицу и эмодзи)
        return text.encode('ascii', 'ignore').decode('ascii')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Analysis')), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE ROAST:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "3. ADDITIONAL FINDINGS:", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.multi_cell(0, 7, txt=clean_text(data.get('hidden_findings', '')))

    # PAGE 2: CLINICAL & HOME WEAPONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. CLINICAL PROTOCOL", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc['description'])); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. YOUR HOME WEAPONS", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon['explanation'])); pdf.ln(2)

    # PAGE 3: ROUTINE
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "6. DETAILED ROUTINE", ln=True, align='C')
    for step in data.get('detailed_routine', []):
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    # PAGE 4: FINAL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(200, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.ln(10); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data.get('disclaimers', '')), align='C')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI / LOGIC ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    # LANDING PAGE
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> Saving for a Jaguar E-Type. Every $10 analysis gets me 0.000001% closer to the dream.</div>', unsafe_allow_html=True)
    try:
        st.image("scan_face.png", use_column_width=True)
    except:
        st.info("🖼 scan_face.png missing.")
    
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #aaa; font-size: 1.2rem;">Get a brutally honest analysis and a tailored routine to fix your face.</p>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)

else:
    # APP AFTER PAYMENT
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "No Sleep", "Sugar", "No SPF", "Stress"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a top-tier clinical dermatologist and roast comedian. 
                Create a 4-page premium report in JSON for {u_name}, age {u_age}.
                1. header: "Skin Condition Analysis for {u_name}"
                2. roast: 4-5 cynical sentences about lifestyle choices ({u_sins}).
                3. clinical_analysis: Minimum 6 sentences. Deep medical analysis of photo: texture, barrier, type. No jokes.
                4. hidden_findings: 2-3 other issues detected on photo besides {u_enemy}.
                5. clinical_protocol: 2 procedures from {logic['procedures']} with detailed descriptions.
                6. home_weapons: 3 actives from {logic['ingredients']} with molecular explanations.
                7. detailed_routine: Step list with technique (e.g. massage 1 min, apply on damp skin).
                8. disclaimers: Full medical disclaimer.
                9. final_joke: Inspiring but sharp closing joke.
                10. monetization: Explain they can search for free or buy our curated list for $5 to fund my Jaguar dream.
                STRICT JSON FORMAT. No other text.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": mega_prompt},
                        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}]}
                    ]
                )
                
                # Парсинг ответа
                report_data = json.loads(response.choices[0].message.content)
                
                st.success("Analysis Complete.")
                pdf_path = create_premium_pdf(report_data)
                
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
                    
            except Exception as e:
                st.error(f"Error: {e}")
