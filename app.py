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
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid", "procedures": "Microcurrent Therapy, Lymphatic Drainage"},
    "Redness": {"ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask"},
    "Large Pores": {"ingredients": "Retinoids, BHA (Salicylic Acid), Niacinamide", "procedures": "Fractional Laser, Carbon Peel"},
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
    pdf.cell(0, 15, clean_text(data['header']).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
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
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon['explanation']))
        pdf.set_font("Helvetica", 'B', 9); pdf.set_text_color(150, 0, 0)
        pdf.multi_cell(0, 5, txt=f"WARNING: {clean_text(weapon['safety_warning'])}")
        pdf.set_text_color(0, 0, 0); pdf.ln(2)

    # PAGE 3: DAILY OPERATIONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. DAILY OPERATIONS: SEALING PROTOCOL", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    for step in data['morning_routine']:
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data['evening_routine']:
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    # PAGE 4: FINAL WORD & DISCLAIMERS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data['final_joke']), align='C')

    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(0, 7, txt=clean_text(data['monetization']), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)

    pdf.ln(10); pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(0, 10, "SAFETY DISCLAIMER:", ln=True)
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 4, txt=clean_text(data['safety_disclaimer']))
    
    pdf.ln(5); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "MEDICAL NOTICE:", ln=True)
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 4, txt=clean_text(data['medical_notice']))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> Saving for a Jaguar E-Type. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
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
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing clinical scan..."):
            try:
                base_4_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a world-class clinical dermatologist and a witty 'Bro-Coach'. 
                Generate a 4-page premium report in JSON for {u_name}, age {u_age}.
                
                STRICT JSON STRUCTURE:
                {{
                  "header": "Skin Upgrade Protocol for {u_name}",
                  "roast": "4-5 sentences of 'Sandwich Roast'. Respect -> sharp metaphor about {u_sins} -> support. No cheap insults.",
                  "clinical_analysis": "Minimum 8 sentences. Deep photo analysis: texture, barrier, type. Serious tone.",
                  "hidden_findings": "2-3 additional issues found besides {u_enemy}.",
                  "clinical_protocol": [
                    {{"name": "Procedure", "description": "3 sentences on action and result."}}
                  ],
                  "home_weapons": [
                    {{
                      "name": "Active Ingredient", 
                      "explanation": "3 sentences on molecular action.",
                      "safety_warning": "CRITICAL: SPF requirement or patch test instruction."
                    }}
                  ],
                  "morning_routine": ["Step 1 with technique", "Step 2 with technique", "Step 3 (Sealing)"],
                  "evening_routine": ["Step 1 with technique", "Step 2 with technique", "Step 3 (Sealing)"],
                  "safety_disclaimer": "Detailed notice on actives: start slow, patch test, and necessity of SPF.",
                  "medical_notice": "Legal notice: Informational only, consult a doctor.",
                  "final_joke": "Inspiring cynical joke about success.",
                  "monetization": "Buy our list for $5 to fund my Jaguar."
                }}
                Use logic: {logic['ingredients']} and {logic['procedures']}.
                """

                response = client.chat.completions.create(
                    model="gpt-4o", response_format={ "type": "json_object" },
                    messages=[{"role": "system", "content": mega_prompt},
                              {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}}]}]
                )
                
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e: st.error(f"Error: {e}")
