import json
import socket as sockt
from socket import socket as Socket

from assistant.config import settings


class Server:
    def __init__(self) -> None:
        self.socket = Socket(sockt.AF_INET, sockt.SOCK_STREAM)
        self.socket.setsockopt(sockt.SOL_SOCKET, sockt.SO_REUSEADDR, 1)

    def listen(self) -> None:
        self.socket.bind((settings.HOST, settings.PORT))
        self.socket.listen(5)

    def print_myself(self) -> None:
        ip = sockt.gethostbyname(sockt.gethostname())
        print(ip)

    def panic(self, msg: str, guest_socket: Socket) -> None:
        guest_socket.sendall(msg.encode("utf-8"))
        self.close()

    def wait_for_data(self) -> None:
        conn, addr = self.socket.accept()
        try:
            data = conn.recv(4096).decode('utf-8')
            req = json.loads(data)
            if "msg" not in req:
                return self.panic("No msg key in json data!", conn)
            if "rules" not in req:
                return self.panic("No rules key in json data!", conn)
        except ConnectionRefusedError:
            print("Server is not running or IP/port is wrong")
        except Exception as e:
            print(f"Client error: {e}")
        conn.close()

    def close(self) -> None:
        self.socket.close()


def listen_for_data() -> None:
    server = Server()
    server.listen()
    server.print_myself()
    server.wait_for_data()
    server.close()
