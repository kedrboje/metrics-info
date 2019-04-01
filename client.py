import socket
import time

class Client():
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metrics_name, value, timestamp=None):
        if timestamp == None:
            timestamp = str(int(time.time()))
        try:
            with socket.create_connection((self.host, self.port)) as sock:
                sock.sendall()
        except:
            raise ClientError
        pass

    def get(self, metrics_name):
        pass


class ClientError(Exception):
    pass
