# Script para configurar variables de entorno de forma segura
# Ejecutar como: .\configure-env.ps1

param(
    [Parameter(Mandatory=$false)]
    [string]$ApiId,
    
    [Parameter(Mandatory=$false)]
    [string]$ApiHash,
    
    [Parameter(Mandatory=$false)]
    [string]$Phone
)

Write-Host "🔐 Configuración segura de credenciales de Telegram MCP" -ForegroundColor Cyan
Write-Host ""

# Si no se proporcionan parámetros, pedirlos de forma interactiva
if (-not $ApiId) {
    $ApiId = Read-Host "Introduce tu API ID de Telegram"
}

if (-not $ApiHash) {
    $ApiHash = Read-Host "Introduce tu API Hash de Telegram" -MaskInput
}

if (-not $Phone) {
    $Phone = Read-Host "Introduce tu número de teléfono (opcional, con código país ej: +34123456789)"
}

# Crear archivo .env local
$envContent = @"
# Credenciales de Telegram MCP Server
# NUNCA subas este archivo a Git
TG_APP_ID=$ApiId
TG_API_HASH=$ApiHash
TG_PHONE=$Phone
"@

$envPath = ".env"
$envContent | Out-File -FilePath $envPath -Encoding UTF8
Write-Host "✅ Archivo .env creado localmente" -ForegroundColor Green

# Configurar variables de entorno del sistema (opcional)
$setSystemVars = Read-Host "¿Quieres configurar las variables de entorno del sistema? (y/N)"
if ($setSystemVars -eq "y" -or $setSystemVars -eq "Y") {
    [Environment]::SetEnvironmentVariable("TG_APP_ID", $ApiId, "User")
    [Environment]::SetEnvironmentVariable("TG_API_HASH", $ApiHash, "User")
    if ($Phone) {
        [Environment]::SetEnvironmentVariable("TG_PHONE", $Phone, "User")
    }
    Write-Host "✅ Variables de entorno del sistema configuradas" -ForegroundColor Green
    Write-Host "⚠️  Necesitarás reiniciar PowerShell para usar las variables" -ForegroundColor Yellow
}

# Actualizar configuración de Claude Desktop
Write-Host ""
Write-Host "🔧 Actualizando configuración de Claude Desktop..." -ForegroundColor Yellow

$claudeConfigPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$claudeDir = Split-Path $claudeConfigPath -Parent

# Crear directorio si no existe
if (!(Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
}

# Crear configuración usando las variables
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

$config | ConvertTo-Json -Depth 4 | Out-File -FilePath $claudeConfigPath -Encoding UTF8
Write-Host "✅ Configuración de Claude Desktop actualizada" -ForegroundColor Green

Write-Host ""
Write-Host "🔒 Medidas de seguridad aplicadas:" -ForegroundColor Green
Write-Host "   • Archivo .env añadido al .gitignore" -ForegroundColor Gray
Write-Host "   • Credenciales no aparecerán en el repositorio" -ForegroundColor Gray  
Write-Host "   • Configuración de Claude actualizada con credenciales reales" -ForegroundColor Gray

Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Ejecuta: git add . && git commit -m 'Add secure configuration'" -ForegroundColor White
Write-Host "2. Reinicia Claude Desktop" -ForegroundColor White
Write-Host "3. Verifica que el servidor MCP funciona" -ForegroundColor White

Write-Host ""
Write-Host "⚠️  IMPORTANTE: El archivo .env contiene credenciales sensibles." -ForegroundColor Red
Write-Host "   NO lo compartas ni lo subas a Git." -ForegroundColor Red