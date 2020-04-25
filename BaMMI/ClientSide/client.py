# from cli import CommandLineInterface
# from .Reader import Reader
from BaMMI.ClientSide.Reader import Reader
from BaMMI.utils.connection import get_from_url, post_from_url

# cli = CommandLineInterface()


# @cli.command
def upload_sample(host: str, port: int, path: str):
    url = '/'.join((f'http://{":".join((host, str(port)))}', 'transfers'))
    reader = Reader(path)
    server_accepted_fields = get_server_fields('/'.join((url, 'config')))
    send_user_data('/'.join((url, 'users')), reader)
    send_snapshots_data('/'.join((url, 'snapshots')), reader, server_accepted_fields)


def send_user_data(url: str, reader: Reader):
    post_from_url(url, headers={'Content-Type': reader.get_data_content_type()},
                  data=reader.get_user_data_ready_to_send())


def get_server_fields(url: str):
    return get_from_url(url).json()


def send_snapshots_data(url: str, reader: Reader, server_accepted_fields: list):
    user_id = reader.get_user_data().user_id
    for snapshot in reader.generate_snapshot_data_ready_to_send(server_accepted_fields):
        post_from_url(url, headers={'Content-Type': reader.get_data_content_type(),
                                    'user-id': str(user_id)}, data=snapshot)


upload_sample('127.0.0.1', 5000, r"/sample.mind.gz")
