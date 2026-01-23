import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. SETTINGS & FULL DATABASE ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing.")

# Динамическая база под каждую проблему
SPECIFIC_LOGIC = {
    "Redness": {
        "home": [("Azelaic Acid", "Reduces inflammation."), ("Centella", "Calms the fire.")],
        "pro": [("Phototherapy (IPL)", "Targeting broken capillaries."), ("Laser", "Vascular reset.")],
        "deep": "Your skin's barrier is compromised, likely due to over-cleansing or environmental stress."
    },
    "Wrinkles / Aging": {
        "home": [("Retinol", "Collagen king."), ("Peptides", "Structural support.")],
        "pro": [("Botox", "Muscle freeze."), ("RF-Lifting", "Tightening.")],
        "deep": "Visible collagen degradation detected. The structural integrity is thinning."
    },
    "Eye Bags / Dark Circles": {
        "home": [("Caffeine", "De-puffing."), ("Vit K", "Blood flow.")],
        "pro": [("Fillers", "Volume restoration."), ("Lymphatic drainage", "Fluid removal.")],
        "deep": "Periorbital exhaustion. This is more about sleep debt and thin skin than just 'tiredness'."
    }
    # ... остальные 7 проблем добавляются по аналогии
}

def create_pdf(name, age, problem, roast_text, routine):
    pdf = FPDF()
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')
    data = SPECIFIC_LOGIC.get(problem, SPECIFIC_LOGIC["Wrinkles / Aging"])

    # PAGE 1: VIBE & SCAN
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean(roast_text))

    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, f"DEEP SCAN: {clean(problem).upper()}", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean(data["deep"]))

    # PAGE 2: WEAPONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 10, "CLINICAL PROTOCOL (PRO)", ln=True)
    for t, d in data["pro"]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 7, f"[*] {t}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 5, f"Target: {d}", ln=True); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "HOME WEAPONS", ln=True)
    for w, y in data["home"]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 7, f"[+] {w}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 5, f"Why: {y}", ln=True); pdf.ln(1)

    # PAGE 3: ROUTINE & JOKE
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "RESCUE ROUTINE", ln=True)
    pdf.set_font("Helvetica", size=10)
    ops = f"AM: Cleanse -> {data['home'][0][0]} -> SPF 50+\nPM: Cleanse -> {data['home'][1][0]} -> Barrier Repair."
    pdf.multi_cell(0, 7, txt=clean(ops))

    pdf.ln(20); pdf.set_fill_color(240, 240, 240); pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "FINAL BRO-ROAST:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    final_joke = f"Look, {name}, I'm roasting you because you're too valuable to look like a 'before' photo. Fix it and buy me that house."
    pdf.multi_cell(0, 7, txt=clean(final_joke))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 3. UI ---
with st.form("roast_logic"):
    u_name = st.text_input("Name")
    u_age = st.selectbox("Age", ["18-24", "25-34", "35-44", "45-54", "55+"])
    u_enemy = st.selectbox("Problem", list(SPECIFIC_LOGIC.keys()))
    u_file = st.file_uploader("Selfie", type=['jpg', 'png'])
    submit = st.form_submit_button("GENERATE")

if submit and u_file:
    with st.spinner("Real analysis in progress..."):
        base64_img = base64.b64encode(u_file.read()).decode('utf-8')
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a witty Bro-Roast comedian. IMPORTANT: Compare the User's photo with their chosen problem. If they choose 'Redness' but the photo is clear, call out their lie. Be cynical but scientific. Max 100 words."},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Name: {u_name}, Chosen Problem: {u_enemy}. Roast my skin based ONLY on what you see in the photo."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]}
            ]
        )
        roast = response.choices[0].message.content
        st.write(roast)
        pdf_p = create_pdf(u_name, u_age, u_enemy, roast, "Current Routine")
        with open(pdf_p, "rb") as f:
            st.download_button("Download Plan", f, file_name="Roast.pdf")
