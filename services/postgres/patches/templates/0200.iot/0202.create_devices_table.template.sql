CREATE TABLE IF NOT EXISTS {db.tables.devices.schema}.{db.tables.devices.name} (
    id          SERIAL PRIMARY KEY,
    mac         TEXT NOT NULL UNIQUE,
    location_id INTEGER REFERENCES {db.tables.locations.schema}.{db.tables.locations.name}(id) NOT NULL
);