import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key is missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
GOAL, CURRENT = 6150000, 260

# --- 2. МЕДИЦИНСКАЯ БАЗА ЗНАНИЙ (10 Проблем) ---
SKIN_DATABASE = {
    "Acne / Pimples": {"home": [("Salicylic Acid", "Deep pore cleansing."), ("Benzoyl Peroxide", "Kills acne bacteria.")], "pro": "Chemical Peels"},
    "Wrinkles / Aging": {"home": [("Retinol", "Collagen king."), ("Peptides", "Elasticity support.")], "pro": "Botox / RF-Lifting"},
    "Eye Bags / Dark Circles": {"home": [("Caffeine", "Fluid drainage."), ("Vitamin K", "Brightening.")], "pro": "Fillers / Lymphatic Drainage"},
    "Dryness / Flaking": {"home": [("Ceramides", "Barrier repair."), ("Hyaluronic Acid", "Hydration.")], "pro": "Biorevitalization"},
    "Oily Skin": {"home": [("Niacinamide", "Oil control."), ("Clay", "Toxin removal.")], "pro": "HydraFacial"},
    "Pigmentation": {"home": [("Vitamin C", "Evening tone."), ("Tranexamic Acid", "Dark spot fading.")], "pro": "IPL / Laser"},
    "Blackheads": {"home": [("BHA", "Oil dissolution."), ("Oil Cleanser", "Deep pore prep.")], "pro": "Manual Extraction"},
    "Redness / Irritation": {"home": [("Azelaic Acid", "Redness control."), ("Centella", "Soothing.")], "pro": "Phototherapy"},
    "Large Pores": {"home": [("Retinoids", "Pore shrinking."), ("BHA", "Texture refinement.")], "pro": "Fractional Laser"},
    "Dullness": {"home": [("Glycolic Acid", "Exfoliation."), ("Vit C", "Glow.")], "pro": "Mesotherapy"}
}

# --- 3. ПОЛНЫЙ PDF-ГЕНЕРАТОР (4 СТРАНИЦЫ) ---
def create_comprehensive_pdf(name, age, problem, roast_text, routine, sins):
    pdf = FPDF()
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')
    data = SKIN_DATABASE.get(problem, SKIN_DATABASE["Wrinkles / Aging"])

    # PAGE 1: THE BRUTAL ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, f"OFFICIAL SKIN DOSSIER: {clean(name).upper()}", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 5, f"Subject Age: {age} | Targets: {clean(problem)}", ln=True, align='C')

    pdf.ln(15)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 10, "THE VIBE CHECK (AI ROAST):", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, txt=clean(roast_text))

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "EXPANDED DEEP SCAN:", ln=True)
    scan_text = (f"Analysis of {problem} at age {age} shows structural instability. "
                 f"Current routine ({routine}) and lifestyle factors ({', '.join(sins)}) "
                 "have led to accelerated dermal aging. Immediate reset is required.")
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(scan_text))

    # PAGE 2: CLINICAL PROTOCOLS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=f"To address {problem} effectively, consider these professional treatments:")
    
    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, f"[*] {data['pro']}", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="Consult a licensed dermatologist for clinical procedures.")

    # PAGE 3: HOME WEAPONS & ROUTINE
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "YOUR HOME WEAPONS & ROUTINE", ln=True)
    for weapon, why in data['home']:
        pdf.set_font("Helvetica", 'B', 13); pdf.cell(0, 10, f"[+] {weapon}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=f"Why: {why}"); pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "DAILY OPS (RESCUE MISSION):", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=f"AM: Cleanse -> {data['home'][1][0]} -> SPF 50+\nPM: Cleanse -> {data['home'][0][0]} -> Barrier Repair Cream.")

    # PAGE 4: FINAL WORD & UPSELL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 15, "FINAL WORD FROM THE COMIC:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    final_joke = (f"Listen, {name}, your skin has the texture of a crumpled-up tax return. "
                  "Fix it now, or spend the next 20 years explaining why you look like a "
                  "dehydrated raisin. I'm rooting for you—mostly for my Lake Oswego fund.")
    pdf.multi_cell(0, 8, txt=clean(final_joke))

    pdf.ln(20)
    pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, ">>> GET THE FULL SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    
    pdf.ln(20); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt="MEDICAL DISCLAIMER: Not medical advice. Informational purposes only.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Progress to Lake Oswego House: ${CURRENT} / ${GOAL:,}")

with st.form("roast_logic"):
    c1, c2 = st.columns(2)
    with c1:
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
    with c2:
        u_enemy = st.selectbox("Main Skin Enemy", list(SKIN_DATABASE.keys()))
        u_routine = st.selectbox("Current Routine", ["None/Water", "Soap", "Basic Moisturizer", "Full Routine"])
    
    u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "No Sleep", "Junk Food", "Stress", "No SPF"])
    u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button("GENERATE FULL REPORT")

if submit and u_file and u_name:
    with st.spinner("Analyzing photo and habits..."):
        try:
            # РЕАЛЬНЫЙ АНАЛИЗ ФОТО
            base64_img = base64.b64encode(u_file.read()).decode('utf-8')
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a witty Bro-Roast comedian. Analyze the photo and call out the TRUTH. If the photo looks fine but they chose 'Acne', tease them for being a perfectionist. Max 100 words."},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"Name: {u_name}, Age: {u_age}, Goal: {u_enemy}. Roast me."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]}
                ]
            )
            roast = response.choices[0].message.content
            st.success("Analysis Complete.")
            
            pdf_p = create_comprehensive_pdf(u_name, u_age, u_enemy, roast, u_routine, u_sins)
            with open(pdf_p, "rb") as f:
                st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
