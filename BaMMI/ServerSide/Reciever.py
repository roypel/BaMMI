import json
from flask import Blueprint, jsonify, request, url_for
from BaMMI.BaMMI_pb2 import Snapshot, User
from google.protobuf.json_format import MessageToDict
from BaMMI.ServerSide import Utils


bp = Blueprint('recieve_data', __name__, url_prefix='/transfers')
message_type_data = ['pose', 'feelings', 'datetime']
binary_type_data = ['color_image', 'depth_image']
known_users = {}


@bp.route('/config', methods=['GET'])
def send_server_supported_fields():
    return jsonify([*message_type_data, *binary_type_data])


@bp.route('/users', methods=['POST'])
def receive_user_data():
    user_data = request.data
    user = User()
    user.ParseFromString(user_data)
    known_users[str(user.user_id)] = user
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
    with open('./snapshots', 'a') as f:
        print([known_users[user_id], data_to_publish], file=f)
    return jsonify(success=True)


def prepare_data_for_queue(user_id, data):
    # if data is dict:
    #     if [field for field in data if field not in [*message_type_data, *binary_type_data]]:
    #         raise ValueError("Got field that parsers can't handle")
    #     data['user_data'] = known_users[user_id]
    #     return json.dumps(data)
    # if data is Snapshot:
    data_to_publish = MessageToDict(data, preserving_proto_field_name=True)
    # TODO: In case data comes in other options, convert it to a valid json
