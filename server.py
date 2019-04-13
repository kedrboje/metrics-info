import asyncio


def run_server(host, port):

    local_data = {}
    sorted_data = {}

    async def handle_echo(reader, writer):
        while True:
            tmp_data = await reader.readline()
            await asyncio.sleep(1) # may be deleted
            if tmp_data:
                message = tmp_data.decode('utf8')
                print(message)
                if message[:3] == 'put':
                    data = message[:-1].split(' ')[1:]
                    if data[0] not in local_data:
                        local_data[data[0]] = [(int(data[2]), float(data[1]))]
                    else:
                        local_data[data[0]].append((int(data[2]), float(data[1])))
                    writer.write(b'ok\n\n')
                    await writer.drain()
                elif message[:3] == 'get':
                    key = message.split(" ")[1]
                    print(key)
                    for item in local_data:
                        tmp_list = sorted(local_data[item], key=lambda x: x[0])
                        sorted_data[item] = tmp_list
                    print(sorted_data)
                    if key == "*":
                        writer.write(b'da\n')
                    elif key in local_data:
                        pass
                    else:
                        writer.write(b'ok\n\n')
                        await writer.drain() 
                        pass
                else:
                    writer.write(b'error\nwrong command\n\n')
                await writer.drain() 
            else:
                print('no data')
                break
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