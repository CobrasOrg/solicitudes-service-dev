# Solicitudes Service - Repositorio de Desarrollo

Este es el repositorio de desarrollo para el servicio de solicitudes. Aquí puedes trabajar con todas las herramientas de testing y desarrollo, mientras mantienes sincronizado con el repositorio de producción.

## 🚀 Configuración Inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/CobrasOrg/solicitudes-service-dev.git
cd solicitudes-service-dev
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
# Todas las dependencias (incluyendo testing)
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp env.example .env
# Editar .env con tus configuraciones de MongoDB y Firebase
```

### 5. Ejecutar el servidor

```bash
python main.py
```

La aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

### Usar la API desde Swagger

1. Abre http://localhost:8000/docs en tu navegador
2. Explora los endpoints disponibles
3. Haz clic en "Try it out" para probar los endpoints
4. Completa los parámetros requeridos
5. Ejecuta la petición

### 2. Configurar remotes

```bash
# Verificar remotes actuales
git remote -v

# Si necesitas agregar el remote de producción
git remote add production https://github.com/CobrasOrg/solicitudes-service.git
```

## 🧪 Testing

### Tests Rápidos
```bash
python test_quick.py
```

### Tests Completos
```bash
python run_tests.py
```

### Tests con pytest
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_solicitudes.py::test_get_all_solicitudes -v

# Tests con coverage
pytest --cov=app tests/
```

## 🔄 Sincronización con Producción

### Sincronización Automática (Windows)
```bash
sync-to-production.bat
```

### Sincronización Manual
```bash
# 1. Ejecutar tests
pytest -q

# 2. Hacer commit de cambios
git add .
git commit -m "feat: nueva funcionalidad"

# 3. Push a desarrollo
git push origin main

# 4. Sincronizar con producción
git push production main
```

## 📁 Estructura del Proyecto

```
solicitudes-service-dev/
├── app/                    # Código principal de la aplicación
├── tests/                  # Tests de la aplicación
├── development-files/      # Archivos de desarrollo (no se sincronizan)
├── requirements.txt        # Dependencias principales
├── requirements-test.txt   # Dependencias de testing
├── pytest.ini            # Configuración de pytest
├── test_quick.py         # Tests rápidos
├── run_tests.py          # Tests completos
├── sync-to-production.bat # Script de sincronización (Windows)
└── README-DEVELOPMENT.md # Este archivo
```

## 🔧 Flujo de Trabajo

### 1. Desarrollo
- Trabaja en el código en la carpeta `app/`
- Escribe tests en la carpeta `tests/`
- Usa `test_quick.py` para verificaciones rápidas

### 2. Testing
- Ejecuta tests antes de cada commit
- Usa `pytest` para tests completos
- Verifica que todos los tests pasen

### 3. Sincronización
- Usa `sync-to-production.bat` para sincronizar automáticamente
- O haz push manual a ambos repositorios

### 4. Despliegue
- El repositorio de producción se mantiene limpio
- Solo contiene código de producción
- Se despliega automáticamente desde producción

## 🛠️ Herramientas Disponibles

### Scripts de Testing
- `test_quick.py`: Tests básicos de conexión y funcionalidad
- `run_tests.py`: Tests completos de la API
- `pytest`: Framework de testing completo

### Scripts de Sincronización
- `sync-to-production.bat`: Sincronización automática (Windows)
- `sync-to-production.sh`: Sincronización automática (Linux/Mac)

### Configuración
- `pytest.ini`: Configuración de pytest
- `requirements-test.txt`: Dependencias de testing

## 🚨 Troubleshooting

### Error: "No se encontró remote 'production'"
```bash
git remote add production https://github.com/CobrasOrg/solicitudes-service.git
```

### Error: "Los tests fallaron"
- Revisa que MongoDB esté corriendo
- Verifica las variables de entorno
- Ejecuta `python test_quick.py` para diagnóstico

### Error: "Error al sincronizar con producción"
- Verifica permisos de escritura en el repositorio de producción
- Asegúrate de estar autenticado con GitHub
- Revisa que el repositorio de producción exista

## 📊 Monitoreo

### Logs de Testing
```bash
# Tests con verbose
pytest -v

# Tests con output detallado
pytest -s

# Tests con coverage
pytest --cov=app --cov-report=html
```

### Estado de Sincronización
```bash
# Verificar remotes
git remote -v

# Verificar estado de commits
git log --oneline -10
```

## 🎯 Próximos Pasos

1. ✅ Configurar repositorio de desarrollo
2. ✅ Instalar dependencias de testing
3. ✅ Configurar remote de producción
4. 🔄 Ejecutar tests iniciales
5. 🔄 Comenzar desarrollo con testing completo
6. 🔄 Configurar CI/CD si es necesario

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de error
2. Ejecuta `python test_quick.py` para diagnóstico
3. Verifica la configuración de MongoDB
4. Revisa las variables de entorno

---

**Nota**: Este repositorio contiene archivos de desarrollo que NO se sincronizan con producción. El repositorio de producción se mantiene limpio y optimizado para despliegue. 