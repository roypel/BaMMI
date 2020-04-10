from flask import Blueprint, jsonify, request, url_for
from BaMMI.BaMMI_pb2 import Snapshot, User
from BaMMI.ServerSide import Utils


bp = Blueprint('recieve_data', __name__, url_prefix='/transfers')
available_parsers_list = ['pose', 'color_image', 'feelings', 'depth_image', 'datetime']
known_users = {}


@bp.route('/config', methods=['GET'])
def send_server_supported_fields():
    return jsonify(available_parsers_list)


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
    color_image_path = Utils.build_path_for_files_from_data('.', user_id, snapshot, 'color_image.bin')
    Utils.save_data_to_file(snapshot.color_image.data,
                            color_image_path,
                            'b')
    snapshot.color_image = color_image_path
    with open('./snapshots', 'a') as f:
        print([known_users[user_id], snapshot], file=f)
    return jsonify(success=True)
