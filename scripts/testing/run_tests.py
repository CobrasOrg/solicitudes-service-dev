#!/usr/bin/env python3
"""
Script para ejecutar tests rápidos o completos
Uso: python run_tests.py [quick|full]
"""

import sys
import subprocess
import os

def run_quick_tests():
    """Ejecutar tests rápidos de funcionalidad"""
    print("🧪 Ejecutando tests rápidos...")
    
    # Tests básicos de funcionalidad
    test_files = [
        "tests/test_deployment.py",
        "tests/test_solicitudes.py::test_get_solicitudes_vet",
        "tests/test_solicitudes.py::test_get_solicitudes_user",
        "tests/test_solicitudes.py::test_create_solicitud_vet",
        "tests/test_solicitudes.py::test_create_solicitud_user"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"📋 Ejecutando: {test_file}")
            result = subprocess.run([
                "python", "-m", "pytest", test_file, "-v", "--tb=short"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {test_file}: PASÓ")
            else:
                print(f"❌ {test_file}: FALLÓ")
                print(result.stdout)
                print(result.stderr)
        else:
            print(f"⚠️ Archivo no encontrado: {test_file}")

def run_full_tests():
    """Ejecutar todos los tests"""
    print("🧪 Ejecutando todos los tests...")
    
    result = subprocess.run([
        "python", "-m", "pytest", "tests/", "-v"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Todos los tests pasaron")
    else:
        print("❌ Algunos tests fallaron")
        print(result.stdout)
        print(result.stderr)

def main():
    if len(sys.argv) != 2:
        print("❌ Uso: python run_tests.py [quick|full]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "quick":
        run_quick_tests()
    elif mode == "full":
        run_full_tests()
    else:
        print("❌ Modo inválido. Use 'quick' o 'full'")
        sys.exit(1)

if __name__ == "__main__":
    main() 