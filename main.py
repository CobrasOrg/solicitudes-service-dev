import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Cargar variables de entorno desde .env
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import mongodb
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=None  # Se reemplazará abajo
)

# Lifespan para inicialización y cierre
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongodb.connect_to_mongo()
    from app.services.firebase_service import firebase_service
    firebase_service._initialize_firebase()
    yield
    await mongodb.close_mongo_connection()

app.router.lifespan_context = lifespan

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Solicitudes Service API",
        "version": settings.VERSION,
        "features": [
            "Gestión de solicitudes de donación de sangre",
            "Soporte para imágenes con Firebase Storage",
            "Base de datos MongoDB",
            "Endpoints para veterinarias y usuarios"
        ]
    }

@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de la aplicación
    """
    try:
        # Verificar MongoDB
        await mongodb.client.admin.command('ping')
        mongo_status = "healthy"
    except Exception:
        mongo_status = "unhealthy"
    
    return {
        "status": "ok",
        "mongodb": mongo_status,
        "firebase": "initialized"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 