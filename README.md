# 🤖 Telegram Monitor - Agente de Monitoreo Inteligente

> **Proyecto desarrollado para curso de Programación Asistido por IA**  
> Monitor automático de grupos de Telegram con detección de URLs y análisis de contenido

## 🎯 Características

- ✅ **Monitoreo en tiempo real** del grupo "test-ia-agents"
- 🔗 **Detección automática de URLs** en mensajes
- 💾 **Guardado local** de mensajes y URLs en formato JSON
- 🌐 **Interfaz web moderna** para visualización y control
- 🚀 **Arquitectura MCP** (Model Context Protocol) con Telegram
- 📊 **Dashboard en tiempo real** con estadísticas

## 🏗️ Arquitectura

```
telegram-monitor-agent/
├── simple_monitor.py          # ✅ Monitor principal (CLI)
├── web_server.py             # 🌐 Servidor web con Flask  
├── web/
│   └── index.html           # 📱 Dashboard web moderno
├── results/                 # 💾 Archivos JSON generados
├── requirements.txt         # 📦 Dependencias Python
├── .env                    # 🔑 Configuración (API keys)
└── README.md              # 📚 Documentación
```

## 🚀 Instalación Rápida

### 1. Prerrequisitos
```bash
# Instalar Node.js (para MCP server)
# Instalar Python 3.8+
```

### 2. Configurar el proyecto
```bash
# Clonar repositorio
git clone https://github.com/JoseTapiaUex/TelegramMCPserver.git
cd TelegramMCPserver/telegram-monitor-agent

# Instalar dependencias Python
pip install -r requirements.txt

# Instalar MCP server de Telegram
npm install -g @chaindead/telegram-mcp
```

### 3. Configurar credenciales

Crear archivo `.env` basado en `.env.example`:
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales reales
TG_APP_ID=TU_API_ID_AQUI
TG_API_HASH=TU_API_HASH_AQUI
TG_PHONE=+34XXXXXXXXX
TARGET_CHAT=cht[ID_DEL_CHAT]
MONITORING_INTERVAL=60
```

> ⚠️ **IMPORTANTE**: Obtén tus credenciales en https://my.telegram.org/apps

## 💻 Uso

### Modo CLI (Monitor Simple)
```bash
# Ejecutar monitor en consola
python simple_monitor.py
```

### Modo Web (Dashboard)
```bash
# Iniciar servidor web
python web_server.py

# Acceder al dashboard
# http://localhost:5000
```

## 📊 Funcionalidades del Dashboard

- **🎛️ Control del Monitor**: Iniciar/detener monitoreo
- **📈 Estadísticas en Tiempo Real**: Mensajes procesados, URLs detectadas
- **💬 Mensajes Recientes**: Últimos mensajes del grupo
- **🔗 URLs Detectadas**: Lista de enlaces encontrados con metadata
- **🔄 Auto-actualización**: Datos actualizados cada 5 segundos

## 🔧 Configuración Avanzada

### Variables de Entorno Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `TG_APP_ID` | ID de la aplicación Telegram | `TU_API_ID` |
| `TG_API_HASH` | Hash API de Telegram | `4b525537a...` |
| `TARGET_CHAT` | ID del chat a monitorear | `cht[CHAT_ID]` |
| `MONITORING_INTERVAL` | Intervalo en segundos | `60` |

## 📁 Archivos Generados

### Mensajes (`results/message_*.json`)
```json
{
  "id": "2025-09-30 20:33:15_130587018990476347",
  "text": "https://x.com/OpenAI/status/1973071069016641829",
  "date": "2025-09-30 20:33:15",
  "from": "usuario",
  "urls": ["https://x.com/OpenAI/status/1973071069016641829"],
  "chat": "cht[CHAT_ID]"
}
```

### URLs (`results/url_*.json`)
```json
{
  "url": "https://x.com/OpenAI/status/1973071069016641829",
  "found_in_message": "2025-09-30 20:33:15_130587018990476347",
  "from_user": "usuario",
  "timestamp": "2025-09-30T20:47:08.679785",
  "status": "detected"
}
```

## 🎓 Contexto Académico

Este proyecto fue desarrollado como parte de un **curso de Programación Asistido por IA**, demostrando:

- **Integración de APIs** (Telegram MCP)
- **Procesamiento en tiempo real** de datos
- **Arquitectura web moderna** (Flask + HTML5)
- **Gestión de estados** y persistencia de datos
- **Interfaces de usuario** responsivas y funcionales

## 🔗 URLs Detectadas en Pruebas

El sistema ha detectado exitosamente URLs de:
- 🐦 **X/Twitter**: Posts de OpenAI y otros
- 📰 **Noticias**: Marca.com, Hoy.es, El País, BBC
- 💻 **GitHub**: Repositorios y documentación
- 🎸 **Blogs especializados**: AprendizDeLuthier.com

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Flask**: Framework web
- **MCP Protocol**: Comunicación con Telegram
- **JSON-RPC**: Protocolo de comunicación
- **HTML5/CSS3/JS**: Frontend moderno
- **NPX**: Ejecución del servidor MCP

## � Seguridad

### Variables de Entorno Protegidas
- **`.env`** está en `.gitignore` - NUNCA se sube al repositorio
- Usa **`.env.example`** como plantilla
- Credenciales solo en tu máquina local

### Configuración Recomendada
```bash
# Configurar .env
cp .env.example .env
# Editar .env con TUS credenciales
```

### ⚠️ IMPORTANTE
- **NUNCA subas credenciales al repositorio**
- **TARGET_CHAT** ahora es opcional (selección dinámica)
- Regenera credenciales si se comprometen

## �📝 Logs y Monitoreo

- Logs guardados en `telegram_monitor.log`
- Formato timestamp con nivel de log
- Encoding UTF-8 para caracteres especiales
- Rotación automática de archivos de resultados

## 🎉 Estado del Proyecto

✅ **COMPLETADO Y FUNCIONAL**
- Monitor CLI operativo
- Detección de URLs exitosa  
- Interfaz web implementada
- Arquitectura limpia y documentada
- Pruebas realizadas con datos reales

---

*Desarrollado con ❤️ para el curso de Programación Asistido por IA*
