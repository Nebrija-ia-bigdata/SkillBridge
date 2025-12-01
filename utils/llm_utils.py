from groq import Groq
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(texto, modelo="llama-3.3-70b-versatile"):
    #Genera un resumen usando Groq
    completion = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": f"Resume este texto de forma clara y breve:\n\n{texto}"}],
        max_tokens=1024
    )
    return completion.choices[0].message.content

def ask_about_text(contexto, pregunta, modelo="llama-3.1-8b-instant"):
    #Permite hacer preguntas sobre un texto
    completion = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": f"Contexto: {contexto}\n\nPregunta: {pregunta}"}],
        max_tokens=1024
    )
    return completion.choices[0].message.content
