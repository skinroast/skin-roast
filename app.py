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
PATREON_LINK = "https://www.patreon.com/your_link" 

# --- 2. TREATMENT MATRIX ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Professional Deep Cleaning, IPL Therapy, Chemical Peels"},
    "Wrinkles / Aging": {"ingredients": "Retinol (Vitamin A), Peptides, Vitamin C", "procedures": "Botox Injections, RF-Lifting, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid", "procedures": "Microcurrent Therapy, Lymphatic Drainage, Eye Peels"},
    "Redness": {"ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask"},
    "Large Pores": {"ingredients": "Retinoids, BHA (Salicylic Acid), Niacinamide", "procedures": "Fractional Laser, Carbon Peel, Microneedling"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA (Glycolic)", "procedures": "Microneedling (Dermapen), Laser Resurfacing, Medium Peels"}
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
    
    # PAGE 1: ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Report')).upper(), ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))
    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))

    # PAGE 2: PROCEDURES & ACTIVES
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "3. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc.get('description'))); pdf.ln(4)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation')))
        pdf.set_font("Helvetica", 'B', 9); pdf.set_text_color(150, 0, 0)
        pdf.multi_cell(0, 5, txt=f"WARNING: {clean_text(weapon.get('safety_warning'))}")
        pdf.set_text_color(0, 0, 0); pdf.ln(4)

    # PAGE 3: ROUTINE (MIRROR READY)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. THE SEALING PROTOCOL (DAILY OPERATIONS)", ln=True, align='C')
    pdf.set_line_width(0.5); pdf.rect(10, 40, 190, 160) 
    pdf.set_xy(15, 45)
    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    for step in data.get('morning_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}"); pdf.ln(2)
    pdf.ln(5); pdf.set_x(15); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data.get('evening_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 6, txt=f"- {clean_text(step)}"); pdf.ln(2)

    # PAGE 4: FINAL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12); pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
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
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace;">⚠️ HONEST WARNING: Saving for a Jaguar E-Type. Each analysis helps.</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic_form"):
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        u_routine = st.selectbox("Current Operations", ["Water only", "Bar Soap", "Basic", "Full Protocol"])
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
               mega_prompt = f"""
You are a top-tier clinical dermatologist with the sharp, dark wit of a professional roast comedian. 
Generate an ultra-premium, high-volume 4-page JSON report for {u_name}, age {u_age}.
User's current routine: {u_routine}. Their lifestyle sins: {u_sins}. Primary concern: {u_enemy}.

STRICT CONTENT RULES:
1. THE REALITY CHECK (ROAST): Write a massive, 6-8 sentence brutal roast. Don't just mention the sins, paint a cinematic, cynical picture of their skin's future if they continue. Use high-level vocabulary and dark medical humor. It must be a true 'Skin Roast'.
2. CLINICAL ANALYSIS: Minimum 10-12 full sentences. Deep-dive into dermal density, epidermal thickness, and micro-vascular congestion. Use serious medical terminology to justify the high price of this report.
3. CLINICAL PROTOCOL: List EXACTLY 3 high-end procedures from {logic['procedures']}. For EACH, write 4 detailed sentences explaining the technology, the cellular response, and the long-term structural benefits.
4. HOME WEAPONS: List EXACTLY 3 actives from {logic['ingredients']}. For EACH, provide a molecular-level explanation and a bolded safety warning regarding SPF and sensitivity.
5. THE SEALING PROTOCOL (ROUTINE): For every AM and PM step, provide 3-4 sentences. Include the technique, the amount of product, and the exact sensation the user should feel (e.g., 'a slight tingle indicating active penetration'). Ensure the text fills the page.
6. MONETIZATION: Close with a sharp, funny pitch about how their $5 purchase of the 'Shopping List' is the only thing standing between you and a vintage Jaguar E-Type.

STRICT JSON STRUCTURE:
{{
  "header": "ULTIMATE SKIN UPGRADE PROTOCOL: {u_name}",
  "roast": "Long brutal roast here",
  "clinical_analysis": "Very long medical deep-dive here",
  "clinical_protocol": [ {{ "name": "...", "description": "4 sentences" }} ],
  "home_weapons": [ {{ "name": "...", "explanation": "3 sentences", "safety_warning": "..." }} ],
  "morning_routine": ["Step 1 with heavy detail", "Step 2 with heavy detail", "Step 3 Sealing"],
  "evening_routine": ["Step 1 with heavy detail", "Step 2 with heavy detail", "Step 3 Sealing"],
  "safety_disclaimer": "Safety rules...",
  "medical_notice": "Legal notice...",
  "final_joke": "One final dark joke about looking better than your lifestyle suggests.",
  "monetization": "Jaguar pitch..."
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
