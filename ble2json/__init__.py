import os
from flask import Flask
from . import db, device, listener, router


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_mapping(PERSISTENT=False)

    app.config.from_json("config.json", silent=True)

    if app.config["PERSISTENT"]:
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/dev/shm/ble2json.db"

    app.register_blueprint(router.bp)

    db.init(app)

    device.init(app)

    thread = listener.init(app)

    return app
