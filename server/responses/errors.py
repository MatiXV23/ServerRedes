def NotImplementedErr(body = None, content_type: str = 'text/plain', close_connection:bool = False):
    return (
        "HTTP/1.1 501 Not Implemented\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body) if body else 0}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{body if body else ''}"
    )

def VersionNotSupported(body = None, close_connection:bool = False):
    return (
        "HTTP/1.1 505 Version Not Supported\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT\r\n"
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
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT\r\n"
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
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body) if body else 0}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{body if body else ''}"
    )