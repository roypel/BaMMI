import struct
from BaMMI.BaMMI_pb2 import User, Snapshot


class Reader:

    def __init__(self, file_path):
        self.user_id = None
        self.user_name = None
        self.user_birth_date = None
        self.user_gender = None
        self.snapshots = []
        with open(file_path, 'rb') as f:
            self.read_user_data(f)

    def read_user_data(self, f):
        self.user_id = _read_bytes_as_format_from_file(f, 64, 'Q')
        name_length = _read_bytes_as_format_from_file(f, 64, 'I')
        self.user_name = _read_bytes_as_format_from_file(f, name_length, f"{name_length}s")
        self.user_birth_date = _read_bytes_as_format_from_file(f, 32, 'I')
        self.user_gender = _read_bytes_as_format_from_file(f, 1, 'c')

    def build_snapshots(self, f):
        while True:
            snapshot_data = f.read()
            self.snapshots = read_snapshot_from_file()


def read_snapshot_from_file(f):
    pass


def _read_bytes_as_format_from_file(f, num_of_bytes, bytes_format, endian='little'):
    """
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
