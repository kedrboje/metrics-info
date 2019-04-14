import asyncio


def run_server(host, port):

    local_data = {}
    sorted_data = {}

    async def handle_echo(reader, writer):
        while True:
            tmp_data = await reader.readline()
            message = tmp_data.decode('utf8')
            await asyncio.sleep(1)  # may be deleted

            if message:
                # print(message)
                if message[:3] == 'put':

                    data = message[:-1].split(' ')[1:]  # delete put and \n
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

                    # print(sorted_data)

                    if key is "*":

                        f_res_str = "ok"
                        count = 0

                        for k in sorted_data:

                            f_res_str += "\n" + str(k)

                            for tuple_f in sorted_data[k]:
                                for item in tuple_f:
                                    count += 1
                                    if count <= 2:
                                        f_res_str += " " + str(item)
                                    else:
                                        count = 1
                                        f_res_str += "\n" + str(k) + " " + str(item)
                            count = 0

                        f_res_str += "\n\n"
                        # print(f_res_str)
                        writer.write(f_res_str.encode('utf8'))
                        await writer.drain()

                    elif key in sorted_data:

                        s_res_str = "ok"
                        c = 0

                        for i in sorted_data:

                            if i == key:

                                s_res_str += "\n" + str(i)
                                
                                for tuple_s in sorted_data[i]:
                                    for item_s in tuple_s:
                                        c += 1
                                        if c <= 2:
                                            s_res_str += " " + str(item_s)
                                        else:
                                            c = 1
                                            s_res_str += "\n" + str(i) + " " + str(item_s)
                                c = 0
                        
                        s_res_str += "\n\n"
                        # print(s_res_str)
                        writer.write(s_res_str.encode('utf8'))
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


if __name__ == "__main__":  # should be deleted
    run_server('127.0.0.1', 8181)
