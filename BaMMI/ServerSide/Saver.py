from BaMMI.ServerSide.DBWrapper import DBWrapper
from BaMMI.ServerSide.PubSuber import PubSuber
from BaMMI.ServerSide.Utils import extract_json_from_raw_data


class Saver:

    def __init__(self, url):
        self.db_con = DBWrapper(url)
        self.pubsuber = PubSuber('rabbitmq://127.0.0.1:5672/')
        self.known_fields = ['pose', 'feelings', 'color_image', 'depth_image']

    def save(self, topic_name, data):
        if topic_name in self.known_fields:
            user_data, snapshot_data = extract_json_from_raw_data(data)
            update_key = {'user_id': user_data['user_id'], 'datetime': snapshot_data['datetime']}

            self.db_con.upsert_data_unit(update_key, data)
        else:
            raise ValueError(f"Unknown field {topic_name}")

    def consume_topics(self):
        self.pubsuber.init_exchange('parsers_results', exchange_type='topic')
        self.pubsuber.bind_queue(binding_keys='#')
        self.pubsuber.consume_messages(lambda ch, method, properties, body: self.save(method.routing_key, body))


saver = Saver("mongodb://127.0.0.1:27017/")
saver.consume_topics()
