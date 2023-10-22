import asyncio

from log import get_logger

logger = get_logger(__file__)

async def main() -> None:
    """Connect to the server, send a message, and receive the response.

    Establishes a connection to the server at "localhost" on port 5432 using asyncio.
    Sends the command "CREATE DATABASE test" to the server and waits for the response.
    If the response contains "InvalidQueryError", logs an error message and closes the connection.

    Args:
    ----
    None

    Returns:
    -------
    None
    """
    reader, writer = await asyncio.open_connection("localhost", 5432)

    logger.info("Sending: 'CREATE DATABASE test'")
    writer.write(b"CREATE DATABASE test")

    data = await reader.read(100)

    response = data.decode()
    logger.info(f"Received: {response!r}")

    if "InvalidQueryError" in response:
        logger.error(response)
        return

    logger.info("Closing the connection")
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
