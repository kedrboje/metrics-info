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
                sock.sendall(f"{metrics_name} {value} {timestamp} \n".encode('utf8'))
        except:
            raise ClientError
        

    def get(self, metrics_name):
        try:
            with socket.create_connection((self.host, self.port)) as sock:
                data = sock.recv(1024)
                # data.decode('utf8')
                # data = data.split(" ")
                # for item in data:
                    # if item[]
                # print(data.decode('utf8'))
        except:
            raise ClientError


class ClientError(Exception):
    pass


client = Client("127.0.0.1", 10001)
client.put("asd", 3)
client.put("qwe", 4)
client.put("zxc", 5)
client.get("asd")