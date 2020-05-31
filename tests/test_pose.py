import pytest
from BaMMI.parsers.ParserHandler import ParserHandler


# Not a real test, used only to check docker-compose finished loading RMQ which takes most of the time
def test_parsers_up():
    ph = ParserHandler()
    ph.run_parser('pose', 'rabbitmq://127.0.0.1:5672/')
