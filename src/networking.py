import socket
from .config import HEADER


def recv(from_conn: socket.socket):
    return from_conn.recv(HEADER).decode().strip()


def send(to_conn: socket.socket, data: str):
    data = data.encode()
    data += b' ' * (HEADER - len(data))
    to_conn.send(data)


