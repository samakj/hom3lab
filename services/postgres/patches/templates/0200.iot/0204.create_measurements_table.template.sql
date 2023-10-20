CREATE TABLE IF NOT EXISTS {db.tables.measurements.schema}.{db.tables.measurements.name} (
    id          SERIAL PRIMARY KEY,
    timestamp   TIMESTAMP NOT NULL,
    device_id   INTEGER REFERENCES {db.tables.devices.schema}.{db.tables.devices.name}(id) NOT NULL,
    location_id INTEGER REFERENCES {db.tables.locations.schema}.{db.tables.locations.name}(id) NOT NULL,
    metric_id   INTEGER REFERENCES {db.tables.metrics.schema}.{db.tables.metrics.name}(id) NOT NULL,
    tags        TEXT[],
    value       JSONB NOT NULL
);