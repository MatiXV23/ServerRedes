import os
from responses.errors import NotFoundErr

FOTOS_DIR = "fotos"

def getFotoRes(foto_name):
    foto_path = os.path.join(FOTOS_DIR, foto_name)
    
    if not os.path.exists(foto_path):
        return NotFoundErr(f"Foto '{foto_name}' no encontrada")
    
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
        
        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += f"Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        response += f"Access-Control-Allow-Headers: Content-Type\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(foto_data)}\r\n"
        response += f"Connection: keep-alive\r\n"
        response += "\r\n"
        
        return response.encode('utf-8') + foto_data
    
    except Exception as e:
        return NotFoundErr(f"Error al leer foto: {str(e)}")