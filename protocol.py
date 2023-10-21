import asyncio
from errors import InvalidQueryException

from execute_query import ExecuteQuery
from log import get_logger

logger = get_logger(__file__)


class TcpProtocol(ExecuteQuery):
    async def handle_client_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info("peername")
        logger.info(f"Received {message} from {addr}")

        try:
            self.execute_query(message)
        except InvalidQueryException as error:
            logger.error(f"Invalid query: {error}")
            msg = str(error)
            writer.write(bytes(msg, "utf-8"))
            await writer.drain()
            writer.close()
            return

        logger.info("Send: ACK!")
        writer.write(b"ACK!")
        await writer.drain()
        writer.close()

    async def create_server(self) -> None:
        server = await asyncio.start_server(self.handle_client_request, "0.0.0.0", 5432)
        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    tcp_protocol = TcpProtocol()
    asyncio.run(tcp_protocol.create_server())
