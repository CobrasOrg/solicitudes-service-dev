# Servicio de Solicitudes de Donación de Sangre

Servicio backend para la gestión de solicitudes de donación de sangre para mascotas, desarrollado con FastAPI.

## Características

- FastAPI como framework web
- MongoDB como base de datos
- Firebase Storage para imágenes
- Estructura modular y escalable
- Configuración de CORS
- Variables de entorno con python-dotenv
- Documentación automática con Swagger y ReDoc
- Validación de datos con Pydantic
- Endpoints para veterinarias y usuarios

## Requisitos

- Python 3.8+
- MongoDB
- Firebase (para almacenamiento de imágenes)
- pip

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/CobrasOrg/solicitudes-service.git
cd solicitudes-service
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:

```bash
cp env.example .env
# Editar .env con tus configuraciones de MongoDB y Firebase
```

5. Ejecutar el servidor:

```bash
python main.py
```

La aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## Configuración

### Firebase (para imágenes)

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a "Storage" y haz clic en "Get started"
4. Selecciona "Start in test mode" y elige ubicación
5. Ve a "Project settings" > "Service accounts"
6. Haz clic en "Generate new private key"
7. Descarga el archivo JSON
8. Copia los valores del JSON a las variables de entorno

### Variables de Entorno

```bash
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=solicitudes

# Firebase Configuration
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=tu-proyecto-id-aqui
FIREBASE_PRIVATE_KEY_ID=tu-private-key-id-aqui
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nTU_CLAVE_PRIVADA_AQUI\n-----END PRIVATE KEY-----"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@tu-proyecto-id.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=tu-client-id-aqui
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxxxx%40tu-proyecto-id.iam.gserviceaccount.com
FIREBASE_STORAGE_BUCKET=tu-proyecto-id.appspot.com
```

## Ejecución

Una vez configurado todo, ejecuta:

```bash
python main.py
```

### Acceso a la API

- **API Base**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Usar la API desde Swagger

1. Abre http://localhost:8000/docs en tu navegador
2. Explora los endpoints disponibles
3. Haz clic en "Try it out" para probar los endpoints
4. Completa los parámetros requeridos
5. Ejecuta la petición

## Endpoints Disponibles

### Veterinarias

#### Obtener Todas las Solicitudes
- **Endpoint**: `GET /solicitudes/vet/`
- **Descripción**: Retorna todas las solicitudes independientemente de su estado
- **Respuestas**:
  - `200`: Lista de todas las solicitudes
  - `500`: Error interno del servidor

#### Filtrar Solicitudes por Estado
- **Endpoint**: `GET /solicitudes/vet/filtrar`
- **Descripción**: Retorna las solicitudes filtradas por estado y otros criterios
- **Parámetros de Consulta**:
  - `estado`: Estado de las solicitudes (Activa, Completada, Cancelada, Revision)
  - `especie`: Filtrar por especie (ej: Perro, Gato)
  - `tipo_sangre`: Filtrar por tipo de sangre (ej: DEA 1.1+, A)
  - `urgencia`: Filtrar por nivel de urgencia (Alta, Media, Baja)
  - `localidad`: Filtrar por localidad (ej: Suba, Chapinero)
- **Respuestas**:
  - `200`: Lista de solicitudes filtradas
  - `400`: Estado inválido
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Obtener Solicitud Específica
- **Endpoint**: `GET /solicitudes/vet/{solicitud_id}`
- **Descripción**: Retorna una solicitud específica por su ID
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Respuestas**:
  - `200`: Solicitud encontrada
  - `404`: Solicitud no encontrada
  - `500`: Error interno del servidor

#### Crear Nueva Solicitud
- **Endpoint**: `POST /solicitudes/vet/`
- **Descripción**: Crea una nueva solicitud de donación de sangre
- **Cuerpo de la Solicitud** (multipart/form-data):
  ```
  nombre_veterinaria: string
  nombre_mascota: string
  especie: string
  localidad: string
  descripcion_solicitud: string
  direccion: string
  ubicacion: string
  contacto: string
  peso_minimo: number
  tipo_sangre: string
  urgencia: string
  foto_mascota: file (opcional)
  ```
