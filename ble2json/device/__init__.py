import re
from flask import current_app
from ble2json import db, defaults, error


def init(app):
    with app.app_context():
        conn = db.get_conn()

        for dev in current_app.config.get("ADD_DEVICES", defaults.ADD_DEVICES):
            name = dev.get("name")
            addr = validate_mac(dev.get("address"))
            fmt = dev.get("format")

            if name and addr and fmt:
                obj_path = "/org/bluez/hci0/dev_" + addr.replace(":", "_")

                conn.execute(
                    """INSERT INTO device (name, address, objPath, format)
                       VALUES (?, ?, ?, ?)
                       ON CONFLICT (address)
                       DO UPDATE SET name = excluded.name, format = excluded.format""",
                    (name, addr, obj_path, fmt),
                )
            else:
                error.log(500, "Config Error", f"Device {name} is missing required properties.")
                

        conn.commit()

        for addr in current_app.config.get("DELETE_DEVICES", defaults.DELETE_DEVICES):
            address = validate_mac(addr)
            conn.execute("DELETE FROM device WHERE address = ?", (address,))

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


def validate_mac(addr):
    if addr and re.match("^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", addr):
        return addr.upper()
        
    error.log(500, "Config Error", f"Invalid MAC address {addr}.")
