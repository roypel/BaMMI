import sys
import click
from .Saver import Saver
from ..utils.Constants import mongodb_url
from ..utils.CLITemplate import log, main


@main.command()
@click.option('-d', '--database', default=mongodb_url, type=str)
@click.argument('topic-name', type=str)
@click.argument('raw-data-path', type=click.Path(exists=True))
def save(database, topic_name, raw_data_path):
    saver = Saver(database)
    log(saver.save(topic_name, raw_data_path))


@main.command('run-saver')
@click.argument('db_url', type=str)
@click.argument('mq_url', type=str)
def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    log(saver.consume_topics(mq_url))


if __name__ == '__main__':
    try:
        main(prog_name='saver', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
