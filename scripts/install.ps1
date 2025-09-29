# Script de instalación automática para Telegram MCP Server
# Ejecutar como: .\install.ps1

Write-Host "🚀 Instalando Telegram MCP Server..." -ForegroundColor Cyan

# Verificar Node.js
Write-Host "📦 Verificando Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js encontrado: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js no encontrado. Instala Node.js desde https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Verificar NPX
Write-Host "📦 Verificando NPX..." -ForegroundColor Yellow
try {
    $npxVersion = npx --version
    Write-Host "✅ NPX encontrado: $npxVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ NPX no encontrado" -ForegroundColor Red
    exit 1
}

# Instalar el servidor MCP
Write-Host "📥 Descargando Telegram MCP Server..." -ForegroundColor Yellow
try {
    npx -y @chaindead/telegram-mcp --version
    Write-Host "✅ Telegram MCP Server instalado correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error instalando el servidor MCP" -ForegroundColor Red
    exit 1
}

# Verificar Claude Desktop
Write-Host "🔍 Verificando Claude Desktop..." -ForegroundColor Yellow
$claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
if (Test-Path $claudeConfigPath) {
    Write-Host "✅ Archivo de configuración de Claude encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Archivo de configuración de Claude no encontrado" -ForegroundColor Yellow
    Write-Host "   Se creará cuando configures el servidor" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🎉 ¡Instalación completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Obtén tu API ID y Hash de https://my.telegram.org/auth" -ForegroundColor White
Write-Host "2. Ejecuta: npx -y @chaindead/telegram-mcp auth --app-id TU_ID --api-hash TU_HASH --phone TU_TELEFONO" -ForegroundColor White
Write-Host "3. Configura Claude Desktop con el archivo example en /config/" -ForegroundColor White
Write-Host "4. Reinicia Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "📚 Consulta docs/instalacion.md para más detalles" -ForegroundColor Gray