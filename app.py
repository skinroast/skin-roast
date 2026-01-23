import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# Custom CSS for the "Lazy Millionaire" vibe
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #D32F2F; color: white; }
    .report-box { padding: 20px; border: 1px solid #FF4B2B; border-radius: 10px; background-color: #1E1E1E; }
    </style>
""", unsafe_allow_html=True)

# Visual goal tracker
GOAL = 6150000 
CURRENT = 260 

# --- 2. AUTHENTICATION ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing in Secrets.")

# Links for monetization
PAYMENT_URL = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# --- 3. HARDCODED MEDICAL LOGIC ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ing": "Salicylic Acid, Zinc", "why": "Dissolves oil and kills bacteria."},
    "Wrinkles / Aging": {"ing": "Retinol, Peptides", "why": "Boosts collagen production overnight."},
    "Eye Bags / Tired": {"ing": "Caffeine, Green Tea Extract", "why": "Constricts blood vessels to reduce puffiness."},
    "Large Pores": {"ing": "Niacinamide, BHA", "why": "Refines skin texture and clears debris."}
}

# --- 4. FUNCTIONS ---
def analyze_face(image_file, user_data):
    encoded_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    
    # Ton of Voice: Hard Bro / Hard Coach
    system_msg = "You are a clinical but cynical dermatologist. Use male metaphors. Provide a roast and treatment plan in JSON."
    prompt = f"Name: {user_data['name']}, Age: {user_data['age']}, Problem: {user_data['problem']}, Habits: {user_data['habits']}. Logic: {TREATMENT_LOGIC.get(user_data['problem'])}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Scan Failed: {e}")
        return None

def generate_pdf(data, name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, f"{name.upper()}'S SKIN DOSSIER", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VERDICT (ROAST):", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, txt=data.get('roast_intro', 'Analysis missing.'))
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, "Deep scan found 3 critical hidden issues. Unlock full audit for $5.", ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 5. UI FLOW ---
st.title("SKIN ROAST AI 🔥")
st.markdown(f"**House Fund Goal:** ${CURRENT} of ${GOAL:,}")
st.progress(CURRENT / GOAL)

is_paid = st.query_params.get("paid") == "true"

if not is_paid:
    # Landing Page logic
    st.image("https://via.placeholder.com/600x300?text=YOUR+MIRROR+LIES") 
    st.subheader("Your mirror lies. AI doesn't.")
    st.write("Get a brutally honest analysis of your skin health and a plan to fix it.")
    st.link_button("UNLOCK MY ROAST ($10)", PAYMENT_URL, type="primary")
else:
    # App logic after payment
    st.success("Payment Verified. Let's look at the damage.")
    
    with st.form("dossier_form"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["Under 25", "25-34", "35-44", "45+"])
        u_enemy = st.selectbox("Main Enemy", list(TREATMENT_LOGIC.keys()))
        u_sins = st.multiselect("Naughty List", ["Smoking", "Alcohol", "Sugar", "No Sleep", "No Sunscreen"])
        u_file = st.file_uploader("Upload Selfie (No Filters!)", type=['jpg', 'png'])
        submit = st.form_submit_button("GENERATE ROAST")

    if submit:
        if u_file and u_name:
            with st.spinner("AI is judging your life choices..."):
                result = analyze_face(u_file, {"name": u_name, "age": u_age, "problem": u_enemy, "habits": u_sins})
                if result:
                    st.markdown("### The Verdict")
                    st.error(result.get('roast_intro'))
                    
                    report_path = generate_pdf(result, u_name)
                    with open(report_path, "rb") as f:
                        st.download_button("⬇️ DOWNLOAD FULL PDF REPORT", f, f"{u_name}_Skin_Roast.pdf")
