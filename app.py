import streamlit as st
from PIL import Image
import os

from utils.pdf_utils import extract_pdf_text
from utils.llm_utils import summarize_text, ask_about_text
from utils.skill_analysis import (
    analyze_career_transition,
    compare_cvs_for_position,
)

# Configuración
st.set_page_config(page_title="SkillBridge", page_icon="🧭", layout="wide")
st.title("🧭 SkillBridge – Asistente de Habilidades Transferibles")

