import socket


class Connection:

    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        from_connection = ':'.join(map(str, self.socket.getsockname()))
        to_connection = ':'.join(map(str, self.socket.getpeername()))
        return f"<Connection from {from_connection} to {to_connection}>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        accumulated_message = bytearray()
        while len(accumulated_message) < size:
            received_message = self.socket.recv(size - len(accumulated_message))
            if received_message:
                accumulated_message.extend(received_message)
            else:
                raise (Exception, 'Connection was closed before all data was received')
        return accumulated_message

    def close(self):
        self.socket.close()

    @classmethod
    def connect(cls, host, port):
        conn = socket.socket()
        conn.connect((host, port))
        return cls(conn)
