Endpoints
=========

"/"
---

Return all configured devices with their data from the specified time interval.
Accepts parameters "start" and "end", which can be date-times in ISO 8601 format,
or one of the aliases listed below. If only "start" or "end" is present,
the other parameter defaults to UNIX epoch or current time.
With no parameters, return the latest data from each device.

Aliases:
    "epoch" => 1970-01-01T00:00:00Z
    "now"   => current date-time
    "day"   => start of current day
    "week"  => start of current week
    "month" => start of current month
    "year"  => start of current year

Example request:
    GET /?start=2021-02-02T10:10:10Z HTTP/1.1

Response:
    HTTP/1.1 200 OK
    ...
    [
        {
            "address":"CB:98:33:4C:88:4F",
            "name":"example",
            "rssi":-88,
            "sensorData": [
                { ... },
                ...
            ]
        }
        ...
    ]

"/\<name\>"
-------

Return the device with matching name.
Accepts the same parameters as above.

Example request:
    GET /example HTTP/1.1

Response:
    HTTP/1.1 200 OK
    ...
    {
        "address":"CB:98:33:4C:88:4F",
        "name":"example",
        "rssi":-88,
        "sensorData": { 
            ... 
        }
    }



