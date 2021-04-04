import os
from flask import Flask
from . import cleanup, db, defaults, device, listener, router
from .tests import testdb


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_object(defaults)
    
    app.config.from_json("config.json", silent=True)

    if app.config.get("PERSISTENT"):
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/dev/shm/ble2json.db"

    app.register_blueprint(router.bp)
    
    db.init(app)
    
    if app.config.get("TESTING"):
        testdb.generate(app.config["DB_PATH"])
    else:
        device.init(app)

    if not app.config.get("NO_LISTEN"):
        listener.init(app)

    cleanup.init(app)

    return app
