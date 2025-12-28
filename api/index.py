"""
Vercel serverless function entry point for Django
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Import Django and setup
import django
django.setup()

# Import WSGI application
from config.wsgi import application

# Vercel Python handler - simple wrapper
def handler(request):
    """Vercel serverless function handler for Django WSGI"""
    from io import BytesIO
    
    # Extract request data
    method = request.method
    path = request.path
    query_string = request.query_string or ''
    headers = dict(request.headers)
    body = request.body if hasattr(request, 'body') else b''
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('Content-Type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'SERVER_NAME': headers.get('Host', 'localhost').split(':')[0],
        'SERVER_PORT': headers.get('Host', 'localhost').split(':')[1] if ':' in headers.get('Host', '') else '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https' if headers.get('X-Forwarded-Proto') == 'https' else 'http',
        'wsgi.input': BytesIO(body),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers to environ
    for key, value in headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    # Call WSGI application
    response_data = []
    status_code = 200
    response_headers = []
    
    def start_response(status, headers):
        nonlocal status_code, response_headers
        status_code = int(status.split()[0])
        response_headers = headers
    
    result = application(environ, start_response)
    
    # Build response body
    body = b''.join(result) if result else b''
    
    # Convert headers to dict
    headers_dict = dict(response_headers)
    
    # Return response in Vercel format
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': body.decode('utf-8') if isinstance(body, bytes) else body
    }


