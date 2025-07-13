#!/bin/bash

# Script para sincronizar con repositorio de producción
# Uso: ./sync-to-production.sh

set -e  # Salir si hay errores

echo "🔄 Sincronizando con repositorio de producción..."
echo "📦 Excluyendo archivos de testing, desarrollo y assets..."

# Verificar que estamos en main branch
if [ "$(git branch --show-current)" != "main" ]; then
    echo "❌ Error: Debes estar en la branch 'main'"
    echo "💡 Ejecuta: git checkout main && git merge develop"
    exit 1
fi

# Crear directorio temporal para producción
TEMP_DIR=$(mktemp -d)
echo "📁 Directorio temporal: $TEMP_DIR"

# Crear archivo de exclusión
cat > sync-exclude.txt << EOF
tests/
pytest.ini
test_quick.py
run_tests.py
.pytest_cache/
node_modules/
package.json
package-lock.json
commitlint.config.js
.pre-commit-config.yaml
.git/
venv/
__pycache__/
.env
development-files/
TESTING.md
sync-to-production.bat
sync-to-production.sh
scripts/
sync-exclude.txt
.github/
production-gitignore
assets/
reports/
.pytest_cache/
__pycache__/
.coverage
coverage.xml
.mypy_cache/
.ruff_cache/
.vscode/
.idea/
*.log
*.tmp
*.bak
EOF

# Copiar archivos de producción (excluyendo tests, assets y desarrollo)
rsync -av --exclude-from=sync-exclude.txt . "$TEMP_DIR/"

# Cambiar al directorio temporal
cd "$TEMP_DIR"

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    git init
    # Usar token de GitHub para autenticación
    if [ -n "$GITHUB_TOKEN" ]; then
        git remote add origin https://x-access-token:$GITHUB_TOKEN@github.com/CobrasOrg/solicitudes-service.git
    else
        git remote add origin https://github.com/CobrasOrg/solicitudes-service.git
    fi
fi

# Hacer commit de los cambios
git add .
git commit -m "Sync from development: $(date)"

# Intentar push con diferentes estrategias
echo "🔄 Intentando push a producción..."

# Estrategia 1: Push a main
if git push origin main; then
    echo "✅ Sincronización exitosa a branch 'main'!"
elif git push origin HEAD:main; then
    echo "✅ Branch 'main' creado y sincronizado!"
elif git push origin master; then
    echo "✅ Sincronización exitosa a branch 'master'!"
elif git push origin HEAD:master; then
    echo "✅ Branch 'master' creado y sincronizado!"
else
    echo "❌ Error al sincronizar con producción"
    echo "💡 Verifica que:"
    echo "   - El repositorio CobrasOrg/solicitudes-service existe"
    echo "   - Tienes permisos de escritura"
    echo "   - Tu token de GitHub está configurado"
    exit 1
fi

# Limpiar
cd ..
rm -rf "$TEMP_DIR"
rm sync-exclude.txt

echo "🎉 Sincronización completada!"
echo "📋 El repo de producción maneja su propio despliegue"
echo "🚫 Assets y archivos de desarrollo excluidos" 