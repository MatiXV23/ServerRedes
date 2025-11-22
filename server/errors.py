def NotImplementedErr(body = None, close_connection:bool = False):
    return (
            "HTTP/1.1 501 Not Implemented\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body) if body else 0}\r\n"
            f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
            "\r\n"
            f"{body}"
        )


def NotFoundErr(body = None):
    return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body) if body else 0}\r\n"
            f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
            "\r\n"
            f"{body}"
        )