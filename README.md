# Telegram Monitor Agent

Agente IA que monitoriza diariamente un grupo de Telegram, resume los contenidos enlazados y los publica en una aplicación web tras la aprobación humana.

## 🚀 Características

- Integración con el servidor [telegram-mcp](https://github.com/chaindead/telegram-mcp) para recuperar mensajes del grupo configurado.
- Procesamiento de URLs con extracción de metadatos, resumen (2-3 líneas) y generación automática de imagen si no existe una destacada.
- Flujo humano-en-el-bucle con vista previa, edición manual y regeneración de imagen antes de publicar.
- Backend Flask + SQLite con API REST (`GET/POST`) y frontend en JavaScript vanilla con diseño responsive.

## 📁 Estructura de directorios

```
.
├── agent/               # Código del agente de monitoreo
│   ├── config.py        # Gestión de configuración (.env)
│   ├── main.py          # Punto de entrada CLI del agente
│   ├── preview.py       # Flujo de aprobación humana
│   ├── publisher.py     # Cliente REST hacia el backend
│   ├── state.py         # Persistencia del último mensaje procesado
│   ├── telegram_monitor.py # Cliente MCP para Telegram
│   ├── url_processor.py # Extracción, resumen e imagen
│   └── utils.py         # Utilidades generales
├── backend/
│   ├── app.py           # API Flask (GET/POST /api/posts)
│   └── database.py      # Inicialización y conexión SQLite
├── frontend/
│   ├── index.html       # Interfaz web responsive
│   ├── styles.css       # Estilos de las tarjetas
│   └── app.js           # Fetch al API y render dinámico
├── requirements.txt     # Dependencias Python
├── run.py               # Script histórico (no utilizado en la nueva versión)
└── README.md
```

## 🧰 Requisitos

- Python 3.10+
- Node.js (para ejecutar el servidor telegram-mcp)
- Cuenta de Telegram con `api_id` y `api_hash`
- API key de OpenAI con acceso a modelos de texto e imagen

## ⚙️ Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Instala el servidor MCP:

```bash
npm install -g @chaindead/telegram-mcp
```

## 🔐 Configuración

Puedes copiar `.env.example` y completar tus credenciales:

```bash
cp .env.example .env
```

Luego edita el archivo `.env` en la raíz con:

```
TELEGRAM_CHAT_ID=tu_chat_id
TELEGRAM_MCP_SERVER=ws://localhost:2024
TELEGRAM_MCP_API_KEY=token_si_aplica
OPENAI_API_KEY=sk-...
OPENAI_SUMMARY_MODEL=gpt-4o-mini
OPENAI_IMAGE_MODEL=gpt-image-1
BACKEND_BASE_URL=http://localhost:8000
AGENT_STATE_FILE=agent_state.json
REQUEST_TIMEOUT=20
```

## 🗄️ Backend Flask

```bash
export FLASK_APP=backend.app
flask run --host=0.0.0.0 --port=8000
```

- `GET /api/posts` devuelve `{ "items": [...] }`
- `GET /api/posts/<id>` recupera un post específico
- `POST /api/posts` crea un post. Campos requeridos: `title`, `summary`, `source_url`, `release_date`

La base de datos SQLite (`backend/posts.db`) se crea automáticamente.

## 🌐 Frontend

Sirve el contenido de `frontend/` con cualquier servidor estático (por ejemplo `python -m http.server 3000`).
Configura `window.API_BASE_URL` si el backend se sirve en otra URL.

## 🤖 Ejecución del agente

1. Inicia el servidor `telegram-mcp` apuntando al chat objetivo.
2. Ejecuta el backend Flask.
3. Lanza el agente:

```bash
python -m agent.main
```

Flujo del agente:

1. Recupera los mensajes desde el último `message_id` guardado.
2. Extrae URLs y procesa cada una (título, resumen, imagen, tipo, proveedor, fecha actual).
3. Presenta en consola una vista previa. El humano puede:
   - **Aceptar**: se envía al backend.
   - **Modificar**: actualizar título/resumen o regenerar imagen.
   - **Descartar**: ignora la URL.
4. Guarda el `message_id` más reciente para la siguiente ejecución.

## 🧪 Desarrollo y pruebas

- Ejecuta `flask run` para probar la API.
- Abre `frontend/index.html` (sirviéndolo con un servidor) para verificar la UI.
- Utiliza entornos de prueba o chats privados en Telegram.

## 📝 Notas

- El módulo `telegram_monitor.py` requiere la librería `mcp`. Instálala con `pip install mcp`.
- Si la URL no provee una imagen válida, el agente genera una nueva usando el modelo configurado.
- `agent_state.json` almacena el ID del último mensaje procesado para ejecuciones diarias.

## 📄 Licencia

Proyecto educativo. Utilízalo y adáptalo según tus necesidades.
