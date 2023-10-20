CREATE TABLE IF NOT EXISTS {db.tables.users.schema}.{db.tables.users.name} (
    id             SERIAL PRIMARY KEY,
    username       TEXT NOT NULL UNIQUE,
    password       TEXT NOT NULL,
    name           TEXT NOT NULL,
    scopes         TEXT[]
);