CREATE TABLE IF NOT EXISTS {db.tables.metrics.schema}.{db.tables.metrics.name} (
    id           SERIAL PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    abbreviation TEXT NOT NULL UNIQUE,
    unit         TEXT
);