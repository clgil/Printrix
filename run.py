#!/usr/bin/env python3
"""
Punto de entrada principal para la aplicación
Sistema de Gestión de Talleres de Impresoras
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Ejecutar en modo debug solo para desarrollo
    # En producción usar: waitress-serve --port=5000 run:app
    app.run(host='0.0.0.0', port=5000, debug=True)
