# 🤖 Telegram Monitor - Agente de Monitoreo Inteligente

> **Proyecto desarrollado para curso de Programación Asistido por IA**  
> Monitor automático de chats de Telegram con detección de URLs y contenido

## 📊 Estructura de Datos

### 📁 Archivos Generados
```
results/
├── message_YYYYMMDD_HHMMSS_*.json    # Mensajes capturados
└── url_YYYYMMDD_HHMMSS_*.json        # URLs con metadata
```

### 📄 Formato de Datos
```json
// Ejemplo de mensaje capturado
{
  "message_id": 12345,
  "text": "Contenido del mensaje", 
  "from_user": "usuario",
  "timestamp": "2025-10-01T01:35:07.965000",
  "chat": "nombre_del_chat"
}
```

## 🛠️ Stack Tecnológico

- **🐍 Backend**: Python 3.8+ + Flask
- **🌐 Frontend**: HTML5, CSS3, JavaScript
- **📡 Protocolo**: MCP (Model Context Protocol)
- **🔄 APIs**: JSON-RPC 2.0 
- **💾 Datos**: JSON local + logs estructurados

## 📝 Logs y Diagnósticos

- **Logs detallados**: `telegram_monitor.log`
- **Formato estructurado**: Timestamp + nivel + mensaje
- **Encoding UTF-8**: Soporte completo caracteres especiales
- **Rotación automática**: Gestión eficiente de archivos

## 🎉 Estado del Proyecto

### ✅ **COMPLETADO Y FUNCIONAL**
- 🎛️ **Setup UX optimizado**: Flujo simplificado primer uso
- 📊 **Dashboard completo**: Interfaz moderna y responsive
- 🔄 **Monitoreo dinámico**: Selección multi-chat en tiempo real  
- 🔗 **Detección avanzada**: URLs con metadata completo
- 💾 **Persistencia robusta**: Datos JSON + logs estructurados
- 🔒 **Seguridad implementada**: Credenciales protegidas

### 🚀 **Casos de Uso Validados**
- Monitoreo de grupos de Telegram en tiempo real
- Detección automática de URLs compartidas
- Dashboard interactivo para control y visualización
- Setup seguro y amigable para nuevos usuarios

---

*💡 Desarrollado con ❤️ para el curso de **Programación Asistida por IA***

🎯 **Demo funcional**: `python run.py --web` → http://localhost:5000

## 🎯 Características Principales

- ✅ **Monitoreo en tiempo real** de cualquier chat de Telegram
- 🔗 **Detección automática de URLs** en mensajes
- 💾 **Guardado local** de mensajes y URLs en formato JSON
- 🌐 **Interfaz web moderna** con dashboard interactivo
- 🚀 **Arquitectura MCP** (Model Context Protocol) con Telegram
- 📊 **Estadísticas en tiempo real** y métricas de actividad
- 🎯 **Selección dinámica de chats** - sin configuración previa
- 🔒 **Setup seguro** con flujo UX optimizado

## 🏗️ Arquitectura del Sistema

```
telegram-monitor-agent/
├── run.py                    # 🚀 Punto de entrada principal
├── simple_monitor.py         # ⚙️ Lógica de monitoreo
├── web_server.py            # 🌐 Servidor Flask + APIs
├── web/
│   ├── index.html          # � Dashboard principal
│   └── setup.html          # ⚙️ Configuración inicial
├── results/                # 💾 Datos JSON generados
├── requirements.txt        # 📦 Dependencias Python
├── .env                   # 🔑 Credenciales (local)
├── .env.example          # 📋 Plantilla de configuración
└── README.md            # 📚 Esta documentación
```

## 🚀 Instalación y Configuración

### 1. Prerrequisitos
- **Python 3.8+** instalado
- **Node.js** (para MCP server de Telegram)
- Cuenta de Telegram y API keys

### 2. Clonar y configurar
```bash
# Clonar el repositorio
git clone https://github.com/JoseTapiaUex/Telegram-monitor-agent.git
cd Telegram-monitor-agent

# Crear entorno virtual (recomendado)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar MCP server de Telegram
npm install -g @chaindead/telegram-mcp
```

1. Ve a https://my.telegram.org/apps
2. Inicia sesión con tu cuenta de Telegram  
3. Crea una nueva aplicación
4. Anota tu `API ID` y `API Hash`

## 💻 Ejecución

### 🌐 Modo Web (Recomendado)
```bash
# Iniciar servidor con interfaz web
python run.py --web
```

**🎯 Primer uso**: El sistema detecta automáticamente si necesitas configuración y te redirige al setup.

**🚀 Usos posteriores**: Acceso directo al dashboard en `http://localhost:5000`

### ⚡ Modo CLI (Avanzado)  
```bash
# Ejecutar monitor directo en consola
python simple_monitor.py
```

## 🎮 Flujo de Trabajo

### 📋 Configuración Inicial (Solo primer uso)
1. **Ejecuta**: `python run.py --web`
2. **Setup automático**: Se abre el navegador en `http://localhost:5000/setup`
3. **Introduce credenciales**: API ID, API Hash, y número de teléfono
4. **Verificación**: El sistema autentica con Telegram
5. **¡Listo!**: Redirige automáticamente al dashboard

### 🚀 Uso Normal (Posteriores ejecuciones)
1. **Ejecuta**: `python run.py --web` 
2. **Dashboard directo**: Se abre automáticamente en `http://localhost:5000`
3. **Selecciona chat**: Elige dinámicamente qué chat monitorizar
4. **Inicia monitoreo**: Un clic para comenzar la captura en tiempo real

## 📊 Características del Dashboard

- **🎛️ Control Total**: Iniciar/pausar/detener monitoreo con un clic
- **📈 Métricas en Vivo**: Contador de mensajes, URLs, y actividad
- **💬 Feed en Tiempo Real**: Stream de mensajes capturados
- **🔗 Análisis de URLs**: Lista completa con metadata de enlaces
- **📊 Estadísticas**: Gráficos de actividad y tendencias
- **🎯 Multi-chat**: Cambio dinámico entre diferentes chats
- **💾 Exportación**: Descarga de datos en formato JSON
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
