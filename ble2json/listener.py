from threading import Thread
from flask import current_app
from gi.repository import GLib, Gio
from . import db
from .device import insert_rssi, insert_data


def init(app):
    with app.app_context():
        db_path = current_app.config["DB_PATH"]
        thread = Thread(target=listen, args=(db_path,))
        thread.start()


def listen(db_path):
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

        conn = db.connect(db_path)
        user_data = {"db_path": db_path}

        for row in conn.execute("SELECT obj_path FROM device"):
            bus.signal_subscribe(
                None,
                "org.freedesktop.DBus.Properties",
                "PropertiesChanged",
                row["obj_path"],
                None,
                Gio.DBusSignalFlags.NONE,
                callback,
                user_data,
            )

        conn.close()
        loop = GLib.MainLoop()
        loop.run()

    except Exception as e:
        raise SystemExit(e)


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
                insert_rssi(user_data["db_path"], object_path, par["RSSI"])

            if "ManufacturerData" in par:
                insert_data(user_data["db_path"], object_path, par["ManufacturerData"])

    except Exception as e:
        print(e)
