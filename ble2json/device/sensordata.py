from flask import abort
from ble2json import db
from ble2json.device import ruuvi3, ruuvi5
from ble2json.timeutil import get_datetimes

VALID_COLS = [
    "temperature",
    "humidity",
    "pressure",
    "accelerationX",
    "accelerationY",
    "accelerationZ",
    "voltage",
    "txPower",
    "movementCounter",
    "measurementSequence",
]

MAX_LEN = len("".join(VALID_COLS)) + len(VALID_COLS) - 1


def validate_columns(cols):
    if len(cols) > MAX_LEN:
        abort(400)

    for col in cols.split(","):
        if col not in VALID_COLS:
            abort(400)

    return cols


def parse_mfdata(mfdata):
    if 0x0499 in mfdata:
        rawdata = mfdata[0x499]

        if len(rawdata) == 14 and rawdata[0] == 3:
            return ruuvi3.from_bytes(bytes(rawdata))
        elif len(rawdata) == 24 and rawdata[0] == 5:
            return ruuvi5.from_bytes(bytes(rawdata))

        raise Exception("Unrecognized data format!")

    else:
        raise Exception("Unrecognized manufacturer id!")


def insert(db_path, obj_path, rate_limit, time, mfdata):
    conn = db.connect(db_path)

    latest = (
        conn.execute(
            """SELECT MAX(time) as time FROM data WHERE deviceId = 
               (SELECT id FROM device WHERE objPath = ?)""",
            (obj_path,),
        )
        .fetchone()
        .get("time")
    )

    if not latest:
        latest = 0

    if time - latest >= rate_limit:
        data = parse_mfdata(mfdata)

        conn.execute(
            """INSERT INTO data
               VALUES ((SELECT id FROM device WHERE objPath = ?), 
               ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                obj_path,
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
            ),
        )

        conn.commit()

    conn.close()


def get(dev_id, fmt, start, end, cols):
    mod = get_mod(fmt)

    print(cols)

    if not cols:
        cols = mod.COLS

    if not start and not end:
        return get_latest(dev_id, cols)

    start, end = get_datetimes(start, end)

    return get_interval(dev_id, start, end, cols)


def get_mod(fmt):
    if fmt == "ruuvi3":
        return ruuvi3
    elif fmt == "ruuvi5":
        return ruuvi5

    raise Exception("Invalid data format!")


def get_latest(dev_id, validate_me):
    conn = db.get_conn()

    cols = validate_columns(validate_me)

    return conn.execute(
        f"""SELECT
            strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
            {cols}
            FROM data WHERE data.deviceId = ?
            AND data.time = (
                SELECT MAX(data.time)
                FROM data WHERE data.deviceId = ?
            )""",
        (dev_id, dev_id),
    ).fetchone()


def get_interval(dev_id, start, end, validate_me):
    conn = db.get_conn()

    cols = validate_columns(validate_me)

    return conn.execute(
        f"""SELECT
            strftime('%Y-%m-%dT%H:%M:%SZ', time, "unixepoch") as time,
            {cols}
            FROM data WHERE data.deviceId = ?
            AND data.time >= strftime("%s", ?)
            AND data.time <= strftime("%s", ?)
            ORDER BY data.time""",
        (dev_id, start, end),
    ).fetchall()
