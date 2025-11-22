from responses.errors import *
from responses.responses import *

from handlers.users import getUserListRes
from handlers.fotos import getFotoRes


titulo = 'Listado Cigaran Perez'

def handle_client(conn, addr):
    print(f"Conexión desde {addr}")

    with conn:
        while True:
            request = conn.recv(1024).decode('utf-8')
            first_line = request.split("\r\n")[0]
            print("first line:", first_line)

            try:
                method, path, _ = first_line.split(" ")
            except ValueError:
                conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                continue
            
            body = ""
            if method == "POST":
                parts = request.split("\r\n\r\n")
                if len(parts) > 1:
                    body = parts[1]

            match path:
                case "/titulo":
                    if method=="GET":
                        response = Response200(titulo , 'application/json', close_connection=True)
                    else:
                        response = NotImplementedErr(f'Metodo {method} para {path} no implementado aun')
                    conn.sendall(response.encode("utf-8"))

                case p if p.startswith("/fotos/"):
                    foto_name = path.split("/fotos/")[1]
                    response = getFotoRes(foto_name)
                    if isinstance(response, bytes):
                        conn.sendall(response)
                    else:
                        conn.sendall(response.encode("utf-8"))
                
                case "/usuarios":
                    match method:
                        case "GET":
                            response = getUserListRes()
                            conn.sendall(response.encode("utf-8"))
                        case "POST":
                            response = createUserRes(body)
                            conn.sendall(response.encode("utf-8"))
                        case _:
                            response = BadRequestErr("Método no permitido")
                            conn.sendall(response.encode("utf-8"))
                
                case "/close":
                    response = Response200('Conexion cerrada' , 'application/json', close_connection=True)
                    conn.sendall(response.encode("utf-8"))
                    conn.close()
                    return

                case _: 
                    response = NotFoundErr("No se encuentra lo que buscas")
                    conn.sendall(response.encode("utf-8"))





