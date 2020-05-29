import sys
import click
from . import ParserHandler
from ..utils.CLITemplate import log, main


@main.group()
@click.pass_context
def parser(context):
    context.obj['parser_handler'] = ParserHandler.ParserHandler()


@parser.group()
@click.pass_obj
@click.option('parser_name', type=str)
@click.argument('raw_data_path', type=click.Path(exists=True))
def parse(obj, parser_name, raw_data_path):
    log(obj['parser_handler'].parse(parser_name, raw_data_path))


@parser.group()
@parser.command('run-parser')
@click.pass_obj
@click.option('parser_name', type=str)
@click.argument('mq_url', type=str)
def run_parser(obj, parser_name, mq_url):
    log(obj['parser_handler'].run_parser(parser_name, mq_url))


if __name__ == '__main__':
    try:
        main(prog_name='parsers', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
