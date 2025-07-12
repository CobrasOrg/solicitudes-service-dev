# Scripts

Esta carpeta contiene todos los scripts utilitarios del proyecto organizados por categoría.

## Estructura

```
scripts/
├── testing/           # Scripts de testing
│   ├── test_quick.py  # Tests rápidos de conectividad
│   └── run_tests.py   # Suite completa de tests
├── database/          # Scripts de gestión de base de datos
│   ├── populate_database.py  # Poblar BD con datos de prueba
│   └── clear_database.py     # Limpiar todas las solicitudes
└── deployment/        # Scripts de despliegue
    └── test_deployment.py    # Pruebas de despliegue
```

## Uso

### Testing
```bash
# Tests rápidos
python scripts/testing/test_quick.py

# Tests completos
python scripts/testing/run_tests.py
```

### Base de Datos
```bash
# Poblar base de datos
python scripts/database/populate_database.py

# Limpiar base de datos
python scripts/database/clear_database.py
```

### Despliegue
```bash
# Pruebas de despliegue
python scripts/deployment/test_deployment.py
```

## Notas

- Todos los scripts están configurados para ejecutarse desde el directorio raíz del proyecto
- Los scripts de testing requieren que el servidor esté corriendo
- Los scripts de base de datos requieren conexión a MongoDB
- Los scripts de despliegue verifican configuración y conectividad 