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
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Chemical Peels, IPL Therapy"},
    "Wrinkles / Aging": {"ingredients": "Retinol, Peptides, Vitamin C", "procedures": "Botox, RF-Lifting"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea, Hyaluronic Acid", "procedures": "Microcurrents, Lymphatic Massage"},
    "Redness": {"ingredients": "Cica, Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy"},
    "Large Pores": {"ingredients": "Retinoids, BHA", "procedures": "Fractional Laser, Peels"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA", "procedures": "Microneedling, Laser Resurfacing"}
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
    
    # PAGE 1: ANALYSIS & ROAST
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Report')).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE VIBE CHECK (ROAST):", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "3. ADDITIONAL FINDINGS:", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.multi_cell(0, 7, txt=clean_text(data.get('hidden_findings', '')))

    # PAGE 2: CLINICAL STRATEGY
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc.get('description'))); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation'))); pdf.ln(2)

    # PAGE 3: DAILY OPERATIONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "6. DETAILED ROUTINE: SEALING PROTOCOL", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(0, 5, txt="IMPORTANT: Apply active serums first, wait 3 mins for absorption, then ALWAYS seal with a moisturizer to prevent active ingredient evaporation.")
    pdf.ln(5)
    for step in data.get('detailed_routine', []):
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(3)

    # PAGE 4: FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(200, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    pdf.ln(10); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data.get('disclaimers', '')), align='C')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> I am saving for a Jaguar E-Type. Your $10 helps the dream.</div>', unsafe_allow_html=True)
    try:
        st.image("scan_face.png", use_column_width=True)
    except:
        st.info("🖼 scan_face.png missing.")
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
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
You are a top-tier clinical dermatologist and a witty 'Bro-Coach'. 
Generate a premium 4-page report in JSON for {u_name}, age {u_age}.

STRICT CONTENT RULES:
1. THE VIBE CHECK: Use the 'Sandwich Roast' (Respect -> Sharp Metaphor -> Support). Avoid cheap insults.
2. CLINICAL ANALYSIS: Min 8 sentences. Deep dive into photo texture, barrier, and vascular patterns. [cite: 4, 16]
3. HOME WEAPONS (ACTIVES): For EVERY active ingredient, you MUST include a specific 'Safety Warning' (e.g., Vitamin C requires SPF to avoid spots, Retinol requires gradual introduction).
4. SEALING PROTOCOL: Every serum must be locked with moisturizer to prevent evaporation. [cite: 165]
5. DISCLAIMERS: You must provide TWO separate disclaimers: one for Medical/Legal and one for Active Ingredient Safety.

STRICT JSON STRUCTURE:
{{
  "header": "Skin Upgrade Protocol for {u_name}",
  "roast": "4-5 sentences.",
  "clinical_analysis": "8+ sentences. Medical tone.",
  "hidden_findings": "2-3 additional issues detected.",
  "clinical_protocol": [
    {{"name": "Procedure", "description": "3 sentences on action and result."}}
  ],
  "home_weapons": [
    {{
      "name": "Ingredient Name", 
      "explanation": "3 sentences on molecular action.",
      "safety_warning": "CRITICAL: Specific instruction on how not to ruin skin with this active (e.g. SPF requirement, patch test)."
    }}
  ],
  "morning_routine": ["Detailed step with technique", "Sealing step with SPF"],
  "evening_routine": ["Detailed step with technique", "Sealing step with barrier cream"],
  "safety_disclaimer": "Detailed notice on actives: start slow, patch test, and the absolute necessity of SPF.",
  "medical_notice": "Legal notice: Informational only, consult a doctor. ",
  "final_joke": "Inspiring cynical joke.",
  "monetization": "Buy our $5 list to help my Jaguar fund. [cite: 44, 47]"
}}
Use logic: {logic['ingredients']} and {logic['procedures']}.
"""
                response = client.chat.completions.create(
                    model="gpt-4o", response_format={ "type": "json_object" },
                    messages=[{"role": "system", "content": mega_prompt},
                              {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}]}]
                )
                
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e: st.error(f"Error: {e}")
