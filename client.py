import socket
import time


class Client():
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sck = socket.create_connection((self.host, self.port), self.timeout)

    def put(self, metrics_name, value, timestamp=None):
        if timestamp is None:
            timestamp = str(int(time.time()))

        # self.sck.connect((self.host, self.port))
        self.sck.sendall(f"put {metrics_name} {value} {timestamp}\n".encode('utf8'))
        data = self.sck.recv(1024).decode('utf8')
        print(data)
        if data == "error\nwrong command\n\n":
            raise ClientError

        if data == "ok\n\n":
            pass

        # self.sck.close()


    def get(self, metrics_name):
        # self.sck.connect((self.host, self.port))
        self.sck.sendall(f"get {metrics_name}\n".encode('utf8'))

        data = self.sck.recv(1024).decode('utf8')
        print(data)
        if data == "ok\n\n":
            return {}

        fdata = data.split("\n")[1:-2]
        rdata = []
        udata = []
        result = {}
        start = 0

        for item in fdata:
            new_item = item.split(" ")
            rdata.append(new_item)

        for i in rdata:
            udata += i

        for _ in udata:

            if start > len(udata) - 3 :
                break

            m_name = udata[start]
            m_val = udata[ start + 1 ]
            m_timestamp = udata[ start + 2 ]
            start += 3

            if not m_name in result:
                result[m_name] = [(int(m_timestamp), float(m_val))]
            else:
                result[m_name].append((int(m_timestamp), (float(m_val))))

        sorted_result = {}

        for key in result:
            tmp_result = sorted(result[key], key=lambda x: x[0])
            sorted_result[key] = tmp_result

        if metrics_name == "*":
            return sorted_result
        if metrics_name in result:
            return {
                str(metrics_name): result[str(metrics_name)]
            }
        else:
            raise ClientError
        # self.sck.close()


class ClientError(Exception):
    pass

client_one = Client("127.0.0.1", 8181)
client_two = Client("127.0.0.1", 8181)
client_three = Client("127.0.0.1", 8181)
client_four = Client('127.0.0.1', 8181)

client_one.put("m_one", 1, 6)
client_two.put("m_one", 2, 2)
client_three.put("m_one", 3, 3)
client_four.get('*')
