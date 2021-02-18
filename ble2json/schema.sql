CREATE TABLE IF NOT EXISTS device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    address TEXT UNIQUE NOT NULL,
    obj_path TEXT UNIQUE NOT NULL,
    rssi INTEGER
);

CREATE TABLE IF NOT EXISTS data (
    device_id INTEGER NOT NULL,
    time INTEGER NOT NULL,
    temperature REAL,
    humidity REAL,
    pressure INTEGER,
    acceleration_x REAL,
    acceleration_y REAL,
    acceleration_z REAL,
    voltage REAL,
    tx_power INTEGER,
    movement_counter INTEGER,
    measurement_sequence INTEGER,
    FOREIGN KEY (device_id) REFERENCES device (id)
);
