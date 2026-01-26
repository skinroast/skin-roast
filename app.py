import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
PATREON_LINK = "https://www.patreon.com/your_link_here" 

# --- 2. MEDICAL LOGIC MATRIX ---
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

with st.form("roast_logic"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        # ВОЗВРАЩАЕМ ПУНКТ ПРО ТЕКУЩУЮ РУТИНУ
        u_routine = st.selectbox("Current Operations", ["Water only", "Bar Soap", "Basic Moisturizer", "Full Protocol"])
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")
# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> Saving for a Jaguar E-Type. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
    try: st.image("scan_face.png", use_column_width=True)
    except: st.info("🖼 scan_face.png missing.")
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        # ВОЗВРАЩАЕМ ПУНКТ ПРО ТЕКУЩУЮ РУТИНУ
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
                You are a world-class clinical dermatologist and a witty 'Bro-Coach'. 
                Generate a premium 4-page report in JSON for {u_name}, age {u_age}.
                
                STRICT CONTENT RULES:
                - CLINICAL PROTOCOL: List EXACTLY 3 procedures from the list: {logic['procedures']}. Each must have 3 detailed sentences.
                - HOME WEAPONS: List EXACTLY 3 active ingredients from: {logic['ingredients']}. Each must have 3 sentences on molecular action AND a specific 'Safety Warning' regarding SPF/irritation.
                - ROUTINE: Describe Morning and Evening routines separately and IN DETAIL. 
                  Example step: "Cleanse: Warm water, emulsify 2 pumps of cleanser in palms, massage for 60s, focus on nose, rinse 10 times."
                - MONETIZATION: Explain that they can hunt for products for free OR buy our brands list for $5 to help fund my Jaguar E-Type dream.

                STRICT JSON STRUCTURE:
                {{
                  "header": "Skin Upgrade Protocol for {u_name}",
                  "roast": "4-5 sentences of 'Sandwich Roast' (Respect -> sharp cinematic metaphor about {u_sins} -> support).",
                  "clinical_analysis": "Minimum 8 sentences. Deep photo analysis of texture, barrier, and vascular patterns.",
                  "clinical_protocol": [ {{"name": "Procedure", "description": "3 sentences"}}, {{"name": "...", "description": "..."}}, {{"name": "...", "description": "..."}} ],
                  "home_weapons": [ {{"name": "Active", "explanation": "3 sentences", "safety_warning": "Warning"}}, {{"name": "...", "explanation": "...", "safety_warning": "..."}}, {{"name": "...", "explanation": "...", "safety_warning": "..."}} ],
                  "morning_routine": ["Detailed Step 1", "Detailed Step 2", "Detailed Step 3"],
                  "evening_routine": ["Detailed Step 1", "Detailed Step 2", "Detailed Step 3"],
                  "safety_disclaimer": "Detailed notice on actives.",
                  "medical_notice": "Full legal notice.",
                  "final_joke": "Inspiring cynical joke about success.",
                  "monetization": "Jaguar fund message."
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
