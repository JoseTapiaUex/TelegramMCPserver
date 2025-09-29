# Guía Detallada de Instalación

Esta guía te llevará paso a paso para configurar el servidor MCP de Telegram en Windows.

## 📋 Verificación de Requisitos Previos

### 1. Verificar Node.js

Abre PowerShell y ejecuta:

```powershell
node --version
npm --version
```

Si no tienes Node.js instalado:
1. Ve a [nodejs.org](https://nodejs.org)
2. Descarga la versión LTS
3. Instala siguiendo las instrucciones

### 2. Verificar Claude Desktop

Asegúrate de tener Claude Desktop instalado y funcionando:
- Descarga desde [claude.ai](https://claude.ai/desktop)
- Instala y configura tu cuenta

### 3. Verificar PowerShell

Asegúrate de usar PowerShell 5.1 o superior:

```powershell
$PSVersionTable.PSVersion
```

## 🔑 Obtener Credenciales de Telegram API

### Paso 1: Acceder al Portal de Desarrollo

1. Ve a [https://my.telegram.org/auth](https://my.telegram.org/auth)
2. Introduce tu número de teléfono (incluye el código de país, ej: +34123456789)
3. Telegram te enviará un código de verificación
4. Introduce el código recibido

### Paso 2: Crear una Aplicación

1. Una vez autenticado, ve a "API development tools"
2. Rellena el formulario:
   - **App title**: "MCP Telegram Server" (o el nombre que prefieras)
   - **Short name**: "mcp-telegram" (solo letras minúsculas, números y guiones)
   - **Platform**: Puedes seleccionar "Other"
   - **Description**: "Servidor MCP para conectar Claude con Telegram"

3. Haz clic en "Create application"

### Paso 3: Guardar las Credenciales

Guarda de forma segura:
- **api_id**: Un número (ej: 1234567)
- **api_hash**: Una cadena alfanumérica (ej: "abcd1234ef567890...")

⚠️ **Importante**: Nunca compartas estas credenciales públicamente.

## 📦 Instalación del Servidor MCP

### Opción 1: Instalación Directa con NPX (Recomendada)

```powershell
# Verificar que npx funciona
npx --version

# Instalar y ejecutar el servidor MCP de Telegram
npx -y @chaindead/telegram-mcp --version
```

### Opción 2: Instalación Global

```powershell
# Instalar globalmente
npm install -g @chaindead/telegram-mcp

# Verificar instalación
telegram-mcp --version
```

## 🔐 Configuración de Autenticación

### Paso 1: Ejecutar el Comando de Autenticación

Sustituye los valores por tus credenciales reales:

```powershell
npx -y @chaindead/telegram-mcp auth --app-id TU_API_ID --api-hash TU_API_HASH --phone TU_NUMERO_TELEFONO
```

Ejemplo:
```powershell
npx -y @chaindead/telegram-mcp auth --app-id 1234567 --api-hash "abcd1234ef567890abcd1234ef567890" --phone +34123456789
```

### Paso 2: Verificación por SMS

1. El comando te pedirá que introduzcas el código que recibirás por Telegram
2. Introduce el código sin espacios ni guiones
3. Si todo va bien, verás un mensaje de confirmación

### Paso 3: Autenticación de Dos Factores (Si la tienes activada)

Si tienes 2FA activada en Telegram, añade el parámetro `--password`:

```powershell
npx -y @chaindead/telegram-mcp auth --app-id TU_API_ID --api-hash TU_API_HASH --phone TU_NUMERO --password TU_PASSWORD_2FA
```

### Paso 4: Verificar la Autenticación

Ejecuta un comando de prueba:

```powershell
npx -y @chaindead/telegram-mcp me
```

Deberías ver información de tu cuenta de Telegram.

## 🔧 Configuración de Claude Desktop

### Paso 1: Localizar el Archivo de Configuración

El archivo de configuración está en:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Para abrirlo rápidamente:

```powershell
# Abrir la carpeta de configuración
explorer "%APPDATA%\Claude"

# O abrir directamente el archivo (si existe)
notepad "%APPDATA%\Claude\claude_desktop_config.json"
```

### Paso 2: Crear o Modificar la Configuración

Si el archivo no existe, créalo. El contenido debe ser:

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "TU_API_ID",
        "TG_API_HASH": "TU_API_HASH"
      }
    }
  }
}
```

Si ya tienes otros servidores MCP configurados, añade la sección "telegram" dentro de "mcpServers":

```json
{
  "mcpServers": {
    "otro-servidor": {
      "command": "otro-comando"
    },
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "TU_API_ID",
        "TG_API_HASH": "TU_API_HASH"
      }
    }
  }
}
```

### Paso 3: Sustituir las Variables

Reemplaza:
- `TU_API_ID` con tu api_id (sin comillas, es un número)
- `TU_API_HASH` con tu api_hash (entre comillas)

Ejemplo final:
```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "abcd1234ef567890abcd1234ef567890"
      }
    }
  }
}
```

### Paso 4: Reiniciar Claude Desktop

1. Cierra completamente Claude Desktop
2. Espera unos segundos
3. Vuelve a abrir Claude Desktop

## ✅ Verificación de la Instalación

### Paso 1: Comprobar que Claude Ve el Servidor

En una conversación nueva en Claude Desktop, deberías ver un icono de herramientas 🔧 que indica que hay servidores MCP conectados.

### Paso 2: Probar una Función Básica

Pregunta a Claude:

```
"¿Puedes mostrarme información de mi cuenta de Telegram?"
```

Claude debería usar la herramienta `tg_me` y mostrarte información de tu cuenta.

### Paso 3: Probar Listado de Chats

```
"¿Puedes mostrarme mis chats de Telegram?"
```

Claude debería usar la herramienta `tg_dialogs` y listar tus conversaciones.

## 🔄 Actualización del Servidor

Para actualizar a la última versión:

```powershell
# Con NPX (se actualiza automáticamente)
npx -y @chaindead/telegram-mcp --version

# Con instalación global
npm update -g @chaindead/telegram-mcp
```

## 📝 Notas Importantes

1. **Seguridad**: Nunca compartas tu archivo de configuración de Claude que contiene las credenciales de Telegram.

2. **Sesiones**: El servidor guarda una sesión de Telegram en tu sistema. Si cambias de dispositivo, necesitarás autenticarte de nuevo.

3. **Límites de API**: Respeta los límites de uso de la API de Telegram para evitar restricciones.

4. **Firewall**: Si tienes problemas de conexión, verifica que tu firewall no bloquee las conexiones de Node.js.

## 🆘 ¿Problemas?

Si encuentras problemas durante la instalación, consulta la [guía de solución de problemas](troubleshooting.md) o crea un issue en este repositorio con los detalles del error.