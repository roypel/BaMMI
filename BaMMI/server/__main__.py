import sys
import click
from .Receiver import publish_to_message_queue
from .Server import run_server
from ..utils.CLITemplate import log, main
from ..utils.Constants import rabbit_mq_url


@main.command('run-server')
@click.argument('url', default=rabbit_mq_url, type=str)
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
def run(url, host='127.0.0.1', port=8000):
    log(run_server(host, port, lambda user_data, snapshot, binary_type_data, array_type_data:
        publish_to_message_queue(user_data, snapshot, binary_type_data, array_type_data, url)))


if __name__ == '__main__':
    try:
        main(prog_name='server', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
