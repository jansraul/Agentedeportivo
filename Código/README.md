# 🏋️ Agente Deportivo – Backend

Este proyecto implementa un agente inteligente capaz de responder preguntas y recomendar productos deportivos (proteínas, implementos de entrenamiento, etc.) utilizando RAG con LangChain, Elasticsearch y memoria PostgreSQL.

---

## 🚀 Tecnologías utilizadas

- 🐍 Python
- 🧠 LangChain
- 🤖 OpenAI API
- 📦 Elasticsearch
- 🐘 PostgreSQL (Cloud SQL)
- 🔥 Google Cloud Run (despliegue)
- 🐳 Docker

---

## 📁 Estructura del Proyecto

Code/
│
├── app.py              # Código principal del backend (FastAPI o Flask)
├── requirements.txt    # Librerías necesarias
├── Dockerfile          # Archivo de configuración para Docker y despliegue


---

## ⚙️ Instrucciones de instalación local

```bash
git clone https://github.com/jansraul/agentesport-backend.git
cd agentesport-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

🌐 Despliegue

El backend fue desplegado en Google Cloud Run. Puedes probar el agente con esta URL:

https://agentesport-v2-891547936974.us-central1.run.app/agent?idagente=demo&msg=proteína

📥 Variables de entorno

Asegúrate de definir en Cloud Run:
	•	OPENAI_API_KEY
	•	LANGCHAIN_API_KEY
	•	DB_URI (PostgreSQL)
	•	es_url, es_user, es_password, index_name


🧠 Funcionalidad
	•	Consulta productos con lenguaje natural
	•	Responde con un tono amigable y personalizado
	•	Accede a base de datos vectorial con Elasticsearch
	•	Almacena memoria de conversación



🧱 Estructura del Proyecto

### 🧱 Estructura del Proyecto

La estructura de carpetas y archivos del backend es la siguiente:

Agentesport-backend/
├── Dockerfile
├── requirements.txt
├── app.py
├── .dockerignore
├── .gitignore
├── README.md
└── code/
├── tools/
│   └── tool_busqueda_producto.py
└── utils/
└── procesamiento_vectorstore.py


- `app.py`: archivo principal que define la lógica del agente y el endpoint.
- `Dockerfile`: define el contenedor para desplegar en Cloud Run.
- `requirements.txt`: librerías necesarias para ejecutar el backend.
- `tools/`: herramientas personalizadas que ayudan a interactuar con la base de datos.
- `utils/`: funciones auxiliares para transformar datos y procesar la memoria.


🚀 Despliegue y Pruebas


### 🚀 Despliegue y Pruebas

Este backend fue desplegado exitosamente en Google Cloud Run. Para realizar el despliegue, se siguieron los siguientes pasos:

1. Se creó una carpeta local con el código limpio (`app.py`, `Dockerfile`, etc.).
2. Se configuró el archivo `Dockerfile` para empaquetar la aplicación con todas sus dependencias.
3. Se ejecutó el despliegue desde la terminal con el siguiente comando:
   ```bash
   gcloud run deploy agentesport-v2 --source . --region us-central1 --allow-unauthenticated

4.	Se configuraron las variables de entorno en Cloud Run, como las claves de OpenAI, Tavily y la URL de Elasticsearch.

5.	Se expuso la IP pública de la instancia de Elasticsearch y se validó que esté accesible desde Cloud Run.








🤝 Autor

Jans Raúl López Ruiz
Proyecto realizado como parte del diplomado en Inteligencia Artificial Generativa - Universidad Ricardo Palma