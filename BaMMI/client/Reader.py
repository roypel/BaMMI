from .ProtoDriver import ProtoDriver


class Reader:

    def __init__(self, file_path):
        self.reader_driver = find_reader_driver(file_path)

    def close(self):
        self.reader_driver.close()

    def get_user_data(self):
        return self.reader_driver.get_user_data()

    def get_user_data_ready_to_send(self):
        return self.reader_driver.get_user_data_ready_to_send()

    def get_data_content_type(self):
        return self.reader_driver.get_data_content_type()

    def generate_snapshot_data_ready_to_send(self, server_accepted_fields=None):
        return self.reader_driver.generate_snapshot_data_ready_to_send(server_accepted_fields)


def find_reader_driver(file_path):
    drivers = {'.mind.gz': ProtoDriver}
    for suffix, cls in drivers.items():
        if file_path.endswith(suffix):
            return cls(file_path)
