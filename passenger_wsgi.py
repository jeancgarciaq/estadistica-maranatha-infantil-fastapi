import os
import sys
import asyncio

# 1. Asegurar el path de la aplicaci��n
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# 2. Importar tu app de FastAPI desde main_web.py
from main_web import app as fast_app

# 3. Adaptador WSGI a ASGI seguro
def application(environ, start_response):
    status_code = "200 OK"
    response_headers = []
    body_chunks = []

    path_info = environ.get('PATH_INFO', '')
    script_name = environ.get('SCRIPT_NAME', '')
    request_method = environ.get('REQUEST_METHOD', '')

    # La app se sirve en la raíz del subdominio (sin prefijo /semi).
    # Si llega una URL legada con /semi, se recorta para que las rutas coincidan.
    if path_info.startswith('/semi'):
        path_info = path_info[len('/semi'):] or '/'

    print(f"--> [WSGI ENTRADA] Method: {request_method} | PATH_INFO: '{path_info}' | SCRIPT_NAME: '{script_name}'")

    async def receive():
        try:
            length = int(environ.get('CONTENT_LENGTH', 0) or 0)
        except ValueError:
            length = 0
        
        body = environ['wsgi.input'].read(length) if length > 0 else b''
        return {
            'type': 'http.request',
            'body': body,
            'more_body': False,
        }

    async def send(message):
        nonlocal status_code, response_headers, body_chunks

        if message['type'] == 'http.response.start':
            status_code = f"{message['status']} Status"
            headers_list = []
            
            for name, value in message.get('headers', []):
                header_name = name.decode('latin1')
                header_val = value.decode('latin1')

                if header_name.lower() == 'location':
                    print(f"<-- [ASGI SALIDA] Header Location generado por Python: {header_val}")

                headers_list.append((header_name, header_val))
                
            response_headers = headers_list

        elif message['type'] == 'http.response.body':
            body_chunks.append(message.get('body', b''))
    
    print("=" * 60)
    print("REQUEST_METHOD:", environ.get("REQUEST_METHOD"))
    print("REQUEST_URI:", environ.get("REQUEST_URI"))
    print("PATH_INFO:", environ.get("PATH_INFO"))
    print("SCRIPT_NAME:", environ.get("SCRIPT_NAME"))
    print("=" * 60)

    scope = {
        'type': 'http',
        'asgi': {'version': '3.0'},
        'http_version': '1.1',
        'method': environ['REQUEST_METHOD'],
        'path': path_info or '/',
        'raw_path': (path_info or '/').encode('latin1'),
        'query_string': environ.get('QUERY_STRING', '').encode('latin1'),
        'root_path': script_name,
        'scheme': environ.get('wsgi.url_scheme', 'http'),
        'headers': [
            (k[5:].lower().replace('_', '-').encode('latin1'), v.encode('latin1'))
            for k, v in environ.items()
            if k.startswith('HTTP_')
        ],
    }

    if 'CONTENT_TYPE' in environ:
        scope['headers'].append((b'content-type', environ['CONTENT_TYPE'].encode('latin1')))
    if 'CONTENT_LENGTH' in environ:
        scope['headers'].append((b'content-length', environ['CONTENT_LENGTH'].encode('latin1')))

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(fast_app(scope, receive, send))
        loop.close()
    except Exception as e:
        status_code = "500 Internal Server Error"
        response_headers = [('Content-Type', 'text/plain; charset=utf-8')]
        body_chunks = [f"Error en adaptador Python: {str(e)}".encode('utf-8')]

    start_response(status_code, response_headers)
    return body_chunks

app = application