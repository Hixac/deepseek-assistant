from collections.abc import Generator
from contextlib import contextmanager
import json
import socket as sockt
from socket import socket as Socket

from zeroconf import ServiceInfo, Zeroconf

from assistant.schemas import Protocol
from assistant.config import settings


class Server:
    def raw_data(self) -> Protocol | None:
        return self.data

    def get_guest_socket(self) -> Socket | None:
        return self.guest_socket

    def __init__(self) -> None:
        self.data: Protocol | None = None
        self.guest_socket: Socket | None = None

        self.socket = Socket(sockt.AF_INET, sockt.SOCK_STREAM)
        self.socket.setsockopt(sockt.SOL_SOCKET, sockt.SO_REUSEADDR, 1)

    def register_zeroconf(self) -> tuple[Zeroconf, ServiceInfo]:
        info = ServiceInfo(
            "_cmd._tcp.local.",
            "RemoteCmdServer._cmd._tcp.local.",
            addresses=[sockt.inet_aton(sockt.gethostbyname(sockt.gethostname()))],
            port=settings.PORT,
            properties={"version": "1.0"}
        )
        zc = Zeroconf()
        zc.register_service(info)
        return zc, info

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

            self.data = Protocol.model_validate(req)
        except ConnectionRefusedError:
            print("Server is not running or IP/port is wrong")
        except Exception as e:
            print(f"Client error: {e}")
        self.guest_socket = conn

    def answer(self, msg: str) -> None:
        guest_socket = self.get_guest_socket()
        if guest_socket is not None:
            guest_socket.sendall(msg.encode("utf-8"))
            guest_socket.close()

    def close(self) -> None:
        if (guest_socket := self.get_guest_socket()) is not None:
            guest_socket.close()
        self.socket.close()


class StupidServer:
    def __init__(self, server: Server) -> None:
        self.server = server

    def wait_for_data(self) -> Protocol | None:
        self.server.wait_for_data()
        return self.server.raw_data()

    def answer(self, msg: str) -> None:
        self.server.answer(msg)


@contextmanager
def listen_for_data() -> Generator[StupidServer]:
    server = Server()
    zc, info = server.register_zeroconf()
    server.listen()
    server.print_myself()

    yield StupidServer(server)

    zc.unregister_service(info)
    zc.close()
    server.close()
