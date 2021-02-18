from datetime import datetime
from flask import current_app
from . import db, ruuvi5


def init(app):
    with app.app_context():
        conn = db.get_conn()

        for name, address in current_app.config["DEVICES"].items():
            if (
                conn.execute("SELECT id FROM device WHERE name = ?", (name,)).fetchone()
                is None
            ):
                obj_path = "/org/bluez/hci0/dev_" + address.replace(":", "_")
                conn.execute(
                    "INSERT INTO device (name, address, obj_path) VALUES (?, ?, ?)",
                    (name, address, obj_path),
                )

        conn.commit()


def get_all(start, end):
    conn = db.get_conn()

    devs = conn.execute("SELECT id, name, address, rssi FROM device").fetchall()

    for dev in devs:
        dev_id = dev.pop("id", None)
        dev["sensorData"] = get_sensor_data(dev_id, start, end)

    return devs


def get_one(name, start, end):
    conn = db.get_conn()

    dev = conn.execute(
        "SELECT id, name, address, rssi FROM device WHERE name = ?", (name,)
    ).fetchone()

    if dev:
        dev_id = dev.pop("id", None)
        dev["sensorData"] = get_sensor_data(dev_id, start, end)

    return dev


def get_sensor_data(dev_id, start, end):
    if not start and not end:
        return ruuvi5.get_latest(dev_id)
    elif not start and end:
        start = "1970-01-01T00:00:00Z"
    elif start and not end:
        end = datetime.now().isoformat(timespec="seconds")

    return ruuvi5.get_interval(dev_id, start, end)
