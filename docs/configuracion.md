# Configuración Avanzada del Servidor MCP Telegram

Esta guía cubre configuraciones avanzadas y personalizaciones del servidor MCP de Telegram.

## 🔧 Variables de Entorno

### Variables Principales

| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `TG_APP_ID` | API ID de Telegram | `1234567` | ✅ |
| `TG_API_HASH` | API Hash de Telegram | `"abcd1234..."` | ✅ |
| `TG_SESSION_PATH` | Ruta personalizada para la sesión | `"C:\\sessions\\telegram.session"` | ❌ |
| `TG_DEVICE_MODEL` | Modelo de dispositivo personalizado | `"Claude MCP Server"` | ❌ |
| `TG_SYSTEM_VERSION` | Versión del sistema personalizada | `"Windows 11"` | ❌ |
| `TG_APP_VERSION` | Versión de la aplicación | `"1.0.0"` | ❌ |

### Configuración con Variables de Entorno

#### Opción 1: En el archivo de Claude Desktop

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "abcd1234ef567890abcd1234ef567890",
        "TG_SESSION_PATH": "C:\\Users\\TuUsuario\\telegram_session",
        "TG_DEVICE_MODEL": "Claude MCP Server",
        "TG_SYSTEM_VERSION": "Windows 11",
        "TG_APP_VERSION": "1.0.0"
      }
    }
  }
}
```

#### Opción 2: Variables de Sistema (PowerShell)

```powershell
# Configurar variables de entorno temporalmente
$env:TG_APP_ID = "1234567"
$env:TG_API_HASH = "abcd1234ef567890abcd1234ef567890"
$env:TG_SESSION_PATH = "C:\\sessions\\telegram.session"

# Ejecutar el servidor con las variables configuradas
npx -y @chaindead/telegram-mcp
```

#### Opción 3: Variables de Sistema Permanentes

```powershell
# Configurar variables permanentes (requiere reiniciar la sesión)
[Environment]::SetEnvironmentVariable("TG_APP_ID", "1234567", "User")
[Environment]::SetEnvironmentVariable("TG_API_HASH", "tu_api_hash", "User")
```

## 📁 Gestión de Sesiones

### Ubicación Predeterminada de la Sesión

Por defecto, el archivo de sesión se guarda en:
```
%USERPROFILE%\.telegram-mcp\session
```

### Configurar Ubicación Personalizada

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_SESSION_PATH": "D:\\MisCosas\\Telegram\\session.db"
      }
    }
  }
}
```

### Respaldo y Restauración de Sesiones

```powershell
# Hacer respaldo de la sesión
Copy-Item "$env:USERPROFILE\\.telegram-mcp\\session" "D:\\Respaldos\\telegram_session_backup"

# Restaurar sesión
Copy-Item "D:\\Respaldos\\telegram_session_backup" "$env:USERPROFILE\\.telegram-mcp\\session"
```

## 🏢 Configuraciones Multi-Cuenta

### Configurar Múltiples Cuentas de Telegram

```json
{
  "mcpServers": {
    "telegram-personal": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "hash_cuenta_personal",
        "TG_SESSION_PATH": "C:\\sessions\\personal.session"
      }
    },
    "telegram-trabajo": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "7654321",
        "TG_API_HASH": "hash_cuenta_trabajo",
        "TG_SESSION_PATH": "C:\\sessions\\trabajo.session"
      }
    }
  }
}
```

### Autenticación para Múltiples Cuentas

```powershell
# Autenticar cuenta personal
$env:TG_SESSION_PATH = "C:\\sessions\\personal.session"
npx -y @chaindead/telegram-mcp auth --app-id 1234567 --api-hash "hash_personal" --phone +34123456789

# Autenticar cuenta de trabajo
$env:TG_SESSION_PATH = "C:\\sessions\\trabajo.session"
npx -y @chaindead/telegram-mcp auth --app-id 7654321 --api-hash "hash_trabajo" --phone +34987654321
```

## 🔐 Configuración de Seguridad

### Permisos de Archivos

