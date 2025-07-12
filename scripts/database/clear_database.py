#!/usr/bin/env python3
"""
Script para limpiar todas las solicitudes de la base de datos.
Útil para resetear la base de datos antes de poblar con nuevos datos.
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"
ENDPOINT_GET = "/api/v1/vet/solicitudes/"
ENDPOINT_DELETE = "/api/v1/vet/solicitudes/"

def clear_database():
    """Limpiar todas las solicitudes de la base de datos"""
    print("🧹 Iniciando limpieza de la base de datos...")
    
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
    
    # Obtener todas las solicitudes
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT_GET}")
        if response.status_code != 200:
            print(f"❌ Error obteniendo solicitudes: {response.status_code}")
            return
        
        solicitudes = response.json()
        total_solicitudes = len(solicitudes)
        print(f"📊 Encontradas {total_solicitudes} solicitudes para eliminar")
        
        if total_solicitudes == 0:
            print("✅ La base de datos ya está vacía")
            return
        
    except Exception as e:
        print(f"❌ Error obteniendo solicitudes: {e}")
        return
    
    # Eliminar cada solicitud
    deleted_count = 0
    error_count = 0
    
    for i, solicitud in enumerate(solicitudes, 1):
        try:
            solicitud_id = solicitud['id']
            print(f"🗑️  Eliminando solicitud {i}/{total_solicitudes}: {solicitud_id} - {solicitud['nombre_mascota']}")
            
            response = requests.delete(f"{BASE_URL}{ENDPOINT_DELETE}{solicitud_id}")
            
            if response.status_code == 204:
                print(f"✅ Eliminada solicitud: {solicitud_id}")
                deleted_count += 1
            else:
                print(f"❌ Error eliminando solicitud {solicitud_id}: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Error procesando solicitud {i}: {e}")
            error_count += 1
    
    # Resumen final
    print(f"\n🎉 Limpieza completada!")
    print(f"✅ Solicitudes eliminadas: {deleted_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📊 Total procesadas: {total_solicitudes}")

if __name__ == "__main__":
    print("🧹 Script de limpieza de base de datos")
    print("=" * 40)
    
    # Confirmar antes de eliminar
    confirm = input("⚠️  ¿Estás seguro de que quieres eliminar TODAS las solicitudes? (s/N): ")
    if confirm.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        exit(0)
    
    clear_database() 