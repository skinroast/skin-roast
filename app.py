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
    
    # PAGE 1: ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, clean_text(data['header']).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE VIBE CHECK (ROAST):", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data['roast']))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data['clinical_analysis']))

    # PAGE 2: CLINICAL STRATEGY
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "3. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data['clinical_protocol']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc['description'])); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data['home_weapons']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon['explanation'])); pdf.ln(2)

    # PAGE 3: DAILY OPERATIONS (РУТИНА)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. DETAILED ROUTINE: THE SEALING PROTOCOL", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(0, 5, txt="Note: Apply active serums first, wait 2-3 mins, then ALWAYS 'seal' with a moisturizer to prevent active evaporation.")
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    pdf.set_font("Helvetica", size=11)
    for step in data['detailed_routine']:
        if "Morning" in step:
            pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data['detailed_routine']:
        if "Evening" in step:
            pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    # PAGE 4: FINAL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data['final_joke']), align='C')

    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(0, 7, txt=clean_text(data['monetization']), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)

    pdf.ln(20); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data['disclaimers']), align='C')

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
You are a dual-role expert: A World-Class Clinical Dermatologist and a sharp, cynical 'Bro-Coach' (vibe: Dr. House meets Ray Donovan).
Generate a premium, high-value 4-page JSON report for {u_name}.

STRICT RULES FOR CONTENT:
1. ROAST: Use the 'Sandwich' method. Acknowledge their hustle, then a sharp cinematic metaphor about their {u_sins}. End with support. No cheap insults.
2. CLINICAL ANALYSIS: Minimum 8 sentences. Deep medical dive into texture, vascular patterns, and epidermal barrier status.
3. DETAILED ROUTINE (THE CORE VALUE): 
   - Every active serum MUST be 'sealed' with a moisturizer. 
   - Explain the 'Occlusion' principle: why a cream is necessary to lock in the serum and prevent Trans-Epidermal Water Loss (TEWL).
   - Use specific techniques: 'wait 3 minutes for the serum to absorb', 'warm the cream in palms', 'press into the skin'.

STRICT JSON STRUCTURE:
{{
  "header": "Skin Upgrade Protocol for {u_name}",
  "roast": "4-5 sentences.",
  "clinical_analysis": "8+ full sentences. Professional clinical tone.",
  "hidden_findings": "2-3 additional issues detected for upsell gap.",
  "clinical_protocol": [
    {{"name": "Procedure", "description": "3 detailed sentences: mechanism, necessity, and result."}}
  ],
  "home_weapons": [
    {{"name": "Ingredient", "explanation": "Molecular action + why it must be sealed with a barrier cream."}}
  ],
  "detailed_routine": [
    "Morning Step 1 (Cleansing): ...",
    "Morning Step 2 (Activation): Apply Serum...",
    "Morning Step 3 (Sealing): Apply Cream/SPF to lock in ingredients and protect armor...",
    "Evening Step 1: ...",
    "Evening Step 2: ...",
    "Evening Step 3: Sealing step..."
  ],
  "disclaimers": "Medical disclaimer.",
  "final_joke": "One final inspiring but sharp 'Bro' joke.",
  "monetization": "Search for free or buy our curated brands list for $5 to fund my Jaguar."
}}
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
