import json
from flask import jsonify, request
from google.protobuf.json_format import MessageToDict
import numpy as np
from ..utils.BaMMI_pb2 import Snapshot, User
from ..utils import UtilFunctions
from ..utils.PubSuber import PubSuber


def publish_to_message_queue(user_data, snapshot, binary_type_data, array_type_data,
                             message_queue_url='rabbitmq://127.0.0.1:5672/'):
    data_to_publish = prepare_data_for_queue(user_data['user_id'], snapshot, binary_type_data, array_type_data)
    publisher = PubSuber(message_queue_url)
    publisher.init_exchange('snapshots_data', exchange_type='topic')
    publisher.publish_message(json.dumps({'user_data': user_data, 'snapshot_data': data_to_publish}),
                              '.'.join(data_to_publish.keys()))


def save_data_to_file(context, data, file_name, data_type=''):
    path = context.build_path_for_files_from_data(file_name)
    context.save_data_to_file(data, path, data_type)


def convert_binary_fields_to_files(user_id, data, binary_type_data, array_type_data):
    field_to_file_path = {}
    for field in data.ListFields():
        field_name = field[0].name
        if field_name in [*binary_type_data, *array_type_data]:
            field_data = field[1].data
            # TODO: Make base path something reasonable
            file_path = UtilFunctions.build_path_for_files_from_data(
                UtilFunctions.get_true_relative_path(__file__, '../storage'),
                user_id, str(data.datetime), '.'.join((field_name, 'raw')))
            if field_name in binary_type_data:
                UtilFunctions.save_data_to_file(field_data, file_path, 'b')
            else:
                array_data = np.array(field_data, dtype=float)
                array_data.astype('float').tofile(file_path)
            field_to_file_path[field_name] = file_path
    return field_to_file_path


def prepare_data_for_queue(user_id, data, binary_type_data, array_type_data):
    file_paths_data = convert_binary_fields_to_files(user_id, data, binary_type_data, array_type_data)
    data_to_publish = MessageToDict(data, preserving_proto_field_name=True)
    for field in file_paths_data:
        data_to_publish[field]['data'] = file_paths_data[field]
    return data_to_publish
    # TODO: In case data comes in other options, convert it to a valid json


class Receiver:

    def __init__(self, publish_function):
        self.publish_function = publish_function
        self.message_type_data = ['pose', 'feelings', 'datetime']
        self.binary_type_data = ['color_image']
        self.array_type_data = ['depth_image']
        self.known_users = {}

    def send_server_supported_fields(self):
        return jsonify([*self.message_type_data, *self.binary_type_data, *self.array_type_data])

    def receive_user_data(self):
        user_data = request.data
        user = User()
        user.ParseFromString(user_data)
        user_dict = MessageToDict(user, preserving_proto_field_name=True)
        for field in user.DESCRIPTOR.fields:
            if field.name not in user_dict:
                # Handling case where zero-value enums are omitted - https://github.com/golang/protobuf/issues/258
                user_dict[field.name] = 0
        self.known_users[str(user.user_id)] = user_dict
        return jsonify(success=True)

    def receive_snapshot_data(self):
        user_id = request.headers.get('user-id')
        snapshot_data = request.data
        snapshot = Snapshot()
        snapshot.ParseFromString(snapshot_data)
        self.publish_function(self.known_users[user_id], snapshot, self.binary_type_data, self.array_type_data)
        return jsonify(success=True)
