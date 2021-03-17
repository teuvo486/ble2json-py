Configuration
=============

The config.json file should be placed in the 
[Flask instance folder](https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders).
All keys are case-sensitive.

"CLEANUP_INTERVAL": object
-----------------------

How long the clean-up thread should wait between runs.
An object that gets converted into a 
[datetime.timedelta](https://docs.python.org/3.8/library/datetime.html#datetime.timedelta) 
instance; see the link for allowed keys. Defaults to `{"hours": 1}`. 

"DEVICES": [object]
-------------------

Devices to add into the database. Array of objects with "name", "address", and "format" keys.

"MAX_AGE": object
-----------------

Clean up all data points older than this. Same format as in `CLEANUP_INTERVAL` and `RATE_LIMIT`.
Defaults to `{"weeks": 4}`. If total duration is equal to 0, the clean-up thread will not run.

"NO_LISTEN": boolean
--------------------

Do not run the listener thread (for testing purposes). Defaults to `false`.

"PERSISTENT": boolean
---------------------

If `true`, write the db file in the instance folder, where it persists between reboots. 
If `false`, write it in temporary storage under `/dev/shm`. Defaults to `false`.

"RATE_LIMIT": object
-----------------

Minimum time between data points from the same device.
Same format as in `CLEANUP_INTERVAL` and `MAX_AGE`. Defaults to `{"minutes": 5}`.

Full config example:
===================

    {
        "CLEANUP_INTERVAL": {
            "days": 1
        },
        
        "DEVICES": [
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
        
        "MAX_AGE": {
            "weeks": 52
        },
        
        "NO_LISTEN": false,
        
        "PERSISTENT": true,
        
        "RATE_LIMIT": {
            "minutes": 30
        }
    }
