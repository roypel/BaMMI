import sys
import click
from .Receiver import publish_to_message_queue
from .Server import run_server
from ..utils.CLITemplate import log, main


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('url', default='rabbitmq://127.0.0.1:5672/', type=str)
def run(url, host='127.0.0.1', port=8000):
    log(run_server(host, port, lambda user_data, snapshot, binary_type_data, array_type_data:
        publish_to_message_queue(user_data, snapshot, binary_type_data, array_type_data, url)))


if __name__ == '__main__':
    try:
        main(prog_name='server', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
