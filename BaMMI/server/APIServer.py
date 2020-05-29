from flask import Flask


class EndpointAction:
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)


class FlaskWrapper:
    app = None

    def __init__(self, name=__name__):
        self.app = Flask(name)

    def run(self, host='127.0.0.1', port=8000):
        self.app.run(host=host, port=port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
