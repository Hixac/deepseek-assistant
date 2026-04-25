import sys
import json
import socket as sockt
from socket import socket as Socket
from typing import Any, override

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class CmdListener(ServiceListener):
    def __init__(self):
        self.server_ip = None
        self.server_port = None

    @override
    def add_service(self, zc: Zeroconf, type_: str, name: str):
        info = zc.get_service_info(type_, name)
        if info and not self.server_ip:
            # Take the first IPv4 address
            for addr in info.addresses:
                ip = sockt.inet_ntoa(addr)
                print(ip)
                if ip.startswith("127."):  # skip localhost
                    continue
                self.server_ip = ip
                self.server_port = info.port
                print(f"Discovered server at {ip}:{self.server_port}")
                break


def discover_server(timeout: int = 3):
    zc = Zeroconf()
    listener = CmdListener()
    _ = ServiceBrowser(zc, "_cmd._tcp.local.", listener)
    try:
        import time
        start = time.time()
        while listener.server_ip is None and (time.time() - start) < timeout:
            time.sleep(0.1)
    finally:
        zc.close()
    return listener.server_ip, listener.server_port


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
        return server_socket.recv(1096 * 20).decode("utf-8")


def send_some_data(data: dict[Any, Any]) -> None:
    ip, _ = discover_server()
    if ip is None:
        print("No ip is present or server is down")
        exit(1)
    print(ip)
    api = API(ip)
    print(api.send_data(data))


if len(sys.argv) == 2:
    if not sys.argv[1].endswith(".json"):
        print("wrong format")
        exit(1)

    with open(sys.argv[1]) as f:
        data = f.read()

    send_some_data(json.loads(data))
