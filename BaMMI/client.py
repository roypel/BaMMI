import datetime as dt
# from cli import CommandLineInterface
# from .Reader import Reader
from BaMMI.Reader import Reader
from BaMMI.thought import Thought
from BaMMI.utils.connection import get_from_url, post_from_url

# cli = CommandLineInterface()


# @cli.command
def upload_sample(host: str, port: int, path: str):
    url = f'http://{":".join((host, str(port)))}'
    reader = Reader(path)
    server_accepted_fields = get_server_fields(url)
    send_user_data(url, reader)
    send_snapshots_data(url, reader, server_accepted_fields)


def send_user_data(url: str, reader: Reader):
    post_from_url(url, headers={'Content-Type': reader.get_data_content_type()},
                  data=reader.get_user_data_ready_to_send())


def get_server_fields(url: str):
    return list(get_from_url(url))


def send_snapshots_data(url: str, reader: Reader, server_accepted_fields: list):
    for snapshot in reader.generate_snapshot_data_ready_to_send(server_accepted_fields):
        post_from_url(url, headers={'Content-Type': reader.get_data_content_type()}, data=snapshot)
