import datetime as dt
# from cli import CommandLineInterface
import requests
from .Reader import Reader
from .thought import Thought

# cli = CommandLineInterface()


# @cli.command
def upload_sample(host, port, path):
    url = f'http://{":".join((host, port))}'
    reader = Reader(path)
    server_fields = get_server_fields()
    send_user_data(url, reader)
    send_snapshots_data(url, reader, server_fields)
    thought = Thought(int(user), dt.datetime.now(), thought)
    message = thought.serialize()
    conn = socket.socket()
    conn.connect((host, port))
    connection = Connection(conn)
    connection.send(message)
    connection.close()
    print('done')


def send_user_data(url, reader):
    resp = requests.put(url, headers={'Content-Type': reader.get_data_content_type()},
                        data=reader.get_user_data_ready_to_send())


def get_server_fields():
    return []


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        address = (argv[1].split(':'))
        upload(address, *argv[2:])
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


# if __name__ == '__main__':
#     cli.main()
