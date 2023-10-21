import asyncio
from log import get_logger

logger = get_logger(__file__)

async def main():
    reader, writer = await asyncio.open_connection('localhost', 5432)

    logger.info('Sending: Hello, Server!')
    writer.write(b'Hello, Server!')

    data = await reader.read(100)
    logger.info(f'Received: {data.decode()!r}')

    logger.info('Closing the connection')
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
