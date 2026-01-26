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
PATREON_LINK = "https://www.patreon.com/your_link_here"

# --- 2. МЕДИЦИНСКАЯ МАТРИЦА ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Professional Deep Cleaning, IPL Therapy, Chemical Peels"},
    "Wrinkles / Aging": {"ingredients": "Retinol (Vitamin A), Peptides, Vitamin C", "procedures": "Botox Injections, RF-Lifting, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid", "procedures": "Microcurrent Therapy, Lymphatic Drainage, Eye Peels"},
    "Redness": {"ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask"},
    "Large Pores": {"ingredients": "Retinoids, BHA (Salicylic Acid), Niacinamide", "procedures": "Fractional Laser, Carbon Peel, Microneedling"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA (Glycolic)", "procedures": "Microneedling (Dermapen), Laser Resurfacing, Medium Peels"}
}

# --- 3. ГЕНЕРАТОР PDF ---
def clean_text(text):
    if isinstance(text, str):
        replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-'}
        for char, rep in replacements.items():
            text = text.replace(char, rep)
        return text.encode('ascii', 'ignore').decode('ascii')
    return str(text)

def create_premium_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: ANALYSIS & ROAST
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Audit')).upper(), ln=True, align='C')
    pdf.ln(5)
    
    # 1. ROAST
    pdf.set_font("Helvetica", 'B', 14); pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)

    # 2. ANALYSIS
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "2. CLINICAL PHOTO-ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))
    pdf.ln(5)

    # 3. HIDDEN FINDINGS
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "3. HIDDEN FINDINGS (DETECTED BY AI):", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('hidden_findings', '')))
    
    # Дальше идут остальные страницы... (3. CLINICAL PROTOCOL и т.д.)
    # PAGE 4: FINAL WORD
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD FROM THE COACH", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    pdf.ln(10); pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "SAFETY DISCLAIMER:", ln=True)
    pdf.set_font("Helvetica", size=8); pdf.multi_cell(0, 4, txt=clean_text(data.get('safety_disclaimer', '')))
    pdf.ln(5); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "MEDICAL NOTICE:", ln=True)
    pdf.set_font("Helvetica", size=8); pdf.multi_cell(0, 4, txt=clean_text(data.get('medical_notice', '')))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<div style="background-color: #2b2d18; color: #e6c957; padding: 20px; border-radius: 10px; border: 1px solid #e6c957; font-family: monospace; font-size: 0.9rem;">⚠️ HONEST WARNING: Saving for a Jaguar E-Type. $10 analysis helps the dream.</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align: center; background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">YOUR MIRROR LIES.<br>AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
    st.title("🔥 Skin Roast AI")
    with st.form(key="main_roast_form"):
        u_name = st.text_input("First Name")
        u_age = st.selectbox("Age Group", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Main Complaint", list(TREATMENT_LOGIC.keys()))
        u_routine = st.selectbox("Current Operations", ["Water only", "Bar Soap", "Basic Moisturizer", "Full Protocol"])
        u_sins = st.multiselect("Lifestyle Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Upload Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE PREMIUM REPORT")

    if submit and u_file and u_name:
        with st.spinner("Executing clinical scan..."):
            try:
                # 1. Подготовка данных
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                
                # 2. Промпт с усиленным анализом фото и скрытыми находками
              raw_prompt = """
                You are a cynical, elite clinical dermatologist. Your vibe: Dr. House meets a Stand-up Roast. 
                Generate a premium 4-page report in JSON for {name}, age {age}.
                Current routine: {routine}. Lifestyle sins: {sins}. Focus on {enemy}.
                
                STRICT CONTENT RULES:
                1. THE REALITY CHECK: Brutal, cinematic 6-8 sentence roast. Use a dark metaphor for {sins}. 
                   Treat their skin like a "crime scene" or a "crumbling architectural disaster". No sugar-coating.
                2. CLINICAL ANALYSIS: 12-15 sentences. Deep-dive into epidermal atrophy and collagen destruction. 
                   Link their sins directly to what you see on the photo (e.g., "I see the sugar crystals screaming in your dermal matrix").
                3. HIDDEN FINDINGS: Find 3 sneaky issues NOT mentioned by the user. Be specific.
                4. CLINICAL PROTOCOL: 3 procedures from: {proc_list}. 4 sentences for each on cellular mechanism.
                5. HOME WEAPONS: 3 actives from: {ing_list}. 3 sentences + RED warning for each.
                6. DETAILED ROUTINE: Every step MUST have 3-4 sentences of specific technique (massage, angles, wait times).
                7. MONETIZATION: Cynical pitch about the $5 list for your Jaguar E-Type V12 fund.

                STRICT JSON STRUCTURE:
                {{
                  "header": "ULTIMATE DERMAL AUDIT: {name}",
                  "roast": "Actual dark roast here", 
                  "clinical_analysis": "Long medical deep-dive",
                  "hidden_findings": "Detailed hidden issues",
                  "clinical_protocol": [ {{ "name": "...", "description": "..." }} ],
                  "home_weapons": [ {{ "name": "...", "explanation": "...", "safety_warning": "..." }} ],
                  "morning_routine": ["Step with technique", "Step...", "Step..."],
                  "evening_routine": ["Step with technique", "Step...", "Step..."],
                  "safety_disclaimer": "...", "medical_notice": "...", "final_joke": "...", "monetization": "..."
                }}
                """
                mega_prompt = raw_prompt.format(
                    name=u_name, 
                    age=u_age, 
                    routine=u_routine, 
                    sins=u_sins, 
                    enemy=u_enemy, 
                    proc_list=logic['procedures'], 
                    ing_list=logic['ingredients']
                )

                # 3. Запрос к API
                response = client.chat.completions.create(
                    model="gpt-4o", 
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": mega_prompt},
                        {"role": "user", "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                        ]}
                    ]
                )
                
                raw_content = response.choices[0].message.content
                
                # 4. Проверка и генерация PDF
                if not raw_content:
                    st.error("AI returned an empty response. Try again.")
                else:
                    report_data = json.loads(raw_content)
                    pdf_path = create_premium_pdf(report_data)
                    with open(pdf_path, "rb") as f:
                        st.download_button("⬇️ DOWNLOAD 4-PAGE CUSTOM PLAN", f, file_name=f"SkinRoast_{u_name}.pdf")
            
            except Exception as e:
                # Этот блок теперь стоит строго под 'try'
                st.error(f"Critical Error: {e}")
