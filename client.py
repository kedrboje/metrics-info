import socket
import time

class Client():
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sck = socket.socket()
        # self.sck.connect((self.host, self.port))
        self.sck.settimeout(self.timeout)

    def put(self, metrics_name, value, timestamp=None):
        if timestamp == None:
            timestamp = str(int(time.time()))
        try:
            self.sck.connect((self.host, self.port))
            self.sck.sendall(f"{metrics_name} {value} {timestamp}\n".encode('utf8'))
            data = self.sck.recv(1024).decode('utf8')
            if not data:
                raise ClientError
            if data == "error\nwrong command\n\n":
                raise ClientError
            if data == "ok\n\n":
                pass
            self.sck.close()
        except:
            raise ClientError
        

    def get(self, metrics_name):

        self.sck.connect((self.host, self.port))
        data = self.sck.recv(1024).decode('utf8')

        if data == "ok\n\n":
            raise ClientError

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

        def by_timestamp(stamp):
            return stamp[1]

        for _ in udata:

            if start > len(udata) - 1 :
                break

            m_name = udata[start]
            m_val = udata[ start + 1 ]
            m_timestamp = udata[ start + 2 ]
            start += 3

            if not m_name in result:
                result[m_name] = [(float(m_val), int(m_timestamp))]
            else:
                result[m_name].append((float(m_val), int(m_timestamp)))
                result[m_name].sort(key=by_timestamp)

        if metrics_name is "*":
            return result
        elif metrics_name in result:
            return {
                str(metrics_name): result[str(metrics_name)]
            }
        else:
            return {}
        self.sck.close()


class ClientError(Exception):
    pass

