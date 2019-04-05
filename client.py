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
            self.sck.close()
        except:
            raise ClientError
        

    def get(self, metrics_name):
        self.sck.connect((self.host, self.port))
        data = self.sck.recv(1024).decode('utf8')
        udata = data.split(" ")
        pass
        self.sck.close()


class ClientError(Exception):
    pass

