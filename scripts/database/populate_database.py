#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de mock_data.json
y subir imágenes a Cloudinary.
"""

import asyncio
import json
import os
import requests
from pathlib import Path
from typing import Dict, Any
import time

# Configuración
BASE_URL = "http://localhost:8000"
ENDPOINT = "/api/v1/vet/solicitudes/"

# Obtener la ruta del directorio actual del script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
IMAGES_DIR = PROJECT_ROOT / "app" / "data" / "images"
MOCK_DATA_FILE = PROJECT_ROOT / "app" / "data" / "mock_data.json"

# Mapeo de especies a imágenes
SPECIES_IMAGES = {
    "Perro": "perro.jpeg",
    "Gato": "gato.jpg"
}

def load_mock_data() -> Dict[str, Any]:
    """Cargar datos de mock_data.json"""
    with open(MOCK_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_image_path(species: str) -> Path:
    """Obtener la ruta de la imagen según la especie"""
    image_filename = SPECIES_IMAGES.get(species)
    if not image_filename:
        raise ValueError(f"Especie no mapeada: {species}")
    
    image_path = IMAGES_DIR / image_filename
    if not image_path.exists():
        raise FileNotFoundError(f"Imagen no encontrada: {image_path}")
    
    return image_path

def create_solicitud_request(solicitud_data: Dict[str, Any], image_path: Path) -> Dict[str, Any]:
    """Crear la petición para crear una solicitud"""
    # Preparar los datos del formulario
    form_data = {
        'nombre_veterinaria': solicitud_data['nombre_veterinaria'],
        'nombre_mascota': solicitud_data['nombre_mascota'],
        'especie': solicitud_data['especie'],
        'localidad': solicitud_data['localidad'],
        'descripcion_solicitud': solicitud_data['descripcion_solicitud'],
        'direccion': solicitud_data['direccion'],
        'ubicacion': solicitud_data['ubicacion'],
        'contacto': solicitud_data['contacto'],
        'peso_minimo': str(solicitud_data['peso_minimo']),
        'tipo_sangre': solicitud_data['tipo_sangre'],
        'urgencia': solicitud_data['urgencia']
    }
    
    # Preparar el archivo
    files = {
        'foto_mascota': (image_path.name, open(image_path, 'rb'), 'image/jpeg')
    }
    
    return form_data, files

async def populate_database():
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando poblamiento de la base de datos...")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print("❌ Error: El servidor no está corriendo en http://localhost:8000")
            print("   Ejecuta: uvicorn app.main:app --reload")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor en http://localhost:8000")
        print("   Ejecuta: uvicorn app.main:app --reload")
        return
    
    # Cargar datos
    try:
        data = load_mock_data()
        solicitudes = data['solicitudes']
        print(f"📊 Cargadas {len(solicitudes)} solicitudes desde mock_data.json")
    except Exception as e:
        print(f"❌ Error cargando mock_data.json: {e}")
        return
    
    # Verificar imágenes
    for species, image_file in SPECIES_IMAGES.items():
        image_path = IMAGES_DIR / image_file
        if not image_path.exists():
            print(f"❌ Error: Imagen no encontrada para {species}: {image_path}")
            return
        print(f"✅ Imagen encontrada para {species}: {image_file}")
    
    # Crear solicitudes
    success_count = 0
    error_count = 0
    
    for i, solicitud in enumerate(solicitudes, 1):
        try:
            print(f"\n📝 Procesando solicitud {i}/{len(solicitudes)}: {solicitud['nombre_mascota']} ({solicitud['especie']})")
            
            # Obtener imagen según especie
            image_path = get_image_path(solicitud['especie'])
            
            # Preparar datos
            form_data, files = create_solicitud_request(solicitud, image_path)
            
            # Enviar petición
            url = f"{BASE_URL}{ENDPOINT}"
            response = requests.post(url, data=form_data, files=files)
            
            # Cerrar el archivo
            files['foto_mascota'][1].close()
            
            if response.status_code == 201:
                created_solicitud = response.json()
                print(f"✅ Creada solicitud: {created_solicitud['id']} - {created_solicitud['nombre_mascota']}")
                success_count += 1
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                error_count += 1
            
            # Pausa pequeña entre peticiones
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error procesando solicitud {i}: {e}")
            error_count += 1
    
    # Resumen final
    print(f"\n🎉 Poblamiento completado!")
    print(f"✅ Solicitudes creadas: {success_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📊 Total procesadas: {len(solicitudes)}")

if __name__ == "__main__":
    print("🐕🐱 Script de poblamiento de base de datos")
    print("=" * 50)
    
    # Verificar archivos necesarios
    if not MOCK_DATA_FILE.exists():
        print(f"❌ Error: No se encuentra {MOCK_DATA_FILE}")
        exit(1)
    
    if not IMAGES_DIR.exists():
        print(f"❌ Error: No se encuentra el directorio {IMAGES_DIR}")
        exit(1)
    
    # Ejecutar
    asyncio.run(populate_database()) 