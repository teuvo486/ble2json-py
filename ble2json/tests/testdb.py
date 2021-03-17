import struct
import sqlite3
from os.path import relpath
from datetime import datetime, timedelta
from ble2json import db
from ble2json.device import sensordata, ruuvi5

DELTA = timedelta(seconds=20)
RATE_LIMIT = timedelta(minutes=5).total_seconds()
TEST_DEVS = [
    {
        "name": "example1",
        "address": "00:00:00:00:00:01",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_01",
        "format": "ruuvi5",
    },
    {
        "name": "example2",
        "address": "00:00:00:00:00:02",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_02",
        "format": "ruuvi5",
    },
    {
        "name": "example3",
        "address": "00:00:00:00:00:03",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_03",
        "format": "ruuvi5",
    },
]


def generate(start, end):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(end)
    db_path = "/dev/shm/ble2json.db"
    conn = db.connect(db_path)

    with open(relpath("ble2json/schema.sql")) as f:
        conn.executescript(f.read())

    for dev in TEST_DEVS:
        name = dev["name"]
        addr = dev["address"]
        obj_path = dev["objPath"]
        fmt = dev["format"]

        conn.execute(
            """INSERT INTO device (name, address, objPath, format)
               VALUES (?, ?, ?, ?)
               ON CONFLICT DO NOTHING""",
            (name, addr, obj_path, fmt),
        )

        conn.commit()
        current = start

        while current < end:
            current += DELTA
            time = int(current.timestamp())
            mfdata = generate_test_data(time)
            sensordata.insert(db_path, obj_path, RATE_LIMIT, time, mfdata)

    conn.commit()
    conn.close()


def generate_test_data(time):
    b = struct.pack(
        ruuvi5.FMT,
        5,
        -32767 + time % 65534,
        time % 40000,
        time % 65534,
        -32767 + time % 65534,
        -32767 + time % 65534,
        -32767 + time % 65534,
        time % 65502,
        time % 254,
        time % 65534,
        0,
        0,
        0,
        0,
        0,
        0,
    )

    return {0x0499: b}
