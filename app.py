import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os
import base64
import re

# --- 1. SETUP & SECRETS ---
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# LINKS
LEMON_SQUEEZY_LINK = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_LINK = "https://skin-roast.lemonsqueezy.com/buy"

st.set_page_config(page_title="Skin Roast: Upgrade Plan", page_icon="🔥", layout="centered")

# CSS STYLE
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 3.5em;
        background-color: #D32F2F; 
        color: white;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .success-box {
        padding: 20px;
        background-color: #1E1E1E;
        border: 1px solid #00FF00;
        color: #00FF00;
        text-align: center;
        font-family: monospace;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. AI BRAIN (CULTURAL CODE & CREATIVITY FIXED) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO".
GOAL: Create a COMPREHENSIVE, HIGH-VALUE protocol.

INSTRUCTIONS:
1. ROAST (THE CULTURAL MIX): 
   - Compliment their masculine vibe (e.g., "You have that main character energy...").
   - IMPROVISE a metaphor using POP CULTURE or HIGH STATUS exaggeration.
     - USE MOVIES/TV: "Die Hard" (John McClane in the vents), "Yellowstone" (Dutton protecting the ranch), "Fight Club" (Project Mayhem), "Wolf of Wall Street", "Peaky Blinders".
     - USE SPORTS: MMA Fighter after 5 rounds, F1 Driver, Marathon runner.
     - EXAGGERATE STATUS: Roast them like they are a tired BILLIONAIRE. 
       - "You look like you ate too much black caviar and haven't slept because you were counting your gold bars."
       - "You look like a rockstar coming off a 6-month world tour."
   - End with Support ("Let's fix the chassis").
   - IMPORTANT: DO NOT COPY THIS INSTRUCTION. WRITE A NEW UNIQUE PARAGRAPH.

2. DEEP SCAN: Analyze the SELECTED problem in detail based on visuals.
3. CLINICAL PROCEDURES: Recommend 2-3 professional treatments.
4. ROUTINE: Detailed steps. Mention SPF!

RESPONSE FORMAT (JSON ONLY):
{
  "roast_intro": "WRITE THE ACTUAL ROAST TEXT HERE. Do not describe it. Be creative and funny.",
  "deep_dive_analysis": "Detailed visual analysis (5-6 sentences).",
  "other_issues_teaser": "List 2-3 other detected issues.",
  "ingredients": [
      {"name": "Active Ingredient", "why": "Scientific explanation"}
  ],
  "clinical_treatments": [
      {"name": "Procedure Name", "why": "What it does"}
  ],
  "routine_morning": "Detailed AM steps.",
  "routine_evening": "Detailed PM steps."
}
"""

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_skin_with_vision(image_file, age, skin_type, problem, habits):
    if not openai.api_key:
        return None
    
    base64_image = encode_image(image_file)
    habits_str = ", ".join(habits) if habits else "None"
    user_text = f"User Data: Age {age}, Skin Type {skin_type}. FOCUS PROBLEM: {problem}. Habits: {habits_str}."

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": [
                    {"type": "text", "text": user_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        if not content:
            st.error("AI Safety Filter blocked this image. Please use a regular selfie.")
            return None
            
        return json.loads(content)

    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

def clean_text(text):
    if isinstance(text, str):
        return text.encode('latin-1', 'replace').decode('latin-1')
    return str(text)

def create_pdf(data, problem_name):
    """Generate PDF"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1 ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.ln(5)
    
    # ROAST (CULTURAL MIX)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['roast_intro']))
    pdf.ln(5)

    # DEEP SCAN
    pdf.set_font("Helvetica", 'B', 14)
    clean_problem = clean_text(problem_name).upper()
    pdf.cell(0, 10, f"DEEP SCAN: {clean_problem}", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['deep_dive_analysis']))
    pdf.ln(10)
    
    # TEASER
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "ALSO DETECTED (NOT INCLUDED):", ln=True)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['other_issues_teaser']))
    pdf.set_text_color(0, 0, 0)
    
    # --- PAGE 2 ---
    pdf.add_page()
