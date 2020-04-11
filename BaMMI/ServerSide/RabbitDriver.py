import pika


available_exchanges = ['direct', 'topic', 'fanout', 'headers']


class RabbitDriver:

    def __init__(self, host='127.0.0.1', port=5672):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.exchange_name = ''
        self.queue_name = ''

    def init_exchange(self, exchange_name, exchange_type):
        if exchange_type not in available_exchanges:
            raise ValueError(f"Unknown exchange type for RabbitMQ. Choose one of {available_exchanges}")
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        self.exchange_name = exchange_name

    def init_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def publish_message(self, message, routing_key):
        self.channel.basic_publish(
            exchange=self.exchange_name, routing_key=routing_key, body=message)

    def close(self):
        self.connection.close()
