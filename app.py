import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
PATREON_LINK = "https://www.patreon.com/your_link" 

# --- 2. LOGIC MATRIX ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Professional Cleaning, IPL"},
    "Wrinkles / Aging": {"ingredients": "Retinol, Peptides, Vitamin C", "procedures": "Botox, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea, Hyaluronic Acid", "procedures": "Microcurrents"},
    "Redness": {"ingredients": "Cica, Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy"},
    "Large Pores": {"ingredients": "Retinoids, BHA", "procedures": "Fractional Laser"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA", "procedures": "Microneedling, Laser Resurfacing"}
}

# --- 3. ROBUST UTILS ---
def clean_text(text):
    if isinstance(text, str):
        replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-', '\u2026': '...'}
        for char, rep in replacements.items():
            text = text.replace(char, rep)
        return text.encode('ascii', 'ignore').decode('ascii')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: DEEP ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Analysis')), ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE VIBE CHECK (ROAST):", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "3. ADDITIONAL FINDINGS:", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.multi_cell(0, 7, txt=clean_text(data.get('hidden_findings', '')))

    # PAGE 2: PROCEDURES & ACTIVES
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc.get('name', ''))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc.get('description', ''))); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name', ''))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation', ''))); pdf.ln(2)

    # PAGE 3: DETAILED ROUTINE
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "6. DETAILED ROUTINE (TECHNIQUE)", ln=True, align='C')
    for step in data.get('detailed_routine', []):
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(3)

    # PAGE 4: FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(200, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.ln(10); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data.get('disclaimers', '')), align='C')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
if query_params.get("paid") != "true":
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace;">⚠️ Saving for a Jaguar E-Type. Each analysis helps the dream.</div>', unsafe_allow_html=True)
    st.title("YOUR MIRROR LIES. AI DOESN'T.")
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
        with st.spinner("AI is executing deep clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a top-tier clinical dermatologist and a witty 'Bro-Coach' (vibe: Dr. House meets high-end fixer).
                Create a 4-page premium skin report in JSON for {u_name}, age {u_age}.
                
                STRICT JSON STRUCTURE:
                {{
                  "header": "Skin Upgrade Protocol for {u_name}",
                  "roast": "4-5 sentences of 'Sandwich Roast'. Start with respect for their vibe/hustle, then an ironic comparison about their {u_sins} (use metaphors like corporate burnout, tech-founder stress, or survival ops). End with support. No cheap insults.",
                  "clinical_analysis": "Minimum 6 full sentences. High-level medical analysis of photo: identify skin type (oily, dry, aging), barrier function, and vascular patterns. Be professional and detailed.",
                  "hidden_findings": "2-3 additional dermatological issues detected on photo besides {u_enemy}.",
                  "clinical_protocol": [
                    {{"name": "Procedure", "description": "3 detailed sentences on how it works and the clinical result."}},
                    {{"name": "Procedure 2", "description": "3 detailed sentences on how it works and the clinical result."}}
                  ],
                  "home_weapons": [
                    {{"name": "Ingredient 1", "explanation": "3 sentences on molecular action for this user."}},
                    {{"name": "Ingredient 2", "explanation": "3 sentences on molecular action."}},
                    {{"name": "Ingredient 3", "explanation": "3 sentences on molecular action."}}
                  ],
                  "detailed_routine": [
                    "Morning Step 1: Specific cleanser technique (e.g. rub in hands for 10s, massage on wet skin for 60s, rinse with cool water).",
                    "Morning Step 2: ...",
                    "Evening Step 1: ...",
                    "Evening Step 2: ..."
                  ],
                  "disclaimers": "Full medical disclaimer: Informational only. Consult a doctor.",
                  "final_joke": "One final inspiring but cynical 'Bro' joke.",
                  "monetization": "Explain they can hunt for products for free or buy our curated brands list for $5 to fund my Jaguar dream."
                }}
                Recommend these based on logic: {logic['ingredients']} and {logic['procedures']}.
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
