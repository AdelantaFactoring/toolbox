# 🚀 Script PowerShell para instalar Adelanta Toolbox desde AWS CodeArtifact
# Usar este script en lugar de la instalación manual

Write-Host "🔧 ADELANTA TOOLBOX - Instalación desde CodeArtifact" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# 1. Login a CodeArtifact
Write-Host "🔑 Autenticando con AWS CodeArtifact..." -ForegroundColor Yellow
try {
    aws codeartifact login --tool pip --repository adelanta-toolbox --domain adelanta --region us-east-2
    Write-Host "✅ Autenticación exitosa" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error en autenticación. Verifica credenciales AWS." -ForegroundColor Red
    exit 1
}

# 2. Instalar/actualizar la librería
Write-Host "📦 Instalando Adelanta Toolbox..." -ForegroundColor Yellow
try {
    uv pip install adelanta-toolbox --upgrade
    Write-Host "✅ Instalación completada" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error en instalación" -ForegroundColor Red
    exit 1
}

# 3. Verificar instalación
Write-Host "🧪 Verificando instalación..." -ForegroundColor Yellow
python -c "import toolbox; print(f'✅ Adelanta Toolbox v{toolbox.__version__} instalado correctamente')"

Write-Host ""
Write-Host "🎉 ¡Adelanta Toolbox listo para usar!" -ForegroundColor Green
Write-Host "📚 Uso: import toolbox" -ForegroundColor Cyan