- **Respuestas**:
  - `201`: Solicitud creada exitosamente
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Actualizar Datos de Solicitud
- **Endpoint**: `PATCH /solicitudes/vet/{solicitud_id}`
- **Descripción**: Actualiza los datos de una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Cuerpo de la Solicitud** (multipart/form-data o JSON):
  ```
  especie: string (opcional)
  tipo_sangre: string (opcional)
  urgencia: string (opcional)
  peso_minimo: number (opcional)
  descripcion_solicitud: string (opcional)
  direccion: string (opcional)
  estado: string (opcional)
  foto_mascota: file (opcional)
  ```
- **Respuestas**:
  - `200`: Solicitud actualizada exitosamente
  - `404`: Solicitud no encontrada
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Actualizar Estado de Solicitud
- **Endpoint**: `PATCH /solicitudes/vet/{solicitud_id}/estado`
- **Descripción**: Actualiza el estado de una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Cuerpo de la Solicitud**:
  ```json
  {
    "estado": "string"
  }
  ```
- **Respuestas**:
  - `200`: Estado actualizado exitosamente
  - `400`: Estado inválido
  - `404`: Solicitud no encontrada
  - `422`: Error de validación
  - `500`: Error interno del servidor

#### Eliminar Solicitud
- **Endpoint**: `DELETE /solicitudes/vet/{solicitud_id}`
- **Descripción**: Elimina una solicitud existente
- **Parámetros de Ruta**:
  - `solicitud_id`: ID de la solicitud
- **Respuestas**:
  - `200/204`: Solicitud eliminada exitosamente
  - `404`: Solicitud no encontrada
  - `500`: Error interno del servidor

### Usuarios

#### Obtener Solicitudes Activas
- **Endpoint**: `GET /solicitudes/user/activas`
- **Descripción**: Retorna todas las solicitudes que tienen estado 'Activa'
- **Respuestas**:
  - `200`: Lista de solicitudes activas
  - `500`: Error interno del servidor

#### Filtrar Solicitudes Activas
- **Endpoint**: `GET /solicitudes/user/activas/filtrar`
- **Descripción**: Retorna las solicitudes activas filtradas por criterios
- **Parámetros de Consulta**:
  - `especie`: Filtrar por especie (ej: Perro, Gato)
  - `tipo_sangre`: Filtrar por tipo de sangre (ej: DEA 1.1+, A)
  - `urgencia`: Filtrar por nivel de urgencia (Alta, Media, Baja)
  - `localidad`: Filtrar por localidad (ej: Suba, Chapinero)
- **Respuestas**:
  - `200`: Lista de solicitudes activas filtradas
  - `422`: Error de validación
  - `500`: Error interno del servidor

## Estructura del Proyecto

```
solicitudes-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── base.py
│   │       │   ├── solicitudes/
│   │       │   │   ├── user/
│   │       │   │   └── vet/
│   │       └── api.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── mongodb.py
│   ├── models/
│   │   ├── base.py
│   │   ├── solicitud.py
│   │   └── solicitud_mongo.py
│   ├── schemas/
│   │   ├── base.py
│   │   └── solicitud.py
│   ├── constants/
│   │   └── solicitudes.py
│   ├── data/
│   │   └── mock_data.json
│   └── services/
│       └── firebase_service.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
├── CHANGELOG.md
└── requirements.txt
```

### Descripción de Carpetas y Archivos

- `app/`: Directorio principal de la aplicación
  - `api/`: Endpoints y rutas de la API
  - `core/`: Configuraciones centrales
  - `db/`: Configuración y conexión a la base de datos
  - `models/`: Modelos de datos y lógica de negocio
  - `schemas/`: Esquemas Pydantic para validación de datos
  - `constants/`: Constantes y enumeraciones del sistema
  - `data/`: Datos mock y archivos de datos
  - `services/`: Servicios externos (Firebase, etc.)



## Desarrollo

### Agregar Nuevos Endpoints

1. Crear nuevo archivo en `app/api/v1/endpoints/solicitudes/`
2. Definir router y endpoints
3. Registrar router en `app/api/v1/api.py`

## Estado del Proyecto

### Implementado
- ✅ Estructura base del proyecto
- ✅ Endpoints principales
- ✅ Validación de datos
- ✅ Integración con MongoDB
- ✅ Firebase Storage para imágenes
- ✅ Documentación de API
- ✅ Datos mock

### Pendiente
- ⏳ Autenticación y autorización
- ⏳ Logging y monitoreo
- ⏳ Rate limiting
- ⏳ Caché
- ⏳ Despliegue en producción

## Despliegue

Este repositorio está optimizado para producción. Para desarrollo y testing, ver el repositorio de desarrollo.

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: add some amazing feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

MIT 