Configuration
=============

The config.json file should be placed in the 
[Flask instance folder](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders),
which defaults to `/usr/var/ble2json-instance`.
All keys are case-sensitive.

"ADD_DEVICES": [object]
-------------------

BLE devices to be added into the database. An array of objects with required "name", 
"address", and "format" keys; "name" can be any string except "errors", "address" must be a colon-separated
MAC address, and "format" can be "ruuvi3" or "ruuvi5" (as of v0.2.0). Entries with a 
duplicate address update the existing device's name and format. Duplicate names are a fatal
error. Defaults to `[]`.

"CLEANUP_INTERVAL": object
-----------------------

How long the clean-up thread should wait between runs.
An object that gets converted into a 
[datetime.timedelta](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta) 
instance; see the link for allowed keys. Defaults to `{"hours": 6}`. 

"DELETE_DEVICES": [string]
-------------------

BLE devices to be deleted from the database. An array of strings corresponding to the 
address of an existing device. Defaults to `[]`.

"MAX_AGE": object
-----------------

Clean up all data points older than this. Same format as in `CLEANUP_INTERVAL` and `RATE_LIMIT`.
Defaults to `{"weeks": 10}`. If total duration is equal to 0, the clean-up thread will not run.

"NO_LISTEN": boolean
--------------------

Do not run the listener thread (for testing purposes). Defaults to `false`.

"PERSISTENT": boolean
---------------------

If `true`, write the db file in the instance folder, where it persists between reboots. 
If `false`, write it in the temporary folder `/run/ble2json`. Defaults to `false`.

"RATE_LIMIT": object
-----------------

Minimum time between data points from the same device.
Same format as in `CLEANUP_INTERVAL` and `MAX_AGE`. Defaults to `{"minutes": 5}`.

"TEST_DB": boolean
------------------

Populate the database with test data; skip adding and deleting devices.
Defaults to `false`.

Full config example:
===================

    {
        "ADD_DEVICES": [
            { 
                "name": "example1",
                "address": "00:00:00:00:00:01",
                "format": "ruuvi5"
            },
            { 
                "name": "example2",
                "address": "00:00:00:00:00:02",
                "format": "ruuvi5"
            }
        ],

        "CLEANUP_INTERVAL": {
            "hours": 12
        },

        "DELETE_DEVICES": [
            "00:00:00:00:00:00",
            "FF:FF:FF:FF:FF:FF"
        ],
        
        "MAX_AGE": {
            "weeks": 52
        },
        
        "NO_LISTEN": false,
        
        "PERSISTENT": true,
        
        "RATE_LIMIT": {
            "minutes": 10
        },
        
        "TEST_DB": false,
    }
