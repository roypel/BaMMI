from pymongo import MongoClient, ASCENDING


class MongoDriver:

    def __init__(self, url, db_name="bammi_data", table_name="users_and_snapshots"):
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.table_name = self.db[table_name]

    def insert_single_data_unit(self, data):
        self.table_name.insert_one(data)

    def insert_many_data_units(self, data_list):
        self.table_name.insert_many(data_list)

    def upsert_data_unit(self, key, data):
        self.table_name.update_one(key, data, upsert=True)

    def create_index_for_id(self, key_name, *args, **kwargs):
        self.table_name.create_index([(key_name, ASCENDING)], *args, **kwargs)

    def query_data(self, query=None, *args, **kwargs):
        self.table_name.find(query, *args, **kwargs)

    def insert_snapshot_data_by_uid(self, user_id, snapshot_data, field_name):
        self.upsert_data_unit({'user_id': user_id},
                                  {
                                      f'snapshots.0.{field_name}': snapshot_data[field_name]
                                  }
                              )
        self.upsert_data_unit({'user_id': user_id,
                               'snapshots':
                                   {'$elemMatch':
                                    {'datetime':
                                     snapshot_data['datetime']
                                     }
                                    }
                               },
                              {'$addToSet':
                                  {
                                      f'snapshots.$.{field_name}': snapshot_data[field_name]
                                  }
                               }
                              )
