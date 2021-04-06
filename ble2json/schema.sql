CREATE TABLE IF NOT EXISTS device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    address TEXT UNIQUE NOT NULL,
    objPath TEXT UNIQUE NOT NULL,
    format TEXT NOT NULL,
    rssi INTEGER
);

CREATE TABLE IF NOT EXISTS data (
    deviceId INTEGER NOT NULL,
    time INTEGER NOT NULL,
    temperature REAL,
    humidity REAL,
    pressure INTEGER,
    accelerationX REAL,
    accelerationY REAL,
    accelerationZ REAL,
    voltage REAL,
    txPower INTEGER,
    movementCounter INTEGER,
    measurementSequence INTEGER,
    FOREIGN KEY (deviceId) REFERENCES device (id) ON DELETE CASCADE
);
