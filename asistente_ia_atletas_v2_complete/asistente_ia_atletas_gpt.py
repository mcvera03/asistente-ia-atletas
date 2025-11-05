import streamlit as st

# 🧩 Primero SIEMPRE debe ir set_page_config
st.set_page_config(page_title="Asistente IA para Atletas", page_icon="🤖")

# Luego puedes mostrar avisos, imports extra, etc.
import cv2
import numpy as np
from PIL import Image
import openai

# intentar cargar mediapipe
try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except Exception:
    HAS_MEDIAPIPE = False
    st.warning("⚠️ Mediapipe no está disponible en este entorno (Python 3.13). "
               "La app se ejecutará en modo limitado sin análisis corporal.")

st.title("🤖 Asistente IA para Atletas en Recuperación y Rehabilitación")
st.write("""
Sube una foto (opcional) y conversa con tu entrenador IA sobre tu recuperación,
rutinas y prevención de lesiones.
""")

if "OPENAI_API_KEY" not in st.secrets:
    st.error("Agrega tu `OPENAI_API_KEY` en Settings → Secrets.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("📸 Sube una foto (opcional)", type=["jpg","jpeg","png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    if HAS_MEDIAPIPE:
        st.info("Procesando pose corporal ...")
        # Aquí puedes restaurar el análisis corporal más adelante
    else:
        st.info("Modo limitado — no se puede analizar la postura.")
        st.write("Puedes continuar con el chat IA normalmente.")

st.subheader("💬 Chat con tu Asistente IA")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "system",
         "content": "Eres un asistente especializado en recuperación y rehabilitación deportiva."},
        {"role": "assistant",
         "content": "¡Hola atleta! 👋 ¿Cómo te sientes hoy? ¿Tienes alguna molestia o lesión?"}
    ]

for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f"**🧍 Tú:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Asistente:** {msg['content']}")

entrada = st.text_input("Escribe tu mensaje…")
if st.button("Enviar") and entrada:
    st.session_state.mensajes.append({"role": "user", "content": entrada})
    with st.spinner("Pensando... 💭"):
        respuesta = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state.mensajes,
            temperature=0.7,
        )
    content = respuesta["choices"][0]["message"]["content"]
    st.session_state.mensajes.append({"role": "assistant", "content": content})
    st.experimental_rerun()
