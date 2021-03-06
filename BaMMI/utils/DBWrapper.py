from .drivers.db_drivers import db_drivers
from .UtilFunctions import find_driver


class DBWrapper:

    def __init__(self, url):
        self.db_driver = find_db_driver(url)

    def insert_single_data_unit(self, data):
        self.db_driver.insert_single_data_unit(data)

    def insert_many_data_units(self, data_list):
        self.db_driver.insert_many_data_units(data_list)

    def upsert_data_unit(self, key, data):
        self.db_driver.upsert_data_unit(key, data)

    def create_index_for_id(self, key_name, *args, **kwargs):
        self.db_driver.create_index_for_id(key_name, *args, **kwargs)

    def query_data(self, query=None, *args, **kwargs):
        return self.db_driver.query_data(query, *args, **kwargs)

    def insert_snapshot_data_by_user(self, user_id, snapshot_data, field_name):
        self.db_driver.insert_snapshot_data_by_user(user_id, snapshot_data, field_name)


def find_db_driver(url: str):
    return find_driver(db_drivers, url)
