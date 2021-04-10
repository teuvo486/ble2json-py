import os
from flask import Flask
from . import cleanup, config, db, device, error, listener, router
from .tests import testdb


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(router.bp)
    load_ok = config.load(app)
    db.init(app)

    if not config.validate(load_ok, app):
        return app

    if not app.config.get("TEST_DB") == True:
        device.init(app)
    else:
        testdb.generate(app.config["DB_PATH"])

    if not app.config.get("NO_LISTEN") == True:
        listener.init(app)

    cleanup.init(app)
    return app
