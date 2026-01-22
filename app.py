import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os

# --- 1. SETUP & SECRETS ---
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# LINKS
LEMON_SQUEEZY_LINK = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_LINK = "https://skin-roast.lemonsqueezy.com/buy"

st.set_page_config(page_title="Skin Roast: Upgrade Plan", page_icon="🔥", layout="centered")

# CSS HACK (DARK MODE & STYLING)
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

# --- 2. AI BRAIN (STRICT MODE) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO". A ruthless but helpful mentor.
Your goal: Make the user rich and handsome.
TONE: Stoic, aggressive, high-value male, Wall Street style.

TASK: Analyze the user's skin data and generate a DETAILED report.
IMPORTANT: DO NOT USE EMOJIS IN ANY PART OF THE JSON RESPONSE.

RESPONSE FORMAT (JSON ONLY):
{
  "roast": "A harsh roast of their current look (3-4 sentences). Compare them to a tired intern.",
  "science_why": "Scientific explanation of why their skin is failing (2-3 sentences, use terms like 'Cortisol', 'Sebum', 'Oxidation').",
  "problems_list": ["Problem 1", "Problem 2", "Problem 3"],
  "ingredients": [
      {"name": "Ingredient Name", "why": "Detailed reason why it works"}
  ],
  "diet_roast": "Roast their diet habits (sugar/alcohol) and tell them what to eat instead.",
  "lifestyle_fix": "Strict advice on sleep and stress. Mention that 'Sleep is ROI'.",
  "routine_morning": "Step-by-step morning routine (detailed).",
  "routine_evening": "Step-by-step evening routine (detailed).",
  "motivation": "Final closing statement about Discipline and Success."
}
"""

def analyze_skin(age, skin_type, problem, habits):
    if not openai.api_key:
        return None  
    user_prompt = f"Data: Age {age}, Skin {skin_type}, Problem {problem}, Sins {habits}."
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except:
        return None

def create_pdf(data):
    """Generate RICH PDF (NO EMOJIS ALLOWED)"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Helper to clean text
    def clean(text):
        if isinstance(text, str):
            return text.encode('latin-1', 'replace').decode('latin-1')
        return str(text)

    # TITLE
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "PROTOCOL: UPGRADE", ln=True, align='C')
    pdf.ln(5)
    
    # 1. THE ROAST
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "STATUS REPORT:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean(data['roast']))
    pdf.ln(5)

    # 2. THE SCIENCE
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE BIOLOGICAL FAILURE:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean(data['science_why']))
    pdf.ln(5)
    
    # 3. IDENTIFIED ISSUES
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "CRITICAL ERRORS:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    for prob in data['problems_list']:
        pdf.cell(0, 6, txt=f"[X] {clean(prob)}", ln=True)

    pdf.ln(10)
    
    # 4. DIET & LIFESTYLE
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "INTERNAL SYSTEMS", ln=True, align='L')
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Line
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "FUEL INTAKE:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0
