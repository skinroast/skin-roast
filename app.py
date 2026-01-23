import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# --- 2. AUTH & CONSTANTS ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing in Secrets.")

GOAL, CURRENT = 6150000, 260
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

SKIN_PROBLEMS = {
    "Acne / Pimples": "Salicylic Acid & Benzoyl Peroxide.",
    "Wrinkles / Aging": "Retinol, Peptides & Hyaluronic Acid.",
    "Dryness": "Ceramides & Glycerin.",
    "Oily Skin": "Niacinamide & Zinc.",
    "Pigmentation": "Vitamin C & Alpha Arbutin.",
    "Irritation": "Panthenol & Centella.",
    "Blackheads": "BHA (Salicylic Acid).",
    "Flaking": "Lactic Acid & Urea.",
    "Redness": "Azelaic Acid & Niacinamide."
}

# --- 3. PDF GENERATOR (FULL VERSION) ---
def create_pdf(name, age, problem, roast_text, routine):
    pdf = FPDF()
    
    def clean_t(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')

    # --- PAGE 1: ANALYSIS ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean_t(name).upper()}'S UPGRADE PLAN", ln=True, align='C') # [cite: 1, 52]

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True) # [cite: 2, 53]
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_t(roast_text)) # [cite: 3, 54]

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean_t(problem).upper()}", ln=True) # [cite: 6, 55]
    pdf.set_font("Helvetica", size=11)
    # Увеличенный блок Deep Scan
    deep_details = (
        f"The pronounced state of {problem} indicates structural neglect. At {age}, your skin "
        f"shouldn't be fighting for its life. The current routine ('{routine}') is clearly "
        "failing to mitigate micro-damage. We are seeing a breakdown in dermal density that, "
        "if untreated, will accelerate visible aging by 5-7 years within the next decade. "
        "Immediate intervention is non-negotiable."
    ) # [cite: 7, 56, 57]
    pdf.multi_cell(0, 7, txt=clean_t(deep_details))

    # Also Detected Section
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 10, "ALSO DETECTED (ADDITIONAL ANALYSIS REQUIRED):", ln=True) # 
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.cell(0, 7, "- Secondary dehydration markers", ln=True) # [cite: 12, 59]
    pdf.cell(0, 7, "- UV-induced micro-pigmentation", ln=True) # [cite: 12, 60]
    pdf.cell(0, 7, "- Structural elasticity decline", ln=True) # [cite: 12, 61]

    # --- PAGE 2: CLINICAL & HOME PROTOCOLS ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True) # [cite: 13]
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="Consult a certified doctor before these treatments.") # [cite: 14]
    
    pro_treatments = [
        ("Botox Injections", "Relaxes muscles to reduce wrinkles."), # [cite: 15, 16]
        ("Biorevitalization", "Deep hydration to restore suppleness."), # [cite: 17, 18]
        ("RF-Lifting", "Tightens skin and reduces fine lines.") # [cite: 19, 20]
    ]
    for treat, target in pro_treatments:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 7, f"[*] {treat}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 5, f"Target: {target}", ln=True)
        pdf.ln(2)

    # Home Weapons
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "YOUR HOME WEAPONS", ln=True) # [cite: 21]
    weapons = [
        ("Retinol (Vitamin A)", "Boosts collagen production."), # [cite: 22, 23]
        ("Peptides", "Enhances skin barrier function."), # [cite: 24, 25]
        ("Vitamin C", "Brightens and protects.") # [cite: 26, 27]
    ]
    for w, why in weapons:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 7, f"[+] {w}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 5, f"Why: {why}", ln=True)
        pdf.ln(1)

    # --- PAGE 3: SAFETY & OPERATIONS ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, "[!] SAFETY PROTOCOL:", ln=True) # [cite: 28]
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=10)
    safety = (
        "1. Active ingredients can burn if misused.\n" # [cite: 29]
        "2. ALWAYS use SPF 30+ with Retinol/Acids.\n" # 
        "3. PATCH TEST on neck before full face application.\n" # [cite: 31]
        "4. Start slowly: 2 times a week, then increase." # [cite: 32]
    )
    pdf.multi_cell(0, 6, txt=clean_t(safety))

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS", ln=True) # [cite: 33, 62]
    pdf.set_font("Helvetica", size=10)
    ops = (
        "AM: Cleanse -> Vit C Serum -> SPF 50+.\n" # [cite: 63]
        "PM: Cleanse -> Active Ingredient -> Heavy Cream." # [cite: 64]
    )
    pdf.multi_cell(0, 6, txt=clean_t(ops))

    # Final Bro-Roast & Upsell
    pdf.ln(20)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "HONEST NOTE FROM DR. ROAST:", ln=True, fill=True) # [cite: 44, 65]
    
    final_joke = (
        f"Listen, {name}, you can find these active substances for free. " # [cite: 45, 66]
        "But since I'm saving for a house in Lake Oswego and a car, I'm offering " # [cite: 46, 67]
        "the easy way out. Stop being cheap with your only face. Buy the curated "
        "shopping list and save yourself the research time." # [cite: 47, 48, 68]
    )
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 7, txt=clean_t(final_joke))

    pdf.ln(10)
    pdf.set_text_color(220, 0, 0)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, ">>> GET THE READY-MADE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL) # [cite: 48, 69]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 4. UI FLOW ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Goal: House in Lake Oswego. Raised: ${CURRENT} / ${GOAL:,}")

with st.form("roast_logic"):
    col1, col2 = st.columns(2)
    with col1:
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"]) # Категория 55+ на месте
    with col2:
        u_enemy = st.selectbox("Main Enemy", list(SKIN_PROBLEMS.keys()))
        u_routine = st.selectbox("Current Routine", ["Water only", "Soap/3-in-1", "Moisturizer", "Full Routine"]) # Поле рутины на месте
    
    u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No Sleep", "No Sunscreen"])
    u_file = st.file_uploader("Upload Evidence (Selfie)", type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button("GENERATE BRUTAL ROAST")

if submit:
    if u_file and u_name:
        with st.spinner("Analyzing the damage..."):
            try:
                # В реальной версии здесь будет вызов openai.chat.completions.create с Vision
                roast = f"Hey {u_name}, your face looks like a topographic map of bad decisions. Fix it." # [cite: 54]
                
                pdf_path = create_pdf(u_name, u_age, u_enemy, roast, u_routine)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD YOUR DOSSIER", f, file_name=f"Roast_{u_name}.pdf")
                st.success("Analysis complete. Fix your face.")
            except Exception as e:
                st.error(f"Error: {e}")
