import datetime as dt
import socket
from cli import CommandLineInterface
from connection import Connection
from thought import Thought

cli = CommandLineInterface()


@cli.command
def upload(address, user, thought):
    ip, port = address.split(':')
    port = int(port)
    thought = Thought(int(user), dt.datetime.now(), thought)
    message = thought.serialize()
    conn = socket.socket()
    conn.connect((ip, port))
    connection = Connection(conn)
    connection.send(message)
    connection.close()
    print('done')


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


if __name__ == '__main__':
    cli.main()
