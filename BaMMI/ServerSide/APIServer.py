from flask import Flask


def create_api_by_blueprint(blueprint):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(blueprint)
    return app
