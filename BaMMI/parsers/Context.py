import os
from ..utils import UtilFunctions


class Context:

    def __init__(self, base_path, user_data, snapshot_data):
        self.base_path = base_path
        self.user_id = user_data['user_id']
        self.snapshot_timestamp = snapshot_data['datetime']

    def generate_path(self, file_name):
        of_the_jedi = UtilFunctions.build_path_for_files_from_data(self.base_path, self.user_id,
                                                                   self.snapshot_timestamp, file_name)
        UtilFunctions.ensure_dir(os.path.dirname(of_the_jedi))
        return of_the_jedi

    def format_returned_data(self, field_name, data):
        return {'datetime': self.snapshot_timestamp, field_name: data}
