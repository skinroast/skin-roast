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
# Замени на свою ссылку из Patreon
PATREON_LINK = "https://www.patreon.com/твоя_ссылка" 

# --- 2. МЕДИЦИНСКАЯ МАТРИЦА (HARDCODED LOGIC) ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {
        "ingredients": "Salicylic Acid (BHA), Zinc, Niacinamide",
        "procedures": "Professional Deep Cleaning, Chemical Peels (Jessner), IPL Therapy",
        "why_ing": "Dissolves oil and kills bacteria.",
        "why_proc": "Clears clogged pores mechanically."
    },
    "Wrinkles / Aging": {
        "ingredients": "Retinol (Vitamin A), Peptides, Vitamin C",
        "procedures": "Botox Injections, Biorevitalization, RF-Lifting",
        "why_ing": "Boosts collagen production overnight.",
        "why_proc": "Relaxes muscles and hydrates deeply."
    },
    "Eye Bags / Tired": {
        "ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid",
        "procedures": "Lymphatic Drainage Massage, Microcurrent Therapy",
        "why_ing": "Constricts blood vessels to reduce puffiness.",
        "why_proc": "Physically pushes fluid away from the eyes."
    },
    "Redness": {
        "ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides",
        "procedures": "BBL / IPL Phototherapy (Laser)",
        "why_ing": "Calms inflammation and repairs barrier.",
        "why_proc": "Coagulates visible capillaries."
    },
    "Large Pores": {
        "ingredients": "Retinoids, BHA (Salicylic Acid)",
        "procedures": "Fractional Laser, Chemical Peels",
        "why_ing": "Tightens pore walls and controls sebum.",
        "why_proc": "Resurfaces skin texture."
    },
    "Post-Acne / Scars": {
        "ingredients": "Vitamin C, Azelaic Acid, AHA Acids",
        "procedures": "Microneedling (Dermapen), Laser Resurfacing, Medium Peels",
        "why_ing": "Brightens spots and speeds up cell turnover.",
        "why_proc": "Stimulates deep tissue repair to level out scars."
    }
}

# --- 3. ГЕНЕРАТОР PDF ---
def clean_text(text):
    """
    Ультимативная очистка текста для FPDF. 
    Заменяет юникод на ASCII аналоги и убирает всё, что не влазит в latin-1.
    """
    if isinstance(text, str):
        # Словарь замен для «умных» символов GPT
        replacements = {
            '\u2018': "'", '\u2019': "'", # Одинарные кавычки
            '\u201c': '"', '\u201d': '"', # Двойные кавычки
            '\u2013': '-', '\u2014': '-', # Тире
            '\u2026': '...',             # Многоточие
            '’': "'", '‘': "'", '“': '"', '”': '"', '—': '-'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # Кодируем в latin-1, заменяя неизвестные символы на '?' чтобы не было вылета
        return text.encode('latin-1', 'replace').decode('latin-1')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page 1: Roast & Clinical Analysis
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, clean_text(data['header']), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "1. THE ROAST:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data['roast']))

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "2. CLINICAL PHOTO ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data['clinical_analysis']))

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "3. ADDITIONAL FINDINGS:", ln=True)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 7, txt=clean_text(data['hidden_findings']))

    # Page 2: Clinical Protocol & Ingredients
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "4. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data['clinical_protocol']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc['description'])); pdf.ln(2)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "5. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data['home_weapons']:
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon['name'])}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon['explanation'])); pdf.ln(2)

    # Page 3: Routine
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 15, "6. DETAILED ROUTINE (HOW-TO)", ln=True, align='C')
    
    pdf.set_font("Helvetica", 'B', 13); pdf.cell(0, 10, "MORNING / УТРО:", ln=True)
    pdf.set_font("Helvetica", size=11)
    for step in data['morning_routine']:
        pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}")
        pdf.ln(1)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 13); pdf.cell(0, 10, "EVENING / ВЕЧЕР:", ln=True)
    pdf.set_font("Helvetica", size=11)
    for step in data['evening_routine']:
        pdf.multi_cell(0, 7, txt=f"- {clean_text(step)}")
        pdf.ln(1)

    # Page 4: Final
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12)
    pdf.multi_cell(0, 8, txt=clean_text(data['final_joke']), align='C')

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 11); pdf.set_text_color(200, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data['monetization']), align='C')
    pdf.cell(0, 10, "CLICK HERE FOR THE SHOPPING LIST", ln=True, align='C', link=UPSELL_URL)

    pdf.ln(20); pdf.set_text_color(100, 100, 100); pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(0, 5, txt=clean_text(data['disclaimers']), align='C')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI / LOGIC ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    # LENDING
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem; margin-bottom: 25px;">⚠️ <b>HONEST WARNING:</b> Saving for a Jaguar E-Type. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
    try:
        st.image("scan_face.png", use_column_width=True)
    except:
        st.info("🖼 scan_face.png missing.")
    
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)

else:
    st.title("🔥 Skin Roast AI")
    with st.form("roast_logic"):
        u_name = st.text_input("Your Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Enemy", list(TREATMENT_LOGIC.keys()))
        u_sins = st.multiselect("Naughty List", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("AI is executing clinical scan..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                mega_prompt = f"""
                You are a dual-role expert: A World-Class Clinical Dermatologist and a sharp Roast Comedian.
                Analyze the user and return a JSON report.
                {{
                  "header": "Разбор состояния кожи {u_name}",
                  "roast": "4-5 sentences of witty, cynical 'Bro Roast' about skin neglect and lifestyle sins ({u_sins}). No insults.",
                  "clinical_analysis": "Minimum 6 sentences. Deep medical analysis of the photo: skin type (oily, dry, aging), texture, barrier function. Serious tone.",
                  "hidden_findings": "2-3 other issues detected on the photo besides {u_enemy}.",
                  "clinical_protocol": [
                      {{"name": "Procedure", "description": "2-3 sentences on action and results."}}
                  ],
                  "home_weapons": [
                      {{"name": "Active Ingredient", "explanation": "2-3 sentences on molecular action for this user."}}
                  ],
                  "morning_routine": ["Step with detail & technique", "Step with detail & technique"],
                  "evening_routine": ["Step with detail & technique", "Step with detail & technique"],
                  "disclaimers": "Medical disclaimer: Informational only, consult a doctor.",
                  "final_joke": "One final inspiring but sharp joke.",
                  "monetization": "Message about searching for free vs buying our $5 curated list to help my Jaguar fund."
                }}
                Use these for recommendations: {logic['ingredients']} and {logic['procedures']}.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": mega_prompt},
                        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}]}
                    ]
                )
                
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e:
                st.error(f"Error: {e}")
