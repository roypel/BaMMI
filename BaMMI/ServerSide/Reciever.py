from flask import Blueprint, jsonify, request, url_for
from BaMMI.BaMMI_pb2 import Snapshot, User


bp = Blueprint('recieve_data', __name__, url_prefix='/transfers')
available_parsers_list = ['pose', 'color_image', 'feelings']
user_list = []


@bp.route('/config', methods=['GET'])
def send_server_supported_fields():
    return jsonify(available_parsers_list)


@bp.route('/users', methods=['POST'])
def receive_user_data():
    user_data = request.data
    user = User()
    user.ParseFromString(user_data)
    user_list.append(user)
    with open('./log.txt', 'w') as f:
        print(user_list, file=f)
    return jsonify(success=True)


@bp.route('/snapshots', methods=['POST'])
def receive_snapshot_data():
    user_id = request.headers.get('user-id')
    snapshot_data = request.data
    snapshot = Snapshot()
    snapshot.ParseFromString(snapshot_data)
    with open('./snapshots', 'a') as f:
        print([user_id, snapshot], file=f)
