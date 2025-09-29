# Script de prueba de conexión del servidor MCP Telegram
# Ejecutar como: .\test-connection.ps1

Write-Host "🧪 Probando la configuración del servidor MCP de Telegram..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Verificar Node.js
Write-Host "1️⃣ Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "   ✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Node.js no encontrado" -ForegroundColor Red
    exit 1
}

# Test 2: Verificar NPX
Write-Host "2️⃣ Verificando NPX..." -ForegroundColor Yellow
try {
    $npxVersion = npx --version
    Write-Host "   ✅ NPX: $npxVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ NPX no encontrado" -ForegroundColor Red
    exit 1
}

# Test 3: Verificar servidor MCP
Write-Host "3️⃣ Verificando servidor MCP..." -ForegroundColor Yellow
$env:TG_APP_ID = "23082217"
$env:TG_API_HASH = "4b525537a8164ddf9ce4d098b767e3a1"
try {
    $mcpOutput = npx -y @chaindead/telegram-mcp help 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Servidor MCP responde correctamente" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Servidor MCP instalado pero con advertencias" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Error al conectar con el servidor MCP" -ForegroundColor Red
}

# Test 4: Verificar archivo de configuración de Claude
Write-Host "4️⃣ Verificando configuración de Claude..." -ForegroundColor Yellow
$claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $claudeConfigPath) {
    Write-Host "   ✅ Archivo de configuración existe" -ForegroundColor Green
    try {
        $config = Get-Content $claudeConfigPath | ConvertFrom-Json
        if ($config.mcpServers.telegram) {
            Write-Host "   ✅ Configuración de Telegram MCP encontrada" -ForegroundColor Green
        } else {
            Write-Host "   ❌ Configuración de Telegram MCP no encontrada" -ForegroundColor Red
        }
    } catch {
        Write-Host "   ❌ Error al leer la configuración" -ForegroundColor Red
    }
} else {
    Write-Host "   ❌ Archivo de configuración no encontrado" -ForegroundColor Red
}

# Test 5: Verificar sesión de Telegram
Write-Host "5️⃣ Verificando sesión de Telegram..." -ForegroundColor Yellow
$sessionPath = "$env:USERPROFILE\.telegram-mcp\session.json"
if (Test-Path $sessionPath) {
    Write-Host "   ✅ Sesión de Telegram encontrada" -ForegroundColor Green
} else {
    Write-Host "   ❌ Sesión de Telegram no encontrada" -ForegroundColor Red
    Write-Host "   💡 Ejecuta: npx -y @chaindead/telegram-mcp auth --app-id 23082217 --api-hash \"4b525537a8164ddf9ce4d098b767e3a1\" --phone +34627733998" -ForegroundColor Gray
}

# Test 6: Probar conectividad con Telegram (si la sesión existe)
if (Test-Path $sessionPath) {
    Write-Host "6️⃣ Probando conectividad con Telegram..." -ForegroundColor Yellow
    try {
        # Intentar obtener información de la cuenta
        $telegramTest = npx -y @chaindead/telegram-mcp --dry 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Conectividad con Telegram OK" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Conectividad con Telegram con advertencias" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ❌ Error al conectar con Telegram" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📋 Resumen de la configuración:" -ForegroundColor Cyan
Write-Host "   • API ID: 23082217" -ForegroundColor Gray
Write-Host "   • API Hash: 4b525537...3a1" -ForegroundColor Gray
Write-Host "   • Teléfono: +34627733998" -ForegroundColor Gray
Write-Host "   • Archivo de configuración: $claudeConfigPath" -ForegroundColor Gray
Write-Host "   • Archivo de sesión: $sessionPath" -ForegroundColor Gray

Write-Host ""
Write-Host "🎯 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Asegúrate de que Claude Desktop esté completamente cerrado" -ForegroundColor White
Write-Host "2. Abre Claude Desktop" -ForegroundColor White
Write-Host "3. Busca el icono de herramientas 🔧 en la interfaz" -ForegroundColor White
Write-Host "4. Prueba con: '¿Puedes mostrarme información de mi cuenta de Telegram?'" -ForegroundColor White

Write-Host ""
Write-Host "📚 Para más ayuda, consulta docs/troubleshooting.md" -ForegroundColor Gray