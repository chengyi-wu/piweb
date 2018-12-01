from flask import Flask, render_template
from . import dashboard, api

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    app.register_blueprint(dashboard.bp)
    app.register_blueprint(api.bp)

    return app