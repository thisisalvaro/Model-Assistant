import os
import time
import openai
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuración de claves API
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def obtener_clima(ciudad):
    """Obtiene el clima actual desde OpenWeatherMap"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&units=metric&lang=es"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        clima = datos['weather'][0]['description']
        temperatura = datos['main']['temp']
        return f"El clima en {ciudad} es {clima} con una temperatura de {temperatura}°C."
    else:
        return f"No se pudo obtener el clima de {ciudad}."


# Registrar la función en el asistente
openai.beta.assistants.update(
    assistant_id=ASSISTANT_ID,
    tools=[{
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": "Obtiene el clima actual de una ciudad específica.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {"type": "string"}
                },
                "required": ["ciudad"]
            }
        }
    }]
)


def procesar_respuesta_asistente(thread_id, run_id):
    run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    
    # Añadir impresión para depuración
    print("Estado del run:", run.status)
    print(run)  # Esto te permitirá ver toda la respuesta del run

    if run.status == "requires_action":
        if 'required_action' in run and run.required_action:
            tool_call = run.required_action.get('tool_calls', [])[0]
            if tool_call.get('function', {}).get('name') == "obtener_clima":
                ciudad = tool_call['function']['arguments'].get('ciudad')
                if ciudad:
                    resultado = obtener_clima(ciudad)
                    openai.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run_id,
                        tool_outputs=[{
                            "tool_call_id": tool_call['id'],
                            "output": resultado
                        }]
                    )


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

        # Esperar a que el asistente termine o solicite una función
        while True:
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print("Estado del run:", run.status)  # Imprime el estado del run para depurar
            if run.status == "completed":
                break
            elif run.status == "requires_action":
                procesar_respuesta_asistente(thread.id, run.id)
            time.sleep(1)

        # Obtener la respuesta generada
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value

    except Exception as e:
        return f"Error: {str(e)}"


# Interfaz Streamlit
def interfaz():
    st.title("Asistente del Clima con OpenAI")
    st.write("Pregúntame el clima de cualquier ciudad 🌦️")

    prompt = st.text_input("Escribe tu pregunta:")

    if prompt:
        respuesta = obtener_respuesta(prompt)
        st.write("Respuesta del Asistente:")
        st.write(respuesta)


if __name__ == "__main__":
    interfaz()
