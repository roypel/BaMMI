from flask import Flask, Response


class EndpointAction:
    def __init__(self, action, status=200, headers=None):
        if headers is None:
            headers = {}
        self.action = action
        self.response = Response(status=status, headers=headers)

    def __call__(self, *args, **kwargs):
        self.action(*args, **kwargs)
        return self.response


class FlaskWrapper:
    app = None

    def __init__(self, name=__name__):
        self.app = Flask(name)

    def run(self, host='127.0.0.1', port=8000):
        self.run(host=host, port=port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def register_blueprint(self, blueprint):
        self.app.register_blueprint(blueprint)
