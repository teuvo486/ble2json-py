from time import time
from threading import Thread
from flask import current_app
from gi.repository import GLib, Gio
from . import db, error
from .device import update_rssi, sensordata
from .timeutil import get_timedelta


def init(app):
    with app.app_context():
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)

            names = bus.call_sync(
                "org.freedesktop.DBus",
                "/org/freedesktop/DBus",
                "org.freedesktop.DBus",
                "ListNames",
                None,
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None,
            )

            if "org.bluez" not in names[0]:
                error.log(
                    500,
                    "BlueZ Error",
                    "The BlueZ service is unreachable on the system bus.",
                )
                return None

            user_data = {
                "db_path": current_app.config["DB_PATH"],
                "rate_limit": get_timedelta(
                    current_app.config.get("RATE_LIMIT")
                ).total_seconds(),
            }

            thread = Thread(target=listen, args=(user_data,))
            thread.start()

        except GLib.Error:
            error.log(500, "DBus Error", "Could not connect to the system bus.")


def listen(user_data):
    try:
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)

        bus.call_sync(
            "org.bluez",
            "/org/bluez/hci0",
            "org.bluez.Adapter1",
            "StartDiscovery",
            None,
            None,
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )

        conn = db.connect(user_data["db_path"])

        for row in conn.execute("SELECT objPath FROM device"):
            bus.signal_subscribe(
                "org.bluez",
                "org.freedesktop.DBus.Properties",
                "PropertiesChanged",
                row["objPath"],
                None,
                Gio.DBusSignalFlags.NONE,
                callback,
                user_data,
            )

        conn.close()
        loop = GLib.MainLoop()
        loop.run()

    except GLib.Error:
        error.log_no_context(
            user_data["db_path"],
            500,
            "DBus Error",
            "Connection to the system bus was lost.",
        )


def callback(
    connection,
    sender_name,
    object_path,
    interface_name,
    signal_name,
    parameters,
    user_data,
):
    try:
        for par in parameters:
            if "RSSI" in par:
                update_rssi(user_data["db_path"], object_path, par["RSSI"])

            if "ManufacturerData" in par:
                sensordata.insert(
                    user_data["db_path"],
                    object_path,
                    user_data["rate_limit"],
                    int(time()),
                    par["ManufacturerData"],
                )

    except Exception as e:
        print(e)
