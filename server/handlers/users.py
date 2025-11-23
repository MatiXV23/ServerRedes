import json
import os
import base64
from responses.responses import Response200, Response201
from responses.errors import BadRequestErr

FOTOS_DIR = "fotos"

usuarios_db = [
    {"id": 1, "nombre": "Juan Pérez", "foto": "juan.png"},
    {"id": 2, "nombre": "María García", "foto": "maria.png"},
    {"id": 3, "nombre": "Carlos López", "foto": "carlos.png"}
]

def getUserListRes():
    return Response200(usuarios_db, 'application/json', close_connection=False)

def createUserRes(request_body):
    print(f"Usuario Create")
    try:
        print(f"Usuario Create 2")
        data = json.loads(request_body)
        print(f"Usuario Create 3")
        if not all(key in data for key in ['nombre', 'imagen_base64']):
            return BadRequestErr("Faltan campos requeridos: nombre, imagen_base64")
        print(f"Usuario Create 4")
        foto_nombre = data["nombre"].replace(" ", "_") + '.png'

        nuevo_usuario = {
            "id": len(usuarios_db) + 1,
            "nombre": data["nombre"],
            "foto": foto_nombre 
        }
        print(f"usuario: {nuevo_usuario}")
        usuarios_db.append(nuevo_usuario)
        try:
            os.makedirs(FOTOS_DIR, exist_ok=True)

            imagen_bytes = base64.b64decode(data["imagen_base64"])

            foto_path = os.path.join(FOTOS_DIR, foto_nombre)
            with open(foto_path, 'wb') as f:
                f.write(imagen_bytes)
            

        except Exception as e:
            return BadRequestErr(f"Error al guardar imagen")
        
        return Response201(nuevo_usuario, 'application/json', close_connection=False)
    
    except json.JSONDecodeError:
        return BadRequestErr("JSON inválido")
    except Exception as e:
        return BadRequestErr(f"Error al procesar solicitud")