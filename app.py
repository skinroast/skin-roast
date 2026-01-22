import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os
import base64
import re

# --- 1. CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="Skin Roast: Upgrade Plan", page_icon="🔥", layout="centered")

# --- 2. SETUP & SECRETS ---
try:
    if "OPENAI_API_KEY" in st.secrets:
        openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ OpenAI Key not found in Secrets.")

# LINKS
LEMON_SQUEEZY_LINK = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_LINK = "https://skin-roast.lemonsqueezy.com/buy"

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

# --- 3. AI BRAIN (PURE CYNICISM / NO FAIRYTALES) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO". 
Tone: Cynical, World-Weary, Witty, "Succession" meets "Fight Club".
GOAL: A "Sandwich Roast" that hurts the ego but heals the soul.

🛑 STRICT BAN LIST (DO NOT USE):
- NO Pirates, NO Sea Captains, NO Vikings.
- NO Wizards, NO Magic, NO "Wise Sage", NO "Ancient Mysteries".
- NO "Adventures", NO "Nature".
- NO basic insults like "You look drunk".

✅ MANDATORY INSTRUCTIONS (MODERN STRESS):
- USE THEMES: High Finance, Tech Startups, Criminal Defense, Expensive Divorce, Michelin Kitchens, 72-Hour Coding Sprints, IRS Audits.
- FORMULA: "You look like [High Status Person] BUT [In a disastrous situation]."

EXAMPLES OF THE VIBE WE WANT:
- "You have the intense stare of a hedge fund manager... specifically one who just realized he forgot to hedge and lost 4 billion dollars."
- "You look like the lead singer of a rock band... but the version that's been on a reunion tour for 6 months without sleep."
- "You give off the vibe of a high-end lawyer... who just spent 72 hours shredding documents before the FBI arrived."
- "You look like a tech founder... right after his crypto coin went to zero."

STRUCTURE OF ROAST INTRO:
1. Compliment (Status/Vibe).
2. The TWIST (The cynical reality check based on skin issues).
3. The SUPPORT (We can fix this).

2. DEEP SCAN: Analyze the SELECTED problem in detail.
3. CLINICAL PROCEDURES: Recommend 2-3 professional treatments.
4. ROUTINE: Detailed steps. Mention SPF!

RESPONSE FORMAT (JSON ONLY):
{
  "roast_intro": "WRITE THE ROAST HERE. Modern, cynical, funny.",
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
    
    # ROAST
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
    
    # CLINICAL
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True, align='C')
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt="Professional treatments for faster results. Consult a certified doctor first.", align='C')
    pdf.ln(5)

    for item in data['clinical_treatments']:
        pdf.set_font("Helvetica", 'B', 13)
        pdf.cell(0, 8, txt=f"[*] {clean_text(item['name'])}", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 5, txt=f"Target: {clean_text(item['why'])}\n")
        pdf.ln(2)

    pdf.ln(5)

    # INGREDIENTS
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR HOME WEAPONS", ln=True, align='C')
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 13)
        pdf.cell(0, 8, txt=f"[+] {clean_text(item['name'])}", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 5, txt=f"Why: {clean_text(item['why'])}\n")
        pdf.ln(2)

    # --- PAGE 3 ---
    pdf.add_page()
    
    # SAFETY
    pdf.set_fill_color(255, 200, 200) 
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "[!] SAFETY PROTOCOL (READ THIS):", ln=True, fill=True)
    pdf.set_font("Helvetica", '', 11)
    safety_text = (
        "1. Active ingredients (Retinol, Acids) are powerful. They can burn if misused.\n"
        "2. ALWAYS use SPF 30+ if you use Retinol or Acids. No excuses.\n"
        "3. PATCH TEST: Apply a small amount on your neck before putting it on your face.\n"
        "4. Start slowly: Use Retinol 2 times a week, then increase.\n"
        "5. Check for allergies and read the instructions on the bottle."
    )
    pdf.multi_cell(0, 6, txt=safety_text)
    pdf.ln(10)

    # ROUTINE
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "DAILY OPERATIONS", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "MORNING:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['routine_morning']))
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "EVENING:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['routine_evening']))

    pdf.ln(10)
    
    # JOKE
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "HONEST NOTE:", ln=True, align='C')
    pdf.set_font("Helvetica", '', 11)
    
    joke_text = (
        "You can find these cosmetics by active substance yourself through GPT or Gemini completely free of charge. "
        "But since I am saving for a house and a car, in the best traditions of capitalism, "
        "I offer you to buy a ready-made list for $5."
    )
    pdf.multi_cell(0, 6, txt=joke_text, align='C')
    pdf.ln(5)

    # LINK
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    
    pdf.ln(15)
    
    # DISCLAIMER
    pdf.set_text_color(100, 100, 100) 
    pdf.set_font("Helvetica", 'I', 8)
    disclaimer = (
        "MEDICAL DISCLAIMER: This report is generated by AI for informational purposes only. "
        "It does not constitute medical advice, diagnosis, or treatment. "
        "Always seek the advice of a qualified physician or dermatologist. "
        "The user assumes full responsibility for the use of any recommended products."
    )
    pdf.multi_cell(0, 4, txt=disclaimer, align='C')

    return pdf

# --- 4. UI INTERFACE ---
st.warning("""
⚠️ **HONEST WARNING:**
I have a goal: **Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)**.
Every $10 you spend gets me closer.
In return, I give you the truth about your face. Fair trade.
""")

GOAL = 6150000 
CURRENT = 160 
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
    
    p_age = st.selectbox("Your Age", ["Under 25", "25-35", "35-45", "45+"], key="p_age")
    p_skin = st.selectbox("Skin Type", ["Oily (Shiny)", "Dry (Tight)", "Normal", "Sensitive"], key="p_skin")
    p_enemy = st.selectbox("FOCUS PROBLEM", ["Acne / Pimples", "Wrinkles / Aging", "Eye Bags / Tired", "Redness"], key="p_enemy")
    p_sins = st.multiselect("Bad Habits", ["Smoking", "Alcohol", "Sugar", "No Sleep", "Stress"], key="p_sins")

    upl = st.file_uploader("Upload Selfie (Required)", type=['jpg', 'png'])
    
    if st.button("GENERATE REPORT NOW"):
        if upl:
            with st.spinner("SCANNING FACE & DATA..."):
                data = analyze_skin_with_vision(upl, p_age, p_skin, p_enemy, p_sins)
                if data:
                    try:
                        pdf = create_pdf(data, p_enemy)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ DOWNLOAD FULL DOSSIER (PDF)", f, "Skin_Roast_Cynical.pdf", "application/pdf")
                        st.success("REPORT GENERATED.")
                        st.link_button("GET THE TOOLS ($5)", UPSELL_LINK)
                    except Exception as e:
                        st.error(f"PDF Error: {e}")
        else:
            st.error("Upload a photo!")
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
