from . import error


defaults = {
    "ADD_DEVICES": [],
    "CLEANUP_INTERVAL": {"hours": 6},
    "DELETE_DEVICES": [],
    "MAX_AGE": {"weeks": 10},
    "NO_LISTEN": False,
    "PERSISTENT": True,
    "RATE_LIMIT": {"minutes": 5},
    "TEST_DB": False,
}


def load(app):
    try:
        app.config.from_json("config.json", silent=True)
    except:
        app.config.update(defaults)
        return True

    for key in defaults:
        if key not in app.config:
            app.config[key] = defaults[key]

    return False
