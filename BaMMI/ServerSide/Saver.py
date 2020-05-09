from BaMMI.ServerSide.PubSuber import PubSuber
from BaMMI.ServerSide.DBWrapper import DBWrapper


class Saver:

    def __init__(self, url):
        self.db_con = DBWrapper(url)
        self.pubsuber = PubSuber('rabbitmq://127.0.0.1:5672/')
        self.known_fields = ['pose', 'feelings', 'color_image', 'depth_image']

    def save(self, topic_name, data):
        if topic_name in self.known_fields:
            self.db_con.upsert_data_unit(topic_name, data)
        else:
            raise ValueError(f"Unknown field {topic_name}")

    def consume_topics(self):
        self.pubsuber.init_exchange('parsers_results', exchange_type='topic')
        self.pubsuber.bind_queue(binding_keys='#')
        self.pubsuber.consume_messages(lambda ch, method, properties, body: self.save(method.routing_key, body))
