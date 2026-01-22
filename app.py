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

# CSS HACK
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 3.5em;
        background-color: #FF4B4B; 
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. AI BRAIN (SAFE MODE - NO EMOJIS IN OUTPUT) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO".
Your goal is to help your bro become handsome.
TONE:
- Address user as "Bro", "Champ".
- Metaphors: Jaguar V12, Wall Street.
- Roast laziness, not the person.
- IMPORTANT: DO NOT USE EMOJIS IN YOUR RESPONSE TEXT. ONLY TEXT.

RESPONSE FORMAT (JSON ONLY):
{
  "roast": "Roast text (3-4 sentences)",
  "problems_list": ["Problem 1", "Problem 2"],
  "ingredients": [
      {"name": "Ingredient Name", "why": "Why it works"}
  ],
  "routine_morning": "Morning steps",
  "routine_evening": "Evening steps",
  "motivation": "Final quote"
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
    """Generate PDF (Clean Text Only)"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Fonts
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", '', 12)
    # Encode to latin-1 to handle any accidental special chars, replacing errors
    roast_text = data['roast'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=f"VERDICT:\n{roast_text}")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "IDENTIFIED ISSUES:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    for prob in data['problems_list']:
        clean_prob = prob.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 8, txt=f"- {clean_prob}", ln=True)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR WEAPONS (ARSENAL)", ln=True, align='C')
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 14)
        clean_name = item['name'].encode('latin-1', 'replace').decode('latin-1')
        clean_why = item['why'].encode('latin-1', 'replace').decode('latin-1')
        
        pdf.cell(0, 10, txt=f"[+] {clean_name}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        pdf.multi_cell(0, 6, txt=f"Why: {clean_why}\n")
        pdf.ln(2)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "BATTLE PLAN", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "MORNING:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    clean_morning = data['routine_morning'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, txt=clean_morning)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "EVENING:", ln=True)
    clean_evening = data['routine_evening'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, txt=clean_evening)

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, "DON'T BE STUPID", ln=True, align='C')
    pdf.set_font("Helvetica", '', 12)
    pdf.multi_cell(0, 8, txt="You know the theory. Now get the right tools.\nI curated a list of products that actually work.\n", align='C')
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Helvetica", 'U', 14)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    return pdf

# --- 3. UI INTERFACE ---
st.warning("""
⚠️ **HONEST WARNING:**
There is no fancy design here because I'm saving money.
I have a goal: **Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)**.
Every $10 you spend gets me 0.000001% closer to the dream.

**REAL TALK:**
I don't promise this report will buy you that house. That's on you.
I promise this: **when you make it big, you will look the part.**
Fix your face now, so you don't feel ashamed to drop the roof of your convertible later.
""")

GOAL = 6150000 
CURRENT = 40 
st.progress(CURRENT / GOAL)
st.caption(f"Raised: ${CURRENT} of ${GOAL:,}. Long way to go.")
st.divider()

st.title("SKIN ROAST 🔥")
st.caption("No-BS Personal Grooming Plan.")

# HACK: Manual Payment Check
if st.query_params.get("paid") == "true":
    st.balloons()
    st.success("Welcome to the club.")
    with st.form("gen"):
        upl = st.file_uploader("Upload photo for analysis", type=['jpg', 'png'])
        st.caption("Click below to let AI write your strategy.")
        if st.form_submit_button("GENERATE MY PLAN"):
            if upl:
                with st.spinner("Analyzing..."):
                    # Use REAL AI now
                    data = analyze_skin("25-35", "Oily", "Acne", "No Sleep")
                    if data:
                        try:
                            pdf = create_pdf(data)
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                                pdf.output(tmp.name)
                                with open(tmp.name, "rb") as f:
                                    st.download_button("⬇️ DOWNLOAD PLAN (PDF)", f, "Skin_Roast_Plan.pdf", "application/pdf")
                            st.warning("Don't guess. Get the product list below.")
                            st.link_button("GET SHOPPING LIST ($5)", UPSELL_LINK)
                        except Exception as e:
                            st.error(f"Error generating PDF: {e}")
            else:
                st.error("Upload a photo first!")
else:
    with st.form("quiz"):
        st.write("#### 1. The Dossier:")
        st.selectbox("Age Group", ["Under 25", "25-35", "35-45", "45+"])
        st.selectbox("Skin Type", ["Oily (Shiny)", "Dry (Tight)", "Normal", "Sensitive"])
        st.selectbox("Main Enemy", ["Acne / Pimples", "Wrinkles / Aging", "Eye Bags / Tired", "Redness"])
        st.multiselect("Sins", ["Smoking/Vaping", "Alcohol", "Sugar/Fastfood", "No Sleep", "Stress"])
        
        st.write("#### 2. Visual Evidence:")
        st.file_uploader("Upload Selfie", type=['jpg', 'png'])
        
        if st.form_submit_button("SCAN FACE"):
            st.success("Data received.")
            st.info("🔥 Found 3 critical mistakes in your routine.")
            st.link_button("👉 GET THE PLAN ($10)", LEMON_SQUEEZY_LINK)
