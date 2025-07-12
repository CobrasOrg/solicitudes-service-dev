#!/usr/bin/env python3
"""
Script para ejecutar pruebas de despliegue y generar PDF
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.deployment.test_deployment import main

if __name__ == "__main__":
    main() 