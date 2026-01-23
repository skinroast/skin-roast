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
def create_pdf_report(name, age, problem, roast_text):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Helvetica", 'B', 24)
    pdf.cell(0, 20, f"OFFICIAL SKIN DOSSIER: {name.upper()}", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 5, f"Subject Age Group: {age} | Target Issue: {problem}", ln=True, align='C')
    
    # The Roast
    pdf.ln(15)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 10, "THE ROAST (TRUTH HURTS):", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, txt=roast_text.encode('latin-1', 'ignore').decode('latin-1'))
    
    # The Solution
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "THE RESCUE PLAN:", ln=True)
    pdf.set_font("Helvetica", size=12)
    advice = SKIN_DATABASE.get(problem, "Basic hygiene. Start there.")
    pdf.multi_cell(0, 8, txt=f"Strategy: {advice}\n\nRoutine:\nAM: Cleanse -> Target Serum -> SPF 50+\nPM: Cleanse -> Treatment -> Heavy Moisturizer")

    # The Final Joke (Hard but Motivating)
    pdf.ln(20)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "A FINAL WORD FROM THE COMIC:", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    
    final_joke = (
        f"Look, {name}, I've seen better complexions on a 2,000-year-old mummy, but at least they have "
        "the excuse of being dead. You're still here. Your face isn't a lost cause—it's just a "
        "fixer-upper. You wouldn't let your car rust into the ground, so stop doing it to your "
        "only head. Apply the cream, drink some water, and maybe—just maybe—one day people "
        "will look at you without wondering if you've been living in a cave. Now go fix it."
    )
    pdf.multi_cell(0, 7, txt=final_joke.encode('latin-1', 'ignore').decode('latin-1'))
    
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
