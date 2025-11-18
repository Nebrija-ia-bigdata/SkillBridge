import streamlit as st
from PIL import Image
import os

from utils.pdf_utils import extract_pdf_text
from utils.llm_utils import summarize_text, ask_about_text
from utils.skill_analysis import (
    analyze_career_transition,
    compare_cvs_for_position,
)

def local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: No se pudo encontrar el archivo CSS en {file_name}")
    except Exception as e:
        st.error(f"Error cargando CSS: {e}")


# -----------------------------------------------------------------

# Configuración
st.set_page_config(page_title="SkillBridge", page_icon="🧭", layout="wide")
local_css("styles.css")

st.title("🧭 SkillBridge – Asistente de Habilidades Transferibles")

# Logo
logo_path = os.path.join("assets", "logo.jpg")
if os.path.exists(logo_path):
    imagen = Image.open(logo_path)
    st.image(imagen, width=200)
else:
    st.warning("⚠️ No se encontró el logo en assets/logo.jpg")

# Subir PDF
st.markdown("### 📄 Sube tu CV o documento laboral")
pdf = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

if pdf:
    # ➜ Vista previa del PDF (nuevo visor de Streamlit)
    st.write("### 👀 Vista previa del PDF")
    st.pdf(pdf)

    try:
        texto = extract_pdf_text(pdf)
        st.session_state["cv_texto"] = texto

        st.text_area(
            "Contenido (vista previa del texto extraído)",
            texto[:800] + "...",
            height=200,
        )

        modelo = st.selectbox(
            "Selecciona modelo Groq:",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        )

        if st.button("🔍 Analizar habilidades detectadas"):
            resumen = summarize_text(
                texto + "\n\nExtrae habilidades (soft y hard skills).", modelo=modelo
            )
            st.subheader("🧩 Habilidades detectadas:")
            st.write(resumen)

        pregunta = st.text_input("💬 Haz una pregunta sobre tu CV:")
        if pregunta:
            respuesta = ask_about_text(texto, pregunta, modelo)
            st.subheader("🤖 Respuesta del asistente:")
            st.write(respuesta)

    except Exception as e:
        st.error(f"❌ Error: {e}")


# Transición profesional
st.markdown("---")
st.header("🎯 Transición profesional")

perfil_texto = st.session_state.get("cv_texto", "")
if not perfil_texto:
    perfil_texto = st.text_area("Describe tu perfil:", height=150)

nuevo_puesto = st.text_input("¿A qué puesto quieres cambiar?")
if st.button("🚀 Analizar transición profesional"):
    if perfil_texto and nuevo_puesto:
        with st.spinner("Analizando..."):
            resultado = analyze_career_transition(perfil_texto, nuevo_puesto)
            st.subheader("🔍 Análisis de transición:")
            st.write(resultado)
    else:
        st.warning("Por favor, proporciona perfil y puesto objetivo.")


st.markdown("---")
st.header("📊 Comparar dos versiones de CV")

cv1 = st.file_uploader("Sube tu CV versión 1", type=["pdf"], key="cv1")
cv2 = st.file_uploader("Sube tu CV versión 2", type=["pdf"], key="cv2")
puesto_objetivo = st.text_input(
    "¿Cuál es el puesto al que quieres aplicar?",
    placeholder="Ejemplo: analista de datos",
)

if st.button("⚖️ Comparar CVs"):
    if cv1 and cv2 and puesto_objetivo:
        try:
            texto_cv1 = extract_pdf_text(cv1)
            texto_cv2 = extract_pdf_text(cv2)

            with st.spinner("Analizando CVs y comparando relevancia..."):
                resultado = compare_cvs_for_position(
                    texto_cv1, texto_cv2, puesto_objetivo
                )

            st.subheader("📌 Resultados de la comparación")
            st.write(resultado)

        except Exception as e:
            st.error(f"❌ Error al procesar los CVs: {e}")
    else:
        st.warning("Por favor, sube ambos CVs y escribe el puesto objetivo.")
