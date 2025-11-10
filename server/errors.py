def NotImplementedErr(body = None):
    return (
            "HTTP/1.1 501 Not Implemented\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body) if body else 0}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )


def NotFoundErr(body = None):
    return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body) if body else 0}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )