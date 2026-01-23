import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import base64

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Skin Roast AI", page_icon="🔥", layout="centered")

# Visual goal tracker from your strategy [cite: 47, 51]
GOAL = 6150000 
CURRENT = 260 

# --- 2. AUTHENTICATION ---
if "OPENAI_API_KEY" in st.secrets:
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key missing. Add it to Streamlit Secrets.")

# Links for your High Ticket Funnel [cite: 35, 36]
PAYMENT_URL = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_URL = "https://skin-roast.lemonsqueezy.com/upsell"

# --- 3. HARDCODED MEDICAL LOGIC [cite: 16, 37] ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ing": "Salicylic Acid, Zinc", "why": "Kills bacteria and clears oil."},
    "Wrinkles / Aging": {"ing": "Retinol, Peptides", "why": "Rebuilds collagen overnight."},
    "Eye Bags": {"ing": "Caffeine, Hyaluronic Acid", "why": "Reduces puffiness and hydrates."},
    "Redness": {"ing": "Azelaic Acid, Ceramides", "why": "Calms inflammation and repairs barrier."}
}

# --- 4. ENGINE FUNCTIONS ---
def analyze_face(image_file, user_data):
    """Sends face to GPT-4o Vision for a brutal roast[cite: 4, 53]."""
    encoded_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    
    system_msg = "You are a cynical dermatologist/comedian. Analyze the image and provide a brutal roast and clinical plan in JSON format."
    prompt = f"User: {user_data['name']}, Age: {user_data['age']}, Problem: {user_data['problem']}. Logic: {TREATMENT_LOGIC[user_data['problem']]}"

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
        st.error(f"Analysis failed: {e}")
        return None

def generate_pdf(data, name):
    """Generates the PDF report—the main product[cite: 36, 55]."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, f"{name.upper()}'S SKIN DOSSIER", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "THE VERDICT:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, txt=data.get('roast_intro', 'No roast generated.'))
    
    # Information Gap Mechanic: Mention issues but don't solve them yet [cite: 42]
    pdf.ln(10)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.cell(0, 10, "Note: Deep scan found 2 other issues. Unlock full audit for $5.", ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# --- 5. INTERFACE ---
st.title("SKIN ROAST AI 🔥")
st.markdown(f"**Goal:** $6.15M for Lake Oswego House & Jaguar E-Type[cite: 47, 120].")
st.progress(CURRENT / GOAL)
st.caption(f"Status: ${CURRENT} raised. Every $10 counts.")

# Logic: Landing vs Paid App [cite: 108, 151]
is_paid = st.query_params.get("paid") == "true"

if not is_paid:
    st.subheader("Your mirror lies. AI doesn't. ")
    st.write("Get a brutally honest analysis of your face and a plan to fix it. [cite: 131]")
    st.image("https://via.placeholder.com/600x300?text=AI+DEEP+SCAN+ANALYSIS") # Use scan_face.png here [cite: 128]
    st.link_button("UNLOCK MY ROAST ($10)", PAYMENT_URL, use_container_width=True, type="primary")
else:
    st.success("Access Granted. Let's see the damage. [cite: 160]")
    
    with st.expander("1. The Dossier", expanded=True):
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age Group", ["Under 25", "25-35", "35-45", "45+"])
        u_enemy = st.selectbox("Focus Problem", list(TREATMENT_LOGIC.keys()))
        u_sins = st.multiselect("Naughty List", ["Smoking", "Sugar", "No Sleep", "Stress"]) [cite: 168]
        
    u_file = st.file_uploader("Upload Selfie (No Filters!)", type=['jpg', 'png']) [cite: 174]

    if st.button("GENERATE ROAST & ROUTINE"):
        if u_file and u_name:
            with st.spinner("AI is judging your life choices... [cite: 178]"):
                result = analyze_face(u_file, {"name": u_name, "age": u_age, "problem": u_enemy})
                if result:
                    report_path = generate_pdf(result, u_name)
                    with open(report_path, "rb") as f:
                        st.download_button("⬇️ DOWNLOAD PDF REPORT", f, "Skin_Roast.pdf")
                    st.info("Ready to buy the exact brands I recommend? [cite: 40]")
                    st.link_button("GET THE SHOPPING LIST ($5)", UPSELL_URL)
        else:
            st.error("Name and Photo are mandatory.")
