DROP TABLE IF EXISTS oil_slicks;

CREATE TABLE oil_slicks (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    lat REAL,
    lng REAL,
    area REAL,
    confidence REAL
);

DROP TABLE IF EXISTS weather_data;

CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oil_slick_id TEXT,
    timestamp TEXT,
    wind_speed REAL,
    wind_dir REAL,
    current_speed REAL,
    current_dir REAL,
    wave_height REAL,
    water_temp REAL,
    FOREIGN KEY(oil_slick_id) REFERENCES oil_slicks(id)
);
