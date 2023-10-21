import socket

from log import get_logger

logger = get_logger(__file__)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5432))
    client.send(b"Hello, Server!")
    response = client.recv(4096)
    logger.info(response)

if __name__ == "__main__":
    main()
