import streamlit as st
from PIL import Image
import os
import base64
from utils.pdf_utils import extract_pdf_text
from utils.llm_utils import summarize_text, ask_about_text
from utils.skill_analysis import analyze_career_transition, compare_cvs_for_position


# --- FUNCIÓN AUXILIAR PARA IMÁGENES EN HTML ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        print(f"Error cargando imagen base64: {e}")
        return ""


logo_path = os.path.join("assets", "logo_skillbridge_img-Photoroom.png")
logo_b64 = get_image_base64(logo_path)
img_html = f'<img src="{logo_b64}" width="70" style="margin-right: 20px; border-radius: 10px;">'


# --- FUNCIÓN CSS ---
def local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"No se cargó el estilo: {e}")


# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SkillBridge", page_icon=logo_path, layout="wide")
local_css("styles.css")


# --- SIDEBAR ---
with st.sidebar:
    # Logo y Título
    logo_path = os.path.join("assets", "logo_skillbridge_img-Photoroom.png")
    if os.path.exists(logo_path):
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            st.image(logo_path, width=60)
        with col2:
            st.markdown(
                "<h2 style='margin:0; font-size:24px;'>Skill<span>Bridge</span></h2>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown("## SkillBridge")

    st.write("")
    st.write("")

    # Elección de IA
    st.markdown("### Modelos de IA:")
    modelo = st.selectbox(
        "Elige un modelo:",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-120b",
            "qwen/qwen3-32b",
        ],
        index=0,
    )
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # Footer
    linkedin_img = get_image_base64(os.path.join("assets", "linkedin-svgrepo-com.png"))
    github_img = get_image_base64(os.path.join("assets", "github-svgrepo-com.png"))

    linkedin_url = ""
    github_url = "https://github.com/Nebrija-ia-bigdata/SkillBridge"

    footer_html = f"""
    <div class="sidebar-footer">
        <hr> 
        <a href="{linkedin_url}" target="_blank">
            <img src="{linkedin_img}" alt="LinkedIn">
        </a>
        <a href="{github_url}" target="_blank">
            <img src="{github_img}" alt="GitHub">
        </a>
        <p style="font-size: 11px; color: #888; margin-top: 5px;">v1.0.0</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# --- HEADER ---
st.markdown(
    f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <div style="flex-shrink: 0; margin-right: 15px;">
                {img_html}
            </div>
            <h1 style="margin: 0; font-size: 2.5rem;">Skill<span>Bridge</span></h1>
        </div>
        <div style="text-align: left;">
            <p style="margin: 0; opacity: 0.8;">Tu asistente inteligente para análisis de carrera y habilidades transferibles</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- GESTIÓN DE ESTADO (Session State) ---
if "cv_texto" not in st.session_state:
    st.session_state["cv_texto"] = ""

# --- NAVEGACIÓN POR PESTAÑAS ---

# 1. Cargamos las imágenes en memoria
icon_1 = get_image_base64("assets/document-text-svgrepo-com.png")
icon_2 = get_image_base64("assets/transition-right-svgrepo-com.png")
icon_3 = get_image_base64("assets/balance-svgrepo-com.png")

st.markdown(
    f"""
    <style>
        button[data-baseweb="tab"] {{
            padding-left: 0 !important; 
        }}
        button[data-baseweb="tab"] p {{
            padding-left: 30px !important;
            background-repeat: no-repeat !important;
            background-position: 0% 55% !important; 
            background-size: 20px !important;       
            display: inline-block; 
            line-height: 24px;
        }}
        button[data-baseweb="tab"]:nth-of-type(1) p {{
            background-image: url('{icon_1}') !important;
        }}
        button[data-baseweb="tab"]:nth-of-type(2) p {{
            background-image: url('{icon_2}') !important;
        }}
        button[data-baseweb="tab"]:nth-of-type(3) p {{
            background-image: url('{icon_3}') !important;
        }}
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Creamos los tabs
tab1, tab2, tab3 = st.tabs(
    ["Analizar Perfil", "Transición de Carrera", "Comparador de CVs"]
)


# ========================================== PESTAÑA 1: ANÁLISIS INDIVIDUAL ==========================================
# Función para mostrar el cv que se ha subido
def mostrar_pdf_en_iframe(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.getvalue()).decode("utf-8")
    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0&scrollbar=0&view=FitH" 
            width="100%" 
            height="850px" 
            type="application/pdf" 
            style="border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)


