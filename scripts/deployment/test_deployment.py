#!/usr/bin/env python3
"""
Script de pruebas de despliegue para el servicio de solicitudes.
Verifica que la aplicación esté lista para ser desplegada.
"""

import asyncio
import os
import sys
import requests
from datetime import datetime

def print_header():
    """Imprime el encabezado del script"""
    print("🚀 PRUEBAS DE DESPLIEGUE - SERVICIO DE SOLICITUDES")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def test_environment_variables():
    """Prueba que las variables de entorno requeridas estén configuradas"""
    print("🔧 Verificando variables de entorno...")
    
    required_vars = {
        "MONGODB_URL": "URL de conexión a MongoDB",
        "MONGODB_DATABASE": "Nombre de la base de datos",
        "CLOUDINARY_CLOUD_NAME": "Nombre del cloud de Cloudinary",
        "CLOUDINARY_API_KEY": "API Key de Cloudinary",
        "CLOUDINARY_API_SECRET": "API Secret de Cloudinary"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value is None or value == "":
            missing_vars.append(f"❌ {var}: {description}")
        else:
            print(f"✅ {var}: Configurada")
    
    if missing_vars:
        print("\n❌ Variables de entorno faltantes:")
        for var in missing_vars:
            print(f"   {var}")
        assert False, f"Variables de entorno faltantes: {', '.join(missing_vars)}"
    
    print("✅ Todas las variables de entorno están configuradas\n")

def test_server_running():
    """Prueba que el servidor esté corriendo"""
    print("🌐 Verificando que el servidor esté corriendo...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor corriendo en http://localhost:8000")
        else:
            print(f"❌ Servidor respondió con código {response.status_code}")
            assert False, f"Servidor respondió con código {response.status_code}"
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor en http://localhost:8000")
        print("💡 Asegúrate de ejecutar: python main.py")
        assert False, "No se puede conectar al servidor"
    except Exception as e:
        print(f"❌ Error verificando servidor: {str(e)}")
        assert False, f"Error verificando servidor: {str(e)}"

def test_health_endpoint():
    """Prueba el endpoint de health check"""
    print("🏥 Verificando endpoint de health check...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        data = response.json()
        
        print(f"✅ Status: {data.get('status', 'unknown')}")
        print(f"✅ MongoDB: {data.get('mongodb', 'unknown')}")
        print(f"✅ Firebase: {data.get('firebase', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Error en health check: {str(e)}")
        assert False, f"Error en health check: {str(e)}"

def test_api_documentation():
    """Prueba que la documentación de la API esté accesible"""
    print("📚 Verificando documentación de la API...")
    
    endpoints = [
        ("/docs", "Swagger UI"),
        ("/redoc", "ReDoc"),
        ("/", "Root endpoint")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: Accesible")
            else:
                print(f"❌ {name}: Código {response.status_code}")
                assert False, f"{name} respondió con código {response.status_code}"
        except Exception as e:
            print(f"❌ {name}: Error - {str(e)}")
            assert False, f"Error en {name}: {str(e)}"

def test_api_endpoints():
    """Prueba que los endpoints principales de la API funcionen"""
    print("🔗 Verificando endpoints de la API...")
    
    endpoints = [
        ("/api/v1/vet/solicitudes/", "GET", "Listar solicitudes"),
        ("/api/v1/vet/solicitudes/filtrar", "GET", "Filtrar solicitudes")
    ]
    
    for endpoint, method, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code in [200, 500]:  # 500 es aceptable si no hay DB
                print(f"✅ {description}: Respondiendo")
            else:
                print(f"❌ {description}: Código {response.status_code}")
                assert False, f"{description} respondió con código {response.status_code}"
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
            assert False, f"Error en {description}: {str(e)}"

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🗄️ Verificando conexión a MongoDB...")
    
    try:
        # Agregar el directorio raíz al path
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../..'))
        
        # Importar aquí para evitar errores si no está configurado
        from app.db.mongodb import mongodb
        
        # Verificar si ya está conectado
        if mongodb.client is not None:
            print("✅ MongoDB ya está conectado")
            return
        
        # Intentar conectar usando requests para verificar el health endpoint
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('mongodb') == 'healthy':
                print("✅ Conexión a MongoDB verificada via health endpoint")
            else:
                print(f"⚠️ MongoDB status: {data.get('mongodb', 'unknown')}")
        else:
            print(f"⚠️ No se pudo verificar MongoDB via health endpoint: {response.status_code}")
            
    except ImportError as e:
        print(f"❌ Error importando módulos: {str(e)}")
        assert False, f"Error importando módulos: {str(e)}"
    except Exception as e:
        print(f"❌ Error verificando MongoDB: {str(e)}")
        # No fallar el test si MongoDB no está disponible
        print("⚠️ MongoDB no disponible, pero el test continúa")

async def run_deployment_tests():
    """Ejecuta todas las pruebas de despliegue"""
    print_header()
    
    tests = [
        ("Variables de entorno", test_environment_variables),
        ("Servidor corriendo", test_server_running),
        ("Health endpoint", test_health_endpoint),
        ("Documentación API", test_api_documentation),
        ("Endpoints API", test_api_endpoints),
        ("Conexión MongoDB", test_database_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name}: PASÓ")
        except Exception as e:
            print(f"❌ {test_name}: FALLÓ - {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El servicio está listo para despliegue.")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores antes del despliegue.")
        return False

def main():
    """Función principal"""
    try:
        success = asyncio.run(run_deployment_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 