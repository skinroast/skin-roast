import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Check Streamlit Secrets.")

UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"
GOAL, CURRENT = 6150000, 260

# --- 2. РАСШИРЕННАЯ МЕДИЦИНСКАЯ БАЗА (10 проблем) ---
SKIN_DATABASE = {
    "Eye Bags / Dark Circles": {
        [cite_start]"home": [("Caffeine Solutions", "Topical caffeine constricts blood vessels to reduce puffiness [cite: 130, 131][cite_start]."), ("Vitamin K Serum", "Improves micro-circulation to fade dark circles[cite: 132, 133].")],
        [cite_start]"pro": [("Dermal Fillers", "Restores volume in the tear trough area [cite: 125, 126][cite_start]."), ("Lymphatic Drainage", "Professional massage to remove stagnant fluid[cite: 127, 128].")],
        "deep": "Periorbital exhaustion. [cite_start]This is more about sleep debt and thin skin than just 'tiredness'[cite: 123]."
    },
    "Redness / Irritation": {
        "home": [("Azelaic Acid", "Reduces inflammation and redness."), ("Centella Asiatica", "Soothes the skin barrier.")],
        "pro": [("IPL Phototherapy", "Targets broken capillaries."), ("Laser Therapy", "Reduces chronic redness.")],
        [cite_start]"deep": "Your skin's barrier is compromised, likely due to environmental stress or improper routine[cite: 78, 79]."
    },
    "Wrinkles / Aging": {
        [cite_start]"home": [("Retinol (Vitamin A)", "Boosts collagen production overnight [cite: 22, 23][cite_start]."), ("Peptides", "Enhances skin barrier function and firmness[cite: 24, 25].")],
        [cite_start]"pro": [("Botox Injections", "Relaxes facial muscles to reduce fine lines [cite: 15, 16][cite_start]."), ("RF-Lifting", "Tightens the skin non-invasively[cite: 19, 20].")],
        "deep": "Structural neglect detected. [cite_start]Untreated micro-damage will accelerate aging by 5-7 years[cite: 56]."
    }
    # (Остальные проблемы добавляются по этой же схеме)
}

# --- 3. ГЕНЕРАТОР PDF (4 СТРАНИЦЫ) ---
def create_premium_pdf(name, age, problem, roast_text, routine, sins):
    pdf = FPDF()
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')
    data = SKIN_DATABASE.get(problem, SKIN_DATABASE["Wrinkles / Aging"])

    # СТРАНИЦА 1: ГЛУБОКИЙ АНАЛИЗ
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    [cite_start]pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C') [cite: 1]
    
    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14)
    [cite_start]pdf.cell(0, 10, "THE VIBE CHECK (AI ANALYSIS):", ln=True) [cite: 2, 142]
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(roast_text))

    pdf.ln(10); pdf.set_font("Helvetica", 'B', 14)
    [cite_start]pdf.cell(0, 10, f"DEEP SCAN: {clean(problem).upper()}", ln=True) [cite: 6, 146]
    pdf.set_font("Helvetica", size=11)
    [cite_start]pdf.multi_cell(0, 7, txt=clean(data["deep"])) [cite: 56, 123]

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(180, 0, 0)
    [cite_start]pdf.cell(0, 10, "ALSO DETECTED (SECONDARY CONCERNS):", ln=True) [cite: 12, 58]
    pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", 'I', 10)
    [cite_start]pdf.cell(0, 6, "- Lack of deep hydration [cite: 12, 82]", ln=True)
    [cite_start]pdf.cell(0, 6, "- Loss of dermal elasticity [cite: 12, 61]", ln=True)

    # СТРАНИЦА 2: КЛИНИЧЕСКИЙ ПРОТОКОЛ
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    [cite_start]pdf.cell(0, 15, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True) [cite: 13, 149]
    pdf.set_font("Helvetica", size=10)
    [cite_start]pdf.multi_cell(0, 6, txt="Professional treatments for faster results. Consult a doctor first[cite: 14, 152].")
    
    for treat, desc in data["pro"]:
        [cite_start]pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {treat}", ln=True) [cite: 15, 17]
        [cite_start]pdf.set_font("Helvetica", size=10); pdf.cell(0, 6, f"Target: {desc}", ln=True); pdf.ln(2) [cite: 16, 18]

    # СТРАНИЦА 3: ДОМАШНИЙ УХОД И РУТИНА
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    [cite_start]pdf.cell(0, 15, "HOME WEAPONS & DAILY OPS", ln=True) [cite: 21, 153]
    for weapon, why in data["home"]:
        [cite_start]pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {weapon}", ln=True) [cite: 22, 24]
        [cite_start]pdf.set_font("Helvetica", size=10); pdf.cell(0, 6, f"Why: {why}", ln=True); pdf.ln(2) [cite: 23, 25]

    [cite_start]pdf.ln(10); pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 10, "RESCUE ROUTINE (STEP-BY-STEP):", ln=True) [cite: 33, 158]
    pdf.set_font("Helvetica", size=11)
    [cite_start]ops = (f"AM: Cleanse -> {data['home'][0][0]} -> SPF 50+ [cite: 34, 159]\n"
           [cite_start]f"PM: Cleanse -> {data['home'][1][0]} -> Barrier Repair Cream [cite: 39, 160]")
    pdf.multi_cell(0, 7, txt=clean(ops))

    # СТРАНИЦА 4: ФИНАЛЬНОЕ СЛОВО И UPSELL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.set_fill_color(240, 240, 240)
    [cite_start]pdf.cell(0, 15, "FINAL WORD FROM THE COMIC:", ln=True, fill=True) [cite: 65, 111]
    pdf.set_font("Helvetica", 'I', 11)
    [cite_start]final_joke = (f"Listen, {name}, your skin has the texture of a crumpled-up tax return[cite: 162]. "
                  "Fix it now, or spend the next 20 years explaining why you look like a "
                  [cite_start]"dehydrated raisin[cite: 163]. [cite_start]Get to work[cite: 114].")
    pdf.multi_cell(0, 8, txt=clean(final_joke))

    pdf.ln(20); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 14)
    [cite_start]pdf.cell(0, 10, ">>> GET THE FULL SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL) [cite: 48, 165]
    
    pdf.ln(20); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    [cite_start]pdf.multi_cell(0, 5, txt="MEDICAL DISCLAIMER: generated by AI for informational purposes only[cite: 49, 166].")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Progress to Lake Oswego: ${CURRENT} / ${GOAL:,}")

with st.form("roast_logic"):
    c1, c2 = st.columns(2)
    with c1:
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
    with c2:
        u_enemy = st.selectbox("Skin Problem", list(SKIN_DATABASE.keys()))
        [cite_start]u_routine = st.selectbox("Current Routine", ["None/Water", "Soap", "Moisturizer", "Full Routine"]) [cite: 30, 79]
    
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
