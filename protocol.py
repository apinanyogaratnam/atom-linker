import socket
import threading

from log import get_logger

logger = get_logger(__file__)


class TcpProtocol:
    def __init__(self) -> None:
        pass

    def handle_client(self, client_socket: socket.socket) -> None:
        request = client_socket.recv(1024)
        logger.info(f"Received: {request}")
        client_socket.send(b"ACK!")
        client_socket.close()

    def create_server(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 5432))
        server.listen(5)
        logger.info("Server listening on port 5432")

        while True:
            client_sock, addr = server.accept()
            logger.info(f"Accepted connection from: {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_sock,))
            client_handler.start()
 