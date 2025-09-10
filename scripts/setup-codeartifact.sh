#!/bin/bash
# 🏗️ Setup AWS CodeArtifact para Adelanta Toolbox
# Ejecutar solo una vez para configurar el repositorio

echo "🚀 Configurando AWS CodeArtifact para Adelanta Toolbox..."

# 1. Crear dominio
echo "📦 Creando dominio 'adelanta'..."
aws codeartifact create-domain \
  --domain adelanta \
  --region us-east-2

# 2. Crear repositorio
echo "📚 Creando repositorio 'adelanta-toolbox'..."
aws codeartifact create-repository \
  --domain adelanta \
  --repository adelanta-toolbox \
  --description "Repositorio privado para Adelanta Toolbox - Librería Financiera" \
  --upstreams repositoryName=pypi-store \
  --region us-east-2

# 3. Crear repositorio upstream para PyPI
echo "🔗 Creando upstream PyPI..."
aws codeartifact create-repository \
  --domain adelanta \
  --repository pypi-store \
  --description "Upstream repository for PyPI" \
  --external-connections externalConnectionName=public:pypi \
  --region us-east-2

# 4. Obtener información de login
echo "🔑 Configurando autenticación..."
aws codeartifact login \
  --tool pip \
  --repository adelanta-toolbox \
  --domain adelanta \
  --region us-east-2

echo "✅ Setup completado!"
echo ""
echo "📋 Para publicar tu librería:"
echo "1. uv build"
echo "2. REPO_URL=\$(aws codeartifact get-repository-endpoint --domain adelanta --repository adelanta-toolbox --format pypi --query repositoryEndpoint --output text --region us-east-2)"
echo "3. uv publish --repository-url \$REPO_URL dist/*"
echo ""
echo "📋 Para instalar desde CodeArtifact:"
echo "aws codeartifact login --tool pip --repository adelanta-toolbox --domain adelanta --region us-east-2"
echo "uv pip install adelanta-toolbox"
