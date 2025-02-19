# 📌 Asistente con OpenAI y Streamlit

Este proyecto implementa un **asistente basado en la API de OpenAI** utilizando el modelo `gpt-4` a través de **Assistants API**. La interfaz de usuario se construye con **Streamlit**, lo que permite interactuar de manera sencilla con el asistente.

---

## 📥 Instalación

Antes de ejecutar el proyecto, asegúrate de tener **Python 3.8+** instalado.

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu-repo/asistente-openai.git
cd asistente-openai
```

### 2️⃣ Crear un entorno virtual (Opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate    # En Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

Si `requirements.txt` no está disponible, instala manualmente:
```bash
pip install openai streamlit
```

---

## 🔑 Configuración

1. **Obtener una API Key de OpenAI:**
   - Ve a [OpenAI API Keys](https://platform.openai.com/api-keys) y copia tu clave.

2. **Obtener el ID del asistente:**
   - Ve a la sección **Assistants** en OpenAI y copia el `Assistant ID` (formato `asst_abc123xyz`).

3. **Configurar las credenciales:**
   - Crea un archivo `.env` o edita el script `asistente.py` y reemplaza:
     ```python
     openai.api_key = "tu-api-key"
     ASSISTANT_ID = "asst_abc123xyz"
     ```

---

## 🚀 Ejecución

Para iniciar la aplicación en **local**, ejecuta:
```bash
streamlit run asistente.py
```
Esto abrirá una interfaz en tu navegador donde podrás chatear con el asistente.

---

## 📌 Estructura del Proyecto
```plaintext
📂 asistente-openai/
 ├── 📜 asistente.py        # Código principal del asistente con Streamlit
 ├── 📜 requirements.txt    # Dependencias del proyecto
 ├── 📜 README.md           # Este archivo
 ├── 📜 .env.example        # Ejemplo de configuración con API Key
 └── 📂 venv/               # (Opcional) Entorno virtual
```

---

## 📌 Funcionalidades
✅ Basado en `gpt-4` con **Assistants API** de OpenAI.  
✅ Interfaz sencilla con **Streamlit**.  
✅ Soporte para múltiples preguntas en una conversación.  
✅ Respuesta en tiempo real con espera automática.

---

## ⚠️ Notas y Problemas Comunes
1. **Error `module 'openai' has no attribute 'beta'`**
   - Solución: Ejecuta `pip install --upgrade openai`

2. **Error `Project does not have access to model gpt-4`**
   - Solución: Asegúrate de que tu proyecto en OpenAI tiene acceso a `gpt-4`.

3. **Error `Runs.retrieve() missing 1 required keyword-only argument: 'thread_id'`**
   - Solución: Asegúrate de que el código usa `thread_id=thread.id` en la llamada a `runs.retrieve()`.

---

## 📜 Licencia
Este proyecto está bajo la licencia **MIT**. Puedes modificarlo y adaptarlo según tus necesidades. 😊

---

**¡Listo! Ahora puedes interactuar con tu asistente en Streamlit! 🚀**

