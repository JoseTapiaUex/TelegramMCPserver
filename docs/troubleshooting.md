# Guía de Solución de Problemas

Si encuentras algún problema con tu servidor MCP de Telegram, aquí tienes las soluciones más comunes.

## 🔧 Problemas Comunes

### 1. Claude no ve el servidor MCP

**Síntomas:**
- No aparece el icono de herramientas 🔧 en Claude Desktop
- Claude dice que no tiene herramientas disponibles

**Soluciones:**
```powershell
# Verificar que el archivo de configuración existe
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"

# Reiniciar Claude Desktop completamente
# 1. Cerrar Claude Desktop
# 2. Abrir Task Manager (Ctrl+Shift+Esc)
# 3. Terminar cualquier proceso "Claude"
# 4. Abrir Claude Desktop de nuevo
```

### 2. Error de autenticación

**Síntomas:**
- "Authentication failed"
- "Invalid session"

**Soluciones:**
```powershell
# Re-autenticar con Telegram
npx -y @chaindead/telegram-mcp auth --app-id 23082217 --api-hash "4b525537a8164ddf9ce4d098b767e3a1" --phone +34627733998

# Si tienes 2FA activado, añade --password
npx -y @chaindead/telegram-mcp auth --app-id 23082217 --api-hash "4b525537a8164ddf9ce4d098b767e3a1" --phone +34627733998 --password TU_PASSWORD_2FA
```

### 3. Problemas con NPX

**Síntomas:**
- "'npx' is not recognized"
- "Command not found"

**Soluciones:**
```powershell
# Actualizar variables de entorno
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

# Verificar Node.js
node --version
npx --version

# Si no funciona, reinstalar Node.js
winget install OpenJS.NodeJS
```

### 4. Sesión expirada

**Síntomas:**
- "Session expired"
- "Please re-authenticate"

**Solución:**
```powershell
# Limpiar sesión anterior y re-autenticar
Remove-Item "$env:USERPROFILE\.telegram-mcp\session.json" -ErrorAction SilentlyContinue
npx -y @chaindead/telegram-mcp auth --app-id 23082217 --api-hash "4b525537a8164ddf9ce4d098b767e3a1" --phone +34627733998
```

### 5. Problemas de permisos

**Síntomas:**
- "Access denied"
- "Permission error"

**Solución:**
```powershell
# Ejecutar PowerShell como administrador
# Luego repetir la configuración
```

## 🛠️ Comandos de Diagnóstico

### Verificar estado completo
```powershell
# 1. Verificar Node.js
Write-Host "Node.js version:" (node --version)
Write-Host "NPX version:" (npx --version)

# 2. Verificar configuración de Claude
if (Test-Path "$env:APPDATA\Claude\claude_desktop_config.json") {
    Write-Host "✅ Archivo de configuración existe"
    Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
} else {
    Write-Host "❌ Archivo de configuración no encontrado"
}

# 3. Verificar sesión de Telegram
if (Test-Path "$env:USERPROFILE\.telegram-mcp\session.json") {
    Write-Host "✅ Sesión de Telegram existe"
} else {
    Write-Host "❌ Sesión de Telegram no encontrada"
}
```

### Probar conectividad
```powershell
# Probar que el servidor responde
$env:TG_APP_ID = "23082217"
$env:TG_API_HASH = "4b525537a8164ddf9ce4d098b767e3a1"
npx -y @chaindead/telegram-mcp help
```

## 🔄 Reinstalación Completa

Si nada funciona, sigue estos pasos para una reinstalación limpia:

```powershell
# 1. Limpiar caché de NPX
npx clear-npx-cache

# 2. Eliminar sesión actual
Remove-Item "$env:USERPROFILE\.telegram-mcp" -Recurse -Force -ErrorAction SilentlyContinue

# 3. Eliminar configuración de Claude
Remove-Item "$env:APPDATA\Claude\claude_desktop_config.json" -ErrorAction SilentlyContinue

# 4. Reinstalar el servidor
npx -y @chaindead/telegram-mcp help

# 5. Re-autenticar
npx -y @chaindead/telegram-mcp auth --app-id 23082217 --api-hash "4b525537a8164ddf9ce4d098b767e3a1" --phone +34627733998

# 6. Recrear configuración de Claude
@'
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "23082217",
        "TG_API_HASH": "4b525537a8164ddf9ce4d098b767e3a1"
      }
    }
  }
}
'@ | Out-File -FilePath "$env:APPDATA\Claude\claude_desktop_config.json" -Encoding UTF8

# 7. Reiniciar Claude Desktop
```

## 📋 Lista de Verificación

Usa esta lista para verificar que todo está correcto:

- [ ] Node.js instalado (`node --version`)
- [ ] NPX funcionando (`npx --version`)
- [ ] Servidor MCP instalado (`npx -y @chaindead/telegram-mcp help`)
- [ ] Autenticación con Telegram completada
- [ ] Archivo `claude_desktop_config.json` creado
- [ ] Claude Desktop reiniciado
- [ ] Icono de herramientas 🔧 visible en Claude
- [ ] Comandos de Telegram funcionando en Claude

## 🌐 Problemas de Red

### Para redes corporativas o con proxy:

```json
{
  "mcpServers": {
    "telegram": {
      "command": "npx",
      "args": ["-y", "@chaindead/telegram-mcp"],
      "env": {
        "TG_APP_ID": "23082217",
        "TG_API_HASH": "4b525537a8164ddf9ce4d098b767e3a1",
        "HTTP_PROXY": "http://proxy.empresa.com:8080",
        "HTTPS_PROXY": "http://proxy.empresa.com:8080"
      }
    }
  }
}
```

## 🆘 Obtener Ayuda

Si sigues teniendo problemas:

1. **Revisa los logs de Claude Desktop**:
   - Ve a `%APPDATA%\Claude\logs`
   - Busca errores relacionados con MCP

2. **Ejecuta con modo debug**:
   ```powershell
   $env:TG_LOG_LEVEL = "debug"
   npx -y @chaindead/telegram-mcp help
   ```

3. **Crea un issue en GitHub**:
   - [Repositorio original](https://github.com/chaindead/telegram-mcp/issues)
   - Incluye el error completo y tu configuración (sin las credenciales)

4. **Consulta la documentación oficial**:
   - [MCP Documentation](https://modelcontextprotocol.io/)
   - [Telegram API](https://core.telegram.org/api)