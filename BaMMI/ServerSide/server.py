import datetime
from os import makedirs, path
import struct
import threading
import click
from flask import Flask, request
from BaMMI.utils.listener import Listener



class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        self.handle_connection()

    def handle_connection(self):
        timestamp, user_id, thought = get_user_data(self.connection)
        self.lock.acquire()
        save_user_data(self.data_dir, timestamp, user_id, thought)
        self.lock.release()


def save_user_data(data_dir, timestamp, user_id, thought):
    timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    output_directory = path.join(data_dir, str(user_id),)
    ensure_dir(output_directory)
    full_file_path = path.join(output_directory, f"{timestamp}.txt")
    if path.isfile(full_file_path):
        add_newline = True
    else:
        add_newline = False
    with open(full_file_path, 'a') as f:
        if add_newline:
            f.write('\n')
        f.write(f'{thought}')


def get_user_data(connection):
    client_data = connection.receive(20)
    user_id, timestamp, thought_size = struct.unpack('<QQL', client_data)
    thought = connection.receive(thought_size)
    thought = struct.unpack('>{}s'.format(thought_size), thought)[0].decode("utf-8")
    timestamp_vec6_format = datetime.datetime.fromtimestamp(timestamp)
    return timestamp_vec6_format, user_id, thought


# @click.command
# @click.option()
def run(address, data):
    ip, port = address.split(':')
    port = int(port)
    listener = Listener(port, ip)
    listener.start()
    try:
        while True:
            connection = listener.accept()
            handler = Handler(connection, data)
            handler.start()
    except KeyboardInterrupt:
        listener.stop()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address = argv[1].split(':')
        address[1] = int(address[1])
        run(tuple(address), argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
