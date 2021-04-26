import socket


if __name__ == '__main__':
    client_socket = socket.socket()
    client_socket.bind(('127.0.0.1', 46283))
    client_socket.connect(('127.0.0.1', 8080))
    content = 'hi'.encode()
    client_socket.send(content)
    client_socket.close()
