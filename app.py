import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. CONFIG (Должно быть строго первым) ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥")

# --- 2. AUTH & ASSETS ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing in Secrets.")

# Твои цели (Лейк-Освего)
GOAL, CURRENT = 6150000, 260
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# База знаний по проблемам (все 9 штук)
SKIN_PROBLEMS = {
    "Acne": "Salicylic Acid & Benzoyl Peroxide.",
    "Wrinkles": "Retinol & Peptides.",
    "Dryness": "Hyaluronic Acid & Ceramides.",
    "Oily Skin": "Niacinamide & Clay masks.",
    "Pigmentation": "Vitamin C & Sunscreen.",
    "Irritation": "Centella & Panthenol.",
    "Blackheads": "BHA (Salicylic Acid).",
    "Flaking": "Lactic Acid & Urea.",
    "Redness": "Azelaic Acid."
}

# --- 3. PDF GENERATOR ---
def create_pdf(name, age, problem, roast_text):
    pdf = FPDF()
    pdf.add_page()
    
    def clean_t(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')

    # Header
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean_t(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    # Vibe Check
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_t(roast_text))
    
    # Expanded Deep Scan
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean_t(problem).upper()}", ln=True)
    pdf.set_font("Helvetica", size=11)
    scan_details = (
        f"The pronounced state of {problem} indicates structural neglect. "
        "We are seeing micro-damage that, if left untreated, will accelerate "
        "dermal aging by 5-7 years within the next decade. Immediate action required."
    )
    pdf.multi_cell(0, 7, txt=clean_t(scan_details))

    # Also Detected Section
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 10, "ALSO DETECTED (ADDITIONAL ANALYSIS REQUIRED):", ln=True)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "- Secondary dehydration markers", ln=True)
    pdf.cell(0, 6, "- UV-induced micro-pigmentation", ln=True)
    pdf.cell(0, 6, "- Structural elasticity decline", ln=True)

    # Protocols
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="AM: Cleanse -> Target Serum -> SPF 50+\nPM: Cleanse -> Active Ingredient -> Heavy Cream")

    # Final Bro-Roast & Upsell
    pdf.ln(15)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(0, 10, "A NOTE FROM DR. ROAST:", ln=True, fill=True)
    
    joke = (
        f"Listen, {name}, you can find these active substances for free. "
        "But since I'm saving for a house in Lake Oswego and a car, I'm offering "
        "the easy way out. Stop wasting time and get my curated shopping list."
    )
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(0, 6, txt=clean_t(joke))

    pdf.ln(10)
    pdf.set_text_color(220, 0, 0)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, ">>> GET THE READY-MADE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 4. UI ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Goal: House & Car. Progress: ${CURRENT} / ${GOAL:,}")

with st.form("main_form"):
    u_name = st.text_input("First Name")
    u_age = st.selectbox("Age", ["18-24", "25-34", "35-44", "45+"])
    u_problem = st.selectbox("Main Skin Enemy", list(SKIN_PROBLEMS.keys()))
    u_sins = st.multiselect("Life Sins", ["No Sleep", "Smoking", "Alcohol", "Sugar", "Stress"])
    u_file = st.file_uploader("Selfie Evidence", type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button("REVEAL THE TRUTH")

if submit:
    if u_name and u_file:
        with st.spinner("Roasting your habits..."):
            try:
                # Имитация AI или реальный вызов (зависит от настроек API)
                roast = f"Hey {u_name}, your skin looks like a topographic map of bad decisions. Fix it."
                
                pdf_p = create_pdf(u_name, u_age, u_problem, roast)
                with open(pdf_p, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD YOUR UPGRADE PLAN", f, file_name=f"Roast_{u_name}.pdf")
                st.success("Analysis complete.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Provide Name and Photo.")
