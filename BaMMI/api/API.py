from flask import Blueprint, jsonify
from ..utils.APIServer import FlaskWrapper
from ..utils.Constants import mongodb_url
from ..utils.DBWrapper import DBWrapper


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
    available_fields = snapshot_data['snapshots'].keys()
    return jsonify(available_fields)
