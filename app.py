import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. CONFIG ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# --- 2. МЕДИЦИНСКАЯ БАЗА (10 проблем) ---
SKIN_DATABASE = {
    "Eye Bags / Dark Circles": {
        "home": [("Caffeine Solutions", "Topical caffeine constricts blood vessels to reduce puffiness."), ("Vitamin K Serum", "Improves micro-circulation to fade dark circles.")],
        "pro": [("Dermal Fillers", "Restores volume in the tear trough area."), ("Lymphatic Drainage", "Professional massage to remove stagnant fluid.")],
        "deep": "Periorbital exhaustion. This is more about sleep debt and thin skin than just 'tiredness'."
    },
    "Wrinkles / Aging": {
        "home": [("Retinol (Vitamin A)", "Boosts collagen production overnight."), ("Peptides", "Enhances skin barrier function and firmness.")],
        "pro": [("Botox Injections", "Relaxes facial muscles to reduce fine lines."), ("RF-Lifting", "Tightens the skin non-invasively.")],
        "deep": "Structural neglect detected. Untreated micro-damage will accelerate aging by 5-7 years."
    },
    "Large Pores": {
        "home": [("Retinoids", "Pore shrinking and oil control."), ("BHA (Salicylic Acid)", "Deep pore texture refinement.")],
        "pro": [("Fractional Laser", "Professional skin resurfacing."), ("Chemical Peels", "Deep exfoliation to clear debris.")],
        "deep": "Pore structural instability often linked to excess sebum and loss of elasticity."
    }
    # Добавьте остальные 7 по аналогии
}

# --- 3. ГЕНЕРАТОР PDF (4 СТРАНИЦЫ) ---
def create_premium_pdf(name, age, problem, roast_text, routine, sins):
    pdf = FPDF()
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')
    data = SKIN_DATABASE.get(problem, SKIN_DATABASE["Wrinkles / Aging"])

    # СТРАНИЦА 1: ГЛУБОКИЙ АНАЛИЗ
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK (AI PHOTO ANALYSIS):", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(roast_text))

    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean(problem).upper()}", ln=True)
    pdf.set_font("Helvetica", size=11)
    scan_details = f"{data['deep']} At {age}, combined with habits like {', '.join(sins)}, the risk of permanent damage is elevated."
    pdf.multi_cell(0, 7, txt=clean(scan_details))

    # СТРАНИЦА 2: КЛИНИЧЕСКИЙ ПРОТОКОЛ
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="Consult a licensed dermatologist before these treatments for faster results.")
    
    for treat, desc in data["pro"]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {treat}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 6, f"Target: {desc}", ln=True); pdf.ln(2)

    # СТРАНИЦА 3: ДОМАШНИЙ УХОД И РУТИНА
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 15, "HOME WEAPONS & DAILY OPS", ln=True)
    for weapon, why in data["home"]:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {weapon}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.cell(0, 6, f"Why: {why}", ln=True); pdf.ln(2)

    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "DAILY OPS (STEP-BY-STEP):", ln=True)
    pdf.set_font("Helvetica", size=11)
    ops = (f"AM: Cleanse -> {data['home'][0][0]} -> SPF 50+\n"
           f"PM: Cleanse -> {data['home'][1][0]} -> Barrier Repair Cream")
    pdf.multi_cell(0, 7, txt=clean(ops))

    # СТРАНИЦА 4: ФИНАЛЬНОЕ СЛОВО
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 15, "FINAL WORD FROM THE COMIC:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    final_joke = (f"Listen, {name}, your skin has the texture of a crumpled-up tax return. "
                  "Fix it now, or spend the next 20 years explaining why you look like a "
                  "dehydrated raisin. Get to work.")
    pdf.multi_cell(0, 8, txt=clean(final_joke))

    pdf.ln(20); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, ">>> GET THE FULL SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    
    pdf.ln(20); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt="MEDICAL DISCLAIMER: generated by AI for informational purposes only.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. ИНТЕРФЕЙС ---
st.title("SKIN ROAST AI 🔥")

with st.form("roast_logic"):
    c1, c2 = st.columns(2)
    with c1:
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
    with c2:
        u_enemy = st.selectbox("Skin Problem", list(SKIN_DATABASE.keys()))
        u_routine = st.selectbox("Current Routine", ["None/Water", "Soap", "Moisturizer", "Full Routine"])
    
    u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "No Sleep", "Junk Food", "Stress", "No SPF"])
    u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button("GENERATE PREMIUM REPORT")

if submit and u_file and u_name:
    with st.spinner("Executing deep AI scan..."):
        try:
            base64_img = base64.b64encode(u_file.read()).decode('utf-8')
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a witty Bro-Roast comedian. Analyze the photo vs the chosen problem. If they choose 'Redness' but the photo is clear, tease them. Max 100 words. Be sharp, not offensive."},
                    {"role": "user", "content": [
                        {"type": "text", "text": f"Name: {u_name}, Age: {u_age}, Goal: {u_enemy}. Analyze me."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]}
                ]
            )
            roast = response.choices[0].message.content
            st.success("Analysis Complete.")
            
            pdf_path = create_premium_pdf(u_name, u_age, u_enemy, roast, u_routine, u_sins)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
        except Exception as e:
            st.error(f"Error: {e}")
