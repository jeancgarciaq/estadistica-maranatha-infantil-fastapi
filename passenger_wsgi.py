#!/usr/bin/env python3
"""
Entry point para cPanel Python App (Passenger)
COLOCAR EN: Raíz de la aplicación (mismo nivel que main_web.py)
"""

import os
import sys

# Añadir el directorio de la app al path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

# Configurar variable de entorno para que use el puerto correcto
# cPanel asigna un puerto via variable de entorno PASSENGER_APP_PORT
# o se puede obtener del archivo passenger_wsgi.ini
port = os.environ.get('PASSENGER_APP_PORT', os.environ.get('PORT', '8555'))
os.environ['PORT'] = port

# Importar la app FastAPI
from main_web import app

# Para Passenger WSGI, necesitamos un objeto application WSGI
# FastAPI es ASGI, así que usamos uvicorn como adaptador
# Passenger 6+ soporta ASGI nativamente si se configura bien

# Si Passenger llama a este archivo como WSGI:
try:
    from uvicorn.middleware.wsgi import WSGIMiddleware
    application = WSGIMiddleware(app)
except ImportError:
    # Fallback: crear wrapper simple
    def application(environ, start_response):
        """WSGI adapter simple para FastAPI"""
        from wsgiref.util import request_uri
        import asyncio
        
        # Esta es una implementación mínima - en producción
        # se recomienda usar uvicorn + Passenger ASGI mode
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Use Passenger ASGI mode for FastAPI']

# Para modo ASGI nativo (Passenger 6+), exportar la app directamente
# Passenger detectará automáticamente si es ASGI
__all__ = ['app', 'application']