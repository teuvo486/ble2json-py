import struct
from time import time
from ble2json import db
from .util import field, sign_and_magnitude

FMT = ">BBBBHhhhH"


def from_bytes(buf):
    t = struct.unpack(FMT, buf)
    return (
        field(t[1], 200, lambda v: v * 0.5),
        sign_and_magnitude(t[2], t[3]),
        field(t[4], 65534, lambda v: v + 50000),
        field(t[5], -32767, lambda v: v * 0.001),
        field(t[6], -32767, lambda v: v * 0.001),
        field(t[7], -32767, lambda v: v * 0.001),
        field(t[8], 3646, lambda v: v * 0.001),
    )


def insert(db_path, obj_path, rawdata):
    data = from_bytes(bytes(rawdata))

    conn = db.connect(db_path)

    dev_id = conn.execute(
        "SELECT id FROM device WHERE obj_path = ?", (obj_path,)
    ).fetchone()["id"]

    cols = (dev_id, int(time())) + data

    conn.execute(
        """INSERT INTO data (
                device_id,
                time,
                humidity,
                temperature,
                pressure,
                acceleration_x,
                acceleration_y,
                acceleration_z,
                voltage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        cols,
    )

    conn.commit()
    conn.close()


def get_latest(dev_id):
    conn = db.get_conn()

    return conn.execute(
        """SELECT
            strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
            humidity,
            temperature,
            pressure,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            voltage
            FROM data WHERE data.device_id = ?
            AND data.time = (
                SELECT MAX(data.time) 
                FROM data WHERE data.device_id = ?
            )""",
        (dev_id, dev_id),
    ).fetchone()


def get_interval(dev_id, start, end):
    conn = db.get_conn()

    return conn.execute(
        """SELECT
            strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
            humidity,
            temperature,
            pressure,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            voltage
            FROM data WHERE data.device_id = ?
            AND data.time >= strftime("%s", ?)
            AND data.time <= strftime("%s", ?)
            ORDER BY data.time""",
        (dev_id, start, end),
    ).fetchall()
