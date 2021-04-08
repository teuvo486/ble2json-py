import os
from flask import Flask
from . import cleanup, db, defaults, device, listener, router
from .tests import testdb


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(defaults)
    app.config.from_json("config.json", silent=True)

    if app.config.get("PERSISTENT"):
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/run/ble2json/ble2json.db"

    app.register_blueprint(router.bp)
    db.init(app)

    if not app.config.get("TESTING"):
        device.init(app)
    else:
        testdb.generate(app.config["DB_PATH"])

    if not app.config.get("NO_LISTEN"):
        listener.init(app)

    cleanup.init(app)
    return app
