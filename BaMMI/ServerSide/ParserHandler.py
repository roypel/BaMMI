import importlib
import inspect
import json
import pathlib
import sys
from BaMMI.ServerSide.PubSuber import PubSuber


class ParserHandler:

    def __init__(self, parsers_folder='./Parsers'):
        self.parsers = {}
        self._load_parsers(parsers_folder)

    def _load_parsers(self, root_folder):
        root = pathlib.Path(root_folder).absolute()
        sys.path.insert(0, str(root.parent))
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            module = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
            self._load_parse_function(module)

    def _load_parse_function(self, module):
        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            if not func_name.startswith('parse'):
                continue
            if isinstance(func.field, list):
                for field in func.field:
                    self._add_parser_to_list(field, func)
            else:
                self._add_parser_to_list(func.field, func)

    def _add_parser_to_list(self, field, func):
        if field in self.parsers:
            self.parsers[field].append(func)
        else:
            self.parsers[field] = [func]

    def parse(self, field_name, raw_data):
        json_data = json.loads(raw_data)
        user_data = json_data['user_data']
        snapshot_data = json_data['snapshot_data']
        if field_name not in self.parsers:
            raise ModuleNotFoundError(f"Parser for {field_name} is not found")
        if len(self.parsers[field_name]) > 1:
            # In case there's a few parsers for a certain field
            parser_results = []
            for func in self.parsers[field_name]:
                parser_results.append(func(snapshot_data))
        else:
            parser_results = self.parsers[field_name][0](snapshot_data)
        return {'user_data': user_data, field_name: parser_results}

    def run_parser(self, field_name, mq_url):
        subscriber = PubSuber(mq_url)
        subscriber.init_exchange('snapshots_data', exchange_type='topic')
        subscriber.bind_queue(binding_keys=f'#.{field_name}.#')
        publisher = PubSuber(mq_url)
        publisher.init_exchange('parsers_results', exchange_type='topic')
        subscriber.consume_messages(
            lambda ch, method, properties, body: self._forward_parsing(field_name, body, publisher)
        )

    def _forward_parsing(self, field_name, data, publisher):
        parser_results = self.parse(field_name, data)
        publisher.publish_message(parser_results, field_name)


parser = ParserHandler()
parser.run_parser('pose', 'rabbitmq://127.0.0.1:5672/')
