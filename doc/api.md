Endpoints
=========

/
---

Return the specified columns from the specified time interval from each device.
With no parameters, return the latest values of all columns from each device.

**Parameters:**

"start": Date-time string of the format YYYY-MM-DDThh:mm:ss(.sss)Z, or a time alias (see below). 
Defaults to "epoch" if "end" is set.

"end": Same format as above. Defaults to "now" if "start" is set.

"columns": Comma-separated list of valid column names, excluding "time", 
which is always included in the output.

**Time aliases:**

"epoch": 1970-01-01T00:00:00Z

"now": current time (UTC)

"day": start of current day (UTC)

"week": start of current week (UTC)

"month": start of current month (UTC)

"year": start of current year (UTC)

**Example request:**

    GET /?start=week&columns=temperature,humidity HTTP/1.1

**Response:**

    HTTP/1.1 200 OK
    ...
    [
        {
            "address": "00:00:00:00:00:01",
            "name": "example1",
            "rssi": -88,
            "sensorData": [
                {
                    "humidity": 38.0, 
                    "temperature": -105.755, 
                    "time": "2021-01-13T22:00:00Z"
                },
                ...
            ]
        }
        ...
    ]

/\<name\>
-----------

Return the device with matching name.
Accepts the same parameters as above.

**Example request:**

    GET /example1?columns=temperature,humidity HTTP/1.1

**Response:**

    HTTP/1.1 200 OK
    ...
    {
        "address": "00:00:00:00:00:01",
        "name": "example1", 
        "rssi": null, 
        "sensorData": {
            "humidity": 38.0, 
            "temperature": -105.755, 
            "time": "2021-01-13T22:00:00Z"
        }
    }


/errors
--------

Return all logged errors from the database.


**Example request:**

    GET /errors HTTP/1.1

**Response:**

    HTTP/1.1 200 OK
    ...
    [
        {
            "code":500,
            "description":"Invalid JSON syntax in config file",
            "name":"Config Error",
            "time":"2021-04-10T14:54:23Z"
        }
        ...
    ]

