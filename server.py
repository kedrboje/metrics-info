import asyncio


def run_server(host, port):

    data = {}

    pass

    async def handle_echo(reader, writer):
        tmp_data = await reader.read(1024)
        await asyncio.sleep(1)
        message = tmp_data.decode()
        print(message)

        writer.write(b'ok\n\n')
        await writer.drain()     
        writer.close()

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, host=host, port=port, loop=loop)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server('127.0.0.1', 8181)