from errors import NotImplementedErr, NotFoundErr
from responses import Response200


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
                    handle_img(cont)    
                    cont = (cont + 1) % len(imgs)
                    
                case "/close":
                    response = Response200("Nos vemos", 'application/json', close_connection=True)
                    conn.sendall(response.encode("utf-8"))
                    conn.close()
                    return
                    
                case _: 
                    response = NotFoundErr("No se encuentra lo que buscas")
                    conn.sendall(response.encode("utf-8"))




def handle_img(idx):
    response = Response200(imgs[idx], 'application/json')
    conn.sendall(response.encode("utf-8"))
    
