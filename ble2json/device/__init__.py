from datetime import date, time, datetime, timedelta
from flask import current_app
from ble2json import db
from . import ruuvi3, ruuvi5


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
                       ON CONFLICT DO NOTHING""",
                    (name, address, obj_path, fmt),
                )

        conn.commit()


def insert_rssi(db_path, obj_path, rssi):
    conn = db.connect(db_path)
    conn.execute("UPDATE device SET rssi = ? WHERE objPath = ?", (rssi, obj_path))
    conn.commit()
    conn.close()


def insert_data(db_path, obj_path, mfdata):
    if 0x0499 in mfdata:
        rawdata = mfdata[0x499]

        if len(rawdata) == 14 and rawdata[0] == 3:
            ruuvi3.insert(db_path, obj_path, rawdata)
        if len(rawdata) == 24 and rawdata[0] == 5:
            ruuvi5.insert(db_path, obj_path, rawdata)
        else:
            raise Exception("Unrecognized data format!")

    else:
        raise Exception("Unrecognized manufacturer id!")


def get_all(start, end):
    conn = db.get_conn()

    devs = conn.execute("SELECT id, name, address, format, rssi FROM device").fetchall()

    for dev in devs:
        dev["sensorData"] = get_sensor_data(dev, start, end)

    return devs


def get_one(name, start, end):
    conn = db.get_conn()

    dev = conn.execute(
        "SELECT id, name, address, format, rssi FROM device WHERE name = ?", (name,)
    ).fetchone()

    if dev:
        dev["sensorData"] = get_sensor_data(dev, start, end)

    return dev


def get_sensor_data(dev, start, end):
    dev_id = dev.pop("id", None)
    fmt = dev.pop("format", None)
    mod = get_mod(fmt)

    if not start and not end:
        return mod.get_latest(dev_id)
    
    start, end = get_datetimes(start, end)

    return mod.get_interval(dev_id, start, end)


def get_mod(fmt):
    if fmt == "ruuvi3":
        return ruuvi3
    elif fmt == "ruuvi5":
        return ruuvi5
    else:
        raise Exception("Invalid data format!")
        

def get_datetimes(start, end):
    aliases = ["epoch", "now", "day", "week", "month", "year"]

    if not start:
        start = resolve_alias("epoch")
    elif start in aliases:
        start = resolve_alias(start)
        
    if not end:
        end = resolve_alias("now")
    elif end in aliases:
        end = resolve_alias(end)
        
    return start, end


def resolve_alias(a):
    if a == "epoch":
        return "1970-01-01T00:00:00Z"
        
    if a == "now":
        return datetime.now().isoformat(timespec="seconds")
    
    if a == "day":
        d = date.today()
    elif a == "week":
        d = date.today() - timedelta(days=date.today().weekday() % 7)
    elif a == "month":
        d = date.today().replace(day=1)
    else:
        d = date.today().replace(day=1, month=1)
    
    return datetime.combine(d, time()).isoformat(timespec="seconds")
    


