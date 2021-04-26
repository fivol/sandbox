from typing import Callable
from json import dumps


def app(environ: dict, start_response: Callable):
    response = {
        'hello ': ''
    }
    data = b"Hello, World!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])

