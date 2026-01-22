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

# --- 2. AI BRAIN ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO". A ruthless but helpful mentor.
Your goal: Make the user rich and handsome.
TONE: Stoic, aggressive, high-value male, Wall Street style.
TASK: Analyze the user's skin data and generate a DETAILED report.
IMPORTANT: DO NOT USE EMOJIS IN ANY PART OF THE JSON RESPONSE.

RESPONSE FORMAT (JSON ONLY):
{
  "roast": "A harsh roast of their current look (3-4 sentences).",
  "science_why": "Scientific explanation of why their skin is failing (2-3 sentences).",
  "problems_list": ["Problem 1", "Problem 2", "Problem 3"],
  "ingredients": [
      {"name": "Ingredient Name", "why": "Detailed reason why it works"}
  ],
  "diet_roast": "Roast their diet habits and tell them what to eat instead.",
  "lifestyle_fix": "Strict advice on sleep and stress.",
  "routine_morning": "Step-by-step morning routine.",
  "routine_evening": "Step-by-step evening routine.",
  "motivation": "Final closing statement about Discipline."
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

def clean_text(text):
    """Helper to remove bad characters for PDF"""
    if isinstance(text, str):
        return text.encode('latin-1', 'replace').decode('latin-1')
    return str(text)

def create_pdf(data):
    """Generate PDF (Stabilized Version)"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Fonts
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "PROTOCOL: UPGRADE", ln=True, align='C')
    pdf.ln(5)
    
    # 1. THE ROAST
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "STATUS REPORT:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_roast = clean_text(data['roast'])
    pdf.multi_cell(0, 6, txt=text_roast)
    pdf.ln(5)

    # 2. THE SCIENCE
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE BIOLOGICAL FAILURE:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_science = clean_text(data['science_why'])
    pdf.multi_cell(0, 6, txt=text_science)
    pdf.ln(5)
    
    # 3. IDENTIFIED ISSUES
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "CRITICAL ERRORS:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    for prob in data['problems_list']:
        text_prob = clean_text(prob)
        pdf.cell(0, 6, txt=f"[X] {text_prob}", ln=True)

    pdf.ln(10)
    
    # 4. DIET & LIFESTYLE
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "INTERNAL SYSTEMS", ln=True, align='L')
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "FUEL INTAKE:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_diet = clean_text(data['diet_roast'])
    pdf.multi_cell(0, 6, txt=text_diet)
    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "OPERATING SYSTEM (SLEEP):", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_life = clean_text(data['lifestyle_fix'])
    pdf.multi_cell(0, 6, txt=text_life)
    
    pdf.add_page() # --- PAGE 2 ---

    # 5. WEAPONS
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR ARSENAL", ln=True, align='C')
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 13)
        name = clean_text(item['name'])
        why = clean_text(item['why'])
        
        pdf.cell(0, 8, txt=f"[+] {name}", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 5, txt=f"Target: {why}\n")
        pdf.ln(2)

    pdf.ln(5)

    # 6. ROUTINE
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "DEPLOYMENT SCHEDULE", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "MORNING (07:00):", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_morning = clean_text(data['routine_morning'])
    pdf.multi_cell(0, 6, txt=text_morning)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "EVENING (22:00):", ln=True)
    pdf.set_font("Helvetica", '', 11)
    
    text_evening = clean_text(data['routine_evening'])
    pdf.multi_cell(0, 6, txt=text_evening)

    pdf.ln(15)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "FINAL DIRECTIVE", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12)
    
    text_motivation = clean_text(data['motivation'])
    pdf.multi_cell(0, 8, txt=text_motivation, align='C')

    pdf.ln(10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> DOWNLOAD SHOPPING LIST (REQUIRED) <<<", ln=True, align='C', link=UPSELL_LINK)
    
    return pdf

# --- 3. UI INTERFACE ---
st.warning("""
⚠️ **HONEST WARNING:**
I have a goal: **Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)**.
Every $10 you spend gets me closer.
In return, I give you the truth about your face. Fair trade.
""")

GOAL = 6150000 
CURRENT = 50 
st.progress(CURRENT / GOAL)
st.caption(f"Raised: ${CURRENT} of ${GOAL:,}.")
st.divider()

st.title("SKIN ROAST 🔥")
st.caption("The Protocol for Men.")

# PAYMENT SUCCESS STATE
if st.query_params.get("paid") == "true":
    st.markdown('<div class="success-box">PAYMENT VERIFIED. ACCESS GRANTED.</div>', unsafe_allow_html=True)
    st.snow() 
    
    upl = st.file_uploader("UPLOAD TARGET DATA (SELFIE)", type=['jpg', 'png'])
    
    if st.button("INITIALIZE ANALYSIS"):
        if upl:
            with st.spinner("PROCESSING BIOMETRICS..."):
                data = analyze_skin("25-35", "Oily", "Acne", "No Sleep")
                if data:
                    try:
                        pdf = create_pdf(data)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ DOWNLOAD DOSSIER (PDF)", f, "Skin_Roast_Plan_v2.pdf", "application/pdf")
                        st.success("REPORT GENERATED.")
                        st.link_button("GET THE TOOLS ($5)", UPSELL_LINK)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.error("PHOTO REQUIRED.")

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
            st.success("SCAN COMPLETE.")
            st.info("🔥 3 Critical Failures Detected.")
            st.link_button("👉 UNLOCK FULL REPORT ($10)", LEMON_SQUEEZY_LINK)
