# asistente_ia_atletas_gpt.py
import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
from PIL import Image
import openai

st.set_page_config(page_title="Asistente IA para Atletas", page_icon="🤖")
st.title("🤖 Asistente IA para Atletas en Recuperación y Rehabilitación")
st.write("""
Soy tu entrenador inteligente 🧠.  
Puedo analizar tus proporciones corporales y diseñarte rutinas personalizadas
para mejorar tu recuperación física y prevenir lesiones.
""")

if "OPENAI_API_KEY" not in st.secrets:
    st.warning("⚠️ No se encontró tu API key de OpenAI. Agrégala en Settings → Secrets.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("📸 Sube una foto de cuerpo completo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen cargada correctamente ✅", use_column_width=True)

    img_array = np.array(image)
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(img_rgb)

        if not results.pose_landmarks:
            st.error("No se detectaron puntos corporales. Intenta subir una foto más clara o de cuerpo completo.")
        else:
            mp_drawing.draw_landmarks(img_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            st.image(cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB), caption="Análisis corporal completado 🧍")

            landmarks = results.pose_landmarks.landmark
            altura = abs(landmarks[mp_pose.PoseLandmark.NOSE].y - landmarks[mp_pose.PoseLandmark.ANKLE_LEFT].y)
            proporciones = round(altura, 2)
            st.success(f"Proporción corporal estimada: {proporciones}")

            st.subheader("💬 Chat con tu Asistente IA")

            if "mensajes" not in st.session_state:
                st.session_state.mensajes = [
                    {"role": "system", "content": "Eres un asistente especializado en recuperación y rehabilitación deportiva. Das consejos de fisioterapia, estiramientos y prevención de lesiones."},
                    {"role": "assistant", "content": "¡Hola atleta! 👋 Cuéntame, ¿cómo te sientes hoy? ¿Tienes alguna molestia o estás recuperándote de una lesión?"}
                ]

            for msg in st.session_state.mensajes:
                if msg["role"] == "user":
                    st.markdown(f"**🧍Tú:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.markdown(f"**🤖 Asistente:** {msg['content']}")

            entrada = st.text_input("Escribe tu mensaje aquí...")

            if st.button("Enviar"):
                if entrada:
                    st.session_state.mensajes.append({"role": "user", "content": entrada})

                    with st.spinner("Pensando... 💭"):
                        respuesta = openai.ChatCompletion.create(
                            model="gpt-4o-mini",
                            messages=st.session_state.mensajes,
                            temperature=0.7
                        )

                    content = respuesta["choices"][0]["message"]["content"]
                    st.session_state.mensajes.append({"role": "assistant", "content": content})
                    st.experimental_rerun()
else:
    st.info("Sube una imagen para iniciar el análisis corporal y activar el chat inteligente.")
