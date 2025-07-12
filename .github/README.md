# GitHub Actions - CI/CD Pipeline

Este directorio contiene la configuración de GitHub Actions para automatizar el testing y deployment.

## 🔄 Flujo de CI/CD

### **1. Tests de Despliegue (Siempre)**
- Se ejecutan en **todos los pushes** y **Pull Requests** a `main` y `develop`
- Verifican que el código es estable para producción
- **Archivo:** `scripts/deployment/test_deployment.py`

### **2. Tests Completos (PRs a main)**
- Se ejecutan **solo en Pull Requests** a la rama `main`
- Incluyen todos los tests funcionales y de integración
- **Comando:** `pytest tests/ -v`

### **3. Deploy Automático (Push a main)**
- Se ejecuta **automáticamente** cuando se hace push a `main`
- Sincroniza el código con el repositorio de producción
- Solo se ejecuta si los tests de despliegue pasan

## 📋 Workflows

### **ci-cd.yml**
- **Tests de despliegue:** En cada push y PR
- **Tests completos:** En PRs a main
- **Deploy automático:** En push a main

## 🔧 Configuración

### **Secrets Requeridos**
Configura estos secrets en tu repositorio (Settings → Secrets and variables → Actions):

```
MONGODB_URL=tu_url_de_mongodb
MONGODB_DATABASE=nombre_de_la_base_de_datos
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

### **Variables de Entorno**
El workflow usa las siguientes variables de entorno:
- `GITHUB_TOKEN`: Token automático de GitHub
- Variables de configuración de la aplicación

## 🚀 Cómo Funciona

### **Para Desarrolladores:**
1. Crear feature branch desde `develop`
2. Hacer cambios y commits
3. Crear Pull Request a `develop`
4. GitHub Actions ejecuta tests automáticamente
5. Merge después de aprobación

### **Para Releases:**
1. Crear Pull Request de `develop` a `main`
2. GitHub Actions ejecuta tests completos
3. Merge después de aprobación
4. **Deploy automático** al repo de producción

### **Para Hotfixes:**
1. Crear Pull Request de `hotfix` a `main`
2. GitHub Actions ejecuta tests completos
3. Merge después de aprobación
4. **Deploy automático** al repo de producción

## 📊 Monitoreo

### **Estado de Workflows**
- Ve a la pestaña "Actions" en GitHub
- Revisa el estado de cada workflow
- Los workflows fallidos bloquean el merge

### **Logs y Debugging**
- Haz clic en cualquier job para ver logs detallados
- Los errores se muestran en tiempo real
- Puedes re-ejecutar workflows fallidos

## 🛡️ Protección de Ramas

### **Rama `main`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ❌ No direct pushes (solo merge desde release/hotfix)

### **Rama `develop`**
- ✅ Require pull request reviews
- ✅ Require status checks to pass before merging
- ❌ Allow force pushes (solo para releases)

## 🔄 Flujo Completo

```
Feature Branch → Develop → Main → Producción
     ↓              ↓        ↓         ↓
   Tests         Tests    Tests    Deploy
   (PR)         (PR)     (PR)    (Auto)
```

## 📞 Soporte

Si hay problemas con los workflows:
1. Revisa los logs en la pestaña "Actions"
2. Verifica que los secrets estén configurados
3. Asegúrate de que los tests pasen localmente
4. Contacta al equipo de DevOps

---

**Nota:** Este sistema reemplaza el script `.bat` manual con un flujo automatizado y más seguro. 