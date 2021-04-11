import re
from copy import deepcopy
from . import error

DEFAULTS = {
    "ADD_DEVICES": [],
    "CLEANUP_INTERVAL": {"hours": 6},
    "DELETE_DEVICES": [],
    "MAX_AGE": {"weeks": 10},
    "NO_LISTEN": False,
    "PERSISTENT": True,
    "RATE_LIMIT": {"minutes": 5},
    "TEST_DB": False,
}


def set_db_path(app):
    if app.config.get("PERSISTENT") == True:
        app.config["DB_PATH"] = app.instance_path + "/ble2json.db"
    else:
        app.config["DB_PATH"] = "/run/ble2json/ble2json.db"


def load(app):
    try:
        app.config.from_json("config.json", silent=True)
        copied = deepcopy(DEFAULTS)
        copied.update(app.config)
        app.config = copied
        set_db_path(app)
        return True
    except:
        app.config.update(DEFAULTS)
        set_db_path(app)
        return False


def validate(load_ok, app):
    with app.app_context():
        if not load_ok:
            error.log(500, "Config Error", "Invalid JSON syntax in config file")
            return False

        for k in DEFAULTS:
            if not isinstance(app.config[k], DEFAULTS[k].__class__):
                error.log(500, "Config Error", f"Key '{k}' has an invalid value")
                return False

        for d in app.config["ADD_DEVICES"]:
            if (
                not valid_name(d.get("name"))
                or not valid_mac(d.get("address"))
                or not valid_fmt(d.get("format"))
            ):
                return False

        for a in app.config["DELETE_DEVICES"]:
            if not valid_mac(a):
                return False

    return True


def valid_name(name):
    if isinstance(name, str) and name != "errors":
        return True

    error.log(500, "Config Error", f"Invalid device name '{name}'")


def valid_mac(addr):
    if isinstance(addr, str) and re.match("^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", addr):
        return True

    error.log(500, "Config Error", f"Invalid MAC address '{addr}'")


def valid_fmt(fmt):
    if fmt == "ruuvi3" or fmt == "ruuvi5":
        return True

    error.log(500, "Config Error", f"Invalid format '{fmt}'")
