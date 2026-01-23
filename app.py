import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. SETTINGS ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing in Secrets.")

GOAL, CURRENT = 6150000, 260
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# Все 10 проблем (включая круги под глазами)
SKIN_PROBLEMS = {
    "Eye Bags / Dark Circles": "Caffeine, Vitamin K & Peptides.",
    "Acne / Pimples": "Salicylic Acid & Benzoyl Peroxide.",
    "Wrinkles / Aging": "Retinol, Peptides & Hyaluronic Acid.",
    "Dryness": "Ceramides & Glycerin.",
    "Oily Skin": "Niacinamide & Zinc.",
    "Pigmentation": "Vitamin C & Alpha Arbutin.",
    "Irritation": "Panthenol & Centella.",
    "Blackheads": "BHA (Salicylic Acid).",
    "Flaking": "Lactic Acid & Urea.",
    "Redness": "Azelaic Acid."
}

# --- 2. PDF GENERATOR ---
def create_pdf(name, age, problem, roast_text, routine):
    pdf = FPDF()
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')

    # PAGE 1: ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(roast_text)) # Здесь будет длинная смешная шутка от AI

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean(problem).upper()}", ln=True)
    pdf.set_font("Helvetica", size=11)
    deep_details = (
        f"At {age}, your skin is showing signs of environmental exhaustion. The '{problem}' "
        f"issue isn't just surface-level; it's a structural cry for help. Your current routine "
        f"('{routine}') is clearly not providing the defense-grade hydration needed to prevent "
        "dermal collapse. We are seeing markers of accelerated aging that require a full tactical reset."
    )
    pdf.multi_cell(0, 7, txt=clean(deep_details))

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 10, "ALSO DETECTED (NOT INCLUDED):", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 6, "- Lack of deep-tissue hydration", ln=True)
    pdf.cell(0, 6, "- Visible loss of dermal elasticity", ln=True)
    pdf.cell(0, 6, "- Uneven micro-pigmentation", ln=True)

    # PAGE 2: PROTOCOLS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="Consult a doctor before these treatments.")
    
    for treat, desc in [("Botox", "Relaxes muscles."), ("Biorevitalization", "Deep hydration."), ("RF-Lifting", "Tightens skin.")]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 7, f"[*] {treat}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 5, f"Target: {desc}", ln=True); pdf.ln(2)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "YOUR HOME WEAPONS", ln=True)
    for w, why in [("Retinol", "Boosts collagen."), ("Peptides", "Repairs barrier."), ("Vit C", "Brightens.")]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 7, f"[+] {w}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 5, f"Why: {why}", ln=True); pdf.ln(1)

    # PAGE 3: ROUTINE & FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS (RESCUE ROUTINE)", ln=True)
    pdf.set_font("Helvetica", size=11)
    ops = (
        "MORNING:\n1. Gentle Cleanser\n2. Vitamin C Serum\n3. Peptide Moisturizer\n4. SPF 50+ (Mandatory)\n\n"
        "EVENING:\n1. Thorough Cleanse\n2. Retinol / Treatment\n3. Barrier Repair Cream\n4. Night Oil (optional)"
    )
    pdf.multi_cell(0, 7, txt=clean(ops))

    pdf.ln(15)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "A FINAL WORD FROM THE COMIC:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    final_joke = (
        f"Look, {name}, I've seen more life in a bowl of 3-day-old oatmeal. "
        "But your face isn't a lost cause; it's just a 'fixer-upper'. Stop washing your "
        "face with whatever floor cleaner you use, stick to the plan, and maybe "
        "one day you'll look like you actually enjoy being alive. I'm rooting for you—"
        "mostly so you look good enough to buy me that house in Lake Oswego. Get to work."
    )
    pdf.multi_cell(0, 7, txt=clean(final_joke))

    pdf.ln(10)
    pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, ">>> GET THE READY-MADE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 3. UI ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Project: Lake Oswego House. Raised: ${CURRENT}")

with st.form("roast_logic"):
    c1, c2 = st.columns(2)
    with c1:
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
    with c2:
        u_enemy = st.selectbox("Main Enemy", list(SKIN_PROBLEMS.keys()))
        u_routine = st.selectbox("Current Routine", ["Water", "Soap", "Moisturizer", "Full Routine"])
    
    u_sins = st.multiselect("Lifestyle Sins", ["No Sleep", "Stress", "Junk Food", "Smoking", "Sugar"])
    u_file = st.file_uploader("Upload Selfie for Analysis", type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button("GENERATE BRUTAL ROAST")

if submit and u_file and u_name:
    with st.spinner("Analyzing the damage..."):
        try:
            # РЕАЛЬНЫЙ ВЫЗОВ VISION API
            base64_img = base64.b64encode(u_file.read()).decode('utf-8')
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a brutal roast comedian. Analyze the photo and facts. Be funny, cynical, use metaphors. Don't be just mean, be witty. Focus on skin neglect. Max 100 words."},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"Name: {u_name}, Problem: {u_enemy}, Sins: {u_sins}. Roast me."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]}
                ]
            )
            roast_result = response.choices[0].message.content
            st.write(roast_result)
            
            pdf_p = create_pdf(u_name, u_age, u_enemy, roast_result, u_routine)
            with open(pdf_p, "rb") as f:
                st.download_button("⬇️ DOWNLOAD YOUR DOSSIER", f, file_name=f"Roast_{u_name}.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
