import os


def ensure_dir(dir_path):
    full_path = os.path.expanduser(dir_path)
    if not os.path.isdir(full_path):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)


def save_data_to_file(data, file_path, data_type=''):
    ensure_dir(file_path)
    with open(file_path, f'w{data_type}') as f:
        f.write(data)


def build_path_for_files_from_data(base_path, user_id, snapshot_data, filename):
    timestamp = str(snapshot_data.datetime)
    return os.path.join(base_path, user_id, timestamp, filename)
