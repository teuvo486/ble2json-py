import struct
from time import time
from ble2json import db
from .util import clamp, field

FMT = ">BhHHhhhHBHBBBBBB"


def from_bytes(buf):
    t = struct.unpack(FMT, buf)
    return (
        field(t[1], -32767, lambda v: v * 0.005),
        field(t[2], 40000, lambda v: v * 0.0025),
        field(t[3], 65534, lambda v: v + 50000),
        field(t[4], -32767, lambda v: v * 0.001),
        field(t[5], -32767, lambda v: v * 0.001),
        field(t[6], -32767, lambda v: v * 0.001),
        field(t[7] >> 5, 2046, lambda v: v * 0.001 + 1.6),
        field(t[7] & 0x1F, 30, lambda v: v * 2 - 40),
        clamp(t[8], 254),
        clamp(t[9], 65534),
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
                temperature,
                humidity,
                pressure,
                acceleration_x,
                acceleration_y,
                acceleration_z,
                voltage,
                tx_power,
                movement_counter,
                measurement_sequence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        cols,
    )

    conn.commit()
    conn.close()


def get_latest(dev_id):
    conn = db.get_conn()

    return conn.execute(
        """SELECT
            strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
            temperature,
            humidity,
            pressure,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            voltage,
            tx_power,
            movement_counter,
            measurement_sequence
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
            temperature,
            humidity,
            pressure,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            voltage,
            tx_power,
            movement_counter,
            measurement_sequence
            FROM data WHERE data.device_id = ?
            AND data.time >= strftime("%s", ?)
            AND data.time <= strftime("%s", ?)
            ORDER BY data.time""",
        (dev_id, start, end),
    ).fetchall()
