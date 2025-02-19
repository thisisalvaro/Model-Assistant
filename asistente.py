import time
import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Configurar API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Función para enviar mensajes al asistente
def obtener_respuesta(prompt):
    try:
        # Crear un hilo para la conversación
        thread = openai.beta.threads.create()

        # Agregar mensaje al hilo
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Ejecutar el asistente en ese hilo
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Esperar hasta que el asistente termine de procesar
        while True:
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,  # 🔹 Se agregó este argumento
                run_id=run.id
            )
            if run.status == "completed":
                break
            time.sleep(1)  # Esperar 1 segundo antes de reintentar

        # Obtener la respuesta generada
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        return f"Error: {str(e)}"

# Interfaz con Streamlit
def interfaz():
    st.title("Asistente con OpenAI")
    st.write("¡Hazle preguntas a tu asistente!")

    prompt = st.text_input("Escribe tu pregunta:")

    if prompt:
        respuesta = obtener_respuesta(prompt)
        st.write("Respuesta del Asistente:")
        st.write(respuesta)

if __name__ == "__main__":
    interfaz()
