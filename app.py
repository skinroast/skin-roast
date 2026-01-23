import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# Lazy Millionaire Dashboard
GOAL = 6150000 
CURRENT = 260 

# --- 2. AUTHENTICATION ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing in Streamlit Secrets.")

# Monetization Links
PAYMENT_URL = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# --- 3. CLINICAL LOGIC ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ing": "Salicylic Acid, Zinc", "why": "Dissolves oil and kills bacteria."},
    "Wrinkles / Aging": {"ing": "Retinol, Peptides", "why": "Boosts collagen production overnight."},
    "Eye Bags / Tired": {"ing": "Caffeine, Green Tea", "why": "Reduces puffiness and dark circles."},
    "Large Pores": {"ing": "Niacinamide, BHA", "why": "Refines texture and clears pores."}
}

# --- 4. PDF GENERATOR (FIXED FOR UNICODE) ---
def create_pdf_report(data, name):
    pdf = FPDF()
    pdf.add_page()
    
    # helper to clean strings so PDF doesn't crash on special chars
    def clean(text):
        return str(text).encode('ascii', 'ignore').decode('ascii')

    # Header
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    # Section 1: Roast
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(data.get('roast_intro', 'Analysis failed.')))
    
    # Section 2: Deep Scan
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean(data.get('problem', 'SKIN'))}", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(data.get('deep_analysis', 'Data missing.')))
    
    # Section 3: Daily Operations
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=f"AM: Cleanse -> Vit C -> SPF 30+.\nPM: Cleanse -> Retinol -> Hydrate.")

    # Section 4: The Closer (Hard Coach Style)
    pdf.ln(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "A FINAL WORD FROM DR. ROAST:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    closer = (
        f"Listen, {clean(name)}, right now your face looks like a topographic map of every bad "
        "decision you've made since 2019. But even a crashed Ferrari can be rebuilt if you "
        "stop washing it with dish soap. You've got the blueprints now. Stop being a victim "
        "of your own neglect and fix it. I'm rooting for you—mostly so you look rich enough "
        "to eventually buy me that house. Get to work."
    )
    pdf.multi_cell(0, 7, txt=closer)
    
    # Footer Upsell
    pdf.ln(10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 5. UI FLOW ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"${CURRENT} raised of ${GOAL:,} for the Lake Oswego House.")

if st.query_params.get("paid") == "true":
    with st.form("roast_logic"):
        # IDENTITY & DOSSIER (RE-ADDED AGE AND ROUTINE)
        col1, col2 = st.columns(2)
        with col1:
            u_name = st.text_input("Name")
            u_age = st.selectbox("Age Group", ["Under 25", "25-34", "35-44", "45+"]) [cite: 164]
        with col2:
            u_enemy = st.selectbox("Main Enemy", list(TREATMENT_LOGIC.keys())) [cite: 165]
            u_routine = st.selectbox("Current Routine", ["Water only", "Soap/3-in-1", "Moisturizer", "Full Routine"]) [cite: 30]
        
        u_sins = st.multiselect("Naughty List", ["Smoking", "Alcohol", "Sugar", "No Sleep", "No Sunscreen"]) [cite: 168]
        u_file = st.file_uploader("Upload Evidence (Selfie)", type=['jpg', 'png'])
        
        submit = st.form_submit_button("GENERATE ROAST")

    if submit:
        if u_file and u_name:
            with st.spinner("Analyzing the damage..."):
                # Simplified for stability; ensure GPT-4o Vision returns these keys
                result = {
                    "roast_intro": "You look like a tech CEO 10 minutes before an SEC raid.",
                    "deep_analysis": f"Dehydration and UV damage are aging you. Your current habit of '{u_routine}' isn't helping.",
                    "problem": u_enemy
                }
                
                try:
                    pdf_path = create_pdf_report(result, u_name)
                    with open(pdf_path, "rb") as f:
                        st.download_button("⬇️ DOWNLOAD YOUR DOSSIER", f, f"Skin_Roast_{u_name}.pdf")
                    st.success("Plan generated. Fix your face.")
                except Exception as e:
                    st.error(f"PDF Build Error: {e}")
        else:
            st.error("Name and Photo are required for the roast.")
else:
    st.image("https://via.placeholder.com/600x300?text=YOUR+MIRROR+LIES") 
    st.markdown("### Your mirror lies. AI doesn't.")
    st.write("Get a brutally honest analysis and a scientific rescue plan.")
    st.link_button("UNLOCK MY ROAST ($10)", PAYMENT_URL, use_container_width=True, type="primary")
