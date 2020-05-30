import sys
import click
from . import ParserHandler
from ..utils.CLITemplate import log, main


parser_handler = ParserHandler.ParserHandler()


@main.command()
@click.argument('parser_name', type=str)
@click.argument('raw_data_path', type=click.Path(exists=True))
def parse(parser_name, raw_data_path):
    log(parser_handler.parse(parser_name, raw_data_path))


@main.command('run-parser')
@click.argument('parser_name', type=str)
@click.argument('mq_url', type=str)
def run_parser(parser_name, mq_url):
    log(parser_handler.run_parser(parser_name, mq_url))


if __name__ == '__main__':
    try:
        main(prog_name='parsers', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
