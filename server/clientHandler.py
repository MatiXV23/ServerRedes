from responses.errors import *
from responses.responses import *

from handlers.users import getUserListRes, createUserRes
from handlers.fotos import getFotoRes


titulo = 'Listado Cigaran Perez'

def read_full_request(conn):
    # Leer headers
    headers = b""
    while b"\r\n\r\n" not in headers:
        chunk = conn.recv(1024)
        if not chunk:
            return None, None
        headers += chunk
    
    # Separar headers del posible body inicial
    header_end = headers.find(b"\r\n\r\n") + 4
    headers_str = headers[:header_end].decode('utf-8')
    body = headers[header_end:]
    
    # Buscar Content-Length en headers
    content_length = 0
    for line in headers_str.split("\r\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break
    
    # Leer el resto del body si es necesario
    while len(body) < content_length:
        remaining = content_length - len(body)
        chunk = conn.recv(min(8192, remaining))
        if not chunk:
            break
        body += chunk
    
    return headers_str, body


def handle_client(conn, addr):
    print(f"\nNueva conexión desde {addr}\n")

    with conn:
        while True:
            try:
                # Leer el request completo
                headers_str, body_bytes = read_full_request(conn)
                
                if not headers_str:
                    break
                
                first_line = headers_str.split("\r\n")[0]
                print("first line:", first_line)

                parts = first_line.split(" ")
                if len(parts) != 3:
                    print(f"Request malformado: {first_line}")
                    break
                
                method, path, version = parts
                
                if version != 'HTTP/1.1':
                    res = VersionNotSupported(f'Version actual: {version}')
                    conn.sendall(res.encode('utf-8'))
                    continue

                # Decodificar body si existe
                body = ""
                if body_bytes:
                    try:
                        body = body_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        print("Warning: Body contiene datos binarios")
                        body = body_bytes.decode('utf-8', errors='ignore')
                
            except Exception as e:
                print(f"Error parseando request: {e}")
                import traceback
                traceback.print_exc()
                break

            if method == "OPTIONS":
                response = (
                    "HTTP/1.1 204 No Content\r\n"
                    "Access-Control-Allow-Origin: *\r\n"
                    "Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT\r\n"
                    "Access-Control-Allow-Headers: Content-Type\r\n"
                    "Access-Control-Max-Age: 86400\r\n"
                    "\r\n"
                )
                conn.sendall(response.encode("utf-8"))
                continue

            try:
                match path:
                    case "/close":
                        response = Response200('Conexion cerrada', 'application/json', close_connection=True)
                        conn.sendall(response.encode("utf-8"))
                        conn.close()
                        break

                    case "/titulo":
                        if method == "GET":
                            response = Response200(titulo, 'text/plain', close_connection=False)
                        else:
                            response = NotImplementedErr(f'Metodo {method} para {path} no implementado aun')
                        conn.sendall(response.encode("utf-8"))

                    case p if p.startswith("/fotos/"):
                        foto_name = path.split("/fotos/")[1]
                        response = getFotoRes(foto_name)
                        conn.sendall(response)
                        
                    case "/usuarios":
                        match method:
                            case "GET":
                                response = getUserListRes()
                                conn.sendall(response.encode("utf-8"))
                            case "POST":
                                response = createUserRes(body)
                                conn.sendall(response.encode("utf-8"))
                            case "PUT":
                                response = NotImplementedErr(f"Método no implentado aun {method}.")
                                conn.sendall(response.encode("utf-8"))
                            case _:
                                response = NotImplementedErr(f"Método no implentado aun {method}.")
                                conn.sendall(response.encode("utf-8"))
                    

                    case _: 
                        response = NotFoundErr("No se encuentra lo que buscas")
                        conn.sendall(response.encode("utf-8"))
                        
            except BrokenPipeError:
                print(f"Cliente {addr} desconectado abruptamente")
                break
            except Exception as e:
                print(f"Error enviando respuesta: {e}")
                import traceback
                traceback.print_exc()
                break
        print("Conexión finalizada correctamente")
        return 0