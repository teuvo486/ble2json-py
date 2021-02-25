Endpoints
=========

"/"
---

Return all configured devices with their data from the specified time interval.
Accepts parameters "start" and "end", which are date-times in ISO 8601 format,
or alternatively "unixepoch" or "now". If only "start" or "end" is present,
the other parameter defaults to the UNIX epoch or current time. With no parameters, 
return the latest data from each device.

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
            "sensor_data": [
                { ... },
                ...
            ]
        }
        ...
    ]

"/\<name\>"
-------

Return the device and data with matching name.
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
        "sensor_data": { 
            ... 
        }
    }



