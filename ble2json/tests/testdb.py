import struct
from datetime import date, datetime, timedelta
from ble2json import db
from ble2json.device import ruuvi5

NAME = "example1"
ADDR = "00:00:00:00:00:01"
OBJ_PATH = "/org/bluez/hci0/dev_00_00_00_00_00_01"
FMT = "ruuvi5"
START = int((datetime.now() - timedelta(days=365)).timestamp())
END = int(datetime.now().timestamp())
DELTA = int(timedelta(minutes=5).total_seconds())


def generate(db_path):
    conn = db.connect(db_path)

    conn.execute(
        """INSERT INTO device (name, address, objPath, format)
           VALUES (?, ?, ?, ?)
           ON CONFLICT DO NOTHING""",
        (NAME, ADDR, OBJ_PATH, FMT),
    )

    conn.commit()

    conn.executemany(
        """INSERT INTO data
           VALUES ((SELECT id FROM device WHERE objPath = ?), 
           ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        generator(),
    )

    conn.commit()
    conn.close()


def generator():
    for t in range(START, END, DELTA):
        yield test_data(t)


def test_data(time):
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

    data = ruuvi5.from_bytes(b)

    return (
        OBJ_PATH,
        time,
        data.get("temperature"),
        data.get("humidity"),
        data.get("pressure"),
        data.get("accelerationX"),
        data.get("accelerationY"),
        data.get("accelerationZ"),
        data.get("voltage"),
        data.get("txPower"),
        data.get("movementCounter"),
        data.get("measurementSequence"),
    )
