from pymongo import MongoClient, ASCENDING, UpdateOne


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
        return self.table_name.find(query, *args, **kwargs)

    def insert_snapshot_data_by_user(self, user_data, snapshot_data, field_name):
        # Idea for array upsert taken from https://stackoverflow.com/questions/22664972/mongodb-upsert-on-array
        user_id = user_data['user_id']
        operations = [
            # If the document doesn't exist at all, insert it
            UpdateOne({'user_id': user_id},
                      {
                          '$setOnInsert': {
                              **{k: v for k, v in user_data.items()},
                              'snapshots': [{'datetime': snapshot_data['datetime']}]
                          }
                      },
                      upsert=True
                      ),
            # If the document exists, update it
            UpdateOne({'user_id': user_id,
                       'snapshots': {
                           '$elemMatch': {
                               'datetime': snapshot_data['datetime']
                           }
                       }
                       },
                      {
                          '$set':
                              {
                                  f'snapshots.$.{field_name}': snapshot_data[field_name]
                              }
                      }
                      ),
            # If an array element doesn't exist, add it. Won't conflict with the update a step before
            UpdateOne({'user_id': user_id, 'snapshots.datetime': snapshot_data['datetime']},
                      {
                          '$addToSet': {
                              'snapshots': {
                                  field_name: snapshot_data[field_name]
                              }
                          }
                      })
        ]
        self.table_name.bulk_write(operations)
