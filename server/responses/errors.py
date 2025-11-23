def NotImplementedErr(body = None, close_connection:bool = False):
    return (
        "HTTP/1.1 501 Not Implemented\r\n"
        "Access-Control-Allow-Origin: http://127.0.0.1:3001\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body) if body else 0}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{body if body else ''}"
    )

def NotFoundErr(body = None, close_connection:bool = False):
    return (
        "HTTP/1.1 404 Not Found\r\n"
        "Access-Control-Allow-Origin: http://127.0.0.1:3001\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body) if body else 0}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{body if body else ''}"
    )

def BadRequestErr(body = None, close_connection:bool = False):
    return (
        "HTTP/1.1 400 Bad Request\r\n"
        "Access-Control-Allow-Origin: http://127.0.0.1:3001\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body) if body else 0}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{body if body else ''}"
    )