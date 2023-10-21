import asyncio

from log import get_logger

logger = get_logger(__file__)

async def main():
    reader, writer = await asyncio.open_connection("localhost", 5432)

    logger.info("Sending: 'CREATE DATABASE test'")
    writer.write(b"CREATE DATABASE test")

    data = await reader.read(100)

    response = data.decode()
    logger.info(f"Received: {response!r}")

    if "InvalidQueryException" in response:
        logger.error(response)
        return

    logger.info("Closing the connection")
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
