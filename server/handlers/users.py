import json
from responses.responses import Response200, Response201
from responses.errors import BadRequestErr
from fotos import FOTOS_DIR

usuarios_db = [
    {"id": 1, "nombre": "Juan Pérez", "foto": "juan.jpg"},
    {"id": 2, "nombre": "María García", "foto": "maria.jpg"},
    {"id": 3, "nombre": "Carlos López", "foto": "carlos.jpg"}
]

def getUserListRes():
    return Response200(usuarios_db, 'application/json', close_connection=False)

def createUserRes(request_body):
    try:
        data = json.loads(request_body)
        
        if not all(key in data for key in ['id', 'nombre', 'foto', 'imagen_base64']):
            return BadRequestErr("Faltan campos requeridos: id, nombre, foto, imagen_base64")
        
        nuevo_usuario = {
            "id": data["id"],
            "nombre": data["nombre"],
            "foto": data["foto"] 
        }
        
        try:
            os.makedirs(FOTOS_DIR, exist_ok=True)
            
            imagen_bytes = base64.b64decode(data["imagen_base64"])

            foto_path = os.path.join(FOTOS_DIR, data["foto"])
            with open(foto_path, 'wb') as f:
                f.write(imagen_bytes)
                
        except Exception as e:
            return BadRequestErr(f"Error al guardar imagen")
        
        usuarios_db.append(nuevo_usuario)
        
        return Response201(nuevo_usuario, 'application/json', close_connection=False)
    
    except json.JSONDecodeError:
        return BadRequestErr("JSON inválido")
    except Exception as e:
        return BadRequestErr(f"Error al procesar solicitud")