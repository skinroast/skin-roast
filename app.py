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
    pdf.rect(10, 40, 190, 160) 
    pdf.set_xy(15, 45)
    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    for step in data.get('morning_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}"); pdf.ln(3)

    pdf.ln(5); pdf.set_x(15)
    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data.get('evening_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}"); pdf.ln(3)

    # PAGE 4: FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    pdf.ln(10); pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "SAFETY DISCLAIMER:", ln=True)
    pdf.set_font("Helvetica", size=8); pdf.multi_cell(0, 4, txt=clean_text(data.get('safety_disclaimer', '')))
    pdf.ln(5); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "MEDICAL NOTICE:", ln=True)
    pdf.set_font("Helvetica", size=8); pdf.multi_cell(0, 4, txt=clean_text(data.get('medical_notice', '')))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> I am saving for a Jaguar E-Type. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
    try:
        st.image("scan_face.png", use_column_width=True)
    except:
        st.info("🖼 scan_face.png missing.")
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic_form"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        u_routine = st.selectbox("Current Operations", ["Water only", "Bar Soap", "Basic Moisturizer", "Full Protocol"])
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a cynical, world-class clinical dermatologist with a dark sense of humor. 
                Generate a premium 4-page report in JSON for {u_name}, age {u_age}.
                Current routine: {u_routine}. Focus on {u_enemy}.
                
                STRICT CONTENT RULES:
                1. THE REALITY CHECK: 4-5 sentences of sharp, cynical 'Bro Roast' about {u_sins}. Dark medical humor only.
                2. CLINICAL ANALYSIS: Minimum 10 sentences. Deep medical dive into texture, barrier, and vascular patterns.
                3. CLINICAL PROTOCOL: EXACTLY 3 procedures from: {logic['procedures']}. Each must have 3 detailed sentences.
                4. HOME WEAPONS: EXACTLY 3 actives from: {logic['ingredients']}. Each must have 3 sentences + a RED safety warning.
                5. DETAILED ROUTINE: For EVERY step, describe the EXACT technique (e.g. "Massage for 60s", "Warm 2 drops and press into skin").
                6. MONETIZATION: Closing pitch about buying a brands list for $5 to help fund the author's Jaguar E-Type dream.

                STRICT JSON STRUCTURE:
                {{
                  "header": "Skin Upgrade Protocol for {u_name}",
                  "roast": "Dark Roast here",
                  "clinical_analysis": "Long medical analysis here",
                  "clinical_protocol": [ {{"name": "Procedure", "description": "3 detailed sentences"}} ],
                  "home_weapons": [ {{"name": "Active", "explanation": "3 sentences", "safety_warning": "Warning"}} ],
                  "morning_routine": ["Step 1 with technique", "Step 2 with technique", "Step 3 Sealing technique"],
                  "evening_routine": ["Step 1 technique", "Step 2 technique", "Step 3 Sealing technique"],
                  "safety_disclaimer": "Safety notice rules.",
                  "medical_notice": "Legal notice.",
                  "final_joke": "Dark medical joke.",
                  "monetization": "Jaguar message."
                }}
                """

                response = client.chat.completions.create(
                    model="gpt-4o", response_format={{ "type": "json_object" }},
                    messages=[{{"role": "system", "content": mega_prompt}},
                              {{"role": "user", "content": [{{"type": "image_url", "image_url": {{"url": f"data:image/jpeg;base64,{{base64_img}}"}}}}]}}]
                )
                
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{{u_name}}.pdf")
            except Exception as e: st.error(f"Error: {{e}}")