```powershell
# Asegurar que solo tu usuario puede leer la sesión
$sessionPath = "$env:USERPROFILE\\.telegram-mcp\\session"
icacls $sessionPath /inheritance:d
icacls $sessionPath /grant:r "$env:USERNAME:F" /remove "Everyone" "Users" "Authenticated Users"
```

### Cifrado de Configuración

Para mayor seguridad, puedes usar variables de entorno en lugar de texto plano en el archivo de configuración:

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "${TG_APP_ID}",
        "TG_API_HASH": "${TG_API_HASH}"
      }
    }
  }
}
```

## 🌐 Configuración de Proxy

### Para Redes Corporativas o Países con Restricciones

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "HTTP_PROXY": "http://proxy.empresa.com:8080",
        "HTTPS_PROXY": "http://proxy.empresa.com:8080"
      }
    }
  }
}
```

### Con Autenticación de Proxy

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "HTTP_PROXY": "http://usuario:password@proxy.empresa.com:8080",
        "HTTPS_PROXY": "http://usuario:password@proxy.empresa.com:8080"
      }
    }
  }
}
```

## 📊 Configuración de Logging

### Habilitar Logs Detallados

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_LOG_LEVEL": "debug",
        "TG_LOG_FILE": "C:\\logs\\telegram-mcp.log"
      }
    }
  }
}
```

### Niveles de Log Disponibles

- `error`: Solo errores críticos
- `warn`: Advertencias y errores
- `info`: Información general (predeterminado)
- `debug`: Información detallada para depuración

## ⚡ Optimización de Rendimiento

### Configuración para Alto Volumen de Mensajes

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_MAX_CONCURRENT_REQUESTS": "10",
        "TG_REQUEST_TIMEOUT": "30000",
        "TG_RETRY_ATTEMPTS": "3"
      }
    }
  }
}
```

### Configuración de Cache

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_CACHE_SIZE": "1000",
        "TG_CACHE_TTL": "300"
      }
    }
  }
}
```

## 🔄 Configuración de Actualización Automática

### Script de Actualización Automática

```powershell
# Crear tarea programada para actualizar el servidor
$trigger = New-ScheduledTaskTrigger -Daily -At "02:00"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-Command npm update -g @chaindead/telegram-mcp"
Register-ScheduledTask -TaskName "UpdateTelegramMCP" -Trigger $trigger -Action $action -Description "Actualizar servidor MCP de Telegram diariamente"
```

## 🎛️ Configuración de Desarrollo

### Para Desarrolladores que Quieren Contribuir

```json
{
  "mcpServers": {
    "telegram-dev": {
      "command": "node",
      "args": ["C:\\dev\\telegram-mcp\\dist\\index.js"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "NODE_ENV": "development",
        "TG_LOG_LEVEL": "debug"
      }
    }
  }
}
```

### Configuración para Testing

```json
{
  "mcpServers": {
    "telegram-test": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_TEST_MODE": "true",
        "TG_MOCK_API": "true"
      }
    }
  }
}
```

## 📋 Validación de Configuración

### Script de Validación

```powershell
# Verificar configuración
$configPath = "$env:APPDATA\\Claude\\claude_desktop_config.json"
if (Test-Path $configPath) {
    $config = Get-Content $configPath | ConvertFrom-Json
    if ($config.mcpServers.telegram) {
        Write-Host "✅ Configuración de Telegram MCP encontrada" -ForegroundColor Green
        Write-Host "   Command: $($config.mcpServers.telegram.command)"
        Write-Host "   Args: $($config.mcpServers.telegram.args -join ' ')"
    } else {
        Write-Host "❌ No se encontró configuración de Telegram MCP" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Archivo de configuración de Claude no encontrado" -ForegroundColor Red
}
```

## 🚨 Recuperación ante Fallos

### Configuración de Reinicio Automático

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "1234567",
        "TG_API_HASH": "tu_api_hash",
        "TG_AUTO_RESTART": "true",
        "TG_MAX_RESTART_ATTEMPTS": "5",
        "TG_RESTART_DELAY": "5000"
      }
    }
  }
}
```

Esta configuración avanzada te permitirá personalizar completamente tu servidor MCP de Telegram según tus necesidades específicas.