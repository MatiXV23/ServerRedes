import os
from responses.errors import NotFoundErr

FOTOS_DIR = "fotos"

def getFotoRes(foto_name):
    foto_path = os.path.join(FOTOS_DIR, foto_name)
    
    os.makedirs('fotos', exist_ok=True)
    if not os.path.exists(foto_path):
        return NotFoundErr(f"Foto '{foto_name}' no encontrada").encode('utf-8')
    
    try:
        with open(foto_path, 'rb') as f:
            foto_data = f.read()
        
        extension = foto_name.lower().split('.')[-1]
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
        }
        content_type = content_types.get(extension, 'application/octet-stream')
        
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Access-Control-Allow-Origin: http://127.0.0.1:3001\r\n"
            "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
            "Access-Control-Allow-Headers: Content-Type\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(foto_data)}\r\n"
            "Connection: keep-alive\r\n"
            "\r\n"
        )
        

        return response_headers.encode('utf-8') + foto_data
    
    except Exception as e:
        return NotFoundErr(f"Error al leer foto: {str(e)}").encode('utf-8')