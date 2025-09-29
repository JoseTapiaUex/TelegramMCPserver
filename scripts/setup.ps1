# Script de configuración rápida para Telegram MCP Server
# Ejecutar como: .\setup.ps1

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiId,
    
    [Parameter(Mandatory=$true)]
    [string]$ApiHash,
    
    [Parameter(Mandatory=$true)]
    [string]$Phone
)

Write-Host "⚡ Configuración rápida de Telegram MCP Server" -ForegroundColor Cyan
Write-Host ""

# Step 1: Autenticación
Write-Host "🔐 Configurando autenticación..." -ForegroundColor Yellow
try {
    npx -y @chaindead/telegram-mcp auth --app-id $ApiId --api-hash $ApiHash --phone $Phone
    Write-Host "✅ Autenticación completada" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en la autenticación" -ForegroundColor Red
    Write-Host "Verifica que los datos sean correctos y que hayas introducido el código de Telegram" -ForegroundColor Gray
    exit 1
}

# Step 2: Configurar Claude Desktop
Write-Host "🔧 Configurando Claude Desktop..." -ForegroundColor Yellow

$claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$claudeDir = Split-Path $claudeConfigPath -Parent

# Crear directorio si no existe
if (!(Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
    Write-Host "📁 Creado directorio de configuración de Claude" -ForegroundColor Gray
}

# Crear configuración
$config = @{
    mcpServers = @{
        telegram = @{
            command = "npx"
            args = @("-y", "@chaindead/telegram-mcp")
            env = @{
                TG_APP_ID = $ApiId
                TG_API_HASH = $ApiHash
            }
        }
    }
}

# Escribir configuración
$config | ConvertTo-Json -Depth 4 | Out-File -FilePath $claudeConfigPath -Encoding UTF8
Write-Host "✅ Configuración de Claude Desktop actualizada" -ForegroundColor Green

# Step 3: Verificar configuración
Write-Host "🧪 Verificando configuración..." -ForegroundColor Yellow
try {
    npx -y @chaindead/telegram-mcp me | Out-Null
    Write-Host "✅ Servidor MCP funcionando correctamente" -ForegroundColor Green
} catch {
    Write-Host "⚠️  No se pudo verificar la conexión" -ForegroundColor Yellow
    Write-Host "   Esto puede ser normal si no has introducido el código de verificación aún" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🎉 ¡Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Últimos pasos:" -ForegroundColor Cyan
Write-Host "1. Reinicia Claude Desktop completamente" -ForegroundColor White
Write-Host "2. Abre Claude Desktop y verifica que veas el icono de herramientas 🔧" -ForegroundColor White
Write-Host "3. Prueba con: '¿Puedes mostrarme información de mi cuenta de Telegram?'" -ForegroundColor White
Write-Host ""
Write-Host "📁 Configuración guardada en:" -ForegroundColor Gray
Write-Host "   $claudeConfigPath" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Más ejemplos en docs/ejemplos.md" -ForegroundColor Gray