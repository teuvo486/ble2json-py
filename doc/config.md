Configuration
=============

The config.json file should be placed in the 
[Flask instance folder](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders).
All keys are case-sensitive.

"DEVICES": [object]
-------------------

Array of objects with "name", "address", and "format" keys.

Example:

    "DEVICES": [
        {
            "name": "example",
            "address": "CB:98:33:4C:88:4F",
            "format": "ruuvi5"
        }
    ]

"PERSISTENT": boolean
---------------------

If `true`, write the db file in the instance folder. If `false`, write it under `/dev/shm/`.
Defaults to `false`.

"MAX_AGE": object
-----------------

Clean up all data older than this. An object that gets converted into a [datetime.timedelta](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta)
instance. See the link for allowed keys. If empty or unset, the clean-up thread will not run.

Example:

    "MAX_AGE": {
        "weeks": 1,
        "hours": 5
    }

"CLEANUP_DELAY": object
-----------------------

How often the clean-up thread should run. Same format as in MAX_AGE. Defaults to `{"hours": 1}`.

"NO_LISTEN": boolean
--------------------

Do not run the listener thread (for testing purposes). Defaults to `false`.

