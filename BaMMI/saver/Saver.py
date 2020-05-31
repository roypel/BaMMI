from ..utils.DBWrapper import DBWrapper
from ..utils.PubSuber import PubSuber
from ..utils.UtilFunctions import extract_json_from_raw_data


class Saver:

    def __init__(self, db_url):
        self.db_con = DBWrapper(db_url)
        self.known_fields = ['pose', 'feelings', 'color_image', 'depth_image']

    def save(self, topic_name, data):
        if topic_name in self.known_fields:
            user_data, snapshot_data = extract_json_from_raw_data(data)
            self.db_con.insert_snapshot_data_by_user(user_data, snapshot_data, topic_name)
        else:
            raise ValueError(f"Unknown field {topic_name}")

    def consume_topics(self, mq_url):
        pubsuber = PubSuber(mq_url)
        pubsuber.init_exchange('parsers_results', exchange_type='topic')
        pubsuber.bind_queue(binding_keys='#')
        pubsuber.consume_messages(lambda ch, method, properties, body: self.save(method.routing_key, body))
