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

# --- 2. LOGIC MATRIX ---
TREATMENT_LOGIC = {
    "Acne / Pimples": {"ingredients": "Salicylic Acid, Zinc, Niacinamide", "procedures": "Professional Deep Cleaning, IPL Therapy, Chemical Peels"},
    "Wrinkles / Aging": {"ingredients": "Retinol (Vitamin A), Peptides, Vitamin C", "procedures": "Botox Injections, RF-Lifting, Biorevitalization"},
    "Eye Bags / Tired": {"ingredients": "Caffeine, Green Tea Extract, Hyaluronic Acid", "procedures": "Microcurrent Therapy, Lymphatic Drainage, Eye Peels"},
    "Redness": {"ingredients": "Centella Asiatica (Cica), Azelaic Acid, Ceramides", "procedures": "BBL Phototherapy, Soothing Mask"},
    "Large Pores": {"ingredients": "Retinoids, BHA (Salicylic Acid), Niacinamide", "procedures": "Fractional Laser, Carbon Peel, Microneedling"},
    "Post-Acne / Scars": {"ingredients": "Vitamin C, Azelaic Acid, AHA (Glycolic)", "procedures": "Microneedling (Dermapen), Laser Resurfacing, Medium Peels"}
}

# --- 3. UTILS ---
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
    
    # PAGE 1: ROAST & PHOTO ANALYSIS
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 22)
    pdf.cell(0, 15, clean_text(data.get('header', 'Skin Audit')).upper(), ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 14); pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 10, "1. THE REALITY CHECK (VIBE CHECK):", ln=True)
    pdf.set_font("Helvetica", 'I', 11); pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('roast', '')))
    pdf.ln(5); pdf.line(10, pdf.get_y(), 200, pdf.get_y()); pdf.ln(5)

    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "2. CLINICAL PHOTO-ANALYSIS:", ln=True)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('clinical_analysis', '')))
    pdf.ln(5)

    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "3. HIDDEN FINDINGS (DETECTED BY AI):", ln=True, fill=True)
    pdf.set_font("Helvetica", 'I', 11)
    pdf.multi_cell(0, 7, txt=clean_text(data.get('hidden_findings', '')))

    # PAGE 2: PROCEDURES & ACTIVES
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "4. CLINICAL PROTOCOL (PRO LEVEL)", ln=True)
    for proc in data.get('clinical_protocol', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[*] {clean_text(proc.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(proc.get('description'))); pdf.ln(4)

    pdf.ln(5); pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "5. YOUR HOME WEAPONS (ACTIVES)", ln=True)
    for weapon in data.get('home_weapons', []):
        pdf.set_font("Helvetica", 'B', 11); pdf.cell(0, 8, f"[+] {clean_text(weapon.get('name'))}", ln=True)
        pdf.set_font("Helvetica", size=10); pdf.multi_cell(0, 6, txt=clean_text(weapon.get('explanation')))
        pdf.set_font("Helvetica", 'B', 9); pdf.set_text_color(150, 0, 0)
        pdf.multi_cell(0, 5, txt=f"WARNING: {clean_text(weapon.get('safety_warning'))}")
        pdf.set_text_color(0, 0, 0); pdf.ln(4)

    # PAGE 3: ROUTINE (BORDERED)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(0, 15, "6. THE SEALING PROTOCOL (DAILY OPS)", ln=True, align='C')
    pdf.set_line_width(0.5); pdf.rect(10, 30, 190, 170)
    pdf.set_xy(15, 35)
    pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "MORNING / AM OPERATION:", ln=True)
    for step in data.get('morning_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 7, txt=f"- {clean_text(step)}"); pdf.ln(3)
    pdf.ln(5); pdf.set_x(15); pdf.set_font("Helvetica", 'B', 12); pdf.cell(0, 10, "EVENING / PM OPERATION:", ln=True)
    for step in data.get('evening_routine', []):
        pdf.set_x(15); pdf.set_font("Helvetica", size=10); pdf.multi_cell(180, 7, txt=f"- {clean_text(step)}"); pdf.ln(3)

    # PAGE 4: FINAL
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14); pdf.cell(0, 15, "FINAL WORD", ln=True, align='C')
    pdf.set_font("Helvetica", 'I', 12); pdf.multi_cell(0, 8, txt=clean_text(data.get('final_joke', '')), align='C')
    pdf.ln(10); pdf.set_text_color(200, 0, 0); pdf.set_font("Helvetica", 'B', 12); pdf.multi_cell(0, 7, txt=clean_text(data.get('monetization', '')), align='C')
    pdf.cell(0, 10, ">>> GET THE SHOPPING LIST ($5) <<<", ln=True, align='C', link=UPSELL_URL)
    pdf.ln(10); pdf.set_text_color(0, 0, 0); pdf.set_font("Helvetica", 'B', 10); pdf.cell(0, 10, "AI ACCURACY NOTICE:", ln=True)
    pdf.set_font("Helvetica", size=8); pdf.multi_cell(0, 4, txt=clean_text(data.get('medical_notice', '')))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name); return tmp.name

# --- 4. UI ---
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    st.markdown('<h1 style="text-align: center;">YOUR MIRROR LIES. AI DOESN\'T.</h1>', unsafe_allow_html=True)
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
else:
    st.title("🔥 Skin Roast AI")
    with st.form(key="final_roast_form"):
        u_name = st.text_input("Name")
        u_age = st.selectbox("Age", ["18-24", "25-34", "35-44", "45-54", "55+"])
        u_enemy = st.selectbox("Complaint", list(TREATMENT_LOGIC.keys()))
        u_routine = st.selectbox("Routine", ["Water only", "Bar Soap", "Basic", "Full Protocol"])
        u_sins = st.multiselect("Sins", ["Smoking", "Alcohol", "Sugar", "No SPF", "No Sleep"])
        u_file = st.file_uploader("Selfie", type=['jpg', 'png', 'jpeg'])
        submit = st.form_submit_button("GENERATE REPORT")

    if submit and u_file and u_name:
        with st.spinner("Analyzing..."):
            try:
                base64_img = base64.b64encode(u_file.read()).decode('utf-8')
                logic = TREATMENT_LOGIC[u_enemy]
                prompt = (
                    "Cynical dermatologist AI (Dr. House style). User: {n}, Age: {a}, Sins: {s}, Logic: {l}. "
                    "Analyze the photo deeply. Return JSON: "
                    "{{ \"header\": \"...\", \"roast\": \"Brutal 8-sentence roast\", \"clinical_analysis\": \"15-sentence deep dive based on photo markers\", "
                    "\"hidden_findings\": \"3 specific issues found on photo\", \"clinical_protocol\": [ {{ \"name\": \"...\", \"description\": \"4 sentences\" }} ], "
                    "\"home_weapons\": [ {{ \"name\": \"...\", \"explanation\": \"3 sentences\", \"safety_warning\": \"...\" }} ], "
                    "\"morning_routine\": [\"Step with technique\"], \"evening_routine\": [\"Step with technique\"], "
                    "\"final_joke\": \"...\", \"monetization\": \"Jaguar pitch\", \"medical_notice\": \"AI accuracy notice...\" }}"
                ).format(n=u_name, a=u_age, s=u_sins, l=logic)

                response = client.chat.completions.create(
                    model="gpt-4o", response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}]}
                    ]
                )
                report_data = json.loads(response.choices[0].message.content)
                pdf_path = create_premium_pdf(report_data)
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇️ DOWNLOAD 4-PAGE REPORT", f, file_name=f"SkinRoast_{u_name}.pdf")
            except Exception as e:
                st.error(f"Error: {e}")
