import os
from flask import Flask
from . import cleanup, config, db, device, error, listener, router
from .tests import testdb


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_failed = config.load(app)

    if app.config.get("PERSISTENT") == True:
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/run/ble2json/ble2json.db"

    app.register_blueprint(router.bp)
    db.init(app)

    if config_failed:
        with app.app_context():
            error.log(500, "Config Error", "Invalid JSON syntax in config file.")

        return app

    if not app.config.get("TEST_DB") == True:
        device.init(app)
    else:
        testdb.generate(app.config["DB_PATH"])

    if not app.config.get("NO_LISTEN") == True:
        listener.init(app)

    cleanup.init(app)
    return app
