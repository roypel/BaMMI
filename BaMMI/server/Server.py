import BaMMI.server.APIServer as APIServer
import BaMMI.server.Receiver as Reciever


def run_server(host='127.0.0.1', port=8000, publish=Reciever.publish_to_message_queue):
    url_prefix = '/uploads'
    app = APIServer.FlaskWrapper('server')
    receiver = Reciever.Receiver(publish)
    app.add_endpoint(f'{url_prefix}/config', 'config', receiver.send_server_supported_fields, methods=['GET'])
    app.add_endpoint(f'{url_prefix}/users', 'user_upload', receiver.receive_user_data, methods=['POST'])
    app.add_endpoint(f'{url_prefix}/snapshots', 'snapshots_upload', receiver.receive_snapshot_data,
                     methods=['POST'])

    app.run(host=host, port=port)
