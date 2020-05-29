import os
import sys
import traceback

import click

from .client import upload_sample as upload


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command()
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('path', default='snapshot.mind.gz', type=str)
def upload_sample(host='127.0.0.1', port=8000, path='snapshot.mind.gz'):
    log(upload(host, port, path))


if __name__ == '__main__':
    try:
        main(prog_name='client', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
