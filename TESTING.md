# Testing - Servicio de Solicitudes

## 🚀 Ejecutar Tests

### Tests Rápidos (Desarrollo)
```bash
python run_tests.py quick
```
Ejecuta solo los tests críticos para validación rápida.

### Tests Completos (Release)
```bash
python run_tests.py full
```
Ejecuta todos los tests del proyecto.

## 📁 Estructura de Tests

### Tests Críticos
- **Despliegue**: `tests/test_deployment.py`
- **Funcionalidad**: Tests básicos de CRUD en `tests/test_solicitudes.py`
- **Autenticación**: Validación de headers y permisos

### Tests Completos
- **Múltiples Filtros**: `tests/test_multiple_filters.py`
- **Todas las Funcionalidades**: Tests exhaustivos de cada endpoint

## 🧪 Scripts de Testing

### `run_tests.py`
Script principal para ejecutar tests locales:
- `python run_tests.py quick` - Tests críticos
- `python run_tests.py full` - Todos los tests

### `scripts/testing/test_quick.py`
Script interno que ejecuta los tests críticos específicos.

## 🔧 CI/CD Pipeline (Optimizado)

### Flujo de Testing
1. **Desarrollo Local**: `python run_tests.py quick`
2. **Push a Develop**: Tests automáticos en CI/CD
3. **Merge a Main**: Sin tests (ya validados en develop)
4. **Producción**: Despliegue automático

### Tests Automáticos (solo en develop)
- ✅ Tests críticos de despliegue
- ✅ Tests rápidos de funcionalidad
- ✅ Despliegue a staging
- ✅ Validación manual en staging

### Tests Manuales
- **Desarrollo local**: `python run_tests.py quick`
- **Antes de release**: `python run_tests.py full`

## 📊 Cobertura de Tests

### Tests Críticos (CI/CD)
- ✅ Configuración de aplicación
- ✅ Conexión a MongoDB
- ✅ Endpoints básicos (health, root)
- ✅ Creación de solicitudes
- ✅ Obtención de solicitudes
- ✅ Actualización de estados

### Tests Completos (Local)
- ✅ Todos los tests críticos
- ✅ Tests de múltiples filtros
- ✅ Tests de autenticación
- ✅ Tests de validación de datos
- ✅ Tests de manejo de errores

## 🚨 Troubleshooting

### Tests Fallan
1. Verificar que MongoDB esté configurado
2. Verificar variables de entorno
3. Ejecutar `python run_tests.py quick` para tests básicos

### Tests Lentos
- Los tests completos pueden tomar varios minutos
- Usar `python run_tests.py quick` para desarrollo
- Los tests críticos toman ~30 segundos

## ⚡ Beneficios del Flujo Optimizado

### Eficiencia
- ✅ Tests solo una vez (en develop)
- ✅ Sin duplicación de tests en main
- ✅ Despliegue más rápido a producción

### Confiabilidad
- ✅ Validación completa en staging
- ✅ Tests críticos garantizados
- ✅ Flujo de trabajo simplificado 