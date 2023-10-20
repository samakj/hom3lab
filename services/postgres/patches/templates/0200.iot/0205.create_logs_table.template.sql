CREATE TABLE IF NOT EXISTS {db.tables.logs.schema}.{db.tables.logs.name} (
    id        SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    device_id INTEGER REFERENCES {db.tables.devices.schema}.{db.tables.devices.name}(id) NOT NULL,
    level     TEXT NOT NULL,
    message   TEXT NOT NULL
);