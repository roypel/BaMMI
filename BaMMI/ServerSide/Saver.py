from BaMMI.ServerSide.PubSuber import PubSuber
from BaMMI.ServerSide.DBWrapper import DBWrapper


class Saver:

    def __init__(self, url):
        self.db_con = DBWrapper(url)

    def save(self, topic_name, data):
        self.db_con.upsert_data_unit()
