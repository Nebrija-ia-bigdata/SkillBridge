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
        # CAMBIO AQUÍ: Pon 'image/png' si tus iconos son PNG
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
            st.markdown("<h2 style='margin:0; font-size:24px;'>SkillBridge</h2>", unsafe_allow_html=True)
    else:
        st.markdown("## SkillBridge")

    st.write("") 
    st.write("")


    # Elección de IA
    st.markdown("### Modelos de IA:")
    modelo = st.selectbox(
        "Elige un modelo:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"], index=0
    )
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


    #Footer
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
            <h1 style="margin: 0; font-size: 2.5rem;">SkillBridge</h1>
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
tab1, tab2, tab3 = st.tabs(
    ["📄 Analizar mi Perfil", "🎯 Transición de Carrera", "⚖️ Comparador de CVs"]
)

# ==========================================
# PESTAÑA 1: ANÁLISIS INDIVIDUAL
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 1. Sube tu documento")
        pdf = st.file_uploader("Sube tu CV (PDF)", type=["pdf"], key="pdf_main")

        if pdf:
            # Procesar PDF solo si cambia
            with st.spinner("Leyendo documento..."):
                texto = extract_pdf_text(pdf)
                st.session_state["cv_texto"] = texto
            st.success("✅ Documento cargado")

            # Vista previa en expander para no ocupar espacio
            with st.expander("👀 Ver texto extraído"):
                st.text_area("Contenido raw", texto, height=150)

    with col2:
        if st.session_state["cv_texto"]:
            st.markdown("### 2. Resultados del Análisis")

            # Botón principal
            if st.button("🔍 Detectar Habilidades (Soft & Hard)", type="primary"):
                with st.spinner("Analizando con IA..."):
                    resumen = summarize_text(
                        st.session_state["cv_texto"]
                        + "\n\nExtrae habilidades formato lista.",
                        modelo=modelo,
                    )
                    # Usamos HTML container para dar estilo de tarjeta
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <h3>🧩 Habilidades Detectadas</h3>
                            {resumen}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

            st.markdown("---")
            st.markdown("#### 💬 Chat con tu CV")
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
                        <div class="result-card" style="border-left-color: #f1c40f;">
                            <b>🤖 Respuesta:</b><br>{respuesta}
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("👈 Sube un PDF en la columna izquierda para comenzar.")

# ==========================================
# PESTAÑA 2: TRANSICIÓN PROFESIONAL
# ==========================================
with tab2:
    st.markdown("### 🚀 Plan de Transición de Carrera")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        # Usamos el texto del CV cargado o permitimos escribir manual
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
        st.write("")  # Espaciador
        st.write("")
        analizar_btn = st.button(
            "✨ Generar Análisis de Brechas", use_container_width=True
        )

    if analizar_btn and perfil_input and nuevo_puesto:
        with st.spinner("Generando estrategia de transición..."):
            resultado = analyze_career_transition(perfil_input, nuevo_puesto)
            st.markdown(
                f"""
                <div class="result-card">
                    <h3>🎯 Estrategia Personalizada</h3>
                    {resultado}
                </div>
            """,
                unsafe_allow_html=True,
            )

# ==========================================
# PESTAÑA 3: COMPARADOR
# ==========================================
with tab3:
    st.markdown("### ⚖️ A/B Testing de Currículums")
    st.write("Sube dos versiones de tu CV para ver cuál se adapta mejor a una oferta.")

    col_c1, col_c2, col_c3 = st.columns([1, 1, 1])

    with col_c1:
        cv1 = st.file_uploader("Versión A", type=["pdf"], key="cv1")
    with col_c2:
        cv2 = st.file_uploader("Versión B", type=["pdf"], key="cv2")
    with col_c3:
        puesto_objetivo = st.text_input("Puesto Objetivo", key="target_pos")
        comparar_btn = st.button("⚖️ Analizar Ganador", type="primary")

    if comparar_btn:
        if cv1 and cv2 and puesto_objetivo:
            try:
                text_a = extract_pdf_text(cv1)
                text_b = extract_pdf_text(cv2)

                with st.spinner("Comparando semánticamente..."):
                    resultado = compare_cvs_for_position(
                        text_a, text_b, puesto_objetivo
                    )

                st.markdown(
                    f"""
                    <div class="result-card" style="border-left: 5px solid #e74c3c;">
                        <h3>🏆 Resultados de la Comparativa</h3>
                        {resultado}
                    </div>
                """,
                    unsafe_allow_html=True,
                )
            except Exception as e:
                st.error(f"Error al procesar: {e}")
        else:
            st.warning("⚠️ Por favor sube ambos archivos y define el puesto.")
