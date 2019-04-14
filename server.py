import asyncio


def run_server(host, port):

    local_data = {}
    sorted_data = {}

    async def handle_echo(reader, writer):
        while True:
            tmp_data = await reader.readline()
            message = tmp_data.decode('utf8')
            await asyncio.sleep(1) # may be deleted

            if message:
                print(message)
                if message[:3] == 'put':

                    data = message[:-1].split(' ')[1:] # delete put and \n
                    m_name = data[0]
                    m_val = data[1]
                    m_timestamp = data[2]
                    
                    if m_name not in local_data:
                        local_data[m_name] = [(float(m_val), int(m_timestamp))]
                    else:
                        if (float(m_val), int(m_timestamp)) not in local_data[m_name]:
                            local_data[m_name].append((float(m_val), int(m_timestamp)))
                        else:
                            pass
                    writer.write(b'ok\n\n')
                    await writer.drain()

                elif message[:3] == 'get':

                    key = message[:-1].split(" ")[1]

                    for item in local_data:
                        tmp_list = sorted(local_data[item], key=lambda x: x[1])
                        sorted_data[item] = tmp_list

                    print(sorted_data)

                    if key is "*":

                        string = "ok"
                        count = 0

                        for k in sorted_data:

                            string = string + "\n" + str(k)

                            for tuple_s in sorted_data[k]:
                                for item in tuple_s:
                                    count += 1
                                    if count <= 2:
                                        string += " " + str(item)
                                    else:
                                        count = 1
                                        string += "\n" + str(k) + " " + str(item)
                            count = 0

                        string += "\n\n"
                        print(string)
                        writer.write(string.encode('utf8'))
                        await writer.drain()

                    elif key in local_data:

                        writer.write(f"ok\n{key} \n\n".encode('utf8'))
                        await writer.drain()
                    else:

                        writer.write(b'ok\n\n')
                        await writer.drain() 
                else:
                    writer.write(b'error\nwrong command\n\n')
                    await writer.drain() 
            else:
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