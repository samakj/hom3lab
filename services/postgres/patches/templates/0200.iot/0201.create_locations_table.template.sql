CREATE TABLE IF NOT EXISTS {db.tables.locations.schema}.{db.tables.locations.name} (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    tags TEXT[] NOT NULL
);