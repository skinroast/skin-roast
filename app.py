import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import base64

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# Кастомный CSS для брутального интерфейса
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; border: none; height: 3.5rem; }
    .stSelectbox label, .stMultiSelect label, .stTextInput label { color: #ff4b4b !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Индикатор цели (Дом в Лейк-Освего)
GOAL = 6150000 
CURRENT = 260 

# --- 2. API SETUP ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Add it to Streamlit Secrets.")

# --- 3. CLINICAL DATABASE (Все твои 9 проблем) ---
SKIN_DATABASE = {
    "Acne / Pimples": "Salicylic Acid & Benzoyl Peroxide. Kill the bacteria before it colonizes your whole face.",
    "Wrinkles": "Retinol (0.5%) & Peptides. Start rebuilding the collagen you've wasted.",
    "Dryness": "Hyaluronic Acid & Ceramides. Your face is a desert; let's give it an oasis.",
    "Oily Skin": "Niacinamide & Clay. Stop the oil spill before the EPA gets involved.",
    "Pigmentation": "Vitamin C & Tranexamic Acid. Fading the evidence of sun damage.",
    "Irritation": "Centella Asiatica & Panthenol. Calm the fire before you look like a lobster.",
    "Blackheads": "BHA (Salicylic Acid). Cleaning out the pores you've neglected for years.",
    "Flaking": "Urea & Lactic Acid. Gently removing the dead cells of your past self.",
    "Redness": "Azelaic Acid. Reducing the 'always embarrassed' look."
}

# --- 4. PDF GENERATOR ---
# --- PDF GENERATOR (MATCHING YOUR TEMPLATE) ---
def create_pdf_report(name, age, problem, roast_text):
    pdf = FPDF()
    pdf.add_page()
    
    # helper для очистки текста (чтобы PDF не падал на спецсимволах)
    def clean(t):
        return str(t).encode('latin-1', 'ignore').decode('latin-1')

    # PAGE 1: THE ROAST
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 20, f"{clean(name).upper()}'S UPGRADE PLAN", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VIBE CHECK:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean(roast_text))
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"DEEP SCAN: {clean(problem).upper()}", ln=True)
    pdf.set_font("Helvetica", size=11)
    # Пример расширенного анализа (можно подтягивать из GPT)
    deep_scan = f"The current state of your {problem} suggests a long-term relationship with stress and questionable life choices. It's not a disaster, but it's a fixer-upper."
    pdf.multi_cell(0, 7, txt=clean(deep_scan))

    # PAGE 2: CLINICAL & HOME WEAPONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6, txt="Professional treatments for faster results. Consult a certified doctor first.")
    
    pro_treatments = [
        ("Botox Injections", "Relaxes facial muscles to reduce appearance of wrinkles."),
        ("Biorevitalization", "Hydrates deeply to help restore skin suppleness."),
        ("RF-Lifting", "Non-invasively tightens the skin and reduces fine lines.")
    ]
    for treat, target in pro_treatments:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 7, f"[*] {treat}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 5, f"Target: {target}", ln=True)
        pdf.ln(2)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "YOUR HOME WEAPONS", ln=True)
    
    logic = SKIN_DATABASE.get(problem, "Basic hygiene.")
    weapons = [
        ("Retinol (Vitamin A)", "Boosts collagen production overnight."),
        ("Peptides", "Enhances skin barrier function and firmness."),
        ("Vitamin C", "Brightens skin and promotes collagen production.")
    ]
    for weapon, why in weapons:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(0, 7, f"[+] {weapon}", ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 5, f"Why: {why}", ln=True)
        pdf.ln(2)

    # PAGE 3: SAFETY & DAILY OPERATIONS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, "[!] SAFETY PROTOCOL (READ THIS):", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=10)
    safety_rules = [
        "1. Active ingredients (Retinol, Acids) are powerful. They can burn if misused.",
        "2. ALWAYS use SPF 30+ if you use Retinol or Acids. No excuses.",
        "3. PATCH TEST: Apply a small amount on your neck first.",
        "4. Start slowly: Use Retinol 2 times a week, then increase."
    ]
    pdf.multi_cell(0, 6, txt="\n".join(safety_rules))

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "DAILY OPERATIONS", ln=True)
    pdf.set_font("Helvetica", size=10)
    ops = (
        "MORNING:\n1. Cleanse with a gentle cleanser.\n2. Apply Vitamin C serum.\n3. Moisturize.\n4. SPF 30+.\n\n"
        "EVENING:\n1. Cleanse thoroughly.\n2. Apply Retinol.\n3. Rich moisturizer."
    )
    pdf.multi_cell(0, 6, txt=ops)

    # FINAL ROAST JOKE (THE BRO COMIC STYLE)
    pdf.ln(15)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "HONEST NOTE FROM THE COMIC:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    # Та самая подбадривающая, но жесткая шутка
    final_joke = (
        f"Listen, {name}, right now your face has the texture of a crumpled-up tax return from 2008. "
        "But here's the good news: unlike your crypto portfolio, skin actually has a recovery plan. "
        "I'm roasting you because I care—mostly about my future house—but also because you're too "
        "valuable to look like a background character in a post-apocalyptic movie. Stop using 3-in-1 "
        "body wash on your face, stick to the plan, and let's turn that 'existential dread' glow "
        "into actual skin health. You've got this. Now go wash your face."
    )
    pdf.multi_cell(0, 7, txt=clean(final_joke))

    # Disclaimer
    pdf.ln(10)
    pdf.set_font("Helvetica", size=8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 4, txt="MEDICAL DISCLAIMER: Generated by AI for info only. Not medical advice. Seek a physician.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 5. UI FLOW ---
st.title("SKIN ROAST AI 🔥")
st.progress(CURRENT / GOAL)
st.caption(f"Fundraising for Lake Oswego: ${CURRENT} / ${GOAL:,}")

if st.query_params.get("paid") == "true":
    with st.form("roast_input"):
        col1, col2 = st.columns(2)
        with col1:
            u_name = st.text_input("First Name")
            u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-55", "55+"])
        with col2:
            u_problem = st.selectbox("Main Issue", list(SKIN_DATABASE.keys()))
            u_routine = st.selectbox("Current Routine", ["None", "Water", "Soap", "Basic", "Advanced"])
            
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "Stress", "No Sleep"])
        u_file = st.file_uploader("Upload Evidence (Selfie)", type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("GENERATE BRUTAL ROAST")

    if submit and u_file and u_name:
        with st.spinner("Calculating the level of neglect..."):
            base64_image = base64.b64encode(u_file.read()).decode('utf-8')
            try:
                # Запрос к GPT-4o
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a world-class dermatologist with a side job as a roast comedian. Your humor is dry, cynical, and very 'tech-bro' focused. Be mean but funny. Max 80 words."},
                        {"role": "user", "content": [
                            {"type": "text", "text": f"Name: {u_name}, Age: {u_age}, Sins: {u_sins}, Problem: {u_problem}. Analyze my face and roast me."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ]
                )
                roast = response.choices[0].message.content
                st.subheader("The Verdict:")
                st.write(roast)
                
                pdf_path = create_pdf_report(u_name, u_age, u_problem, roast)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD YOUR RESCUE PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
else:
    st.markdown("### Your mirror is being polite. I won't be.")
    st.link_button("UNLOCK YOUR ANALYSIS ($10)", "https://skin-roast.lemonsqueezy.com/buy", type="primary")
