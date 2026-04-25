import json
import socket

from assistant.config import settings


class Server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self) -> None:
        self.socket.bind((settings.HOST, settings.PORT))
        self.socket.listen(5)

    def print_myself(self) -> None:
        ip = socket.gethostbyname(socket.gethostname())
        print(ip)

    def wait_for_data(self) -> None:
        conn, addr = self.socket.accept()
        try:
            data = conn.recv(4096).decode('utf-8')
            req = json.loads(data)
            print(req)
            print(addr)
        except:
            pass
        conn.close()


def listen_for_data() -> None:
    server = Server()
    server.listen()
    server.print_myself()
    server.wait_for_data()
