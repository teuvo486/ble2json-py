import json
from json.decoder import JSONDecodeError
from queue import SimpleQueue
from threading import Thread
from gi.repository import GLib, Gio

CONFIG_PATH = "/usr/var/ble2json-instance/config.json"


def prompt():
    while True:
        i = input("Would you like to scan for BLE devices now? [y/n]\n> ").lower()
        if i == "y" or i == "yes":
            run()
            break
        elif i == "n" or i == "no":
            break
        else:
            pass


def run():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        d = {}

    if not d.get("ADD_DEVICES"):
        d["ADD_DEVICES"] = []

    try:
        scan(d["ADD_DEVICES"])
    except KeyboardInterrupt:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4)
            print("")


def scan(devs):
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
        raise SystemExit("BlueZ is not installed!")

    q = SimpleQueue()

    user_data = {"q": q}

    Thread(target=listen, args=(user_data,), daemon=True).start()

    print("Scanning... [CTRL-C to save and quit]")

    while True:
        dev = q.get()
        fmt = dev.get("format")
        addr = dev.get("address")

        if not exists(devs, addr):
            print(f"Found new device of type {fmt} at {addr}")
            i = input("Enter name for this device [s to skip]\n> ").lower()

            if not i == "s":
                dev["name"] = i
                devs.append(dev)
                print("Device added")


def exists(devs, addr):
    for d in devs:
        if d.get("address") == addr:
            return True

    return False


def listen(user_data):
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

    bus.signal_subscribe(
        "org.bluez",
        "org.freedesktop.DBus.ObjectManager",
        "InterfacesAdded",
        None,
        None,
        Gio.DBusSignalFlags.NONE,
        callback1,
        user_data,
    )

    bus.signal_subscribe(
        "org.bluez",
        "org.freedesktop.DBus.Properties",
        "PropertiesChanged",
        None,
        None,
        Gio.DBusSignalFlags.NONE,
        callback2,
        user_data,
    )

    loop = GLib.MainLoop()
    loop.run()


def callback1(
    connection,
    sender_name,
    object_path,
    interface_name,
    signal_name,
    parameters,
    user_data,
):
    for p in parameters:
        if "org.bluez.Device1" in p:
            d1 = p["org.bluez.Device1"]

            if "ManufacturerData" in d1:
                mfdata = d1["ManufacturerData"]

                if 0x499 in mfdata:
                    addr = d1["Address"]
                    put_dev(user_data["q"], mfdata[0x499], addr)


def callback2(
    connection,
    sender_name,
    object_path,
    interface_name,
    signal_name,
    parameters,
    user_data,
):
    for p in parameters:
        if "ManufacturerData" in p:
            mfdata = p["ManufacturerData"]

            if 0x499 in mfdata:
                addr = object_path[-17:].replace("_", ":")
                put_dev(user_data["q"], mfdata[0x499], addr)


def put_dev(q, rawdata, addr):
    if len(rawdata) == 14 and rawdata[0] == 3:
        q.put({"format": "ruuvi3", "address": addr})
    elif len(rawdata) == 24 and rawdata[0] == 5:
        q.put({"format": "ruuvi5", "address": addr})


if __name__ == "__main__":
    prompt()
