import socket
import threading
from errors import NotImplementedErr, NotFoundErr
import json

HOST = '127.0.0.1'
PORT = 8082

imgs = [
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=300&fit=crop",
    "https://cdn.shortpixel.ai/spai/q_lossless+w_888+to_auto+ret_img/independent-photo.com/wp-content/uploads/2022/03/Karen-Pape-1800x1200.jpeg",
    "https://www.blogdelfotografo.com/wp-content/uploads/2017/10/landscape-640617_1920.jpg"
]

def handle_client(conn, addr):
    print(f"Conexión desde {addr}")
    cont = 0
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

            
            match path:
                case "/foto":
                    response = getResponse200(imgs[cont], 'application/json')
                    conn.sendall(response.encode("utf-8"))
                    cont = (cont + 1) % len(imgs)
                    print(response, cont, len(imgs))
                    
                case "/close":
                    response = getResponseClose("Nos vemos", 'application/json')
                    conn.sendall(response.encode("utf-8"))
                    conn.close()
                    return
                case _: 
                    response = NotFoundErr("No se encuentra lo que buscas")
                    conn.sendall(response.encode("utf-8"))
                    

    




def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server escuchando en http://{HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()



def getResponse200(body, content_type: str):
    payload = json.dumps({"data": body})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(payload.encode("utf-8"))}\r\n"
        "Connection: keep-alive\r\n"
        "\r\n"
        f"{payload}"
    )

def getResponseClose(body, content_type: str):
    payload = json.dumps({"data": body})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(payload.encode("utf-8"))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{payload}"
    )

main()