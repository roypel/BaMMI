import pika
import pytest


# Not a real test, used only to check docker-compose finished loading RMQ which takes most of the time
def test_mq_up():
    params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(params)
    connection.channel()
