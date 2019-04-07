import asyncio


def run_server(host, port):

    local_data = {}
    sorted_data = {}

    async def handle_echo(reader, writer):
        tmp_data = await reader.read(1024)
        await asyncio.sleep(1) # may be deleted
        message = tmp_data.decode()
        
        if message[:3] == 'put':
            data = message[:-1].split(' ')[1:]
            if data[0] not in local_data:
                local_data[data[0]] = [(data[1], data[2])]
            else:
                local_data[data[0]].append((data[1], data[2]))
            writer.write(b'ok\n\n')
            await writer.drain() 
        elif message[:3] == 'get':
            key = message.split(" ")[1]
            for item in local_data:
                tmp_list = sorted(local_data[item], key=lambda x: x[1])
                sorted_data[item] = tmp_list
            print(sorted_data)
            if key == "*":
                pass
            elif key in local_data:
                pass
            else:
                writer.write(b'ok\n\n')
                await writer.drain() 
        else:
            writer.write(b'error\nwrong command\n\n')
            await writer.drain() 
        writer.close()
        # print(local_data) # should be deleted

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

if __name__ == "__main__": # should be deleted
    run_server('127.0.0.1', 8181)