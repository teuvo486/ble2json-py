import os
from flask import Flask
from . import cleanup, db, device, listener, router


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_json("config.json")

    if app.config.get("PERSISTENT", False):
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/dev/shm/ble2json.db"

    app.register_blueprint(router.bp)

    db.init(app)

    device.init(app)

    if not app.config.get("NO_LISTEN", False):
        listener.init(app)

    cleanup.init(app)

    return app
