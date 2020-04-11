from urllib.parse import urlparse
import BaMMI.ServerSide.RabbitDriver as RabbitDriver


class Publisher:

    def __init__(self, url):
        self.publisher_driver = find_publisher_driver(url)

    def publish_message(self, message, *args, **kwargs):
        self.publisher_driver.publish_message(message, *args, **kwargs)

    def init_queue(self, queue_name):
        self.publisher_driver.init_queue(queue_name)

    def init_exchange(self, exchange_name, *args, **kwargs):
        self.publisher_driver.init_exchange(exchange_name, *args, **kwargs)

    def close(self):
        self.publisher_driver.close()


def find_publisher_driver(url: str):
    drivers = {'rabbitmq': RabbitDriver.RabbitDriver}
    url_scheme = urlparse(url).scheme
    for scheme, cls in drivers.items():
        if url_scheme.lower() == scheme.lower():
            return cls(url)
