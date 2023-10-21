import asyncio
import multiprocessing

async def handle_client(reader, writer):
    data = await reader.read(100)
    # process data (I/O-bound)
    await asyncio.to_thread(cpu_bound_task, data)  # Offload CPU-bound task to thread
    writer.write(b"Response")
    await writer.drain()
    writer.close()

def cpu_bound_task(data):
    # perform some CPU-bound computation
    pass

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    asyncio.run(main())
