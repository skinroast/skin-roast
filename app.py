import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os

# --- 1. SETUP & SECRETS ---
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# LINKS (REPLACE WITH YOURS LATER)
LEMON_SQUEEZY_LINK = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_LINK = "https://skin-roast.lemonsqueezy.com/buy"

st.set_page_config(page_title="Skin Roast: Upgrade Plan", page_icon="🔥", layout="centered")

# CSS HACK: Hide Streamlit branding & Style Buttons
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

# --- 2. AI BRAIN (BRO PROMPT - ENGLISH) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO". You are the user's best friend and mentor.
Your goal is to help your bro become handsome using the "Sandwich Method":
[Recognition of Potential] -> [Roast of Bad Habits] -> [Motivation].

TONE OF VOICE:
- Address user as "Bro", "Champ", "Man".
- Metaphors: Jaguar V12, Lake Oswego, NBA, Wall Street, Survival Mode.
- NO insults to personality. Roast the LAZINESS and the BAD SKIN HABITS only.

RESPONSE FORMAT (JSON ONLY):
{
  "roast": "Roast text (3-4 punchy sentences)",
  "problems_list": ["Problem 1", "Problem 2"],
  "ingredients": [
      {"name": "Ingredient Name", "why": "Why it works (1 sentence)"}
  ],
  "routine_morning": "Morning steps bullet points",
  "routine_evening": "Evening steps bullet points",
  "motivation": "Final motivational quote"
}
"""

def analyze_skin(age, skin_type, problem, habits):
    """Call OpenAI"""
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
    """Generate English PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Fonts are standard in English (Arial/Helvetica)
    pdf.set_font("Helvetica", 'B', 28)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", '', 14)
    pdf.multi_cell(0, 10, txt=f"VERDICT: {data['roast']}")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "IDENTIFIED ISSUES:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    for prob in data['problems_list']:
        pdf.cell(0, 8, txt=f"- {prob}", ln=True)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, "YOUR WEAPONS (ARSENAL)", ln=True, align='C')
    pdf.ln(10)
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, txt=f"🧪 {item['name']}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        pdf.multi_cell(0, 6, txt=f"Why: {item['why']}\n")
        pdf.ln(5)

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, "BATTLE PLAN (ROUTINE)", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "☀️ MORNING:", ln=True)
    pdf.set_font("Helvetica", '', 12)
    pdf.multi_cell(0, 6, txt=data['routine_morning'])
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "🌙 EVENING:", ln=True)
    pdf.multi_cell(0, 6, txt=data['routine_evening'])

    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 26)
    pdf.cell(0, 30, "DON'T BE STUPID", ln=True, align='C')
    pdf.set_font("Helvetica", '', 14)
    pdf.multi_cell(0, 10, txt="You know the theory. But if you buy trash products, you'll make it worse.\n\nI curated a list of products that actually work.\n\nClick below to get the shopping list.", align='C')
    pdf.ln(20)
    
    pdf.set_text_color(0, 0, 255)
    pdf.set_font("Helvetica", 'U', 14)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    return pdf

# --- 3. UI INTERFACE ---

# THE LEGEND (ENGLISH)
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

# GOAL TRACKER
GOAL = 6150000 
CURRENT = 40 
st.progress(CURRENT / GOAL)
st.caption(f"Raised: ${CURRENT} of ${GOAL:,}. Long way to go.")
st.divider()

st.title("SKIN ROAST 🔥")
st.caption("No-BS Personal Grooming Plan.")

if st.query_params.get("paid") == "true":
    st.balloons()
    st.success("Welcome to the club.")
    with st.form("gen"):
        upl = st.file_uploader("Upload photo for analysis", type=['jpg', 'png'])
        st.caption("Click below to let AI write your strategy.")
        if st.form_submit_button("GENERATE MY PLAN"):
            if upl:
                with st.spinner("Analyzing..."):
                    # Mock data for MVP test
                    data = analyze_skin("30", "Oily", "Acne", "No Sleep")
                    if data:
                        pdf = create_pdf(data)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ DOWNLOAD PLAN (PDF)", f, "Skin_Roast_Plan.pdf", "application/pdf")
                        st.warning("Don't guess. Get the product list below.")
                        st.link_button("GET SHOPPING LIST ($5)", UPSELL_LINK)
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
