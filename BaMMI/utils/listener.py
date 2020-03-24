import socket
from .connection import Connection


class Listener:

    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.server = None

    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}', backlog={self.backlog}, reuseaddr={self.reuseaddr})"

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.server = socket.socket()
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)

    def stop(self):
        self.server.close()

    def accept(self):
        client, address = self.server.accept()
        return Connection(client)
