import asyncio
from protocol import TcpProtocol

if __name__ == "__main__":
    tcp_protocol = TcpProtocol()
    asyncio.run(tcp_protocol.create_server())
