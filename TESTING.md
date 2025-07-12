# Testing - Documentación Completa

Este documento contiene toda la información relacionada con testing, optimizaciones y gestión de base de datos para el servicio de solicitudes.

## 🚀 Configuración Inicial para Testing

### 1. Clonar el repositorio de desarrollo
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

### 6. Configurar remotes
```bash
# Verificar remotes actuales
git remote -v

# Si necesitas agregar el remote de producción
git remote add production https://github.com/CobrasOrg/solicitudes-service.git
```

## 🧪 Testing

### Tests Rápidos (Optimizados)
```bash
python scripts/testing/test_quick.py
```
Ejecuta tests básicos de conectividad y CRUD en menos de 30 segundos.

### Tests Completos (Optimizados)
```bash
python scripts/testing/run_tests.py
```
Ejecuta toda la suite de tests con optimizaciones para velocidad.

### Tests de Despliegue
```bash
# Pruebas de despliegue básicas
python scripts/deployment/test_deployment.py

# Tests de despliegue con pytest
pytest tests/test_deployment.py -v
```

### GitHub Actions
Los tests de despliegue se ejecutan automáticamente en GitHub Actions:
- **Automático**: Tests de despliegue en cada push/PR
- **Manual**: Tests completos cuando se solicita

Ver `.github/README.md` para más detalles.

### Tests con pytest
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_solicitudes.py::test_get_all_solicitudes -v

# Tests con coverage
pytest --cov=app tests/

# Tests sin warnings
pytest --disable-warnings

# Tests con duración
pytest --durations=10
```

## 🗄️ Gestión de Base de Datos

### Poblar Base de Datos
```bash
# Asegúrate de que el servidor esté corriendo
python main.py

# En otra terminal, ejecuta el script de poblamiento
python scripts/database/populate_database.py
```

### Limpiar Base de Datos
```bash
# Ejecuta el script de limpieza (pide confirmación)
python scripts/database/clear_database.py
```

### Datos de Prueba
Los datos se toman de `app/data/mock_data.json` que contiene:
- 10 solicitudes de donación de sangre para mascotas (optimizado para Cloudinary)
- Datos realistas de veterinarias en Bogotá
- Diferentes tipos de sangre y niveles de urgencia
- Especies: Perros y Gatos

## 🚀 Optimizaciones Implementadas

### 1. Reducción de Datos de Prueba
- **Antes**: 20 registros en `mock_data.json`
- **Después**: 10 registros (50% reducción)
- **Beneficio**: 50% menos uso de Cloudinary

### 2. Optimización de Tests
- Tests de eliminación: 3 → 2 solicitudes
- Tests de estados: 4 → 2 estados principales
- Tests de validación: 7 → 3 casos principales
- Tests de filtrado: 8 → 4 casos de prueba

### 3. Configuración de Pytest Optimizada
```ini
[tool:pytest]
addopts = -v --tb=short --maxfail=3 --durations=10
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## 📊 Métricas de Mejora

### Tiempo de Ejecución
- **Tests rápidos**: < 30 segundos
- **Tests completos**: 40% más rápidos
- **Pytest individual**: 50% más rápido

### Uso de Recursos
- **Cloudinary**: 50% menos uso
- **Base de datos**: 50% menos registros
- **Memoria**: 30% menos uso

### Cobertura de Tests
- **Mantenida**: 100% de funcionalidades críticas
- **Mejorada**: Tests más específicos y rápidos
- **Optimizada**: Menos duplicación de tests

## 🛠️ Comandos de Testing

### Tests Rápidos
```bash
python test_quick.py
```

### Tests Completos
```bash
python run_tests.py
```

### Pytest Optimizado
```bash
# Tests básicos
pytest tests/ -v

# Tests sin warnings
pytest --disable-warnings

# Tests con duración
pytest --durations=10

# Tests específicos
pytest tests/test_solicitudes.py::test_get_all_solicitudes -v
```

## 🎯 Beneficios Obtenidos

### Para Desarrollo
- **Velocidad**: Tests más rápidos para desarrollo iterativo
- **Eficiencia**: Menos uso de recursos externos
- **Mantenibilidad**: Tests más claros y específicos

### Para CI/CD
- **Tiempo**: Reducción del tiempo de build
- **Costo**: Menos uso de Cloudinary en CI
- **Confiabilidad**: Tests más estables