with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Sube tu documento")
        pdf = st.file_uploader("Sube tu CV (PDF)", type=["pdf"], key="pdf_main")

        if pdf:
            # Procesar PDF solo si cambia
            with st.spinner("Leyendo documento..."):
                texto = extract_pdf_text(pdf)
                st.session_state["cv_texto"] = texto

            st.markdown("---")

            # 2. RESULTADOS DEL ANÁLISIS
            st.markdown("### Resultados del Análisis")

            # Botón principal
            if st.button("Detectar Habilidades (Soft & Hard)", type="primary"):
                with st.spinner("Analizando con IA..."):
                    resumen = summarize_text(
                        st.session_state["cv_texto"]
                        + "\n\nExtrae habilidades formato lista.",
                        modelo=modelo,
                    )
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <h3>Habilidades Detectadas</h3>
                            {resumen}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

            # Chat con el CV
            st.write("")
            st.markdown("#### Chat con tu CV")
            pregunta = st.text_input(
                "Pregunta algo específico (ej: ¿Tengo experiencia en liderazgo?)"
            )
            if pregunta:
                with st.spinner("Consultando..."):
                    respuesta = ask_about_text(
                        st.session_state["cv_texto"], pregunta, modelo
                    )
                    st.markdown(
                        f"""
                        <div class="result-card" style="border-left-color: #769a8c;">
                            <b>Respuesta:</b><br>{respuesta}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
    # Vista del CV
    with col2:
        if st.session_state.get("cv_texto"):

            st.markdown("### Vista del Documento")
            if pdf:
                mostrar_pdf_en_iframe(pdf)

        else:
            empty_state_html = """
            <div style="
                background-color: rgba(255, 255, 255, 0.5);
                border: 1px dashed #769a8c;
                border-radius: 15px; 
                min-height: 500px; 
                display: flex; 
                flex-direction: column; 
                justify-content: center; 
                align-items: center; 
                text-align: center;
                color: #6b7280;
            ">
                <div style="font-size: 50px; margin-bottom: 20px; opacity: 0.5;">📄</div>
                <h3 style="margin: 0; font-size: 20px; color: #4b5563;">Vista Previa</h3>
                <p style="margin-top: 10px; font-size: 14px;">
                    Sube tu CV en la izquierda para<br>ver el documento aquí.
                </p>
            </div>
            """
            st.markdown(empty_state_html, unsafe_allow_html=True)

# ========================================== PESTAÑA 2: TRANSICIÓN PROFESIONAL ==========================================
with tab2:
    st.markdown("### Plan de Transición de Carrera")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        perfil_input = st.text_area(
            "Tu perfil actual:",
            value=st.session_state.get("cv_texto", ""),
            height=200,
            placeholder="Pega tu CV o resumen aquí...",
        )
    with col_t2:
        nuevo_puesto = st.text_input(
            "¿A qué puesto aspiras?", placeholder="Ej: Product Manager"
        )
        st.write("")  
        st.write("")
        analizar_btn = st.button(
            "Generar Análisis de Brechas", use_container_width=True, type="primary"
        )

    if analizar_btn and perfil_input and nuevo_puesto:
        with st.spinner("Generando estrategia de transición..."):
            resultado = analyze_career_transition(perfil_input, nuevo_puesto)
            st.markdown(
                f"""
                <div class="result-card">
                    <h3>Estrategia Personalizada</h3>
                    {resultado}
                </div>
            """,
                unsafe_allow_html=True,
            )

# ========================================== PESTAÑA 3: COMPARADOR ==========================================

with tab3:
    st.markdown("### A/B Testing de Currículums")
    st.write("Sube dos versiones de tu CV para ver cuál se adapta mejor a una oferta.")

    col_c1, col_c2, col_c3 = st.columns([1, 1, 1])

    with col_c1:
        cv1 = st.file_uploader("Versión A", type=["pdf"], key="cv1")
        if cv1:
            mostrar_pdf_en_iframe(cv1)
            
    with col_c2:
        cv2 = st.file_uploader("Versión B", type=["pdf"], key="cv2")
        if cv2:
            mostrar_pdf_en_iframe(cv2)
            
    with col_c3:
        puesto_objetivo = st.text_input("Puesto Objetivo", key="target_pos")
        comparar_btn = st.button("Analizar Ganador", type="primary")

    if comparar_btn:
        if cv1 and cv2 and puesto_objetivo:
            try:
                # Reiniciar los punteros de los archivos para poder leerlos de nuevo
                cv1.seek(0)
                cv2.seek(0)
                
                text_a = extract_pdf_text(cv1)
                text_b = extract_pdf_text(cv2)

                with st.spinner("Comparando los currículums..."):
                    resultado = compare_cvs_for_position(
                        text_a, text_b, puesto_objetivo
                    )

                st.markdown(
                    f"""
                    <div class="result-card" style="border-left: 5px solid #769a8c;">
                        <h3>Resultados de la Comparativa</h3>
                        {resultado}
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error al procesar: {e}")
        else:
            st.warning("Por favor sube ambos archivos y define el puesto.")