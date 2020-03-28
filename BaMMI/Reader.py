import BaMMI.ProtoDriver as ProtoDriver


class Reader:

    def __init__(self, file_path):
        self.reader_driver = find_reader_driver(file_path)
        self._read_file_data()

    def _read_file_data(self):
        self.reader_driver.read_file_data()

    def get_user_data(self):
        return


def find_reader_driver(file_path):
    drivers = {'.mind.gz': ProtoDriver.ProtoDriver}
    for suffix, cls in drivers.items():
        if file_path.endswith(suffix):
            return cls(file_path)


r = Reader(r"C:\Developing\BaMMI\sample.mind.gz")
