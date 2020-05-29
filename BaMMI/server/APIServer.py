from flask import Flask, Response


class EndpointAction:
    def __init__(self, action):  # , status=200, headers=None):
        # if headers is None:
        #     headers = {}
        self.action = action
        # self.response = Response(status=status, headers=headers)

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)
        # return Response(result, status=200, headers={})


class FlaskWrapper:
    app = None

    def __init__(self, name=__name__):
        self.app = Flask(name)

    def run(self, host='127.0.0.1', port=8000):
        self.app.run(host=host, port=port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
