from .drivers.mq_drivers import mq_drivers
from ..utils.UtilFunctions import find_driver

"""
At first, I thought about separating the modules to Publisher and Subscriber,
however, since we'll use the same message queue for both anyway (even if it's not RMQ),
and there are some actions they do the same, I decided to mash it all in one module.
"""


class PubSuber:

    def __init__(self, url):
        self.pub_sub_driver = find_pub_sub_driver(url)

    def publish_message(self, message, *args, **kwargs):
        self.pub_sub_driver.publish_message(message, *args, **kwargs)

    def consume_messages(self, callback, *args, **kwargs):
        self.pub_sub_driver.consume_messages(callback, *args, **kwargs)

    def init_queue(self, queue_name='', *args, **kwargs):
        self.pub_sub_driver.init_queue(queue_name, *args, **kwargs)

    def bind_queue(self, *args, **kwargs):
        self.pub_sub_driver.bind_queue(*args, **kwargs)

    def init_exchange(self, exchange_name, *args, **kwargs):
        self.pub_sub_driver.init_exchange(exchange_name, *args, **kwargs)

    def close(self):
        self.pub_sub_driver.close()


def find_pub_sub_driver(url: str):
    return find_driver(mq_drivers, url)
