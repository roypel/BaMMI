import click
import BaMMI.ServerSide.APIServer as APIServer
from BaMMI.ServerSide.Reciever import bp, publish_to_message_queue


def run_server(host='127.0.0.1', port=8000, publish=publish_to_message_queue):
    app = APIServer.FlaskWrapper('server')
    app.register_blueprint(bp)
    app.add_endpoint(endpoint='')
    app.run(host=host, port=port)
