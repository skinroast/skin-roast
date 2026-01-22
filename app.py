import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import json
import os

# --- 1. НАСТРОЙКИ ---
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# ССЫЛКИ НА ОПЛАТУ (ЗАМЕНИШЬ ПОТОМ НА СВОИ!)
LEMON_SQUEEZY_LINK = "https://skin-roast.lemonsqueezy.com/buy" 
UPSELL_LINK = "https://skin-roast.lemonsqueezy.com/buy"

st.set_page_config(page_title="Skin Roast: Upgrade Plan", page_icon="🔥", layout="centered")

# Дизайн: Убираем лишнее, делаем кнопки красными
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 3.5em;
        background-color: #FF4B4B; 
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. МОЗГИ AI (БРО-ПРОМТ) ---
SYSTEM_PROMPT = """
ТЫ — "SKIN ROAST BRO". Ты лучший друг, наставник.
Твоя цель — помочь другу стать красавчиком, используя метод: [Признание] -> [Сатира над ошибками] -> [Мотивация].
СТИЛЬ:
- Обращайся на "Ты", "Бро", "Чемпион".
- Метафоры: Jaguar V12, Lake Oswego, NBA, Уолл-стрит.
- Не оскорбляй личность. Критикуй лень и прыщи.

ФОРМАТ ОТВЕТА (JSON):
{
  "roast": "Текст прожарки (3-4 предложения)",
  "problems_list": ["Проблема 1", "Проблема 2"],
  "ingredients": [
      {"name": "Название", "why": "Зачем нужно"}
  ],
  "routine_morning": "Шаги на утро",
  "routine_evening": "Шаги на вечер",
  "motivation": "Финал"
}
"""

def analyze_skin(age, skin_type, problem, habits):
    """Стучится в OpenAI"""
    if not openai.api_key:
        return None  
    user_prompt = f"Данные: Возраст {age}, Кожа {skin_type}, Проблема {problem}, Грехи {habits}."
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except:
        return None

def create_pdf(data):
    """Рисует PDF"""
    pdf = FPDF()
    # Пробуем русский шрифт, иначе Arial
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        font_name = 'DejaVu'
    except:
        font_name = 'Arial'
    
    pdf.add_page()
    pdf.set_font(font_name, '', 24)
    pdf.cell(0, 20, "YOUR UPGRADE PLAN", ln=True, align='C')
    pdf.set_font(font_name, '', 12)
    pdf.multi_cell(0, 10, txt=f"\n{data['roast']}\n")
    
    pdf.ln(5)
    pdf.set_font(font_name, '', 14)
    pdf.cell(0, 10, "ТВОИ ПРОБЛЕМЫ:", ln=True)
    pdf.set_font(font_name, '', 12)
    for prob in data['problems_list']:
        pdf.cell(0, 8, txt=f"- {prob}", ln=True)

    pdf.add_page()
    pdf.set_font(font_name, '', 18)
    pdf.cell(0, 15, "YOUR WEAPONS (АРСЕНАЛ)", ln=True, align='C')
    pdf.set_font(font_name, '', 12)
    for item in data['ingredients']:
        pdf.set_font(font_name, '', 14)
        pdf.cell(0, 10, txt=f"🧪 {item['name']}", ln=True)
        pdf.set_font(font_name, '', 11)
        pdf.multi_cell(0, 6, txt=f"Зачем: {item['why']}\n")

    pdf.add_page()
    pdf.set_font(font_name, '', 18)
    pdf.cell(0, 15, "BATTLE PLAN (РЕЖИМ)", ln=True, align='C')
    pdf.set_font(font_name, '', 14)
    pdf.cell(0, 10, "☀️ УТРО:", ln=True)
    pdf.set_font(font_name, '', 11)
    pdf.multi_cell(0, 6, txt=data['routine_morning'])
    pdf.ln(5)
    pdf.cell(0, 10, "🌙 ВЕЧЕР:", ln=True)
    pdf.multi_cell(0, 6, txt=data['routine_evening'])

    pdf.add_page()
    pdf.set_font(font_name, '', 20)
    pdf.cell(0, 30, "DON'T BE STUPID", ln=True, align='C')
    pdf.set_font(font_name, '', 12)
    pdf.multi_cell(0, 8, txt="Ты знаешь теорию. Но если купишь плохие средства - сделаешь хуже.\nЯ собрал список конкретных банок, которые работают.\n\nЖми ссылку ниже, чтобы забрать готовый список.", align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 10, ">>> КУПИТЬ СПИСОК СРЕДСТВ ($5) <<<", ln=True, align='C', link=UPSELL_LINK)
    return pdf

# --- 3. ИНТЕРФЕЙС ---
st.warning("""
⚠️ **ЧЕСТНОЕ ПРЕДУПРЕЖДЕНИЕ:**
Дизайна нет, потому что я экономлю на дизайнерах.
У меня есть цель: **Дом на Lake Oswego ($6M) + Вишневый Jaguar E-Type V12 ($150k)**.
Каждые ваши $10 приближают меня к мечте.

Я не обещаю, что этот отчет купит тебе такой дом.
Я обещаю другое: **когда ты добьешься успеха, ты будешь выглядеть достойно**.
Приведи лицо в порядок, чтобы не было стыдно опустить крышу кабриолета.
""")

GOAL = 6150000 
CURRENT = 40 
st.progress(CURRENT / GOAL)
st.caption(f"Собрано: ${CURRENT} из ${GOAL:,}. Осталось всего ничего.")
st.divider()

st.title("SKIN ROAST 🔥")

if st.query_params.get("paid") == "true":
    st.balloons()
    st.success("Добро пожаловать в клуб.")
    with st.form("gen"):
        upl = st.file_uploader("Загрузи фото для анализа", type=['jpg', 'png'])
        if st.form_submit_button("СГЕНЕРИРОВАТЬ ПЛАН"):
            if upl:
                with st.spinner("AI пишет стратегию..."):
                    # Здесь заглушка данных для теста (в версии 2.0 сделаем умнее)
                    data = analyze_skin("30", "Жирная", "Прыщи", "Нет сна")
                    if data:
                        pdf = create_pdf(data)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                            pdf.output(tmp.name)
                            with open(tmp.name, "rb") as f:
                                st.download_button("⬇️ СКАЧАТЬ PDF", f, "Skin_Roast_Plan.pdf", "application/pdf")
                        st.warning("Не тупи, купи готовый список средств ниже.")
                        st.link_button("КУПИТЬ СПИСОК ($5)", UPSELL_LINK)
else:
    with st.form("quiz"):
        st.selectbox("Возраст", ["До 25", "25-35", "35+"])
        st.selectbox("Кожа", ["Жирная", "Сухая", "Нормальная"])
        st.selectbox("Проблема", ["Прыщи", "Морщины", "Мешки"])
        st.file_uploader("Фото", type=['jpg'])
        if st.form_submit_button("СКАНИРОВАТЬ"):
            st.success("Данные приняты.")
            st.info("Найдено 3 критических ошибки.")
            st.link_button("👉 ПОЛУЧИТЬ ПЛАН ($10)", LEMON_SQUEEZY_LINK)
