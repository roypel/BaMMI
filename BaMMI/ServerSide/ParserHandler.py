import importlib
import inspect
import pathlib
import sys


class ParserHandler:

    def __init__(self, parsers_folder='./Parsers'):
        self.parsers = {}
        self.load_parsers(parsers_folder)

    def load_parsers(self, root_folder):
        root = pathlib.Path(root_folder).absolute()
        sys.path.insert(0, str(root.parent))
        for path in root.iterdir():
            if path.name.startswith('_') or not path.suffix == '.py':
                continue
            module = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
            self.load_parse_function(module)

    def load_parse_function(self, module):
        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            if not func_name.startswith('parse'):
                continue
            for field in func.field:
                if field in self.parsers:
                    self.parsers[field].append(func)
                else:
                    self.parsers[field] = [func]

    def run_parser(self, field_name, data):
        user_data = data['user_data']
        snapshot_data = data['snapshot_data']
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
