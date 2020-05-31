import sys
import click
from .API import run_api_server
from ..utils.CLITemplate import log, main
from ..utils.Constants import mongodb_url


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.option('-d', '--database', default=mongodb_url, type=str)
def run(host='127.0.0.1', port=5000, url=mongodb_url):
    log(run_api_server(host, port, url))


if __name__ == '__main__':
    try:
        main(prog_name='server', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
