from urllib.parse import urlparse
import pika


available_exchanges = ['direct', 'topic', 'fanout', 'headers']


class RabbitDriver:

    def __init__(self, url):
        parsed_url = urlparse(url)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=parsed_url.hostname, port=parsed_url.port))
        self.channel = self.connection.channel()
        self.exchange_name = ''
        self.queue_name = ''

    def init_exchange(self, exchange_name, exchange_type):
        if exchange_type not in available_exchanges:
            raise ValueError(f"Unknown exchange type for RabbitMQ. Choose one of {available_exchanges}")
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.exchange_name = exchange_name

    def init_queue(self, queue_name, *args, **kwargs):
        result = self.channel.queue_declare(queue=queue_name, *args, **kwargs)
        if not queue_name:
            self.queue_name = result.method.queue

    def publish_message(self, message, routing_key='', *args, **kwargs):
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key=routing_key, body=message, *args, **kwargs)

    def consume_messages(self, callback, *args, **kwargs):
        if not self.queue_name:
            self.init_queue('')
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, *args, **kwargs)
        self.channel.start_consuming()

    def bind_queue(self, binding_keys=None):
        if not self.queue_name:
            self.init_queue('')
        if isinstance(binding_keys, list):
            for binding_key in binding_keys:
                self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=binding_key)
        elif isinstance(binding_keys, str):
            self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=binding_keys)
        else:
            raise TypeError("Binding keys format isn't recognized, pass a string or a list of strings")

    def close(self):
        self.connection.close()
