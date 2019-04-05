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
            self.sck.send(f"{metrics_name} {value} {timestamp} \n".encode(utf8))
            time.sleep(1)
            self.sck.close()
        except:
            raise ClientError
        

    def get(self, metrics_name):

        self.sck.connect((self.host, self.port))
        data = self.sck.recv(1024).decode('utf8')
        udata = data.split(" ")
        result = {}
        start = 0

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

