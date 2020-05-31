import json
import os
from urllib.parse import urlparse


def ensure_dir(dir_path):
    full_path = os.path.expanduser(dir_path)
    if not os.path.isdir(full_path):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)


def save_data_to_file(data, file_path, data_type=''):
    ensure_dir(file_path)
    with open(file_path, f'w{data_type}') as f:
        f.write(data)
    import sys
    print(f'Wrote data to {file_path}', file=sys.stderr)


def get_true_relative_path(file_path, relative_path):
    return os.path.join(os.path.dirname(os.path.realpath(file_path)), relative_path)


def build_path_for_files_from_data(base_path, user_id, snapshot_timestamp, filename):
    return os.path.join(base_path, user_id, snapshot_timestamp, filename)


def find_driver(drivers, url):
    url_scheme = urlparse(url).scheme
    for scheme, cls in drivers.items():
        if url_scheme.lower() == scheme.lower():
            return cls(url)
    raise ValueError("Unknown type of URL was given")


def extract_json_from_raw_data(raw_data):
    json_data = json.loads(raw_data)
    user_data = json_data['user_data']
    snapshot_data = json_data['snapshot_data']
    return user_data, snapshot_data
