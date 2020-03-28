import gzip
import struct
from BaMMI.BaMMI_pb2 import User, Snapshot


class ProtoDriver:
    def __init__(self, file_path):
        self.file_path = file_path
        self.user = None
        self.snapshots = []

    def read_file_data(self):
        with gzip.open(self.file_path) as f:
            self.read_user_data(f)
            self.read_snapshots_data(f)

    def read_user_data(self, f):
        user_data_length = _read_message_length(f)
        self.user = User()
        self.user.ParseFromString(f.read(user_data_length))

    def read_snapshots_data(self, f):
        while True:
            snapshot_length = _read_message_length(f)
            if snapshot_length:
                snapshot = Snapshot()
                snapshot.ParseFromString(f.read(snapshot_length))
                self.snapshots.append(snapshot)
            else:  # EOF reached, no more snapshots
                break


def _read_message_length(f):
    return _read_bytes_as_format_from_file(f, 4, 'I')


def _read_bytes_as_format_from_file(f, num_of_bytes, bytes_format, endian='little'):
    """
    A relic from a time where reading binary data was the norm.
    Helper function to read bytes from a file and parse them according to the given format.
    :param f: An open file to read bytes from.
    :param num_of_bytes: The number of bytes that is required to read.
    :param bytes_format: The format which the bytes aligned to know how to unpack them.
    :param endian: little/big, according to the data endianness.
    :return: The data in the file according to the arguments given.
    """
    if endian.lower() == 'little':
        endian = '<'
    elif endian.lower() == 'big':
        endian = '>'
    else:
        raise ValueError("Endian should be 'little' or 'big'")
    return struct.unpack(f'{endian}{bytes_format}', f.read(num_of_bytes))[0]


