import socket
from contextlib import contextmanager


@contextmanager
def init_socket(address: tuple):
    connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
    connection.bind(address)
    connection.listen(100)
    yield connection
    connection.close()


@contextmanager
def receive_connection(binded_socket: socket.socket):
    sock, addr = binded_socket.accept()
    yield sock, addr
    sock.close()


def generate_response(content_text: str):
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
    }
    headers_str = '\n'.join(': '.join(item) for item in headers.items())
    response_text = f'HTTP/1.1 200 OK\n{headers_str}\n\n{content_text}'
    return response_text.encode('utf-8')


if __name__ == '__main__':

    ip_addr = '127.0.0.1'
    port = 8080
    with init_socket((ip_addr, port)) as server_socket:
        while True:
            with receive_connection(server_socket) as (sock, (ip, port)):
                text = '<h1>Hello world</h1><br><div>Вы обратились с ip: {ip}, port: {port}</div>'
                text = text.format(ip=ip, port=port)
                print(ip, port)
                sock.send(generate_response(text))
