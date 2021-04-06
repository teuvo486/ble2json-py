from flask import current_app
from ble2json import db


def init(app):
    with app.app_context():
        conn = db.get_conn()

        for dev in current_app.config.get("DEVICES", []):
            name = dev.get("name", None)
            address = dev.get("address", None)
            fmt = dev.get("format", None)

            if name and address and fmt:
                obj_path = "/org/bluez/hci0/dev_" + address.replace(":", "_")

                conn.execute(
                    """INSERT INTO device (name, address, objPath, format)
                       VALUES (?, ?, ?, ?)
                       ON CONFLICT (address)
                       DO UPDATE SET name = excluded.name, format = excluded.format""",
                    (name, address, obj_path, fmt),
                )

        conn.commit()


def update_rssi(db_path, obj_path, rssi):
    conn = db.connect(db_path)
    conn.execute("UPDATE device SET rssi = ? WHERE objPath = ?", (rssi, obj_path))
    conn.commit()
    conn.close()


def get_all(start, end, cols):
    conn = db.get_conn()

    devs = conn.execute("SELECT id, name, address, format, rssi FROM device").fetchall()

    for dev in devs:
        dev_id = dev.pop("id")
        fmt = dev.pop("format")
        dev["sensorData"] = sensordata.get(dev_id, fmt, start, end, cols)

    return devs


def get_one(name, start, end, cols):
    conn = db.get_conn()

    dev = conn.execute(
        "SELECT id, name, address, format, rssi FROM device WHERE name = ?", (name,)
    ).fetchone()

    if dev:
        dev_id = dev.pop("id")
        fmt = dev.pop("format")
        dev["sensorData"] = sensordata.get(dev_id, fmt, start, end, cols)

    return dev
