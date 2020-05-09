import json
from flask import Blueprint, jsonify, request
import numpy as np
from BaMMI.BaMMI_pb2 import Snapshot, User
from google.protobuf.json_format import MessageToDict
from BaMMI.ServerSide import Utils
from BaMMI.ServerSide.PubSuber import PubSuber


bp = Blueprint('recieve_data', __name__, url_prefix='/transfers')
message_type_data = ['pose', 'feelings', 'datetime']
binary_type_data = ['color_image']
array_type_data = ['depth_image']
known_users = {}


@bp.route('/config', methods=['GET'])
def send_server_supported_fields():
    return jsonify([*message_type_data, *binary_type_data, *array_type_data])


@bp.route('/users', methods=['POST'])
def receive_user_data():
    user_data = request.data
    user = User()
    user.ParseFromString(user_data)
    known_users[str(user.user_id)] = MessageToDict(user, preserving_proto_field_name=True)
    with open('./log.txt', 'w') as f:
        print(known_users, file=f)
    return jsonify(success=True)


@bp.route('/snapshots', methods=['POST'])
def receive_snapshot_data():
    user_id = request.headers.get('user-id')
    snapshot_data = request.data
    snapshot = Snapshot()
    snapshot.ParseFromString(snapshot_data)
    data_to_publish = prepare_data_for_queue(user_id, snapshot)
    publisher = PubSuber('rabbitmq://127.0.0.1:5672/')
    publisher.init_exchange('snapshots_data', exchange_type='topic')
    publisher.publish_message(json.dumps({'user_data': known_users[user_id], 'snapshot_data': data_to_publish}),
                              '.'.join(data_to_publish.keys()))
    return jsonify(success=True)


def save_data_to_file(context, data, file_name, data_type=''):
    path = context.build_path_for_files_from_data(file_name)
    context.save_data_to_file(data, path, data_type)


def convert_binary_fields_to_files(user_id, data):
    field_to_file_path = {}
    for field in data.ListFields():
        field_name = field[0].name
        if field_name in [*binary_type_data, *array_type_data]:
            field_data = field[1].data
            file_path = Utils.build_path_for_files_from_data('./', user_id, data, '.'.join((field_name, 'raw')))
            if field_name in binary_type_data:
                Utils.save_data_to_file(field_data, file_path, 'b')
            else:
                array_data = np.array(field_data, dtype=float)
                array_data.astype('float').tofile(file_path)
            field_to_file_path[field_name] = file_path
    return field_to_file_path


def prepare_data_for_queue(user_id, data):
    file_paths_data = convert_binary_fields_to_files(user_id, data)
    data_to_publish = MessageToDict(data, preserving_proto_field_name=True)
    for field in file_paths_data:
        data_to_publish[field]['data'] = file_paths_data[field]
    return data_to_publish
    # TODO: In case data comes in other options, convert it to a valid json
