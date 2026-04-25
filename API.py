import json
import socket as sockt
from socket import socket as Socket
from typing import Any


class API:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def _create_socket(self) -> Socket:
        socket = Socket()
        socket.connect((self.ip, 12345))
        return socket

    def send_data(self, data: dict[Any, Any]) -> str:
        socket = self._create_socket()
        socket.sendall(json.dumps(data).encode("utf-8"))
        return self._response(socket)

    def _response(self, server_socket: Socket) -> str:
        return server_socket.recv(4096).decode("utf-8")


def send_some_data() -> None:
    api = API(input("IP: "))
    print(api.send_data({"lol": "kek"}))


send_some_data()
