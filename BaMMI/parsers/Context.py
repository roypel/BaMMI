from ..utils import UtilFunctions


class Context:

    def __init__(self, base_path, user_data, snapshot_data):
        self.base_path = base_path
        self.user_id = user_data['user_id']
        self.snapshot_timestamp = snapshot_data['datetime']

    def path(self, file_name):
        return UtilFunctions.build_path_for_files_from_data(self.base_path, self.user_id, self.snapshot_timestamp, file_name)

    def format_returned_data(self, field_name, data):
        return {'datetime': self.snapshot_timestamp, field_name: data}
