import struct
import sqlite3
from os.path import relpath
from datetime import datetime, timedelta
from ble2json import db
from ble2json.device import ruuvi5

FMT = ">BhHHhhhHBHBBBBBB"
start = datetime(2021, 1, 1)
end = datetime(2021, 2, 1)
delta = timedelta(seconds=20)
test_devs = [
    { 
        "name": "example1",
        "address": "00:00:00:00:00:01",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_01",
        "format": "ruuvi5"
    },
    { 
        "name": "example2",
        "address": "00:00:00:00:00:02",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_02",
        "format": "ruuvi5"
    },
    { 
        "name": "example3",
        "address": "00:00:00:00:00:03",
        "objPath": "/org/bluez/hci0/dev_00_00_00_00_00_03",
        "format": "ruuvi5"
    }
]


def generate():
    conn = db.connect("/dev/shm/ble2json.db")

    with open(relpath("ble2json/schema.sql")) as f:
        conn.executescript(f.read())

    for dev in test_devs:
        conn.execute(
            """INSERT INTO device (name, address, objPath, format)
               VALUES (?, ?, ?, ?)
               ON CONFLICT DO NOTHING""",
            (dev["name"], dev["address"], dev["objPath"], dev["format"]),
        )
        
        conn.commit()
        
        dev_id = conn.execute(
        "SELECT id FROM device WHERE objPath = ?", (dev["objPath"],)
        ).fetchone()["id"]

        current = start

        while current < end:
            current += delta
            
            time = int(current.timestamp())
            
            data = generate_test_data(time)
        
            cols = (dev_id, time) + data
            
            conn.execute(
                """INSERT INTO data (
                        deviceId,
                        time,
                        temperature,
                        humidity,
                        pressure,
                        accelerationX,
                        accelerationY,
                        accelerationZ,
                        voltage,
                        txPower,
                        movementCounter,
                        measurementSequence
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                cols,
            )
        
    conn.commit()
    conn.close()
    

def generate_test_data(time):
    b = struct.pack(
        FMT,
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
    
    return ruuvi5.from_bytes(b)