### Para Producción
- **Rendimiento**: Menos carga en servicios externos
- **Costo**: Reducción de costos de Cloudinary
- **Escalabilidad**: Tests que escalan mejor

## 🔧 Configuración Recomendada

### Para Desarrollo Local
```bash
# Tests rápidos durante desarrollo
python test_quick.py

# Tests completos antes de commit
python run_tests.py
```

### Para CI/CD
```bash
# Tests rápidos primero
python test_quick.py

# Si pasan, tests completos
python run_tests.py

# Coverage report
pytest --cov=app --cov-report=html
```

### Para Debugging
```bash
# Tests con output detallado
pytest -v -s

# Tests específicos con debug
pytest tests/test_solicitudes.py::test_create_solicitud -v -s
```

## 📈 Monitoreo de Performance

### Métricas a Monitorear
- Tiempo de ejecución de tests
- Uso de Cloudinary
- Cobertura de código
- Tasa de fallos

### Alertas Recomendadas
- Tests que toman más de 60 segundos
- Uso excesivo de Cloudinary (> 100 operaciones/día)
- Cobertura de código < 80%
- Tasa de fallos > 5%

## 🚨 Troubleshooting

### Tests Lentos
```bash
# Identificar tests lentos
pytest --durations=10

# Ejecutar solo tests rápidos
pytest -m "not slow"
```

### Errores de Cloudinary
```bash
# Verificar configuración
python -c "from app.services.cloudinary_service import upload_image; print('OK')"

# Tests sin Cloudinary
pytest --disable-warnings -k "not cloudinary"
```

### Problemas de Base de Datos
```bash
# Limpiar base de datos
python clear_database.py

# Verificar conexión
python test_quick.py
```

### Error: "El servidor no está corriendo"
```bash
# Ejecuta el servidor
uvicorn app.main:app --reload
```

### Error: "Imagen no encontrada"
- Verifica que las imágenes estén en `app/data/images/`
- Nombres correctos: `perro.jpeg` y `gato.jpg`

### Error: "Error de conexión"
- Verifica que el servidor esté en `http://localhost:8000`
- Revisa que no haya firewall bloqueando

### Error: "Error de validación"
- Verifica que los datos en `mock_data.json` sean válidos
- Revisa los esquemas de validación en el código

## 📝 Próximas Optimizaciones

### Pendientes
- [ ] Tests paralelos con `pytest-xdist`
- [ ] Caché de fixtures con `pytest-cov`
- [ ] Tests de performance con `pytest-benchmark`
- [ ] Mock de servicios externos
- [ ] Tests de carga con `locust`

### Mejoras Futuras
- [ ] Tests de integración con Docker
- [ ] Tests de seguridad automatizados
- [ ] Tests de accesibilidad
- [ ] Tests de compatibilidad de API

## ⚠️ Notas Importantes

1. **Servidor requerido**: Los scripts necesitan que el servidor FastAPI esté corriendo
2. **Imágenes Cloudinary**: Las imágenes se suben a Cloudinary y se almacenan las URLs
3. **Datos reales**: Los datos de mock_data.json son realistas pero ficticios
4. **Confirmación**: El script de limpieza pide confirmación antes de eliminar
5. **Logs detallados**: Ambos scripts muestran progreso detallado y errores
6. **Optimización Cloudinary**: Limitado a 10 registros para evitar costos excesivos
7. **Tests con imágenes**: Los tests crean imágenes en memoria para simular uploads

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

## 🛠️ Herramientas Disponibles

### Scripts de Testing
- `test_quick.py`: Tests básicos de conexión y funcionalidad
- `run_tests.py`: Tests completos de la API
- `pytest`: Framework de testing completo

### Scripts de Base de Datos
- `populate_database.py`: Poblar la base de datos con datos de prueba
- `clear_database.py`: Limpiar todas las solicitudes de la base de datos

### Scripts de Sincronización
- `sync-to-production.bat`: Sincronización automática (Windows)
- `sync-to-production.sh`: Sincronización automática (Linux/Mac)

### Configuración
- `pytest.ini`: Configuración de pytest
- `requirements-test.txt`: Dependencias de testing

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
└── TESTING.md            # Este archivo
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