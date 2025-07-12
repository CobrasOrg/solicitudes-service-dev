# GitFlow - Modelo de Branching

Este documento describe el modelo de branching GitFlow implementado en todos los repositorios del proyecto.

## 🌿 Estructura de Ramas

### **Ramas Principales**
- `main/` - Código de producción (estable)
- `develop/` - Rama de desarrollo (integración)

### **Ramas de Trabajo**
- `feature/` - Nuevas funcionalidades
- `release/` - Preparación de releases
- `hotfix/` - Correcciones urgentes en producción

## 🔄 Flujo de Trabajo

### **1. Desarrollo de Features**

```bash
# Crear feature desde develop
git checkout develop
git pull origin develop
git checkout -b feature/nombre-feature

# Trabajar en la feature
# ... código ...

# Hacer commits
git add .
git commit -m "feat: descripción de la funcionalidad"

# Push a la rama feature
git push origin feature/nombre-feature
```

### **2. Testing en Features**

```bash
# Ejecutar tests antes de merge
python test_quick.py
pytest

# Si los tests fallan, corregir y hacer commit
git add .
git commit -m "fix: corregir tests"
```

### **3. Merge Feature a Develop**

```bash
# Crear Pull Request: feature → develop
# URL: https://github.com/CobrasOrg/solicitudes-service-dev/pull/new/feature/nombre-feature

# Code review obligatorio
# Tests deben pasar
# Merge solo después de aprobación
```

### **4. Release a Producción**

```bash
# Crear release desde develop
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Testing final
python test_quick.py
pytest

# Ajustes finales si es necesario
git add .
git commit -m "chore: ajustes finales para release"

# Merge a main y develop
git checkout main
git merge release/v1.2.0
git tag v1.2.0
git push origin main --tags

git checkout develop
git merge release/v1.2.0
git push origin develop

# Eliminar rama release
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### **5. Sincronización con Producción**

```bash
# Después de validar en staging, merge a main
git checkout main
git merge develop
git push origin main

# El workflow ci-cd.yml maneja automáticamente:
# - Tests de despliegue
# - Sincronización con repo de producción
# - Exclusión de archivos de testing
```

### **6. Hotfix (Correcciones Urgentes)**

```bash
# Crear hotfix desde main
git checkout main
git pull origin main
git checkout -b hotfix/correccion-urgente

# Corregir el problema
# ... código ...

# Testing
python test_quick.py
pytest

# Merge a main y develop
git checkout main
git merge hotfix/correccion-urgente
git tag v1.2.1
git push origin main --tags

git checkout develop
git merge hotfix/correccion-urgente
git push origin develop

# Eliminar rama hotfix
git branch -d hotfix/correccion-urgente
git push origin --delete hotfix/correccion-urgente
```

## 🛡️ Reglas de Protección de Ramas

### **Rama `main`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Restrict pushes that create files that use the gitfile: protocol
- ❌ No direct pushes (solo merge desde release/hotfix)

### **Rama `develop`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ❌ Allow force pushes (solo para releases)

## 📋 Convenciones de Nomenclatura

### **Ramas Feature**
```
feature/nombre-descriptivo
feature/user-authentication
feature/payment-integration
```

### **Ramas Release**
```
release/v1.2.0
release/v2.0.0
```

### **Ramas Hotfix**
```
hotfix/critical-bug-fix
hotfix/security-patch
```

### **Commits**
```
feat: nueva funcionalidad
fix: corrección de bug
docs: actualización de documentación
style: cambios de formato
refactor: refactorización de código
test: agregar o modificar tests
chore: tareas de mantenimiento
```

## 🧪 Testing Obligatorio

### **Antes de Merge a Develop**
- ✅ `python test_quick.py` debe pasar
- ✅ `pytest` debe pasar
- ✅ Todos los tests deben estar verdes

### **Antes de Release**
- ✅ Testing completo
- ✅ Verificación manual de funcionalidades
- ✅ Documentación actualizada

## 🚀 CI/CD Pipeline

### **Workflow: ci-cd.yml**

#### **Push a `develop`:**
1. ✅ **Tests de despliegue** - Verifica configuración y conectividad
2. ✅ **Despliegue a staging** - Fly.io (https://solicitudes-staging.fly.dev)
3. ✅ **Validación** - Probar funcionalidades en staging

#### **Push a `main`:**
1. ✅ **Tests de despliegue** - Verifica configuración
2. ✅ **Sincronización automática** - Con repo de producción
3. ✅ **Exclusión de archivos** - Sin tests, scripts, o archivos de desarrollo

### **Variables de Entorno Requeridas:**
- `FLY_API_TOKEN` - Token de API de Fly.io
- `MONGODB_URL` - URL de MongoDB Atlas
- `MONGODB_DATABASE` - Nombre de la base de datos
- `CLOUDINARY_CLOUD_NAME` - Cloud name de Cloudinary
- `CLOUDINARY_API_KEY` - API Key de Cloudinary
- `CLOUDINARY_API_SECRET` - API Secret de Cloudinary
- `STAGING_BASE_URL` - URL base de staging

## 📊 Monitoreo

### **Estado de Ramas**
```bash
# Ver ramas locales
git branch

# Ver ramas remotas
git branch -r

# Ver todas las ramas
git branch -a
```

### **Historial de Tags**
```bash
# Ver tags
git tag

# Ver información de un tag
git show v1.2.0
```

## 🚨 Casos Especiales

### **Rollback de Release**
```bash
# Revertir último commit en main
git checkout main
git revert HEAD
git push origin main

# Crear nuevo hotfix si es necesario
git checkout -b hotfix/rollback-release
```

### **Merge Conflict**
```bash
# Resolver conflictos
git status
# Editar archivos con conflictos
git add .
git commit -m "fix: resolver conflictos de merge"
```

## 📞 Soporte

Si tienes problemas con GitFlow:
1. Revisa este documento
2. Consulta con el equipo
3. Verifica las reglas de protección en GitHub
4. Asegúrate de que los tests pasen antes de merge

---

**Nota**: Este modelo se aplica a todos los repositorios del proyecto (frontend y backend). 