import sys
import click
from .client import upload_sample as upload
from ..utils.CLITemplate import log, main


@main.command()
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('path', default='snapshot.mind.gz', type=click.Path(exists=True))
def upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz'):
    log(upload(host, port, path))


if __name__ == '__main__':
    try:
        main(prog_name='client', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
