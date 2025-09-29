# Telegram MCP Server

Servidor MCP (Model Context Protocol) para conectar Claude Desktop con Telegram y poder leer/gestionar mensajes directamente desde Claude.

## 🎯 Objetivo

Configurar un servidor MCP que permita a Claude Desktop acceder a tus mensajes de Telegram, facilitando la gestión y análisis de conversaciones desde la interfaz de Claude.

## 📋 Requisitos Previos

- Windows 10/11
- Node.js instalado
- Cuenta de Telegram
- Claude Desktop instalado
- PowerShell

## 🚀 Guía de Instalación Rápida

### Paso 1: Instalación del Servidor MCP

```powershell
# Instalar el servidor MCP de Telegram usando NPX
npx -y @chaindead/telegram-mcp
```

### Paso 2: Obtener Credenciales de Telegram

1. Ve a [https://my.telegram.org/auth](https://my.telegram.org/auth)
2. Inicia sesión con tu número de teléfono
3. Ve a "API development tools"
4. Crea una nueva aplicación y obtén:
   - `api_id` (TG_APP_ID)
   - `api_hash` (TG_API_HASH)

### Paso 3: Autenticación

```powershell
# Ejecutar el comando de autenticación
npx -y @chaindead/telegram-mcp auth --app-id TU_API_ID --api-hash TU_API_HASH --phone TU_NUMERO
```

Sigue las instrucciones para introducir el código que recibirás por Telegram.

### Paso 4: Configurar de Forma Segura

**Opción A: Usando el script automático (Recomendado)**

```powershell
# Ejecutar el script de configuración segura
.\scripts\configure-env.ps1
```

**Opción B: Configuración manual**

1. Copia el archivo de ejemplo: `cp .env.example .env`
2. Edita `.env` con tus credenciales reales
3. El archivo de configuración de Claude se actualizará automáticamente

⚠️ **IMPORTANTE**: Las credenciales están protegidas por `.gitignore` y no se subirán al repositorio.

## 🛠️ Funcionalidades Disponibles

El servidor MCP de Telegram proporciona las siguientes herramientas:

- **`tg_me`**: Obtener información de la cuenta actual
- **`tg_dialogs`**: Listar diálogos/chats (con filtro de no leídos opcional)
- **`tg_read`**: Marcar diálogo como leído
- **`tg_dialog`**: Obtener mensajes de un diálogo específico
- **`tg_send`**: Enviar mensajes a cualquier diálogo

## 💡 Ejemplos de Uso

### Gestión de Mensajes

```
"Verifica si tengo mensajes importantes sin leer en Telegram"
"Resume todos mis mensajes no leídos de Telegram"
"Lee y analiza mis mensajes no leídos, prepara borradores de respuesta donde sea necesario"
```

### Organización

```
"Analiza mis diálogos de Telegram y sugiere una estructura de carpetas"
"Ayúdame a categorizar mis chats de Telegram por importancia"
"Encuentra todas las conversaciones relacionadas con trabajo"
```

### Comunicación

```
"Monitorea un chat específico en busca de actualizaciones sobre [tema]"
"Redacta una respuesta educada al último mensaje en [chat]"
"Verifica si hay preguntas sin responder en mis chats"
```

## 📁 Estructura del Proyecto

```
TelegramMCPserver/
├── README.md                 # Este archivo
├── docs/                    # Documentación
│   ├── instalacion.md       # Guía de instalación
│   ├── configuracion.md     # Configuración avanzada
│   └── ejemplos.md          # Ejemplos de uso
├── config/                  # Archivos de configuración
│   └── claude_config_example.json
└── scripts/                 # Scripts de automatización
    ├── install.ps1          # Instalación automática
    └── setup.ps1            # Configuración rápida
```

## 🔧 Configuración Avanzada

### Variables de Entorno

Puedes configurar las siguientes variables de entorno:

- `TG_APP_ID`: Tu API ID de Telegram
- `TG_API_HASH`: Tu API Hash de Telegram
- `TG_SESSION_PATH`: Ruta personalizada para el archivo de sesión

### Configuración Personalizada

Para configuraciones más avanzadas, consulta la [documentación de configuración](docs/configuracion.md).

## 🐛 Solución de Problemas

### Problemas Comunes

1. **Error de autenticación**: Verifica que tu API ID y Hash sean correctos
2. **Claude no ve el servidor**: Reinicia Claude Desktop después de cambiar la configuración
3. **Problemas de permisos**: Ejecuta PowerShell como administrador

Para más ayuda, consulta [troubleshooting.md](docs/troubleshooting.md).

## 📚 Recursos Adicionales

- [Documentación oficial de MCP](https://modelcontextprotocol.io/)
- [API de Telegram](https://core.telegram.org/api)
- [Términos de servicio de Telegram API](https://core.telegram.org/api/terms)

## 🔒 Seguridad

**Credenciales protegidas**: Este proyecto usa `.gitignore` para proteger tus credenciales de Telegram. Nunca se subirán al repositorio.

**Archivos sensibles**:
- `.env` - Variables de entorno locales
- `config/claude_desktop_config.json` - Configuración con credenciales
- `.telegram-mcp/` - Archivos de sesión de Telegram

## ⚠️ Importante

Asegúrate de haber leído y entendido los [Términos de Servicio de la API de Telegram](https://core.telegram.org/api/terms) antes de usar este servidor. El mal uso de la API de Telegram puede resultar en la suspensión de tu cuenta.

## 🔗 Referencias

- Basado en: [chaindead/telegram-mcp](https://github.com/chaindead/telegram-mcp)
- Documentación MCP: [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- API de Telegram: [core.telegram.org/api](https://core.telegram.org/api)

## 📄 Licencia

MIT License

---

**¿Problemas?** Revisa la [documentación](docs/) o los issues del [repositorio original](https://github.com/chaindead/telegram-mcp/issues).
