import asyncio

from errors import InvalidQueryError
from execute_query import ExecuteQuery
from log import get_logger

logger = get_logger(__file__)


class TcpProtocol(ExecuteQuery):
    """TCP protocol for handling client requests.

    This class extends the ExecuteQuery class and implements methods for handling client requests and creating a server.
    The `handle_client_request` method reads data from the client, executes the query using the `execute_query` method,
    and sends a response back to the client. The `create_server` method creates a TCP server and listens for client
    requests.

    Args:
    ----
    self: The instance of the class.
    reader (asyncio.StreamReader): The reader object for reading data from the client.
    writer (asyncio.StreamWriter): The writer object for sending data to the client.

    Returns:
    -------
    None
    """

    async def handle_client_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle a client request.

        This method reads data from the client using the provided `reader` object, decodes the data into a message,
        and logs the received message and client address. It then executes the query using the `execute_query` method
        of the instance. If an `InvalidQueryError` is raised, it logs the error, sends the error message back to the
        client, and closes the connection. Otherwise, it sends an acknowledgement message to the client and closes the
        connection.

        Args:
        ----
        self: The instance of the class.
        reader (asyncio.StreamReader): The reader object for reading data from the client.
        writer (asyncio.StreamWriter): The writer object for sending data to the client.

        Returns:
        -------
        None
        """
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info("peername")
        logger.info(f"Received {message} from {addr}")

        try:
            self.execute_query(message)
        except InvalidQueryError as error:
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
        """Create a TCP server.

        This method creates a TCP server using the `start_server` function from the `asyncio` module. The server listens
        on the IP address "0.0.0.0" and port 5432. It logs the server address and enters a loop to handle client
        requests indefinitely.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        None
        """
        server = await asyncio.start_server(self.handle_client_request, "0.0.0.0", 5432)
        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")

        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    tcp_protocol = TcpProtocol()
    asyncio.run(tcp_protocol.create_server())
