# Script de configuración para la integración con Jira
# Ejecutar con: powershell -ExecutionPolicy Bypass -File setup_jira_integration.ps1

Write-Host "🚀 Configurando integración con Jira para pruebas automatizadas" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "🐍 Verificando instalación de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Instala Python antes de continuar." -ForegroundColor Red
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

# Crear archivo .env si no existe
Write-Host ""
Write-Host "⚙️ Configurando variables de entorno..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Write-Host "📝 Creando archivo .env desde .env.example..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Archivo .env ya existe" -ForegroundColor Cyan
}

# Crear directorio de screenshots
Write-Host ""
Write-Host "📸 Configurando directorio de screenshots..." -ForegroundColor Yellow
if (-not (Test-Path "screenshots")) {
    New-Item -ItemType Directory -Name "screenshots"
    Write-Host "✅ Directorio screenshots creado" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Directorio screenshots ya existe" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🔧 CONFIGURACIÓN NECESARIA:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Edita el archivo .env con tus credenciales de Jira:" -ForegroundColor White
Write-Host "   - JIRA_URL=https://tu-empresa.atlassian.net" -ForegroundColor Gray
Write-Host "   - JIRA_USERNAME=tu-email@empresa.com" -ForegroundColor Gray
Write-Host "   - JIRA_API_TOKEN=tu-api-token" -ForegroundColor Gray
Write-Host "   - JIRA_PROJECT_KEY=TU_PROYECTO" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Para obtener tu API Token de Jira:" -ForegroundColor White
Write-Host "   - Ve a: https://id.atlassian.com/manage-profile/security/api-tokens" -ForegroundColor Blue
Write-Host "   - Crea un nuevo token" -ForegroundColor Gray
Write-Host "   - Copia el token al archivo .env" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configura las otras variables según tu entorno" -ForegroundColor White
Write-Host ""

# Preguntar si ejecutar prueba de configuración
$testConfig = Read-Host "¿Deseas ejecutar la prueba de configuración de Jira ahora? (y/n)"

if ($testConfig -eq "y" -or $testConfig -eq "yes") {
    Write-Host ""
    Write-Host "🧪 Ejecutando prueba de configuración..." -ForegroundColor Yellow
    python test_jira_integration.py
}

Write-Host ""
Write-Host "🎉 ¡Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Configura tu archivo .env con las credenciales de Jira" -ForegroundColor White
Write-Host "2. Ejecuta: python test_jira_integration.py (para probar la configuración)" -ForegroundColor White
Write-Host "3. Ejecuta: python main.py (para correr las pruebas con integración Jira)" -ForegroundColor White
Write-Host ""
Write-Host "📚 Ver README_JIRA.md para documentación completa" -ForegroundColor Cyan
