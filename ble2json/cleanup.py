from threading import Thread
import time
from flask import current_app
from datetime import datetime, timedelta
from . import db


def init(app):
    try:
        with app.app_context():
            db_path = current_app.config["DB_PATH"]

            max_age_dict = current_app.config.get("MAX_AGE", None)
            delay_dict = current_app.config.get("CLEANUP_DELAY", {"hours": 1})

            max_age = get_timedelta(max_age_dict)
            delay = get_timedelta(delay_dict)

            if max_age:
                thread = Thread(target=cleanup, args=(db_path, max_age, delay))
                thread.start()

    except Exception as e:
        print(e)
        raise SystemExit


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
        raise SystemExit


def get_timedelta(d):
    if d:
        return timedelta(
            days=d.get("days", 0),
            seconds=d.get("seconds", 0),
            microseconds=d.get("microseconds", 0),
            milliseconds=d.get("milliseconds", 0),
            minutes=d.get("minutes", 0),
            hours=d.get("hours", 0),
            weeks=d.get("weeks", 0),
        )
    else:
        return None
