import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
PATREON_LINK = "https://www.patreon.com/your_link" 

# --- 2. МЕДИЦИНСКАЯ МАТРИЦА ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Chemical Peels, IPL Therapy"},
    "Wrinkles / Aging": {"ingredients": "Retinol, Peptides, Vitamin C", "procedures": "Botox, RF-Lifting"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea, Hyaluronic Acid", "procedures": "Microcurrents"},
    "Redness": {"ingredients": "Cica, Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy"},
    "Large Pores": {"ingredients": "Retinoids, BHA", "procedures": "Fractional Laser"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA", "procedures": "Microneedling, Laser Resurfacing"}
}

# --- 3. ГЕНЕРАТОР PDF ---
def clean_text(text):
    """Ультимативный фикс: заменяет спецсимволы и удаляет то, что не влазит в PDF"""
    if isinstance(text, str):
        replacements = {
            '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
            '\u2013': '-', '\u2014': '-', '\u2026': '...', '’': "'", '—': '-'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        # Удаляем любые не-ASCII символы (включая кириллицу), чтобы PDF не падал
        return text.encode('ascii', 'ignore').decode('ascii')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # СТРАНИЦА 1: Анализ
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, clean_text(data['header']), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "1. THE ROAST:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data['roast']))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "2. CLINICAL ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=clean_text(data['clinical_analysis']))

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "3. ADDITIONAL FINDINGS:", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.multi_cell(0, 7, txt=clean_text(data['hidden_findings']))

    # СТРАНИЦА 2: Протокол и Оружие
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. CLINICAL PROTOCOL", ln=True)
    for proc in data['clinical_protocol']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc['description'])); pdf.ln(2)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. YOUR HOME WEAPONS", ln=True)
    for weapon in data['home_weapons']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon['explanation'])); pdf.ln(2)

    # СТРАНИЦА 3: Рутина
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "6. DETAILED ROUTINE", ln=True, align='C')
    for step in data['detailed_routine']:
        pdf.set_font("Helvetica", size=11); pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}"); pdf.ln(2)

    # СТРАНИЦА 4: Финал
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data['final_joke']), align='C')
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(200, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data['monetization']), align='C')
    pdf.ln(10); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data['disclaimers']), align='C')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
if query_params.get("paid") != "true":
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace;">⚠️ Saving for a Jaguar. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
    st.title("YOUR MIRROR LIES. AI DOESN'T.")
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary")
else:
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic"):
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Enemy", list(TREATMENT_LOGIC.keys()))
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "No Sleep", "Junk Food", "Stress", "No SPF"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing deep clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a world-class clinical dermatologist and roast comedian.
                Create a premium report in JSON format for {u_name}.
                1. header: "Skin Analysis for {u_name}"
                2. roast: 4-5 cynical sentences about life choices ({u_sins}).
                3. clinical_analysis: Min 6 sentences. Medical deep dive into texture, barrier, and type. No jokes.
                4. hidden_findings: 2-3 other issues detected on photo.
                5. clinical_protocol: 2 professional procedures (from {logic['procedures']}) with descriptions.
                6. home_weapons: 3 actives (from {logic['ingredients']}) with molecular explanations.
                7. detailed_routine: List of steps with technique (e.g. rub in hands, massage 1 min).
                8. disclaimers: Medical disclaimer.
                9. final_joke: Inspiring cynical joke.
                10. monetization: Search for free or buy our list for $5 to help fund my Jaguar.
                """

                response = client.chat.completions.create(
                    model="gpt-4o", response_format={ "type": "json_object" },
                    messages=[{"role": "system", "content": mega_prompt},
                              {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}]}]
                )
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e: st.error(f"Error: {e}")
