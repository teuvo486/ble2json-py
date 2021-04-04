import time
from threading import Thread
from datetime import datetime
from flask import current_app
from . import db, defaults
from .timeutil import get_timedelta


def init(app):
    try:
        with app.app_context():
            db_path = current_app.config["DB_PATH"]

            max_age_dict = current_app.config.get("MAX_AGE", defaults.MAX_AGE)
            delay_dict = current_app.config.get("CLEANUP_INTERVAL", defaults.CLEANUP_INTERVAL)

            max_age = get_timedelta(max_age_dict)
            delay = get_timedelta(delay_dict)

            if max_age:
                thread = Thread(target=cleanup, args=(db_path, max_age, delay))
                thread.start()

    except Exception as e:
        print(e)


def cleanup(db_path, max_age, delay):
    try:
        while True:
            time.sleep(delay.total_seconds())
            oldest = (datetime.now() - max_age).timestamp()
            conn = db.connect(db_path)
            conn.execute("DELETE FROM data WHERE data.time < ?", (oldest,))
            conn.commit()
            conn.close()

    except Exception as e:
        print(e)
