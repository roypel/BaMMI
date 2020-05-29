import gzip
import struct
from ..BaMMI_pb2 import User, Snapshot


class ProtoDriver:
    def __init__(self, file_path):
        import os
        print(os.getcwd())

        self.f = gzip.open(file_path, 'rb')
        self.user = None

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    def get_user_data(self):
        if self.user is None and not self.f:
            raise RuntimeError("User data wasn't saved before file closed")
        if self.user is None:  # If we got here, self.f is already opened
            user_data_length = _read_message_length(self.f)
            user = User()
            user.ParseFromString(self.f.read(user_data_length))
            self.user = user
        return self.user

    def get_user_data_ready_to_send(self):
        return self.get_user_data().SerializeToString()

    def generate_snapshot_data_ready_to_send(self, server_accepted_fields):
        while self.f:
            snapshot_length = _read_message_length(self.f)
            if snapshot_length:
                snapshot = Snapshot()
                snapshot.ParseFromString(self.f.read(snapshot_length))
                for field in snapshot.ListFields():
                    field_name = field[0].name
                    if field_name not in server_accepted_fields:
                        snapshot.ClearField(field_name)
                yield snapshot.SerializeToString()
            else:  # EOF reached, no more snapshots
                break

    @staticmethod
    def get_data_content_type():
        return 'application/protobuf'


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


