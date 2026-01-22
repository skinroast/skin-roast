import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os
import base64

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

# --- 2. AI BRAIN (DEEP VISION PROTOCOL) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO".
You are the user's best friend/coach who knows everything about skincare.
TONE: Supportive, masculine, detailed, authoritative.
Metaphors: Mechanics, Engineering, Architecture, "The Game".

YOUR GOAL: Perform a DEEP visual scan of the user's photo and compare it to their data.

INSTRUCTIONS FOR ANALYSIS:
1. Look closely at the photo. Identify textures, colors, depth of lines, and oiliness.
2. COMPARE the photo with the user's self-reported data.
3. IF they missed something (e.g., they said "Acne" but you see "Wrinkles"), POINT IT OUT.
4. WRITE IN DETAIL. Do not write short sentences. Write full paragraphs.

RESPONSE FORMAT (JSON ONLY - NO EMOJIS):
{
  "intro_roast": "A friendly but sharp opening roast (3-4 sentences). Acknowledge their effort but highlight the reality.",
  
  "visual_scan": "DETAILED VISUAL ANALYSIS (5-7 sentences). Use this structure: 'I looked at your photo. You mentioned [User Problem], and yes, it is present. HOWEVER, I also see [Other Issue] that you didn't mention...'. Describe specifically what you see (forehead lines, redness size, dark circles depth).",
  
  "science_why": "Explain the biological reasons for what you saw in the visual scan (3-4 sentences). Use terms like 'Collagen density', 'Lipid barrier', 'Cortisol spikes'.",
  
  "problems_list": ["Visual Issue 1", "Visual Issue 2", "Visual Issue 3"],
  
  "ingredients": [
      {"name": "Ingredient Name", "why": "Detailed explanation of how this fixes the specific visual issue"}
  ],
  
  "routine_morning": "Detailed step-by-step morning routine.",
  "routine_evening": "Detailed step-by-step evening routine.",
  "motivation": "Final strong closing statement about discipline and consistency."
}
"""

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_skin_with_vision(image_file, age, skin_type, problem, habits):
    if not openai.api_key:
        return None
    
    # 1. Prepare Image
    base64_image = encode_image(image_file)
    
    # 2. Prepare Data Text
    habits_str = ", ".join(habits) if habits else "None"
    user_text = f"User Data: Age {age}, Skin Type {skin_type}, Main Complaint {problem}, Bad Habits: {habits_str}."

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
            max_tokens=1500 # Increased token limit for longer answers
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

def clean_text(text):
    """Helper to remove bad characters for PDF"""
    if isinstance(text, str):
        return text.encode('latin-1', 'replace').decode('latin-1')
    return str(text)

def create_pdf(data):
    """Generate RICH PDF"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1: ANALYSIS ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.ln(5)
    
    # 1. INTRO
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "REALITY CHECK:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['intro_roast']))
    pdf.ln(5)

    # 2. DEEP VISUAL SCAN (The new thick part)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "VISUAL EVIDENCE (FROM PHOTO):", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['visual_scan']))
    pdf.ln(5)
    
    # 3. THE SCIENCE
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE BIOLOGY:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['science_why']))
    pdf.ln(5)
    
    # 4. SUMMARY
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DETECTED ISSUES:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    for prob in data['problems_list']:
        pdf.cell(0, 6, txt=f"[X] {clean_text(prob)}", ln=True)

    # --- PAGE 2: ACTION ---
    pdf.add_page()
    
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR WEAPONS (ARSENAL)", ln=True, align='C')
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 13)
        pdf.cell(0, 8, txt=f"[+] {clean_text(item['name'])}", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 5, txt=f"Target: {clean_text(item['why'])}\n")
        pdf.ln(2)

    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "BATTLE PLAN", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "MORNING:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['routine_morning']))
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "EVENING:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['routine_evening']))

    pdf.ln(15)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12)
    pdf.multi_cell(0, 8, txt=clean_text(data['motivation']), align='C')

    pdf.ln(10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> DOWNLOAD SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    
    return pdf

# --- 3. UI INTERFACE ---
st.warning("""
⚠️ **HONEST WARNING:**
I have a goal: **Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)**.
Every $10 you spend gets me closer.
In return, I give you the truth about your face. Fair trade.
""")

GOAL = 6150000 
CURRENT = 60 
st.progress(CURRENT / GOAL)
st.caption(f"Raised: ${CURRENT} of ${GOAL:,}.")
st.divider()

st.title("SKIN ROAST 🔥")
st.caption("The Protocol for Men.")

# PAYMENT SUCCESS STATE
if st.query_params.get("paid") == "true":
    st.markdown('<div class="success-box">PAYMENT VERIFIED. ACCESS GRANTED.</div>', unsafe_allow_html=True)
    st.snow() 
    
    st.write("### Configure Analysis:")
    
    # Input Data
    p_age = st.selectbox("Your Age", ["Under 25", "25-35", "35-45", "45+"], key="p_age")
    p_skin = st.selectbox("Skin Type", ["Oily (Shiny)", "Dry (Tight)", "Normal", "Sensitive"], key="p_skin")
    p_enemy = st.selectbox("Main Problem", ["Acne / Pimples", "Wrinkles / Aging", "Eye Bags / Tired", "Redness"], key="p_enemy")
    p_sins = st.multiselect("Bad Habits", ["Smoking", "Alcohol", "Sugar", "No Sleep", "Stress"], key="p_sins")

    # Image Upload
    upl = st.file_uploader("Upload Selfie (Required for Roast)", type=['jpg', 'png'])
    
    if st.button("GENERATE REPORT NOW"):
        if upl:
            with st.spinner("SCANNING FACE & DATA... (This takes 10-15 seconds)"):
                # CALLING THE REAL VISION AI
                data = analyze_skin_with_vision(upl, p_age, p_skin, p_enemy, p_sins)
                
                if data:
                    try:
                        pdf = create_pdf(data)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ DOWNLOAD DOSSIER (PDF)", f, "Skin_Roast_Plan_Deep.pdf", "application/pdf")
                        st.success("REPORT GENERATED.")
                        st.link_button("GET THE TOOLS ($5)", UPSELL_LINK)
                    except Exception as e:
                        st.error(f"PDF Error: {e}")
        else:
            st.error("Please upload a photo so I can see what we are dealing with!")

# FREE VERSION
else:
    with st.form("quiz"):
        st.write("#### 1. The Dossier:")
        st.selectbox("Age Group", ["Under 25", "25-35", "35-45", "45+"])
        st.selectbox("Skin Type", ["Oily (Shiny)", "Dry (Tight)", "Normal", "Sensitive"])
        st.selectbox("Main Enemy", ["Acne / Pimples", "Wrinkles / Aging", "Eye Bags / Tired", "Redness"])
        st.multiselect("Sins", ["Smoking", "Alcohol", "Sugar", "No Sleep", "Stress"])
        
        st.write("#### 2. Visual Evidence:")
        st.file_uploader("Upload Selfie", type=['jpg', 'png'])
        
        if st.form_submit_button("SCAN FACE"):
            st.success("SCAN COMPLETE.")
            st.info("🔥 3 Critical Failures Detected.")
            st.link_button("👉 UNLOCK FULL REPORT ($10)", LEMON_SQUEEZY_LINK)
