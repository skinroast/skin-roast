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

# --- 2. AI BRAIN (FOCUSED SPECIALIST) ---
SYSTEM_PROMPT = """
YOU ARE "SKIN ROAST BRO".
TONE: Funny, supportive, honest.
GOAL: Analyze ONLY the specific problem the user selected.

INSTRUCTIONS:
1. START with a light playful roast about their habits (Alcohol/Stress). Make a joke.
2. ANALYZE the *User Selected Problem* deeply based on the photo.
   - If they chose "Wrinkles": Describe depth, location (forehead, eyes), and severity.
   - If they chose "Acne": Describe inflammation type, zones.
3. DETECT but DO NOT SOLVE other issues. Mention them as "Also detected".
4. GENERATE A ROUTINE ONLY FOR THE SELECTED PROBLEM.

RESPONSE FORMAT (JSON ONLY):
{
  "roast_intro": "Light roast + joke about their habits (Alcohol, No Sleep). Keep it fun.",
  
  "deep_dive_analysis": "Detailed analysis of the SELECTED problem (e.g. Wrinkles). Describe exactly what you see in the photo regarding this specific issue. (4-5 sentences).",
  
  "other_issues_teaser": "List 2-3 OTHER problems you see in the photo (e.g. 'I also see large pores and redness...'), but add: 'But today we focus only on your main request.'",
  
  "ingredients": [
      {"name": "Ingredient Name", "why": "How it fixes the SELECTED problem"}
  ],
  
  "routine_morning": "Step-by-step morning routine for the SELECTED problem.",
  "routine_evening": "Step-by-step evening routine for the SELECTED problem."
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
    # IMPORTANT: We tell AI to focus ONLY on 'problem'
    user_text = f"User Data: Age {age}, Skin Type {skin_type}. FOCUS PROBLEM: {problem}. Habits to roast: {habits_str}."

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
            max_tokens=1500
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

def create_pdf(data, problem_name):
    """Generate PDF with CAPITALISM JOKE"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PAGE 1: ANALYSIS ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.ln(5)
    
    # 1. ROAST & JOKE
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['roast_intro']))
    pdf.ln(5)

    # 2. DEEP DIVE (SELECTED PROBLEM)
    pdf.set_font("Helvetica", 'B', 14)
    # Dynamic Title
    clean_problem = clean_text(problem_name).upper()
    pdf.cell(0, 10, f"DEEP SCAN: {clean_problem}", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['deep_dive_analysis']))
    pdf.ln(10)
    
    # 3. TEASER (OTHER ISSUES)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(100, 100, 100) # Grey color for teaser
    pdf.cell(0, 10, "ALSO DETECTED (NOT INCLUDED):", ln=True)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 6, txt=clean_text(data['other_issues_teaser']))
    pdf.multi_cell(0, 6, txt="(You can order a separate report for these issues later.)")
    pdf.set_text_color(0, 0, 0) # Reset color
    
    # --- PAGE 2: ACTION ---
    pdf.add_page()
    
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR WEAPONS", ln=True, align='C')
    
    for item in data['ingredients']:
        pdf.set_font("Helvetica", 'B', 13)
        pdf.cell(0, 8, txt=f"[+] {clean_text(item['name'])}", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 5, txt=f"Why: {clean_text(item['why'])}\n")
        pdf.ln(2)

    pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "THE ROUTINE", ln=True, align='C')
    
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
    
    # --- THE CAPITALISM JOKE ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "HONEST NOTE:", ln=True, align='C')
    pdf.set_font("Helvetica", '', 11)
    
    # The Joke Text
    joke_text = (
        "You can find the right cosmetics by active substance yourself through GPT or Gemini completely free of charge. "
        "But since I am saving for a house and a car, in the best traditions of capitalism, "
        "I offer you to buy a ready-made list for $5."
    )
    
    pdf.multi_cell(0, 6, txt=joke_text, align='C')
    pdf.ln(5)

    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    
    return pdf

# --- 3. UI INTERFACE ---
st.warning("""
⚠️ **HONEST WARNING:**
I have a goal: **Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)**.
Every $10 you spend gets me closer.
In return, I give you the truth about your face. Fair trade.
""")

GOAL = 6150000 
CURRENT = 70 
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
    # THE MAIN FOCUS
    p_enemy = st.selectbox("FOCUS PROBLEM (What do we fix today?)", ["Acne / Pimples", "Wrinkles / Aging", "Eye Bags / Tired", "Redness"], key="p_enemy")
    p_sins = st.multiselect("Bad Habits (For the roast)", ["Smoking", "Alcohol", "Sugar", "No Sleep", "Stress"], key="p_sins")

    # Image Upload
    upl = st.file_uploader("Upload Selfie (Required)", type=['jpg', 'png'])
    
    if st.button("GENERATE REPORT NOW"):
        if upl:
            with st.spinner("ANALYZING YOUR SELECTED PROBLEM..."):
                # CALLING THE REAL VISION AI
                data = analyze_skin_with_vision(upl, p_age, p_skin, p_enemy, p_sins)
                
                if data:
                    try:
                        # Pass p_enemy to PDF for the title
                        pdf = create_pdf(data, p_enemy)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ DOWNLOAD DOSSIER (PDF)", f, "Skin_Roast_Plan_Focus.pdf", "application/pdf")
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
