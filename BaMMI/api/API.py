from flask import Blueprint, jsonify, send_from_directory
from ..utils.APIServer import FlaskWrapper
from ..utils.Constants import storage_folder, mongodb_url
from ..utils.DBWrapper import DBWrapper
from ..utils.UtilFunctions import build_path_for_files_from_data


bp = Blueprint('serve_data', __name__, url_prefix='/users')
db = DBWrapper('')


def run_api_server(host='127.0.0.1', port=5000, database_url=mongodb_url):
    global db
    db = DBWrapper(database_url)
    app = FlaskWrapper('server')
    app.register_blueprint(bp)
    app.run(host=host, port=port)


@bp.route('', methods=['GET'])
def get_all_users():
    return jsonify(db.query_data({}, {'_id': 0, 'user_id': 1, 'username': 1}))


@bp.route('/<user_id>', methods=['GET'])
def get_user_data(user_id):
    return jsonify(db.query_data({'user_id': user_id},
                                 {'_id': 0, 'user_id': 1, 'username': 1, 'birthday': 1, 'gender': 1}))


@bp.route('/<user_id>/snapshots', methods=['GET'])
def get_user_snapshots(user_id):
    return jsonify(db.query_data({'user_id': user_id}, {'_id': 0, 'user_id': 0, 'snapshots.datetime': 1}))


@bp.route('/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
def get_snapshot_details(user_id, snapshot_id):
    snapshot_data = db.query_data({'user_id': user_id, 'snapshots.datetime': snapshot_id},
                                  {'_id': 0, 'user_id': 0, 'birthday': 0, 'gender': 0, 'username': 0,
                                   'snapshots.datetime': 0})
    available_fields = list(snapshot_data['snapshots'].keys())
    return jsonify(available_fields)


@bp.route('/<user_id>/snapshots/<snapshot_id>/<result_name>', methods=['GET'])
def get_parsed_result(user_id, snapshot_id, result_name):
    result_name = result_name.replace("-", "_")
    snapshot_data = db.query_data({'user_id': user_id, 'snapshots.datetime': snapshot_id},
                                  {'_id': 0, f'snapshots.{result_name}': 1})
    result = snapshot_data['snapshots'][0][result_name]
    if isinstance(result, str):  # TODO: Come on... You can do better than that...
        possible_file_path = result.split(storage_folder)[1]
        if possible_file_path:  # We found that we're about to return path to the file from our storage folder
            return jsonify(f'GET /users/{user_id}/snapshots/{snapshot_id}/{result_name}/data')
    return jsonify(result)


@bp.route('/<user_id>/snapshots/<snapshot_id>/<result_name>/data', methods=['GET'])
def get_file(user_id, snapshot_id, result_name):
    result_name = result_name.replace("-", "_")
    return send_from_directory(storage_folder, build_path_for_files_from_data('.', user_id, snapshot_id,
                                                                              f'{result_name}.jpg'))
