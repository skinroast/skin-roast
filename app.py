import streamlit as st
import time

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Skin Roast AI", layout="centered")

# --- CSS СТИЛИ ---
st.markdown("""
    <style>
    /* Стиль для желтой плашки */
    .funny-warning {
        background-color: #2b2d18;
        color: #e6c957;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e6c957;
        font-family: monospace;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }
    
    /* Заголовки */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #aaa;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Стиль буллитов */
    .feature-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B2B;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ЛОГИКА: ПОКАЗАТЬ ЛЕНДИНГ ИЛИ ПРИЛОЖЕНИЕ? ---
# Проверяем, есть ли "секретный ключ" в ссылке
query_params = st.query_params
access_granted = query_params.get("paid") == "true"

if not access_granted:
    # ==========================================
    # 🔴 ЧАСТЬ 1: ЛЕНДИНГ (ВИДЯТ ВСЕ)
    # ==========================================

    # 1. ТВОЯ ФИРМЕННАЯ ПЛАШКА
    st.markdown("""
    <div class="funny-warning">
        ⚠️ <b>HONEST WARNING:</b> There is no fancy design here because I'm saving money. 
        I have a goal: <b>Lake Oswego House ($6M) + Cherry Jaguar E-Type V12 ($150k)</b>. 
        Every $10 you spend gets me 0.000001% closer to the dream.<br><br>
        <b>REAL TALK:</b> I don't promise this report will buy you that house. That's on you. 
        I promise this: <b>when you make it big, you will look the part.</b> 
        Fix your face now, so you don't feel ashamed to drop the roof of your convertible later.
    </div>
    """, unsafe_allow_html=True)

    # 2. КАРТИНКА (Лицо со сканом - Исправил на PNG!)
    try:
        st.image("scan_face.png", caption="AI Deep Scan Analysis", use_column_width=True)
    except:
        st.info("🖼 [Картинка scan_face.png не найдена. Загрузи файл в GitHub!]")

    # 3. ПРОДАЮЩИЙ ТЕКСТ
    st.markdown('<div class="main-header">YOUR MIRROR LIES.<br>AI DOESN\'T.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Get a brutally honest analysis of your skin health, real age, and potential issues before they become visible.</div>', unsafe_allow_html=True)

    # 4. ЧТО ВНУТРИ
    st.markdown("""
    <div class="feature-box">
        <h4>What you get for $10:</h4>
        <p>✅ <b>The Roast:</b> No sugar-coating. See exactly what others notice but don't say.</p>
        <p>✅ <b>The Scan:</b> Detects deep wrinkles, acne score, and texture issues.</p>
        <p>✅ <b>The Fix:</b> A personalized Morning & Night routine just for YOUR face.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("") 

    # 5. КНОПКА КУПИТЬ (Patreon)
    # Вставь сюда ссылку на товар!
    PATREON_LINK = "https://www.patreon.com/твоя_ссылка" 
    
    st.link_button("👉 UNLOCK MY ROAST ($10)", PATREON_LINK, type="primary", use_container_width=True)
    st.caption("Secure payment via Patreon. Instant Access.")

else:
    # ==========================================
    # 🟢 ЧАСТЬ 2: ПРИЛОЖЕНИЕ (ЕСЛИ ОПЛАТИЛИ)
    # ==========================================
    
    st.title("🔥 Skin Roast AI")
    st.success("✅ Access Granted. Let's fix your face.")
    
    st.divider()

    # --- ТВОЙ ОПРОСНИК (DOSSIER) ---
    st.subheader("1. The Dossier:")
    
    age = st.selectbox("Age Group", ["Under 25", "25-34", "35-44", "45-54", "55+"])
    skin_type = st.selectbox("Skin Type", ["Oily (Shiny)", "Dry (Flaky)", "Combination (T-Zone)", "Sensitive (Red)", "Normal"])
    main_issue = st.selectbox("Main Enemy", ["Acne / Pimples", "Wrinkles / Aging", "Pigmentation / Spots", "Large Pores", "Dullness / Tired Look"])
    
    st.divider()
    
    # --- ЗАГРУЗКА ФОТО ---
    st.subheader("2. The Evidence:")
    uploaded_file = st.file_uploader("Upload your selfie (No filters!)", type=['jpg', 'png', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Analyzing...", use_column_width=True)
        
        if st.button("Generate Roast & Routine"):
            with st.spinner("AI is judging your life choices..."):
                time.sleep(3) # Имитация работы
                
            # Заглушка результата (потом заменим на реальный AI)
            st.error("💀 ROAST PREVIEW: You look tired. The AI detects sleep deprivation.")
            st.info("💡 ROUTINE PREVIEW: Drink water right now. Use Retinol at night.")
