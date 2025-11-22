def Response200(body, content_type: str, close_connection:bool = False):
    payload = json.dumps({"data": body})
    return (
        "HTTP/1.1 200 OK\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(payload.encode("utf-8"))}\r\n"
        f"Connection: {'close' if close_connection else 'keep-alive'}\r\n"
        "\r\n"
        f"{payload}"
    )