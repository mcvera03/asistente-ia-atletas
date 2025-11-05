# 🤖 Asistente IA para Atletas (v2)

Versión v2 preparada para despliegue en Streamlit Cloud (usa Python 3.10).

## Contenido
- `asistente_ia_atletas_gpt.py` — código principal
- `requirements.txt` — dependencias fijadas (compatibles con MediaPipe)
- `.streamlit/config.toml` — fuerza Python 3.10 en Streamlit Cloud
- `README.md`

## Deploy rápido
1. Subir estos archivos a la raíz de tu repositorio en GitHub.
2. En Streamlit Cloud, configurar **Main file path** a `asistente_ia_atletas_gpt.py`.
3. Añadir secret `OPENAI_API_KEY` en Settings → Secrets.
4. Presionar **Rerun**.

## Nota
Si la instalación de `mediapipe` falla en tu cuenta, considera usar la app sin `mediapipe` (puedo generar esa versión si la necesitas).
