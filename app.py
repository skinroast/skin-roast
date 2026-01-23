import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. BRANDING & GOALS ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥")

# Your "Lazy Millionaire" dashboard [cite: 47, 51]
GOAL = 6150000 
CURRENT = 260 

# --- 2. AUTHENTICATION ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

# Monetization Links [cite: 146, 148]
PAYMENT_URL = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# --- 3. THE PDF ENGINE ---
def create_pdf_report(data, name):
    pdf = FPDF()
    pdf.add_page()
    
    # Page 1: THE VERDICT [cite: 231, 232]
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{name.upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=str(data.get('roast_intro', 'Analysis failed.')))
    
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {data.get('problem', 'SKIN')}", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=str(data.get('deep_analysis', 'Data missing.')))
    
    # Page 2: CLINICAL & HOME WEAPONS [cite: 243, 251]
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt="[*] Botox/Fillers: Relaxes muscles.\n[*] Biorevitalization: Deep hydration.")
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "YOUR HOME WEAPONS", ln=True)
    pdf.multi_cell(0, 7, txt="[+] Retinol: Collagen boost.\n[+] Peptides: Firmness.\n[+] Vitamin C: Brightening.")

    # Page 3: OPERATIONS & THE CLOSER [cite: 258, 263]
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt="AM: Cleanse -> Vit C -> Moisturize -> SPF 30+.\nPM: Cleanse -> Retinol -> Hydrate.")

    # THE CLOSER: THE JOKE YOU ASKED FOR
    pdf.ln(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "A FINAL WORD FROM DR. ROAST:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    # Tough love closer
    closing_joke = (
        f"Look, {name}, right now your face looks like a topographic map of a bad decision. "
        "But even a crashed Ferrari can be rebuilt if you stop washing it with dish soap. "
        "You've got the plan. Now stop being a victim of your own neglect and fix it. "
        "I'm rooting for you—mostly so you look good enough to eventually buy me that house. "
        "Get to work. You've got this."
    )
    pdf.multi_cell(0, 7, txt=closing_joke)

    # Monetization Footer [cite: 278, 280]
    pdf.ln(10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 4. THE APP FLOW ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"${CURRENT} raised of ${GOAL:,}")

if st.query_params.get("paid") == "true":
    with st.form("roast_logic"):
        u_name = st.text_input("Name")
        u_enemy = st.selectbox("Focus", ["Acne", "Wrinkles", "Tired Eyes"])
        u_sins = st.multiselect("Sins", ["Smoking", "Sugar", "No Sleep"]) # Fixed Multiselect scope
        u_file = st.file_uploader("Upload Evidence", type=['jpg', 'png'])
        submit = st.form_submit_button("ROAST ME")

    if submit and u_file:
        with st.spinner("Analyzing the wreckage..."):
            # Mock AI result for testing (Replace with your GPT call)
            result = {
                "roast_intro": "You look like a tech CEO 10 minutes before an SEC raid.",
                "deep_analysis": "Severe dehydration and UV damage detected.",
                "problem": u_enemy
            }
            pdf_path = create_pdf_report(result, u_name)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ DOWNLOAD DOSSIER", f, "My_Skin_Roast.pdf")
else:
    st.link_button("UNLOCK THE TRUTH ($10)", PAYMENT_URL)
